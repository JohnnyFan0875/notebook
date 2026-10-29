[Biology](../../README.md) › [遺傳學](../README.md) › 變異判讀

# 變異判讀 (Variant Interpretation)

把一個變異從「VCF 中的一列」變成「臨床報告中的分級」：先用標準命名描述它，蒐集資料庫、計算預測、家族與功能證據，再依準則組合成五級分類。

## 流程

```
VCF 中的變異 ──正規化 + VEP 註解──► HGVS 命名（MANE 轉錄本）
  ──► 證據蒐集：族群頻率、ClinVar、基因–疾病有效性、in-silico 預測、家族 / 新生、功能試驗
  ──► 依 ACMG/AMP（+ ClinGen 修訂、基因專一規格）逐條判斷準則與強度
  ──► 組合成 P / LP / VUS / LB / B ──► 報告
```

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [HGVS 命名](hgvs-nomenclature.md) | `c.` / `p.` / `g.` 寫法、3′ 規則、驗證工具 | 這個變異該怎麼寫？ |
| [In-silico 預測](in-silico-prediction.md) | 錯義與剪接預測工具、分數範圍、校準閾值 | 計算工具怎麼用在 PP3 / BP4？ |
| [ACMG/AMP 分級](acmg-amp.md) | 28 條準則、組合規則、計分制、ClinGen 修訂、體細胞與 CNV 架構 | 這個變異是致病的嗎？ |
| [ClinGen 指引](clingen-guidelines.md) | SVI 建議、VCEP 規格、Variant Classification Guidance | 準則的細部該怎麼套用？ |
| [ACGS 指引](acgs-guideline.md) | 英國的罕病變異分級最佳實務 | 計分制實際怎麼用？ |

證據來源見 [遺傳學資料庫](../databases/README.md)；基本概念見 [變異等位基因頻率](../foundations/variant-allele-frequency.md)、[新生變異](../foundations/de-novo-variant.md)。
