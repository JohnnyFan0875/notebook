[Data Science](../README.md) › [Data Engineering](README.md) › 雲端資料倉儲

# 雲端資料倉儲 (Cloud Data Warehouses)

Snowflake、BigQuery、Redshift 都是受管、欄式、storage 與 compute（程度不一）分離的分析型倉儲。先看比較表抓差異，再依需要讀各平台細節。SQL 語法差異見 [SQL 方言速查](../databases/sql-dialect-cheatsheet.md)。

## 比較表

| 面向 | Snowflake | BigQuery | Redshift |
| --- | --- | --- | --- |
| 雲端 | 多雲（AWS / Azure / GCP） | GCP | AWS |
| Compute 模型 | virtual warehouse（各自 sizing、隔離 workload，按運作時間計費） | serverless slot；on-demand 依掃描量計費，或購買保留容量 | provisioned cluster 或 Serverless |
| 物件層級 | account → database → schema → table | project → dataset → table | cluster → database → schema → table |
| 減少掃描 | 自動 micro-partition、clustering key | partition + cluster | `DISTKEY`（跨節點分布）+ `SORTKEY`（節點內排序） |
| 載入 | stage + `COPY INTO` | `bq load`、`LOAD DATA` | `COPY`（從 S3）、Spectrum external schema |
| 除錯入口 | Query Profile、Query / Copy History | execution details、bytes processed、`--dry_run` | system tables（`SVV_*`、`STL_*`） |
| 常見陷阱 | warehouse 沒設 auto-suspend、role 設計 | region 建立後不能改；沒用 partition filter 很貴；`LIMIT` 不減少掃描量 | data skew、`SELECT *`、distribution style 選錯 |

共通原則：欄式儲存下只選需要的欄；先用 partition / cluster / sort 讓查詢少掃資料；查詢慢時先看 compute 隔離與資料排列，而不是只改 SQL。

## Snowflake

Snowflake 是受管的雲端資料倉儲，把雲端服務、查詢運算、儲存三層分開。不需要自己準備硬體或軟體，團隊可以把心力放在資料模型、權限、效能與擷取。

| 層 | 角色 |
| --- | --- |
| Cloud services | 協調使用者活動、認證、metadata、查詢最佳化 |
| Query processing | virtual warehouse：MPP（大規模平行處理），把運算分散到多個節點 |
| Database storage | 欄式格式，自動切成 micro-partitions |

| 連線方式 | 用途 |
| --- | --- |
| Web UI（Snowsight） | 查詢、管理、監控 |
| ODBC / JDBC | BI 工具、Java 生態 |
| Python connector、Snowpark、Spark connector | 程式與 notebook |
| SnowSQL / Snowflake CLI | 命令列、腳本化與排錯 |

### Virtual Warehouse

virtual warehouse 是 Snowflake 的運算單位（查詢與載入都用它），與資料本身分開。另建 warehouse 的常見理由：依角色控管存取、分開 engineer 與 analyst 的 workload、慢查詢需要更大的運算、不同團隊要不同的成本配置。

```sql
CREATE WAREHOUSE analytics_wh
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60          -- 閒置 60 秒自動暫停，避免空轉計費
  AUTO_RESUME = TRUE;
```

### 效能

| 概念 | 意義 | 實務 |
| --- | --- | --- |
| 欄式儲存 | 只讀查詢用到的欄 | 避免 `SELECT *` |
| Micro-partitions | 自動管理的小儲存分區，記錄各欄值範圍 | 篩選條件能有效縮小範圍時，只讀需要的分區 (pruning) |
| Clustering key | 大表依常用篩選欄重新排列 | 只對很大且常依同欄篩選的表設定 |
| Query Profile | 查詢各步驟的時間與資源 | 判斷問題在掃描量、計算量還是 warehouse 配置 |

### 角色與存取

| 系統角色 | 用途 |
| --- | --- |
| `ACCOUNTADMIN` | 帳號層級（帳務等），應極少使用 |
| `SECURITYADMIN` | 管理安全相關物件與授權 |
| `USERADMIN` | 管理使用者與角色 |
| `SYSADMIN` | 建立與管理 warehouse、database 等物件 |
| `PUBLIC` | 所有使用者都有，只能用授權給它的物件 |

治理不只是表權限：account、user、role、warehouse 要一起設計；監控資訊通常只開放給高權限角色。

### 載入與監控

```
從雲端儲存準備檔案 → 建立 stage 並設定權限（storage integration）→ COPY INTO 載入 → 檢查 copy history
```

```sql
CREATE STAGE raw_stage URL = 's3://lab-bucket/raw/' STORAGE_INTEGRATION = s3_int;
COPY INTO lab.results FROM @raw_stage FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1);
```

| 歷史 | 內容 | 保留 |
| --- | --- | --- |
| Query History | 過去執行的 SQL，用來找慢查詢與重現問題 | UI 約 14 天；`SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY` 約 1 年 |
| Copy History | 載入的檔案、筆數、成功 / 失敗 | 表層級檢視較即時；`ACCOUNT_USAGE` 檢視有延遲但保留較久 |

Snowflake 也提供 Time Travel（預設 1 天，企業版可延長）與 Marketplace / Data Sharing（直接取用其他帳號分享的資料，不必複製）。

## BigQuery

BigQuery 是 Google Cloud 的 serverless 分析倉儲：沒有要管理的伺服器，compute 與 storage 分離，適合 OLAP，不適合用交易資料庫的心智理解。

| 層級 | 角色 |
| --- | --- |
| Project | 計費、權限、使用者的邊界 |
| Dataset | project 內的邏輯容器，綁定 region |
| Table | 實際資料 |

```sql
SELECT * FROM `project.dataset.table`;            -- 完整名稱；跨 project 查詢也用這個形式
```

主要 SQL 方言是 GoogleSQL；入口有 BigQuery Studio、`bq` CLI 與各語言 client。Google 也在 `bigquery-public-data` 提供公開資料集（含 gnomAD 等基因體資料），可直接查詢。

### Region

| 限制 | 影響 |
| --- | --- |
| dataset 建立後不能改 region | 一開始就要選對（法規、延遲、資料所在） |
| 一個查詢不能直接 join 不同 region 的資料 | 跨區整合要先複製資料 |

### 載入

```bash
bq load --source_format=CSV --autodetect dataset.table gs://mybucket/mydata.csv
```

```sql
LOAD DATA INTO dataset.table
FROM FILES (uris = ['gs://mybucket/mydata.csv'], format = 'CSV', skip_leading_rows = 1);
```

### 成本與效能

| 做法 | 理由 |
| --- | --- |
| 只選需要的欄 | on-demand 依掃描的欄位資料量計費 |
| `LIMIT` 不會省錢 | 仍掃描整欄；預覽資料用表格的 Preview |
| 先 `bq query --dry_run` 或看編輯器的預估量 | 執行前知道會掃多少 |
| 依日期 partition、常用篩選欄 cluster | `WHERE` 帶 partition 條件才會只掃需要的分區 |
| 對大表設 `require_partition_filter` | 強制查詢必須帶 partition 條件 |
| 可接受誤差時用近似聚合 | `APPROX_COUNT_DISTINCT`、`APPROX_QUANTILES`、`APPROX_TOP_SUM` |
| DML 合併成少數大批 | 支援 `INSERT` / `UPDATE` / `DELETE` / `MERGE` / `CREATE TABLE AS`，但不適合大量單筆寫入；`UPDATE` 必須有 `WHERE` |

## Redshift

Amazon Redshift 是 AWS 上的分散式欄式倉儲。語法源自 PostgreSQL（8.0.2）並加上自己的擴充，但效能心智完全不同：資料分散在多個節點，表設計直接決定 join 與聚合要搬多少資料。有 Serverless 與 provisioned cluster 兩種部署，常與 S3、RDS / Aurora、EMR、Kinesis 一起使用，並可透過 external schema（Spectrum）直接查 S3 上的資料。

### 資料分布 (Distribution Style)

| 類型 | 做法 | 適合 |
| --- | --- | --- |
| `ALL` | 整張表複製到每個節點 | 小型 lookup / dimension 表 |
| `KEY` | 依 `DISTKEY` 欄位的值分布 | 常以同一個 key join 或聚合的大表 |
| `EVEN` | 輪流分配到各節點 | 沒有明顯 join key 的大表 |
| `AUTO` | Redshift 依表大小自動選擇 | 預設 |

兩張大表以各自的 `DISTKEY` join 時，相同 key 已在同一節點，不必跨節點搬資料。`DISTKEY` 選到值分布極不均勻的欄位會造成 data skew：少數節點做大部分工作。

### 排序 (`SORTKEY`)

`SORTKEY` 決定節點內資料的排序，讓 `WHERE` 範圍篩選、`JOIN`、`GROUP BY`、`ORDER BY` 可以跳過不需要的區塊。compound sort key 的欄位順序有意義：篩選時要用到前面的欄位才有效。

```sql
CREATE TABLE fact_results (
  sample_id VARCHAR(32), test_code VARCHAR(16), result_date DATE, value DOUBLE PRECISION
)
DISTKEY (sample_id)
COMPOUND SORTKEY (result_date, test_code);
```

### 查詢最佳化

| 做法 | 理由 |
| --- | --- |
| 不要 `SELECT *` | 欄式儲存，多一欄就多一份 I/O |
| 篩選條件貼近 join、用到 `DISTKEY` / `SORTKEY` 欄位 | 讓過濾推到正確節點與資料範圍 |
| 關鍵 predicate 不要包函式（`WHERE date_trunc('day', ts) = ...`） | 無法利用排序跳過區塊 |

### 系統檢視

| 檢視 | 用途 |
| --- | --- |
| `SVV_TABLE_INFO` | 表的 distribution style、sort key、skew（`skew_rows`）、大小 |
| `STL_ALERT_EVENT_LOG` | 查詢觸發的效能警示與建議 |
| `SVV_ALL_SCHEMAS`、`SVV_ALL_TABLES`、`SVV_ALL_COLUMNS` | 盤點 internal 與 external 物件 |
| `SVV_REDSHIFT_SCHEMAS`、`SVV_REDSHIFT_TABLES` | 只看 Redshift 內部物件 |

> Redshift 的效能從 DDL 就開始：查詢慢時，先看 distribution style、sort order、skew 與 alert log，再改 SQL。
