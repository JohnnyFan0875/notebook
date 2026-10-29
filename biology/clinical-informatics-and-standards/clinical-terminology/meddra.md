[臨床資訊與標準](../README.md) › [臨床術語](README.md) › MedDRA

# MedDRA

MedDRA (Medical Dictionary for Regulatory Activities) 是 ICH 制定的法規用醫學術語，用來編碼臨床試驗與上市後監測中的不良事件 (adverse event, AE)、適應症與病史。FDA、EMA、PMDA 等主管機關的安全通報都用它。

| 項目 | 內容 |
| --- | --- |
| 維護 | ICH；由 MedDRA MSSO 負責維護與發行 |
| 網站 | [meddra.org](https://www.meddra.org) |
| 發布 | 每年兩次：3 月（`x.0`）、9 月（`x.1`） |
| 語言 | 多語言（含中文、日文） |
| 授權 | 主管機關、學術、非營利機構可免費；業界依營收訂閱 |
| 何時用 | SDTM `AE` domain、藥物安全通報（ICH E2B）、FAERS / EudraVigilance 資料分析 |

## 五層階層

| 層級 | 意義 | 例 |
| --- | --- | --- |
| SOC (System Organ Class) | 最上層，依器官系統或病因 | Cardiac disorders |
| HLGT (High Level Group Term) | 歸併相關 HLT | Heart failures |
| HLT (High Level Term) | 歸併相關 PT | Heart failures NEC |
| PT (Preferred Term) | 單一醫學概念，**分析與通報的主要層級** | Cardiac failure congestive |
| LLT (Lowest Level Term) | 同義詞、拼寫變體、口語，**編碼時選這層** | Congestive heart failure、CHF |

```
通報原文："病人出現 CHF"
 → LLT  CHF
 → PT   Cardiac failure congestive
 → HLT  Heart failures NEC
 → HLGT Heart failures
 → SOC  Cardiac disorders（primary SOC）
```

> 一個 PT 可以屬於多個 SOC（例如感染性疾病同時在感染 SOC 與器官 SOC），但每個 PT 只有一個 **primary SOC**，彙總計數時用 primary SOC 避免重複計算。

## 分析時的工具

| 工具 | 用途 |
| --- | --- |
| SMQ (Standardised MedDRA Queries) | 預先定義的一組 PT，用於找某類安全訊號（如「肝損傷」、「QT 延長」）；有 narrow / broad 範圍 |
| 版本對齊 | 長期試驗或整合分析要把所有資料重編到同一版 MedDRA |
| 不均衡比例分析 | FAERS 等自發通報資料以 PT 為單位計算 PRR、ROR 找訊號 |

| 對照 | MedDRA | SNOMED CT |
| --- | --- | --- |
| 目的 | 法規通報、安全訊號彙總 | 臨床記錄的完整語意 |
| 粒度 | 為了彙總，刻意較粗 | 細緻 |
| 使用場景 | 試驗、藥物安全 | EHR、問題清單 |

試驗資料的結構見 [CDISC](cdisc.md)。
