[Data Science](../../README.md) › [Deep Learning](../README.md) › 生資應用

# 深度學習的生資應用 (Deep Learning in Bioinformatics)

把前面章節的元件（CNN、Transformer、VAE、GNN）放到生物資料上：DNA / 蛋白質序列、單細胞表現量。重點不只是模型，而是生物資料特有的切分方式、評估陷阱與現成工具。

> 生資 DL 最常見的失敗不是模型不夠強，而是**評估方式讓分數虛高**：同源序列跨 train / test、相鄰基因體區段相關、同一捐贈者的細胞同時出現在兩邊。

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [序列與蛋白模型](sequence-and-protein-models.md) | one-hot CNN、DNA 語言模型（DNABERT、Nucleotide Transformer）、Enformer、ESM、AlphaFold | 怎麼從 DNA / 蛋白質序列預測功能或結構？ |
| [單細胞深度學習](single-cell-deep-learning.md) | scVI / scANVI、批次整合、細胞類型標註、單細胞基礎模型 | 單細胞資料什麼時候用 DL？怎麼用？ |

## 模型 ↔ 資料對照

| 資料 | 結構 | 常用架構 | 見 |
| --- | --- | --- | --- |
| DNA 序列 | 1D、4 種字母、長 | 1D CNN、CNN + Transformer、長序列模型 | [序列與蛋白模型](sequence-and-protein-models.md) |
| 蛋白質序列 / 結構 | 1D 序列、3D 座標 | 蛋白質語言模型 (Transformer)、結構模型 | 同上 |
| 單細胞表現量 | 稀疏計數矩陣 | VAE（負二項似然） | [單細胞 DL](single-cell-deep-learning.md) |
| 顯微 / 病理 / 醫學影像 | 2D / 3D 影像 | CNN、U-Net、ViT | [電腦視覺](../computer-vision/README.md) |
| 分子、PPI、空間鄰接 | 圖 | GNN | [圖神經網路](../representation-learning/graph-neural-networks.md) |
| 臨床表格 / bulk 表現量 | 表格、樣本少 | 通常**不需要 DL**；正則化線性模型、樹模型 | [ML 高維資料](../../machine-learning/foundations/high-dimensional-data.md) |
