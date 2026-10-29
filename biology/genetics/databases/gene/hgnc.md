[資料庫](../README.md) › [基因](README.md) › HGNC

# HGNC (HUGO Gene Nomenclature Committee)

人類基因命名的官方機構，為每個基因指定唯一的符號與 HGNC ID，並記錄別名與舊名。基因改名後，舊名仍會出現在文獻與舊資料中，對照 HGNC 才能避免漏掉或混淆。

| 項目 | 內容 |
| --- | --- |
| 網站 | [genenames.org](https://www.genenames.org/) |
| 完整表格下載 | [hgnc_complete_set.txt](https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt)（含 HGNC ID、符號、別名 `alias_symbol`、舊名 `prev_symbol`、Entrez、Ensembl、RefSeq、UniProt、OMIM 對照） |
| 何時用 | 確認正式符號；把別名 / 舊名轉成現行符號；ID 互相對照 |
| 替代 | NCBI Gene 的 `gene_info`（含同義詞） |

| 常見問題 | 例 |
| --- | --- |
| 基因改名 | `C10orf2` → `TWNK`；`MLL` → `KMT2A` |
| Excel 自動轉日期 | `SEPT1` → 1-Sep、`MARCH1` → 1-Mar；HGNC 已改名為 `SEPTIN1`、`MARCHF1` |
| 一個別名對到多個基因 | 別名不唯一時，要用 HGNC ID 或 Entrez ID 當主鍵 |

> 程式中合併資料時，用穩定的 ID（HGNC ID、Entrez、Ensembl）當主鍵，符號只當顯示用。
