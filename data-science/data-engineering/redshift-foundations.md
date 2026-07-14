# Redshift Foundations

Amazon Redshift 是 AWS 上的 distributed, columnar data warehouse，主要用來支援大規模 SQL analytics。它和一般 row-based transactional database 最大的差別，不只是資料量，而是整個查詢與資料分布的設計思維都不同。

## What Redshift Is

- distributed database
- columnar database
- SQL-first analytics warehouse
- 使用 PostgreSQL 9 syntax 的一部分，並加上自己的擴充
- 同時支援 serverless 與 provisioned clusters

從資料工程角度看，Redshift 的重點不是「像 PostgreSQL 一樣用」，而是理解它如何把資料分散到多個 compute nodes，並讓分析查詢在這些節點上平行執行。

## Why Redshift Feels Different

### Columnar Storage

- 以 column 為單位讀取資料
- 特別適合 analytical queries
- 這也是為什麼 `SELECT *` 特別不划算

### Distributed Execution

- 資料與查詢運算分散在多個 compute nodes
- table design 會直接影響 join、aggregation 與 scan 效率

### AWS-Centric Warehouse Position

Redshift 在 AWS 裡常被當成 primary SQL warehouse，並能和其他服務一起工作，例如：

- RDS for PostgreSQL
- Aurora PostgreSQL-compatible edition
- EMR / Hive
- Kinesis

它也支援 external schemas，因此不只查自己內部資料表，還能把外部資料源接進同一個 SQL workflow。

## Row-Based vs. Columnar Thinking

如果用 row-based OLTP database 的方式思考 Redshift，通常會踩到效能坑。

在 Redshift 裡：

- 查詢常只需要部分欄位時，columnar storage 很有優勢
- table distribution 與 sort order 會影響跨節點資料移動
- query tuning 不只是改 SQL，還包含 table design

## Serverless vs. Provisioned

Redshift 可以是：

- `serverless`
- `provisioned cluster`

這代表團隊可以依 workload、成本模型與管理偏好選擇不同部署方式。但無論是哪種模式，底層仍然是 analytics-first 的 distributed warehouse 心智。

## Distribution and Data Placement

Redshift table 的核心設計問題之一，是資料要怎麼分散到節點上。

### DISTKEY

- `DISTKEY` 用來決定資料依哪個欄位分布
- 對常見 join / aggregation path 很重要

### Distribution Styles

課程整理了四種常見 distribution style：

- `ALL`: 整張表複製到每個 node，適合小型 lookup table
- `KEY`: 依 `DISTKEY` 欄位分布，適合常以同鍵 join 或 aggregate 的表
- `EVEN`: 輪流分布 rows 到各節點，適合沒有明確分布鍵的大表
- `AUTO`: 讓 Redshift 依表大小與條件自動選擇策略

一個實務心智是：

- 小表常適合 `ALL`
- 常 join 的大表要優先思考 `KEY`
- 沒明確 join key 的大表才比較像 `EVEN`

## SORTKEY

`SORTKEY` 影響資料在節點內的排序方式，對 scan 與篩選很重要。

重點包括：

- `WHERE`
- `JOIN`
- `GROUP BY`
- `ORDER BY`

如果查詢模式常會依某些欄位篩選或排序，讓它們進入 `SORTKEY` 通常會更有效率。

課程也特別提醒：

- `ORDER BY` 最好依 `SORTKEY` 定義順序使用
- 多欄排序時，compound sort key 的欄位順序本身就有意義

## Query Optimization Patterns

### Avoid `SELECT *`

因為 Redshift 是 columnar：

- 不要取不需要的欄位
- 只選必要 columns，通常就能少做很多 I/O

### Build Better Predicates

課程的重點不是某一條 SQL，而是 predicate placement：

- 對 joined table 的條件，盡量貼近 join
- 善用 `DISTKEY` / `SORTKEY` 對應欄位
- 避免在關鍵 predicate 上套函式

這麼做的目的，是讓 Redshift 更容易把過濾條件推到適合的節點與資料範圍。

## Table Design Matters

在 Redshift 裡，table definition 不只是 schema。

除了欄位型別，還要一起想：

- distribution style
- `DISTKEY`
- `SORTKEY`
- 查詢主要走向
- 是否有 external schema / external table

這也是為什麼 Redshift 的效能優化很多時候從 DDL 就已經開始，而不是等查詢變慢才補救。

## External Schemas and Spectrum-Like Access

Redshift 支援 internal 與 external schema 的混合視角。

課程中常用到的幾個 system views 包括：

- `SVV_REDSHIFT_SCHEMAS`
- `SVV_ALL_SCHEMAS`
- `SVV_REDSHIFT_TABLES`
- `SVV_ALL_TABLES`
- `SVV_ALL_COLUMNS`

它們的價值在於：

- 區分 internal / external objects
- 讓你能用 SQL 盤點 schemas、tables、columns
- 幫助理解 external data 是否已正確掛進 warehouse

## Monitoring and Diagnostics

Redshift 的調校不只看 query text，也會看系統層資訊。

幾個實用系統檢視包括：

- `SVV_TABLE_INFO`: 看 table details、`DISTKEY`、`SORTKEY`、skew
- `STL_ALERT_EVENT_LOG`: 看觸發 alert 的 query 與可能的效能問題

這類 system views 很重要，因為它們讓調校從「憑感覺改 SQL」變成「根據資料分布與 alert 觀察來決策」。

## Practical Use Cases

Redshift 常見於：

- AWS 內部分析型 warehouse
- 需要和其他 AWS data services 一起運作的 SQL analytics stack
- 外部與內部 schema 混合查詢
- 以 table design 為核心的高效能報表與聚合 workload

## Practical Reminders

- 不要把 Redshift 當成一般 PostgreSQL 來用；語法相近，不代表效能心智相同。
- 在 Redshift 裡，table design 和 query design 幾乎同等重要。
- `DISTKEY` 是資料如何跨節點分布的問題；`SORTKEY` 是資料如何在節點內被掃描的問題。
- `SELECT *` 在 columnar warehouse 裡特別昂貴。
- Redshift 查詢慢時，不一定先怪 SQL；也要看 distribution style、sort order、data skew 與 alert logs。
