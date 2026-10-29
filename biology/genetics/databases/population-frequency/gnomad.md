[資料庫](../README.md) › [族群頻率](README.md) › gnomAD

# gnomAD (Genome Aggregation Database)

Broad Institute 整合大量外顯子與全基因組定序資料的族群變異資料庫，是變異判讀中族群頻率的標準參考，也提供基因對功能喪失的容忍度指標。

| 項目 | 內容 |
| --- | --- |
| 網站 | [gnomad.broadinstitute.org](https://gnomad.broadinstitute.org/) |
| 版本 | v4（GRCh38，約 80.7 萬人：約 73 萬外顯子 + 7.6 萬全基因組）；2026-03 釋出 v4.1.1（更新限制度指標）；v2.1.1 為 GRCh37 |
| 其他資料 | 結構變異 (gnomAD-SV)、粒線體變異、長讀定序（gnomAD-LR，beta）、局部祖源 |
| 下載 | VCF / Hail table（雲端 bucket）；VEP 可直接以 gnomAD 註解 |

## 頁面上要看的欄位

| 欄位 | 意義 | 用途 |
| --- | --- | --- |
| Allele frequency (AF) | 所有樣本中 ALT 等位基因比例 | 粗略判斷常見程度 |
| 族群別 AF / grpmax | 各遺傳祖源群的頻率；最高者 | 創始者效應、族群特有變異 |
| Filtering allele frequency (FAF) | 考慮抽樣誤差後的頻率下界（95% 信心） | ACMG BA1 / BS1 比較的建議值 |
| Homozygotes / hemizygotes | 純合子 / 半合子人數 | 隱性疾病：健康純合子多 → 不太可能致病 |
| Flags（如 low-confidence、segdup、LCR） | 品質警告 | 在難區域的頻率要保留 |

## 基因限制度 (Constraint)

| 指標 | 意義 | 判讀 |
| --- | --- | --- |
| LOEUF | 觀察 / 預期功能喪失 (LoF) 變異比例的 90% 信賴上界 | 越低代表越不能容忍 LoF（單倍劑量不足的候選） |
| pLI | LoF 不耐受的機率（舊指標） | 接近 1 = 不耐受 |
| missense Z / MOEUF | 錯義變異的限制度 | 高 Z = 錯義變異被選擇淘汰 |

> 限制度是「基因」層級的指標，不能直接判斷單一變異是否致病；它支持 PVS1 等準則的適用性。新版本更新了 LOEUF 的建議閾值，引用時註明版本。

相關：[族群頻率原則](README.md)、[ACMG/AMP 變異分級](../../variant-interpretation/acmg-amp.md)。
