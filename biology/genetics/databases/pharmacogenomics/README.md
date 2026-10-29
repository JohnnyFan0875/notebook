[遺傳學](../../README.md) › [資料庫](../README.md) › 藥物基因體

# 藥物基因體資料庫 (Pharmacogenomics Databases)

藥物基因體學 (PGx) 研究遺傳變異如何影響藥物的代謝、療效與副作用。和疾病變異不同，PGx 變異多半很常見，臨床問題是「這個基因型該怎麼調整用藥」。

| 資源 | 用途 | 何時用 |
| --- | --- | --- |
| [ClinPGx（原 PharmGKB）](pharmgkb.md) | 基因–藥物證據彙整、臨床註解與證據等級、藥品仿單註解 | 查一個變異 / 基因 / 藥物的所有 PGx 證據 |
| [CPIC](cpic.md) | 依基因型給出具體處方建議的臨床指引 | 已知基因型，要決定劑量或換藥 |
| PharmVar | 藥物代謝基因的 star allele 命名（`CYP2D6*4`） | 確認等位基因定義 |
| DPWG | 荷蘭藥師學會的 PGx 指引 | 與 CPIC 對照 |
| FDA Table of Pharmacogenomic Biomarkers | 仿單中有 PGx 資訊的藥物 | 法規層面 |

## 從基因型到處方

```
基因型（star allele，如 CYP2C19 *1/*2）
  → 表型（代謝能力：正常 / 中間 / 不良 / 快速 / 超快速代謝者）
  → 處方建議（CPIC：換藥、調整劑量、或依標準用藥）
```

| 經典例子 | 臨床意義 |
| --- | --- |
| *CYP2C19* — clopidogrel | 不良代謝者活化不足，抗血小板效果差 → 考慮替代藥物 |
| *CYP2D6* — codeine | 超快速代謝者產生過量嗎啡 → 中毒風險 |
| *HLA-B\*15:02* — carbamazepine | 東南亞族群（含台灣）帶因者易發生 SJS / TEN → 用藥前篩檢（台灣健保給付） |
| *HLA-B\*58:01* — allopurinol | 嚴重皮膚過敏，台灣、漢人帶因率較高 |
| *DPYD* — fluoropyrimidines | 酵素活性低 → 嚴重毒性，需減量 |
| *TPMT* / *NUDT15* — thiopurines | *NUDT15* 變異在東亞族群常見 → 骨髓抑制風險 |

> 腫瘤的體細胞變異與標靶藥物（如 *EGFR* 與 TKI）屬於癌症基因體的範疇，資源見 [CIViC](../variant/civic.md) 與 [NCCN 指引](../../../genomics/cancer-genomics/nccn.md)。
