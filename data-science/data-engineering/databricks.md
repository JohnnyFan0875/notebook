# Databricks

Databricks 是以 Spark 與 Delta Lake 為核心的 lakehouse 平台。本篇分三部分：平台心智模型（架構、Delta、Unity Catalog、compute）、資料管理（table lifecycle、time travel、views、權限與 PII）、Databricks SQL（SQL warehouse、SQL ingestion、`MERGE`、`OPTIMIZE` / `Z-ORDER`）。Spark 本身的 API 見 [Spark and PySpark](spark.md)。

Databricks 可以被理解成一個建立在 lakehouse 思維上的資料平台。它不是只提供 Spark cluster，也不是只提供 SQL warehouse，而是把 data storage、distributed compute、governance、notebooks 與 analytics workflows 收斂到同一個平台裡。

如果 Spark 比較像運算引擎，Databricks 則更像把 Spark、Delta、catalog、workspace 與 SQL analytics 包成一個可被團隊長期協作的工作環境。

## What Databricks Is

- 以 lakehouse 為核心的 data platform
- 建立在 Apache Spark 與 Delta 生態之上
- 同時服務 data engineering、analytics、BI 與部分 machine learning workflow
- 把 notebooks、compute、catalog 與 SQL experiences 放在同一個平台中

這也是為什麼 Databricks 常被拿來和傳統 warehouse 對照。它不只是「另一個查 SQL 的地方」，而是試圖把 data lake 的彈性和 warehouse 的可治理性整合起來。

## Lakehouse Mental Model

Databricks 很強調 `lakehouse`。

可以把 lakehouse 理解成：

- 底層仍然保有 object storage / open file format 的彈性
- 上層再加上 transaction、table semantics、governance 與 SQL access

這種做法想同時保留兩邊的優點：

- data lake 的開放性與可擴充性
- data warehouse 的可管理性、效能與分析體驗

如果你已經熟悉 medallion architecture，可以把 Databricks 想成很常被拿來承載 bronze、silver、gold 資料成熟度流程的平台。

## Core Architecture

Databricks 的高層架構可以先拆成兩塊：

### Control Plane

- 由 Databricks 管理
- 承載 UI、notebooks 與一般控制邏輯
- 負責協調與編排 compute

### Compute Plane

- 比較接近 customer environment
- 是資料儲存與運算資源真正落地的地方
- 和 networking、applications、security boundary 關係比較大

這個拆分很重要，因為它說明了 Databricks 不是單純一台「Spark 伺服器」，而是平台控制層和實際運算層分開的雲端系統。

## Delta Lake and Table Semantics

Databricks 的資料層有一個很重要的概念是 `Delta`。

從課程的角度看，Delta 最值得記的是：

- open-source storage format
- 建立在 Parquet table collection 之上
- 用 transaction log 追蹤變更
- 支援 ACID semantics
- 同時適合 batch 與 streaming datasets

這使得 lakehouse 裡的檔案不再只是鬆散資料檔，而更像可被治理、可被更新、可被查詢的 table layer。

## Unity Catalog

如果 Delta 比較偏資料表格式，那 `Unity Catalog` 比較偏 Databricks 的治理與資料資產管理層。

它的價值包括：

- 把資料資產放進一致的 catalog hierarchy
- 提供權限管理入口
- 幫助團隊理解 lineage 與相關資產
- 讓 SQL、notebook 與資料探索使用相同的命名與治理模型

從使用者心智模型看，常見層級可以理解為：

- `catalog`
- `schema`
- `table` / `view` / `volume`

而 `Catalog Explorer` 則是平台內探索這些資產的 UI 入口，用來：

- 查找資料資產
- 管理 Unity Catalog permissions
- 查看 lineage 與關聯資產

## Why Databricks Fits Multiple Data Teams

Databricks 一個很重要的賣點，是它不只服務單一角色。

從課程整理出的平台定位來看，它同時對三類團隊有吸引力：

- `data engineering`: 需要 ingest、transform、orchestrate 與維護 Delta tables
- `data warehousing / BI`: 需要 SQL-optimized analytics、dashboard 與 BI connectivity
- `AI / ML`: 需要可擴充 compute、可靠資料層，以及和其他 data teams 共用同一套資產底座

這種跨角色共用平台的價值在於：

- 不同團隊不必各自搬一份資料到不同系統
- governance、lineage 與 asset naming 可以更一致
- upstream engineering 和 downstream analytics / ML 可以站在同一個 lakehouse base 上協作

## Compute in Databricks

Databricks 的 compute 不只一種，至少要先分清楚：

- clusters
- SQL warehouses

這兩者都提供算力，但服務的工作型態不同。

### Clusters

clusters 比較像通用型 compute，常用在：

- notebook-driven exploration
- Spark jobs
- data engineering pipelines
- 一般程式化資料處理

課程裡提到兩個很實用的高層分類：

- `classic`: compute 比較在 customer environment 內，較能沿用既有 compute / security boundary，但啟動通常較慢
- `serverless`: 啟動快、平台代管更多、Databricks 持續優化效能，但 compute ownership boundary 會和 classic 不同

從工作型態來看，cluster 也常被拿來承接：

- 大量資料轉換
- notebook-driven data engineering
- AI / ML 訓練或特徵處理

### SQL Warehouses

`SQL warehouse` 比較偏分析與 BI 消費層。

它的角色比較像：

- 執行 SQL analytics
- 給 analysts 使用的 SQL compute
- 報表與 BI tool 連線的查詢後端

如果 cluster 比較像通用資料運算工作台，SQL warehouse 更像專門給 SQL workloads 的查詢引擎邊界。

## Notebooks and Development Experience

Databricks Notebooks 可以理解成平台內建、偏協作導向的 notebook environment。

它的定位大致是：

- 建立在 Jupyter-like experience 之上
- 和 cluster / data / SQL / visualization 更直接整合
- 適合 exploratory analysis、prototype 與教學式工作流

如果團隊不想完全綁在瀏覽器內，`Databricks Connect` 則提供另一種心智模型：

- 本地 IDE 開發
- 遠端使用 Databricks cluster 的算力
- 在熟悉工具中工作，同時維持平台運算能力

## Data Engineering Workflows on Databricks

Databricks 不是只有「可以跑 Spark」而已，它也提供一些比較平台化的資料工程入口。

課程裡提到幾個特別有代表性的元件：

- `Auto Loader`: 幫助把不同來源的資料持續整合進 lakehouse
- `Delta Live Tables`: 把資料清理與轉換流程變成更可管理的 pipeline
- `Feature Store`: 在 ML workflow 中提供可重用的特徵管理概念

可以把它們理解成：

- Spark 是底層分散式運算能力
- Delta 是 table layer
- 這些平台元件則是在其上提供更完整的 workflow abstraction

對 data engineering 來說，這代表團隊不一定每件事都要從零手刻；有些常見 pipeline 問題，平台已經提供較高階的 building blocks。

## Lakehouse for AI and ML

Databricks 也強調 lakehouse 不只適合 analytics，對 AI / ML 也有吸引力。

課程裡留下來的幾個核心理由是：

- Delta lake 內有比較可靠的 data 與 files base
- compute 可以大規模擴充
- 可以沿用 open standards、libraries 與 frameworks
- 能和其他 data teams 使用同一套資料底座

這種設計的關鍵不是「把模型塞進資料平台」，而是讓資料工程、分析與 ML 不需要各自建立完全分離的 data stack。

## Workspace and Administration

Databricks 的協作單位通常會落在 `workspace`。

workspace 不只是資料夾，而是：

- 使用者協作空間
- notebook 與 compute 的工作入口
- 權限、身份與平台資產的管理邊界之一

課程裡提到兩種常見管理角色：

- `account administrators`: 建立與管理 workspaces、治理 workspace access、管理 account subscription
- `workspace administrators`: 管理 workspace 內的 identities 與 compute resources

這代表 Databricks 的治理不是只有 table permission，而是 account、workspace、identity、compute 幾層一起設計。

## Marketplace and Partner Connectivity

除了核心資料處理，Databricks 也把外部整合做成平台的一部分。

兩個值得記的入口是：

- `Partner Connect`: UI-based partner integration，例如 BI connections、ingestion tools
- `Databricks Marketplace`: 探索與接入第三方 datasets，並把它們整合進資料資產管理流程

這代表 Databricks 不只是在平台內執行資料工作，也在試圖成為更大資料生態的整合中心。

## How It Fits with the Rest of the Stack

可以用這個方式快速定位 Databricks：

- `Spark and PySpark` 比較回答「分散式運算怎麼工作」
- `Storage and Models` 比較回答「lake、warehouse、Delta 這些儲存抽象怎麼分」
- `Databricks Foundations` 比較回答「這些能力在一個實際平台裡怎麼被組合起來」

所以 Databricks 這篇更偏平台心智模型，而不是只講某一個單獨技術元件。

## Practical Reminders

- 不要把 Databricks 縮成「Spark UI」；它比較像一個整合 compute、governance、data assets 與 analytics 的平台。
- cluster 和 SQL warehouse 都是 compute，但服務對象與使用情境不同。
- Delta 解決的是 table semantics 問題；Unity Catalog 解決的是治理與資產管理問題。
- workspace admin 和 account admin 的責任邊界不同，治理時要分清楚。
- 對 SQL 使用者來說，Databricks SQL 是很重要的 adoption bridge，因為它把 lakehouse 能力包進熟悉的 BI / SQL 工作方式。

## Data Management

在 Databricks 裡，資料管理不只是把資料存進 Delta table。真正的工作通常還包括：

- 決定 table 由誰管理生命周期
- 決定資料能不能回看歷史版本
- 決定哪些資產該做成 view
- 決定誰能看、誰能改、誰能擁有敏感資料


### Time Travel and Historical Review

`time travel` 是 Delta 很實用的一個能力，因為它讓團隊可以回看舊版本資料。

這在實務上很有價值，因為它支援：

- historical review
- 追查資料在某次更新前後的差異
- debug pipeline 錯誤或意外覆寫
- 回答「當時看到的資料是什麼」

如果資料平台不能回看歷史，很多資料品質問題只能靠猜；time travel 讓這件事可驗證得多。

### Unified Batch and Streaming Thinking

課程也強調 Delta 可以同時支援 batch 和 streaming workflows。

這代表團隊不需要為了不同處理模式維護完全不同的 storage mental model。從管理角度看，這有幾個好處：

- 減少重複資料管線
- 降低處理流程分裂的複雜度
- 讓同一份 data asset 能同時服務不同更新節奏

### Table Persistence

一個很容易被忽略，但其實非常重要的概念是 `table persistence`。

它影響的是：

- 資料實際存在哪裡
- table 被刪掉時資料會不會跟著刪
- lifecycle 由平台管還是由團隊自己管
- 後續維運與合規責任落在哪一側

Databricks 課程裡把它先分成兩類：

- `managed tables`
- `unmanaged tables`

### Managed vs. Unmanaged Tables

#### Managed Tables

`managed table` 比較像由 Databricks 幫你管理資料位置與生命周期。

課程裡的高層特點包括：

- Databricks 管 data location 與 lifecycle
- 刪掉 table 時，資料通常也跟著刪除
- 適合比較簡單、集中式的管理模式

它的優點是方便，但也代表你要接受平台對 lifecycle 的更高參與度。

#### Unmanaged Tables

`unmanaged table` 則比較接近團隊自己控制底層儲存位置與生命周期。

課程裡提到的重點包括：

- 採較 decentralised 的管理方式
- 團隊自行控制 data storage location 與 lifecycle
- 刪掉 table definition 不一定會刪除底層資料
- 比較適合 custom storage 或 compliance requirements

它的彈性更高，但也意味著要承擔更多治理與維運責任。

#### Practical Tradeoff

可以用這個方式快速判斷：

- 想要簡化管理、讓平台幫忙承接更多 lifecycle 工作時，managed table 通常更自然
- 已經有既定儲存規則、跨系統共享需求或合規限制時，unmanaged table 往往更合適

關鍵不是哪一種永遠比較好，而是 ownership 和 lifecycle 該放在哪一邊。

### Databases, Tables, and Organizational Structure

課程裡也提醒一件很基本但很重要的事：資料結構如果一開始沒整理好，後面治理成本會迅速上升。

在 Databricks 裡，常見做法會先把資料放進有組織的層級，例如：

- database / schema 用來分組相關 tables
- tables 保存主要結構化資料
- 之後再根據需要建立 views 或更高階消費層

這件事聽起來很基本，但它直接影響：

- 資料能不能被快速找到
- 權限能不能被合理地套用
- 團隊能不能理解哪些表屬於同一主題

### Views and Temporary Views

這門課還有一個很值得留下來的重點：不要把所有資料邏輯都直接暴露在 base tables 上。

`view` 的價值通常包括：

- 提供較乾淨、較穩定的查詢入口
- 隱藏不必要的複雜度
- 讓多個使用者共用一致的 business logic

而 `temp view` 則比較適合：

- 暫時性的分析流程
- 中間轉換步驟
- notebook / session 內部工作

可以把它們理解成：

- table 比較像主要資料資產
- persistent view 比較像共享邏輯介面
- temp view 比較像短生命週期的工作台中介層

### Data Explorer and Asset Governance

課程裡用 `Data Explorer` 來說明 Databricks 中資料探索與治理入口的價值。

它的重要性在於：

- 快速找到並管理 table assets
- 直接做權限治理
- 預覽與檢查敏感資料
- 指派 ownership

這種入口的價值不是只有「UI 好用」，而是讓資料治理不必完全依賴每個人各自記住 table 名稱與權限細節。

### Access Rights and Access Levels

資料管理一定會碰到 access control，而這門課有一個很好的提醒：權限不是只有「能不能進去」，而是 access level 的差異會改變風險。

高層來看：

- `read-only` 適合只需要查看資料的角色
- 更高權限則可能包含更新、維護或管理能力

這種區分很重要，因為許多資料風險不是來自外部入侵，而是內部權限過大。

實務上至少要定期檢查：

- 誰只需要看
- 誰真的需要改
- 誰應該是 asset owner

### Sensitive Data and PII

課程也特別拉出 `PII`。

這提醒我們：Databricks 裡的資料治理不是純技術問題，也常直接連到法規與產業要求。

幾個重點包括：

- PII 會因產業與地區規範不同而有不同風險
- healthcare、finance、government 等情境通常要求更嚴格
- 資料儲存、存取與分享都可能受法規約束
- 權限與 ownership 設計必須跟敏感度一起考慮

換句話說，敏感資料不只是「一張重要表」，而是整個 access model、audit 與 lifecycle 都要更謹慎。

### Practical Reminders

- Delta 的價值不只是快，而是更容易支援一致性、追溯與長期維護。
- managed table 和 unmanaged table 的差異，本質上是 ownership 與 lifecycle 的差異。
- 如果 view strategy 不清楚，團隊很容易直接把 base tables 當最終消費層，之後會越來越亂。
- 權限治理要關注 access level，而不只是有沒有 permission。
- PII 與敏感資料治理不該等到資料進平台後才補想，最好在 asset 設計時就一起決定 ownership、visibility 與 retention。

## Databricks SQL

Databricks SQL 可以被理解成 Databricks 平台中專門服務 SQL analysts、BI use cases 與 lakehouse-style warehousing 的入口。它不是把 SQL 硬套在資料湖上，而是把 SQL warehouse、Delta tables、Unity Catalog 與可視化工作流整合成一個比較熟悉的分析環境。


### Why Databricks SQL Exists

課程一開始用一個很實用的對比說明它的定位：

- 傳統 data warehouse 很適合 SQL workloads，但通常更昂貴、較封閉、整合彈性有限
- data lake 很開放也更便宜，但對純 SQL 使用者來說，效能與體驗常常不夠理想

Databricks SQL 想補的，就是這個缺口。

它試圖把：

- SQL users 想要的 familiar experience
- lakehouse 想保留的 open storage 與平台整合

放在同一個地方。

### Core Mental Model

可以把 Databricks SQL 想成：

- 建立在 Databricks 平台上的 SQL-first analytics layer
- 直接查詢 Unity Catalog / Delta table
- 用 SQL warehouse 提供查詢算力
- 同時支援查詢、視覺化、dashboard 與部分資料工程工作

它不是只給最終報表查詢用，也不是只給資料工程師用，而是在兩者之間建立一個共同的 SQL 工作面。

### What SQL Users Get

課程裡幾個最值得留下來的定位是：

- `ANSI SQL` 為基礎
- familiar environment for SQL users
- SQL-optimized performance，例如 `Photon`
- 可以直接連接常見 BI tools
- 內建 visualization 能力
- 不必離開 Databricks 平台就能做查詢與分析

這對 adoption 很重要，因為很多團隊不是不需要 lakehouse，而是不能要求所有 analyst 都先改成 Spark / notebook workflow。

### Querying Data in the Lakehouse

在 Databricks SQL 裡，查詢的重點不只是 `SELECT ... FROM ...` 本身，而是它可以直接站在 lakehouse 資產模型上工作。

常見情境包括：

- 查 Unity Catalog 裡的 managed tables
- 查 volume / file-based data
- 用 familiar SQL patterns 做過濾、聚合與轉換

這讓 SQL 使用者不需要先切到另外一套 storage mental model，仍然可以在平台標準治理與命名下工作。

### Ingesting Data with SQL

這門課有一個很有價值的點：Databricks SQL 不只是查詢入口，也能參與資料進入 lakehouse 的流程。

#### GUI-Based Ingestion Options

課程提到兩種高層入口：

- `Lakeflow Connect`: 內建 connectors，可接 databases、SaaS applications，並建立持續更新的 pipelines
- `Data upload`: 手動上傳 CSV、Parquet 等檔案，快速建立 Delta tables，適合 ad hoc data upload

#### SQL-Based Ingestion

除了 GUI，Databricks SQL 也能直接用 SQL 做 ingestion。

例如：

```sql
COPY INTO my_table
FROM '...';
```

這類操作的價值在於：

- analyst / analytics engineer 不一定要先切回 notebook
- 小型或中型 ingest workflow 可以直接留在 SQL environment
- downstream table 建立與資料接入可以更靠近同一套 SQL workflow

### Transforming Data in SQL

Databricks SQL 也能承接 lakehouse 裡常見的轉換工作。

課程反覆出現的實務語境包括：

- 建立新的 Delta tables
- 把上游資料轉成 downstream tables
- 從較原始的 layer 整理成 gold / BI-ready layer

這代表在 Databricks 裡，SQL 不只是 ad hoc query language，也可以是資料建模與轉換語言的一部分。

### Common Data Engineering Patterns

這門課最值得整合進 notebook 的地方，是它把幾個 lakehouse 上常見的 SQL 模式講得很具體。

#### Incremental Append

當新資料只需要被附加到既有表尾端時，可以用 append pattern。

```sql
INSERT INTO students
TABLE visiting_students;
```

這種做法適合：

- append-only data
- event log 類資料
- 不需要更新既有列的情境

#### Change Data Capture with `MERGE`

當資料需要整合進既有表，而不是單純 append，`MERGE` 就很重要。

```sql
MERGE INTO target
USING source
ON target.key = source.key
WHEN MATCHED THEN UPDATE SET *;
```

它常用在：

- upsert
- CDC ingestion
- 維護 current-state table

如果只會 `INSERT`，通常很快就會卡在資料重送、重複列或更新語意上；`MERGE` 是 lakehouse / warehouse SQL workflow 的核心能力之一。

### Data Optimization Patterns

Databricks SQL 不只處理資料進出，也涉及 Delta table 的效能維護。

課程裡兩個最值得記的操作是：

- `OPTIMIZE`
- `Z-ORDER`

#### `OPTIMIZE`

`OPTIMIZE` 的核心作用，是把資料重新整理與 compact，降低 small file problem。

```sql
OPTIMIZE table_name;
```

也可以只整理特定子集：

```sql
OPTIMIZE table_name
WHERE date >= '2024-01-01';
```

#### `Z-ORDER`

`Z-ORDER` 可以把相關資料更有機會 co-locate 到相近檔案中，幫助讀取效率。

```sql
OPTIMIZE table_name
WHERE date >= current_timestamp() - INTERVAL 1 day
ZORDER BY (eventType);
```

從實務角度看：

- `OPTIMIZE` 比較像檔案整理與 compact
- `Z-ORDER` 比較像為常用查詢條件改善資料局部性

這些操作提醒我們：在 lakehouse 裡，SQL 效能不只來自 query text，也和資料檔案形狀有關。

### Databricks SQL for Analysis

Databricks SQL 也很強調 native analytics experience。

課程裡的定位是：

- analysts 可以直接建立 queries
- 可以做 visualizations
- 可以建立 dashboards
- 也可以接 partner BI tools

這表示團隊可以視情況選擇：

- 直接在 Databricks 內完成查詢與 dashboard
- 或把 Databricks 當成 BI tool 的 SQL backend

### When Databricks SQL Is a Good Fit

Databricks SQL 特別適合這些情境：

- 團隊主要以 SQL 為共同語言
- 已經在 Databricks / lakehouse 平台內工作
- 需要同時兼顧 BI、查詢與部分資料工程轉換
- 想保留 open lakehouse table layer，而不是只依賴封閉式 warehouse

如果需求偏通用 Spark code、heavy custom processing 或 notebook-first engineering，cluster / notebook workflow 仍然更自然；但如果需求是 SQL-first analytics，Databricks SQL 會更順手。

### Practical Reminders

- 不要把 Databricks SQL 想成只有查報表；它也能參與 ingestion、transformation 與 table maintenance。
- `MERGE`、`OPTIMIZE`、`Z-ORDER` 是 Databricks SQL 很有代表性的 lakehouse SQL pattern。
- SQL warehouse 是查詢算力邊界，和通用 cluster 的角色不同。
- SQL 使用者的 adoption 關鍵，不只是語法熟悉，而是整個 catalog、table、dashboard 與 BI workflow 能否保持連續。
- 如果資料已經落在 Delta / Unity Catalog 體系內，Databricks SQL 可以把治理與分析體驗串得很自然。
