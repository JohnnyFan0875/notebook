[Statistics](../README.md) › 多變量分析

# 多變量分析 (Multivariate Analysis)

**同時**分析三個以上變數的關係。雙變數問「X 與 Y 有關嗎？」；多變量問「許多變數如何一起變動、如何共同解釋結果？」基因表現矩陣、多組學 (multi-omics)、影像特徵都是典型的高維多變量資料。

## 建議順序

```
線性代數直覺 → 多變量 EDA → 降維（PCA）→ 分群 → 監督式模型（迴歸、分類）→ 診斷
```

降維通常在分群與迴歸之前：直接處理高維原始資料會放大雜訊、增加計算量、難以解讀。

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [線性代數基礎](linear-algebra-foundations.md) | 向量、矩陣、特徵值、共變異矩陣 | 怎麼用矩陣思考多變量資料？ |
| [多變量 EDA](multivariate-eda.md) | 相關矩陣、pairplot、平行座標、Simpson's paradox | 建模前資料有什麼結構？ |
| [主成分分析 (PCA)](pca.md) | 特徵分解、scree plot、loadings、biplot | 怎麼把相關變數壓成少數軸？ |
| [分群](clustering.md) | K-Means、階層式、DBSCAN、輪廓係數 | 沒有標籤時資料有哪些群？ |
| [多元迴歸：預測與正則化](multiple-regression.md) | 測試集評估、Ridge / Lasso、p > n | 很多預測變數時怎麼建模？ |
| [邏輯斯迴歸與 LDA](logistic-lda.md) | 判別分析、決策邊界 | 怎麼分類？ |
| [模型假設與診斷](assumptions-diagnostics.md) | 殘差、共線性、影響點、分群與 PCA 的檢查 | 模型假設成立嗎？ |
| [結構方程模型 (SEM)](structural-equation-modeling-with-lavaan.md) | 潛在變數、CFA、lavaan | 怎麼檢定潛在變數模型？ |

> 迴歸的完整基礎在 [迴歸分析](../regression-analysis/README.md)；這裡著重多變量工作流程中的應用。ML 版本見 [ML: Dimensionality Reduction](../../machine-learning/unsupervised-learning/dimensionality-reduction/README.md)、[ML: Clustering](../../machine-learning/unsupervised-learning/clustering/README.md)。
