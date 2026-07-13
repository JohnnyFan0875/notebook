# Azure Services Overview

這一頁的目標不是列出所有 Azure 產品，而是把常見服務放進幾個穩定分類，幫助你判斷一個 workload 應該先從哪一類解法開始找。

## 先用服務類別思考

學 Azure 時，很容易被大量產品名稱分散注意力。比較好的方式是先問：

- 這個需求主要是 compute、storage、database，還是 networking
- 我需要的是較高控制權，還是較高託管程度
- 這個 workload 偏應用交付、資料平台，還是基礎網路能力

先把問題放到類別裡，再去看服務名稱，通常比較不會迷路。

## Compute

Compute 的核心問題是：程式要跑在哪裡，以及你願意自己管理多少底層細節。

### Virtual Machines

`Azure Virtual Machines` 是最典型的 IaaS compute。

適合：

- 需要自己控制 OS 與 runtime
- 跑傳統伺服器型 workload
- 搬遷既有 legacy applications
- 進行需要較高自由度的 analytics 或 data-related tasks

如果你想保留最高控制權，通常先想到 VM。

### App Service

`Azure App Service` 比較偏向 web application 的託管式平台。

可以先把它理解成：

- 平台幫你處理更多部署與維運細節
- 比 VM 更接近 PaaS
- 適合 web app 與網站託管場景

### Functions

`Azure Functions` 是 Azure 常見的 serverless compute 選項。

適合：

- 事件驅動任務
- 短時執行的程式邏輯
- 希望把基礎設施管理責任再往下交給平台

### Containers

如果應用已經容器化，Azure 也提供不同層級的容器選項。

#### Azure Container Instances

`Azure Container Instances` 適合：

- 快速啟動容器
- 測試或執行單一應用
- 不想先管理完整 orchestrator

#### Azure Kubernetes Service

`Azure Kubernetes Service (AKS)` 則比較適合：

- microservices architecture
- 需要 orchestration 的 containerized applications
- 希望獨立維護、擴展或更新多個服務元件

簡單說：

- 想快速跑容器，先想到 `Container Instances`
- 想管理大規模容器編排，先想到 `AKS`

## Storage

Azure storage 不只是一種東西。入門時先用資料型態與存取方式來分，比背產品有效。

### Blob Storage

`Blob Storage` 是 object storage。

適合：

- 檔案
- 文件
- 備份
- 非結構化資料

它是 Azure 很核心的儲存入口之一。

### Azure Files

`Azure Files` 是託管式檔案共享服務。

適合：

- 多台機器共享檔案
- 需要檔案系統語意
- 想把共享檔案放在集中式 cloud location

### Table Storage

`Table Storage` 可以先理解成較輕量的 NoSQL key-value / semi-structured storage。

適合：

- 結構較簡單的非關聯式資料
- 不需要完整關聯式資料庫功能的情境

### Queue Storage

`Queue Storage` 比較偏訊息與非同步處理用途。

這提醒我們 storage 不只是存檔，也常被拿來協調系統之間的工作流。

### Disk Storage

Azure 也提供給 VM 使用的磁碟型儲存。

可以先把它理解成：

- 比較接近運算實例的持久化磁碟
- 常和 VM 一起出現
- 適合伺服器型 workload 的作業系統與資料磁碟

## Storage Redundancy Choices

Azure storage 還有一個重要維度是冗餘策略。

### LRS

`Locally Redundant Storage (LRS)` 可以先理解成：

- 複本保留在 primary region 內
- 成本通常較低
- 保護範圍較偏單一區域內的硬體失效

### ZRS

`Zone-Redundant Storage (ZRS)`：

- 複本分散在同一 region 的不同 availability zones
- 比 LRS 更強調區域內高可用

### GRS

`Geo-Redundant Storage (GRS)`：

- 會把資料複製到 secondary region
- 比較偏跨 region 的額外保護

### GZRS

`Geo-Zone-Redundant Storage (GZRS)`：

- 同時結合 zone-level 與 geo-level 冗餘
- 既強調區域內高可用，也兼顧 regional outage 保護

這些選項的差異，核心都在回答一件事：你希望資料在什麼範圍的失效下仍然可用。

## Databases

Azure 的資料服務也應該先按 workload 類型來分。

### Azure SQL

`Azure SQL` 比較偏託管式關聯式資料庫。

適合：

- 傳統交易型應用
- schema 較明確的 relational workload

### Cosmos DB

`Cosmos DB` 比較偏 NoSQL 與全球分散式資料需求。

適合：

- 需要高擴展與低延遲
- 不適合硬套進傳統 relational model 的應用資料

### Synapse

`Azure Synapse` 比較偏分析型與資料平台場景。

可以先把它理解成：

- 偏資料倉儲或分析工作負載
- 不同於日常交易型資料庫

## Networking

Networking 的重點不是把所有元件背下來，而是知道 Azure 怎麼讓你的資源被連接、隔離與對外暴露。

### Virtual Network

`Virtual Network (VNet)` 是 Azure 網路治理的基本邊界。

它回答的問題包括：

- 資源放在哪個私有網路空間
- 哪些系統可以互通
- 流量要怎麼被隔離

### VPN Gateway

`Azure VPN Gateway` 主要用來建立安全的網路連線。

它常出現在：

- on-premises 與 Azure 之間的連通
- 不同網路邊界之間的安全連線

### ExpressRoute

`Azure ExpressRoute` 可以先理解成更專用、企業級的連線方式。

適合：

- 對穩定性、私有性或效能有更高要求的連線場景

### Azure DNS

`Azure DNS` 用來管理 DNS records。

重點是：

- 把網站名稱轉成機器能處理的位址
- 讓 DNS 管理也能落在 Azure 基礎設施中

## 一張簡化地圖

如果把常見 Azure 服務用一句話記住，可以先這樣抓：

| 類別 | 代表服務 | 先記住的用途 |
| --- | --- | --- |
| compute | Virtual Machines, App Service, Functions | 跑應用與程式邏輯 |
| containers | Container Instances, AKS | 跑容器與容器編排 |
| object storage | Blob Storage | 檔案、備份、非結構化資料 |
| file storage | Azure Files | 共享檔案系統 |
| simple NoSQL storage | Table Storage, Queue Storage | 輕量資料與訊息流程 |
| disk storage | managed disks | 給 VM 的持久化磁碟 |
| relational database | Azure SQL | 結構化交易資料 |
| NoSQL database | Cosmos DB | 高擴展、低延遲的非關聯式資料 |
| analytics platform | Synapse | 資料平台與分析 workload |
| networking | VNet, VPN Gateway, ExpressRoute, Azure DNS | 網路隔離、連線與名稱解析 |

## 常見誤區

- 把所有 Azure workload 都當成 VM 問題
- 沒有區分 object、file、disk 與 NoSQL-style storage
- 把容器與 Kubernetes 當成同一層抽象
- 沒先分清楚交易型資料庫和分析型平台
- 只記服務名稱，不去想控制權、資料型態與連線邊界

## Related Concepts

- [Azure Fundamentals](azure-fundamentals.md)
- [Cloud Computing Fundamentals](cloud-computing-fundamentals.md)
- [Databricks Foundations](../../data-science/data-engineering/databricks-foundations.md)

[Back to Cloud](README.md)
