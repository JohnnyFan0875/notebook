[臨床資訊與標準](../README.md) › [臨床術語](README.md) › CPT / HCPCS

# CPT / HCPCS

CPT 與 HCPCS 是美國醫療處置、服務與耗材的申報代碼。用美國申報資料（Medicare、商業保險 claims）或 OMOP 的 procedure 表時一定會遇到；分子檢測也有專屬的 CPT 代碼。

| 項目 | CPT | HCPCS Level II |
| --- | --- | --- |
| 全名 | Current Procedural Terminology | Healthcare Common Procedure Coding System |
| 維護 | American Medical Association (AMA) | Centers for Medicare & Medicaid Services (CMS) |
| 內容 | 醫師與醫療人員提供的處置、檢查、檢驗 | CPT 沒有的項目：耗材、耐用醫材、救護車、部分藥物 |
| 格式 | 5 碼 | 1 字母 + 4 位數字 |
| 更新 | 每年一次（1 月 1 日生效） | 每季 |
| 授權 | 受 AMA 著作權保護，商業使用需授權 | 公開 |
| 網站 | [ama-assn.org](https://www.ama-assn.org/practice-management/cpt) | [cms.gov](https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system) |

HCPCS 分兩級：Level I 就是 CPT，Level II 是 CMS 自己的代碼。

## CPT 分類

| 類別 | 格式 | 用途 | 例 |
| --- | --- | --- | --- |
| Category I | 5 位數字 | 已普及的處置與服務 | `99213` 門診複診（既有病人） |
| Category II | 4 位數字 + `F` | 品質指標追蹤（不計費） | — |
| Category III | 4 位數字 + `T` | 新興技術（暫時代碼） | — |
| PLA | 4 位數字 + `U` | 特定實驗室的專有檢測 (Proprietary Laboratory Analyses) | — |

## 分子檢測代碼

| 代碼範圍 | 內容 |
| --- | --- |
| Tier 1 分子病理（`81105` 起，至 `813xx`） | 特定基因的特定檢測，如 `81235` *EGFR* 常見變異 |
| Tier 2 分子病理（`81400`–`81408`） | 依技術複雜度分級的其他基因檢測 |
| 基因組序列分析（`81410`–`81471` 一帶） | 多基因 panel、外顯子組、基因組 |
| PLA（`xxxxU`） | 特定商業檢測（如某家公司的 NGS panel） |

> 申報代碼記錄「做了什麼、收多少錢」，不記錄結果；要知道變異或檢驗值，仍需要報告本身或 LOINC 編碼的結果資料。

| 對應 | 用法 |
| --- | --- |
| [FHIR](fhir.md) | `Procedure.code`、`ServiceRequest.code`、`Claim` |
| [OMOP-CDM](omop-cdm.md) | CPT-4、HCPCS 是 procedure domain 的標準詞彙之一 |
| [ICD-10-PCS](icd.md) | 美國**住院**處置用 ICD-10-PCS，門診與醫師服務用 CPT |
| [健保支付標準](taiwan-nhi-service-standards.md) | 台灣對應的處置 / 檢驗計價代碼 |
