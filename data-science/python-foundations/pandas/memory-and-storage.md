[Python Foundations](../README.md) › [pandas](README.md) › 記憶體與儲存格式

# 記憶體與儲存格式 (Memory & Storage Formats)

pandas 把整張表放進記憶體，而且常佔用檔案大小的數倍。資料一大，先做三件事：**只讀需要的欄、縮小 dtype、把 CSV 換成 Parquet**。這篇處理「放得進但很吃記憶體」與「中間檔怎麼存」；各格式的基本讀法見 [匯入資料](../importing-data.md#二進位與統計軟體格式)。

## 量測記憶體

```python
df.info(memory_usage="deep")                  # 總記憶體（deep 才會計算字串實際大小）
df.memory_usage(deep=True) / 1e6              # 每欄 MB
df.memory_usage(deep=True).sum() / 1e6
```

不加 `deep=True` 時，`object` 欄只算指標大小，會嚴重低估。

## 縮小 dtype

以 100 萬列的長表（sample、gene、chrom 三個字串欄 + count、tpm 兩個數值欄）為例：

| 版本 | 記憶體 |
| --- | --- |
| 字串欄為 `object`（pandas 2 預設） | 181 MB |
| 字串欄為 `str`（pandas 3 預設，Arrow 儲存） | 58 MB |
| 字串欄轉 `category`、`int32`、`float32` | 12 MB |

```python
df = df.astype({
    "sample": "category",            # 50 種值重複 100 萬次 → 類別
    "gene": "category",              # 2 萬種仍遠少於列數 → 仍划算
    "chrom": "category",
    "count": "int32",
    "tpm": "float32",
})

pd.to_numeric(df["count"], downcast="integer")   # 自動選能裝下的最小整數型別（此例 int8）
pd.to_numeric(df["tpm"], downcast="float")       # float32
```

| 欄位 | 建議 | 注意 |
| --- | --- | --- |
| 重複值多的字串 | `category` | 唯一值接近列數（ID、序列）時沒好處 |
| 整數計數 | `int32`（< 21 億） | 不要用 `int8` / `int16` 存計數：之後相加會溢位 |
| 連續值 | `float32` | 約 7 位有效數字；統計檢定、累加大量數值時保留 `float64` |
| 布林旗標 | `bool` / `boolean` | 不要存成 `"yes"` / `"no"` 字串 |

> 縮小 dtype 是在「省記憶體」與「數值安全」間取捨：`int8` 的 count 欄加總、平方都可能悄悄溢位。分析中途若要做大量運算，先轉回 `int64` / `float64`。

## 讀檔時就省

```python
pd.read_csv(
    "counts.csv",
    usecols=["gene", "sample", "count"],                    # 只讀需要的欄
    dtype={"count": "int32", "sample": "category"},         # 直接指定 dtype，不用先讀成 int64 再轉
)

pd.read_csv("counts.csv", dtype_backend="pyarrow")          # 全部欄用 Arrow 型別（int64[pyarrow]、string[pyarrow]…）
pd.read_csv("counts.csv", engine="pyarrow")                 # 用 pyarrow 解析器（多執行緒）

# 比記憶體大：分塊彙總
totals = sum(chunk.groupby("gene")["count"].sum()
             for chunk in pd.read_csv("counts.csv", chunksize=500_000))
```

| `dtype_backend` | 型別 | 缺值 |
| --- | --- | --- |
| 預設（NumPy） | `int64`、`float64`、`str` | `NaN`（整數欄有缺值會變 float） |
| `"numpy_nullable"` | `Int64`、`Float64`、`string` | `pd.NA` |
| `"pyarrow"` | `int64[pyarrow]`、`string[pyarrow]` | `pd.NA`；與 Parquet / Polars / DuckDB 零複製交換 |

## 儲存格式

同一張 100 萬列的表：

| 格式 | 檔案大小 | 保留 dtype | 部分讀取 | 其他語言 | 適合 |
| --- | --- | --- | --- | --- | --- |
| CSV | 43 MB | 否（每次重新推斷） | 只能選欄，仍需掃全檔 | 全部 | 交付、給人看、跨工具最低公約數 |
| **Parquet** | 12 MB | 是（含 category） | 選欄、依條件跳過 row group | R arrow、Spark、DuckDB、Polars | **分析中間檔首選** |
| Feather (Arrow IPC) | 32 MB | 是 | 選欄 | R arrow、Polars | 同一流程內暫存、讀寫最快 |
| HDF5（pandas `HDFStore`） | 15 MB | 是 | `where` 查詢（table 格式） | 需 PyTables 結構才好讀 | 單檔多張表、可追加 |
| pickle | — | 是 | 否 | 僅 Python，且版本相依 | 只放自己的暫存物件 |

### Parquet

欄式 (columnar) 儲存：每欄分開壓縮，讀取時可只讀需要的欄；檔案內記錄每個 row group 的最小 / 最大值，篩選條件可直接跳過不需要的區塊。

```python
df.to_parquet("expr.parquet")                         # 需要 pyarrow；預設 snappy 壓縮
df.to_parquet("expr.parquet", compression="zstd")     # 壓縮率較高
pd.read_parquet("expr.parquet", columns=["gene", "count"])                 # 只讀兩欄
pd.read_parquet("expr.parquet", filters=[("count", ">", 40)])              # 依條件讀列

# 分區 (partitioning)：依欄值拆成資料夾，查詢某一分區時只讀那些檔案
df.to_parquet("expr_by_chrom", partition_cols=["chrom"])
# expr_by_chrom/chrom=chr1/xxx.parquet
# expr_by_chrom/chrom=chr10/xxx.parquet ...
pd.read_parquet("expr_by_chrom", filters=[("chrom", "==", "chr1")])        # 只讀 chr1 資料夾；chrom 讀回為 category
```

| 分區欄的選擇 | |
| --- | --- |
| 好 | 常用來篩選、唯一值數十到數百（染色體、樣本批次、日期） |
| 壞 | 唯一值上萬（基因、樣本 ID）→ 產生大量小檔，反而變慢 |

更大的資料可以不經 pandas，直接用 DuckDB 或 Polars 對 Parquet 下查詢，只把結果讀進記憶體：

```python
import duckdb
duckdb.sql("SELECT gene, avg(tpm) FROM 'expr_by_chrom/**/*.parquet' WHERE chrom = 'chr17' GROUP BY gene").df()
```

DuckDB 完整用法見 [DuckDB 與 Parquet](../../databases/duckdb-and-parquet.md)；另見 [Polars](../performance-and-scaling/polars.md) 的 `scan_parquet`。

### HDF5

HDF5 是階層式容器：一個檔案內有群組 (group) 與資料集 (dataset)，像檔案系統。pandas 透過 PyTables（`pip install tables`）讀寫自己的結構；其他工具寫的 HDF5（`.h5ad`、`.loom`、10x `.h5`）用 `h5py` 或專用套件讀，見 [匯入資料](../importing-data.md#生資常見格式)。

```python
df.to_hdf("store.h5", key="expr", format="table", data_columns=["sample", "chrom", "count"], complevel=5)
pd.read_hdf("store.h5", "expr", where="sample == 'S001'")   # 只讀符合條件的列（欄需列在 data_columns）

with pd.HDFStore("store.h5") as store:
    store.put("meta", meta, format="table")                 # 同一檔案放多張表
    store.append("expr", new_batch, format="table",         # 分批追加：適合逐批產生的結果
                 min_itemsize={"gene": 20})                 # 字串欄預留長度，後面批次的長字串才放得下
    store.keys()                                            # ['/expr', '/meta']
    store.select("expr", where="chrom == 'chr1' & count > 40", columns=["gene", "count"])
```

| `format=` | 寫入 | 查詢 / 追加 |
| --- | --- | --- |
| `"fixed"`（預設） | 快 | 不能 `where`、不能 `append` |
| `"table"` | 較慢 | 可以 |

> 新專案的表格資料優先用 Parquet：跨語言、生態系完整、可分區。HDF5 適合大型多維數值陣列（影像、模擬結果）與既有的 HDF5 生態（單細胞 AnnData 底層即 HDF5）。多個 process 同時寫同一個 HDF5 檔案會損毀，平行寫入時每個 worker 寫自己的檔案。

## 選擇流程

```text
資料放得進記憶體嗎？
├─ 放得進，但很吃記憶體 → usecols + 指定 dtype + category / 縮小數值型別
├─ 勉強 / 放不進
│   ├─ 只需要彙總結果 → chunksize 分塊，或 DuckDB / Polars lazy 直接查 Parquet
│   └─ 需要全部資料做運算 → Polars、Dask 或 Spark
└─ 中間檔要存什麼格式？
    ├─ 表格 → Parquet（常依某欄篩選 → partition_cols）
    ├─ 多維數值陣列 → HDF5 / Zarr / .npy
    └─ 交付給別人或 Excel 使用者 → CSV
```

相關：[平行運算](../performance-and-scaling/parallel.md)、[Scalable Processing](../../data-engineering/scalable-processing-and-out-of-core.md)。
