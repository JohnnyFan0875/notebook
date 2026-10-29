[Data Science](../README.md) › [Data Engineering](README.md) › 串流處理

# 串流處理 (Streaming)

串流處理讓資料一到達就被接住、保存並分發給下游，而不是等下一次 batch。本篇前半是事件串流的觀念與 Kafka，後半是 AWS 上的 serverless 版本（Kinesis、Firehose、Lambda）。batch vs stream 的取捨見 [處理與 Pipeline](processing-and-pipelines.md#batch-vs-stream)。

## 先問延遲要求

real-time 在資料工程裡很少代表瞬間，而是一個回應時間的保證：可能是一天、一小時、一分鐘或幾秒。

| 問題 | 為什麼 |
| --- | --- |
| 可接受的延遲是多少？要當成 SLA 嗎？ | 決定架構等級 |
| 為了更低延遲願意付多少成本與複雜度？ | 延遲、容量、成本互相取捨 |
| 只需要事件觸發，還是要長時間運作的串流？ | 很多需求用 event-triggered batch 就夠 |

| 模式 | 意義 | 例子 |
| --- | --- | --- |
| Batch | 分組後一次處理 | 夜間彙總 |
| Event-based | 事件發生時觸發一次性任務 | 新檔案到達 → 啟動匯入 |
| Streaming | 持續處理沒有終點的事件流 | 訂單狀態、感測器、資安告警、clickstream |

## Queue：最基本的模型

queue 讓 producer 把工作送進佇列、worker 依序 (FIFO) 處理。好處是解耦上下游、平滑突發流量、讓非同步工作不阻塞前台請求。很多串流設計都可以從 queue 開始理解。

## Kafka

Apache Kafka 是開源、分散式的事件串流平台：producer 把事件寫進 Kafka，Kafka 依序保存並分散在多台機器上，consumer 讀出去處理。和一般 queue 的差別是事件被**保存一段時間**（retention），多個下游可以各自讀取，也可以重播。

| 元件 | 意義 |
| --- | --- |
| Topic | 事件類型的邏輯分類（`orders`、`delivery_status`、`security_alerts`） |
| Partition | topic 的切分；提高平行度與分散儲存 |
| Offset | 事件在 partition 中的位置編號；consumer 記錄自己讀到哪 |
| Producer | 寫入端；可寫多個 topic，一個 topic 可有多個 producer |
| Consumer | 讀取端；可讀多個 topic，一個 topic 可被多個 consumer 使用 |
| Consumer group | 同一 group 的 consumer 分工：每個 partition 同時只分給 group 中一個 consumer |
| Broker / cluster | Kafka 伺服器；以叢集運作，負責儲存與通訊（Kafka 4.0 起只用 KRaft，不再需要 ZooKeeper） |

```
producers → topic "orders"
              ├── partition 0: e0 e3 e6 ...  ──┐
              ├── partition 1: e1 e4 e7 ...  ──┼─→ consumer group A（寫入分析表）
              └── partition 2: e2 e5 e8 ...  ──┘─→ consumer group B（即時告警）
```

### 順序、平行度與容錯

| 性質 | 要記住的 |
| --- | --- |
| 順序 | 只保證**同一 partition 內**的順序；需要同一實體的事件有序時，用該實體 ID 當 message key（同 key 進同一 partition） |
| 平行度 | 一個 group 的有效 consumer 數上限 = partition 數 |
| Replication | partition 複製到多個 broker；replication factor = N 時最多可承受 N − 1 個 broker 故障，但 factor 不能超過 broker 數，且會增加儲存與協調成本 |

### 傳遞語意

| 語意 | 意義 | 實務 |
| --- | --- | --- |
| At-most-once | 可能遺失，不會重複 | 先 commit offset 再處理 |
| At-least-once | 不會遺失，可能重複 | 處理完才 commit；最常見，下游要冪等 |
| Exactly-once | 不遺失也不重複 | 需要 idempotent producer + 交易，或下游以唯一 ID 去重 |

> 預設把串流當作 at-least-once：下游寫入用唯一事件 ID 做 upsert，重複送達也不會算兩次。

### CLI 操作與排錯

```bash
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders \
  --partitions 6 --replication-factor 3
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders
kafka-topics.sh --bootstrap-server localhost:9092 --list

kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders \
  --from-beginning --max-messages 10          # 讀舊資料、只取少量驗證
```

| 症狀 | 常見原因 |
| --- | --- |
| 連不上 | 服務沒啟動、`--bootstrap-server` 位址或 port 錯、防火牆 |
| 讀不到資料 | consumer 從最新位置開始（沒加 `--from-beginning`）、topic 名稱打錯 |
| 多出奇怪的 topic | 開啟自動建立 topic 時，打錯字（`ordrs`）直接變成新 topic；正式環境應關閉並訂命名規範 |
| consumer lag 持續增加 | 處理速度跟不上；增加 partition 與 consumer，或加快處理 |

## 工具選擇

| 工具 | 定位 | 適合 |
| --- | --- | --- |
| Celery / RQ | 分散式任務佇列 | 背景工作：寄信、縮圖、非同步計算 |
| Kafka | 事件日誌與分發層 | 多個下游共享事件、需要重播、高吞吐 |
| Spark Structured Streaming / Flink | 串流處理引擎 | 對事件流做轉換、視窗聚合、join；常接在 Kafka 後面 |
| Kinesis / Pub/Sub / Event Hubs | 雲端受管的事件串流 | 不想自己維運 Kafka |

Spark 舊的 DStream API（Spark Streaming）已不再發展；新程式用 Structured Streaming，同一套 DataFrame 程式可用於 batch 與 stream：

```python
from pyspark.sql import functions as F

events = (spark.readStream.format("kafka")
          .option("kafka.bootstrap.servers", "broker:9092")
          .option("subscribe", "orders").load())

counts = (events.selectExpr("CAST(value AS STRING) AS json", "timestamp")
          .withWatermark("timestamp", "10 minutes")            # 允許的遲到時間
          .groupBy(F.window("timestamp", "5 minutes")).count())

(counts.writeStream.format("delta").outputMode("append")
       .option("checkpointLocation", "chk/orders_counts")     # 失敗重啟時從這裡接續
       .start("tables/orders_counts"))
```

| 需求 | 選擇 |
| --- | --- |
| 只是把工作丟給背景 worker | 任務佇列；Kafka 太重 |
| 多下游共享、可重播、可擴充的事件流 | Kafka 或雲端受管串流；任務佇列太窄 |
| 每天匯總一次檔案 | batch，不需要串流 |

## AWS：Kinesis + Firehose + Lambda

```
來源 → Kinesis Data Streams ──→ Lambda（過濾、轉換、enrichment）──→ S3 / Redshift / OpenSearch / API
          或 Amazon Data Firehose（緩衝後直接送達目的地，可掛 Lambda 轉換）
                                   └→ CloudWatch 指標 / 告警 → SNS 通知
```

| 服務 | 角色 | 類比 |
| --- | --- | --- |
| Kinesis Data Streams | 持續接收事件的入口，以 shard 擴充；可被多個 consumer 或 Lambda 讀取 | AWS 受管的 Kafka-like 串流 |
| Amazon Data Firehose（原 Kinesis Data Firehose） | 傳送服務：緩衝 (buffering) 後送到 S3、Redshift、OpenSearch 等 | 不用自己寫投遞邏輯 |
| AWS Lambda | 由事件喚起的小型函式：過濾、轉換、enrichment、觸發後續流程 | 不用管伺服器的 consumer |

### Lambda 轉換的兩種事件格式

```python
import base64, json

# 1. Kinesis Data Streams 觸發：event["Records"]，資料在 record["kinesis"]["data"]
def handle_stream(event, context):
    for record in event["Records"]:
        payload = json.loads(base64.b64decode(record["kinesis"]["data"]))
        process(payload)                         # 要能承受重送：以事件 ID 去重

# 2. Firehose 資料轉換：event["records"]，必須回傳相同 recordId 與處理結果
def handle_firehose(event, context):
    out = []
    for r in event["records"]:
        item = json.loads(base64.b64decode(r["data"]))
        if item.get("hashtag") != "#target":
            out.append({"recordId": r["recordId"], "result": "Dropped", "data": r["data"]})
            continue
        item["sentiment"] = score(item["text"])                   # enrichment
        data = base64.b64encode((json.dumps(item) + "\n").encode()).decode()
        out.append({"recordId": r["recordId"], "result": "Ok", "data": data})
    return {"records": out}
```

### 目的地

| 目的地 | 適合 |
| --- | --- |
| S3 | 原始資料落地、歷史保存、後續批次分析；通常是最穩健的第一層 |
| Redshift | 結構化分析、SQL 報表 |
| OpenSearch（原 Elasticsearch） | 搜尋、即時探索、營運監控 dashboard |

### Serverless 的取捨

| 好處 | 代價 |
| --- | --- |
| 少管基礎設施、事件直接觸發 | 執行時間與記憶體受平台限制 |
| 適合突發或不穩定的流量 | 本機重現與除錯不直覺 |
| 元件鬆耦合，可分開擴充 | 權限、trigger、失敗重試、冪等要明確設計 |

Lambda 串 Lambda（非同步 invoke 下一段做聚合或告警）可以分散責任，但會增加可觀察性、重試與事件鏈追蹤的成本，分工清楚時才用。serverless 減少的是主機維運，不是系統設計。

### 告警範例與設計問題

例如「只處理特定 hashtag 的貼文，5 分鐘內負面貼文超過門檻就通知管理者」：這是時間窗聚合，不是逐筆判斷，需要有地方保存窗口內的計數（Structured Streaming 的 window、或 DynamoDB / CloudWatch 指標）。

| 實作前要回答 | |
| --- | --- |
| 紀錄格式是什麼？ | schema 與版本演進 |
| 哪一層存原始資料？哪一層做轉換？ | 出錯時能從原始資料重跑 |
| 告警是逐筆判斷還是時間窗聚合？ | 是否需要狀態 |
| 下游是 warehouse、搜尋還是 API？ | 目的地選擇 |
| 哪些元件要同步回應，哪些可非同步？ | 延遲與重試策略 |
