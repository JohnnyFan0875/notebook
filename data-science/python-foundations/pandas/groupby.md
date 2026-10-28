[Python Foundations](../README.md) › [pandas](README.md) › 分組彙總

# 分組彙總 (GroupBy & Aggregation)

`groupby` 是 split-apply-combine：依 key 把列分組 → 對每組套用函式 → 把結果組回來。關鍵是分清楚三種輸出：每組一個值（`agg`）、每列一個值（`transform`）、保留或丟掉整組（`filter`）。

```text
            split               apply                     combine
df ──groupby("species")──▶ setosa     ─┬─ agg       → 每組 1 列（3 列）
                           versicolor ─┼─ transform → 對齊原表（150 列）
                           virginica  ─┴─ filter    → 保留符合條件的整組
```

| 方法 | 輸出列數 | 用途 | SQL / dplyr 對應 |
| --- | --- | --- | --- |
| `agg` / `mean` / `size`… | 組數 | 每組摘要 | `GROUP BY` / `summarise` |
| `transform` | 與原表相同 | 組內標準化、組平均貼回每列、組內補值 | window function `OVER (PARTITION BY)` / `group_by + mutate` |
| `filter` | ≤ 原表 | 只留符合條件的組 | `HAVING` / `group_by + filter` |
| `apply` | 不定 | 上面都做不到時的萬用解；最慢 | |

## 基本彙總

```python
import pandas as pd
import seaborn as sns

iris = sns.load_dataset("iris")

iris.groupby("species")["sepal_length"].mean()       # setosa 5.006, versicolor 5.936, virginica 6.588
iris.groupby("species")["sepal_length"].agg(["mean", "std"])
iris.groupby("species").size()                       # 每組列數（含缺值）
iris.groupby("species")["sepal_length"].count()      # 每組非缺值數
iris.groupby("species")["sepal_width"].describe()
iris.groupby(["species", "sepal_width"])[["petal_length", "petal_width"]].mean()   # 多個 key

# 結果要當一般欄位用（畫圖、merge）時
iris.groupby("species", as_index=False)["sepal_length"].mean()
iris.groupby("species")["sepal_length"].mean().reset_index()      # 同上
```

## 多個彙總與命名 (Named Aggregation)

```python
iris.groupby("species").agg(
    sl_mean=("sepal_length", "mean"),               # 新欄名=(欄, 函式)
    n=("sepal_length", "size"),
    pl_q90=("petal_length", lambda s: s.quantile(0.9)),
)
#             sl_mean   n  pl_q90
# setosa         5.01  50    1.70
# versicolor     5.94  50    4.80
# virginica      6.59  50    6.31

# dict 寫法：欄名會變成 MultiIndex（('sepal_length', 'mean')…），通常不如上面好用
iris.groupby("species").agg({"sepal_length": ["mean", "max"], "petal_length": "sum"})
```

自訂函式可直接傳入；要放進 list 時，函式名稱會成為欄名：

```python
def pct30(s):
    return s.quantile(0.3)

iris.groupby("species")["sepal_length"].agg([pct30, "median"])
```

## Transform：結果對齊回原表

```python
g = iris.groupby("species")["petal_length"]

iris["pl_group_mean"] = g.transform("mean")                    # 每列填入所屬組的平均
iris["pl_centered"] = iris["petal_length"] - g.transform("mean")
iris["pl_z"] = g.transform(lambda s: (s - s.mean()) / s.std())  # 組內 z-score
iris["pl_rank"] = g.rank(ascending=False)                      # 組內排名
iris["pl_share"] = iris["petal_length"] / g.transform("sum")   # 占組內總和的比例
iris["pl_filled"] = g.transform(lambda s: s.fillna(s.median()))  # 組內中位數補值
iris["cum"] = g.cumsum()                                       # 組內累計（cumsum / cumcount / shift / diff 也是對齊原表）
```

> 生資常見用法：依批次 (batch) 或樣本做組內標準化、計算每個基因在組內的 log fold change。若是要校正批次效應，簡單的組內中心化不一定夠，見 [批次效應](../../statistics/experimental-design/confounding-bias.md#生資最常見的干擾批次效應-batch-effect)。

## Filter：保留整組

```python
iris.groupby("species").filter(lambda g: g["sepal_length"].mean() > 5.5)   # 100 列：versicolor + virginica
df.groupby("gene").filter(lambda g: (g["count"] >= 10).sum() >= 3)        # 至少 3 個樣本 count ≥ 10 的基因

iris.groupby("species").head(2)                    # 每組前 2 列
iris.groupby("species").nth(0)                     # 每組第 1 列
iris.sort_values("sepal_length").groupby("species").tail(1)   # 每組最大的那列
iris.loc[iris.groupby("species")["sepal_length"].idxmax()]    # 同上
```

## 布林平均 = 比例

布林欄的 `mean()` 就是事件比例（True = 1、False = 0），回答「多少比例的列符合條件」最簡潔：

```python
(iris["sepal_length"] > 6).groupby(iris["species"]).mean()
# setosa 0.0, versicolor 0.4, virginica 0.82

df.groupby("district")["is_arrested"].mean()                 # 各區逮捕率
df.groupby(["cohort", "arm"])["responded"].mean()            # 各組反應率
```

## 分組的 key

```python
iris.groupby(pd.cut(iris["sepal_length"], [4, 6, 8]), observed=True).size()   # 依區間分組
df.groupby(df["date"].dt.year)["value"].sum()                                  # 依衍生的 Series
df.groupby(level="sample").sum()                                               # 依 index 層級
df.groupby("grp", dropna=False).size()                                         # 預設會丟掉 key 為 NaN 的列

# 分組 + 時間重採樣
iris["date"] = pd.date_range("2024-01-01", periods=len(iris), freq="D")
iris.groupby("species").resample("ME", on="date")["sepal_length"].mean()       # 每組每月平均；"M" 已改名為 "ME"
```

| 陷阱 | 說明 |
| --- | --- |
| key 有缺值 | 預設 `dropna=True`，那些列靜靜消失；用 `dropna=False` 保留 |
| key 是 category | pandas 3 預設 `observed=True` 只顯示出現過的類別；要列出 0 筆的類別用 `observed=False` |
| `size()` vs `count()` | `size` 含缺值、`count` 不含；兩者差異就是缺值數 |
| `apply` 很慢 | 能用內建字串名稱（`"mean"`、`"sum"`）就不要用 lambda，內建的有最佳化 |

## 試算表的樞紐分析表

`groupby` 就是最基本的 pivot table：列 = key、值 = 欄、摘要 = 函式。要把第二個 key 攤成欄時用 `pivot_table` 或 `.unstack()`，見 [Reshape 與 Merge](reshape-merge.md#pivot-與-pivot_table)。

```python
sales.groupby("store")["revenue"].sum()                         # 列：store、值：revenue、摘要：sum
sales.groupby(["store", "month"])["revenue"].sum().unstack()    # month 攤成欄
```
