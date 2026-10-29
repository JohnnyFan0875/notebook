[Data Science](../README.md) › Data Engineering

# 資料工程 (Data Engineering)

資料工程讓資料能被穩定地擷取、儲存、轉換與交付：分析與模型要能每天重跑、出錯時查得到原因，靠的是這一層。對生資與 ML 工作者最實用的部分是檔案格式、超出記憶體的處理、資料品質檢查與可重跑的 pipeline；平台（Databricks、雲端 warehouse）在需要時再讀。

## 建議順序

```
核心觀念 → 儲存與格式 → 擷取 → Pipeline
                               ↓
         資料建模 → 維度模型          大資料：out-of-core → Spark → 基因體 Spark
                               ↓
                  資料品質 → 治理          平台：Databricks / 雲端 warehouse / dbt / 串流
```

## 筆記

### 核心觀念

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [資料工程基礎](foundations.md) | 角色分工、資料生命週期、現代 vs 傳統架構 | 資料工程做什麼？什麼時候需要 pipeline？ |
| [儲存與資料模型](storage-and-models.md) | 結構化程度、database / warehouse / lake / lakehouse、Delta、檔案格式 | 資料該放哪裡、存成什麼格式？ |
| [資料擷取](ingestion.md) | 檔案、資料庫、API 來源；型別、編碼、checksum、增量擷取 | 資料進來時要先確認什麼？ |
| [處理與 Pipeline](processing-and-pipelines.md) | ETL / ELT、batch vs stream、排程與編排、冪等、測試 | 怎麼把一次性腳本變成可重跑的流程？ |

### 建模、品質與治理

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [資料建模基礎](data-modeling-foundations.md) | entity / attribute / relationship、cardinality、key、ER model | 資料表之間怎麼連？ |
| [資料倉儲與維度模型](dimensional-modeling-and-star-schema.md) | warehouse 分層、Inmon vs Kimball、medallion、star schema、grain、SCD | 分析用的表要怎麼設計？ |
| [資料品質檢查](data-quality-checks.md) | 品質維度、偵測 vs 預防規則、閾值與告警、pandera / Great Expectations | 怎麼把「資料要乾淨」變成可執行的檢查？ |
| [資料治理](governance.md) | metadata、catalog、lineage、存取控制、分類標籤、治理計畫 | 誰能用哪些資料？出錯時影響到誰？ |
| [資料版本與 DVC](../machine-learning/production/dvc.md) | 資料版本、`dvc.yaml`、`params.yaml` | 怎麼重現某次分析用的資料？ |

### 大資料處理

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [超出記憶體的處理](scalable-processing-and-out-of-core.md) | 分塊處理、split-apply-combine、可合併的部分結果、Polars / DuckDB / R 工具 | 資料大於 RAM 但不想上叢集怎麼辦？ |
| [Spark 與 PySpark](spark.md) | 分散式模型、DataFrame、lazy evaluation、清理、特徵工程、Spark SQL | 什麼時候需要 Spark？怎麼寫才不會慢？ |
| [sparklyr](sparklyr.md) | R 的 Spark 介面、`compute()` vs `collect()`、`sdf_` / `ft_` / `ml_` | R 使用者怎麼用 Spark？ |
| [Spark 處理基因體資料](spark-for-genomics.md) | Glow、Hail：讀 VCF、variant / sample QC、GWAS、PCA | 數十萬樣本的變異資料怎麼分析？ |

### 平台

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Databricks](databricks.md) | lakehouse、Delta、Unity Catalog、compute、time travel、`MERGE` / `OPTIMIZE` | Databricks 上的資料怎麼管理？ |
| [雲端資料倉儲](cloud-data-warehouses.md) | Snowflake / BigQuery / Redshift 比較、計費與效能陷阱 | 三大雲端 warehouse 差在哪？ |
| [dbt](dbt-foundations.md) | model、`ref()` / `source()`、測試、seed、snapshot、文件 | 怎麼讓 SQL 轉換可測試、可追蹤？ |
| [串流處理](streaming.md) | Kafka（topic / partition / consumer group）、Structured Streaming、AWS Kinesis + Lambda | 什麼時候真的需要即時處理？ |

## 與其他章節的關係

| 想做的事 | 去哪裡 |
| --- | --- |
| SQL 查詢、資料庫設計、DuckDB | [Databases](../databases/README.md) |
| 單機 pandas / Polars 效能 | [記憶體與儲存格式](../python-foundations/pandas/memory-and-storage.md)、[Polars](../python-foundations/performance-and-scaling/polars.md) |
| 生資 workflow（Nextflow）、Airflow 排程 | [Workflow Engines](../../computing/workflow-engines/README.md) |
| 模型部署與監控 | [MLOps](../machine-learning/production/README.md) |
| 報表與 BI 工具 | [Data Communication](../data-communication/README.md) |
| 個資、受控存取、去識別化 | [Responsible AI](../responsible-ai/README.md) |
| Scala 語言基礎 | [Scala Fundamentals](../../computing/programming-languages/scala-fundamentals.md) |
