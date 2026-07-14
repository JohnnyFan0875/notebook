# Azure Fundamentals

這份筆記的目標不是列出所有 Azure 服務，而是先建立一個穩定的入門心智模型，知道 Azure 在雲端版圖中的角色、資源怎麼被管理，以及 storage 大致怎麼分。

## Azure 是什麼

Azure 是 Microsoft 提供的雲端平台。

如果 [Cloud Computing Fundamentals](cloud-computing-fundamentals.md) 講的是雲端的一般概念，這一頁就是把那些概念放到 Azure 這個供應商上理解。

Azure 常出現在這些情境：

- 企業既有系統已經深度使用 Microsoft 生態
- 身分管理、治理與權限控管需求明確
- 團隊希望把基礎設施、資料服務與應用部署放進同一個平台

## Regions, Zones, and Reliability

理解 Azure 時，除了服務名稱，另一個重要視角是可用性與地理配置。

### Region

`Region` 是 Azure 在某個地理區域內提供的一組雲端基礎設施。

它通常和這些問題有關：

- 使用者離服務有多近
- 是否有資料主權或法規要求
- 災難復原是否需要跨地理區域

### Availability Zone

`Availability Zone` 可以理解成同一個 region 內彼此分散的可用性單位。

心智模型上：

- region 解決的是地理層級
- zone 解決的是區域內的高可用層級

如果 workload 需要更高韌性，常會考慮跨 zone 或跨 region 配置。

## 先用三個層次理解 Azure

學 Azure 時，先不要急著背服務名稱，可以先分三層看：

1. 資源怎麼被組織與管理
2. 常見服務落在哪些大類
3. 資料應該放在哪一種 storage

## 資源管理的基本單位

Azure 的一個核心特色，是大多數能力都被包裝成可以管理的 `resource`。

常見例子包括：

- virtual machine
- storage account
- database
- virtual network

這些資源通常可以透過 portal、CLI、SDK 或 IaC 工具建立與管理。心智模型上，Azure 不是一堆獨立產品，而是一組可程式化管理的資源。

### Resource Group

`Resource Group` 是 Azure 很重要的整理與治理單位。

可以先把它理解成：

- 一個邏輯上的資源容器
- 用來把同一個應用或工作負載的資源放在一起
- 方便做權限、部署、標籤與生命週期管理

例如一個 web application 可能會把這些東西放在同一個 resource group：

- app service 或 virtual machine
- storage account
- database
- monitoring 資源

它不一定代表技術上的依賴關係，但通常代表治理與營運上想一起管理的一組東西。

### Azure Resource Manager

`Azure Resource Manager (ARM)` 可以先理解成 Azure 的中央管理層。

它的角色大致是：

- 提供一致的資源管理入口
- 對 resources 與 resource groups 套用管理邏輯
- 在建立、修改、刪除資源時檢查權限

如果 resource 是 Azure 的基本物件，ARM 就是用來協調這些物件如何被建立與管理的控制面。

## 常見服務類別

Azure 的產品名稱很多，但入門時先抓服務類別比較有效。

### Compute

Compute 主要回答「程式跑在哪裡」。

常見方向包括：

- virtual machine
- app service
- functions
- container 相關服務

可以先用控制權與託管程度來區分：

- 想保留較高控制權時，通常會想到 VM
- 想把部署與維運壓低時，會偏向 PaaS 或 serverless

### Serverless vs. Stateless

這兩個詞很容易混在一起，但其實不是同一件事。

- `Serverless`: 不是沒有伺服器，而是平台幫你抽象掉更多基礎設施管理，並依 workload 自動擴縮
- `Stateless`: 每次請求都被視為新的互動，不保留前一次狀態

也就是說：

- serverless 在回答「誰管理基礎設施」
- stateless 在回答「應用是否保留狀態」

一個服務可以是 serverless，也可以是 stateless，但兩者不是同義詞。

### Networking

Networking 主要處理：

- 資源之間如何連線
- 哪些服務暴露給外部
- 流量如何被隔離與保護

心智模型上，它和 AWS 的 VPC 類概念相近，都是在回答網路邊界與流量治理問題。

### Data and Databases

Azure 也提供關聯式資料庫、NoSQL、分析與資料平台能力。

入門時比較重要的不是背產品，而是先分清楚：

- 這是交易型資料庫還是分析型系統
- 這是應用資料，還是資料平台的一部分
- 這個 workload 需要高控制權，還是偏好 managed service

## Azure 與部署流程

原始教材有提到 Azure 服務可與 `GitHub`、`Azure DevOps`、`Bitbucket` 整合，並支援 continuous deployment。

這裡最值得保留的不是平台名稱本身，而是這個觀念：

- 應用部署可以直接接到原始碼管理與 CI/CD 流程
- 更新可以透過自動化方式推進
- 雲端平台不只提供基礎設施，也提供應用交付的整合能力

換句話說，Azure 不只是放主機的地方，也常被當成部署與營運流程的一部分。

## Azure Storage 的基本分類

Azure storage 入門時，先不要背太多產品細節，先分清楚資料型態。

### Object Storage

`Blob Storage` 適合放：

- 檔案
- 影像
- 備份
- data lake 類資料

如果你熟悉 AWS，可以把它先類比成接近 `S3` 的 object storage 心智模型。

### File Storage

檔案共享型需求比較接近 file storage。

適合：

- 想保留檔案系統語意
- 多個應用或節點要共享目錄

### Queue and Message-like Storage

某些 storage 類型更偏向訊息或非同步流程用途，而不是單純存檔。

這提醒我們一件事：storage 不只是「把資料放起來」，也常參與系統之間的解耦與資料交換。

### Structured or Semi-structured Storage

有些 Azure storage 服務比較偏 key-value 或結構化資料存放。

入門重點不是記名稱，而是理解 Azure 會依資料存取模式，提供不同的儲存抽象，而不是只有一種萬用磁碟。

## Storage Account 心智模型

Azure storage 常會圍繞 `storage account` 來管理。

可以先把它理解成：

- 儲存服務的管理邊界
- 權限、設定與命名空間的承載單位
- 不同儲存能力的進入點

實務上先想清楚資料類型、存取模式與成本要求，再決定要怎麼設計 storage account，通常比直接選產品名稱更重要。

### Storage Redundancy

Azure storage 還有一個很重要的設計面向，是資料冗餘怎麼做。

教材裡最值得保留的兩種心智模型是：

- `Geo-redundant storage`: 複本分散到不同 regions
- `Zone-redundant storage`: 複本分散在同一個 region 內的不同 availability zones

這提醒我們：

- 冗餘不只是備份問題
- 它和可用性、故障範圍與成本都有關

選 storage 時，不只要問「存哪裡」，也要問「失效時怎麼撐住」。

## 一個最小 Azure 心智模型

如果只想先記住最重要的東西，可以抓這六點：

1. Azure 是一個可程式化管理資源的雲端平台
2. `Resource Group` 是理解 Azure 治理方式的核心入口
3. `Region` 和 `Availability Zone` 代表的是地理與高可用設計，不只是命名細節
4. 服務先分成 compute、networking、data、storage 幾類來看
5. Azure 常和原始碼平台與部署流程整合，不只是基礎設施
6. storage 先分 object、file、資料抽象與 redundancy，不要把所有需求視為同一件事

## 常見誤區

- 把 Azure 理解成只有 VM 的主機租賃平台
- 沒有先設計 resource group，就讓資源散落各處
- 把所有 storage 需求都視為同一類問題
- 只看服務名稱，不看治理、部署與維運流程

## Related Concepts

- [Cloud Computing Fundamentals](cloud-computing-fundamentals.md)
- [AWS Services Overview](aws-services-overview.md)
- [MLOps Overview](../../data-science/machine-learning/production/mlops-overview.md)

[Back to Cloud](README.md)
