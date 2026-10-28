[Machine Learning](../README.md) › 非監督式學習

# 非監督式學習 (Unsupervised Learning)

沒有標籤時尋找資料結構：分群、降維視覺化、找異常、挖共現規則。沒有「正確答案」可以對照，所以更需要視覺化、領域知識與穩定性檢查。

## 模組

| 模組 | 內容 | 回答的問題 |
| --- | --- | --- |
| [分群](clustering/README.md) | K-Means、階層式、DBSCAN / HDBSCAN、GMM | 資料自然分成幾群？ |
| [降維](dimensionality-reduction/README.md) | PCA、t-SNE、UMAP、NMF | 高維資料怎麼壓縮、怎麼畫出來？ |
| [異常偵測](anomaly-detection/README.md) | Isolation Forest、LOF、時間序列異常 | 哪些觀測值不尋常？ |
| [關聯規則](association-rules/README.md)（選讀） | Apriori、FP-Growth、support / confidence / lift | 哪些項目常一起出現？ |

## 典型用途

| 用途 | 例子 |
| --- | --- |
| 探索與分群 | 顧客分群、單細胞找細胞類型、腫瘤亞型 |
| 視覺化高維資料 | 基因表現的 PCA / UMAP 圖、批次效應檢查 |
| 壓縮與降噪 | PCA 後再分群或建模 |
| 找罕見或可疑的觀測 | 詐欺、儀器故障、QC 不合格樣本 |
| 共現模式 | 購物籃、共同出現的症狀或突變 |

## 閱讀提醒

| 提醒 | 說明 |
| --- | --- |
| 分群結果是**假設**，不是發現 | 只是某種距離定義下的切分；任何資料都能被切成 k 群，見 [分群是假設，不是結論](../../statistics/multivariate-analysis/clustering.md#分群是假設不是結論) |
| 降維圖分得開 ≠ 原空間分得開 | t-SNE / UMAP 會放大局部分離；群間距離沒有意義 |
| 高 confidence 的規則 ≠ 因果 | 甚至可能是負相關（lift < 1） |
| 距離型方法都要先縮放 | K-Means、階層式、DBSCAN、KNN、LOF |
| 先看技術因素 | 生資資料的「群」常是批次、定序深度或樣本品質，見 [批次效應](../../statistics/experimental-design/confounding-bias.md#生資最常見的干擾批次效應-batch-effect) |
