# Data Engineering

資料工程關注的是讓資料可以被穩定地擷取、儲存、轉換與交付，而不只是把資料先「放進某個資料庫」。如果 data science 比較常聚焦在分析與建模，data engineering 更像是在建立整條資料供應鏈，確保下游拿到的資料是最新、正確、可追蹤、可擴充的。

## Topics

- [Foundations](foundations.md): data engineer 的角色、big data 與資料管線的基本脈絡
- [Storage and Models](storage-and-models.md): structured、semi-structured、unstructured data，以及 database、warehouse、lake 的差異
- [Dimensional Modeling and Star Schema](dimensional-modeling-and-star-schema.md): medallion 到 gold layer、fact / dimension、SCD 與特殊維度設計
- [Scalable Processing and Out-of-Core Workflows](scalable-processing-and-out-of-core.md): RAM 限制、disk-backed structures、chunk-wise processing 與 split-apply-combine
- [Governance](governance.md): data catalog、lineage、access control、encryption 與合規
- [Ingestion](ingestion.md): 常見資料來源、flat files、JSON、web requests 與擷取時的資料型態判斷
- [Processing and Pipelines](processing-and-pipelines.md): ETL、batch vs. stream、scheduling、parallel 與 cloud processing
- [Microsoft Fabric Environment Design and Deployment](microsoft-fabric-environment-design-and-deployment.md): workspace、capacity、Git integration、deployment stages 與 Fabric 平台生命周期管理
- [Semantic Models and Power BI](semantic-models-and-power-bi.md): semantic layer、relationships、row/object-level security 與報表消費層
- [Spark and PySpark](spark-and-pyspark.md): Spark 的分散式處理心智模型、RDD、DataFrame、partition 與 PySpark 的基本入口
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
3. 接著看 [Dimensional Modeling and Star Schema](dimensional-modeling-and-star-schema.md)，理解 gold layer 常見的分析模型應該長什麼樣子。
4. 再看 [Scalable Processing and Out-of-Core Workflows](scalable-processing-and-out-of-core.md)，理解當資料放不進 RAM 時應該怎麼重新設計處理流程。
5. 再看 [Governance](governance.md)，理解資料不是能存就好，還要能被控管、追蹤與保護。
6. 再看 [Ingestion](ingestion.md)，理解資料究竟從哪些地方進來、該怎麼讀。
7. 接著看 [Processing and Pipelines](processing-and-pipelines.md)，把資料移動、轉換、排程與運算串起來。
8. 再看 [Microsoft Fabric Environment Design and Deployment](microsoft-fabric-environment-design-and-deployment.md)，理解整合式分析平台中的 workspace、capacity、Git、deployment 與效能治理。
9. 再看 [Semantic Models and Power BI](semantic-models-and-power-bi.md)，理解資料整理完成後如何被建成可分析、可控管的語意層。
10. 再看 [Spark and PySpark](spark-and-pyspark.md)，理解分散式資料處理、RDD 與 DataFrame 的基本模型。
11. 再看 [Streaming and Kafka](streaming-and-kafka.md)，理解事件流與批次資料流在系統設計上的差異。
12. 接著看 [AWS Streaming with Kinesis and Lambda](aws-streaming-with-kinesis-and-lambda.md)，把串流觀念映射到一個常見的 cloud-native 實作。
13. 再看 [Data Versioning and DVC](data-versioning-and-dvc.md)，理解資料、參數與實驗輸出如何被版本化與重現。
14. 最後看 [ETL](etl.md)，把前面的概念收斂成一個可運作的資料流程視角。

[Back to Data Science](../README.md)
