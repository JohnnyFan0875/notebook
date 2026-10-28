# Data Governance

前半是平台與技術面的治理（catalog、lineage、存取控制、加密、分類標籤）；後半是組織面的治理計畫（pillars、角色、governance office、策略、衡量）。資料品質規則與監控見 [Data Quality Checks](data-quality-checks.md)。

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

## Governance Program and Operating Model

Data governance is the set of principles, roles, standards, and processes used to ensure that data is trusted, accessible, protected, and used responsibly.

Key point: Data governance is not the same as data management. Governance defines what should happen and who is accountable; data management provides the operational and technical means to make it happen.

### Why Data Governance Exists

Organizations want to use data for reporting, analytics, operations, and AI, but that only works if people trust the data and understand the rules around it.

| Governance Need | Why It Matters |
| --- | --- |
| Trusted, high-quality data | Weak data quality breaks reporting and decision-making |
| Accessible and available data | Useful data must be discoverable and usable |
| Clear roles and accountability | Ownership prevents ambiguity and issue drift |
| Protection and safety | Sensitive data needs policy and control boundaries |

Tip: A governance program creates confidence in data the same way product standards create confidence in a physical product: quality, safety, usability, and accountability are all expected before use.

### What Data Governance Covers

At a high level, governance answers "what must happen," while the framework answers "how we organize people, process, and technology to make it real."

| Concept | Focus |
| --- | --- |
| Data governance | Principles and processes for trusted, high-quality, well-governed data |
| Data governance framework | The blueprint for how people, technology, and processes interact to follow those principles |

### Core Pillars

Most data governance programs revolve around a stable set of pillars.

| Pillar | Practical Meaning |
| --- | --- |
| Ownership and accountability | Named people are responsible for data decisions and issue handling |
| Data quality | Data is accurate, consistent, complete enough, and fit for use |
| Data protection and safety | Access, masking, encryption, and recovery controls protect sensitive data |
| Data use and availability | Data is usable, reliable, and available to the right users |
| Monitoring and communication | Progress, quality, risk, and compliance are measured and shared |
| Data literacy and culture | People across the organization understand why governance matters |

### Data Governance vs. Data Management

These are related but different.

| Area | Main Question |
| --- | --- |
| Governance | What rules, rights, and expectations apply to the data? |
| Management | Which tools, flows, and operational controls implement those rules? |

Key point: Governance without management stays theoretical. Management without governance becomes inconsistent and local to each team.

### Strategy, Policies, and Standards

Governance begins with a strategy and is translated into policies and standards.

| Component | Role |
| --- | --- |
| Strategy | Defines how data should be used and treated to support business goals |
| Policy | States principles, rights, expectations, and responsibilities |
| Standard | Provides consistent rules or best practices for complying with policy |

A strong strategy helps the organization treat data as a real asset rather than a byproduct of applications.

### Processes and Technology

Governance depends on repeatable processes and supporting technical capabilities.

Common governance-supporting processes include:

1. data quality monitoring
2. data issue remediation
3. data sharing review
4. metadata management
5. master data management

Technical capabilities matter because teams need a way to implement, monitor, and track these processes over time.

### Roles in the Governance Model

Governance requires coordination between business and technology.

| Role | Typical Responsibility |
| --- | --- |
| Data owner | Accountable for a data domain and its use decisions |
| Data producer | Creates or captures source data |
| Data engineer | Builds and maintains data pipelines and transformation logic |
| Data custodian | Maintains storage, access, and technical protection |
| Data steward | Oversees data quality, definitions, and day-to-day governance practices |
| Analyst or data scientist | Uses governed data and helps identify quality or interpretation issues |

Tip: Titles vary across organizations, but the important part is that ownership, stewardship, production, and custody are not all left vague.

### The Data Governance Office

Larger organizations often formalize governance through a dedicated office or coordinating function.

| Office Role | Typical Focus |
| --- | --- |
| Chief Data Officer (CDO) | Sets data strategy, drives culture, and aligns governance with business value |
| Data governance lead | Defines framework, policies, and implementation approach |
| Governance consultant or SME | Guides business lines and translates policy into practice |
| Data quality analyst | Profiles data, writes rules, and supports remediation |
| Data architect | Designs secure, integrated data flows and architecture |

Key point: The governance office should coordinate, guide, and measure. It should not become a detached documentation team with no operational influence.

Practical data leadership is often more distributed than the org chart suggests.

Examples:

- a manager who aligns KPI use with team decisions
- an analyst who mentors colleagues and improves data habits
- an engineer who standardizes trustworthy access and definitions
- an operations lead who reinforces shared workflows and adoption

### Sponsorship, Committees, and Collaboration

Governance works best when it has visible sponsorship and a practical interaction model.

| Governance Need | Why It Matters |
| --- | --- |
| Executive sponsorship | Helps resolve conflicts and create organizational momentum |
| Cross-functional committees | Align business, risk, privacy, and technical perspectives |
| Defined interaction model | Clarifies how issues are escalated and resolved |
| Collaboration routines | Prevent governance from becoming isolated or purely reactive |

Warning: Governance often fails not because the framework is wrong, but because no one can actually coordinate across teams when priorities conflict.

### Assessing the Current State

Before building a governance program, teams need to understand where they are starting from.

Typical assessment steps include:

1. identify key data sources and stakeholders
2. interview stakeholders about pain points and responsibilities
3. evaluate current capabilities and maturity
4. document current state and target state
5. analyze gaps and prioritize what matters most

A simple maturity improvement loop is:

1. assess the current maturity level
2. choose specific action items
3. introduce needed tools, processes, or training
4. monitor progress and adjust along the way
5. strengthen collaboration and standardization where gaps persist

Tip: Governance maturity work should be selective. Not every gap deserves equal urgency.

Warning: There is no one-size-fits-all maturity target. The right operating model depends on business goals, team structure, risk profile, and the organization’s starting point.

### Building a Governance Strategy

A data governance strategy should be simple enough to communicate and specific enough to guide action.

Useful components include:

| Strategy Component | Purpose |
| --- | --- |
| Vision statement | Explains the desired future state in clear, motivating language |
| Mission statement | Connects day-to-day action to that future state |
| Value proposition | Shows why the program is worth funding and following |
| Guiding principles | Sets behavioral rules for how data should be treated |
| Roles and responsibilities | Makes enforcement and participation concrete |

Examples of governance value often include:

- more accurate data for action
- stronger compliance and risk control
- increased trust in data for decision-making

### Measurement and Program Monitoring

Governance needs evidence of progress.

| Metric Area | Example |
| --- | --- |
| Data quality | Error rates, completeness, freshness, rule pass rates |
| Risk and privacy | Exposure levels, unresolved issues, control exceptions |
| Compliance | Policy adherence, remediation timeliness, audit findings |
| Program value | Adoption, process coverage, ROI or business impact |

Key point: If governance cannot measure progress, it usually cannot sustain executive support.

### Enabling Governance with Technology

Governance tooling supports consistency, scale, and shared language.

Common examples include:

| Tooling Area | What It Helps With |
| --- | --- |
| Business glossary | Standard definitions and shared vocabulary |
| Metadata management | Discovery, lineage, and context |
| Data quality tooling | Rule execution, profiling, and issue tracking |
| Master data management | Consistent handling of core entities |
| Workflow and issue systems | Remediation, approvals, and auditability |

Tip: Tooling should support the governance model. Buying software before defining ownership and process usually creates shelfware.

### Minimum Standard for a Data Governance Program

Before calling a governance program operational, you should be able to explain:

1. which data domains matter most and who owns them
2. which policies and standards teams are expected to follow
3. how data quality, protection, and access are measured
4. how issues are escalated and remediated
5. what business value the governance program is expected to create
