# Data Engineering

資料工程關注的是讓資料可以被穩定地擷取、儲存、轉換與交付，而不只是把資料先「放進某個資料庫」。如果 data science 比較常聚焦在分析與建模，data engineering 更像是在建立整條資料供應鏈，確保下游拿到的資料是最新、正確、可追蹤、可擴充的。

## Topics

- [Foundations](foundations.md): data engineer 的角色、big data 與資料管線的基本脈絡
- [Storage and Models](storage-and-models.md): structured、semi-structured、unstructured data，以及 database、warehouse、lake 的差異
- [Data Modeling Foundations](data-modeling-foundations.md): entity / attribute / relationship、cardinality、primary / foreign key 與 normalization 的上游設計基礎
- [Dimensional Modeling and Star Schema](dimensional-modeling-and-star-schema.md): medallion 到 gold layer、fact / dimension、SCD 與特殊維度設計
- [Scalable Processing and Out-of-Core Workflows](scalable-processing-and-out-of-core.md): RAM 限制、disk-backed structures、chunk-wise processing 與 split-apply-combine
- [Governance](governance.md): data catalog、lineage、access control、encryption 與合規
- [Ingestion](ingestion.md): 常見資料來源、flat files、JSON、web requests 與擷取時的資料型態判斷
- [Processing and Pipelines](processing-and-pipelines.md): ETL、batch vs. stream、scheduling、parallel 與 cloud processing
- [Microsoft Fabric Fundamentals](microsoft-fabric-fundamentals.md): lakehouse、dataflow / pipeline / notebook、semantic model 與 Power BI 在 Fabric 中的整體關係
- [Microsoft Fabric Environment Design and Deployment](microsoft-fabric-environment-design-and-deployment.md): workspace、capacity、Git integration、deployment stages 與 Fabric 平台生命周期管理
- [DAX in Power BI](dax-in-power-bi.md): context、calculated columns vs measures、`CALCULATE()` 與模型層計算心智模型
- [Power BI Overview](power-bi-overview.md): Desktop / Service、Power Query Editor、views、filter scope、互動式視覺化與報表工作流
- [Power BI Service for End Users](power-bi-service-for-end-users.md): workspace、apps、sharing、alerts、permissions 與 end-user analysis workflow
- [Financial Analysis in Power BI](financial-analysis-in-power-bi.md): financial dashboard、KPI / OKR、scenario analysis、forecasting 與 capital budgeting 指標在 Power BI 中的落地方式
- [Customer Churn Analysis in Power BI](customer-churn-analysis-in-power-bi.md): churn 定義、snapshot data 限制、segment drill-down 與 stakeholder-facing report narrative
- [HR Analytics in Power BI](hr-analytics-in-power-bi.md): workforce KPI、attrition、metadata、fact/dimension grain 與 HR dashboard 的敏感解讀邊界
- [Python in Power BI](python-in-power-bi.md): Power Query 與 Python 的分工、missing data、Seaborn、correlation 與 Power BI 內的 Python workflow
- [Trend Analysis in Power BI](trend-analysis-in-power-bi.md): time series、MoM change、rolling average、anomalies、decomposition tree 與 key influencers
- [Data Connections in Power BI](data-connections-in-power-bi.md): data sources、`Import` / `DirectQuery` / `Live`、parameters、gateway 與 incremental refresh
- [Data Preparation in Power BI](data-preparation-in-power-bi.md): Power Query、`Applied Steps`、preview features 與文字 / 數值 / 日期欄位清理
- [Data Transformation in Power BI](data-transformation-in-power-bi.md): pivot / unpivot、append / merge、custom columns、`M language` 與 Advanced Editor
- [Report Design in Power BI](report-design-in-power-bi.md): progressive disclosure、themes、bookmarks、mobile layout 與報表 UX
- [Reports in Power BI](reports-in-power-bi.md): dashboards vs reports、bookmark state、navigation、custom tooltips 與 Q&A
- [Semantic Models and Power BI](semantic-models-and-power-bi.md): semantic layer、relationships、row/object-level security 與報表消費層
- [Spark and PySpark](spark-and-pyspark.md): Spark 的分散式處理心智模型、RDD、DataFrame、partition 與 PySpark 的基本入口
- [Spark with sparklyr](sparklyr.md): `spark_connect()`、`compute()` / `collect()`、`DBI` SQL、`sdf_` / `ft_` / `ml_` 與 R 介面的 Spark workflow
- [Spark SQL in PySpark](spark-sql-in-pyspark.md): `spark.sql()`、temp view、window functions、文字 ETL 與 Spark 內部 SQL 工作流
- [Databricks Foundations](databricks-foundations.md): lakehouse 平台心智模型、Delta、Unity Catalog、clusters、SQL warehouses 與 workspace 治理
- [Databricks Data Management](databricks-data-management.md): Delta table lifecycle、time travel、managed vs unmanaged tables、views 與敏感資料治理
- [Databricks SQL](databricks-sql.md): SQL warehouse、lakehouse-style querying、SQL ingestion、`MERGE`、`OPTIMIZE` 與 `Z-ORDER`
- [Scala Foundations](scala-foundations.md): Scala 的語言定位、腳本 vs 應用程式、靜態型別與 Spark / JVM 生態的關聯
- [dbt Foundations](dbt-foundations.md): dbt project 結構、`profiles.yml`、models、`dbt run`、`ref()`、documentation 與 lineage
- [BigQuery Foundations](bigquery-foundations.md): serverless warehouse 心智模型、`project.dataset.table`、region 限制、資料載入與 query optimization
- [Snowflake Foundations](snowflake-foundations.md): Snowflake 架構、virtual warehouse、roles、marketplace / stage 與 query / copy history
- [Redshift Foundations](redshift-foundations.md): distributed columnar warehouse、`DISTKEY` / `SORTKEY`、distribution styles、external schemas 與 tuning views
- [Streaming and Kafka](streaming-and-kafka.md): event streaming、topic / partition、producer / consumer、replication 與 Kafka 的實務定位
- [AWS Streaming with Kinesis and Lambda](aws-streaming-with-kinesis-and-lambda.md): Kinesis、Firehose、Lambda、serverless transformation 與即時警示流程
- [Data Versioning and DVC](data-versioning-and-dvc.md): data lineage、reproducibility、`params.yaml`、`dvc.yaml` 與資料版本管理
- [ETL](etl.md): 從商業需求拆出 extract / transform / load，並把一次性處理變成可重跑流程

## Why It Matters

- 分析做得再好，如果資料沒有穩定進來、格式不一致，模型和報表都會失效。
- 許多團隊的瓶頸不是演算法，而是資料延遲、品質不穩、欄位定義混亂、流程無法重跑。
- 資料工程的核心價值是把一次性的資料處理，變成可以自動化、監控、擴充的系統。

## Practical Reading Order

1. 先看 [Foundations](foundations.md)，建立角色分工與 pipeline 思維。
2. 再看 [Storage and Models](storage-and-models.md)，理解不同資料型態該放在哪裡。
3. 再看 [Data Modeling Foundations](data-modeling-foundations.md)，先把 entity、relationship、keys 與 normalization 的上游設計語言建立起來。
4. 接著看 [Dimensional Modeling and Star Schema](dimensional-modeling-and-star-schema.md)，理解 gold layer 常見的分析模型應該長什麼樣子。
5. 再看 [Scalable Processing and Out-of-Core Workflows](scalable-processing-and-out-of-core.md)，理解當資料放不進 RAM 時應該怎麼重新設計處理流程。
6. 再看 [Governance](governance.md)，理解資料不是能存就好，還要能被控管、追蹤與保護。
7. 再看 [Ingestion](ingestion.md)，理解資料究竟從哪些地方進來、該怎麼讀。
8. 接著看 [Processing and Pipelines](processing-and-pipelines.md)，把資料移動、轉換、排程與運算串起來。
9. 先看 [Microsoft Fabric Fundamentals](microsoft-fabric-fundamentals.md)，理解 lakehouse、pipeline、notebook、semantic model 與 Power BI 在同一平台中的關係。
10. 再看 [Microsoft Fabric Environment Design and Deployment](microsoft-fabric-environment-design-and-deployment.md)，理解整合式分析平台中的 workspace、capacity、Git、deployment 與效能治理。
11. 再看 [Power BI Overview](power-bi-overview.md)，理解 Desktop / Service、Power Query Editor、report interactions 與 BI 消費層的基本工作流。
12. 再看 [Power BI Service for End Users](power-bi-service-for-end-users.md)，理解 workspace、apps、sharing、alerts、permissions 與 end-user exploration workflow。
13. 再看 [Financial Analysis in Power BI](financial-analysis-in-power-bi.md)，理解 financial dashboard、scenario analysis、forecasting 與資本配置指標如何被做成互動式分析。
14. 再看 [Customer Churn Analysis in Power BI](customer-churn-analysis-in-power-bi.md)，理解 churn 定義、snapshot data 限制、segment drill-down 與報表敘事安排。
15. 再看 [HR Analytics in Power BI](hr-analytics-in-power-bi.md)，理解 workforce KPI、attrition、metadata 與 HR 報表中的 grain / governance 問題。
16. 再看 [Python in Power BI](python-in-power-bi.md)，理解 Power Query / Quick Measures 與 `pandas` / `seaborn` 的分工邊界。
17. 再看 [Trend Analysis in Power BI](trend-analysis-in-power-bi.md)，理解 time series、period-over-period comparison、rolling average、anomalies 與 explanation visuals。
18. 再看 [Data Connections in Power BI](data-connections-in-power-bi.md)，理解 data sources、storage modes、parameters、gateway 與 refresh strategy。
19. 再看 [Data Preparation in Power BI](data-preparation-in-power-bi.md)，理解 Power Query、`Applied Steps`、preview features 與欄位清理的實務心智模型。
20. 再看 [Data Transformation in Power BI](data-transformation-in-power-bi.md)，理解 pivot / unpivot、append / merge、custom columns、`M language` 與 Advanced Editor。
21. 再看 [Report Design in Power BI](report-design-in-power-bi.md)，理解 progressive disclosure、themes、bookmarks、mobile layout 與報表層 UX 心法。
22. 再看 [Reports in Power BI](reports-in-power-bi.md)，理解 dashboards vs reports、bookmark state、navigation、custom tooltips 與 Q&A。
23. 再看 [Semantic Models and Power BI](semantic-models-and-power-bi.md)，理解資料整理完成後如何被建成可分析、可控管的語意層。
24. 再看 [DAX in Power BI](dax-in-power-bi.md)，理解 context、measures、`CALCULATE()`、日期欄位與 period comparison 的模型層心智模型。
25. 再看 [Spark and PySpark](spark-and-pyspark.md)，理解分散式資料處理、RDD 與 DataFrame 的基本模型。
26. 再看 [Spark with sparklyr](sparklyr.md)，理解 R 使用者如何透過 `dplyr`、SQL 與 `ml_` / `ft_` 介面接上 Spark。
27. 接著看 [Spark SQL in PySpark](spark-sql-in-pyspark.md)，理解 `spark.sql()`、temp views、window functions 與 Spark 內部 SQL workflow。
28. 再看 [Databricks Foundations](databricks-foundations.md)，理解 lakehouse 平台如何把 Delta、catalog、clusters、SQL warehouse 與 notebook 工作流組在一起。
29. 再看 [Databricks Data Management](databricks-data-management.md)，理解 Delta table lifecycle、table persistence、views 與權限治理怎麼落到實際資料資產上。
30. 再看 [Databricks SQL](databricks-sql.md)，理解 SQL warehouse、SQL-based ingestion、Delta table maintenance 與 analyst-facing query workflow。
31. 再看 [Scala Foundations](scala-foundations.md)，理解 Spark 背後常見的 JVM / Scala 脈絡，以及腳本、編譯與靜態型別的設計取向。
32. 再看 [dbt Foundations](dbt-foundations.md)，理解 warehouse 內轉換如何被工程化、版本化與文件化。
33. 再看 [BigQuery Foundations](bigquery-foundations.md)，理解 serverless warehouse 的資料層級、region 邊界與成本導向查詢設計。
34. 再看 [Snowflake Foundations](snowflake-foundations.md)，理解 cloud warehouse 中 compute / storage 分離、role hierarchy、micro-partitions 與 external loading workflow。
35. 再看 [Redshift Foundations](redshift-foundations.md)，理解 distributed warehouse 中資料分布、sort order 與 AWS 生態整合的調校重點。
36. 再看 [Streaming and Kafka](streaming-and-kafka.md)，理解事件流與批次資料流在系統設計上的差異。
37. 接著看 [AWS Streaming with Kinesis and Lambda](aws-streaming-with-kinesis-and-lambda.md)，把串流觀念映射到一個常見的 cloud-native 實作。
38. 再看 [Data Versioning and DVC](data-versioning-and-dvc.md)，理解資料、參數與實驗輸出如何被版本化與重現。
39. 最後看 [ETL](etl.md)，把前面的概念收斂成一個可運作的資料流程視角。

[Back to Data Science](../README.md)
