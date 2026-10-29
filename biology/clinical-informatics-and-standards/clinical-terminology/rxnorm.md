[臨床資訊與標準](../README.md) › [臨床術語](README.md) › RxNorm

# RxNorm

RxNorm 是美國 NLM 維護的臨床藥品標準命名，把各家藥品資料庫（First Databank、Micromedex、FDA SPL 等）的同一藥品對到同一個 RxCUI，並記錄成分、劑量、劑型、品牌之間的關係。美國 EHR、電子處方與 OMOP 的藥物標準概念都用它。

| 項目 | 內容 |
| --- | --- |
| 維護 | U.S. National Library of Medicine (NLM) |
| 網站 / API | [RxNav](https://mor.nlm.nih.gov/RxNav/)、[RxNorm API](https://lhncbc.nlm.nih.gov/RxNav/APIs/RxNormAPIs.html) |
| 發布 | 每月完整版 + 每週更新 |
| 授權 | 完整版需 UMLS 授權；Current Prescribable Content 子集不需授權 |
| 限制 | 以美國上市藥品為主；台灣資料需用健保藥品代碼或 ATC |

## 概念類型 (Term Type)

| TTY | 意義 | 例 |
| --- | --- | --- |
| IN | 成分 (Ingredient) | acetaminophen |
| PIN | 精確成分（鹽類、水合物） | metformin hydrochloride |
| BN | 品牌名 | Tylenol |
| DF | 劑型 | Oral Tablet |
| SCD | 臨床藥品 = 成分 + 劑量 + 劑型 | acetaminophen 500 MG Oral Tablet（RxCUI `198440`） |
| SBD | 品牌藥品 = SCD + 品牌 | acetaminophen 500 MG Oral Tablet [Tylenol]（RxCUI `209459`） |

```
IN  acetaminophen ──┐
DF  Oral Tablet ────┼──► SCD acetaminophen 500 MG Oral Tablet
BN  Tylenol ────────┘          │
                               └──► SBD acetaminophen 500 MG Oral Tablet [Tylenol]
                                     └─ 對應多個 NDC（包裝層級）
```

## 常見用途

| 任務 | 做法 |
| --- | --- |
| 合併不同來源的用藥紀錄 | NDC / 品牌名 → RxCUI → 往上取 IN，在成分層級分析 |
| 藥物分類 | RxCUI → ATC、VA Class（RxClass API） |
| 交互作用 / 過敏檢查 | 系統以 RxCUI 為鍵查詢知識庫 |
| FHIR | `Medication.code`、`MedicationRequest.medication` |
| OMOP | `drug_exposure.drug_concept_id`（RxNorm 為藥物 standard vocabulary，美國以外藥品可用 RxNorm Extension） |

```bash
# RxNorm REST API：名稱 → RxCUI，再查相關成分
curl "https://rxnav.nlm.nih.gov/REST/rxcui.json?name=acetaminophen%20500%20MG%20Oral%20Tablet"
curl "https://rxnav.nlm.nih.gov/REST/rxcui/198440/related.json?tty=IN"   # acetaminophen (RxCUI 161)
```

藥物基因體（藥物 × 基因型）見 [藥物基因體資料庫](../../genetics/databases/pharmacogenomics/README.md)。
