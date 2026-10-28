[Data Science](../README.md) › [Python Foundations](README.md) › 匯入資料

# 匯入資料 (Importing Data)

匯入資料前先問三件事：純文字還是二進位？表格還是巢狀？要的是 NumPy array、pandas DataFrame，還是專用物件（`AnnData`、`pysam.AlignmentFile`）？R 的對應寫法見 [R 匯入資料](../r-foundations/importing-data.md)；資料庫見 [Databases](../databases/README.md)；HTTP / API 見 [API 與 HTTP](api-http.md)；做成可重複的匯入管線見 [Data Engineering](../data-engineering/README.md)。

## 選工具

| 資料 | 讀取 | 得到 |
| --- | --- | --- |
| 乾淨的純數值文字 | `np.loadtxt` / `np.genfromtxt`（有缺值） | `ndarray` |
| CSV / TSV（有欄名、混合型別） | `pd.read_csv` | `DataFrame` |
| Excel | `pd.read_excel`（需 `openpyxl`） | `DataFrame` |
| JSON / JSON Lines | `json`、`pd.read_json`、`pd.json_normalize` | `dict` / `DataFrame` |
| Parquet / Feather | `pd.read_parquet` / `pd.read_feather`（需 `pyarrow`） | `DataFrame`（保留 dtype） |
| HDF5 | `h5py`；pandas 寫的用 `pd.read_hdf` | 群組 / dataset 階層 |
| SAS / Stata / SPSS | `pd.read_sas` / `pd.read_stata` / `pd.read_spss` | `DataFrame` |
| MATLAB `.mat` | `scipy.io.loadmat`（v7.3 以後是 HDF5，改用 `h5py`） | `dict` of arrays |
| Python 物件快照 | `pickle` / `joblib` | 任意物件（**不可讀不受信任的來源**） |
| SQL 資料庫 | `pd.read_sql` + SQLAlchemy | `DataFrame` |
| 網頁上的表格 | `pd.read_html`（需 `lxml`） | `list[DataFrame]` |

### 生資常見格式

| 格式 | Python 工具 | 備註 |
| --- | --- | --- |
| FASTA / FASTQ | `Bio.SeqIO`（Biopython）、`pyfastx`、`pysam.FastxFile` | 逐筆 iterator；自己寫 parser 見 [迭代器與生成器](iterator.md#生成器-generators惰性求值) |
| SAM / BAM / CRAM | `pysam` | 需要 `.bai` 索引才能依區間查詢 |
| VCF / BCF | `pysam.VariantFile`、`cyvcf2`；`scikit-allel` 轉成 array | |
| BED / GTF / GFF | `pd.read_csv(sep="\t", header=None, comment="#")`、`pyranges`、`gtfparse` | BED 是 0-based、GTF 是 1-based |
| 計數矩陣（TSV / MTX） | `pd.read_csv`、`scipy.io.mmread`（稀疏） | 10x 輸出用 `scanpy.read_10x_mtx` |
| `.h5ad`（單細胞） | `anndata.read_h5ad` / `scanpy` | HDF5 為底；`backed="r"` 不全部載入 |
| Zarr / 大型陣列 | `zarr`、`xarray` | 雲端友善、可分塊 |

## CSV / TSV：`pd.read_csv`

```python
import pandas as pd

df = pd.read_csv(
    "counts.tsv",
    sep="\t",                       # TSV；不確定分隔符時 sep=None, engine="python" 讓它猜
    index_col=0,                    # 第一欄當 index（例如 gene ID）
    header=0,                       # 欄名在第幾列；無欄名用 header=None, names=[...]
    skiprows=2,                     # 跳過開頭的說明行
    comment="#",                    # 忽略 # 開頭的註解
    usecols=["gene", "S1", "S2"],   # 只讀需要的欄，省記憶體
    dtype={"gene": "string", "chrom": "category"},   # 明確指定型別
    na_values=["NA", ".", "-"],     # 額外視為缺值的字串
    parse_dates=["collected"],
    nrows=1000,                     # 先讀一小段確認格式
    compression="infer",            # .gz / .zip / .zst 依副檔名自動解壓
    encoding="utf-8",
)
df = pd.read_csv("https://example.org/data.csv")   # 直接讀 URL
```

讀完立刻檢查——`read_csv` 成功不代表資料可以用：

```python
df.shape
df.head()
df.info()                         # dtype 對嗎？數值欄變成 object / str 代表有雜值
df.describe(include="all")
df.isna().sum()
df.index.is_unique                # ID 有沒有重複
```

### 常見陷阱

| 症狀 | 原因 | 處理 |
| --- | --- | --- |
| 數值欄變成字串 | 混進 `"NA"`、`"."`、`"<0.01"`、千分位逗號 | `na_values=`、`thousands=","`；`pd.to_numeric(errors="coerce")` 後檢查變 NaN 的列 |
| ID 前導零消失（`00123` → `123`） | 被當成整數 | `dtype={"id": "string"}` |
| 大整數 ID 變成浮點數 | 欄位有缺值，int 被升格成 float | `dtype="Int64"`（可為 NA 的整數） |
| 基因名變成日期（`SEPT2`、`MARCH1` → 日期） | 檔案曾被 Excel 開過存檔 | 回原始來源取檔；HGNC 已改名為 `SEPTIN2`、`MARCHF1` |
| 只有一欄 | 分隔符錯了 | 用 `sep="\t"` 或先用 `head` 看檔案 |
| 記憶體爆掉 | 整檔一次讀入 | `usecols`、`dtype`、`chunksize`、改用 Parquet 或 [Polars](performance-and-scaling/polars.md)；見 [pandas 記憶體與儲存格式](pandas/memory-and-storage.md) |

### 大檔與多檔

```python
# 分塊處理：記憶體只放一塊
totals = None
for chunk in pd.read_csv("large.csv", chunksize=100_000):
    part = chunk.groupby("sample")["reads"].sum()
    totals = part if totals is None else totals.add(part, fill_value=0)

# 同一 schema 的多個檔案：讀成 list 後合併，並保留來源
from pathlib import Path
files = sorted(Path("data").glob("sample_*.csv"))
df = pd.concat(
    [pd.read_csv(f).assign(source=f.stem) for f in files],
    ignore_index=True,
)
```

> 合併前確認各檔欄位一致：`{tuple(pd.read_csv(f, nrows=0).columns) for f in files}` 應該只有一個元素。

### 純數值：NumPy

```python
import numpy as np

X = np.loadtxt("mnist.csv", delimiter=",", skiprows=1, usecols=[0, 2], dtype=float)
X = np.genfromtxt("with_missing.csv", delimiter=",", skip_header=1)   # 缺值變 nan
X = df.to_numpy()                                                     # 從 DataFrame 轉
```

`np.loadtxt` 要求檔案規則、型別一致；有缺值、註解或混合型別時改用 pandas。

## Excel

```python
pd.read_excel("data.xlsx", sheet_name="Sheet1", skiprows=3, usecols="A:F")
pd.read_excel("data.xlsx", sheet_name=None)        # 所有工作表 → {sheet_name: DataFrame}

xls = pd.ExcelFile("fruit_tabs.xlsx")              # 先看有哪些工作表再逐張讀
xls.sheet_names                                    # ['price', 'color']
price = xls.parse("price")
```

> Excel 適合交給人看，不適合當分析中間檔：會自動轉日期、截斷大數字的精度、隱藏格式。分析流程內改存 CSV 或 Parquet。

## JSON

```python
import json

with open("config.json", encoding="utf-8") as f:
    data = json.load(f)                            # 檔案 → dict / list
data = json.loads('{"fruit": "apple", "n": 10}')   # 字串 → dict

# JSON Lines / NDJSON：一行一筆記錄（log、API 匯出常見）
df = pd.read_json("events.jsonl", lines=True)
for chunk in pd.read_json("events.jsonl", lines=True, chunksize=10_000):   # 大檔分塊
    ...

# 巢狀 JSON → 平面表格
records = [
    {"id": 1, "user": {"name": "A", "loc": "TW"}, "tags": ["x", "y"]},
    {"id": 2, "user": {"name": "B"}, "tags": []},
]
pd.json_normalize(records)                         # 欄位：id, tags, user.name, user.loc
pd.json_normalize(records, record_path="tags", meta=["id"])   # 把 list 欄展開成多列
```

| 巢狀資料原則 | 說明 |
| --- | --- |
| 只攤平需要的欄位 | 先挑出關鍵路徑，不必一次把整份文件攤平 |
| 欄位不一定每筆都有 | 某些路徑只在特定記錄類型存在（如轉推才有 `quoted_status`）；用 `.get()` 或接受 NaN |
| 「有值」本身可能是篩選偏誤 | 例如只有少數記錄有精確座標，這群人不代表全體；把缺值比例一併報告 |
| 不同精度的欄位不要混成一欄 | 自填地點 / 範圍框 / 精確座標 是不同層級的資訊 |

## 二進位與統計軟體格式

```python
# Parquet：欄式儲存，保留 dtype、壓縮率高、可只讀部分欄位 → 分析中間檔首選
df.to_parquet("counts.parquet")
pd.read_parquet("counts.parquet", columns=["gene", "S1"])

# HDF5：群組 (group) / 資料集 (dataset) 的階層結構
import h5py
with h5py.File("data.h5", "r") as f:
    list(f.keys())                                 # 先看結構
    f.visit(print)                                 # 列出所有路徑
    strain = f["strain/Strain"][:]                 # [:] 才真正讀進記憶體
    f["strain/Strain"].attrs["Xspacing"]           # metadata 存在 attrs

pd.read_hdf("store.h5", key="mydata")              # 只能讀 pandas 自己寫的 HDF5（需 tables）

# MATLAB
import scipy.io
mat = scipy.io.loadmat("albeck_gene_expression.mat")
[k for k in mat if not k.startswith("__")]         # 略過 __header__ 等 metadata

# SAS / Stata / SPSS
pd.read_sas("urbanpop.sas7bdat")
pd.read_stata("urbanpop.dta")
pd.read_spss("survey.sav")                         # 需 pyreadstat

# pickle：只用於自己產生、同版本 Python / 套件的暫存
import pickle
with open("model.pkl", "rb") as f:
    obj = pickle.load(f)
```

| 中間檔格式 | 跨語言 | 保留 dtype | 速度 / 大小 | 適用 |
| --- | --- | --- | --- | --- |
| CSV | 是 | 否 | 慢 / 大 | 交換、人工檢視 |
| Parquet | 是（R arrow、Spark、DuckDB） | 是 | 快 / 小 | **分析中間檔首選** |
| Feather | 是 | 是 | 最快 | 短期暫存 |
| HDF5 | 是 | 是 | 快 | 大型多維陣列、科學資料 |
| pickle | 否（僅 Python） | 是（任意物件） | 快 | 暫存物件；**勿載入他人提供的檔案**（可執行任意程式碼） |

## 網路來源

```python
from urllib.request import urlretrieve
urlretrieve("https://archive.ics.uci.edu/.../winequality-white.csv", "wine.csv")   # 下載存檔

import requests
r = requests.get("https://www.omdbapi.com/", params={"t": "hackers", "apikey": KEY}, timeout=10)
r.raise_for_status()
r.json()                                           # JSON → dict；r.text 是 HTML 字串，r.content 是 bytes

tables = pd.read_html("https://en.wikipedia.org/wiki/Iris_flower_data_set")   # 網頁中所有 <table>
tables[0]
```

查詢參數用 `params=` 而不是手動拼 `?t=...`，會自動處理編碼。完整的 HTTP、認證、重試見 [API 與 HTTP](api-http.md)；HTML 解析與爬蟲見 [Web Scraping](../web-scraping/README.md)。

## 資料庫

```python
from sqlalchemy import create_engine

engine = create_engine("sqlite:///iris.db")        # PostgreSQL: postgresql+psycopg://user:pw@host/db
df = pd.read_sql("SELECT * FROM iris WHERE species = :sp", engine, params={"sp": "setosa"})
df.to_sql("iris_copy", engine, if_exists="replace", index=False)
```

詳見 [Python 與 SQLAlchemy](../databases/python-sqlalchemy.md)。

## 格式互轉 (Data Type Transformation)

| 轉換 | 寫法 |
| --- | --- |
| dict ↔ JSON 檔 | `json.dump(d, f, indent=2)` / `json.load(f)` |
| dict ↔ JSON 字串 | `json.dumps(d)` / `json.loads(s)` |
| list ↔ tuple | `tuple(x)` / `list(x)` |
| 字串 ↔ datetime | `strptime` / `strftime`，見 [日期與時間](datetime.md) |
| CSV ↔ list of dict | `csv.DictReader` / `csv.DictWriter` |
| list of list / array → DataFrame | `pd.DataFrame(data, columns=[...])` |
| DataFrame → array | `df.to_numpy()`（混合型別會變 `object`，先 `select_dtypes("number")`） |
| DataFrame → dict | `df.to_dict(orient="records")`（另有 `dict`、`list`、`series`、`split`、`index`） |
| Series → list | `s.tolist()` |
| DataFrame → 檔案 | `to_csv(index=False)`、`to_parquet()`、`to_excel()`、`to_json(orient="records", lines=True)` |

```python
import csv, json

with open("sample.json", "w", encoding="utf-8") as f:
    json.dump({"name": "Alice", "age": 30}, f, indent=2, ensure_ascii=False)   # 中文不轉成 \uXXXX

with open("sample.csv", newline="", encoding="utf-8") as f:   # csv 模組要 newline=""
    rows = list(csv.DictReader(f))                            # 每列一個 dict，值都是字串

with open("out.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["name", "age"])
    w.writeheader()
    w.writerows([{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}])

df = pd.DataFrame([[1, "Alice", 30], [2, "Bob", 25]], columns=["ID", "Name", "Age"])
df.to_dict(orient="records")       # [{'ID': 1, 'Name': 'Alice', 'Age': 30}, ...]
df.select_dtypes("number").to_numpy()
```

## 匯入流程檢查表

```
辨識格式（副檔名 + 用 head / less 看前幾行）
  → 決定目標結構（array / DataFrame / 專用物件）
  → 大檔先讀一小段（nrows / chunksize）
  → 檢查 shape、dtype、缺值、ID 唯一性、欄名
  → 才進入清理與分析
```

很多下游的奇怪結果（平均數是 NaN、merge 後列數暴增、類別多出一個 `"NA"`）其實是匯入時就錯了。清理步驟見 [EDA 工作流程](../data-manipulation-and-eda/eda-workflow.md)。
