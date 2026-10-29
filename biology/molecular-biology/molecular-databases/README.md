[Biology](../../README.md) › [分子生物學](../README.md) › 分子資料庫

# 分子資料庫 (Molecular Databases)

蛋白質層級的參考資料庫：序列與功能、結構域、表現與定位。解讀變異時用來判斷「變異落在哪個功能區域」「這個蛋白在疾病相關組織有沒有表現」；做蛋白語言模型或結構預測時則是主要的訓練與標註來源。

| 資源 | 用途 | 何時用 |
| --- | --- | --- |
| [UniProt](uniprot.md) | 蛋白質序列、功能、結構域、PTM、疾病變異的中心資料庫 | 查一個蛋白的功能、isoform、結構域位置；取得標準序列 |
| [InterPro](interpro.md) | 整合 Pfam、PANTHER 等 13 個資料庫的家族 / 結構域分類 | 註解新序列的結構域；判斷變異是否落在保守結構域 |
| [Human Protein Atlas](human-proteome-atlas.md) | 組織、單細胞、細胞內定位的 RNA 與蛋白表現 | 蛋白實際在哪個組織 / 細胞 / 胞器表現？ |
| [Protein of the Month](protein-of-the-month.md) | 熱門藥物標的的結構與功能短文 | 快速了解一個標的蛋白的結構生物學背景 |

## 查詢流程

```text
基因名 → HGNC 確認正式符號 → UniProt（標準 isoform、功能、PTM、結構域座標）
       → InterPro（結構域 / 家族）→ AlphaFold DB / PDB（3D 結構）
       → Human Protein Atlas（表現與定位）
```

其他常用：[PDB / RCSB](https://www.rcsb.org/)（實驗解析的結構）、[AlphaFold DB](https://alphafold.ebi.ac.uk/)（預測結構）、[STRING](https://string-db.org/)（蛋白交互作用）。基因與變異層級的查詢見[遺傳學資料庫總覽](../../genetics/databases/README.md)，組織 RNA 表現見 [GTEx](../../genetics/databases/functional-expression/gtex.md)。
