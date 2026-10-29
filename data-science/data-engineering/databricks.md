[Data Science](../README.md) › [Data Engineering](README.md) › Databricks

# Databricks

Databricks 是以 Spark 與 Delta Lake 為核心的 lakehouse 平台：把物件儲存上的開放格式資料、分散式運算、治理（Unity Catalog）、notebook 與 SQL 分析收在同一個平台。如果 Spark 是引擎，Databricks 就是把引擎、table 層、catalog、workspace 與 BI 包成團隊長期協作的環境。本篇分三部分：平台心智模型、資料管理、Databricks SQL；Spark API 見 [Spark 與 PySpark](spark.md)。

## 平台心智模型

### Lakehouse

| 來自 data lake | 來自 data warehouse |
| --- | --- |
| 物件儲存、開放檔案格式（Parquet）、便宜、可擴充 | 交易、table 語意、治理、SQL 效能與 BI 體驗 |

同一份資料可以同時服務資料工程（擷取、轉換、維護 Delta 表）、BI（SQL、dashboard）與 AI / ML（大規模運算、特徵），不必各搬一份到不同系統；常承載 bronze → silver → gold 的 [medallion 架構](dimensional-modeling-and-star-schema.md#倉儲分層)。

### 架構

| 平面 | 由誰管 | 內容 |
| --- | --- | --- |
| Control plane | Databricks | UI、notebook、job 排程、叢集管理 |
| Compute plane | 客戶雲端帳號（classic）或 Databricks（serverless） | 實際執行運算；資料存在客戶的物件儲存 |

### Delta Lake

Delta 是在 Parquet 檔案集合之上加 transaction log（`_delta_log/`）的開源 table format：

| 能力 | 用途 |
| --- | --- |
| ACID 交易 | 多個寫入者不會讀到寫一半的資料 |
| Time travel | 查詢舊版本、回復誤操作 |
| Schema enforcement / evolution | 擋下欄位不符的寫入；必要時明確允許新增欄位 |
| `MERGE` / `UPDATE` / `DELETE` | 在檔案型資料上做 upsert 與 CDC |
| batch 與 streaming 共用 | 同一張表同時被批次與串流讀寫 |

### Unity Catalog

Unity Catalog 是治理與資料資產管理層：三層命名 `catalog.schema.table`（也包含 view、volume、function、model），統一權限、lineage 與稽核。Catalog Explorer 是瀏覽資產、管理權限、看 lineage 的 UI。

```sql
GRANT SELECT ON TABLE main.genomics.variants_qc TO `analysts`;
GRANT USE CATALOG ON CATALOG main TO `analysts`;
SHOW GRANTS ON TABLE main.genomics.variants_qc;
```

### Compute

| 類型 | 用途 | 特性 |
| --- | --- | --- |
| All-purpose cluster | 互動式 notebook、探索 | 多人共用、閒置也計費（設 auto-termination） |
| Job cluster | 排程的 pipeline | 跑完就關，較便宜 |
| SQL warehouse | SQL 分析、dashboard、BI 工具連線 | 專為 SQL 最佳化（Photon） |
| Classic vs serverless | classic 在自己的雲端帳號內、啟動較慢；serverless 啟動快、由 Databricks 代管 | 資料邊界與網路設定不同 |

### 開發與資料工程元件

| 元件 | 用途 |
| --- | --- |
| Notebooks | 平台內建、整合叢集與資料的協作 notebook |
| Databricks Connect | 在本機 IDE 開發，使用遠端叢集算力 |
| Auto Loader | 增量偵測並擷取雲端儲存中的新檔案 |
| Lakeflow Declarative Pipelines（原 Delta Live Tables） | 宣告式定義表與資料品質規則 (expectations)，由平台管理依賴與重跑 |
| Lakeflow Jobs（Workflows） | 排程與編排 |
| Feature Store / Feature Engineering | ML 特徵的重用與線上 / 離線一致 |
| MLflow | 實驗追蹤與模型管理，見 [MLflow](../machine-learning/production/mlflow.md) |
| Partner Connect、Marketplace | 接 BI / 擷取工具、取得第三方資料集 |

平台元件會改名（例如 DLT 在 2025 年併入 Lakeflow），找文件時新舊名稱都要搜。

### 管理角色

| 角色 | 責任 |
| --- | --- |
| Account admin | 建立與管理 workspace、帳號訂閱、Unity Catalog metastore |
| Workspace admin | workspace 內的身分、群組與運算資源 |

## 資料管理

### Managed vs External Tables

| | Managed table | External table |
| --- | --- | --- |
| 資料位置與生命週期 | Databricks / Unity Catalog 管理 | 團隊自行指定儲存位置（`LOCATION`） |
| `DROP TABLE` | 資料也會刪除 | 只刪定義，底層檔案保留 |
| 適合 | 簡單、集中管理；可用平台自動最佳化 | 既有儲存規則、跨系統共享、合規要求 |

舊文件稱 external table 為 unmanaged table。差別本質上是 ownership 與 lifecycle 放在哪一側。

### Time Travel

```sql
DESCRIBE HISTORY main.genomics.variants_qc;                      -- 每次寫入的版本、時間、操作
SELECT * FROM main.genomics.variants_qc VERSION AS OF 12;
SELECT * FROM main.genomics.variants_qc TIMESTAMP AS OF '2026-10-01';
RESTORE TABLE main.genomics.variants_qc TO VERSION AS OF 12;     -- 回復誤操作
```

用途：追查某次更新前後的差異、除錯 pipeline、回答「當時看到的資料是什麼」，也讓分析可以引用固定版本以便重現。

> `VACUUM` 會刪除超過保留期（預設 7 天）的舊檔案，之後就無法 time travel 到那些版本。需要長期可重現的版本時，另外保存快照或記錄版本並調整保留期。

### Table、View、Temp View

| 物件 | 角色 | 生命週期 |
| --- | --- | --- |
| Table | 主要資料資產 | 永久 |
| View | 共享的邏輯介面：隱藏複雜度、統一業務邏輯、限制可見欄位 | 永久，不存資料 |
| Temp view | notebook / session 內的中介步驟 | session 結束即消失 |

不要讓使用者直接把 base table 當最終消費層；用 view 提供穩定的查詢入口，之後 base table 改結構時下游比較不受影響。

### 權限與敏感資料

| 原則 | 做法 |
| --- | --- |
| 區分存取層級 | 只讀、可修改、擁有者分開授權 |
| 用群組授權 | 不逐一指派個人 |
| 指定 owner | 每個資產都有負責人 |
| 敏感欄位 | column mask、row filter、只開放去識別化的 view |
| PII / PHI | 醫療、金融、政府資料的法規要求更嚴；儲存、存取、分享都受約束 |

敏感資料治理要在資產設計時就決定 ownership、可見範圍與保存期限，而不是進平台後才補，見 [資料治理](governance.md)、[隱私與法規](../responsible-ai/privacy-and-regulation.md)。

## Databricks SQL

Databricks SQL 是平台上的 SQL-first 分析層：以 ANSI SQL 直接查 Unity Catalog 中的 Delta 表，用 SQL warehouse 提供算力（Photon 引擎），內建查詢編輯器、視覺化與 dashboard，也可作為 Power BI / Tableau 的後端。它補的是傳統 warehouse（貴、封閉）與 data lake（便宜開放但 SQL 體驗差）之間的缺口：讓 SQL 分析師不必改用 Spark / notebook 也能使用 lakehouse。

### 擷取

| 方式 | 用途 |
| --- | --- |
| Lakeflow Connect | 內建 connector，從資料庫、SaaS 建立持續更新的 pipeline |
| 檔案上傳 UI | 手動上傳 CSV / Parquet 快速建 Delta 表，適合臨時資料 |
| `COPY INTO` | SQL 增量載入雲端儲存中的檔案（已載入的檔案不會重複載入） |

```sql
COPY INTO main.lab.results
FROM 's3://lab-bucket/results/'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true');
```

### 轉換模式

```sql
-- 1. 純附加：append-only 的事件或 log
INSERT INTO students TABLE visiting_students;

-- 2. Upsert / CDC：有就更新、沒有就新增
MERGE INTO patients AS t
USING patients_updates AS s
ON t.patient_id = s.patient_id
WHEN MATCHED AND s.is_deleted THEN DELETE
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- 3. 由上游建立下游表（silver → gold）
CREATE OR REPLACE TABLE main.gold.tissue_summary AS
SELECT tissue, gene, avg(log_tpm) AS mean_log_tpm, count(*) AS n
FROM main.silver.expression GROUP BY tissue, gene;
```

> `MERGE` 的 source 若有多列對到同一個 target 列會直接失敗；先在 source 去重（例如每個 key 只留最新一筆）。只寫 `WHEN MATCHED` 沒有 `WHEN NOT MATCHED` 時，新 key 不會被加入。

### 資料檔案最佳化

| 指令 | 作用 |
| --- | --- |
| `OPTIMIZE t` | 把小檔案合併成大檔 (compaction)，解決 small file problem |
| `OPTIMIZE t WHERE date >= '2026-01-01'` | 只整理部分資料；`WHERE` 只能用 partition 欄位 |
| `OPTIMIZE t ZORDER BY (col)` | 讓常用篩選欄位相近的值放在相同檔案，提高 data skipping |
| `ALTER TABLE t CLUSTER BY (col)` | liquid clustering：新表建議的做法，取代 partition + Z-order，可隨查詢模式調整 |
| `VACUUM t` | 刪除不再被參照的舊檔（影響 time travel） |

lakehouse 上的 SQL 效能不只取決於查詢寫法，也取決於資料檔案的形狀。

### 何時用 Databricks SQL

| 適合 | 改用 cluster / notebook |
| --- | --- |
| 團隊以 SQL 為共同語言 | 通用 Spark 程式、大量自訂處理 |
| 已在 lakehouse 內，需要 BI、查詢與部分轉換 | notebook-first 的工程與 ML |
| 想保留開放的 table 格式而非封閉 warehouse | |
