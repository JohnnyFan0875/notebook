# Streaming

串流處理讓資料在到達時就被處理。本篇前半是事件串流的通用心智模型與 Kafka（topic、partition、producer / consumer、replication），後半是 AWS 上的 serverless 版本（Kinesis Data Streams、Firehose、Lambda）。batch vs stream 的取捨見 [Processing and Pipelines](processing-and-pipelines.md#batch-vs-stream)。

## Why Event Streaming Matters

不是所有資料都適合等到每天晚上再批次處理。

當資料本身代表持續發生的事件時，例如：

- 訂單建立
- 配送狀態更新
- 感測器訊號
- 使用者行為紀錄
- 資安告警

團隊常需要的是「資料一出現就能被接住、保存、分發」，而不是等下一次 batch job 再一起處理。

這就是 event streaming 的價值：

- 從來源持續取得事件
- 可靠地保存事件
- 把事件分發給不同下游

但要先分清楚三件事：

- batch processing: 把資料分組後一次處理完
- event-based processing: 某個事件發生時就觸發任務
- streaming: 持續處理沒有明確終點的事件流

這三者會重疊，但不是同義詞。

## From Batch to Event-Driven to Streaming

很多資料系統不是直接從 batch 跳到完整 streaming，而是經過一段 event-driven 過渡。

可以用很粗略的方式理解：

- batch 世界：固定時間或固定大小後才跑一次 job
- event-driven 世界：事件發生就觸發任務，但任務本身仍可能是一次性的
- streaming 世界：事件源持續存在，下游也持續消費與處理

這個區分很實用，因為有些需求其實只需要 event trigger，不需要維持一整套長時間運作的 streaming stack。

## What "Real-Time" Usually Means

real-time 在資料工程裡很少代表絕對瞬時，而比較像一種 response-time guarantee。

不同情境下，可接受的 real-time 可能是：

- 1 day
- 1 hour
- 1 minute
- 幾秒內

所以真正該問的不是「要不要 real-time」，而是：

- 可接受的延遲是多少
- 這個延遲是否要被當成 SLA 或系統保證
- 為了更低延遲願意付出多少成本與複雜度

延遲、容量與成本之間通常存在 trade-off，不是所有事件都值得走最快路徑。

## Kafka in One Sentence

Apache Kafka 是一個 open-source、distributed、scalable 的 event streaming 平台，設計來處理大量資料並把事件穩定交給多個消費端。

如果把它講得更白話一點：

- producer 把事件寫進 Kafka
- Kafka 把事件存好、排好、分散好
- consumer 再把事件讀出去做處理

## Core Components

### Topics

topic 可以把它想成事件類型的邏輯分類，例如：

- `orders`
- `payments`
- `delivery_status`
- `security_alerts`

producer 通常把訊息寫進某個 topic，consumer 再從該 topic 讀取。

### Producers

producer 是寫入端。

- 負責把 messages 或 events 寫進 Kafka topics
- 一個 producer 可以寫入一個或多個 topics
- 同一個 topic 也可以有多個 producers

producer 的重點不是「把資料存到某台機器」，而是把事件送進 Kafka 這個可持續消費的事件層。

### Consumers

consumer 是讀取端，也常被想成 subscriber。

- 從 Kafka topics 讀取訊息
- 一個 consumer 可以讀一個或多個 topics
- 同一個 topic 也可以被多個 consumers 使用

這種設計讓同一份事件資料可以同時服務多個下游，例如：

- 一個 consumer 寫入分析資料表
- 一個 consumer 做即時告警
- 一個 consumer 更新產品狀態

### Brokers and Clusters

Kafka server 常被稱為 broker。

- broker 負責儲存資料
- 管理 producers 與 consumers 的通訊
- 通常以 cluster 形式運作，而不是只靠單機

實務上，Kafka 的價值很大一部分來自 cluster 架構，因為它讓事件串流系統更能承受高流量與節點故障。

## Topics, Partitions, and Ordering

Kafka 不只是把資料塞進一個大桶子，而是透過 topic 與 partition 來組織事件。

### Partitions

一個 topic 可以被切成多個 partitions。

這麼做的原因通常是：

- 提高平行處理能力
- 分散儲存壓力
- 讓大量事件可以更容易擴充

### Ordering

Kafka 很重要的一個特性是：

- 同一個 partition 內的訊息會維持寫入順序
- 但如果 topic 有多個 partitions，就不要把「全域完全排序」當成預設前提

這是很多串流系統設計的關鍵提醒。你能依賴的通常是 partition-level ordering，而不是 topic-level total ordering。

## Replication and Fault Tolerance

Kafka 之所以常被拿來做關鍵資料流，很大原因是它支援 replication。

- partition 可以被複製到多個 brokers
- 如果某個 broker 故障，其他 broker 仍可能提供資料
- replication factor 越高，通常能承受的故障越多，但成本也更高

可以用一個簡化的方式理解：

- replication factor = 2，代表同一份資料通常有兩份副本
- 在這種情況下，系統通常能承受一個相關節點失效

但也要注意：

- replication factor 不能超過 broker 數量
- 故障容忍不是免費的，會換來更多儲存與協調成本

## Common Kafka Workflow

一條 Kafka-based pipeline 常見會長這樣：

1. source systems 持續產生 events
2. producers 把 events 寫進 topics
3. Kafka cluster 保存並分發 events
4. consumers 讀取事件後做下游處理

下游可能是：

- 即時監控
- operational service
- 分析資料表
- feature pipeline
- 告警系統

## Queues and FIFO Thinking

在進入 Kafka 之前，先有一個很重要的概念是 queue。

queue 的常見直覺模型是：

- 事件先進先出，也就是 FIFO
- producer / sender 把工作送進 queue
- worker / consumer 再依序處理

這種模式的價值包括：

- 解耦上游與下游
- 平滑突發流量
- 讓非同步工作不必阻塞前台請求

很多 streaming 或 event-driven system 的設計思路，都能從 queue mindset 開始理解。

## Tool Choice: Celery vs. Kafka vs. Spark Streaming

實務上沒有單一「最佳串流工具」，而是看你要解的問題是什麼。

### Celery

Celery 比較像 distributed task queue。

它常見於：

- password reset emails
- 數位訂單履行
- 圖片縮放
- 其他 asynchronous background jobs

如果需求重點是「把工作丟給背景 worker 處理」，Celery 這類 task queue 常比完整 event streaming platform 更直接。

### Kafka

Kafka 比較偏 event log / event distribution layer。

它的強項在於：

- 保存事件
- 讓多個 consumers 共用同一事件流
- 提供可擴充的分發與重播能力

如果你需要的是 shared event backbone，Kafka 會比單純 task queue 更合適。

### Spark Streaming

Spark Streaming 比較偏 processing engine。

它的重點是：

- 處理 streaming data
- 把既有 Spark 資料轉換能力延伸到 stream 場景
- 讓 batch 與 stream workflow 較容易共用處理邏輯

但它不是專門拿來保存或長期記錄事件的系統，因此常和 Kafka 這類事件層搭配，而不是互相完全取代。

## Choosing by Requirement

工具選型時，至少要先問：

- 我需要保存事件，還是只需要非同步處理工作
- 我需要多個 consumers 共用同一資料流嗎
- 我最在意的是 latency、throughput，還是成本
- 這個 use case 是一般事件、sensor data，還是 location / clickstream / security alerts
- 系統是否有不同 SLA，要不要按服務等級分流

如果需求只是背景任務，Kafka 可能太重。
如果需求是多下游共享事件、可重播、可擴充，task queue 可能又太窄。

## When Kafka Fits Well

Kafka 常見於這些場景：

- order tracking
- ride-share 或 food delivery 狀態流
- sensor / IoT data
- cybersecurity events
- 需要多個下游共享同一事件來源的系統

如果需求只是每天匯總一次檔案，Kafka 往往太重。

如果需求是：

- 低延遲
- 可重播事件
- 多個 consumer 共用同一事件流
- 需要較強的可擴充性與容錯

那 Kafka 就比較合理。

## Operational Basics

在操作 Kafka 時，topic management 是最基本的一層。

常見動作包括：

- create topic
- describe topic
- list topics
- delete topic

其中有幾個實務上特別重要的設定：

- `--partitions`: 決定 partition 數量
- `--replication-factor`: 決定副本數量

這兩個設定直接影響：

- throughput
- parallelism
- fault tolerance

## Troubleshooting Mindset

Kafka 是 networked service，所以很多問題其實不是「Kafka 壞掉」，而是：

- service 沒有啟動
- `--bootstrap-server` 指錯
- port / IP 不正確
- firewall 擋住
- topic 名稱打錯

特別值得記住的是：某些環境下，topic 可能在寫入時被自動建立。這雖然方便，但也可能讓 typo 直接變成新 topic，例如把 `orders` 打成 `ordrs`。

因此實務上要特別留意：

- topic naming 是否有治理規範
- 是否允許 auto topic creation
- 指令回傳內容是否符合預期

consumer 端也常有兩個容易忘記的點：

- `--from-beginning`: 需要讀舊資料時再加
- `--max-messages`: 只想驗證少量資料時很有用

## Practical Reminders

- Kafka 解決的是事件流的保存與分發，不是所有資料問題都該用 Kafka。
- partition 提供的是可擴充性與局部排序，不是全域排序保證。
- replication 提高容錯，但也會增加基礎設施與管理成本。
- 同一事件流能被多個 consumers 重複利用，是 Kafka 很大的系統設計優勢。
- 在串流架構裡，topic 命名、consumer 邊界與錯誤處理策略，往往比 CLI 指令本身更重要。
- 問題定義要先於工具選型，因為 Celery、Kafka 與 Spark Streaming 解的是相鄰但不同的問題。

## AWS Streaming with Kinesis and Lambda

### Why This Pattern Exists

當團隊已經決定要做 event-driven 或 streaming workflow，下一個問題通常不是「要不要串流」，而是要怎麼把：

- incoming events
- transformation logic
- storage
- monitoring
- alerting

串成一條可維運的 cloud-native pipeline。

在 AWS 生態裡，一個很常見的組合就是：

- Kinesis Data Streams 或 Firehose 接住資料
- Lambda 做即時轉換或路由
- S3、Redshift、Elasticsearch/OpenSearch 等系統做落地或查詢

### Core Services in This Stack

#### Kinesis Data Streams

Kinesis Data Streams 比較像持續接收事件的入口層。

它適合：

- 接住高頻事件
- 讓多筆 records 持續進入 stream
- 作為後續 consumer 或 Lambda trigger 的上游

如果把它和 Kafka 類比，可以把它理解成 AWS 內建的 managed event stream 服務之一。

#### Kinesis Firehose

Firehose 比較偏 delivery service。

它的常見角色是：

- 接收 streaming records
- 視設定做 buffering
- 幫你把資料送到下游目的地

常見目的地包括：

- S3
- Redshift
- Elasticsearch / OpenSearch

如果需求重點是「穩定把串流資料送去目的地」，Firehose 往往比自己手刻 delivery logic 更省事。

#### AWS Lambda

Lambda 常用來承接兩類工作：

- response to stream events
- 輕量轉換、過濾、 enrichment、後續 trigger

它的價值不只是不用自己管伺服器，而是讓小型處理邏輯可以被事件直接喚起。

### Serverless Trade-Offs

serverless 的吸引力通常來自：

- 少管基礎設施
- 容易用事件觸發
- 適合 bursty 或不穩定流量

但也要注意：

- execution model 受平台限制
- debugging 與本機重現不一定直覺
- 服務之間的權限、trigger 與失敗重試需要更明確設計

換句話說，serverless 減少的是部分維運成本，不是系統設計成本。

### A Common Data Flow

一條常見的 AWS streaming pipeline 可以整理成：

1. source 持續送出 records
2. Kinesis stream 或 Firehose 接住資料
3. Lambda 依事件觸發，做過濾或轉換
4. 轉換後資料送往 S3、warehouse、search system 或 API
5. 監控與 alerting 依指標或條件再往下通知

這種設計的好處是：ingestion、transform、storage、alerting 可以拆成多個鬆耦合元件，而不是全塞進同一個長腳本。

### Transformation Pattern in Lambda

串流中的 Lambda 很常做幾件事：

- 逐筆讀取 `event['records']`
- decode payload，例如 base64
- parse JSON
- 補上新欄位或 enrichment
- 回傳轉換後 records

例如：

- 從 tweet text 做 sentiment enrichment
- 從 sensor event 萃取特定欄位
- 依條件過濾不符合規則的紀錄

這類函式的關鍵不是程式碼長短，而是要確保輸入輸出格式穩定、可重跑、可觀察。

### Storage and Destination Choices

streaming data 的下游目的地應該依使用情境決定。

#### S3

適合：

- raw landing
- 歷史保存
- 後續批次分析

這通常是最穩健的第一層落地選擇。

#### Redshift

適合：

- structured analytics
- SQL-heavy reporting
- 定期查詢與商業分析

如果重點是 warehouse-style analysis，Redshift 比 search engine 更對路。

#### Elasticsearch / OpenSearch

適合：

- 搜尋
- 即時探索
- dashboard-driven operational monitoring

如果需求偏查詢、搜尋與快速互動式觀察，這類系統會比 warehouse 更自然。

### Event Chaining and Lambda-to-Lambda Invocation

有些 workflow 不只是一個 Lambda 處理完就結束，而是：

- 一個 Lambda 先整理資料
- 再非同步 invoke 另一個 Lambda
- 讓後續 aggregation、reporting 或 alerting 分段完成

這種設計能降低單一函式責任過重，但也會增加：

- observability 需求
- retry 與 idempotency 設計成本
- 事件鏈追蹤難度

所以 Lambda chaining 很方便，但最好只在分工真的清楚時採用。

### Monitoring and Alerting

串流系統的價值很常來自「即時知道有沒有異常」。

常見需求包括：

- 監控事件量是否異常
- 監控負面訊號是否超過門檻
- 在固定時間窗內觸發 alert

像課程裡的情境就是：

- 只處理特定 hashtag 的推文
- 在 5 分鐘內負面推文超過門檻時通知管理者

這說明了 streaming pipeline 不只是搬資料，而是能把業務條件直接接到 alerting workflow。

### Practical Design Questions

在實作 AWS streaming pipeline 前，先回答這些問題通常很有幫助：

- record format 是什麼
- 哪一層負責 raw storage
- 哪一層負責 transformation
- alert 條件是逐筆判斷，還是時間窗聚合
- downstream 是 warehouse、search，還是 API response
- 哪些元件需要同步回應，哪些可以非同步

### Practical Reminders

- Kinesis、Firehose、Lambda 雖然常一起出現，但三者分工不同，不要把它們視為同一件事。
- Firehose 偏 delivery，Lambda 偏 transformation，S3 常是最穩定的原始落地層。
- serverless 架構減少了主機維運，但沒有消除 schema、權限、重試與監控問題。
- streaming pipeline 的成功標準，不只是資料有流動，還包括 alerting、monitoring 與 downstream consumer 真的能接住結果。
