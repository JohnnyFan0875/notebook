[Biology](../README.md) › 臨床資訊與標準

# 臨床資訊與標準 (Clinical Informatics and Standards)

病歷、檢驗、用藥、試驗資料要能跨系統交換與合併分析，靠的是共同的**術語 (terminology)** 與**資料模型 (data model)**。做真實世界資料 (real-world data, RWD)、臨床基因體或醫療 AI 時，第一步通常是搞清楚每個欄位用哪套代碼。

建議順序：臨床術語（先懂代碼）→ 臨床資料庫（用代碼建世代）→ 法規資料庫（藥物與伴隨診斷）

## 模組

| 模組 | 內容 | 回答的問題 |
| --- | --- | --- |
| [臨床術語與資料標準](clinical-terminology/README.md) | SNOMED CT、ICD、LOINC、RxNorm、UCUM、UMLS、FHIR、OMOP-CDM、openEHR、CDISC、MedDRA、健保支付標準 | 這個欄位用哪套代碼？不同代碼怎麼對應？ |
| [臨床資料庫](clinical-databases/README.md) | MIMIC-IV、eICU、PhysioNet、UK Biobank | 哪裡有可申請的去識別化病歷 / 世代資料？怎麼申請？ |
| [法規資料庫](regulatory-databases/README.md) | FDA（Drugs@FDA、伴隨診斷）、EMA、罕病教育資源 | 這個藥何時核准？哪個檢測是指定的伴隨診斷？ |

相關：基因層級的臨床資料庫（ClinVar、OMIM、HPO）見 [遺傳學資料庫](../genetics/databases/README.md)；病歷資料的隱私與去識別化見 [隱私與法規](../../data-science/responsible-ai/privacy-and-regulation.md)。
