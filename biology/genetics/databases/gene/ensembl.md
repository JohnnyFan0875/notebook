[資料庫](../README.md) › [基因](README.md) › Ensembl

# Ensembl

EMBL-EBI 的基因組註解平台，涵蓋數百個物種的基因、轉錄本、變異、比較基因體與調控區域。人類的基因模型與 GENCODE 相同。

| 存取方式 | 用途 |
| --- | --- |
| [網站](https://www.ensembl.org/) | 查基因模型、轉錄本結構、exon 座標、變異頁面 |
| [BioMart](https://www.ensembl.org/biomart/) | 批次查詢與 ID 轉換（網頁或 R `biomaRt`） |
| [REST API](https://rest.ensembl.org/) | 程式化查詢（序列、變異、VEP） |
| [FTP](https://ftp.ensembl.org/pub/) | GTF、FASTA、VCF 下載（見 [參考基因組](../../../genomics/reference-data/reference-genomes.md)） |
| [VEP](../variant/ensembl-vep.md) | 變異效應預測 |
| [GRCh37 網站](https://grch37.ensembl.org/) | 舊版基因組（註解凍結不再更新） |

```bash
# REST：取得基因資訊
curl -s "https://rest.ensembl.org/lookup/symbol/homo_sapiens/TP53?expand=1" -H "Content-Type: application/json"
```

| 注意 | 說明 |
| --- | --- |
| 記錄 release 與基因組版本 | 每年數次 release，ID 版本號、轉錄本會變 |
| 轉錄本選擇 | 臨床用途對照 MANE Select（頁面上有標示） |
| 染色體命名 | Ensembl 用 `1`、`MT`，與 UCSC 的 `chr1`、`chrM` 不同 |

GENCODE、RefSeq、MANE 的比較見 [基因註解](../../../genomics/reference-data/gene-annotations.md)。
