[資料處理與 EDA](../../README.md) › [視覺化](../README.md) › Seaborn

# Seaborn

建立在 Matplotlib 之上的統計繪圖套件：直接吃長格式 (long format) DataFrame，用 `hue`、`col` 等參數把欄位對應到顏色與子圖，並自動計算平均、信賴區間、KDE、迴歸線。本章以 Seaborn 0.13 為準。

```text
基礎（figure-level vs axes-level、hue、主題）→ 分布 → 類別 → 關係 → 迴歸 → 矩陣
```

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [基礎](basics.md) | 函式家族、figure-level vs axes-level、`hue`、主題、圖例 | Seaborn 的 API 怎麼組織？ |
| [分布圖](distribution.md) | `histplot`、`kdeplot`、`ecdfplot`、`displot`、bins 與頻寬 | 單一變數長什麼樣？各組分布怎麼比？ |
| [類別圖](categorical.md) | count / bar / box / violin / strip / point、`errorbar` | 類別與數值的關係？ |
| [關係圖](relational.md) | `scatterplot`、`lineplot`、`relplot`、facet | 兩個連續變數、時間趨勢？ |
| [迴歸圖](regression.md) | `regplot`、`lmplot`、`residplot`、診斷圖 | 線性關係多強？模型假設成立嗎？ |
| [矩陣圖](matrix.md) | `heatmap`、`clustermap`、`pairplot` | 多變數之間的關係？樣本 / 基因怎麼分群？ |

## 函式家族

| 家族 | figure-level（回傳 `FacetGrid`，可 `col=` / `row=`） | axes-level（回傳 `Axes`，可 `ax=`） |
| --- | --- | --- |
| 分布 | `displot(kind=)` | `histplot`、`kdeplot`、`ecdfplot`、`rugplot` |
| 類別 | `catplot(kind=)` | `countplot`、`barplot`、`boxplot`、`violinplot`、`stripplot`、`swarmplot`、`pointplot`、`boxenplot` |
| 關係 | `relplot(kind=)` | `scatterplot`、`lineplot` |
| 迴歸 | `lmplot` | `regplot`、`residplot` |
| 矩陣 | `clustermap`、`pairplot`、`jointplot` | `heatmap` |

## Seaborn vs Matplotlib

| | Seaborn | Matplotlib |
| --- | --- | --- |
| 輸入 | 長格式 DataFrame + 欄名 | 陣列 |
| 分組 | `hue=` 一個參數 | 自己迴圈 |
| 統計 | 自動算平均、CI、KDE、迴歸 | 自己算 |
| 細節控制 | 有限，要回到 `ax` | 完整 |

> Seaborn 讓畫圖變快，但不會判斷這張圖是否適合你的問題；選圖見 [圖表設計原則](../chart-design-principles.md)。寬表（基因 × 樣本）要先 `melt` 成長格式才能用 `hue`，見 [pandas Reshape](../../../python-foundations/pandas/reshape-merge.md)。
