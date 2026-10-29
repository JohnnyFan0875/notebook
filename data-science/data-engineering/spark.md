[Data Science](../README.md) › [Data Engineering](README.md) › Spark 與 PySpark

# Spark 與 PySpark

Apache Spark 是分散式資料處理引擎：把資料切成 partition 分散到多台機器，以 lazy evaluation 最佳化整條計算再執行。前半是 PySpark 的核心模型（RDD、DataFrame、清理、特徵工程），後半是 Spark SQL。R 介面見 [sparklyr](sparklyr.md)；基因體資料見 [Spark 處理基因體資料](spark-for-genomics.md)；單機放不下但不需要叢集時先看 [超出記憶體的處理](scalable-processing-and-out-of-core.md)。

## 什麼時候需要 Spark

| 適合 | 不適合 |
| --- | --- |
| 資料量或運算超過單機能處理的範圍（數百 GB 以上） | 資料放得進單機：pandas / Polars / DuckDB 更快更簡單 |
| ETL 需要平行化、資料在 HDFS / S3 / Delta | 團隊沒有叢集維運能力、只是偶爾跑一次 |
| 想把 SQL、轉換、部分 ML 放在同一平台 | 需要低延遲的單筆查詢（用資料庫） |

| 名詞 | 意義 |
| --- | --- |
| Cluster computing | 多台機器的資源一起工作 |
| Parallel computing | 同時做多個計算 |
| Distributed computing | 網路上的多個節點合作完成任務 |

| 系統 | 特性 |
| --- | --- |
| Hadoop MapReduce | 可擴充、容錯；每步寫回磁碟，偏傳統 batch |
| Apache Spark | 記憶體內運算、較高階的 API；batch、SQL、streaming、ML 同一生態；支援 Python、Scala、Java、R、SQL |

## 執行架構

```
Driver（你的程式、SparkSession、規劃 DAG）
   │  切成 stages / tasks
   ├── Executor 1：處理 partition 1, 4, ...
   ├── Executor 2：處理 partition 2, 5, ...
   └── Executor 3：...
```

| 概念 | 意義 | 影響 |
| --- | --- | --- |
| Partition | 資料的邏輯切分單位，一個 task 處理一個 | 決定平行度；太少用不滿核心，太多 overhead 大 |
| Transformation | 產生新的 DataFrame / RDD（`select`、`filter`、`join`） | lazy：只記錄步驟 |
| Action | 觸發計算或回傳結果（`count`、`show`、`collect`、`write`） | 真正執行 |
| Narrow vs wide | narrow（`filter`、`select`）不需搬資料；wide（`groupBy`、`join`、`orderBy`）需要 shuffle | shuffle 是最主要的效能成本 |

lazy evaluation 讓 Spark 把多個步驟合併、把篩選推到讀取階段 (predicate pushdown)、只讀需要的欄。代價是錯誤常在 action 時才出現，而且同一個 DataFrame 被多次 action 會重算整條鏈。

| 模式 | 用途 |
| --- | --- |
| Local mode | 單機，測試、除錯、原型 |
| Cluster mode | 多台機器（YARN、Kubernetes、Databricks），正式資料 |

程式通常不必大改就能從 local 搬到 cluster。

## 入口：SparkSession

```python
from pyspark.sql import SparkSession

spark = (SparkSession.builder
         .appName("expr-etl")
         .config("spark.sql.shuffle.partitions", "200")   # shuffle 後的 partition 數
         .getOrCreate())                                   # 已有 session 就重用
sc = spark.sparkContext                                    # RDD 世界的入口（較少直接用）
spark.version
```

`SparkContext`（`sc`）是傳統的 RDD 入口；`SparkSession`（`spark`）是 DataFrame 與 SQL 的入口，現代工作流都從這裡開始。

## RDD vs DataFrame

| 面向 | RDD (Resilient Distributed Dataset) | DataFrame |
| --- | --- | --- |
| 抽象層級 | 低：分散的 Python 物件集合 | 高：有 schema、具名欄位的分散表格 |
| 最佳化 | 幾乎沒有（Spark 看不懂你的 lambda） | Catalyst 最佳化器 + Tungsten 執行 |
| Python 效能 | 資料要在 JVM 與 Python 間序列化，慢 | 內建函式在 JVM 執行，快 |
| 用途 | 理解分散式模型、特殊低階處理 | ETL、分析、特徵整理、SQL |

```python
# RDD：了解即可
rdd = sc.parallelize(range(10), numSlices=4)
rdd.map(lambda x: x * x).filter(lambda x: x % 2 == 0).collect()   # [0, 4, 16, 36, 64]
rdd.getNumPartitions()                                             # 4
```

## 讀取與 schema

```python
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

schema = StructType([
    StructField("sample_id", StringType(), nullable=False),
    StructField("gene", StringType(), nullable=False),
    StructField("count", IntegerType(), nullable=True),
    StructField("tpm", DoubleType(), nullable=True),
])

df = spark.read.csv("expr/*.csv.gz", header=True, schema=schema, comment="#")
# 沒給 schema 也沒 inferSchema=True 時，所有欄位都是字串
df = spark.read.parquet("expr_parquet/")        # Parquet 自帶 schema，最常用
df = spark.read.json("events.jsonl")            # 每行一筆 JSON

df.printSchema(); df.columns; df.count(); df.show(5); df.describe("tpm").show()
```

| 明確定義 schema 的好處 | 不定義的代價 |
| --- | --- |
| 讀取快（不必掃一遍推斷型別） | `inferSchema` 要多掃一次資料 |
| 一開始就擋下格式不對的資料 | 錯誤延後到下游才出現 |
| ID 欄保持字串（`"001"` 不變 `1`） | 型別推斷因檔案而異 |

> 中間結果寫成 Parquet 後，下游不必再猜 schema；這通常比 `cache()` 更穩。

## DataFrame 常用操作與清理

```python
from pyspark.sql import functions as F

clean = (df
    .where(F.col("gene").isNotNull())
    .dropDuplicates(["sample_id", "gene"])                     # 不保證保留哪一筆
    .withColumn("gene", F.upper(F.trim("gene")))
    .withColumn("log_tpm", F.log2(F.col("tpm") + 1))
    .withColumn("expressed", F.when(F.col("tpm") > 1, 1).otherwise(0))
    .withColumnRenamed("count", "raw_count")
    .na.fill({"raw_count": 0})                                  # 依欄位補值；na.drop() 丟掉含 null 的列
    .drop("tpm"))

# 字串與陣列
parts = df.withColumn("fields", F.split("info", ";"))
parts.select(F.size("fields").alias("n"), F.col("fields").getItem(0).alias("first"))

# 聚合與 join
per_gene = clean.groupBy("gene").agg(F.mean("log_tpm").alias("mean_log_tpm"),
                                     F.countDistinct("sample_id").alias("n_samples"))
annotated = clean.join(F.broadcast(meta), on="sample_id", how="left")   # 小表 broadcast，避免 shuffle
```

| 原則 | 理由 |
| --- | --- |
| 能用 `pyspark.sql.functions` 就不要寫 Python UDF | UDF 要把資料序列化到 Python，慢且無法最佳化 |
| 非寫 UDF 不可時用 pandas UDF（`@F.pandas_udf`） | 以 Arrow 批次傳輸，比逐列 UDF 快很多 |
| `dropDuplicates()` 前先定義保留規則 | 重複列品質不同時，用 `ROW_NUMBER()` 依規則保留 |
| join 後檢查列數 | key 不唯一時列數膨脹，不會報錯 |
| 不要對大表 `collect()` / `toPandas()` | 把分散的資料全拉回 driver，常直接記憶體不足 |

### 快取 (Caching)

```python
clean.cache()          # 標記要保留（lazy）
clean.count()          # 第一次 action 才 materialize
clean.is_cached        # True
clean.unpersist()      # 用完釋放
```

只有同一份中間結果會被多次 action 或多個分支重用、重算成本高時才值得快取。`cache()` 不是鎖定記憶體：記憶體壓力大時各 worker 會以類似 LRU 的方式逐出。資料太大或只能落到慢磁碟時，寫成 Parquet 再讀回通常更穩定。

## 特徵工程與 MLlib

| 步驟 | 工具 |
| --- | --- |
| 確認環境、抽查欄位 | `spark.version`、`select().show()` |
| 去重、移除常數 / 錯誤欄 | `dropDuplicates()`、`drop()` |
| 缺值診斷 | `F.sum(F.col(c).isNull().cast("int"))`；或 `sample()` 一小部分轉 pandas 畫 heatmap |
| 衍生特徵 | `withColumn()` 算術、`F.log()` 處理偏態 |
| 二元化 / 分箱 | `Binarizer`、`Bucketizer`、`QuantileDiscretizer` |
| 類別編碼 | `StringIndexer` → `OneHotEncoder` |
| 組成特徵向量 | `VectorAssembler`（MLlib 模型需要單一 `features` 欄） |

```python
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator

pipe = Pipeline(stages=[
    StringIndexer(inputCol="tissue", outputCol="tissue_idx", handleInvalid="keep"),
    OneHotEncoder(inputCols=["tissue_idx"], outputCols=["tissue_ohe"]),
    VectorAssembler(inputCols=["age", "mean_log_tpm", "tissue_ohe"], outputCol="raw"),
    StandardScaler(inputCol="raw", outputCol="features"),
    LogisticRegression(labelCol="label", featuresCol="features"),
])

# 有時間軸時依時間切，而不是 randomSplit，避免時間洩漏
cutoff = "2025-01-01"
train, test = data.where(F.col("date") < cutoff), data.where(F.col("date") >= cutoff)

model = pipe.fit(train)                 # 編碼與標準化參數只從訓練集學
pred = model.transform(test)
BinaryClassificationEvaluator(labelCol="label").evaluate(pred)    # 預設 areaUnderROC
```

把轉換放進 `Pipeline` 的價值在於訓練與推論用同一套邏輯，而且參數只從訓練集學到，避免 [資料洩漏](../machine-learning/foundations/data-leakage.md)。MLlib 不見得比 scikit-learn 好，它的優勢是在叢集上處理單機放不下的資料，並與 Spark 的資料處理接在一起；資料聚合到放得進記憶體後，轉 pandas 用 scikit-learn 通常更方便。

## Spark SQL

Spark SQL 把 DataFrame 與 SQL 接起來：`spark.sql()` 與 DataFrame API 在同一個執行引擎上，經過同一個最佳化器，效能相同。用哪個看哪一段寫起來最清楚。

```python
df.createOrReplaceTempView("schedule")          # temp view：session 內的 SQL 別名

spark.sql("SHOW COLUMNS FROM schedule").show()
spark.sql("DESCRIBE schedule").show()           # 欄名與型別，不必拉資料

result = spark.sql("""
    SELECT train_id, station, time,
           ROW_NUMBER() OVER (PARTITION BY train_id ORDER BY time)  AS stop_no,
           LEAD(time, 1) OVER (PARTITION BY train_id ORDER BY time) AS time_next
    FROM schedule
    WHERE station IS NOT NULL
""")

# SQL 與 DataFrame API 混用
result.where("stop_no <= 3").groupBy("train_id").count()
```

同樣的 window 用 DataFrame API：

```python
from pyspark.sql import Window

w = Window.partitionBy("train_id").orderBy("time")
df = (df.withColumn("stop_no", F.row_number().over(w))
        .withColumn("time_next", F.lead("time", 1).over(w)))
```

| SQL | PySpark |
| --- | --- |
| `OVER (PARTITION BY a ORDER BY b)` | `Window.partitionBy("a").orderBy("b")` |
| `ROW_NUMBER()`、`LAG()`、`LEAD()` | `F.row_number()`、`F.lag()`、`F.lead()` |
| `CASE WHEN ... THEN ... ELSE ... END` | `F.when(...).otherwise(...)` |

window 的細節（frame、`RANGE` 陷阱、每組 top-N）見 [Window Functions](../databases/sql-window-functions.md)。

### 文字處理

```python
text = spark.read.text("sherlock.txt")          # 單欄 value，每列是原檔一行
words = (text
    .select(F.lower("value").alias("v"))
    .select(F.regexp_replace("v", r"[^a-z\s]", "").alias("v"))
    .select(F.explode(F.split("v", r"\s+")).alias("word"))
    .where(F.col("word") != ""))
words.groupBy("word").count().orderBy(F.desc("count")).show(10)
```

保持在 DataFrame 內用內建函式逐步轉換，最後才聚合。

### Spark SQL vs Databricks SQL

| | Spark SQL | Databricks SQL |
| --- | --- | --- |
| 層次 | Spark 引擎內的查詢介面 | Databricks 平台上的 SQL-first 分析層 |
| 用法 | notebook / PySpark 中的 `spark.sql()` | SQL warehouse、dashboard、BI 連線、表維護 |

見 [Databricks](databricks.md#databricks-sql)。

## 效能檢查清單

| 症狀 | 可能原因 | 做法 |
| --- | --- | --- |
| 某幾個 task 特別久 | data skew：少數 key 資料特別多 | 對熱門 key 加鹽 (salting)、開啟 AQE skew join |
| shuffle 量很大 | 大表對大表 join、多次 `groupBy` | 小表 `broadcast()`；先篩選再 join |
| 大量小檔案 | 每個 partition 寫一個檔 | 寫出前 `coalesce()` / `repartition()` |
| 同一段重算很多次 | 多次 action、沒有快取 | `cache()` 或寫出中間 Parquet |
| driver 記憶體不足 | `collect()` / `toPandas()` 大表 | 在 Spark 內聚合，只拉回小結果 |
| Python UDF 很慢 | 逐列序列化 | 改用內建函式或 pandas UDF |

用 `df.explain()` 看執行計畫，Spark UI（預設 `localhost:4040`）看各 stage 的時間與 shuffle 量。Spark 3 起預設開啟 Adaptive Query Execution (AQE)，會在執行中自動合併小 partition、處理 skew join。
