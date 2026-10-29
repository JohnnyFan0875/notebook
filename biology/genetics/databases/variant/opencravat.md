[資料庫](../README.md) › [變異](README.md) › OpenCRAVAT

# OpenCRAVAT

約翰霍普金斯大學 Karchin Lab 開發的開源變異註解平台：從模組商店挑選需要的註解來源（ClinVar、gnomAD、COSMIC、預測分數…），對整個 VCF 批次註解，並提供互動式結果瀏覽器。

| 項目 | 內容 |
| --- | --- |
| 線上版 | [run.opencravat.org](https://run.opencravat.org/server/nocache/login.html)（需註冊） |
| 本機安裝 | `pip install open-cravat`；資料留在本機，適合有隱私限制的資料 |
| 特點 | 模組化、可自訂；結果存成 SQLite，可用 GUI 篩選 |
| 衍生專案 | OakVar（以 OpenCRAVAT 為基礎的分支） |

```bash
oc module install-base
oc module install clinvar gnomad4 revel spliceai     # 模組名稱以 `oc module ls -a` 為準
oc run sample.vcf -l hg38 -a clinvar gnomad4 revel -t excel
oc gui                                               # 瀏覽器檢視結果
```

> 註解模組各有版本與授權，結果中記錄模組版本。與 [VEP](ensembl-vep.md) 相比，OpenCRAVAT 安裝與挑選註解較簡單，VEP 在轉錄本後果與社群支援上較完整。
