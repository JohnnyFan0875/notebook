[資料庫](../README.md) › [變異](README.md) › SNPnexus

# SNPnexus

Barts Cancer Institute（倫敦瑪麗皇后大學）的網頁版變異註解工具，強項是**非編碼變異**的功能註解：調控元件、保守性與多種非編碼評分。

| 項目 | 內容 |
| --- | --- |
| 網站 | [snp-nexus.org](https://www.snp-nexus.org/)（舊版 [v4](https://www.snp-nexus.org/v4/) 已退役，改用 v5） |
| 輸入 | 座標（染色體、位置、REF / ALT）、< 1 Mb 的區域、rsID、VCF 檔 |
| 基因組 | GRCh38、GRCh37 |
| 限制 | 批次查詢上限約 10,000 個變異（頁面上另寫上傳上限 100,000，以實際為準）；學術與非營利免費，商業使用需聯絡 |

| 註解類別 | 來源 |
| --- | --- |
| 基因 / 蛋白後果 | Ensembl、RefSeq、UCSC、CCDS；SIFT、PolyPhen |
| 族群頻率 | 1000 Genomes、gnomAD |
| 調控 | ENCODE、Roadmap Epigenomics、Ensembl Regulatory Build、miRBase、CpG island |
| 保守性 | PHAST、GERP++ |
| 疾病 | ClinVar、COSMIC、GWAS Catalog |
| 非編碼評分 | CADD、FunSeq2（v4 另有 EIGEN、FATHMM、GWAVA、ReMM） |
| 其他 | 結構變異類別、Reactome 通路分析 |

適合：GWAS 位點或非編碼候選變異的初步功能註解；大量資料改用本機的 [VEP](ensembl-vep.md) 或 [OpenCRAVAT](opencravat.md)。
