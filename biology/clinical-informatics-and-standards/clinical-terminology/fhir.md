[臨床資訊與標準](../README.md) › [臨床術語](README.md) › FHIR

# HL7 FHIR

FHIR (Fast Healthcare Interoperability Resources) 是 HL7 的病歷資料交換標準：把臨床資料拆成模組化的 **resource**（Patient、Observation、Condition…），用 REST API 與 JSON 傳遞。它規定「資料放哪個欄位、怎麼傳」，欄位裡的代碼則來自 LOINC、SNOMED CT、RxNorm 等術語。

| 項目 | 內容 |
| --- | --- |
| 維護 | HL7 International |
| 網站 | [hl7.org/fhir](https://hl7.org/fhir)（目前發布版 R5，2023） |
| 版本 | DSTU2 → STU3 → R4（2019，實務上最廣泛採用）→ R4B → R5；R6 制定中 |
| 授權 | 開放、免費 |
| 何時用 | 從 EHR 取資料（API）、跨院交換、SMART on FHIR 應用、臨床基因報告 |

## 核心觀念

| 觀念 | 說明 |
| --- | --- |
| Resource | 最小交換單位，R5 約有 150 種；每個有固定欄位、可用 `reference` 互相連結 |
| RESTful API | `GET /Patient/123`、`GET /Observation?patient=123&code=http://loinc.org\|2345-7`、`POST`、`PUT`、`DELETE` |
| 格式 | JSON（最常用）、XML、RDF/Turtle |
| Terminology binding | 欄位綁定值集 (value set)，如 `Observation.code` 建議用 LOINC |
| Profile / IG | 在基礎 resource 上加限制與擴充，形成 Implementation Guide（如 US Core、IPS、Genomics Reporting） |
| Extension | 標準沒有的欄位用 extension 加，不破壞相容性 |
| Bundle | 把多個 resource 包成一次傳輸（交易、搜尋結果、文件） |

## Resource 與範例

| Resource | 內容 | 常用代碼 |
| --- | --- | --- |
| `Patient` | 人口學、識別碼 | — |
| `Encounter` | 門診、住院、急診 | — |
| `Condition` | 診斷、問題清單 | SNOMED CT、ICD-10 |
| `Observation` | 檢驗、生命徵象、基因變異 | LOINC + UCUM |
| `MedicationRequest` | 處方 | RxNorm |
| `Procedure` | 處置、手術 | SNOMED CT、CPT |
| `DiagnosticReport` | 檢驗 / 影像 / 基因報告，連到多個 Observation | LOINC |
| `ImagingStudy` | 影像檢查的 metadata，連到 DICOM | DICOM UID |

```json
{
  "resourceType": "Observation",
  "id": "glucose",
  "status": "final",
  "code": {
    "coding": [{ "system": "http://loinc.org", "code": "2345-7",
                 "display": "Glucose [Mass/volume] in Serum or Plasma" }]
  },
  "subject": { "reference": "Patient/123" },
  "effectiveDateTime": "2026-10-01T08:30:00+08:00",
  "valueQuantity": { "value": 95, "unit": "mg/dL",
                     "system": "http://unitsofmeasure.org", "code": "mg/dL" }
}
```

`code.coding` 是陣列：同一筆資料可同時帶院內代碼與 LOINC。`subject` 用 reference 指向 `Patient`，取資料時用 `_include` 或再查一次。

## 讀 FHIR 資料做分析

```python
import requests
import pandas as pd

base = "https://hapi.fhir.org/baseR4"   # 公開測試伺服器，資料為假資料
r = requests.get(f"{base}/Observation",
                 params={"code": "http://loinc.org|2345-7", "_count": 50})
bundle = r.json()

rows = [{
    "patient": e["resource"]["subject"]["reference"],
    "time": e["resource"].get("effectiveDateTime"),
    "value": e["resource"].get("valueQuantity", {}).get("value"),
    "unit": e["resource"].get("valueQuantity", {}).get("code"),
} for e in bundle.get("entry", [])]
df = pd.DataFrame(rows)
# 分頁：bundle["link"] 中 relation == "next" 的 url
```

FHIR 適合**交換與取用**單一病人或小量資料；大規模分析通常用 Bulk Data API（`$export`，輸出 NDJSON）匯出後轉成 [OMOP-CDM](omop-cdm.md) 或資料倉儲。JSON 這類半結構化資料的處理見 [儲存與資料模型](../../../data-science/data-engineering/storage-and-models.md)。

## 與其他標準的關係

| 標準 | 關係 |
| --- | --- |
| HL7 v2 | 醫院內部仍大量使用的訊息格式（以分隔符號切欄位的文字訊息）；FHIR 常透過介接引擎從 v2 轉換 |
| [openEHR](open-ehr.md) | openEHR 管系統內部儲存與臨床模型，FHIR 管系統之間交換；archetype 可對到 resource |
| [OMOP-CDM](omop-cdm.md) | FHIR → ETL → OMOP，做多中心分析 |
| DICOM | 影像本身用 DICOM；FHIR `ImagingStudy` 只帶 metadata 與連結 |
| SMART on FHIR | 以 OAuth 2.0 授權第三方 App 讀取 EHR 的 FHIR API |
