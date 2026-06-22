# AWS Streaming with Kinesis and Lambda

## Why This Pattern Exists

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

## Core Services in This Stack

### Kinesis Data Streams

Kinesis Data Streams 比較像持續接收事件的入口層。

它適合：

- 接住高頻事件
- 讓多筆 records 持續進入 stream
- 作為後續 consumer 或 Lambda trigger 的上游

如果把它和 Kafka 類比，可以把它理解成 AWS 內建的 managed event stream 服務之一。

### Kinesis Firehose

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

### AWS Lambda

Lambda 常用來承接兩類工作：

- response to stream events
- 輕量轉換、過濾、 enrichment、後續 trigger

它的價值不只是不用自己管伺服器，而是讓小型處理邏輯可以被事件直接喚起。

## Serverless Trade-Offs

serverless 的吸引力通常來自：

- 少管基礎設施
- 容易用事件觸發
- 適合 bursty 或不穩定流量

但也要注意：

- execution model 受平台限制
- debugging 與本機重現不一定直覺
- 服務之間的權限、trigger 與失敗重試需要更明確設計

換句話說，serverless 減少的是部分維運成本，不是系統設計成本。

## A Common Data Flow

一條常見的 AWS streaming pipeline 可以整理成：

1. source 持續送出 records
2. Kinesis stream 或 Firehose 接住資料
3. Lambda 依事件觸發，做過濾或轉換
4. 轉換後資料送往 S3、warehouse、search system 或 API
5. 監控與 alerting 依指標或條件再往下通知

這種設計的好處是：ingestion、transform、storage、alerting 可以拆成多個鬆耦合元件，而不是全塞進同一個長腳本。

## Transformation Pattern in Lambda

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

## Storage and Destination Choices

streaming data 的下游目的地應該依使用情境決定。

### S3

適合：

- raw landing
- 歷史保存
- 後續批次分析

這通常是最穩健的第一層落地選擇。

### Redshift

適合：

- structured analytics
- SQL-heavy reporting
- 定期查詢與商業分析

如果重點是 warehouse-style analysis，Redshift 比 search engine 更對路。

### Elasticsearch / OpenSearch

適合：

- 搜尋
- 即時探索
- dashboard-driven operational monitoring

如果需求偏查詢、搜尋與快速互動式觀察，這類系統會比 warehouse 更自然。

## Event Chaining and Lambda-to-Lambda Invocation

有些 workflow 不只是一個 Lambda 處理完就結束，而是：

- 一個 Lambda 先整理資料
- 再非同步 invoke 另一個 Lambda
- 讓後續 aggregation、reporting 或 alerting 分段完成

這種設計能降低單一函式責任過重，但也會增加：

- observability 需求
- retry 與 idempotency 設計成本
- 事件鏈追蹤難度

所以 Lambda chaining 很方便，但最好只在分工真的清楚時採用。

## Monitoring and Alerting

串流系統的價值很常來自「即時知道有沒有異常」。

常見需求包括：

- 監控事件量是否異常
- 監控負面訊號是否超過門檻
- 在固定時間窗內觸發 alert

像課程裡的情境就是：

- 只處理特定 hashtag 的推文
- 在 5 分鐘內負面推文超過門檻時通知管理者

這說明了 streaming pipeline 不只是搬資料，而是能把業務條件直接接到 alerting workflow。

## Practical Design Questions

在實作 AWS streaming pipeline 前，先回答這些問題通常很有幫助：

- record format 是什麼
- 哪一層負責 raw storage
- 哪一層負責 transformation
- alert 條件是逐筆判斷，還是時間窗聚合
- downstream 是 warehouse、search，還是 API response
- 哪些元件需要同步回應，哪些可以非同步

## Practical Reminders

- Kinesis、Firehose、Lambda 雖然常一起出現，但三者分工不同，不要把它們視為同一件事。
- Firehose 偏 delivery，Lambda 偏 transformation，S3 常是最穩定的原始落地層。
- serverless 架構減少了主機維運，但沒有消除 schema、權限、重試與監控問題。
- streaming pipeline 的成功標準，不只是資料有流動，還包括 alerting、monitoring 與 downstream consumer 真的能接住結果。

[Back to Data Engineering](README.md)
