[視覺化](../README.md) › [Seaborn](README.md) › 類別圖

# 類別圖 (Categorical Plots)

x（或 y）是類別、另一軸是數值或次數的圖。`catplot(kind=...)` 是 figure-level 入口，各 `kind` 也有對應的 axes-level 函式。類別順序與編碼的資料處理見 [pandas dtype 與類別](../../../python-foundations/pandas/dtypes-categorical-strings.md)。

## 選哪一種

| `kind` / 函式 | 呈現 | 適用 | 注意 |
| --- | --- | --- | --- |
| `count` / `countplot` | 每類次數 | 類別分布、不平衡 | 連續變數改用 `histplot`，見 [類別 vs 連續](distribution.md#類別-vs-連續) |
| `bar` / `barplot` | 平均 + 誤差線 | 摘要報告 | 藏住分布，n 小時不建議單獨使用 |
| `point` / `pointplot` | 平均 + 誤差線，以線相連 | 交互作用（兩因子的平均如何變化） | 連線只代表同一 `hue` 組 |
| `box` / `boxplot` | 五數摘要 + 離群值 | 多組分布比較 | 看不到雙峰，見 [箱型圖](../matplotlib/box-plot.md) |
| `violin` / `violinplot` | 箱型 + KDE | 中大樣本的形狀 | n 小時 KDE 不可靠 |
| `boxen` / `boxenplot` | 更多分位數的箱型 | 大樣本（數千以上）的尾巴 | — |
| `strip` / `stripplot` | 每個點（加 jitter） | n 小（< 100 / 組） | 點多會重疊 |
| `swarm` / `swarmplot` | 每個點，不重疊排列 | n 小 | 點太多時排不下會警告 |

## 寫法

```python
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

iris = sns.load_dataset("iris")
tips = sns.load_dataset("tips")
fig, axes = plt.subplots(2, 2, figsize=(11, 8), layout="constrained")

# 1. 次數：order 指定順序；改用 y= 變水平
sns.countplot(data=tips, y="day", order=["Thur", "Fri", "Sat", "Sun"], ax=axes[0, 0])

# 2. 平均 ± SD 的長條圖（errorbar 見下表）
sns.barplot(data=iris, x="species", y="sepal_length", errorbar="sd", ax=axes[0, 1])

# 3. 箱型 + 原始點：最推薦的組合
sns.boxplot(data=iris, x="species", y="petal_length", showfliers=False, color="lightgray", ax=axes[1, 0])
sns.stripplot(data=iris, x="species", y="petal_length", alpha=0.5, ax=axes[1, 0])

# 4. 點圖看交互作用；estimator 改成中位數
sns.pointplot(data=tips, x="day", y="tip", hue="sex", estimator=np.median,
              errorbar=("ci", 95), dodge=True, capsize=0.1, ax=axes[1, 1])

# figure-level：facet
sns.catplot(data=tips, x="day", y="total_bill", hue="sex", col="time", kind="violin", split=True)
```

## 誤差線 `errorbar`

Seaborn 0.12 起用 `errorbar=` 取代舊的 `ci=`：

| 寫法 | 意義 | 描述的是 |
| --- | --- | --- |
| `("ci", 95)`（預設） | bootstrap 95% 信賴區間 | 平均數估得多準（推論） |
| `("se", 1)` | ± 1 個標準誤 | 同上，較窄 |
| `("sd", 1)` / `"sd"` | ± 1 個標準差 | 資料本身的分散（描述） |
| `("pi", 50)` | 中間 50% 的百分位區間 | 資料本身的分散 |
| `None` | 不畫 | — |

> 預設的 CI 是 bootstrap 抽樣算的，每次執行可能略有不同；需要可重現時加 `seed=`。SD 與 SE 的差別見 [SD vs SE](../../../statistics/descriptive-statistics/univariate-numerical.md#標準差-vs-標準誤-sd-vs-se)。

## 常用參數

| 參數 | 用途 |
| --- | --- |
| `order` / `hue_order` | 類別順序（類別型欄位預設依 categories 順序） |
| `dodge=True` | `hue` 各組並排而非重疊 |
| `estimator` | 摘要統計（`bar` / `point`），預設 `"mean"` |
| `whis`、`showfliers` | 箱型圖鬚長、是否畫離群點（傳給 Matplotlib） |
| `linestyle="none"` | 點圖不連線（0.13 起取代 `join=False`） |
| `capsize` | 誤差線端帽寬度 |
| `split=True` | violin 兩個 `hue` 組各畫一半 |
| `inner=` | violin 內部：`"box"`、`"quart"`、`"point"`、`None` |
| `native_scale=True` | x 為數值時保留原本間距（0.13+） |

| 舊寫法（會警告或報錯） | 新寫法 |
| --- | --- |
| `ci="sd"`、`ci=None` | `errorbar="sd"`、`errorbar=None` |
| `join=False` | `linestyle="none"` |
| `sym=""`（Matplotlib `ax.boxplot` 的參數，傳給 Seaborn 會報錯） | `showfliers=False` |

## 先彙總再畫

資料已經在 pandas 彙總好（每組一列）時，`barplot` 只會畫出該值、沒有誤差線：

```python
totals = tips.groupby("day", observed=True, as_index=False)["total_bill"].sum()
sns.barplot(data=totals, x="day", y="total_bill")
```
