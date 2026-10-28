[Python Foundations](../README.md) › [pandas](README.md) › 建立資料

# 建立資料 (Creating Data)

`Series` 是帶 index 的一維 array，`DataFrame` 是共用同一個 index 的多個 Series（每欄一個 dtype）。實務上多半從檔案讀入（見 [匯入資料](../importing-data.md)），但小型對照表、測試資料、模擬結果都需要手動建立。

## Series

```python
import numpy as np
import pandas as pd

s = pd.Series([10, 20, 30], index=["A", "B", "C"], name="reads")
pd.Series({"A": 10, "B": 20})                   # dict：key 變 index
pd.Series(np.arange(3))                         # 沒給 index → 0, 1, 2
pd.Series(5, index=["x", "y"])                  # 純量會廣播

s.index, s.values, s.to_numpy(), s.name         # 取出 index / 資料
s["B"], s.iloc[1]                               # 20, 20：標籤 vs 位置
```

## DataFrame

| 來源 | 寫法 | 適合 |
| --- | --- | --- |
| dict of lists（每個 key 是一欄） | `pd.DataFrame({"a": [...], "b": [...]})` | 最常用 |
| list of lists（每個內層是一列） | `pd.DataFrame(rows, columns=[...])` | 逐列產生的資料 |
| list of dicts（records） | `pd.DataFrame(records)` / `pd.json_normalize(records)` | API / JSON 回傳；巢狀時用 `json_normalize` |
| dict of dicts / 以列為 key | `pd.DataFrame.from_dict(d, orient="index")` | `{sample: {gene: value}}` |
| NumPy 2D array | `pd.DataFrame(arr, index=..., columns=...)` | 模擬結果、矩陣 |
| 多個 Series | `pd.concat([s1, s2], axis=1)` | 依 index 對齊 |

```python
# 1. dict of lists
df = pd.DataFrame({
    "species": ["setosa", "versicolor", "virginica"],
    "avg_length": [5.0, 5.9, 6.5],
})

# 2. list of lists
df = pd.DataFrame([["setosa", 5.0], ["versicolor", 5.9]], columns=["species", "avg_length"])

# 3. list of dicts：缺的 key 變 NaN
pd.DataFrame([{"id": 1, "x": 0.5}, {"id": 2, "y": 3}])        # 欄位 id, x, y

# 4. 巢狀 dict：外層 key 當列
counts = {"S1": {"TP53": 120, "BRCA1": 30}, "S2": {"TP53": 98, "BRCA1": 41}}
pd.DataFrame.from_dict(counts, orient="index")                # 列 = 樣本、欄 = 基因

# 5. NumPy array + 標籤
rng = np.random.default_rng(0)
expr = pd.DataFrame(
    rng.poisson(10, size=(3, 4)),
    index=["S1", "S2", "S3"],
    columns=["TP53", "BRCA1", "EGFR", "MYC"],
)

# 6. 建立時指定 dtype
pd.DataFrame({"id": [1, 2], "grp": ["a", "b"]}).astype({"id": "int32", "grp": "category"})
```

> dict 中各 list 長度不同會 `ValueError: All arrays must be of the same length`；Series 不同長度則會依 index 對齊、補 NaN。

## Index 與欄名

```python
df = pd.DataFrame([[5.1, 3.5], [4.9, 3.0], [4.7, 3.2]])
df.index = ["row1", "row2", "row3"]
df.columns = ["sepal_length", "sepal_width"]

df = df.rename(columns={"sepal_length": "sl"})        # 改部分欄名
df.columns = df.columns.str.lower().str.replace(" ", "_")   # 批次清理欄名
df.index.name = "sample_id"

df = df.reset_index()                                 # index → 欄（sample_id 變成一般欄）
df = df.set_index("sample_id")                        # 欄 → index
```

index 的進階操作見 [Index 與 MultiIndex](index-multiindex.md)。

## 練習用資料集

```python
import seaborn as sns
iris = sns.load_dataset("iris")             # 也有 tips、penguins、titanic…（需網路，第一次下載後快取）

from sklearn.datasets import load_diabetes
diabetes = load_diabetes(as_frame=True).frame
```

本章其他筆記多以 iris（150 列、4 個數值欄 + `species`）示範。
