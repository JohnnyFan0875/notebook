[Python Foundations](../README.md) › [pandas](README.md) › Index 與 MultiIndex

# Index 與 MultiIndex

index 是 pandas 與 NumPy 最大的差異：運算會**依 index 標籤對齊**，而不是依位置。這讓 `s1 + s2` 自動配對相同樣本，但也是「為什麼多出一堆 NaN」的來源。MultiIndex 則是多層 key，常見於 `groupby` 多個欄位之後。

## Index 對齊

```python
import pandas as pd

a = pd.Series([1, 2, 3], index=["S1", "S2", "S3"])
b = pd.Series([10, 20, 30], index=["S2", "S3", "S4"])

a + b                       # S1 NaN, S2 12, S3 23, S4 NaN：依標籤配對，沒對到的變 NaN
a.add(b, fill_value=0)      # S1 1, S2 12, S3 23, S4 30
a.to_numpy() + b.to_numpy() # [11 22 33]：依位置，忽略標籤（小心）

b.reindex(a.index)          # 依 a 的順序重排 b；不存在的標籤補 NaN
a.index.intersection(b.index)   # ['S2', 'S3']：共同樣本
```

> 生資常見：表達矩陣（基因 × 樣本）與樣本資訊表 (metadata) 要對齊樣本順序。用 `meta = meta.loc[expr.columns]` 或 `reindex`，並 `assert (meta.index == expr.columns).all()`，不要假設兩個檔案的樣本順序相同。

## 設定與重設 Index

```python
import seaborn as sns
iris = sns.load_dataset("iris")

df = iris.set_index("species")                      # 欄 → index
df = iris.set_index(["species", "sepal_length"])    # 多個欄 → MultiIndex
df.reset_index()                                    # index → 欄
df.reset_index(drop=True)                           # 丟掉 index，重新編 0..n-1

df.index.name, df.index.names
iris.set_index("species").index.is_unique           # False：loc 會回傳多列
iris.set_index("id", verify_integrity=True)         # 有重複就報錯
```

| 何時把欄設為 index | 何時保持一般欄 |
| --- | --- |
| 有唯一 ID（樣本、基因）且常用它查找、對齊 | 要 merge、groupby、畫圖、匯出 |
| 時間序列（`DatetimeIndex` 才能 `resample`、`rolling("7D")`） | 欄位可能重複 |

## MultiIndex 選取

```python
m = iris.set_index(["species", "sepal_length"]).sort_index()   # 切片前一定要排序

m.index.names                       # ['species', 'sepal_length']
m.index.levels                      # 每層的唯一值
m.index.get_level_values("species") # 每列在某層的值

m.loc["setosa"]                                    # 第一層
m.loc[("setosa", 5.0)]                             # 完整 key
m.loc[[("setosa", 5.1), ("virginica", 6.3)]]       # 多個 key

idx = pd.IndexSlice
m.loc[idx[:, 5.0:5.2], :]                          # 第二層切片（不論第一層）：23 列
m.xs(5.0, level="sepal_length")                    # 取某層的某值：10 列
```

| 操作 | 寫法 |
| --- | --- |
| 依層排序 | `m.sort_index(level=["species", "sepal_length"], ascending=[True, False])` |
| 交換層順序 | `m.swaplevel()`；`reorder_levels([...])` |
| 移除一層 | `m.droplevel("sepal_length")` |
| 依層分組 | `m.groupby(level="species").mean()` |
| 欄的 MultiIndex 攤平 | `df.columns = ["_".join(c) for c in df.columns]` |

## Stack 與 Unstack

```text
unstack：row index 的某一層 → 變成欄（變寬）
stack  ：欄 → 變成 row index 的最內層（變長）

              sepal_width  False  True                       species     sepal_width
species                                    stack()           setosa      False     4.64
setosa                      4.64   5.08   ─────────▶                     True      5.08
versicolor                  5.83   6.49   ◀─────────         versicolor  False     5.83
virginica                   6.48   6.81    unstack()         ...
```

```python
w = iris.groupby(["species", iris["sepal_width"] > 3])["sepal_length"].mean()   # 2 層 index 的 Series

w.unstack()                         # 最內層 → 欄（上圖左）
w.unstack(level="species")          # 指定哪一層攤開
w.unstack(level=0, fill_value=0)    # 不存在的組合補 0（業務上合理時）
w.unstack().stack()                 # 還原
cars.unstack(level=["brand", "model"])   # 一次攤開多層
```

`unstack` 產生 NaN 是正常的：不是每個 index 組合都存在。pandas 3 的 `stack` 不再接受 `dropna=` 參數（新實作不會自己產生全 NaN 的列）；需要去掉缺值時在之後接 `.dropna()`。

寬長表轉換的一般做法（`pivot` / `melt`）見 [Reshape 與 Merge](reshape-merge.md)；`stack` / `unstack` 適合資料已經放在 index 時。
