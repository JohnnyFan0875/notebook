# GCP Fundamentals

這份筆記的重點不是背 GCP 全部產品，而是建立一個穩定的入門視角：GCP 在雲端供應商中有什麼特色、常見 workload 會落在哪些服務類別，以及為什麼大家常把它和資料、分析、AI 一起談。

## GCP 是什麼

`GCP` 是 Google Cloud Platform，也就是 Google 提供的雲端平台。

如果 [Cloud Computing Fundamentals](cloud-computing-fundamentals.md) 講的是雲端的一般原理，這一頁就是把那些概念放到 GCP 這個供應商上理解。

入門時可以先記住 GCP 常見的幾個印象：

- 雲端平台供應商之一，和 AWS、Azure 同屬主流選項
- 很強調全球網路基礎設施
- 在資料、分析與 AI 工作流裡特別常被提到

## 先用三個問題理解 GCP

學 GCP 時，先不要被產品名稱帶著跑，可以先問：

1. 這個 workload 是要跑應用，還是處理資料
2. 需要的是 VM、容器、還是 serverless
3. 這份資料是拿來交易、分析，還是訓練模型

這三個問題通常已經足夠把大部分 GCP 服務放回正確脈絡。

## GCP 的幾個核心印象

原始教材裡反覆出現的訊息，大致可以整理成下面幾點。

### 全球基礎設施與網路

GCP 很常強調自己的全球高吞吐網路。

這個特性通常和幾件事有關：

- 跨區域服務能力
- 大規模應用的網路傳輸
- 全球使用者存取體驗

實務上不需要先背所有 region 或 zone 名稱，但要理解 GCP 會把網路能力當成平台特色的一部分。

### Compute 選項很多，但邏輯很穩定

教材把 compute 服務分成幾個穩定方向：

- virtual machines
- container orchestration
- serverless compute

這個分類本身就很值得記。

#### Virtual Machines

如果你需要較高控制權、想自己管 OS 或 runtime，通常會想到 VM 類服務。

#### Containers

如果 workload 已經容器化，或團隊想把部署標準化，容器與 orchestration 會是常見路線。

#### Serverless

如果你想讓平台接手更多維運細節，serverless compute 會是更自然的方向。

所以 GCP compute 入門的重點，不是先背產品，而是先把 workload 放進：

- 高控制權
- 容器化
- 事件驅動或高託管

這三種思路裡。

## Data on GCP

GCP 很常被拿來談資料平台，這也是它最鮮明的特色之一。

### Data-driven culture

教材前段不是先講產品，而是先講資料驅動文化。這個順序很合理，因為資料平台的價值從來不只是儲存資料，而是讓決策從直覺轉向 evidence-based。

cloud 在這裡扮演的角色通常是：

- 提供大規模儲存
- 支援即時或近即時處理
- 讓分析與應用可以更快連起來

### 先分資料型態，再選服務

GCP 的資料服務很多，但入門時先分資料型態比較有效：

- 非結構化或檔案型資料
- 關聯式交易資料
- 大規模分析資料

這樣比較不容易把所有資料都塞進同一個系統。

### Cloud Storage

`Cloud Storage` 可以先理解成 GCP 的 object storage 核心入口。

適合：

- 檔案
- 多媒體資料
- 備份
- data lake 類資產

如果你熟悉 AWS，可以把它先類比成接近 `S3` 的心智模型。

### Cloud SQL 與 Cloud Spanner

教材點到兩種很不同的資料庫思路：

- `Cloud SQL`：比較偏傳統關聯式資料庫託管
- `Cloud Spanner`：偏向大規模、分散式、仍希望保有關聯式特性的資料庫

這兩者放在一起看時，重點不是產品名稱，而是你是否需要：

- 傳統 relational workload
- 更大規模的水平擴展與高可用設計

### BigQuery

教材在分析需求那段提到 data warehouse 的概念，這正是 `BigQuery` 很常出現的脈絡。

可以先把 `BigQuery` 理解成：

- 分析型資料倉儲
- 用來跑大規模查詢
- 和 BI、報表、分析 workflow 密切相關

心智模型上，它不是拿來取代交易型資料庫，而是處理 analytics workload。

### Looker

`Looker` 則比較靠近資料分析與商業視覺化的消費層。

它回答的不是「資料存在哪」，而是「分析結果怎麼被人使用」。

## GCP 為什麼常和 AI 放在一起

教材後段把 Data and AI 放在一起談，這很符合 GCP 的常見定位。

### Vertex AI

`Vertex AI` 可以先理解成 GCP 上整合多種 AI 任務的平台入口。

心智模型上，它比較接近：

- 模型開發與訓練流程的平台化
- 推論與部署能力的整合
- 把資料與模型工作流接起來

所以 GCP 的一個鮮明特徵是，資料服務和 AI 平台之間的敘事通常很連續。

## 一個最小 GCP 心智模型

如果只想先抓最重要的東西，可以記這五點：

1. GCP 是主流雲端供應商之一，特別強調全球網路、資料與 AI
2. compute 先分 VM、container、serverless 三種路線
3. `Cloud Storage`、`Cloud SQL`、`Cloud Spanner`、`BigQuery` 分別對應不同資料需求
4. 分析型 workload 和交易型 workload 不應該混為一談
5. `Vertex AI` 讓 GCP 的資料與 AI 脈絡更自然地接在一起

## 常見誤區

- 把 GCP 只看成另一個 VM 平台
- 沒有先分資料型態，就急著選資料服務
- 把 `BigQuery` 當成一般交易型資料庫
- 只背產品名稱，沒有先理解 compute 與 data 的抽象類別

## Related Concepts

- [Cloud Computing Fundamentals](cloud-computing-fundamentals.md)
- [AWS Services Overview](aws-services-overview.md)
- [Azure Fundamentals](azure-fundamentals.md)
- [Introduction to Spark SQL in Python](../../data-science/data-engineering/pyspark/introduction-to-spark-sql-in-python.md)

[Back to Cloud](README.md)
