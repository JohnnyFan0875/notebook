[資料庫](../README.md) › [變異](README.md) › GWAS Catalog

# GWAS Catalog

NHGRI 與 EMBL-EBI 共同維護，收錄已發表 GWAS 的顯著關聯（變異–性狀、效應量、p 值、族群），以及完整的摘要統計 (summary statistics)。

| 項目 | 內容 |
| --- | --- |
| 網站 | [ebi.ac.uk/gwas](https://www.ebi.ac.uk/gwas/)、[下載](https://www.ebi.ac.uk/gwas/docs/file-downloads) |
| 收錄門檻 | 關聯 p < 1 × 10⁻⁵（不只 5 × 10⁻⁸） |
| 性狀 | 以 EFO（Experimental Factor Ontology）標準化 |
| 摘要統計 | 全基因組的 β / SE / p，可用於 colocalization、MR、PRS |
| 程式存取 | REST API |

| 用途 | 說明 |
| --- | --- |
| 查某個變異 / 基因有哪些已知關聯 | 解讀 GWAS 位點或 eQTL 時 |
| 下載摘要統計 | 做 [colocalization](../../../genomics/genome-wide-analysis/colocalization.md)、孟德爾隨機化、PRS |
| 查某性狀的所有研究 | 比較族群、樣本數、效應方向 |

> GWAS 關聯是**族群層級、效應通常很小**的統計關聯，不能用來判斷個人的孟德爾疾病變異是否致病；方法見 [GWAS 基礎](../../../genomics/genome-wide-analysis/gwas-fundamental.md)。另一個相關資源是 [PGS Catalog](https://www.pgscatalog.org/)（多基因風險分數）。
