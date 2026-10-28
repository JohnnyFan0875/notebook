# Cloud Data Warehouses

Snowflake、BigQuery、Redshift 都是 managed、columnar、storage 與 compute（程度不一）分離的分析型 warehouse。先看比較表抓差異，再依需要讀各平台細節。

## 比較表

| 面向 | Snowflake | BigQuery | Redshift |
| --- | --- | --- | --- |
| 雲端 | 多雲（AWS / Azure / GCP） | GCP | AWS |
| Compute 模型 | virtual warehouse（可各自 sizing、隔離 workload） | serverless（slot，依掃描量或保留容量計費） | provisioned cluster 或 Serverless |
| 物件層級 | account → database → schema → table | project → dataset → table | cluster → database → schema → table |
| 資料排列 / 掃描削減 | 自動 micro-partitions、clustering key | partition + cluster | `DISTKEY`（跨節點分布）+ `SORTKEY`（節點內排序） |
| 載入 | stage + `COPY INTO` | `bq load`、`LOAD DATA` | `COPY`（S3）、Spectrum external schema |
| 除錯入口 | Query Profile、Query / Copy History | execution details、bytes processed | system tables、alert logs |
| 常見陷阱 | warehouse sizing、role 設計 | region 建立後不能改、沒用 partition filter 很貴 | data skew、`SELECT *`、distribution style 選錯 |

共通原則：columnar storage 下只選需要的欄位；先用 partition / cluster / sort 讓查詢少掃資料；查詢慢時先看 compute 隔離與資料排列，而不是只改 SQL。

## Snowflake

Snowflake 是一個受管的 cloud data warehousing platform，常被用在歷史分析、報表與大規模 SQL analytics。它不是傳統自己架設的資料庫，而是把 storage、compute 與管理層分開處理的資料平台。

### What Snowflake Is

- cloud-native data warehouse
- SQL-first analytics platform
- 常被 Data Engineers、BI Engineers 與 analysts 使用
- 適合 large-scale historical analysis and reporting

從資料工程角度看，Snowflake 的重點不是「能不能跑 SQL」，而是它把 warehouse 變成一個可管理、可擴充、可分權的受管平台。

### Why Snowflake Is Popular

- 不需要自己 provisioning hardware 或 software
- 建立帳號後就能快速開始使用
- 以 self-managed service 的體驗提供資料平台能力

這種體驗讓團隊可以把心力放在 data modeling、permissions、performance 與 ingestion，而不是底層基礎設施維護。

### Ways to Connect

Snowflake 不只透過 web UI 使用，實務上常見的連線方式還包括：

- `ODBC` / `JDBC`: 給 BI tools、Java 生態或一般資料庫整合使用
- language connectors: 例如 Python、Spark 等
- `SnowSQL` / Snowflake CLI: 適合 command-line workflow、腳本化操作與排錯

這很重要，因為 Snowflake 往往不是孤立使用，而是被接進 ETL、BI、notebook 或 application pipeline。

### Core Architecture

Snowflake 的平台結構可以粗分成三層：

#### Cloud Services

- 協調 user activities
- 負責較偏控制面的平台行為

#### Query Processing

- 使用 MPP, massive parallel processing
- 將 compute work 分散到多個 nodes

#### Database Storage

- 以 columnar format 儲存資料
- 針對 analytical queries 最佳化

這個分層很重要，因為它說明了 Snowflake 不是單一 database server，而是一個把管理、運算、儲存拆開的 analytics system。

### Mental Model: Storage vs. Compute

和其他現代 warehouse 類似，Snowflake 的一個核心觀念是：

- 資料儲存不等於查詢計算
- 你可以針對不同工作負載配置不同 compute resource

這也是 virtual warehouse 重要的原因。

### Virtual Warehouses

`virtual warehouse` 是 Snowflake 中主要的 compute unit。

它的角色比較像：

- 查詢運算資源
- 資料載入時的執行資源
- 依 workload 分離的 compute boundary

#### Why Create a New Virtual Warehouse

常見原因包括：

- role-based warehouse access
- 將 engineers 與 analysts 的 workload 分開
- 慢查詢需要更多 compute
- 不同團隊需要不同成本與效能配置

這代表 Snowflake 的效能管理，很多時候不是只改 SQL，而是重新思考 warehouse size、workload isolation 與 access boundaries。

### Query Performance Mental Model

Snowflake 的查詢效能，很大一部分來自它怎麼把 analytical workload 映射到 storage 和 compute。

幾個值得記的概念是：

- `MPP`: massively parallel processing，讓多個 compute nodes 同時處理查詢工作
- `columnar storage`: 以欄為單位儲存，比較適合只讀部分欄位的大型分析查詢
- `micro-partitions`: Snowflake 自動管理的小型儲存分區，幫助資料裁剪與讀取效率
- `Query Profile`: 用來觀察查詢執行步驟與資源使用情況的診斷入口

如果把它們放在一起看，可以得到一個比較實用的理解方式：

- storage 不是以傳統 row-store 為主
- compute 不是單機執行，而是平行處理
- 效能問題不只跟 SQL 有關，也和 warehouse 選擇、資料分布與掃描範圍有關

#### Columnar Storage vs. Row-Based Thinking

row-based storage 比較適合頻繁逐筆交易；columnar storage 則更適合只讀部分欄位、再做聚合與過濾的分析型查詢。

這也是為什麼在 Snowflake 上：

- 避免無差別 `SELECT *`
- 先釐清查詢真正需要哪些欄位
- 減少不必要的大範圍掃描

通常都能帶來更自然的效能改善。

#### Micro-Partitions and Scan Reduction

micro-partitions 可以把資料拆成較小的儲存單位，讓系統有機會只讀查詢真正需要的部分。

從實務角度看，這提醒我們：

- 查詢條件如果能有效縮小掃描範圍，通常比事後硬調 warehouse 更健康
- 資料模型與欄位設計，也會間接影響查詢是否容易做出不必要的大掃描

#### Query Profile as a Debugging Tool

當查詢變慢時，`Query Profile` 很有價值，因為它不是只告訴你「慢」，而是幫你看：

- 查詢大致經過哪些步驟
- 哪些部分消耗較多資源
- 問題比較像是掃描量、計算量，還是 warehouse 配置

這讓效能調校不再只靠猜測。

### Roles and Access Control

Snowflake 很依賴 role-based access control。

課程裡提到的幾個重要角色：

- `ACCOUNTADMIN`: account-level tasks，例如 billing
- `SECURITYADMIN`: 管理 account 內的 security-related objects
- `USERADMIN`: 管理 users 與 roles 的存取
- `SYSADMIN`: 管理自己擁有的 objects
- `PUBLIC`: 只能使用授權給該角色的 objects

實務上這件事很重要，因為：

- 平台治理不只是 table permissions
- account、user、role、warehouse 彼此之間是一起設計的
- 敏感操作與監控資訊通常不會開給低權限角色

### Object Hierarchy and Data Types

使用 Snowflake 時，通常要同時理解兩種結構：

- object hierarchy: `database -> schema -> table / view`
- data types: 資料欄位實際怎麼被儲存與比較

入門常見型別包括：

- text/string: `VARCHAR`, `CHAR`, `TEXT`
- numeric: `INTEGER`
- boolean: `BOOLEAN`

雖然這些型別看起來很基本，但它們會直接影響 schema design、casting、join behavior 與 downstream analytics。

### Marketplace and External Data

Snowflake 不只是一個自己放資料的 warehouse，也支援從 Snowflake Marketplace 或雲端來源取得資料。

這代表它除了查詢既有 tables，也常被放進更大的資料供應鏈中：

- 從外部供應者取資料
- 從 cloud storage 載入資料
- 把共享資料接進自己的分析環境

### Loading Data from Cloud Storage

課程第二章的重點比較接近一個高層流程：

1. 從 cloud provider 準備資料
2. 設定 stage permissions
3. 讓 Snowflake 可以存取外部檔案位置
4. 將資料載入資料表
5. 用 monitoring / copy history 驗證載入結果

這裡最值得記的不是畫面操作，而是：

- external stage 是 Snowflake 接外部檔案來源的重要概念
- 權限設定是 ingestion 成敗的核心部分
- 載入流程和權限、角色、warehouse 都有關

### Monitoring and History

Snowflake 也很重視查詢與載入的歷史追蹤。

#### Query History

- 可以找回過去執行過的 SQL
- 課程提到預設可查看過去 14 天的查詢歷史
- 有助於找慢查詢、debug 失敗與重現問題

#### Copy History

`Copy History` 對資料載入特別有用，可以觀察：

- 外部來源進來的資料量
- load success vs. failure
- 哪些表被 copy 了多少資料

課程提到兩個觀察入口：

- `Monitoring > Copy History`
- `Table > Copy History`

其中：

- Monitoring 視角可能有延遲
- Table 視角更即時

而且這些資訊通常只對較高權限角色開放。

### Practical Snowflake Use Cases

Snowflake 常見於這些情境：

- 建企業分析型 warehouse
- 提供 BI / reporting 的 SQL backend
- 承接 external data sharing 或 marketplace data
- 把不同團隊的分析 workload 分開治理

### Practical Reminders

- 不要把 Snowflake 想成只有「一個 database」；它更像完整資料平台。
- virtual warehouse 是 compute boundary，不是資料本身。
- 角色設計會直接影響誰能查資料、誰能管理 warehouse、誰能看監控資訊。
- 載入外部資料時，stage permissions 往往和 SQL 本身一樣重要。
- 如果查詢慢，不一定先改 SQL；有時應該先問是不是 workload isolation 或 warehouse sizing 問題。

## BigQuery

BigQuery 是 Google Cloud 上的 enterprise data warehouse，核心定位是用 SQL 對大量資料做分析，而不是自己管理傳統 database server。

### What BigQuery Is

- SQL-first analytics platform
- 適合 OLAP workload
- 可擴充到 massive datasets
- serverless
- compute 與 storage 分離

這個組合很重要，因為它代表使用者通常更關心資料模型、查詢模式與成本，而不是自己管理機器、叢集與容量規劃。

### Why BigQuery Feels Different

#### Serverless

- 沒有傳統意義上的固定資料庫主機可供管理
- 不需要自己挑一台「多大」的 warehouse server 才能開始查詢

#### Separate Compute and Storage

- 資料存放與查詢運算不是綁死在同一個節點
- 這讓 BigQuery 更像受管分析系統，而不是傳統單機 database

#### OLAP-Oriented

- 重點是大型分析查詢
- 不適合用 transactional database 的心智模型直接理解

### Resource Hierarchy

BigQuery 常見資源層級可以這樣看：

- `project`: 權限、使用者與控制邊界
- `dataset`: project 內的邏輯容器，像資料表資料夾
- `table`: 真正存放資料的地方

完整表名通常長這樣：

```sql
SELECT *
FROM `project.dataset.table`
```

實務上要先有這個命名心智，因為很多查詢、權限設定與跨專案存取都會直接依賴這個結構。

### Querying

#### Query Surface

BigQuery 查詢常見入口包括：

- BigQuery Studio
- `bq` command-line tool
- 其他會送 SQL 到 BigQuery 的程式或服務

#### SQL Dialect

BigQuery 的主要 SQL 方言是 GoogleSQL。

如果只是一般 SQL 基礎，像 `SELECT`、`JOIN`、`GROUP BY`、CTE，概念跟其他 warehouse 很接近；真正比較值得特別記的是 BigQuery 的平台規則與函式生態。

### Regions and Data Location

BigQuery 的 region 選擇不是小設定，而是會直接影響可查詢性。

關鍵限制：

- dataset 建立後不能直接改 region
- 可以搬移或複寫資料到其他 region
- 不能直接查詢位於兩個不同 regions 的資料

這代表：

- 一開始就要想好資料落在哪裡
- 跨區資料整合不能假設「之後再 join 就好」
- region 決策會和成本、法規、延遲與資料協作一起綁定

### Data Loading

課程中整理了三種常見載入方式：

1. 在 BigQuery Studio 載入
2. 用 `bq` command-line tool
3. 用 SQL 的 `LOAD DATA`

#### Using `bq`

```bash
bq load \
  dataset.table \
  gs://mybucket/mydata.csv \
  --source_format=CSV \
  --autodetect
```

#### Using `LOAD DATA`

```sql
LOAD DATA INTO dataset.table
FROM FILES(
  uris = ['gs://mybucket/mydata.csv'],
  format = 'CSV',
  skip_leading_rows = 1
)
```

這幾種方式反映的其實是同一件事：BigQuery 很常跟 GCS、SQL workflow 與 managed UI 一起使用，而不是只靠單一 ingestion 入口。

### Performance and Cost-Aware Querying

BigQuery 的查詢設計常直接影響成本與速度，所以效能最佳化通常不是最後才做的事。

#### Partitions and Clusters

- 考慮使用 table partitions 和 clusters
- 如果資料表依日期分割，查詢時應在 `WHERE` clause 帶入日期條件

這樣做的目的，是減少不必要的掃描範圍。

#### Approximate Aggregations

在某些分析場景，可以考慮近似聚合函式，例如：

- `APPROX_TOP_SUM`
- `APPROX_COUNT_DISTINCT`

這類函式通常是在精確度可接受的前提下，用較低成本換取更快或更可擴充的查詢。

### DML Notes

BigQuery 也支援常見 DML：

- `INSERT`
- `UPDATE`
- `DELETE`
- `MERGE`
- `CREATE TABLE AS`

幾個實務提醒：

- 能合併的 DML 儘量一起處理，不要切成很多小次執行
- `UPDATE` 需要明確的 `WHERE` 條件
- 若是大規模資料改寫，表設計與 partition / cluster 策略往往比單條 SQL 更重要

### Mental Model for Data Engineering

把 BigQuery 放進資料工程脈絡時，可以這樣理解：

- 它不是 raw landing zone，而是分析型 warehouse
- 它強在 managed analytics，不強在 transaction-first 應用設計
- schema、region、table layout、query pattern 會直接影響使用成本
- 很多工作其實是在設計「怎麼少掃資料、怎麼少跨區、怎麼讓查詢可維護」

### Practical Reminders

- 先想清楚 `project / dataset / table` 層級，不要只記得資料表名稱。
- region 一開始就要選對，因為之後不能直接改，而且跨 region 查詢有限制。
- 查詢大表時，優先確認是否能利用 partition filter。
- BigQuery 雖然 serverless，但不是「不用管效能」；只是效能問題通常會反映在 query pattern 和 cost 上。
- 如果需求偏向大量分析與 managed SQL warehouse，BigQuery 很合適；如果需求是高頻交易式寫入，就不要用同樣心智期待它。

## Redshift

Amazon Redshift 是 AWS 上的 distributed, columnar data warehouse，主要用來支援大規模 SQL analytics。它和一般 row-based transactional database 最大的差別，不只是資料量，而是整個查詢與資料分布的設計思維都不同。

### What Redshift Is

- distributed database
- columnar database
- SQL-first analytics warehouse
- 使用 PostgreSQL 9 syntax 的一部分，並加上自己的擴充
- 同時支援 serverless 與 provisioned clusters

從資料工程角度看，Redshift 的重點不是「像 PostgreSQL 一樣用」，而是理解它如何把資料分散到多個 compute nodes，並讓分析查詢在這些節點上平行執行。

### Why Redshift Feels Different

#### Columnar Storage

- 以 column 為單位讀取資料
- 特別適合 analytical queries
- 這也是為什麼 `SELECT *` 特別不划算

#### Distributed Execution

- 資料與查詢運算分散在多個 compute nodes
- table design 會直接影響 join、aggregation 與 scan 效率

#### AWS-Centric Warehouse Position

Redshift 在 AWS 裡常被當成 primary SQL warehouse，並能和其他服務一起工作，例如：

- RDS for PostgreSQL
- Aurora PostgreSQL-compatible edition
- EMR / Hive
- Kinesis

它也支援 external schemas，因此不只查自己內部資料表，還能把外部資料源接進同一個 SQL workflow。

### Row-Based vs. Columnar Thinking

如果用 row-based OLTP database 的方式思考 Redshift，通常會踩到效能坑。

在 Redshift 裡：

- 查詢常只需要部分欄位時，columnar storage 很有優勢
- table distribution 與 sort order 會影響跨節點資料移動
- query tuning 不只是改 SQL，還包含 table design

### Serverless vs. Provisioned

Redshift 可以是：

- `serverless`
- `provisioned cluster`

這代表團隊可以依 workload、成本模型與管理偏好選擇不同部署方式。但無論是哪種模式，底層仍然是 analytics-first 的 distributed warehouse 心智。

### Distribution and Data Placement

Redshift table 的核心設計問題之一，是資料要怎麼分散到節點上。

#### DISTKEY

- `DISTKEY` 用來決定資料依哪個欄位分布
- 對常見 join / aggregation path 很重要

#### Distribution Styles

課程整理了四種常見 distribution style：

- `ALL`: 整張表複製到每個 node，適合小型 lookup table
- `KEY`: 依 `DISTKEY` 欄位分布，適合常以同鍵 join 或 aggregate 的表
- `EVEN`: 輪流分布 rows 到各節點，適合沒有明確分布鍵的大表
- `AUTO`: 讓 Redshift 依表大小與條件自動選擇策略

一個實務心智是：

- 小表常適合 `ALL`
- 常 join 的大表要優先思考 `KEY`
- 沒明確 join key 的大表才比較像 `EVEN`

### SORTKEY

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

### Query Optimization Patterns

#### Avoid `SELECT *`

因為 Redshift 是 columnar：

- 不要取不需要的欄位
- 只選必要 columns，通常就能少做很多 I/O

#### Build Better Predicates

課程的重點不是某一條 SQL，而是 predicate placement：

- 對 joined table 的條件，盡量貼近 join
- 善用 `DISTKEY` / `SORTKEY` 對應欄位
- 避免在關鍵 predicate 上套函式

這麼做的目的，是讓 Redshift 更容易把過濾條件推到適合的節點與資料範圍。

### Table Design Matters

在 Redshift 裡，table definition 不只是 schema。

除了欄位型別，還要一起想：

- distribution style
- `DISTKEY`
- `SORTKEY`
- 查詢主要走向
- 是否有 external schema / external table

這也是為什麼 Redshift 的效能優化很多時候從 DDL 就已經開始，而不是等查詢變慢才補救。

### External Schemas and Spectrum-Like Access

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

### Monitoring and Diagnostics

Redshift 的調校不只看 query text，也會看系統層資訊。

幾個實用系統檢視包括：

- `SVV_TABLE_INFO`: 看 table details、`DISTKEY`、`SORTKEY`、skew
- `STL_ALERT_EVENT_LOG`: 看觸發 alert 的 query 與可能的效能問題

這類 system views 很重要，因為它們讓調校從「憑感覺改 SQL」變成「根據資料分布與 alert 觀察來決策」。

### Practical Use Cases

Redshift 常見於：

- AWS 內部分析型 warehouse
- 需要和其他 AWS data services 一起運作的 SQL analytics stack
- 外部與內部 schema 混合查詢
- 以 table design 為核心的高效能報表與聚合 workload

### Practical Reminders

- 不要把 Redshift 當成一般 PostgreSQL 來用；語法相近，不代表效能心智相同。
- 在 Redshift 裡，table design 和 query design 幾乎同等重要。
- `DISTKEY` 是資料如何跨節點分布的問題；`SORTKEY` 是資料如何在節點內被掃描的問題。
- `SELECT *` 在 columnar warehouse 裡特別昂貴。
- Redshift 查詢慢時，不一定先怪 SQL；也要看 distribution style、sort order、data skew 與 alert logs。
