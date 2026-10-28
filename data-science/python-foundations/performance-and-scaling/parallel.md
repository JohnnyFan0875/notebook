[Python Foundations](../README.md) › [效能與擴展](README.md) › 平行運算

# 平行運算：multiprocessing 與 Dask (Parallel Computing)

單核程式已經量測、向量化過（見 [Efficient Python](efficient-python.md)）仍然太慢或資料放不進記憶體時，才考慮平行化。先判斷工作是 **CPU-bound** 還是 **I/O-bound**，再選工具。

## 選工具

| 情境 | 工具 | 原因 |
| --- | --- | --- |
| I/O-bound：下載、API 呼叫、讀很多小檔 | `ThreadPoolExecutor`、`asyncio` | 等待 I/O 時 GIL 會釋放，thread 就夠 |
| CPU-bound 純 Python：同一函式套到很多輸入 | `ProcessPoolExecutor` / `multiprocessing.Pool`、`joblib` | 多個 process 各有自己的 GIL |
| CPU-bound NumPy / pandas 運算 | 先確認 BLAS 是否已經多執行緒；Dask | NumPy 的矩陣運算常已用滿多核 |
| 比記憶體大的 array / DataFrame | Dask、[Polars](polars.md) streaming | 分塊、延遲計算 |
| 多個外部工具串成的流程 | Snakemake / Nextflow | 斷點續跑、HPC 排程，見 [工作流引擎](../../../computing/workflow-engines/README.md) |
| 多台機器、TB 級資料 | Dask distributed、Spark | 見 [分散式處理](../../data-engineering/scalable-processing-and-out-of-core.md) |

### GIL (Global Interpreter Lock)

CPython 同一時間只讓一個 thread 執行 Python bytecode，所以**純 Python 的 CPU 運算開 thread 不會變快**。例外：I/O 等待，以及 NumPy、pandas 等 C 擴充在計算時會釋放 GIL。Python 3.13 起有實驗性的 free-threaded 版本（`python3.13t`）可關閉 GIL，但套件支援仍在進行中。

## `concurrent.futures`：首選的高階介面

```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import os

def count_reads(path):                     # 必須定義在模組頂層，子 process 才能 import（pickle）
    ...

if __name__ == "__main__":                 # Windows / macOS 用 spawn 啟動，一定要有這個保護
    files = sorted(Path("fastq").glob("*.fastq.gz"))
    n = int(os.environ.get("SLURM_CPUS_PER_TASK", os.cpu_count()))   # HPC 上用實際分配的核心數

    with ProcessPoolExecutor(max_workers=n) as ex:
        results = list(ex.map(count_reads, files, chunksize=4))       # 保持輸入順序

    with ThreadPoolExecutor(max_workers=8) as ex:                     # I/O-bound：下載
        futures = {ex.submit(download, url): url for url in urls}
        for fut in as_completed(futures):                             # 誰先完成先處理
            url = futures[fut]
            try:
                fut.result()
            except Exception as e:
                log.error("%s failed: %s", url, e)
```

`multiprocessing.Pool` 是較舊的等價介面：

```python
import multiprocessing as mp

def square(x):
    return x * x

if __name__ == "__main__":
    with mp.Pool(processes=4) as pool:
        pool.map(square, [1, 2, 3, 4, 5])          # [1, 4, 9, 16, 25]
        pool.starmap(pow, [(2, 3), (3, 2)])        # 多個參數：[8, 9]

    p1 = mp.Process(target=print, args=("Hello",))   # 不同任務各開一個 process（較少用）
    p1.start(); p1.join()
```

| | `Pool.map` / `Executor.map` | `Process` |
| --- | --- | --- |
| 用途 | 同一函式套到很多輸入 | 不同任務各自執行 |
| 管理 | 自動分配與回收 | 手動 `start()` / `join()`、用 `Queue` 溝通 |

`joblib`（scikit-learn 內部使用）寫法更短，並對 NumPy 大陣列有記憶體映射優化：

```python
from joblib import Parallel, delayed
Parallel(n_jobs=-1)(delayed(pow)(i, 2) for i in range(5))   # [0, 1, 4, 9, 16]；-1 = 所有核心
```

### 常見陷阱

| 陷阱 | 說明 / 處理 |
| --- | --- |
| 少了 `if __name__ == "__main__"` | Windows / macOS 子 process 會重新執行整個腳本，無限產生 process |
| 函式是 lambda 或定義在 notebook / 函式內 | 無法 pickle；放到 `.py` 模組頂層再 import。notebook 中可改用 `joblib` |
| 任務太小 | 啟動 process 與傳輸資料的成本 > 計算本身；用 `chunksize` 或合併任務 |
| 傳遞大型物件 | 每個 worker 都複製一份；改傳檔案路徑，讓 worker 自己讀 |
| 超額訂閱 (oversubscription) | 8 個 process × 每個 NumPy 再開 8 個 BLAS thread = 64 個 thread 搶 8 核；設 `OMP_NUM_THREADS=1` 或用 `threadpoolctl` |
| 每個 worker 亂數相同 | fork 時複製了同一個亂數狀態；用 `SeedSequence.spawn` 給每個任務獨立的種子 |

```python
import numpy as np

def simulate(seed_seq):
    rng = np.random.default_rng(seed_seq)          # 每個任務獨立、可重現的亂數串流
    return rng.normal(size=1000).mean()

seeds = np.random.SeedSequence(42).spawn(100)      # 從一個主種子衍生 100 個互不重疊的種子
with ProcessPoolExecutor() as ex:
    estimates = list(ex.map(simulate, seeds))      # 不論 worker 數、執行順序，結果都相同
```

## Dask

Dask 把工作拆成很多小任務、組成任務圖 (task graph)，交給 scheduler 執行；呼叫 `.compute()` 前都只是**延遲 (lazy)** 的計畫。

| collection | 類似 | 適用 |
| --- | --- | --- |
| `dask.array` | NumPy | 大型多維陣列（影像、模擬、表現矩陣） |
| `dask.dataframe` | pandas | 比記憶體大的表格、很多 CSV / Parquet 檔 |
| `dask.bag` | Python list | 半結構化資料（JSON 記錄、文字） |
| `dask.delayed` | 一般函式 | 自訂的多步驟流程 |

```python
import dask
import dask.array as da
import dask.bag as db
import dask.dataframe as dd

# array：切成 chunks，延後運算
x = da.ones((4000, 6000), chunks=(1000, 2000))     # 4 × 3 = 12 個區塊
total = x.sum()                                    # 只是計畫
total.compute()                                    # 24000000.0：真正執行

# dataframe：很多檔案當成一個表，API 與 pandas 幾乎相同
df = dd.read_parquet("variants/*.parquet")         # 或 dd.read_csv("data/*.csv")
af = df[df["qual"] > 30].groupby("chrom")["af"].mean()
af.compute()                                       # 回傳 pandas Series

# bag：半結構化資料
db.from_sequence(["Really good service", "Second time", "Great"], npartitions=2).map(len).compute()
# [19, 11, 5]

# delayed：自訂函式組成的流程
@dask.delayed
def load(path): ...
@dask.delayed
def qc(data): ...
reports = [qc(load(p)) for p in paths]
dask.compute(*reports)                             # 所有獨立任務平行執行
```

### chunk 大小與 scheduler

| chunk 太大 | chunk 太小 |
| --- | --- |
| 平行度不足、單一任務記憶體壓力高 | 排程成本 > 計算，任務太碎 |

經驗上每個 chunk 約 100 MB 左右；Parquet 檔的 row group 也影響 dataframe 的分割。

| scheduler | 預設用於 | 適合 |
| --- | --- | --- |
| `threads` | array、dataframe、delayed | 底層是 NumPy / pandas（會釋放 GIL） |
| `processes` | bag | 純 Python 物件處理 |
| `distributed` | — | 有 dashboard 可看進度與記憶體；也能擴展到多台機器 |

```python
x.compute(scheduler="processes")

from dask.distributed import Client
client = Client(n_workers=4, threads_per_worker=2, memory_limit="4GB")
client.dashboard_link                              # 瀏覽器開啟，看任務圖與記憶體使用
```

### Dask 的陷阱

| 陷阱 | 說明 |
| --- | --- |
| 忘記 `.compute()` | 拿到的是 lazy 物件，不是結果 |
| 多次 `.compute()` 重算同一段 | 用 `dask.compute(a, b)` 一次算，或 `.persist()` 把中間結果留在記憶體 |
| 小資料也用 Dask | 放得進記憶體的資料，pandas / Polars 通常更快 |
| 需要全域排序、大量 shuffle 的操作 | `set_index`、未排序的 `merge` 很昂貴 |
| 當成任何 Python 程式的自動加速器 | 它只是排程器；每個任務本身仍要寫得有效率 |

## multiprocessing vs Dask

| | `multiprocessing` / `concurrent.futures` | Dask |
| --- | --- | --- |
| 抽象層次 | 你自己分派函式到 process | 描述資料或任務依賴，scheduler 安排 |
| 適合 | 同一函式套到很多獨立輸入 | 分塊陣列、比記憶體大的表格、有依賴關係的流程 |
| 記憶體外資料 | 不支援，要自己分塊 | 內建 |
| 擴展到多機 | 否 | 是（distributed） |
