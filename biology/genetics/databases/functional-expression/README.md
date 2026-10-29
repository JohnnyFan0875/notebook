[遺傳學](../../README.md) › [資料庫](../README.md) › 功能與表現

# 功能與表現資料庫 (Functional & Expression Databases)

回答「這個基因 / 變異在生物學上可能做什麼」：在哪個組織表現、屬於哪條通路、蛋白質有什麼功能。這類證據支持**生物學合理性**，但通常不足以單獨證明臨床因果關係。

| 資料庫 | 用途 | 何時用 |
| --- | --- | --- |
| [GTEx](gtex.md) | 人體約 50 種組織的表現量與 eQTL / sQTL | 基因是否在疾病相關組織表現？變異是否影響表現量？ |
| [KEGG](kegg.md) | 代謝與訊號通路圖、疾病、藥物 | 基因清單的通路背景、富集分析 |
| [UniProt](../../../molecular-biology/molecular-databases/uniprot.md) | 蛋白質序列、功能、結構域、PTM | 變異落在哪個功能區域？ |
| [InterPro](../../../molecular-biology/molecular-databases/interpro.md) | 蛋白質家族與結構域 | 蛋白質結構域註解 |
| [Human Protein Atlas](../../../molecular-biology/molecular-databases/human-proteome-atlas.md) | 組織 / 細胞層級的蛋白表現與定位 | 蛋白質實際在哪裡表現？ |

其他常用通路 / 基因集資源：Reactome（人工審閱的反應與通路，開放授權）、Gene Ontology、MSigDB（GSEA 用的基因集）。富集分析見 [RNA-seq 09](../../../genomics/workflows/rna-seq/09-annotation-and-functional-enrichment.md)。

> 使用表現量證據時記錄組織、細胞類型、資料集版本與基因 ID；bulk 組織的表現量可能反映的是細胞組成而非單一細胞類型。
