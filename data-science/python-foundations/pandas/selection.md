[Python Foundations](../README.md) › [pandas](README.md) › 選取與篩選

# 選取與篩選 (Selection & Filtering)

pandas 有標籤 (label) 與位置 (position) 兩套選取方式；混用是最常見的錯誤來源。原則：選欄用 `df[...]`，選列或同時選列欄用 `.loc`（標籤）或 `.iloc`（位置）。純位置的 array 索引見 [NumPy Array 基礎](../numpy/array-basics.md#索引與切片-indexing--slicing)。

```python
import pandas as pd

df = pd.DataFrame(
    {"name": ["Bella", "Charlie", "Lucy"], "height_cm": [56, 43, 46], "weight_kg": [24, 22, 24]},
    index=["dog1", "dog2", "dog3"],
)
```

## 選取速查

| 想做的事 | 寫法 | 回傳 |
| --- | --- | --- |
| 一欄 | `df["name"]` | Series |
| 多欄 | `df[["name", "weight_kg"]]` | DataFrame |
| 依 dtype 選欄 | `df.select_dtypes(include="number")` | DataFrame |
| 依欄名模式選欄 | `df.filter(like="_cm")`、`df.filter(regex="^h")` | DataFrame |
| 一個值（標籤 / 位置） | `df.at["dog1", "name"]` / `df.iat[0, 0]` | 純量 |
| 列 + 欄（標籤） | `df.loc["dog1":"dog2", ["name"]]` | DataFrame |
| 列 + 欄（位置） | `df.iloc[0:2, [0]]` | DataFrame |
| 前 / 後幾列 | `df.head(2)` / `df.tail(2)` | DataFrame |

## `.loc`（標籤）與 `.iloc`（位置）

```python
# .loc：用 index 標籤與欄名，切片「包含」終點
df.loc["dog1", "weight_kg"]                  # 24
df.loc["dog1"]                               # 整列 → Series
df.loc[["dog1", "dog3"], ["name", "height_cm"]]
df.loc["dog1":"dog2"]                        # dog1、dog2 都包含
df.loc[:, "name":"height_cm"]                # 欄名也能切片

# .iloc：用整數位置，切片「不包含」終點（同 Python）
df.iloc[0, 1]                                # 56
df.iloc[:2]                                  # 前兩列
df.iloc[[0, 2], [0, 2]]
df.iloc[:, 2]                                # Series
df.iloc[:, [2]]                              # DataFrame（用 list 保留維度）
df.iloc[-1]                                  # 最後一列
```

| | `.loc` | `.iloc` |
| --- | --- | --- |
| 依據 | index 標籤、欄名、布林遮罩 | 整數位置 |
| 切片終點 | **包含** | 不包含 |
| index 是整數（0, 1, 2…）時 | `df.loc[0]` 是「標籤為 0」的列 | `df.iloc[0]` 是「第一列」 |

> 篩選或排序後 index 不再是 0..n-1，`df.loc[0]` 可能 `KeyError` 或拿到別列。要「第幾列」一律用 `.iloc`；需要時先 `reset_index(drop=True)`。

## 布林篩選

```python
import seaborn as sns
iris = sns.load_dataset("iris")

iris[iris["sepal_length"] > 5.0]
iris[(iris["petal_length"] >= 1.5) & (iris["petal_length"] <= 2.0)]   # & | ~，每個條件加括號
iris[iris["petal_length"].between(1.5, 2.0)]                          # 同上（預設兩端都包含）
iris[iris["species"].isin(["setosa", "virginica"])]
iris[~iris["species"].isin(["setosa"])]                               # 不在清單中

# 篩列同時選欄：用 .loc
iris.loc[iris["sepal_width"] > 3.5, ["species", "sepal_width"]]

# query：條件多時較易讀；@ 引用 Python 變數
threshold = 3.5
iris.query("sepal_width > @threshold or petal_width < 0.2")
iris.query("species in ['setosa', 'virginica']")
```

| 錯誤寫法 | 問題 | 正確寫法 |
| --- | --- | --- |
| `df[df.a > 1 and df.b < 2]` | `and` 不能用在 Series | `df[(df.a > 1) & (df.b < 2)]` |
| `df[df.a > 1 & df.b < 2]` | `&` 優先順序高於 `>` | 每個條件加括號 |
| `df[df.a == None]` | 缺值不等於任何值 | `df[df.a.isna()]` |

## 字串條件

```python
s = iris["species"]
iris[s.str.contains("osa")]                   # 預設當 regex
iris[s.str.contains("se|gi")]                 # 含 se 或 gi
iris[s.str.startswith("v")]                   # 開頭
iris[s.str.endswith("ca")]                    # 結尾
iris[s.str.contains("SETOSA", case=False)]    # 不分大小寫
iris[s.str.contains("v.", regex=False)]       # 字面比對（含 . 等特殊字元時）
iris[s.str.contains("osa", na=False)]         # 缺值視為 False，避免遮罩中出現 NaN
```

`.str` 的完整用法見 [dtype、類別與字串](dtypes-categorical-strings.md#字串操作-str)；regex 語法見 [文字清理與 Regex](../text-cleaning-and-regex.md)。

## 依條件產生新欄

```python
import numpy as np

iris["is_setosa"] = iris["species"] == "setosa"                     # 布林欄，不需要 np.where
iris["size"] = np.where(iris["petal_length"] > 4, "large", "small") # 二選一
iris["size_group"] = np.select(
    [iris["petal_length"] < 2, iris["petal_length"] <= 5],          # 依序判斷，取第一個成立的
    ["small", "medium"],
    default="large",
)
iris["capped"] = iris["sepal_length"].clip(upper=7)                 # 截斷
iris["sl_or_nan"] = iris["sepal_length"].where(iris["sepal_length"] > 5)   # 不符合 → NaN
```

數值切成區間用 [`pd.cut`](ordering-binning-sampling.md#分箱-binning)，比 `np.select` 更適合。

## MultiIndex 選取

```python
dogs = df.set_index(["name", "height_cm"]).sort_index()     # 切片前要先排序
dogs.loc[("Bella", 56)]                     # 一個完整 key
dogs.loc[[("Bella", 56), ("Lucy", 46)]]     # 多個 key
dogs.loc["Bella":"Charlie"]                 # 第一層切片，包含 Charlie
dogs.xs("Lucy", level="name")               # 取某層的某值
```

更多見 [Index 與 MultiIndex](index-multiindex.md)。
