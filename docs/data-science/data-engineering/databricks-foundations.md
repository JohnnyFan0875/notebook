# Databricks Foundations

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

## Databricks SQL

Databricks 不只給 Spark developers 用，也很重視 SQL users。

課程裡幾個值得留下來的定位是：

- `Databricks SQL` 服務 data warehousing for the lakehouse
- 提供熟悉的 SQL environment
- 強調 SQL-optimized performance，例如 `Photon`
- 能連接常見 BI tools
- 內建在平台裡，不需要另外跳到完全不同的產品

這讓 Databricks 不只是工程平台，也能成為分析與報表查詢的消費層入口。

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

[Back to Data Engineering](README.md)
