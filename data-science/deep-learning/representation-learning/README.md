[Data Science](../../README.md) › [Deep Learning](../README.md) › 表示學習

# 表示學習 (Representation Learning)

不靠標籤、或資料不是規則網格（影像 / 序列）時，怎麼學到有用的低維表示。Autoencoder / VAE 是非線性版的降維，也是 scVI 等單細胞模型的基礎；GNN 處理以圖表示的資料（分子、PPI 網路、空間轉錄體的細胞鄰接）。

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Autoencoder 與 VAE](autoencoders-and-vae.md) | 編碼 / 解碼、重建 loss、VAE 的 KL 項與重參數化、與 PCA 的關係 | 怎麼無監督地把高維資料壓成低維表示？ |
| [圖神經網路](graph-neural-networks.md) | 訊息傳遞、GCN / GAT、節點 / 邊 / 圖層級任務、PyG | 資料是圖時怎麼建模？ |

## 和其他章節的關係

| 主題 | 位置 |
| --- | --- |
| 線性降維、t-SNE、UMAP | [降維](../../machine-learning/unsupervised-learning/dimensionality-reduction/README.md) |
| 古典網路分析（中心性、社群偵測） | [網路分析](../../network-analysis/README.md) |
| VAE 在單細胞的應用（scVI） | [單細胞深度學習](../bio-applications/single-cell-deep-learning.md) |
