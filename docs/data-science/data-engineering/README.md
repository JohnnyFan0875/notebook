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
- [Microsoft Fabric Environment Design and Deployment](microsoft-fabric-environment-design-and-deployment.md): workspace、capacity、Git integration、deployment stages 與 Fabric 平台生命周期管理
- [Semantic Models and Power BI](semantic-models-and-power-bi.md): semantic layer、relationships、row/object-level security 與報表消費層
- [Spark and PySpark](spark-and-pyspark.md): Spark 的分散式處理心智模型、RDD、DataFrame、partition 與 PySpark 的基本入口
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
9. 再看 [Microsoft Fabric Environment Design and Deployment](microsoft-fabric-environment-design-and-deployment.md)，理解整合式分析平台中的 workspace、capacity、Git、deployment 與效能治理。
10. 再看 [Semantic Models and Power BI](semantic-models-and-power-bi.md)，理解資料整理完成後如何被建成可分析、可控管的語意層。
11. 再看 [Spark and PySpark](spark-and-pyspark.md)，理解分散式資料處理、RDD 與 DataFrame 的基本模型。
12. 再看 [Databricks Foundations](databricks-foundations.md)，理解 lakehouse 平台如何把 Delta、catalog、clusters、SQL warehouse 與 notebook 工作流組在一起。
13. 再看 [Databricks Data Management](databricks-data-management.md)，理解 Delta table lifecycle、table persistence、views 與權限治理怎麼落到實際資料資產上。
14. 再看 [Databricks SQL](databricks-sql.md)，理解 SQL warehouse、SQL-based ingestion、Delta table maintenance 與 analyst-facing query workflow。
15. 再看 [Scala Foundations](scala-foundations.md)，理解 Spark 背後常見的 JVM / Scala 脈絡，以及腳本、編譯與靜態型別的設計取向。
16. 再看 [dbt Foundations](dbt-foundations.md)，理解 warehouse 內轉換如何被工程化、版本化與文件化。
17. 再看 [BigQuery Foundations](bigquery-foundations.md)，理解 serverless warehouse 的資料層級、region 邊界與成本導向查詢設計。
18. 再看 [Snowflake Foundations](snowflake-foundations.md)，理解 cloud warehouse 中 compute / storage 分離、role hierarchy、micro-partitions 與 external loading workflow。
19. 再看 [Redshift Foundations](redshift-foundations.md)，理解 distributed warehouse 中資料分布、sort order 與 AWS 生態整合的調校重點。
20. 再看 [Streaming and Kafka](streaming-and-kafka.md)，理解事件流與批次資料流在系統設計上的差異。
21. 接著看 [AWS Streaming with Kinesis and Lambda](aws-streaming-with-kinesis-and-lambda.md)，把串流觀念映射到一個常見的 cloud-native 實作。
22. 再看 [Data Versioning and DVC](data-versioning-and-dvc.md)，理解資料、參數與實驗輸出如何被版本化與重現。
23. 最後看 [ETL](etl.md)，把前面的概念收斂成一個可運作的資料流程視角。

[Back to Data Science](../README.md)
