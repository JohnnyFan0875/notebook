[遺傳學](../../README.md) › [資料庫](../README.md) › 變異

# 變異資料庫 (Variant Databases)

查一個變異的 ID、臨床分類、預測效應，或批次註解整個 VCF。查詢前先把變異[正規化](../../../genomics/file-formats/vcf.md#同一個變異的不同寫法)並確認基因組版本與轉錄本（[HGVS 命名](../../variant-interpretation/hgvs-nomenclature.md)）。

## Germline / 一般

| 資料庫 | 用途 | 何時用 |
| --- | --- | --- |
| [dbSNP](dbsnp.md) | rsID 與基本資訊 | 把 rsID 轉成座標，或反查 |
| [ClinVar](clinvar.md) | 臨床分類的公開彙整，附審閱等級 | **判讀時的第一站**：別人怎麼分類這個變異？ |
| [Ensembl VEP](ensembl-vep.md) | 對轉錄本 / 蛋白 / 調控區的效應預測，可整合多種註解 | 批次註解 VCF |
| [GWAS Catalog](gwas-catalog.md) | 已發表 GWAS 的關聯 | 常見變異與複雜疾病 / 性狀 |
| [BRCA Exchange](brca-exchange.md) | *BRCA1/2* 變異與 ENIGMA 專家分類 | 遺傳性乳癌 / 卵巢癌 |
| [HGMD](../gene-disease-association/hgmd.md) | 文獻報告的致病變異（多需訂閱） | 補充 ClinVar 沒有的文獻 |

## 癌症（體細胞）

| 資料庫 | 用途 | 何時用 |
| --- | --- | --- |
| [COSMIC](cosmic.md) | 腫瘤中觀察到的體細胞突變、Cancer Gene Census | 某突變在哪些癌別出現、多常見 |
| [CIViC](civic.md) | 開放、社群審閱的變異–療效 / 預後證據 | 變異有無臨床治療意義 |
| [PMKB](pmkb.md) | 依腫瘤類型撰寫的變異臨床解讀 | 撰寫報告時參考解讀文字 |

## 整合 / 註解平台

| 平台 | 用途 | 何時用 |
| --- | --- | --- |
| [VarSome](varsome.md) | 彙整多資料庫並自動套用 ACMG 準則 | 快速瀏覽單一變異 |
| [OpenCRAVAT](opencravat.md) | 開源、模組化的批次註解 | 本機批次註解、自選註解來源 |
| [SNPnexus](snpnexus.md) | 網頁版批次註解（編碼、調控、保守性、非編碼評分） | 非編碼變異的功能註解 |

> 整合平台方便瀏覽，但會落後原始資料庫的更新，自動 ACMG 分類也只是起點；正式判讀回到原始資料庫並依 [ACMG/AMP](../../variant-interpretation/acmg-amp.md) 逐條評估。日本族群頻率資料庫 HGVD 已移到 [族群頻率](../population-frequency/hgvd.md)。
