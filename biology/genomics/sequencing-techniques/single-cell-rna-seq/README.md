[基因體學](../../README.md) › [定序技術](../README.md) › 單細胞 RNA-seq

# 單細胞 RNA-seq (Single-Cell RNA-seq)

bulk RNA-seq 量的是一群細胞的平均表現；單細胞 RNA-seq (scRNA-seq) 為每個細胞各給一組表現量，能分辨細胞類型、稀有族群與連續的分化狀態。代價是資料極度稀疏（大部分基因在大部分細胞是 0）、技術雜訊大。

## 平台

| 方式 | 例 | 細胞數 | 特點 |
| --- | --- | --- | --- |
| 液滴 (droplet) | 10x Genomics Chromium | 數千–數萬 / 樣本 | 主流；3′ 或 5′ 端計數；每個細胞有 barcode、每個分子有 UMI |
| 孔盤 (plate) | Smart-seq2 / 3 | 數百 | 全長轉錄本，可看 isoform 與 SNV；細胞數少 |
| 組合索引 (split-pool) | Parse、sci-RNA-seq | 數萬–百萬 | 不需特殊儀器，可固定後保存 |
| 單核 (snRNA-seq) | 同上，改用細胞核 | — | 冷凍組織、難解離組織（腦、心臟）；偏 intron reads |
| 空間轉錄體 | Visium、Xenium、MERFISH | — | 保留組織位置 |

## 分析流程

```
FASTQ ──Cell Ranger / STARsolo / alevin-fry──► 細胞 × 基因 count matrix（稀疏）
  ──► QC：每細胞基因數、UMI 數、粒線體比例、doublet 偵測
  ──► 正規化（log-normalize / SCTransform）──► 高變異基因
  ──► PCA ──► 批次整合（Harmony、scVI）──► 鄰近圖 ──► 分群（Leiden）──► UMAP 視覺化
  ──► 細胞類型註解（marker 基因、參考圖譜）
  ──► 差異表現（pseudobulk）、軌跡、細胞間通訊
```

| 步驟 | 常用閾值 / 工具 | 注意 |
| --- | --- | --- |
| 細胞 QC | 基因數 200–6,000、粒線體 reads < 10–20%（依組織） | 粒線體比例高 = 細胞破損；閾值依組織調整（心肌本來就高） |
| Doublet | scDblFinder、Scrublet | 兩個細胞被包在同一液滴，會像「中間型」細胞 |
| 環境 RNA | SoupX、CellBender | 破裂細胞釋出的 RNA 污染所有液滴 |
| 批次整合 | Harmony、scVI、Seurat integration | 過度整合會抹掉真實的生物差異 |
| 分群 | Leiden / Louvain（resolution 參數） | 群數受參數影響，不等於「真的有幾種細胞」 |
| 註解 | 已知 marker、CellTypist、Azimuth、SingleR | 先粗分（T / B / 髓系），再細分 |
| 差異表現 | **pseudobulk**（同一樣本同一細胞類型加總後用 DESeq2 / edgeR） | 直接把細胞當獨立樣本做檢定是**假重複**，p 值嚴重高估 |

> UMAP 只用來視覺化：群與群的距離、群的大小都不代表真實的生物距離或比例。

## 工具生態

| | Python | R |
| --- | --- | --- |
| 資料物件 | AnnData（見 [AnnData 與 scanpy](../../../../data-science/python-foundations/anndata-and-scanpy.md)） | Seurat 物件、SingleCellExperiment（見 [Bioconductor](../../../bioinformatics-tools/bioconductor.md)） |
| 主要套件 | scanpy、scvi-tools、squidpy（空間） | Seurat、scran / scater、Monocle |
| 深度學習 | scVI、scGPT 等基礎模型（見 [單細胞深度學習](../../../../data-science/deep-learning/bio-applications/single-cell-deep-learning.md)） | — |

## 筆記

| 筆記 | 內容 |
| --- | --- |
| [軌跡分析](trajectory.md) | pseudotime、分支、RNA velocity |

統計觀念：[假重複與生物重複](../../../../data-science/statistics/experimental-design/README.md)、[PCA](../../../../data-science/statistics/multivariate-analysis/pca.md)、[分群](../../../../data-science/statistics/multivariate-analysis/clustering.md)、[多重檢定](../../../../data-science/statistics/inferential-statistics/multiple-testing.md)。bulk RNA-seq 見 [RNA-seq 分析](../../workflows/rna-seq/README.md)。
