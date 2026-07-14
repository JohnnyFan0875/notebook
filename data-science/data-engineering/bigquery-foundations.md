# BigQuery Foundations

BigQuery 是 Google Cloud 上的 enterprise data warehouse，核心定位是用 SQL 對大量資料做分析，而不是自己管理傳統 database server。

## What BigQuery Is

- SQL-first analytics platform
- 適合 OLAP workload
- 可擴充到 massive datasets
- serverless
- compute 與 storage 分離

這個組合很重要，因為它代表使用者通常更關心資料模型、查詢模式與成本，而不是自己管理機器、叢集與容量規劃。

## Why BigQuery Feels Different

### Serverless

- 沒有傳統意義上的固定資料庫主機可供管理
- 不需要自己挑一台「多大」的 warehouse server 才能開始查詢

### Separate Compute and Storage

- 資料存放與查詢運算不是綁死在同一個節點
- 這讓 BigQuery 更像受管分析系統，而不是傳統單機 database

### OLAP-Oriented

- 重點是大型分析查詢
- 不適合用 transactional database 的心智模型直接理解

## Resource Hierarchy

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

## Querying

### Query Surface

BigQuery 查詢常見入口包括：

- BigQuery Studio
- `bq` command-line tool
- 其他會送 SQL 到 BigQuery 的程式或服務

### SQL Dialect

BigQuery 的主要 SQL 方言是 GoogleSQL。

如果只是一般 SQL 基礎，像 `SELECT`、`JOIN`、`GROUP BY`、CTE，概念跟其他 warehouse 很接近；真正比較值得特別記的是 BigQuery 的平台規則與函式生態。

## Regions and Data Location

BigQuery 的 region 選擇不是小設定，而是會直接影響可查詢性。

關鍵限制：

- dataset 建立後不能直接改 region
- 可以搬移或複寫資料到其他 region
- 不能直接查詢位於兩個不同 regions 的資料

這代表：

- 一開始就要想好資料落在哪裡
- 跨區資料整合不能假設「之後再 join 就好」
- region 決策會和成本、法規、延遲與資料協作一起綁定

## Data Loading

課程中整理了三種常見載入方式：

1. 在 BigQuery Studio 載入
2. 用 `bq` command-line tool
3. 用 SQL 的 `LOAD DATA`

### Using `bq`

```bash
bq load \
  dataset.table \
  gs://mybucket/mydata.csv \
  --source_format=CSV \
  --autodetect
```

### Using `LOAD DATA`

```sql
LOAD DATA INTO dataset.table
FROM FILES(
  uris = ['gs://mybucket/mydata.csv'],
  format = 'CSV',
  skip_leading_rows = 1
)
```

這幾種方式反映的其實是同一件事：BigQuery 很常跟 GCS、SQL workflow 與 managed UI 一起使用，而不是只靠單一 ingestion 入口。

## Performance and Cost-Aware Querying

BigQuery 的查詢設計常直接影響成本與速度，所以效能最佳化通常不是最後才做的事。

### Partitions and Clusters

- 考慮使用 table partitions 和 clusters
- 如果資料表依日期分割，查詢時應在 `WHERE` clause 帶入日期條件

這樣做的目的，是減少不必要的掃描範圍。

### Approximate Aggregations

在某些分析場景，可以考慮近似聚合函式，例如：

- `APPROX_TOP_SUM`
- `APPROX_COUNT_DISTINCT`

這類函式通常是在精確度可接受的前提下，用較低成本換取更快或更可擴充的查詢。

## DML Notes

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

## Mental Model for Data Engineering

把 BigQuery 放進資料工程脈絡時，可以這樣理解：

- 它不是 raw landing zone，而是分析型 warehouse
- 它強在 managed analytics，不強在 transaction-first 應用設計
- schema、region、table layout、query pattern 會直接影響使用成本
- 很多工作其實是在設計「怎麼少掃資料、怎麼少跨區、怎麼讓查詢可維護」

## Practical Reminders

- 先想清楚 `project / dataset / table` 層級，不要只記得資料表名稱。
- region 一開始就要選對，因為之後不能直接改，而且跨 region 查詢有限制。
- 查詢大表時，優先確認是否能利用 partition filter。
- BigQuery 雖然 serverless，但不是「不用管效能」；只是效能問題通常會反映在 query pattern 和 cost 上。
- 如果需求偏向大量分析與 managed SQL warehouse，BigQuery 很合適；如果需求是高頻交易式寫入，就不要用同樣心智期待它。
