[臨床資訊與標準](../README.md) › [臨床術語](README.md) › openEHR

# openEHR

openEHR 是開放的電子病歷 (EHR) 建模與儲存規格。它的核心是**兩層建模 (two-level modeling)**：底層的參考模型 (Reference Model) 固定不變，臨床內容由臨床人員用 archetype 定義，因此新增臨床欄位不必改資料庫 schema。FHIR 解決系統之間的交換，openEHR 解決系統內部的長期儲存。

| 項目 | 內容 |
| --- | --- |
| 維護 | openEHR International |
| 網站 | [openehr.org](https://openehr.org)、archetype 庫 [Clinical Knowledge Manager (CKM)](https://ckm.openehr.org) |
| 授權 | 規格與 CKM 中的 archetype 開放 |
| 何時用 | 建置或研究以 openEHR 為核心的臨床資料平台（北歐、英國、德國等地較常見） |

## 兩層建模

| 層 | 內容 | 例 | 誰維護 |
| --- | --- | --- | --- |
| Reference Model (RM) | 資料型別、版本控制、稽核、Composition / Entry 等結構 | `DV_QUANTITY`、`OBSERVATION` | 規格 |
| Archetype | 一個臨床概念的完整定義（最大集合） | `openEHR-EHR-OBSERVATION.blood_pressure.v2` | 社群 / 臨床人員（CKM） |
| Template | 依用途組合、裁剪 archetype | 生命徵象表單、出院摘要 | 各機構 |

```
Applications（表單、決策支援、分析）
        │  AQL 查詢
Templates（用途專屬：生命徵象 = 血壓 + 心率 + 體溫）
        │
Archetypes（臨床概念：blood_pressure.v2）
        │
Reference Model（固定的資料結構與型別）
        │
儲存（版本化、稽核紀錄）
```

```
openEHR-EHR-OBSERVATION.blood_pressure.v2
 ├── systolic      DV_QUANTITY (mm[Hg])
 ├── diastolic     DV_QUANTITY (mm[Hg])
 ├── position      DV_CODED_TEXT（站 / 坐 / 臥）
 └── time          DV_DATE_TIME
```

## 查詢：AQL

openEHR 用 Archetype Query Language (AQL) 依 archetype 路徑查資料，不依實體表格：

```sql
SELECT o/data[at0001]/events[at0006]/data[at0003]/items[at0004]/value/magnitude AS systolic
FROM EHR e CONTAINS COMPOSITION c CONTAINS OBSERVATION o[openEHR-EHR-OBSERVATION.blood_pressure.v2]
WHERE o/data[at0001]/events[at0006]/data[at0003]/items[at0004]/value/magnitude > 140
```

## 與其他標準的關係

| 標準 | 關係 |
| --- | --- |
| [FHIR](fhir.md) | 交換時把 composition 轉成 FHIR resource |
| [SNOMED CT](snomed-ct.md) / [LOINC](loinc.md) | archetype 的節點可綁定術語代碼 |
| [OMOP-CDM](omop-cdm.md) | 研究分析時從 openEHR 匯出、ETL 成 OMOP |
