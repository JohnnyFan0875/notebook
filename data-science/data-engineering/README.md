# Data Engineering

資料工程關注的是讓資料可以被穩定地擷取、儲存、轉換與交付，而不只是把資料先「放進某個資料庫」。如果 data science 比較常聚焦在分析與建模，data engineering 更像是在建立整條資料供應鏈，確保下游拿到的資料是最新、正確、可追蹤、可擴充的。

## 建議閱讀順序

1. 先讀核心觀念：從 [Foundations](foundations.md)、[Storage and Models](storage-and-models.md)、[Ingestion](ingestion.md)、[Processing and Pipelines](processing-and-pipelines.md) 建立資料流的基本語言。
2. 再讀資料模型：用 [Data Modeling Foundations](data-modeling-foundations.md) 與 [Data Warehousing and Dimensional Modeling](dimensional-modeling-and-star-schema.md) 建立分析資料表設計能力。
3. 再補可擴展、品質與治理：讀 [Scalable Processing and Out-of-Core Workflows](scalable-processing-and-out-of-core.md)、[Data Quality Checks](data-quality-checks.md)、[Data Governance](governance.md)、[Data Versioning and DVC](../machine-learning/production/dvc.md)。
4. 接著選平台路線：偏資料平台走 [Spark](spark.md) / [Databricks](databricks.md) / [Cloud Data Warehouses](cloud-data-warehouses.md)；偏即時資料流看 [Streaming](streaming.md)；偏 BI 交付看 [BI Tools](../data-communication/bi-tools/README.md)。

## 主題分組

### 核心觀念與管線基礎

- [Foundations](foundations.md): data engineer 的角色、big data 與資料管線的基本脈絡
- [Storage and Models](storage-and-models.md): structured、semi-structured、unstructured data，以及 database、warehouse、lake 的差異
- [Ingestion](ingestion.md): 常見資料來源、flat files、JSON、web requests 與擷取時的資料型態判斷
- [Processing and Pipelines](processing-and-pipelines.md): ETL / ELT 三階段、batch vs. stream、scheduling vs orchestration、pipeline testing、parallel 與 cloud processing

### 資料建模、品質與治理

- [Data Modeling Foundations](data-modeling-foundations.md): entity / attribute / relationship、cardinality、primary / foreign key、ER modeling（正規化見 [Database Normalization](../databases/database-normalization.md)）
- [Data Warehousing and Dimensional Modeling](dimensional-modeling-and-star-schema.md): warehouse vs lake / mart、分層、Inmon vs Kimball、medallion 到 gold layer、fact / dimension、SCD、OLAP vs OLTP、ETL vs ELT
- [Data Quality Checks](data-quality-checks.md): 品質維度、detective vs preventative rules、閾值與告警、remediation，以及用 Great Expectations 寫成可執行檢查
- [Data Governance](governance.md): data catalog、lineage、access control、encryption、分類標籤，以及治理計畫的角色、策略與衡量
- [Data Versioning and DVC](../machine-learning/production/dvc.md): data lineage、reproducibility、`params.yaml`、`dvc.yaml` 與資料版本管理

### 可擴展處理與分散式工作流

- [Scalable Processing and Out-of-Core Workflows](scalable-processing-and-out-of-core.md): RAM 限制、disk-backed structures、chunk-wise processing 與 split-apply-combine
- [Spark and PySpark](spark.md): 分散式處理心智模型、RDD、DataFrame、partition、清理與特徵工程，以及 Spark SQL（`spark.sql()`、temp view、window functions）
- [Spark with sparklyr](sparklyr.md): `spark_connect()`、`compute()` / `collect()`、`DBI` SQL、`sdf_` / `ft_` / `ml_` 與 R 介面的 Spark workflow
- [Scala Fundamentals](../../computing/programming-languages/scala-fundamentals.md): Scala 的語言定位、腳本 vs 應用程式、靜態型別與 Spark / JVM 生態的關聯

### 資料平台與雲端 Warehouse

- [Databricks](databricks.md): lakehouse、Delta、Unity Catalog、clusters vs SQL warehouses、managed vs unmanaged tables、time travel、Databricks SQL（`MERGE`、`OPTIMIZE`、`Z-ORDER`）
- [dbt Foundations](dbt-foundations.md): dbt project 結構、`profiles.yml`、models、`dbt run`、`ref()`、documentation 與 lineage
- [Cloud Data Warehouses](cloud-data-warehouses.md): Snowflake / BigQuery / Redshift 比較表，virtual warehouse、`project.dataset.table`、`DISTKEY` / `SORTKEY` 等平台細節

### 串流與即時資料

- [Streaming](streaming.md): event streaming、Kafka 的 topic / partition / replication、Celery vs Kafka vs Spark Streaming，以及 AWS Kinesis + Firehose + Lambda

## Why It Matters

- 分析做得再好，如果資料沒有穩定進來、格式不一致，模型和報表都會失效。
- 許多團隊的瓶頸不是演算法，而是資料延遲、品質不穩、欄位定義混亂、流程無法重跑。
- 資料工程的核心價值是把一次性的資料處理，變成可以自動化、監控、擴充的系統。

[Back to Data Science](../README.md)
