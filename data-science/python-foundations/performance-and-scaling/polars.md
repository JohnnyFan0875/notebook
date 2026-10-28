[Python Foundations](../README.md) › [效能與擴展](README.md) › Polars

# Polars

Polars 是用 Rust 寫的 DataFrame 引擎：多執行緒、欄式儲存（Apache Arrow），以**表達式 (expression)** 描述整個查詢，並能在 lazy 模式下先最佳化再執行。資料在數 GB、pandas 開始變慢或吃光記憶體時，常是比上 Spark 更簡單的選擇。

| | pandas | Polars |
| --- | --- | --- |
| 思考方式 | 一步步修改 DataFrame | 描述整個查詢，交給引擎執行 |
| 執行 | eager、多數操作單執行緒 | eager 或 lazy、自動多執行緒 |
| index | 有（常是混淆來源） | **沒有**，一律用欄位 |
| 缺值 | `NaN` / `None` / `pd.NA` 混用 | 統一 `null`（`NaN` 是浮點值，不是缺值） |
| 比記憶體大的資料 | 要自己分塊 | lazy + streaming 引擎 |
| 生態系 | sklearn、statsmodels、seaborn 直接吃 | 需要時 `.to_pandas()` / `.to_numpy()` 轉換 |

## 讀取：eager vs lazy

```python
import polars as pl

df = pl.read_csv("rentals.csv")                # eager：立刻讀成 DataFrame（探索、除錯）
lf = pl.scan_csv("rentals.csv")                # lazy：只建立查詢計畫（LazyFrame）
lf = pl.scan_parquet("variants/*.parquet")     # 多檔、Parquet 也一樣
lf.collect()                                   # 執行並回傳 DataFrame
```

| 用 eager | 用 lazy |
| --- | --- |
| 探索資料、一步步看中間結果 | 已知完整流程、串接很多步驟 |
| 除錯某段轉換 | 資料大、在乎速度與記憶體 |
| | 只需要部分欄位 / 列（引擎會只讀需要的部分） |

## 表達式 (Expressions)

`pl.col("x")` 本身不是資料，而是「對欄位 x 的運算描述」，放進 `select`、`with_columns`、`filter`、`agg` 等 context 才會執行。

| Context | 作用 | pandas 對應 |
| --- | --- | --- |
| `select(...)` | **只保留**指定的輸出欄 | `df[["a", "b"]]` + 新欄 |
| `with_columns(...)` | 保留原欄位，新增或覆寫欄 | `df.assign(...)` |
| `filter(...)` | 篩選列 | `df[mask]` / `df.query()` |
| `group_by(...).agg(...)` | 分組彙總 | `df.groupby().agg()` |
| `sort(...)` | 排序 | `sort_values()` |
| `join(...)` | 合併 | `merge()` |

```python
df = pl.DataFrame({
    "name": ["a", "bb", "ccc", "d"],
    "type": ["Villa", "Flat", "Villa", "Villa"],
    "price": [300, 120, 800, 450],
    "beds": [3, 1, 4, 0],
    "beach": [True, False, True, False],
})

df.select("name", "price")
df.select((pl.col("price") / pl.col("beds")).alias("price_per_bed"))   # alias 命名輸出欄

df.with_columns(
    (pl.col("price") * 0.9).alias("discount_price"),
    pl.when(pl.col("beds") > 0)                                        # 條件運算：取代 np.where
      .then(pl.col("price") / pl.col("beds"))
      .otherwise(None)
      .alias("ppb"),                                                   # [100.0, 120.0, 200.0, null]
)

df.filter((pl.col("price") < 500) & pl.col("beach"))                  # 多條件用 & | ~，每個條件加括號

df.group_by("type").agg(
    pl.len().alias("n"),
    pl.col("price").mean().alias("mean_price"),
)                                                                      # Flat: 1, 120.0；Villa: 3, 516.7

df.with_columns(pl.col("price").rank().over("type").alias("rank_in_type"))   # 視窗函數：類似 groupby().transform

df.with_columns(pl.col(pl.String).str.len_chars().name.suffix("_len"))      # 依 dtype 一次選多欄
df.join(hosts, on="host_id", how="left")
```

字串用 `.str`、日期用 `.dt`、list 欄用 `.list` 命名空間，和 pandas 類似。

## Lazy 查詢與最佳化

```python
result = (
    pl.scan_csv("rentals.csv")
    .filter(pl.col("type") == "Villa")
    .with_columns((pl.col("price") / pl.col("beds")).alias("price_per_bed"))
    .select("name", "price", "price_per_bed")
    .collect()
)

print(pl.scan_csv("rentals.csv").filter(pl.col("type") == "Villa").select("name", "price").explain())
# Csv SCAN [rentals.csv]
#   PROJECT 3/5 COLUMNS              ← projection pushdown：只讀用到的 3 欄
#   SELECTION: col("type") == "Villa" ← predicate pushdown：讀檔時就過濾
```

| 最佳化 | 意義 |
| --- | --- |
| projection pushdown | 只讀查詢用到的欄位 |
| predicate pushdown | 篩選條件推到讀檔階段，少讀很多列（Parquet 尤其有效） |
| 共同子表達式消除 | 重複的運算只算一次 |

### 比記憶體大的資料：streaming

```python
(
    pl.scan_parquet("gnomad_chr*.parquet")
    .filter(pl.col("AF") > 0.01)
    .group_by("chrom")
    .agg(pl.len())
    .collect(engine="streaming")             # 分批處理，不需要整份放進記憶體
)

pl.scan_csv("huge.csv").filter(...).sink_parquet("filtered.parquet")   # 結果直接寫檔，不經過記憶體
```

## 與 pandas / NumPy 互轉

```python
pdf = df.to_pandas()                         # 給 seaborn、statsmodels、sklearn
df = pl.from_pandas(pdf)
X = df.select(pl.col(pl.Float64)).to_numpy()
```

> 常見做法：繁重的讀取、篩選、join、彙總用 Polars（lazy），結果變小後 `.to_pandas()` 交給統計 / 繪圖套件。

## 從 pandas 轉過來的注意事項

| pandas 習慣 | Polars |
| --- | --- |
| `df["new"] = ...` 原地修改 | 物件不可變；`df = df.with_columns(...)` |
| 依賴 index 對齊、`loc` | 沒有 index；用欄位 `join` / `filter` |
| `apply(lambda ...)` | 改用表達式；`map_elements` 是最後手段（會失去平行與最佳化） |
| `df[df.a > 1]` | `df.filter(pl.col("a") > 1)` |
| `groupby` 結果有 index | `group_by` 結果是一般欄位，**順序不保證**（需要時 `maintain_order=True` 或 `sort`） |
| `NaN` 當缺值 | 用 `null`；`fill_null` / `is_null`，`fill_nan` 只處理浮點 NaN |

R 使用者可對照 `dplyr`：`select` / `filter` / `mutate`（`with_columns`）/ `group_by` + `summarise`（`agg`）幾乎一一對應，見 [R 資料處理](../../r-foundations/README.md)。SQL 使用者也可以直接 `pl.SQLContext` 或改用 DuckDB 查 Parquet，見 [Databases](../../databases/README.md)。
