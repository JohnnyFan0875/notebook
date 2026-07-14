# Governance

## Why Governance Exists

資料治理不是額外的行政負擔，而是讓團隊真正知道自己手上有哪些資料、資料是否可信、誰可以使用，以及是否符合安全與法規要求。

一個簡單的理解方式是：governance 讓資料不只是「存在」，而是能被組織可靠地理解、保護與使用。

## Core Questions

Data governance 通常圍繞兩組問題：

### Know Our Data

- 我們有哪些資料？
- 資料從哪裡來？
- 品質如何？
- 定義與責任歸屬是什麼？

### Secure Our Data

- 誰可以存取哪些資料？
- 敏感資料如何被保護？
- 是否符合合規與法規要求？

## Common Roles

| 類別 | 角色 | 主要責任 |
| --- | --- | --- |
| Governor / Approver | data owner / steward | 制定與落實治理策略、分類資料、管理資料 |
| User | data analyst / scientist | 使用資料做分析、決策與模型 |
| Ancillary / Additional | executive、legal | 支援整體治理策略與合規要求 |

## Metadata and Catalogs

治理的基礎通常不是先寫規則，而是先把 metadata 建起來。

常見 metadata 類型：

- technical metadata: data types、欄位名稱、資料來源、表關係
- business metadata: 定義、規則、data owner
- operational metadata: timestamps、ETL job status、quality metrics
- usage metadata: 誰在何時用過資料、怎麼使用

當這些 metadata 被集中管理後，才比較可能做出可用的 data catalog、lineage 與審計能力。

## Lineage and Quality

- **Data lineage** 關心資料的來源、經過哪些轉換、最後流向哪裡。
- **Data quality** 關心資料是否完整、正確、一致、及時。

這兩者通常一起出現，因為當資料出錯時，團隊需要同時回答：

1. 哪裡出了問題？
2. 哪些下游表、報表或模型受影響？

## Access Control, Encryption, and Masking

常見的治理與安全控制包括：

- access control: 定義誰能存取哪些資料
- encryption: 保護 at rest 與 in transit 的資料
- data masking: 讓資料可被使用，但不直接暴露敏感內容

在雲端環境裡，這些概念常會對應到：

- IAM / role-based access control
- key management services
- network or context-based restrictions

## Governance in Managed Analytics Platforms

像 Microsoft Fabric 這類整合式平台，治理常不只發生在單一 table 或 storage path，而是同時分布在：

- tenant level settings
- capacity management
- workspace administration
- item-level sharing
- semantic model security

這代表同一份資料，可能同時受到平台管理層、工作區角色、個別 item 權限與 semantic layer 規則影響。

如果只看其中一層，很容易誤以為「已經有權限控制」，但實際上共享路徑可能仍然過寬。

## Least Privilege and Group-Based Access

平台型環境特別適合把 least privilege 做成預設原則：

- 先給最低必要權限
- 盡量用 security groups 管人，而不是逐一指派個人
- 定期審查既有分享與 workspace role
- 把例外權限留下文件與理由

這樣做的原因不是保守，而是因為 analytics platform 往往同時連著 lakehouse、warehouse、reports 與 semantic models，一個過大的權限範圍會在多個下游一起擴散。

## Sensitivity Labels and Classification

除了存取權限，資料分類本身也是治理的一部分。

sensitivity labels 的價值通常在於：

- 標示哪些資料屬於敏感內容
- 讓團隊對同類型資料採一致處理方式
- 支援合規要求與審計溝通
- 降低資料外洩時的辨識與處理成本

標籤本身不等於完整保護，但它能把「哪些資料需要更嚴格對待」這件事提前明確化。

## Dependency Review Before Change

治理不只是在平常限制存取，也包含修改前知道會影響誰。

如果平台能提供 dependency graph 或 impact analysis，就很適合在下列動作前先檢查：

- 分享某個 item
- 修改 semantic model
- 調整 warehouse 結構
- 更新 pipeline 或上游來源

因為真正高成本的問題，常不是單一物件壞掉，而是團隊不知道有哪些報表、模型或資料產品會一起被波及。

## Practical Reminders

- 沒有 metadata 與 ownership，治理通常只會停留在口號。
- catalog、lineage、access policy 應該跟資料平台一起設計，而不是等資料量爆掉後再補。
- 治理的目標不是讓資料更難用，而是讓正確的人更安全、更有信心地使用資料。
- 在整合式分析平台裡，tenant、workspace、item、semantic model 往往是不同層的治理邊界，不能只檢查其中一層。

[Back to Data Engineering](README.md)
