# Streaming and Kafka

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

[Back to Data Engineering](README.md)
