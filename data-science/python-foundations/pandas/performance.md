[Python Foundations](../README.md) › [pandas](README.md) › 效能

# 效能 (Performance & Row Operations)

pandas 慢，九成是因為用 Python 迴圈逐列處理本來可以整欄運算的資料。最佳化順序：先量測 → 整欄向量化 → group-wise 用 `transform` / `filter` → 不得已才 `apply(axis=1)` → 最後才逐列迭代。記憶體與檔案格式見 [記憶體與儲存格式](memory-and-storage.md)；通用 Python 效能技巧見 [Efficient Python](../performance-and-scaling/efficient-python.md)。

## 各寫法的速度

10 萬列、計算 `a + b`（pandas 3.1，單次量測，數量級比較用）：

| 寫法 | 時間 | 相對向量化 |
| --- | --- | --- |
| `for _, r in df.iterrows()` | 880 ms | ~7000× |
| `df.apply(lambda r: ..., axis=1)` | 310 ms | ~2400× |
| `for r in df.itertuples()` | 32 ms | ~250× |
| `df["a"] + df["b"]` | 0.13 ms | 1× |
| `df["a"].to_numpy() + df["b"].to_numpy()` | 0.06 ms | ~0.5× |

```python
# 量測：notebook 用 %timeit，腳本用 timeit / perf_counter
%timeit df["a"] + df["b"]

import time
start = time.perf_counter()
result = df["a"] + df["b"]
time.perf_counter() - start
```

## 改寫成向量化

```python
import numpy as np

# 1. 算術：整欄運算
df["total"] = df["a"] + df["b"] + df["c"]
df["row_sum"] = df[["a", "b", "c"]].sum(axis=1)         # 列方向彙總也是向量化

# 2. if / else：布林遮罩、np.where、np.select
df["flag"] = np.where(df["ratio"] > 2, "high", "normal")
df["grade"] = np.select([df["x"] < 0.3, df["x"] < 0.7], ["low", "mid"], default="high")
df.loc[df["x"] < 0, "x"] = 0

# 3. 對照表：map / replace，而不是逐值 if
df["gender"] = df["gender"].replace({"MALE": "M", "FEMALE": "F"})

# 4. 字串、日期：用 .str / .dt
df["gene"] = df["gene"].str.upper()
df["year"] = df["date"].dt.year

# 5. 純數值、大量運算：轉成 NumPy（失去標籤，確定不需要時才用）
vals = df[["x1", "x2", "x3"]].to_numpy()
df["norm"] = np.sqrt((vals ** 2).sum(axis=1))
```

| 慢的寫法 | 改成 |
| --- | --- |
| 逐列迴圈算新欄 | 欄運算、`np.where` / `np.select` |
| 每列 `if / else` | 布林遮罩 + `.loc` |
| 多個 `df.loc[df.x == v, "x"] = w` | `.replace({...})` / `.map({...})` |
| 手動迴圈每組再拼回 | `groupby().transform()` / `.filter()` |
| 迴圈中 `concat` / `loc[len(df)] = row` | 先收進 list，最後一次 `pd.DataFrame(rows)` |
| 迴圈中反覆 `df.at[i, "x"]` | 整欄操作；真要逐格就先 `.to_numpy()` |

## Group-wise 運算

```python
# transform：每列拿到組內的值（不必先 agg 再 merge 回去）
df["bill_z"] = df.groupby("time")["total_bill"].transform(lambda s: (s - s.mean()) / s.std())

# 更快：用內建字串名稱，避免對每組呼叫 Python 函式
g = df.groupby("time")["total_bill"]
df["bill_z"] = (df["total_bill"] - g.transform("mean")) / g.transform("std")

# filter：以組為單位保留或丟棄
df.groupby("day").filter(lambda g: g["total_bill"].mean() > 20)
```

10 萬列、100 組：`transform("mean")` 1.2 ms，`transform(lambda s: s.mean())` 8.9 ms。內建名稱（`"mean"`、`"sum"`、`"std"`、`"rank"`…）走 Cython 最佳化路徑。詳見 [分組彙總](groupby.md)。

## 逐列處理（真的避不掉時）

需要呼叫外部函式（例如每列查 API、解析複雜字串、跑一個非向量化的模型）時：

```python
# 1. apply(axis=1)：每列是一個 Series
df["score"] = df.apply(lambda r: custom(r["x1"], r["x2"]), axis=1)

# 2. itertuples：比 iterrows 快約 30 倍，用屬性取值
results = [custom(r.x1, r.x2) for r in df.itertuples(index=False)]

# 3. 只用到幾欄：zip 最快
df["score"] = [custom(a, b) for a, b in zip(df["x1"], df["x2"])]

# 4. 單欄逐元素：Series.map
df["label"] = df["sepal_length"].map(lambda x: "long" if x > 5.8 else "short")
```

> `iterrows()` 把每列轉成 Series，會**改變 dtype**：同一列有 int 與 float 欄時，int 會變成 float（`1` → `1.0`），大整數 ID 可能因此失去精度。`itertuples()` 保留各欄 dtype。

## 其他加速選項

| 情境 | 選項 |
| --- | --- |
| 資料數 GB、單機 | [Polars](../performance-and-scaling/polars.md)（多執行緒、lazy） |
| 記憶體放不下 | 只讀需要的欄、縮小 dtype、分塊，見 [記憶體與儲存格式](memory-and-storage.md) |
| 數值迴圈無法向量化 | [Numba](../performance-and-scaling/efficient-python.md#迴圈無法避免時numba) |
| 多核心平行（每組獨立） | [平行運算](../performance-and-scaling/parallel.md) |
| 用 SQL 思考、資料在 Parquet | DuckDB 直接查 DataFrame / Parquet |
| 跨機器 | [Spark](../../data-engineering/spark.md) |
