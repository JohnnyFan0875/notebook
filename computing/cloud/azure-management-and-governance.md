[Computing](../README.md) › [Cloud](README.md) › Azure 管理與治理

# Azure 管理與治理 (Azure Management and Governance)

管理與治理是讓雲端資源能被持續操作、觀測、控制成本並符合組織規範的控制層。[Azure 基礎](azure-fundamentals.md) 講資源階層，[Azure 服務總覽](azure-services-overview.md) 講服務分類，本篇講怎麼和 Azure 互動、怎麼部署與管理資源、怎麼控成本、怎麼訂規則與監控。

| 名詞 | 意義 | 例子 |
| --- | --- | --- |
| 服務 (service) | 一類功能能力 | Azure Monitor、Cost Management |
| 資源 (resource) | 服務之下被建立、修改、刪除與**計費**的實體 | 一台 VM、一個資料庫 |

## 操作介面

| 介面 | 適合 |
| --- | --- |
| Azure Portal | 圖形介面：瀏覽、手動管理、dashboard |
| Azure CLI（`az`） | 跨平台腳本與自動化：`az group create -n rg-demo -l eastasia` |
| Azure PowerShell（`Az` 模組） | Windows / PowerShell 為主的團隊 |
| Cloud Shell | 瀏覽器內建的 CLI / PowerShell，免安裝 |
| Azure mobile app | 外出時監看狀態、處理警示 |
| Azure Arc | 把地端、其他雲的伺服器與 Kubernetes 納入 Azure 統一管理（政策、監控） |

## 資源部署與 IaC

| 元件 | 作用 |
| --- | --- |
| Azure Resource Manager (ARM) | 所有操作的控制平面：驗證權限，交給資源提供者執行 |
| 資源提供者 (resource provider) | 負責特定資源類型的模組，如 `Microsoft.Compute`（VM）、`Microsoft.Storage` |
| ARM 範本（JSON）/ Bicep | 宣告式 IaC：資源定義可版本控制、重複部署、模組化，可接 CI/CD；新專案用 Bicep（語法較簡潔，會編譯成 ARM JSON） |
| Template Specs | 把範本存成 Azure 資源，可版本化並分享 |
| Deployment Stacks | 把一組資源當成單位部署與管理，可鎖定以防被修改或刪除 |
| 資源鎖 (lock) | `CanNotDelete` / `ReadOnly`，避免誤刪重要資源 |
| 標籤 (tag) | `project`、`owner`、`env` 等鍵值，用於成本歸屬與篩選 |

```bash
az deployment group create -g rg-demo -f main.bicep -p env=dev    # 部署 Bicep 範本到資源群組
```

> 跨雲常用 Terraform 做 IaC，概念相同。

## 成本管理

| 成本驅動因素 | 說明 |
| --- | --- |
| 用量 | 運算時間、儲存量、交易數 |
| 資源類型與設定 | 規格、層級（Premium vs Standard） |
| 區域 | 同一服務在不同區域價格不同 |
| 資料傳輸 | 傳出 Azure 與跨區域傳輸收費 |
| 訂用帳戶類型 | 隨用隨付、企業合約、學生 / 免費額度 |

| 工具 | 用途 |
| --- | --- |
| Pricing Calculator | 建立資源前估算費用 |
| TCO Calculator | 比較地端與 Azure 的總持有成本（含電力、機房、人力），用於遷移評估 |
| Cost Management | 成本分析、預算與警示、依標籤 / 資源群組拆分、匯出 |
| Azure Advisor（成本建議） | 找出閒置或過大的資源 |
| Reservations / Savings Plans | 承諾 1 或 3 年換折扣 |
| Spot VMs | 可被收回的便宜 VM，適合可中斷的批次工作 |

## 治理與合規

| 工具 | 作用 |
| --- | --- |
| Azure RBAC | 依角色授權（Owner、Contributor、Reader 與自訂角色），在任一層級指派並向下繼承 |
| Azure Policy | 定義並強制資源規則：禁止某些區域、強制加標籤、要求加密；可稽核、拒絕或自動補救（如補上缺少的標籤） |
| Policy initiative | 一組相關政策的集合，對應某個合規目標（例如 ISO 27001、HIPAA 相關的內建 initiative） |
| Microsoft Defender for Cloud | 安全態勢評分與建議 |
| Microsoft Purview | 資料治理：資料目錄、分類、資料譜系，見 [資料治理](../../data-science/data-engineering/governance.md) |

| | Azure Policy | 標準化部署 |
| --- | --- | --- |
| 回答 | 什麼規則必須被遵守 | 新環境應該怎麼被標準化建立 |
| 工具 | Policy、initiative | Template Specs + Deployment Stacks（取代 Azure Blueprints） |

> **Azure Blueprints 已淘汰**：Microsoft 公告 Blueprints（預覽版）自 2026 年 7 月起淘汰，以 Template Specs（版本化的範本）與 Deployment Stacks（指派、生命週期與鎖定）取代。舊教材中 Blueprint 的「artifacts」（角色指派、政策指派、資源群組、範本）在新做法中分別由 RBAC、Policy 與 Bicep 範本表達。

## 監控

```text
資料收集（metrics、logs）→ 分析與視覺化（Log Analytics、workbooks、dashboard）→ 警示與自動回應
```

| 工具 | 作用 |
| --- | --- |
| Azure Monitor | 統一的監控平台 |
| Metrics | 數值時間序列（CPU、記憶體）：適合門檻警示 |
| Logs（Log Analytics 工作區） | 事件紀錄：用 KQL 查詢、篩選、稽核、診斷 |
| Application Insights | 應用程式效能監控：可用性、回應時間、錯誤、使用狀況 |
| Alerts | 依指標或查詢條件觸發；透過 action group 通知（email、SMS、webhook）或自動補救 |
| Activity Log | 訂用帳戶層級的操作紀錄：誰在何時建立 / 刪除了什麼 |
| Service Health | **Azure 平台本身**的狀態：服務中斷、計畫維護、即將到來的變更 |
| Azure Advisor | 個人化建議：成本、安全、可靠性、效能、卓越營運 |

```kusto
// Log Analytics（KQL）：過去一天各 VM 的平均 CPU
Perf
| where TimeGenerated > ago(1d) and CounterName == "% Processor Time"
| summarize avg(CounterValue) by Computer
| order by avg_CounterValue desc
```

## 重點整理

| 主題 | 一句話 |
| --- | --- |
| 服務 vs 資源 | 服務是能力，資源是被管理與計費的實體 |
| 介面 | Portal 手動、CLI / PowerShell 自動化、Arc 納管外部資源 |
| 部署 | ARM 是控制平面，Bicep / Template Specs / Deployment Stacks 讓部署可重複 |
| 成本 | 先看驅動因素，部署前估算，部署後用預算與分析追蹤 |
| 治理 | RBAC 管人、Policy 管規則、範本管標準環境 |
| 監控 | Monitor 看自己的系統，Service Health 看平台，Advisor 給建議 |
