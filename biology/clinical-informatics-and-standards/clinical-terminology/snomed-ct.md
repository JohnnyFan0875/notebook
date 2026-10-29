[臨床資訊與標準](../README.md) › [臨床術語](README.md) › SNOMED CT

# SNOMED CT

SNOMED CT (Systematized Nomenclature of Medicine – Clinical Terms) 是最完整的臨床術語本體，涵蓋疾病、臨床發現、處置、解剖、微生物、物質等。它的目的是讓病歷中的臨床語意可被電腦理解；ICD 則偏向統計與申報分類，兩者互補。

| 項目 | 內容 |
| --- | --- |
| 維護 | SNOMED International（前身 IHTSDO） |
| 網站 / 瀏覽器 | [snomed.org](https://www.snomed.org)、[SNOMED CT Browser](https://browser.ihtsdotools.org/) |
| 授權 | 會員國境內免費（向國家發布中心登記）；非會員國經 MLDS 申請年度授權，可能收費 |
| 發布 | International Edition 定期發布；各會員國另有 national extension（如 US Edition） |
| 何時用 | EHR 問題清單、臨床表型定義、OMOP 的 condition / procedure 標準概念 |

## 概念模型

| 元素 | 說明 | 例 |
| --- | --- | --- |
| Concept ID (SCTID) | 數字代碼，只代表概念、不帶語意 | `44054006` |
| Fully Specified Name (FSN) | 唯一、帶語意標籤的全名 | *Diabetes mellitus type 2 (disorder)* |
| Synonym | 同義詞，含偏好詞 (preferred term) | *Type 2 diabetes mellitus*、*Non-insulin dependent diabetes mellitus* |
| Relationship | 定義語意的邏輯關係 | `is a` → *Diabetes mellitus*；`finding site` → *Structure of endocrine system* |
| Hierarchy | 頂層類別，如 *Clinical finding*、*Procedure*、*Body structure*、*Organism*、*Substance* | — |

```
Clinical finding
 └── Disease
      └── Disorder of endocrine system
           └── Diabetes mellitus
                └── Diabetes mellitus type 2
```

> SNOMED CT 是**多重繼承 (polyhierarchy)**：一個概念可以有多個父節點（例如糖尿病腎病同時是腎臟疾病與糖尿病併發症）。用 `is a` 往下展開所有子孫概念，是定義表型時「這個疾病及其所有亞型」的標準做法。

## 與其他標準的關係

| 對象 | 關係 |
| --- | --- |
| [ICD-10 / 11](icd.md) | 官方 map（SNOMED → ICD-10）存在，通常多對一；適合由臨床記錄產生申報代碼 |
| [FHIR](fhir.md) | `Condition.code`、`Procedure.code`、`Observation.valueCodeableConcept` |
| [OMOP-CDM](omop-cdm.md) | condition 與大部分 procedure 的 standard vocabulary；ICD 等來源碼經 `Maps to` 對到 SNOMED |
| [UMLS](umls.md) | 作為來源術語之一，可經 CUI 對到 MeSH、ICD 等 |
| [HPO](../../genetics/databases/gene-disease-association/hpo.md) | 罕病表型多用 HPO；HPO 與 SNOMED 之間有部分對應 |
