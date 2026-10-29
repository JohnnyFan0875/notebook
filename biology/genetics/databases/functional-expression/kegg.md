[資料庫](../README.md) › [功能與表現](README.md) › KEGG

# KEGG (Kyoto Encyclopedia of Genes and Genomes)

京都大學維護的整合資料庫，把基因、蛋白質、化合物、反應、通路、疾病與藥物連成網路；最為人知的是手繪的代謝與訊號通路圖。

| 項目 | 內容 |
| --- | --- |
| 網站 | [genome.jp/kegg](https://www.genome.jp/kegg/) |
| 主要資料庫 | PATHWAY（`hsa04110` 細胞週期）、MODULE、DISEASE、DRUG、COMPOUND、KO（同源群） |
| ID | 人類基因用 Entrez ID（`hsa:7157`） |
| 程式存取 | KEGG REST API；R `clusterProfiler::enrichKEGG()`、`pathview`（把表現量畫在通路圖上） |
| 授權 | 學術網站免費瀏覽；**FTP 批次下載與商業使用需付費授權**；API 有使用量限制 |

```r
library(clusterProfiler)
ekegg <- enrichKEGG(gene = sig_entrez, universe = universe_entrez, organism = "hsa", pAdjustMethod = "BH")
# 需要網路：每次執行從 KEGG API 取得最新通路，結果可能隨時間改變
```

| 注意 | 說明 |
| --- | --- |
| 可重現性 | 線上取得的通路會更新；報告時記錄查詢日期，或改用可固定版本的離線資源 |
| 通路重疊 | 許多通路共用基因（如 MAPK、PI3K-Akt 與多種癌症通路），富集結果常成串出現 |
| 替代 | Reactome（開放授權、階層清楚）、WikiPathways、GO |

富集分析流程見 [RNA-seq 09](../../../genomics/workflows/rna-seq/09-annotation-and-functional-enrichment.md)。
