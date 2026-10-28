[Python Foundations](../README.md) › [pandas](README.md) › 修改資料

# 修改資料 (Updating, Adding & Removing)

修改 DataFrame 時最大的坑不是語法，而是「改到的是原表還是副本」。pandas 3 起 Copy-on-Write 是唯一行為，規則變簡單了：**只有對原物件直接用 `.loc` / `.iloc` / `[]` 賦值才會改到它**。

## View vs Copy 與 Copy-on-Write

```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2, 3], "b": [4.0, 5.0, 6.0]})

# 1. 從 df 取出的任何子集合，修改它都不會影響 df
sub = df[df["a"] > 1]
sub["a"] = 0                  # 只改 sub；不再有 SettingWithCopyWarning
s = df["a"]
s.iloc[0] = -1                # 只改 s；df 不變

# 2. 鏈式賦值 (chained assignment) 永遠不會成功
df["a"][0] = 100              # ChainedAssignmentError 警告，df 不變
df[df["a"] > 1]["b"] = 0      # 同上
df["a"].replace(1, 100, inplace=True)   # 同上：對中間物件 inplace

# 3. 正確寫法：一步到位
df.loc[0, "a"] = 100
df.loc[df["a"] > 1, "b"] = 0
df["a"] = df["a"].replace(1, 100)
```

| 寫法 | pandas < 3（舊行為） | pandas ≥ 3（Copy-on-Write） |
| --- | --- | --- |
| `sub = df[mask]; sub["x"] = 0` | `SettingWithCopyWarning`，可能改到 df | 只改 sub |
| `df["x"][0] = 0` | 有時改得到、有時改不到 | 永遠改不到，發出警告 |
| `df.loc[mask, "x"] = 0` | 改 df | 改 df |
| `df.copy()` 後再改 | 必要的防禦性寫法 | 多數情況不再需要 |
| `df["x"].to_numpy()` | 可寫入、可能改到 df | 回傳**唯讀** array；要寫入用 `.to_numpy(copy=True)` |

> CoW 的 copy 是延遲的：取子集合時不複製，等到真的被修改才複製，所以不再需要為了安全到處 `.copy()`。仍在用 pandas 2.x 時可用 `pd.options.mode.copy_on_write = True` 提前啟用。NumPy 本身的 view 規則不同，見 [NumPy view vs copy](../numpy/array-basics.md#view-vs-copy)。

## 更新值

```python
import seaborn as sns
iris = sns.load_dataset("iris")

# 依條件
iris.loc[iris["species"] == "setosa", "sepal_length"] = 6.0
iris.loc[iris["petal_width"] < 1.0, "petal_length"] += 0.5
iris.loc[(iris["species"] == "versicolor") & iris["sepal_length"].isna(), "sepal_length"] = 0

# 依位置 / 標籤的單一格（較快）
iris.iloc[0, 1] = 3.5
iris.at[0, "petal_width"] = 0.4
iris.iat[1, 2] = 1.5

# 整欄依條件改：回傳新 Series 再賦值
iris["sepal_length"] = iris["sepal_length"].where(iris["sepal_length"] < 7, 7)   # 不符合條件的換成 7
iris["sepal_length"] = iris["sepal_length"].mask(iris["sepal_length"] < 0)       # 符合條件的換成 NaN
```

## 取代與對應 (Replace & Map)

```python
s = pd.Series([1, 2, 3])
s.replace({1: "a"})           # ['a', 2, 3]：沒列到的保留原值
s.map({1: "a"})               # ['a', nan, nan]：沒列到的變 NaN

iris["species"] = iris["species"].replace({"virginica": "VIR", "setosa": "SET"})
iris["species"] = iris["species"].str.replace("versi", "VERSI", regex=False)   # 子字串
iris["length_label"] = iris["sepal_length"].map(lambda x: "short" if x < 5.5 else "long")
```

| 方法 | 作用於 | 沒對到的值 | 用途 |
| --- | --- | --- | --- |
| `replace(dict)` | Series / DataFrame | 保留 | 修正少數錯誤值 |
| `map(dict / func)` | Series | NaN | 完整的對照表（可藉 NaN 抓漏網值）、逐元素函式 |
| `.str.replace` | 字串 Series | 保留 | 子字串、regex |
| `DataFrame.map(func)` | DataFrame 每一格 | | 逐格函式（舊名 `applymap`，pandas 3 已移除） |
| `apply(func, axis=1)` | 每一列 | | 需要多欄的邏輯；慢，見 [效能](performance.md) |

```python
num = iris.select_dtypes("number")
num.map(lambda x: x * 2)      # 逐格；這個例子直接寫 num * 2 更快
iris["ratio"] = iris.apply(lambda r: r["sepal_length"] / r["sepal_width"], axis=1)  # 可行但慢
iris["ratio"] = iris["sepal_length"] / iris["sepal_width"]                          # 向量化
```

## 新增欄

```python
iris["sepal_area"] = iris["sepal_length"] * iris["sepal_width"]   # 運算結果
iris["dataset"] = "iris"                                          # 常數
iris.insert(0, "id", range(len(iris)))                            # 指定位置

# assign：回傳新 DataFrame，適合方法鏈 (method chaining)
result = (
    iris
    .assign(
        petal_ratio=lambda d: d["petal_length"] / d["petal_width"],
        is_long=lambda d: d["petal_ratio"] > 5,                  # 可引用同一個 assign 前面建的欄
    )
    .query("is_long")
)
```

`lambda d:` 讓 `assign` 使用鏈中「當下」的 DataFrame，而不是最初的 `iris`。

## 刪除欄與列

```python
iris.drop(columns=["dataset", "sepal_area"])         # 刪欄（比 axis=1 易讀）
iris.drop(index=[0, 1])                              # 依 index 標籤刪列
iris.drop(iris[iris["sepal_length"] > 7.5].index)    # 依條件刪列
iris = iris[iris["sepal_length"] <= 7.5]             # 同上：保留想要的列，通常更直接
iris.drop(columns=["x"], errors="ignore")            # 欄不存在時不報錯
```

## 新增列

```python
new_rows = pd.DataFrame({
    "sepal_length": [5.0, 6.5], "sepal_width": [3.5, 3.0],
    "petal_length": [1.3, 5.2], "petal_width": [0.2, 2.0],
    "species": ["setosa", "virginica"],
})
iris = pd.concat([iris, new_rows], ignore_index=True)   # DataFrame.append 已在 pandas 2.0 移除
```

> 不要在迴圈中逐列 `concat`（每次都複製整張表，O(n²)）。把每列先收進 list of dicts，最後一次建表：`pd.DataFrame(rows)`。

## 改欄名

```python
iris.rename(columns={"sepal_length": "sl"})
iris.rename(columns=str.upper)                        # 對每個欄名套函式
iris.columns = iris.columns.str.replace("_", ".")
iris.add_prefix("x_"), iris.add_suffix("_cm")
```

## `inplace=True`

| | `inplace=True` | 回傳新物件再賦值 |
| --- | --- | --- |
| 寫法 | `df.dropna(inplace=True)` | `df = df.dropna()` |
| 回傳 | `None`（`x = df.sort_values(..., inplace=True)` 會讓 x 變 None） | 新物件 |
| 方法鏈 | 不行 | 可以 |
| 效能 | 通常沒有比較快 | |

建議一律用「回傳新物件再賦值」；pandas 官方也不建議 `inplace`。
