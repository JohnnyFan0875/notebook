[資料庫](../README.md) › [變異](README.md) › ClinVar

# ClinVar

NCBI 的公開資料庫，彙整臨床實驗室、研究者與專家小組對變異臨床意義的提交。它是「別人怎麼判讀這個變異」的第一站，但它本身是提交的集合，不是單一權威分類。

| 項目 | 內容 |
| --- | --- |
| 網站 | [ncbi.nlm.nih.gov/clinvar](https://www.ncbi.nlm.nih.gov/clinvar/) |
| VCF（每週更新） | [vcf_GRCh38](https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/)、vcf_GRCh37 |
| 表格 | [tab_delimited](https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/)（`variant_summary.txt.gz`：每個變異一列，含分類、審閱狀態、基因、HGVS） |
| 分類類型 | Germline classification（P / LP / VUS / LB / B）、Somatic clinical impact、Oncogenicity 三類分開 |

## 審閱等級（星等）

| 星等 | 審閱狀態 | 可信度 |
| --- | --- | --- |
| ☆☆☆☆ | 無判讀準則 / 無分類 | 低 |
| ★☆☆☆ | 單一提交者有準則；或提交者間**分類衝突** | 參考，需自行評估 |
| ★★☆☆ | 多個提交者有準則、無衝突 | 較可信 |
| ★★★☆ | 專家小組審閱（ClinGen VCEP） | 高 |
| ★★★★ | 實務指引 | 最高 |

## 判讀時注意

| 注意 | 說明 |
| --- | --- |
| 看星等與提交日期 | 舊的提交可能未依 2015 年 ACMG 準則；同一變異的分類會隨證據更新 |
| 看衝突 | "Conflicting classifications" 時打開各提交，看各自的證據與疾病 |
| 疾病對應 | 分類是針對特定疾病；同一基因可能有多種疾病 |
| 轉錄本 | 搜尋時用 MANE 轉錄本的 HGVS，或用基因組座標 |
| 不能直接當證據 | ClinVar 的分類本身不是 ACMG 準則（PP5 / BP6 已不建議使用），要回到提交者的證據 |

```bash
# 把 ClinVar 分類加到自己的 VCF（染色體命名：ClinVar VCF 用 1、2…）
bcftools annotate -a clinvar.vcf.gz -c INFO/CLNSIG,INFO/CLNREVSTAT,INFO/CLNDN in.vcf.gz -Oz -o out.vcf.gz
```

改名稱與正規化見 [bcftools](../../../bioinformatics-tools/ngs-tools/bcftools.md)；判讀架構見 [ACMG/AMP](../../variant-interpretation/acmg-amp.md)。
