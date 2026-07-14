# Data Engineering

資料工程關注的是讓資料可以被穩定地擷取、儲存、轉換與交付，而不只是把資料先「放進某個資料庫」。如果 data science 比較常聚焦在分析與建模，data engineering 更像是在建立整條資料供應鏈，確保下游拿到的資料是最新、正確、可追蹤、可擴充的。

## 建議閱讀順序

1. 先讀核心觀念：從 [Foundations](foundations.md)、[Storage and Models](storage-and-models.md)、[Ingestion](ingestion.md)、[Processing and Pipelines](processing-and-pipelines.md) 建立資料流的基本語言。
2. 再讀資料模型：用 [Data Modeling Foundations](data-modeling-foundations.md) 與 [Dimensional Modeling and Star Schema](dimensional-modeling-and-star-schema.md) 建立分析資料表設計能力。
3. 再補可擴展與治理：讀 [Scalable Processing and Out-of-Core Workflows](scalable-processing-and-out-of-core.md)、[Governance](governance.md)、[Data Versioning and DVC](data-versioning-and-dvc.md)。
4. 接著選平台路線：如果偏資料平台，走 Spark / Databricks / warehouse；如果偏 BI 交付，走 Fabric / Power BI；如果偏即時資料流，再看 Kafka / Kinesis。

## 主題分組

### 核心觀念與管線基礎

- [Foundations](foundations.md): data engineer 的角色、big data 與資料管線的基本脈絡
- [Storage and Models](storage-and-models.md): structured、semi-structured、unstructured data，以及 database、warehouse、lake 的差異
- [Ingestion](ingestion.md): 常見資料來源、flat files、JSON、web requests 與擷取時的資料型態判斷
- [Processing and Pipelines](processing-and-pipelines.md): ETL、batch vs. stream、scheduling、parallel 與 cloud processing
- [ETL](etl.md): 從商業需求拆出 extract / transform / load，並把一次性處理變成可重跑流程

### 資料建模與治理

- [Data Modeling Foundations](data-modeling-foundations.md): entity / attribute / relationship、cardinality、primary / foreign key 與 normalization 的上游設計基礎
- [Dimensional Modeling and Star Schema](dimensional-modeling-and-star-schema.md): medallion 到 gold layer、fact / dimension、SCD 與特殊維度設計
- [Governance](governance.md): data catalog、lineage、access control、encryption 與合規
- [Data Versioning and DVC](data-versioning-and-dvc.md): data lineage、reproducibility、`params.yaml`、`dvc.yaml` 與資料版本管理

### 可擴展處理與分散式工作流

- [Scalable Processing and Out-of-Core Workflows](scalable-processing-and-out-of-core.md): RAM 限制、disk-backed structures、chunk-wise processing 與 split-apply-combine
- [Spark and PySpark](spark-and-pyspark.md): Spark 的分散式處理心智模型、RDD、DataFrame、partition 與 PySpark 的基本入口
- [Spark SQL in PySpark](spark-sql-in-pyspark.md): `spark.sql()`、temp view、window functions、文字 ETL 與 Spark 內部 SQL 工作流
- [Spark with sparklyr](sparklyr.md): `spark_connect()`、`compute()` / `collect()`、`DBI` SQL、`sdf_` / `ft_` / `ml_` 與 R 介面的 Spark workflow
- [Scala Foundations](scala-foundations.md): Scala 的語言定位、腳本 vs 應用程式、靜態型別與 Spark / JVM 生態的關聯

### 資料平台與雲端 Warehouse

- [Databricks Foundations](databricks-foundations.md): lakehouse 平台心智模型、Delta、Unity Catalog、clusters、SQL warehouses 與 workspace 治理
- [Databricks Data Management](databricks-data-management.md): Delta table lifecycle、time travel、managed vs unmanaged tables、views 與敏感資料治理
- [Databricks SQL](databricks-sql.md): SQL warehouse、lakehouse-style querying、SQL ingestion、`MERGE`、`OPTIMIZE` 與 `Z-ORDER`
- [dbt Foundations](dbt-foundations.md): dbt project 結構、`profiles.yml`、models、`dbt run`、`ref()`、documentation 與 lineage
- [BigQuery Foundations](bigquery-foundations.md): serverless warehouse 心智模型、`project.dataset.table`、region 限制、資料載入與 query optimization
- [Snowflake Foundations](snowflake-foundations.md): Snowflake 架構、virtual warehouse、roles、marketplace / stage 與 query / copy history
- [Redshift Foundations](redshift-foundations.md): distributed columnar warehouse、`DISTKEY` / `SORTKEY`、distribution styles、external schemas 與 tuning views

### BI 與語意層交付

- [Microsoft Fabric Fundamentals](microsoft-fabric-fundamentals.md): lakehouse、dataflow / pipeline / notebook、semantic model 與 Power BI 在 Fabric 中的整體關係
- [Microsoft Fabric Environment Design and Deployment](microsoft-fabric-environment-design-and-deployment.md): workspace、capacity、Git integration、deployment stages 與 Fabric 平台生命周期管理
- [Power BI Overview](power-bi-overview.md): Desktop / Service、Power Query Editor、views、filter scope、互動式視覺化與報表工作流
- [Power BI Service for End Users](power-bi-service-for-end-users.md): workspace、apps、sharing、alerts、permissions 與 end-user analysis workflow
- [Data Connections in Power BI](data-connections-in-power-bi.md): data sources、`Import` / `DirectQuery` / `Live`、parameters、gateway 與 incremental refresh
- [Data Preparation in Power BI](data-preparation-in-power-bi.md): Power Query、`Applied Steps`、preview features 與文字 / 數值 / 日期欄位清理
- [Data Transformation in Power BI](data-transformation-in-power-bi.md): pivot / unpivot、append / merge、custom columns、`M language` 與 Advanced Editor
- [Semantic Models and Power BI](semantic-models-and-power-bi.md): semantic layer、relationships、row/object-level security 與報表消費層
- [DAX in Power BI](dax-in-power-bi.md): context、calculated columns vs measures、`CALCULATE()` 與模型層計算心智模型
- [Report Design in Power BI](report-design-in-power-bi.md): progressive disclosure、themes、bookmarks、mobile layout 與報表 UX
- [Reports in Power BI](reports-in-power-bi.md): dashboards vs reports、bookmark state、navigation、custom tooltips 與 Q&A

### BI 案例與實務延伸

- [Financial Analysis in Power BI](financial-analysis-in-power-bi.md): financial dashboard、KPI / OKR、scenario analysis、forecasting 與 capital budgeting 指標在 Power BI 中的落地方式
- [Customer Churn Analysis in Power BI](customer-churn-analysis-in-power-bi.md): churn 定義、snapshot data 限制、segment drill-down 與 stakeholder-facing report narrative
- [HR Analytics in Power BI](hr-analytics-in-power-bi.md): workforce KPI、attrition、metadata、fact/dimension grain 與 HR dashboard 的敏感解讀邊界
- [Python in Power BI](python-in-power-bi.md): Power Query 與 Python 的分工、missing data、Seaborn、correlation 與 Power BI 內的 Python workflow
- [Trend Analysis in Power BI](trend-analysis-in-power-bi.md): time series、MoM change、rolling average、anomalies、decomposition tree 與 key influencers

### 串流與即時資料

- [Streaming and Kafka](streaming-and-kafka.md): event streaming、topic / partition、producer / consumer、replication 與 Kafka 的實務定位
- [AWS Streaming with Kinesis and Lambda](aws-streaming-with-kinesis-and-lambda.md): Kinesis、Firehose、Lambda、serverless transformation 與即時警示流程

## Why It Matters

- 分析做得再好，如果資料沒有穩定進來、格式不一致，模型和報表都會失效。
- 許多團隊的瓶頸不是演算法，而是資料延遲、品質不穩、欄位定義混亂、流程無法重跑。
- 資料工程的核心價值是把一次性的資料處理，變成可以自動化、監控、擴充的系統。

[Back to Data Science](../README.md)
