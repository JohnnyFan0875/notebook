[Data Science](../README.md) › [Data Engineering](README.md) › 超出記憶體的處理

# 超出記憶體的處理 (Scalable Processing and Out-of-Core Workflows)

很多資料流程的第一個瓶頸不是演算法，而是資料放不進記憶體。超出 RAM 後作業系統會把資料換到磁碟 (swap)，速度慢幾個數量級，甚至直接崩潰。解法不是硬撐，而是改變資料被讀取與計算的方式：讓資料主要留在磁碟，每次只處理一部分。

## 先判斷要不要處理

| 情況 | 做法 |
| --- | --- |
| 資料 < RAM 的 1/3–1/2 | 先縮 dtype、只讀需要的欄，通常就夠，見 [記憶體與儲存格式](../python-foundations/pandas/memory-and-storage.md) |
| 資料接近或大於 RAM，但單機磁碟放得下 | 本篇：分塊處理、out-of-core 工具（DuckDB、Polars streaming、Arrow） |
| 單機磁碟或運算都不夠、需要多機平行 | [Spark](spark.md)、[sparklyr](sparklyr.md)、[Spark 處理基因體資料](spark-for-genomics.md) |

> 很多「大資料問題」其實是重複讀寫磁碟、過早把大物件載入記憶體、或合併步驟設計不佳。先 benchmark，分清楚瓶頸在 I/O、解析還是計算。

## 兩種策略

| 策略 | 概念 | 適合 | 限制 |
| --- | --- | --- | --- |
| 磁碟為底的資料結構 (disk-backed / out-of-core) | 資料存在磁碟，需要時才把部分載入；保留類似原生物件的隨機存取 | 形狀固定的大矩陣、需反覆存取不同區塊 | 常要求矩陣形式、不易動態增減列欄、仍需足夠磁碟 |
| 分塊處理 (chunk-wise processing) | 讀一塊 → 計算 → 保留部分結果 → 丟掉 → 讀下一塊 | 以掃描與彙總為主的表格資料 | 需要演算法可拆解與合併 |

| 語言 | 磁碟為底 | 分塊 / 串流 |
| --- | --- | --- |
| Python | `numpy.memmap`、HDF5（`h5py`）、Zarr、AnnData backed mode | `pd.read_csv(chunksize=)`、Polars `scan_*` + streaming、DuckDB、`pyarrow.dataset` |
| R | `bigmemory::big.matrix`、`DelayedArray` / `HDF5Array`（Bioconductor） | `iotools::chunk.apply`、`readr::read_csv_chunked`、`arrow::open_dataset`、`duckdb` |

## 載入與解析是兩件事

匯入資料包含兩個成本：從磁碟取出位元組 (I/O)，以及把位元組解析成原生物件 (parsing)。文字格式（CSV、VCF）的解析常比計算還慢，所以：

- 只讀需要的欄與列（`usecols`、欄式格式的 column pruning、predicate pushdown）
- 大檔轉成 Parquet 等二進位欄式格式後，之後每次讀取都省掉解析
- 高效系統會把 scan、parse、decode、materialize 分成不同層，延後到真正需要時才 materialize

## Split-Apply-Combine

資料能切成互相獨立的分區時：

```
split：切成 partitions / chunks → apply：每塊做相同計算 → combine：合併部分結果
```

R 的 `split()` / `Map()` / `Reduce()`、map-reduce、Spark 的 transformation + action、分塊的 pandas / SQL 聚合都是同一個想法。

### 設計可合併的部分結果

關鍵在 combine：部分結果要保留足夠資訊，且能安全地合併（最好具備結合律、可加性）。

| 統計量 | 每塊保留 | 合併方式 | 可直接拆？ |
| --- | --- | --- | --- |
| 總和、計數 | sum、n | 相加 | 是 |
| 平均數 | sum、n（**不是**各塊平均） | Σsum / Σn | 是 |
| 變異數 | n、mean、M2（Welford / Chan 平行公式） | 公式合併 | 是（注意數值穩定） |
| 最大 / 最小 | max、min | 取 max / min | 是 |
| 線性迴歸 | XᵀX、Xᵀy | 相加後解方程 | 是 |
| 中位數、分位數（精確） | 需要全部資料排序 | — | 否：改用近似（t-digest、Spark `approxQuantile`、DuckDB `approx_quantile`） |
| distinct 數（精確） | 所有 distinct 值 | 聯集 | 記憶體隨基數增加；改用 HyperLogLog（`APPROX_COUNT_DISTINCT`） |

> 各塊平均再平均是常見錯誤：塊大小不同時結果有偏。保留 sum 與 count 才對。

```python
import pandas as pd

# 分塊計算每個基因的平均表現量（長格式：gene, sample, tpm）
sums, counts = {}, {}
for chunk in pd.read_csv("expr_long.csv", chunksize=1_000_000,
                         usecols=["gene", "tpm"], dtype={"gene": "string"}):
    g = chunk.groupby("gene")["tpm"].agg(["sum", "count"])
    for gene, row in g.iterrows():
        sums[gene] = sums.get(gene, 0) + row["sum"]
        counts[gene] = counts.get(gene, 0) + row["count"]
mean_tpm = pd.Series(sums) / pd.Series(counts)

# 同一件事交給 out-of-core 引擎：自動分塊、多執行緒、超出記憶體時寫暫存
import polars as pl
mean_tpm = (pl.scan_csv("expr_long.csv")
              .group_by("gene").agg(pl.col("tpm").mean())
              .collect(engine="streaming"))          # 舊版 polars：collect(streaming=True)

import duckdb
duckdb.sql("SELECT gene, avg(tpm), median(tpm) FROM 'expr_long.csv' GROUP BY gene").df()
```

DuckDB 與 Polars 會自動處理分塊與部分結果合併，連中位數也能算（必要時溢寫到磁碟），通常比手寫分塊迴圈簡單且快，見 [DuckDB 與 Parquet](../databases/duckdb-and-parquet.md)、[Polars](../python-foundations/performance-and-scaling/polars.md)。

```r
# R：bigmemory 的磁碟矩陣（file-backed，跨 session 重用）
library(bigmemory)
x <- read.big.matrix("geno.csv", type = "integer", header = TRUE,
                     backingfile = "geno.bin", descriptorfile = "geno.desc")
colMeans(x[, 1:100])                       # 只把需要的欄載入記憶體
x <- attach.big.matrix("geno.desc")        # 之後直接掛載，不必重新解析

# R：iotools 分塊處理（讀原始位元組 → 解析 → 計算 → 合併）
library(iotools)
partial <- chunk.apply("expr_long_noheader.csv", function(chunk) {   # 檔案無標題列
  df <- dstrsplit(chunk, col_types = c("character", "character", "numeric"), sep = ",")
  rowsum(cbind(sum = df[[3]], n = 1), group = df[[1]])    # 每塊：各基因的 sum 與 n
}, CH.MERGE = rbind)
total <- rowsum(partial, rownames(partial))                # 合併各塊（同一基因可能跨塊）
mean_tpm <- total[, "sum"] / total[, "n"]

# R：arrow 只讀需要的欄並延後計算
library(arrow); library(dplyr)
open_dataset("counts_parquet/") |> filter(tissue == "liver") |>
  group_by(gene) |> summarise(mean_tpm = mean(tpm)) |> collect()
```

## 循序 vs 平行分塊

| | 循序 | 平行 |
| --- | --- | --- |
| 適合 | 資源有限、合併狀態需逐步攜帶、I/O 已是瓶頸 | 各塊獨立、apply 可完全平行、合併成本可控 |
| 注意 | — | 單機 I/O 常先成瓶頸；worker 協調有成本；塊太小時調度 overhead 大於收益 |

chunk size 是重要調參：太大會爆記憶體，太小 overhead 變重。平行化前先確認運算能被安全拆解與合併。Python 平行化見 [平行處理](../python-foundations/performance-and-scaling/parallel.md)，R 見 [R 平行程式設計](../r-foundations/parallel-programming-in-r.md)。

## 選擇

| 情況 | 選擇 |
| --- | --- |
| 形狀固定的大矩陣、要隨機存取、單機磁碟夠 | 磁碟為底的結構（memmap、HDF5、`big.matrix`、AnnData backed） |
| 表格流、以掃描與彙總為主 | DuckDB / Polars / Arrow；需要自訂邏輯才手寫分塊 |
| 需要跨多機或天然平行 | split-apply-combine on [Spark](spark.md) |
