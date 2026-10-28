[Data Science](../README.md) › [Python Foundations](README.md) › 腳本與 CLI

# 腳本與命令列工具 (Scripting & CLI)

把 notebook 裡的操作改成可重跑、可排程、可放進 pipeline 的腳本：入口點、命令列參數、設定檔、路徑與檔案、logging、呼叫外部程式。

## 腳本骨架

```python
#!/usr/bin/env python
"""Filter a count matrix by minimum counts per gene."""
import argparse
import logging
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)

def filter_counts(df: pd.DataFrame, min_count: int) -> pd.DataFrame:   # 純邏輯：可 import、可測試
    return df[df.sum(axis=1) >= min_count]

def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("counts", type=Path, help="input TSV (genes x samples)")
    p.add_argument("-o", "--output", type=Path, required=True)
    p.add_argument("--min-count", type=int, default=10)
    p.add_argument("-v", "--verbose", action="store_true")
    return p.parse_args(argv)

def main(argv=None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    log.info("reading %s", args.counts)
    df = pd.read_csv(args.counts, sep="\t", index_col=0)
    out = filter_counts(df, args.min_count)
    log.info("kept %d / %d genes", len(out), len(df))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, sep="\t")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())          # 回傳值變成 exit code：0 成功，非 0 失敗
```

```bash
python filter_counts.py counts.tsv -o results/filtered.tsv --min-count 20 -v
```

### `if __name__ == "__main__"`

| 執行方式 | `__name__` | `main()` 會跑嗎？ |
| --- | --- | --- |
| `python filter_counts.py` | `"__main__"` | 會 |
| `import filter_counts` | `"filter_counts"` | 不會：只取得函式定義 |

邏輯放函式、入口只負責「何時執行」：同一個檔案可以直接跑、被其他模組 import 重用，也能在測試裡呼叫 `main(["in.tsv", "-o", "out.tsv"])`（`argv` 參數的用途）。

> 讓 exit code 正確（失敗時非 0）很重要：Snakemake、Nextflow、shell 的 `&&` 都靠它判斷步驟是否成功。

## argparse

| 需求 | 寫法 |
| --- | --- |
| 位置參數（必填） | `add_argument("filename")` |
| 選項 + 型別 + 預設 | `add_argument("-p", "--port", type=int, default=5432)` |
| 必填選項 | `required=True` |
| 限定值 | `choices=["fast", "slow"]` |
| 開關 | `action="store_true"` |
| `--x` / `--no-x` 成對開關 | `action=argparse.BooleanOptionalAction`（3.9+） |
| 一次多個值 | `nargs="+"`（≥1）、`nargs="*"`（≥0） |
| 可重複的選項 | `action="append"`：`--tag a --tag b` → `["a", "b"]` |
| 計數（`-vv`） | `action="count", default=0` |
| 路徑 | `type=Path` |
| 子命令 | `add_subparsers(dest="command", required=True)` |
| 在 help 顯示預設值 | `formatter_class=argparse.ArgumentDefaultsHelpFormatter` |

```python
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-m", "--mode", choices=["fast", "slow"], default="fast")
parser.add_argument("-v", "--verbose", action="count", default=0)
parser.add_argument("--samples", nargs="+", help="sample IDs")
parser.add_argument("--tag", action="append")
parser.add_argument("--cache", action=argparse.BooleanOptionalAction, default=True)

sub = parser.add_subparsers(dest="command", required=True)
p_align = sub.add_parser("align", help="align reads")
p_align.add_argument("--threads", type=int, default=4)
p_qc = sub.add_parser("qc", help="run QC")
p_qc.add_argument("bam", type=Path)

args = parser.parse_args(["-vv", "--samples", "S1", "S2", "--no-cache", "align", "--threads", "8"])
args.verbose, args.samples, args.cache, args.command, args.threads
# 2, ['S1', 'S2'], False, 'align', 8
```

參數名稱中的 `-` 會轉成屬性的 `_`（`--min-count` → `args.min_count`）。更複雜的 CLI 可考慮 `typer` 或 `click`（用型別註記 / decorator 定義參數）。安裝後直接當指令用，見 [Python 套件與環境](python-packages.md#pyprojecttoml)的 `[project.scripts]`。

## 設定檔 (Configuration Files)

參數一多（門檻、路徑、參考版本），就從程式中搬到設定檔：換資料不必改程式碼，設定也能跟結果一起存檔。

| 格式 | 註解 | 讀取 | 典型用途 |
| --- | --- | --- | --- |
| TOML | 有 | 標準庫 `tomllib`（3.11+，唯讀） | `pyproject.toml`、Python 工具設定 |
| YAML | 有 | `PyYAML`（`yaml.safe_load`） | Snakemake / nf-core 設定、CI、Kubernetes |
| JSON | **沒有** | 標準庫 `json` | 程式之間交換、API |
| INI | 有限 | 標準庫 `configparser`（值都是字串） | 舊工具 |
| `.py` | 有 | `import config` | 只限個人小專案：混合邏輯與設定，且會執行任意程式碼 |
| `.env` | 有 | `python-dotenv` | 密碼、token（不進 git） |

```toml
# config.toml
[filter]
min_count = 10
min_samples = 3

[reference]
genome = "GRCh38"
gtf = "data/ref/gencode.v46.annotation.gtf"
```

```yaml
# config.yaml
filter:
  min_count: 10
  min_samples: 3
samples: [S1, S2, S3]
use_cache: true          # YAML 1.1 也把 yes/no/on/off 當布林；"NO"（挪威國碼）會變 False，字串要加引號
```

```python
import json, tomllib, yaml, configparser

with open("config.toml", "rb") as f:          # tomllib 要用二進位模式開
    cfg = tomllib.load(f)
cfg["filter"]["min_count"]                    # 10（int）

with open("config.yaml") as f:
    cfg = yaml.safe_load(f)                   # 用 safe_load；yaml.load 可能執行任意物件

with open("config.json") as f:
    cfg = json.load(f)

ini = configparser.ConfigParser()
ini.read("config.ini")
ini["mysql"]["host"], ini.getboolean("other", "use_anonymous")   # 需要時自行轉型
```

| 原則 | 說明 |
| --- | --- |
| 優先序 | 預設值 < 設定檔 < 環境變數 < CLI 參數 |
| 密碼不進設定檔 | 用環境變數或 `.env`（加進 `.gitignore`），雲端用 secret manager |
| 讀入後驗證 | 檢查必要欄位與型別，或用 `pydantic` 定義 schema |
| 跟結果一起存 | 把實際使用的設定寫進輸出資料夾，結果才可追溯 |

```python
import os
from dotenv import load_dotenv          # pip / uv add python-dotenv

load_dotenv()                           # 讀取 .env 到環境變數
token = os.environ["NCBI_API_KEY"]      # 不存在就 KeyError：必要設定應立刻失敗
db_host = os.getenv("DB_HOST", "localhost")   # 可選設定給預設值
```

## 路徑與檔案 (`pathlib`)

用 `pathlib.Path` 取代字串拼接與 `os.path`：跨平台（Windows `\` vs POSIX `/`）且可讀。

```python
from pathlib import Path

root = Path(__file__).resolve().parent      # 腳本所在資料夾（不受執行時的工作目錄影響）
data = root / "data" / "raw"                # 用 / 組合路徑
fq = data / "S1_R1.fastq.gz"

fq.name, fq.stem, fq.suffix, fq.suffixes    # 'S1_R1.fastq.gz', 'S1_R1.fastq', '.gz', ['.fastq', '.gz']
fq.with_suffix(".bam")                      # 只換最後一個副檔名 → S1_R1.fastq.bam
fq.exists(), fq.is_file(), fq.stat().st_size
Path.cwd(), Path.home()

sorted(data.glob("*.fastq.gz"))             # 同一層；結果順序不保證，記得排序
sorted(data.rglob("*_R1*.fastq.gz"))        # 遞迴所有子資料夾（= glob("**/...")）

out = root / "results"
out.mkdir(parents=True, exist_ok=True)      # 等同 mkdir -p
(out / "note.txt").write_text("done\n", encoding="utf-8")
text = (out / "note.txt").read_text(encoding="utf-8")
```

| `os` / `glob` 舊寫法 | `pathlib` |
| --- | --- |
| `os.path.join(a, b)` | `Path(a) / b` |
| `os.path.dirname(os.path.abspath(__file__))` | `Path(__file__).resolve().parent` |
| `os.path.basename(p)` / `splitext` | `p.name` / `p.stem`、`p.suffix` |
| `os.makedirs(p, exist_ok=True)` | `p.mkdir(parents=True, exist_ok=True)` |
| `glob.glob("d/**/*.csv", recursive=True)` | `Path("d").rglob("*.csv")` |
| `os.getcwd()` | `Path.cwd()` |

搬移、複製、刪除整個資料夾用 `shutil`（`shutil.copy2`、`shutil.move`、`shutil.rmtree`）；暫存檔用 `tempfile.TemporaryDirectory()`。

### `open()` 與檔案模式

```python
with open("example.txt", "r", encoding="utf-8") as f:   # with 確保檔案一定關閉
    for line in f:                                       # 逐行讀，不會一次載入整檔
        ...

import gzip
with gzip.open("reads.fastq.gz", "rt") as f:            # 壓縮檔：用文字模式 "rt"
    header = next(f)
```

| 模式 | 讀 | 寫 | 不存在時建立 | 清空原內容 | 起始位置 |
| --- | --- | --- | --- | --- | --- |
| `r` | ✓ | | 否（報錯） | | 開頭 |
| `r+` | ✓ | ✓ | 否（報錯） | | 開頭 |
| `w` | | ✓ | ✓ | **✓** | 開頭 |
| `w+` | ✓ | ✓ | ✓ | **✓** | 開頭 |
| `a` | | ✓ | ✓ | | 結尾 |
| `a+` | ✓ | ✓ | ✓ | | 結尾 |
| `x` | | ✓ | ✓（已存在則報錯） | | 開頭 |

加 `b`（如 `rb`、`wb`）為二進位模式。讀寫混用時游標會移動，需要重讀用 `f.seek(0)`。

> 一律寫明 `encoding="utf-8"`：Windows 上預設編碼可能是 cp950 / cp1252，同一個腳本換平台就讀出亂碼。`w` 會**直接清空**檔案，不想覆蓋既有結果用 `x`。

## Logging

`print` 適合互動除錯；腳本與 pipeline 用 `logging`：有等級、時間戳，可同時輸出到螢幕與檔案。

| 等級 | 用途 |
| --- | --- |
| `DEBUG` | 詳細除錯資訊 |
| `INFO` | 正常進度（讀了哪個檔、保留幾筆） |
| `WARNING` | 不影響執行但值得注意（樣本被跳過） |
| `ERROR` | 某步驟失敗 |
| `CRITICAL` | 整個程式無法繼續 |

```python
import logging

logging.basicConfig(                          # 只在入口（main）設定一次
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("run.log")],
)
log = logging.getLogger(__name__)             # 每個模組取自己的 logger

log.info("loaded %d samples", 12)             # 用 % 參數，不要先 f-string（等級關閉時省下格式化）
log.warning("sample %s has no reads, skipped", "S3")
try:
    1 / 0
except ZeroDivisionError:
    log.exception("failed")                   # ERROR 等級 + 自動附 traceback
```

> 函式庫模組只呼叫 `logging.getLogger(__name__)`，不要呼叫 `basicConfig`；設定交給執行入口決定。

## 呼叫外部程式 (`subprocess`)

```python
import subprocess

# 參數用 list 傳：不經過 shell，路徑有空白也安全
result = subprocess.run(
    ["samtools", "flagstat", "S1.bam"],
    capture_output=True, text=True,           # 擷取 stdout / stderr 為字串
    check=True,                               # exit code ≠ 0 時丟 CalledProcessError
    timeout=600,
)
result.stdout.splitlines()[0]
result.returncode                             # 0

# 輸出直接寫檔
with open("S1.sorted.bam", "wb") as out:
    subprocess.run(["samtools", "sort", "-@", "4", "S1.bam"], stdout=out, check=True)

# 錯誤處理：保留工具的 stderr
try:
    subprocess.run(["bwa", "mem", "ref.fa", "R1.fq"], capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
    log.error("bwa failed (%d): %s", e.returncode, e.stderr[-500:])
    raise

# 管線：前一個的 stdout 接下一個的 stdin
p1 = subprocess.Popen(["bwa", "mem", "ref.fa", "R1.fq"], stdout=subprocess.PIPE)
p2 = subprocess.run(["samtools", "sort", "-o", "S1.bam", "-"], stdin=p1.stdout, check=True)
p1.stdout.close()
p1.wait()
```

| 參數 | 作用 |
| --- | --- |
| `capture_output=True` | 擷取 stdout 與 stderr |
| `text=True` | 以字串而非 bytes 處理 |
| `check=True` | 失敗時丟例外（**幾乎都要加**，否則失敗會被忽略） |
| `stdout=f` / `stderr=subprocess.STDOUT` | 導向檔案 / 把 stderr 併進 stdout |
| `cwd=` | 子程序的工作目錄 |
| `env={**os.environ, "OMP_NUM_THREADS": "1"}` | 環境變數（要保留原有的就展開 `os.environ`） |
| `timeout=` | 超時就終止並丟 `TimeoutExpired` |

| `shell=True` | 說明 |
| --- | --- |
| 何時需要 | 必須用 shell 功能（`*` 萬用字元、`|`、`>`）時 |
| 風險 | 字串含使用者輸入或檔名時可能被注入指令；必須用時以 `shlex.quote()` 跳脫 |
| 替代 | 萬用字元用 `Path.glob`；管線用上面的 `Popen` 串接 |

> 多個工具串成的流程、需要斷點續跑或丟到 HPC 排程器時，改用 Snakemake / Nextflow 比在 Python 裡疊 `subprocess` 可靠，見 [工作流引擎](../../computing/workflow-engines/README.md)。

## 常用小片段

```python
import sys, os, platform, time
from importlib.metadata import version, distributions
from pprint import pprint

sys.version_info >= (3, 11)                   # 檢查 Python 版本
platform.system()                             # 'Windows' / 'Linux' / 'Darwin'
version("pandas")                             # 已安裝套件版本（pkg_resources 已棄用）
sorted(d.metadata["Name"] for d in distributions())   # 所有已安裝套件

t0 = time.perf_counter()                      # 量測執行時間；細部量測見 Efficient Python
...
print(f"{time.perf_counter() - t0:.2f}s")

pprint({"name": "Alice", "hobbies": ["reading", "cycling"]})   # 巢狀結構好讀的輸出
sys.stdout.reconfigure(encoding="utf-8")      # Windows 主控台印中文出錯時（3.7+）

os.cpu_count()                                # 平行化時決定 worker 數
os.environ.get("SLURM_CPUS_PER_TASK")         # HPC 上實際分配到的核心數
```

> 不要用 `sys.path.append("/path/to/module")` 讓 import 成功：換台機器就壞。把程式整理成套件並安裝到環境（`uv sync`），見 [Python 套件與環境](python-packages.md)。
