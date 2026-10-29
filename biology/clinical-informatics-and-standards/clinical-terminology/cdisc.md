[臨床資訊與標準](../README.md) › [臨床術語](README.md) › CDISC

# CDISC SDTM / ADaM

CDISC (Clinical Data Interchange Standards Consortium) 制定臨床試驗資料從收集、整理到送審的標準。最常碰到的是 **SDTM**（把收集到的資料整理成標準 domain）與 **ADaM**（由 SDTM 衍生出可直接做統計分析的資料集）。

| 項目 | 內容 |
| --- | --- |
| 維護 | CDISC |
| 網站 | [cdisc.org](https://www.cdisc.org)；Controlled Terminology 由 NCI EVS 發布 |
| 授權 | 標準文件免費（需註冊） |
| 何時用 | 藥廠 / CRO 的試驗資料處理、送審 FDA / PMDA、分析公開的試驗資料 |

## 標準家族

```
CDASH（收集：CRF 欄位）
   │
SDTM（整理：標準 domain）     SEND（非臨床 / 動物試驗版的 SDTM）
   │  derivation
ADaM（分析：analysis-ready）
   │
TLF（Tables, Listings, Figures → 臨床試驗報告）

Define-XML：描述每個資料集與變數的 metadata，隨資料一起送審
```

## SDTM

每個 domain 一個資料集，用兩個字母代碼命名。

| Domain | 內容 | 主要變數 |
| --- | --- | --- |
| DM | 人口學 | `USUBJID`、`AGE`、`SEX`、`ARM` |
| AE | 不良事件 | `AETERM`（原始描述）、`AEDECOD`（MedDRA PT）、`AESEV`、`AESTDTC` |
| LB | 檢驗 | `LBTESTCD`、`LBORRES`、`LBSTRESN`、`LBSTRESU`、`LBLOINC` |
| VS | 生命徵象 | `VSTESTCD`、`VSSTRESN` |
| EX / CM | 試驗藥物暴露 / 併用藥物 | `EXDOSE`；`CMDECOD`（WHODrug） |

| STUDYID | USUBJID | AETERM | AEDECOD | AESEV | AESTDTC |
| --- | --- | --- | --- | --- | --- |
| STUDY01 | STUDY01-001 | Headache | Headache | MILD | 2024-06-15 |

## ADaM

| 資料集 | 內容 |
| --- | --- |
| ADSL | 每位受試者一列：分組、基線特徵、分析族群旗標（`SAFFL`、`ITTFL`） |
| BDS 結構（ADLB、ADVS…） | 每位受試者 × 參數 × 時間點一列：`PARAMCD`、`AVISIT`、`AVAL`、`BASE`、`CHG` |
| ADAE | 不良事件分析資料集（OCCDS 結構） |
| ADTTE | 存活分析（time-to-event）：`AVAL` 為時間、`CNSR` 為設限旗標 |

| USUBJID | PARAMCD | AVISIT | BASE | AVAL | CHG |
| --- | --- | --- | --- | --- | --- |
| STUDY01-001 | SYSBP | Week 8 | 125 | 120 | -5 |

> ADaM 的核心要求是**可追溯性 (traceability)**：每個衍生變數都要能從 metadata 追到 SDTM 的來源與推導規則。`CHG = AVAL − BASE` 這類規則寫在 Define-XML / 分析資料說明中。

## 術語與法規

| 項目 | 使用 |
| --- | --- |
| 不良事件、病史 | [MedDRA](meddra.md) |
| 藥物 | WHODrug Global |
| 檢驗 | CDISC CT 的 `LBTESTCD`，另以 `LBLOINC` 帶 [LOINC](loinc.md) |
| 單位 | CDISC CT 的 Unit codelist（與 [UCUM](ucum.md) 不完全相同） |
| FDA | NDA / BLA / ANDA 送審，2016-12-17 後開始的試驗須用 SDTM / ADaM（FDA Data Standards Catalog） |
| PMDA（日本） | 電子資料送審須符合 CDISC |
| EMA | 未強制要求 CDISC 格式 |

R 生態系的 [pharmaverse](https://pharmaverse.org/)（`admiral` 產生 ADaM、`sdtm.oak` 產生 SDTM）是目前開源的主要工具。試驗設計（平行、交叉、區集）見 [常見研究設計](../../../data-science/statistics/experimental-design/designs.md)。
