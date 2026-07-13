# Snowflake Foundations

Snowflake 是一個受管的 cloud data warehousing platform，常被用在歷史分析、報表與大規模 SQL analytics。它不是傳統自己架設的資料庫，而是把 storage、compute 與管理層分開處理的資料平台。

## What Snowflake Is

- cloud-native data warehouse
- SQL-first analytics platform
- 常被 Data Engineers、BI Engineers 與 analysts 使用
- 適合 large-scale historical analysis and reporting

從資料工程角度看，Snowflake 的重點不是「能不能跑 SQL」，而是它把 warehouse 變成一個可管理、可擴充、可分權的受管平台。

## Why Snowflake Is Popular

- 不需要自己 provisioning hardware 或 software
- 建立帳號後就能快速開始使用
- 以 self-managed service 的體驗提供資料平台能力

這種體驗讓團隊可以把心力放在 data modeling、permissions、performance 與 ingestion，而不是底層基礎設施維護。

## Ways to Connect

Snowflake 不只透過 web UI 使用，實務上常見的連線方式還包括：

- `ODBC` / `JDBC`: 給 BI tools、Java 生態或一般資料庫整合使用
- language connectors: 例如 Python、Spark 等
- `SnowSQL` / Snowflake CLI: 適合 command-line workflow、腳本化操作與排錯

這很重要，因為 Snowflake 往往不是孤立使用，而是被接進 ETL、BI、notebook 或 application pipeline。

## Core Architecture

Snowflake 的平台結構可以粗分成三層：

### Cloud Services

- 協調 user activities
- 負責較偏控制面的平台行為

### Query Processing

- 使用 MPP, massive parallel processing
- 將 compute work 分散到多個 nodes

### Database Storage

- 以 columnar format 儲存資料
- 針對 analytical queries 最佳化

這個分層很重要，因為它說明了 Snowflake 不是單一 database server，而是一個把管理、運算、儲存拆開的 analytics system。

## Mental Model: Storage vs. Compute

和其他現代 warehouse 類似，Snowflake 的一個核心觀念是：

- 資料儲存不等於查詢計算
- 你可以針對不同工作負載配置不同 compute resource

這也是 virtual warehouse 重要的原因。

## Virtual Warehouses

`virtual warehouse` 是 Snowflake 中主要的 compute unit。

它的角色比較像：

- 查詢運算資源
- 資料載入時的執行資源
- 依 workload 分離的 compute boundary

### Why Create a New Virtual Warehouse

常見原因包括：

- role-based warehouse access
- 將 engineers 與 analysts 的 workload 分開
- 慢查詢需要更多 compute
- 不同團隊需要不同成本與效能配置

這代表 Snowflake 的效能管理，很多時候不是只改 SQL，而是重新思考 warehouse size、workload isolation 與 access boundaries。

## Query Performance Mental Model

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

### Columnar Storage vs. Row-Based Thinking

row-based storage 比較適合頻繁逐筆交易；columnar storage 則更適合只讀部分欄位、再做聚合與過濾的分析型查詢。

這也是為什麼在 Snowflake 上：

- 避免無差別 `SELECT *`
- 先釐清查詢真正需要哪些欄位
- 減少不必要的大範圍掃描

通常都能帶來更自然的效能改善。

### Micro-Partitions and Scan Reduction

micro-partitions 可以把資料拆成較小的儲存單位，讓系統有機會只讀查詢真正需要的部分。

從實務角度看，這提醒我們：

- 查詢條件如果能有效縮小掃描範圍，通常比事後硬調 warehouse 更健康
- 資料模型與欄位設計，也會間接影響查詢是否容易做出不必要的大掃描

### Query Profile as a Debugging Tool

當查詢變慢時，`Query Profile` 很有價值，因為它不是只告訴你「慢」，而是幫你看：

- 查詢大致經過哪些步驟
- 哪些部分消耗較多資源
- 問題比較像是掃描量、計算量，還是 warehouse 配置

這讓效能調校不再只靠猜測。

## Roles and Access Control

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

## Object Hierarchy and Data Types

使用 Snowflake 時，通常要同時理解兩種結構：

- object hierarchy: `database -> schema -> table / view`
- data types: 資料欄位實際怎麼被儲存與比較

入門常見型別包括：

- text/string: `VARCHAR`, `CHAR`, `TEXT`
- numeric: `INTEGER`
- boolean: `BOOLEAN`

雖然這些型別看起來很基本，但它們會直接影響 schema design、casting、join behavior 與 downstream analytics。

## Marketplace and External Data

Snowflake 不只是一個自己放資料的 warehouse，也支援從 Snowflake Marketplace 或雲端來源取得資料。

這代表它除了查詢既有 tables，也常被放進更大的資料供應鏈中：

- 從外部供應者取資料
- 從 cloud storage 載入資料
- 把共享資料接進自己的分析環境

## Loading Data from Cloud Storage

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

## Monitoring and History

Snowflake 也很重視查詢與載入的歷史追蹤。

### Query History

- 可以找回過去執行過的 SQL
- 課程提到預設可查看過去 14 天的查詢歷史
- 有助於找慢查詢、debug 失敗與重現問題

### Copy History

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

## Practical Snowflake Use Cases

Snowflake 常見於這些情境：

- 建企業分析型 warehouse
- 提供 BI / reporting 的 SQL backend
- 承接 external data sharing 或 marketplace data
- 把不同團隊的分析 workload 分開治理

## Practical Reminders

- 不要把 Snowflake 想成只有「一個 database」；它更像完整資料平台。
- virtual warehouse 是 compute boundary，不是資料本身。
- 角色設計會直接影響誰能查資料、誰能管理 warehouse、誰能看監控資訊。
- 載入外部資料時，stage permissions 往往和 SQL 本身一樣重要。
- 如果查詢慢，不一定先改 SQL；有時應該先問是不是 workload isolation 或 warehouse sizing 問題。
