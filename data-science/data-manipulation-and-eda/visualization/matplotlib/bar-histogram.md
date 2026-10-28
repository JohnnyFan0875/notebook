[視覺化](../README.md) › [Matplotlib](README.md) › 長條圖與直方圖

# 長條圖與直方圖 (Bar Plot & Histogram)

兩者外觀相似、用途不同：

| | 長條圖 (bar plot) | 直方圖 (histogram) |
| --- | --- | --- |
| x 軸 | 類別（離散） | 連續數值切成區間 (bins) |
| 長條之間 | 有間隔，順序可調整 | 相鄰無間隔，順序固定 |
| 高度代表 | 次數或某個摘要值（平均、總和） | 落在該區間的次數（或密度） |
| Matplotlib | `ax.bar` / `ax.barh` | `ax.hist` |
| Seaborn | `countplot` / `barplot` | `histplot` |

## 長條圖

```python
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

iris = sns.load_dataset("iris")
tips = sns.load_dataset("tips")

fig, axes = plt.subplots(1, 3, figsize=(14, 4), layout="constrained")

# 1. 排序後的水平長條圖：類別名稱長時比垂直好讀
counts = tips["day"].value_counts().sort_values()
axes[0].barh(counts.index.astype(str), counts.values, color="steelblue")
axes[0].bar_label(axes[0].containers[0])            # 在長條末端標數值

# 2. 分組長條：pandas 寬表直接 .plot.bar，每欄一組顏色
means = iris.groupby("species").mean()               # 3 物種 × 4 特徵
means.T.plot.bar(ax=axes[1], rot=0)
axes[1].set_ylabel("Mean (cm)")

# 3. 堆疊長條：bottom= 指定起點
ct = tips.groupby(["day", "sex"], observed=True).size().unstack()
axes[2].bar(ct.index.astype(str), ct["Male"], label="Male")
axes[2].bar(ct.index.astype(str), ct["Female"], bottom=ct["Male"], label="Female")
axes[2].legend()
```

| 想做 | 寫法 |
| --- | --- |
| 手動分組（並排） | `x = np.arange(n)`；`ax.bar(x - w/2, a, w)`、`ax.bar(x + w/2, b, w)`；`ax.set_xticks(x, labels)` |
| 比例堆疊（每根 100%） | `ct.div(ct.sum(axis=1), axis=0).plot.bar(stacked=True)` |
| 誤差線 | `ax.bar(x, mean, yerr=sd, capsize=4)` |

> 長條圖的 y 軸要從 0 開始；只畫平均的長條圖會藏住分布，n 小時改畫原始點，見 [圖表設計原則](../chart-design-principles.md#常見誤導)。

## 直方圖

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")

# 1. 單一變數；bins 可給數字、邊界陣列或規則字串
axes[0].hist(iris["sepal_length"], bins="auto", color="steelblue", edgecolor="white")

# 2. 多組疊加：共用 bins 才能比較，並用 density=True 消除樣本數差異
bins = np.histogram_bin_edges(iris["sepal_length"], bins=20)
for species, d in iris.groupby("species"):
    axes[1].hist(d["sepal_length"], bins=bins, alpha=0.5, density=True, label=species)
axes[1].legend()
```

| 參數 | 用途 |
| --- | --- |
| `bins` | 預設 10；`"auto"`、`"fd"`（Freedman–Diaconis，對離群值穩健）、`"sturges"`，或邊界陣列 |
| `density=True` | 高度改為密度（總面積 = 1），不同 n 的組才能比較 |
| `cumulative=True` | 累積分布 |
| `histtype="step"` | 只畫外框，多組疊加時比半透明清楚 |
| `log=True` | y 軸 log，看長尾 |

> bin 數會改變直方圖的形狀，太少會藏住雙峰；比較不同 bin 的效果見 [Seaborn 分布圖](../seaborn/distribution.md#bins-與頻寬)。直方圖加 KDE 曲線也用 Seaborn 的 `histplot(kde=True)` 較方便。
