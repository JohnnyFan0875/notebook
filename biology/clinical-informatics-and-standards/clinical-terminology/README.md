[Biology](../../README.md) › [臨床資訊與標準](../README.md) › 臨床術語

# 臨床術語與資料標準 (Clinical Terminology and Data Standards)

臨床資料標準分三層：**術語**決定「一個概念用什麼代碼」，**資料模型 / 交換標準**決定「代碼放在哪個欄位、怎麼傳」，**研究與法規標準**決定「試驗資料怎麼送審」。同一筆資料通常同時用到好幾套。

## 標準一覽

| 類別 | 標準 | 編碼對象 | 典型代碼 | 授權 |
| --- | --- | --- | --- | --- |
| 術語 | [SNOMED CT](snomed-ct.md) | 臨床概念（疾病、發現、處置、解剖…），細緻的本體 | `44054006` | 會員國免費，其他需申請 |
| 術語 | [ICD-10 / ICD-11](icd.md) | 疾病與死因分類，統計與申報用 | `E11`、`5A11` | 免費 |
| 術語 | [LOINC](loinc.md) | 檢驗項目、觀察值、問卷、文件類型 | `2345-7` | 免費（需帳號） |
| 術語 | [RxNorm](rxnorm.md) | 美國臨床藥品（成分 + 劑量 + 劑型） | RxCUI `198440` | 完整版需 UMLS 授權 |
| 術語 | [UCUM](ucum.md) | 計量單位 | `mg/dL`、`10*3/uL` | 免費 |
| 術語 | [CPT / HCPCS](cpt-hcpcs.md) | 美國醫療處置與耗材申報 | `99213`、`A0429` | CPT 需 AMA 授權 |
| 術語 | [健保支付標準](taiwan-nhi-service-standards.md) | 台灣健保醫療服務給付項目 | `09005C` | 公開 |
| 術語 | [MedDRA](meddra.md) | 藥物不良事件、適應症（法規用） | 8 位數字代碼 | 非營利免費，業界訂閱 |
| 整合 | [UMLS](umls.md) | 把上百套術語對到共同概念 (CUI) | `C0011860` | 免費（需授權帳號） |
| 整合 | [Ontology Lookup Service](ontology-lookup-service.md) | 研究用本體（HPO、MONDO、GO…）查詢 | `HP:0001250` | 免費 |
| 交換 | [HL7 FHIR](fhir.md) | 病歷資料交換的 REST API 與 resource | `Observation` | 開放 |
| 儲存 | [openEHR](open-ehr.md) | 病歷系統內部的臨床模型（archetype） | `blood_pressure.v2` | 開放 |
| 分析 | [OMOP-CDM](omop-cdm.md) | 多中心觀察性研究的共同資料表 | `concept_id` | 開放 |
| 試驗 | [CDISC SDTM / ADaM](cdisc.md) | 臨床試驗資料送審格式 | `AE`、`ADSL` | 開放 |

## 誰負責哪個欄位

一筆檢驗結果從醫院到研究資料庫的路徑：

```
醫院 LIS：「飯前血糖 95 mg/dl」（本地代碼 GLU-AC）
   │  對應 (mapping)
   ▼
FHIR Observation
   code          = LOINC 1558-6 (Fasting glucose)
   valueQuantity = 95  unit = UCUM mg/dL
   subject       → Patient/123
   │  ETL
   ▼
OMOP measurement
   measurement_concept_id ← LOINC 對到的 OMOP standard concept
   unit_concept_id        ← UCUM mg/dL
   value_source_value     = "95 mg/dl"（保留原值）
```

| 資料類型 | 臨床 / 研究用 | 申報 / 統計用 | 法規 / 試驗用 |
| --- | --- | --- | --- |
| 診斷 | SNOMED CT | ICD-10-CM（台灣健保自 2016 年起）、ICD-11 | MedDRA（病史、適應症） |
| 處置 | SNOMED CT | CPT / HCPCS、ICD-10-PCS、健保支付標準 | — |
| 檢驗 | LOINC + UCUM | 健保支付標準（計價項目，不是檢驗語意） | CDISC LB（`LBLOINC`） |
| 藥物 | RxNorm（美國）、ATC | NDC、健保藥品代碼 | WHODrug |
| 不良事件 | SNOMED CT | — | MedDRA |

## 對應的陷阱

| 陷阱 | 說明 |
| --- | --- |
| 對應不是一對一 | SNOMED → ICD 常是多對一（細節遺失）；ICD → SNOMED 常是一對多（要選） |
| 用途不同就不能互換 | ICD 是為了統計 / 申報分類，SNOMED 是為了臨床語意；用 ICD 定義表型會受申報行為影響（例：為了給付而編碼） |
| 版本與年份 | ICD-9 → ICD-10 切換前後同一疾病代碼不同（美國 2015-10、台灣 2016-01）；長期世代要合併兩版 |
| 計價代碼 ≠ 檢驗語意 | 健保支付代碼對應「收費項目」，同一碼可能涵蓋不同檢體或方法，分析檢驗值時要用 LOINC 或院內代碼 |
| 單位 | 同一檢驗可能有 `mg/dL` 與 `mmol/L` 兩種單位，合併前要換算；UCUM 只統一寫法，不會自動換算數值 |

工具：跨術語查對應用 [UMLS](umls.md) 或 OMOP 的 [Athena](https://athena.ohdsi.org/)；研究用本體用 [OLS](ontology-lookup-service.md)。罕病編碼另見 [Orphanet](../../genetics/databases/gene-disease-association/orphanet.md)，表型用語見 [HPO](../../genetics/databases/gene-disease-association/hpo.md)。
