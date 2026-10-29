[資料庫](../README.md) › [基因](README.md) › NCBI Gene

# NCBI Gene

NCBI 的基因中心索引：每個基因一個 Entrez Gene ID，連結到 RefSeq 轉錄本與蛋白、基因組位置、表現、GeneRIF 文獻摘要、ClinVar、dbSNP 等 NCBI 資源。

| 項目 | 內容 |
| --- | --- |
| 網站 | [ncbi.nlm.nih.gov/gene](https://www.ncbi.nlm.nih.gov/gene/) |
| 批次資料 | [gene/DATA](https://ftp.ncbi.nlm.nih.gov/gene/DATA/)：`gene_info`（ID、符號、同義詞、描述）、`gene2refseq`、`gene2ensembl`、`gene2go` |
| MANE | [MANE_human/current](https://ftp.ncbi.nlm.nih.gov/refseq/MANE/MANE_human/current/)：MANE Select / Plus Clinical 的轉錄本對照表與 GFF |
| 何時用 | 需要 Entrez ID（KEGG、clusterProfiler 預設）、RefSeq 轉錄本、MANE 對照 |
| 程式存取 | NCBI Datasets CLI、E-utilities、R `org.Hs.eg.db`（以 Entrez ID 為核心） |

```bash
# MANE Select 對照表：Entrez、Ensembl gene / transcript、RefSeq NM_ 一次對齊
curl -O https://ftp.ncbi.nlm.nih.gov/refseq/MANE/MANE_human/current/MANE.GRCh38.v1.5.summary.txt.gz
```

> MANE 檔名中的版本號會更新（2026-10 查詢時為 v1.5），以 `current/` 目錄下的實際檔名為準。MANE 的用途見 [基因註解](../../../genomics/reference-data/gene-annotations.md)。
