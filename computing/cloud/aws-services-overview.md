# AWS Services Overview

這一頁的目標不是列出所有 AWS 產品，而是把常見服務放進幾個穩定的分類，幫助你判斷一個 workload 大致該從哪裡開始找解法。

## 先用服務類別思考

初學 AWS 很容易卡在服務名稱太多。比較好的方式是先問：

- 我要解決的是 compute、database、storage，還是 networking 問題？
- 我想要的是基礎資源，還是託管程度更高的 managed service？
- 這個需求偏應用交付、資料平台，還是 AI / ML？

## Compute

Compute 是大多數 workload 的起點，差別主要在控制權與託管程度。

### EC2

`EC2` 是虛擬伺服器。

適合：

- 需要自己控制 OS、runtime、儲存配置
- 長時間運行的應用
- 傳統伺服器型 workload

### Lambda

`Lambda` 是 serverless compute。

適合：

- 事件驅動任務
- 短時、按需執行的程式
- 不想自行管理伺服器的情境

### 怎麼選

- 想保留較高控制權，先想到 `EC2`
- 想把維運壓到最低，先想到 `Lambda`

## Databases

資料庫服務的選擇，通常取決於資料模型、查詢模式與擴展方式。

### Amazon RDS

`RDS` 可以理解成託管式關聯式資料庫服務。

重點是：

- 不必自己從零管理底層資料庫基礎設施
- 適合傳統交易型應用
- 關聯式 schema 明確時很常見

### Amazon Aurora

`Aurora` 是 AWS 提供的雲端原生關聯式資料庫選項。

可以先把它理解成：

- 與 RDS 脈絡接近的關聯式體系
- 偏向雲端託管最佳化
- 常被拿來處理需要高可用與較高效能的關聯式 workload

### Amazon DynamoDB

`DynamoDB` 是 NoSQL 託管資料庫。

適合：

- key-value 或文件型資料
- 高吞吐、低延遲需求
- schema 彈性較高的應用

心智模型上，可以把它和 RDS 類服務分開看：

- `RDS / Aurora` 偏關聯式
- `DynamoDB` 偏 NoSQL 與高擴展場景

### Amazon Redshift

`Redshift` 比較偏分析型資料倉儲，而不是日常交易資料庫。

適合：

- BI
- 大規模分析查詢
- 資料倉儲工作負載

## Storage

AWS storage 先用資料存放型態來分，比背產品有效。

### Object Storage: S3

`S3` 是 AWS 最核心的 object storage 服務之一。

適合：

- 檔案與物件儲存
- data lake
- 備份
- 靜態網站資產

常見概念包括：

- object 而不是傳統檔案系統
- 可搭配不同 storage classes 做成本分層
- 可用 lifecycle rules 在儲存類別間轉換

### Block Storage: EBS

`EBS` 偏向提供給運算實例使用的區塊儲存。

可以把它理解成：

- 比較像掛在伺服器旁的磁碟
- 常和 `EC2` 一起出現
- 適合需要持久化磁碟的伺服器型 workload

### File Storage: EFS

`EFS` 是託管式檔案儲存服務。

適合：

- 多個運算節點共享檔案系統
- 需要檔案系統語意，而不是單純 object 存取

## Networking

Networking 的核心不是背全部網路元件，而是知道 AWS 如何讓你的資源被隔離、連接與暴露。

### VPC

`Amazon VPC` 是邏輯上隔離的虛擬網路空間。

它回答的是：

- 你的資源放在哪個網路邊界裡
- 哪些子網可公開，哪些要私有
- 流量如何路由
- 哪些存取要被允許或拒絕

### Subnet, Route, Gateway, ACL

入門時可以先這樣理解：

- `Subnet`: 把 VPC 的位址空間切成較小區塊
- `Route Table`: 決定流量往哪裡走
- `Gateway`: 讓 VPC 連到外部網路或其他網路
- `Network ACL`: 在子網層級控制流量

這些概念一起構成 AWS 網路治理的基本骨架。

### CloudFront

`CloudFront` 比較像全球內容分發層。

適合：

- 加速靜態內容傳遞
- 讓全球使用者更快拿到內容
- 搭配 edge locations 降低延遲

## AI / ML Services

AWS 的 AI / ML 服務可以先分成兩類：

- 直接可用的預訓練 AI 能力
- 自己建模、訓練與部署的 ML 平台

### 預訓練 AI 服務

教材裡出現的例子包括：

- `Amazon Translate`: 文字翻譯
- `Amazon Polly`: 文字轉語音
- `Amazon Lex`: 對話式介面與 chatbot
- `Amazon Comprehend`: NLP 分析
- `Amazon Rekognition`: 影像分析

它們的共同特徵是：

- 不一定要自己從零訓練模型
- 適合把 AI 能力快速嵌入產品流程

### Amazon SageMaker

`SageMaker` 比較偏完整的 ML 平台。

可以先把它理解成：

- 協助準備資料、訓練模型、調參與部署
- 適合需要自己建立 ML workflow 的團隊
- 比單點 AI API 更接近真正的 ML 平台工作流

## 一張簡化地圖

如果把常見 AWS 服務用一句話記住，可以先這樣抓：

| 類別 | 代表服務 | 先記住的用途 |
| --- | --- | --- |
| compute | EC2, Lambda | 跑程式與應用 |
| relational database | RDS, Aurora | 結構化交易資料 |
| NoSQL | DynamoDB | 高擴展、低延遲 key-value / document |
| analytics database | Redshift | 資料倉儲與分析 |
| object storage | S3 | 檔案、資料湖、備份 |
| block storage | EBS | 給運算實例的磁碟 |
| file storage | EFS | 共享檔案系統 |
| networking | VPC, CloudFront | 網路隔離與內容分發 |
| AI / ML | Translate, Comprehend, SageMaker | 預訓練 AI 與 ML 平台 |

## 常見誤區

- 把所有資料都往同一種資料庫放
- 把 `S3`、`EBS`、`EFS` 當成可以互換的儲存方案
- 一看到 AI 需求就想自己訓練模型，而不是先看 managed AI 服務
- 把 VPC 當成單純「網路開關」，沒有理解它是整個隔離與流量治理邊界

## Related Concepts

- [AWS Certified Cloud Practitioner](aws-certified-cloud-practitioner.md)
- [Cloud Computing Fundamentals](cloud-computing-fundamentals.md)
- [AWS Streaming with Kinesis and Lambda](../../data-science/data-engineering/aws-streaming-with-kinesis-and-lambda.md)
- [MLOps Overview](../../data-science/machine-learning/production/mlops-overview.md)

[Back to Cloud](README.md)
