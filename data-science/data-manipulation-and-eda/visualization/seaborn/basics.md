[視覺化](../README.md) › [Seaborn](README.md) › 基礎

# Seaborn 基礎 (Basics)

Seaborn 的核心是「把 DataFrame 的欄位對應到圖的視覺屬性」：`x`、`y` 決定位置，`hue` 決定顏色，`col` / `row` 決定子圖。底層的 figure / axes 概念見 [Matplotlib 基礎](../matplotlib/basics.md)。

## 資料格式：長格式

```python
import seaborn as sns
import matplotlib.pyplot as plt

iris = sns.load_dataset("iris")     # 內建資料：iris、tips、penguins、flights、titanic…（需連網下載）

# 寬表 → 長表：一列 = 一個觀測值，才能用欄名對應 hue / col
long = iris.melt(id_vars="species", var_name="feature", value_name="cm")
sns.boxplot(data=long, x="feature", y="cm", hue="species")
```

| 參數 | 對應到 |
| --- | --- |
| `x`、`y` | 位置 |
| `hue` | 顏色（類別或數值） |
| `size`、`style` | 點大小、點形 / 線型（關係圖） |
| `col`、`row`、`col_wrap` | 子圖（只有 figure-level 函式） |
| `order`、`hue_order` | 類別順序 |
| `palette` | 色盤名稱、list，或 `{類別: 顏色}` dict |

## figure-level vs axes-level

| | figure-level | axes-level |
| --- | --- | --- |
| 例子 | `relplot`、`catplot`、`displot`、`lmplot` | `scatterplot`、`boxplot`、`histplot`、`regplot` |
| 回傳 | `FacetGrid`（`g`） | Matplotlib `Axes`（`ax`） |
| 子圖 | `col=` / `row=` 自動切 | 用 `ax=` 放進自己建立的 `plt.subplots` |
| 尺寸 | `height=`、`aspect=`（每個子圖） | 由 `figsize` 決定 |
| 標題 / 標籤 | `g.set(...)`、`g.set_titles("{col_name}")`、`g.figure.suptitle(...)` | `ax.set(...)`、`ax.set_title(...)` |

```python
# figure-level：自動 facet
g = sns.catplot(data=iris, x="species", y="petal_length", kind="box", col="species", height=3)
g.set(xlabel="", ylabel="Petal length (cm)")
g.set_titles("{col_name}")
g.figure.suptitle("Petal length by species", y=1.05)   # 建議用 .figure（.fig 為舊名）

# axes-level：放進自訂版面
fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
sns.histplot(data=iris, x="sepal_length", hue="species", ax=axes[0])
sns.scatterplot(data=iris, x="sepal_length", y="petal_length", hue="species", ax=axes[1])
axes[1].set(title="Sepal vs petal", xlabel="Sepal length (cm)")
```

## hue 與顏色

```python
tips = sns.load_dataset("tips")
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="smoker",
                hue_order=["No", "Yes"], palette={"No": "gray", "Yes": "tomato"})

sns.scatterplot(data=tips, x="total_bill", y="tip", hue="size", palette="viridis")  # 數值 hue → 連續色盤
```

## 圖例

| 想做 | 寫法 |
| --- | --- |
| 不要圖例 | `sns.scatterplot(..., legend=False)` |
| 移到圖外 | `sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))`（`ax` 或 `g` 都可） |
| 改標題 | `sns.move_legend(ax, "best", title="Smoker")` |
| 移除已畫的 | axes-level：`ax.get_legend().remove()`；figure-level：`g.legend.remove()` |

## 主題 (Theme)

```python
sns.set_theme(style="whitegrid", palette="colorblind", context="notebook", font_scale=1.1)
sns.set_style("ticks")            # 只改背景與格線："white"、"dark"、"whitegrid"、"darkgrid"、"ticks"
sns.set_context("talk")           # 字與線的大小："paper" < "notebook" < "talk" < "poster"
sns.despine()                     # 移除上、右框線
with sns.axes_style("white"):     # 只影響這個區塊
    sns.histplot(data=iris, x="sepal_length")
```

> 主題設定是**全域**的，會影響之後所有 Matplotlib 圖。`sns.set()` 是 `sns.set_theme()` 的舊別名；`sns.reset_defaults()` 回到 Matplotlib 預設。
