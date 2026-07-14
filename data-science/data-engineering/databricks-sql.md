# Databricks SQL

Databricks SQL 可以被理解成 Databricks 平台中專門服務 SQL analysts、BI use cases 與 lakehouse-style warehousing 的入口。它不是把 SQL 硬套在資料湖上，而是把 SQL warehouse、Delta tables、Unity Catalog 與可視化工作流整合成一個比較熟悉的分析環境。

如果 [Databricks Foundations](databricks-foundations.md) 比較回答平台是什麼，這篇更偏向回答：只用 SQL 的團隊在 Databricks 上到底怎麼工作。

## Why Databricks SQL Exists

課程一開始用一個很實用的對比說明它的定位：

- 傳統 data warehouse 很適合 SQL workloads，但通常更昂貴、較封閉、整合彈性有限
- data lake 很開放也更便宜，但對純 SQL 使用者來說，效能與體驗常常不夠理想

Databricks SQL 想補的，就是這個缺口。

它試圖把：

- SQL users 想要的 familiar experience
- lakehouse 想保留的 open storage 與平台整合

放在同一個地方。

## Core Mental Model

可以把 Databricks SQL 想成：

- 建立在 Databricks 平台上的 SQL-first analytics layer
- 直接查詢 Unity Catalog / Delta table
- 用 SQL warehouse 提供查詢算力
- 同時支援查詢、視覺化、dashboard 與部分資料工程工作

它不是只給最終報表查詢用，也不是只給資料工程師用，而是在兩者之間建立一個共同的 SQL 工作面。

## What SQL Users Get

課程裡幾個最值得留下來的定位是：

- `ANSI SQL` 為基礎
- familiar environment for SQL users
- SQL-optimized performance，例如 `Photon`
- 可以直接連接常見 BI tools
- 內建 visualization 能力
- 不必離開 Databricks 平台就能做查詢與分析

這對 adoption 很重要，因為很多團隊不是不需要 lakehouse，而是不能要求所有 analyst 都先改成 Spark / notebook workflow。

## SQL Warehouses

Databricks SQL 背後的主要算力邊界是 `SQL warehouse`。

它的角色比較像：

- 執行 SQL 查詢的 compute resource
- 支援 analysts、BI reports 與 dashboards
- 把查詢工作和一般 Spark cluster 的通用運算分開

如果 cluster 比較像工程師的通用工作台，SQL warehouse 更像分析消費層的專用查詢引擎。

## Querying Data in the Lakehouse

在 Databricks SQL 裡，查詢的重點不只是 `SELECT ... FROM ...` 本身，而是它可以直接站在 lakehouse 資產模型上工作。

常見情境包括：

- 查 Unity Catalog 裡的 managed tables
- 查 volume / file-based data
- 用 familiar SQL patterns 做過濾、聚合與轉換

這讓 SQL 使用者不需要先切到另外一套 storage mental model，仍然可以在平台標準治理與命名下工作。

## Ingesting Data with SQL

這門課有一個很有價值的點：Databricks SQL 不只是查詢入口，也能參與資料進入 lakehouse 的流程。

### GUI-Based Ingestion Options

課程提到兩種高層入口：

- `Lakeflow Connect`: 內建 connectors，可接 databases、SaaS applications，並建立持續更新的 pipelines
- `Data upload`: 手動上傳 CSV、Parquet 等檔案，快速建立 Delta tables，適合 ad hoc data upload

### SQL-Based Ingestion

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

## Transforming Data in SQL

Databricks SQL 也能承接 lakehouse 裡常見的轉換工作。

課程反覆出現的實務語境包括：

- 建立新的 Delta tables
- 把上游資料轉成 downstream tables
- 從較原始的 layer 整理成 gold / BI-ready layer

這代表在 Databricks 裡，SQL 不只是 ad hoc query language，也可以是資料建模與轉換語言的一部分。

## Common Data Engineering Patterns

這門課最值得整合進 notebook 的地方，是它把幾個 lakehouse 上常見的 SQL 模式講得很具體。

### Incremental Append

當新資料只需要被附加到既有表尾端時，可以用 append pattern。

```sql
INSERT INTO students
TABLE visiting_students;
```

這種做法適合：

- append-only data
- event log 類資料
- 不需要更新既有列的情境

### Change Data Capture with `MERGE`

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

## Data Optimization Patterns

Databricks SQL 不只處理資料進出，也涉及 Delta table 的效能維護。

課程裡兩個最值得記的操作是：

- `OPTIMIZE`
- `Z-ORDER`

### `OPTIMIZE`

`OPTIMIZE` 的核心作用，是把資料重新整理與 compact，降低 small file problem。

```sql
OPTIMIZE table_name;
```

也可以只整理特定子集：

```sql
OPTIMIZE table_name
WHERE date >= '2024-01-01';
```

### `Z-ORDER`

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

## Databricks SQL for Analysis

Databricks SQL 也很強調 native analytics experience。

課程裡的定位是：

- analysts 可以直接建立 queries
- 可以做 visualizations
- 可以建立 dashboards
- 也可以接 partner BI tools

這表示團隊可以視情況選擇：

- 直接在 Databricks 內完成查詢與 dashboard
- 或把 Databricks 當成 BI tool 的 SQL backend

## When Databricks SQL Is a Good Fit

Databricks SQL 特別適合這些情境：

- 團隊主要以 SQL 為共同語言
- 已經在 Databricks / lakehouse 平台內工作
- 需要同時兼顧 BI、查詢與部分資料工程轉換
- 想保留 open lakehouse table layer，而不是只依賴封閉式 warehouse

如果需求偏通用 Spark code、heavy custom processing 或 notebook-first engineering，cluster / notebook workflow 仍然更自然；但如果需求是 SQL-first analytics，Databricks SQL 會更順手。

## Practical Reminders

- 不要把 Databricks SQL 想成只有查報表；它也能參與 ingestion、transformation 與 table maintenance。
- `MERGE`、`OPTIMIZE`、`Z-ORDER` 是 Databricks SQL 很有代表性的 lakehouse SQL pattern。
- SQL warehouse 是查詢算力邊界，和通用 cluster 的角色不同。
- SQL 使用者的 adoption 關鍵，不只是語法熟悉，而是整個 catalog、table、dashboard 與 BI workflow 能否保持連續。
- 如果資料已經落在 Delta / Unity Catalog 體系內，Databricks SQL 可以把治理與分析體驗串得很自然。

[Back to Data Engineering](README.md)
