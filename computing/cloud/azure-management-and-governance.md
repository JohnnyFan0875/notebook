# Azure Management and Governance

Azure 的 management 與 governance 不是附加功能，而是讓雲端資源能被持續管理、觀測、控成本並符合組織規範的控制層。

如果 [Azure Fundamentals](azure-fundamentals.md) 偏向平台心智模型，[Azure Services Overview](azure-services-overview.md) 偏向服務分類，這一頁則更關心：你要怎麼和 Azure 互動、怎麼管資源、怎麼控成本、怎麼建立治理規則。

## 先分清楚 service 和 resource

教材一開始有一個很重要的區分。

### Service

`Service` 是一組功能能力或平台元件。

例如：

- Azure Monitor
- Azure Resource Manager
- Microsoft Cost Management

### Resource

`Resource` 是 service 之下可以被管理的具體物件。

例如：

- database
- web application
- virtual machine

Key point: service 是能力類別，resource 是被建立、修改、刪除與計費的實體。

## 和 Azure 互動的主要方式

Azure 不只有一個操作入口，不同角色會用不同介面。

### Azure Portal

`Azure Portal` 是圖形化主控台。

適合：

- 日常查看資源
- 手動管理服務
- 需要 dashboard 式視角的使用者

### PowerShell and Azure CLI

`PowerShell` 與 `Azure CLI` 都偏向腳本化與自動化管理。

適合：

- IT 或平台團隊
- 重複性管理任務
- 需要自動化與批次操作的情境

### Azure Arc

`Azure Arc` 可以先理解成把外部資源拉回 Azure 管理脈絡中的方式。

它的價值在於：

- 不只管理原生 Azure 資源
- 也能把外部環境納入統一管理視角

### Azure Mobile

`Azure Mobile` 比較像輕量監看與隨手管理入口。

重點不是完整取代 Portal，而是讓使用者能在外出時快速掌握資源狀態。

## Resource Management

Azure 的管理核心，仍然是圍繞資源如何被組織與操作。

### Resource Groups

`Resource Group` 是相關資源的邏輯集合。

它的重要性不只是分資料夾，而是可以在群組層級套用：

- tags
- properties
- access roles

也就是說，resource group 是資源治理的實務邊界之一。

### Azure Resource Manager

`Azure Resource Manager (ARM)` 是 Azure 的資源管理層。

它負責：

- create / update / delete resources
- 處理 access control 與 resource properties
- 透過 resource providers 執行具體資源操作

如果 resource group 是治理容器，ARM 就是協調資源生命週期與管理動作的控制面。

### Resource Providers

`Resource provider` 可以先理解成管理特定資源類型的專門模組。

例如：

- `Microsoft.Compute` 管 virtual machines 相關能力

心智模型上：

- ARM 像總承包或管理中樞
- resource providers 像不同專業工種

ARM 不直接實作每種資源，而是依賴 providers 去完成特定任務。

### ARM Templates

`ARM templates` 的價值在於把資源定義變成可重複使用的 IaC。

常見特徵包括：

- 定義與配置資源供重複部署
- 模組化組合較複雜的環境
- 可與 Azure DevOps pipelines 整合
- 支援 versioning
- 可用內建模板，也可用 `Bicep` 自訂

這讓資源部署從手動點選，走向可版本化、可自動化的管理方式。

## Cost Management

雲端成本治理的第一步不是省錢技巧，而是知道哪些因素在驅動成本。

### What Affects Cost

教材整理的幾個主要因素包括：

- consumption
- subscription type
- resource type and settings
- region

也就是說，成本不只由「有沒有開資源」決定，也和定價層級、地理位置與跨區傳輸有關。

### Ways to Manage Cost

比較實務的做法通常包括：

- 找出 underused 或過度昂貴的資源
- 評估短期彈性與長期承諾的 pricing model 取捨
- 減少不必要的 inter-regional data transfers
- 用 budgets 與 alerts 建立監控機制

### Cost Tools

#### Pricing Calculator

`Pricing Calculator` 適合：

- 預估特定資源配置的成本
- 規劃個別服務或組合方案
- 在正式建立資源前先做粗估

#### TCO Calculator

`TCO Calculator` 適合：

- 比較 on-premises 與 Azure Cloud 的總持有成本
- 把隱性營運成本一起納入考量
- 支援 migration 評估

#### Cost Management

`Cost Management` 是 Azure 的成本治理中樞。

可以先把它理解成：

- 成本與帳務相關的 central hub
- 可設定 budgets 與 cost alerts
- 可做 cost analysis
- 可把成本資料匯出到外部系統

## Governance and Compliance

治理的核心不是列規則，而是把規則做成可繼承、可檢查、可落地的控制。

### Azure Policy

`Azure Policy` 用來定義與套用資源規則。

它的作用包括：

- 設定 rules and standards for resources
- 強制符合特定 standards 或 regulations
- 在不同層級套用並自動繼承到下層
- 做自動補救，例如補上 missing tags

這讓治理不只是文件要求，而是實際作用在資源上的平台控制。

### Policy Initiatives

`Initiatives` 是一組相關 policies 的集合。

適合：

- 用較高層級目標管理多條規則
- 對應常見法規或標準情境
- 同時檢查多個治理要求

例如教材提到的方向包括：

- MFA 是否啟用
- subscription 是否不只有單一 owner
- 管理者群組是否缺少必要成員

### Azure Blueprints

`Azure Blueprints` 比較偏向標準化部署與環境複製。

它的重點包括：

- standardize new subscriptions or deployments
- 把「應該部署什麼」和「實際部署了什麼」連起來
- 用 versioning 追蹤更新或回到先前版本

### Blueprint Artifacts

Blueprint 的組成元件稱為 `artifacts`。

常見內容包括：

- role assignments
- policy assignments
- resource group configuration
- predefined resource templates

這讓 blueprint 不只是抽象原則，而是能直接包含治理與部署元件。

### Policy vs Blueprint

可以先這樣分工：

- `Azure Policy`: 定義並強制規則
- `Azure Blueprints`: 把規則、角色與資源配置一起打包成可重複部署的標準環境

如果 Policy 回答「什麼規則必須被遵守」，Blueprint 更像在回答「新環境應該怎麼被標準化建立」。

## Monitoring

治理不只在建立資源時發生，也包括持續觀察系統是否健康、成本是否失控、應用是否退化。

### Azure Monitor

`Azure Monitor` 是 Azure 的綜合監控平台。

可以先用三段 workflow 理解它：

1. data collection
2. analysis and visualization
3. proactive monitoring and alerts

### Metrics and Logs

Azure Monitor 裡最重要的兩類資料是：

- `metrics`: 數值型監控資料，例如 memory usage
- `logs`: 事件型資料，例如某個使用者做了哪些變更

這兩者通常分工很清楚：

- metrics 適合做時間序列觀察與門檻告警
- logs 適合做查詢、過濾、稽核與診斷

### Application Insights

`Application Insights` 比較偏應用程式效能管理。

適合：

- 偵測與診斷應用問題
- 觀察 availability、performance、usage
- 找錯誤、bugs 與 live monitoring 信號

### Log Analytics

`Log Analytics` 比較偏系統層與資源層的觀測分析。

適合：

- 追蹤資源表現
- troubleshooting and diagnostics
- capacity planning
- security and compliance 分析

### Alerts

Azure Monitor 的 `Alerts` 用來建立自動通知與回應機制。

重點包括：

- 根據特定 metrics 或條件觸發
- 用不同通知通道發送警示
- 問題持續時可 escalated
- 可搭配 automatic remediation

### Service Health

`Service Health` 主要回答 Azure 平台本身發生了什麼。

常見用途：

- 看 planned maintenance
- 看 outages and incidents
- 提前知道 upcoming updates and changes

這和應用監控不同，它更偏雲端供應商層級的健康狀態。

### Advisor

`Azure Advisor` 提供個人化建議，幫你優化 Azure 使用方式。

它通常從幾個面向提供建議：

- cost
- security
- performance
- reliability
- operational excellence

心智模型上，可以把它理解成一個持續巡檢與優化建議入口，而不是單一監控報表。

## 一個最小心智模型

如果只想先記住最重要的東西，可以抓這六點：

1. service 是能力集合，resource 是被實際管理與計費的物件
2. Azure Portal、CLI、PowerShell、Arc 代表不同操作方式與自動化程度
3. ARM、resource groups、resource providers、templates 構成資源管理主幹
4. 成本治理要同時看驅動因素、估算工具、預算與持續分析
5. Azure Policy 管規則，Azure Blueprints 管標準化部署
6. Azure Monitor、Service Health、Advisor 共同構成持續觀測與優化回路

## Related Concepts

- [Azure Fundamentals](azure-fundamentals.md)
- [Azure Services Overview](azure-services-overview.md)
- [Governance](../../data-science/data-engineering/governance.md)
- [AWS Security and Cost Management](aws-security-and-cost-management.md)

[Back to Cloud](README.md)
