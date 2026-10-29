[臨床資訊與標準](../README.md) › [臨床術語](README.md) › LOINC

# LOINC

LOINC (Logical Observation Identifiers Names and Codes) 為檢驗項目、臨床量測、問卷與文件類型提供通用代碼。各醫院檢驗系統的本地代碼不同，合併多中心檢驗值時，先把本地代碼對到 LOINC 是最關鍵的一步。

| 項目 | 內容 |
| --- | --- |
| 維護 | Regenstrief Institute |
| 網站 | [loinc.org](https://loinc.org)、搜尋 [SearchLOINC](https://loinc.org/search/) |
| 授權 | 免費，下載需註冊帳號 |
| 發布 | 每年約兩次 |
| 何時用 | FHIR `Observation.code`、OMOP `measurement`、CDISC `LBLOINC`、公衛通報 |

## LOINC 名稱的六個軸

每個 LOINC 代碼由六個軸定義；任何一軸不同就是不同代碼。

| 軸 | 意義 | `2345-7` 的值 |
| --- | --- | --- |
| Component | 量什麼 | Glucose |
| Property | 量的性質 | `MCnc`（質量濃度） |
| Time | 單一時間點或一段時間 | `Pt`（時間點） |
| System | 檢體 | `Ser/Plas`（血清或血漿） |
| Scale | 尺度 | `Qn`（定量） |
| Method | 方法（可空白） | 空白（不限方法） |

`2345-7` = *Glucose [Mass/volume] in Serum or Plasma*。對照：`1558-6` 是空腹血糖（Component 不同）、`2339-0` 是全血血糖（System 不同）、`14749-6` 是以 `mmol/L` 計的血糖（Property 為 `SCnc` 物質濃度）。

> 對應本地代碼時最常見的錯誤是**檢體與單位**：血清 vs 全血、質量濃度 vs 莫耳濃度會對到不同 LOINC。對應前先確認檢驗科的檢體類型與報告單位。

## 涵蓋範圍

| 類別 | 例 |
| --- | --- |
| 檢驗 | 生化、血液、微生物、分子檢驗 |
| 臨床量測 | 生命徵象、身高、體重、BMI |
| 基因檢測 | `48018-6` Gene studied、`81252-9` Discrete genetic variant、`69548-6` Genetic variant assessment（FHIR Genomics Reporting IG 使用） |
| 問卷 / 量表 | PHQ-9、PROMIS |
| 文件類型 | 出院摘要、放射報告、病理報告 |

單位寫法見 [UCUM](ucum.md)；檢驗值在 FHIR 中的結構見 [FHIR](fhir.md#resource-與範例)。
