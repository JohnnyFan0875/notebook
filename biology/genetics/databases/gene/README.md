[遺傳學](../../README.md) › [資料庫](../README.md) › 基因

# 基因資料庫 (Gene Databases)

查一個基因的正式名稱、ID、位置、轉錄本與相關資源。

| 資料庫 | 用途 | 何時用 |
| --- | --- | --- |
| [HGNC](hgnc.md) | 人類基因的**官方符號**與別名、舊名 | 確認基因名稱、處理別名與改名 |
| [NCBI Gene](ncbi-gene.md) | Entrez Gene ID、RefSeq 轉錄本、MANE、文獻 | 需要 Entrez ID（KEGG、clusterProfiler）、RefSeq |
| [Ensembl](ensembl.md) | ENSG / ENST ID、基因模型、BioMart、VEP、多物種比較 | RNA-seq 註解、批次 ID 轉換、變異註解 |
| [UCSC Genome Browser](ucsc-genome-browser.md) | 基因組瀏覽器：疊加基因、保守性、重複、調控軌道 | 目視檢查區域、Table Browser 下載 |
| [GeneCards](genecards.md) | 彙整多個資料庫的基因摘要 | 快速了解陌生基因 |

## ID 對照

| ID 類型 | 例（TP53） | 來源 |
| --- | --- | --- |
| HGNC 符號 / ID | `TP53` / `HGNC:11998` | HGNC |
| Entrez Gene ID | `7157` | NCBI Gene |
| Ensembl gene ID | `ENSG00000141510` | Ensembl / GENCODE |
| RefSeq 轉錄本 | `NM_000546.6` | NCBI |
| Ensembl 轉錄本 | `ENST00000269305.9` | Ensembl |
| UniProt | `P04637` | UniProt |

批次轉換：R 的 `AnnotationDbi::mapIds()` / biomaRt（見 [RNA-seq 09](../../../genomics/workflows/rna-seq/09-annotation-and-functional-enrichment.md)）、HGNC 的 complete set 表格、Ensembl BioMart。轉錄本該選哪一個見 [基因註解：MANE](../../../genomics/reference-data/gene-annotations.md)。
