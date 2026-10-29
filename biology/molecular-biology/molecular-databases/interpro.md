[分子生物學](../README.md) › [分子資料庫](README.md) › InterPro

# InterPro

由 EMBL-EBI 維護，把多個蛋白質特徵資料庫的預測整合成單一條目，將蛋白質序列分類到家族，並預測結構域 (domain) 與功能位點。

| 項目 | 內容 |
| --- | --- |
| 入口 | [ebi.ac.uk/interpro](https://www.ebi.ac.uk/interpro/)；本機註解用 [InterProScan](https://interproscan-docs.readthedocs.io/) |
| 成員資料庫 (13) | Pfam、PANTHER、CATH-Gene3D、SUPERFAMILY、SMART、PROSITE、PRINTS、PIRSF、HAMAP、NCBIfam（含 TIGRFAMs）、CDD、SFLD、MobiDB Lite（無序區） |
| 條目類型 | Family、Domain、Homologous superfamily、Repeat、Site（active / binding / conserved / PTM） |
| 適用情境 | 註解新蛋白 / 宏基因體預測蛋白；判斷變異是否落在保守結構域；以 GO term 做功能推論 |
| 替代 / 互補 | [UniProt](uniprot.md)（已整合 InterPro 結構域）、Pfam（現已併入 InterPro 網站） |

```bash
# 對預測蛋白序列跑 InterProScan，輸出 TSV + GO 與通路註解
interproscan.sh -i proteins.faa -f tsv -goterms -pa -cpu 8 -o proteins.interpro.tsv
```

> 變異判讀中「位於突變熱點或無良性變異的關鍵功能結構域」對應 ACMG 的 PM1，結構域邊界常由 InterPro / UniProt 取得，見 [ACMG/AMP](../../genetics/variant-interpretation/acmg-amp.md)。

<sub>成員資料庫清單依 [InterPro 文件](https://interpro-documentation.readthedocs.io/en/latest/databases.html)</sub>
