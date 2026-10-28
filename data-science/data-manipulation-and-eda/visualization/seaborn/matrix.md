[視覺化](../README.md) › [Seaborn](README.md) › 矩陣圖

# 矩陣圖 (Matrix Plots)

一次看多個變數或一整個矩陣：`heatmap` 畫數值矩陣（相關矩陣、表現量），`clustermap` 再加上階層式分群，`pairplot` 畫所有變數兩兩的散布圖。多變數 EDA 的整體策略見 [多變量探索](../../../statistics/multivariate-analysis/multivariate-eda.md)。

## Heatmap：相關矩陣

```python
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

iris = sns.load_dataset("iris")
corr = iris.corr(numeric_only=True)          # pandas ≥ 2.0：有字串欄時必須 numeric_only=True

mask = np.triu(np.ones_like(corr, dtype=bool), k=1)   # 只畫下三角，避免重複
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f",
            cmap="RdBu_r", vmin=-1, vmax=1, center=0, square=True, linewidths=0.5)
```

| 參數 | 用途 |
| --- | --- |
| `annot=True`、`fmt=".2f"` | 格子內顯示數值與格式 |
| `cmap` | 有正負的值用 diverging（`RdBu_r`、`vlag`），只有正值用 sequential（`viridis`） |
| `vmin`、`vmax`、`center` | 色階範圍；相關矩陣固定 −1 到 1、中心 0，不同圖才能比較 |
| `mask` | 隱藏部分格子（上三角、不顯著的值） |
| `square=True`、`linewidths` | 正方形格子、格線 |
| `cbar_kws={"label": ...}` | 色條標籤與大小 |

> 不設 `vmin` / `vmax` 時色階依資料最小最大值自動縮放，0.3 的相關可能被畫成深紅；顏色深淺沒有固定意義。

## Clustermap：表現量矩陣

基因 × 樣本的表現量 heatmap（生資最常見的圖之一）要先決定**怎麼標準化**：

```python
# expr：基因 × 樣本（log 轉換後）；meta：樣本資訊
top = expr.loc[expr.var(axis=1).nlargest(500).index]      # 先挑變異最大的基因

col_colors = meta["condition"].map({"ctrl": "gray", "treat": "tomato"})
g = sns.clustermap(top, z_score=0,              # 0 = 每列（基因）標準化；1 = 每欄
                   cmap="vlag", center=0, vmin=-2, vmax=2,
                   method="average", metric="correlation",
                   col_colors=col_colors, yticklabels=False, figsize=(7, 8))
g.ax_heatmap.set_xlabel("Sample")
```

| 參數 | 用途 |
| --- | --- |
| `z_score=0` / `1` | 每列 / 每欄減平均除以 SD；看「基因在樣本間的相對高低」時用 `0` |
| `standard_scale=0` / `1` | 縮放到 0–1（與 `z_score` 二擇一） |
| `method` | 階層式分群的連結法：`"average"`、`"complete"`、`"ward"`（需歐氏距離） |
| `metric` | 距離：`"euclidean"`、`"correlation"`（形狀相似）、`"cosine"` |
| `row_cluster` / `col_cluster` | 關閉某一邊的分群（樣本順序已有意義時） |
| `row_colors` / `col_colors` | 側邊色條標示批次、條件，一眼看出分群是否跟著批次走 |

> 不做列標準化時，高表現基因主導顏色，其他基因看起來都一樣；做了 z-score 後顏色只代表**相對**高低，無法跨基因比較絕對表現量。圖說要寫清楚用了哪一種。分群方法本身見 [Clustering](../../../statistics/multivariate-analysis/clustering.md)。

## Pairplot

```python
sns.pairplot(data=iris, hue="species", corner=True)          # corner=True 只畫下三角
sns.pairplot(data=iris, vars=["sepal_length", "petal_length"], kind="reg", diag_kind="hist")
```

| 參數 | 用途 |
| --- | --- |
| `hue` | 依類別上色；有 `hue` 時對角線預設為 KDE |
| `vars` | 只挑部分變數（變數 > 6–8 個時圖會太擠，改看相關 heatmap 或 PCA） |
| `kind` | 非對角：`"scatter"`、`"kde"`、`"hist"`、`"reg"` |
| `diag_kind` | 對角：`"auto"`、`"hist"`、`"kde"`、`None` |
| `corner=True` | 省略重複的上三角 |
| `plot_kws` | 傳給非對角圖的參數，如 `{"alpha": 0.5, "s": 10}` |

更彈性的版面用 `sns.PairGrid`：`g = sns.PairGrid(iris, hue="species"); g.map_lower(sns.scatterplot); g.map_diag(sns.histplot)`。
