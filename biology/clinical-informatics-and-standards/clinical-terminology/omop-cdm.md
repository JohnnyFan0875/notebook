[臨床資訊與標準](../README.md) › [臨床術語](README.md) › OMOP-CDM

# OMOP 共同資料模型 (OMOP-CDM)

OMOP Common Data Model 是 OHDSI 社群維護的觀察性研究資料模型：各機構把自己的 EHR、申報、登錄資料 ETL 成同一組資料表與同一套標準詞彙，之後同一份分析程式（或 ATLAS 的世代定義）就能在各站直接執行，只回傳彙總結果，不必集中病人資料。

| 項目 | 內容 |
| --- | --- |
| 維護 | OHDSI (Observational Health Data Sciences and Informatics) |
| 規格 | [ohdsi.github.io/CommonDataModel](https://ohdsi.github.io/CommonDataModel/)（目前版本 v5.5；v5.4 仍廣泛使用） |
| 詞彙下載 | [Athena](https://athena.ohdsi.org/)（需帳號；CPT 等授權術語要另外申請） |
| 授權 | 開放（Apache 2.0） |
| 何時用 | 多中心真實世界研究、藥物安全、跨國網路研究（如 EHDEN、N3C） |

## 主要資料表

| 群組 | 資料表 | 內容 |
| --- | --- | --- |
| 人 | `person`、`observation_period`、`death` | 人口學、資料涵蓋期間 |
| 就醫 | `visit_occurrence`、`visit_detail` | 門診、住院、急診 |
| 臨床事件 | `condition_occurrence`、`drug_exposure`、`procedure_occurrence`、`device_exposure` | 診斷、用藥、處置、醫材 |
| 量測 | `measurement`、`observation` | 檢驗值、生命徵象；其他觀察 |
| 文字 | `note`、`note_nlp` | 病歷文字與 NLP 結果 |
| 衍生 | `condition_era`、`drug_era` | 合併連續事件成期間 |
| 經濟 | `cost`、`payer_plan_period` | 費用、保險 |
| 詞彙 | `concept`、`concept_relationship`、`concept_ancestor`、`vocabulary` | 標準詞彙與對應關係 |

## 標準概念 (Standard Concept)

每個事件欄位存兩份代碼：**source**（原始代碼，保留）與 **standard**（對到的標準概念，用來分析）。

| Domain | 標準詞彙 | 常見來源碼 |
| --- | --- | --- |
| Condition | SNOMED CT | ICD-9-CM、ICD-10-CM、院內碼 |
| Drug | RxNorm / RxNorm Extension | NDC、ATC、院內藥碼 |
| Measurement | LOINC | 院內檢驗碼 |
| Procedure | SNOMED CT、CPT-4、HCPCS、ICD-10-PCS | 申報碼 |
| Unit | UCUM | 原始單位字串 |

```sql
-- 找出第 2 型糖尿病（含所有 SNOMED 子孫概念）的病人
SELECT DISTINCT co.person_id
FROM condition_occurrence co
JOIN concept_ancestor ca
  ON co.condition_concept_id = ca.descendant_concept_id
WHERE ca.ancestor_concept_id = 201826;   -- Type 2 diabetes mellitus (SNOMED 44054006)

-- 來源碼 → 標準概念
SELECT c1.concept_code AS icd10, c2.concept_id, c2.concept_name
FROM concept c1
JOIN concept_relationship cr ON c1.concept_id = cr.concept_id_1 AND cr.relationship_id = 'Maps to'
JOIN concept c2 ON cr.concept_id_2 = c2.concept_id
WHERE c1.vocabulary_id = 'ICD10CM' AND c1.concept_code = 'E11.9';
```

`concept_ancestor` 讓「某疾病及其所有亞型」一次查完，不用自己展開階層；階層查詢的一般寫法見 [遞迴與階層 SQL](../../../data-science/databases/recursive-and-hierarchical-sql.md)。

## OHDSI 工具

| 工具 | 用途 |
| --- | --- |
| WhiteRabbit / Rabbit-in-a-Hat | 掃描來源資料、設計 ETL 對應 |
| Usagi | 院內代碼 → 標準概念的半自動對應 |
| Achilles / Data Quality Dashboard | 資料特性描述與品質檢查 |
| ATLAS | 網頁介面定義世代、描述統計、發生率 |
| HADES（R 套件群） | CohortMethod、PatientLevelPrediction、CohortDiagnostics 等 |

> 對應品質決定研究品質：院內代碼對不到標準概念時會落到 `concept_id = 0`，分析前先看 Achilles 報告中未對應的比例。
