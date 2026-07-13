# Spark SQL in PySpark

Spark SQL 是 Spark 裡把 DataFrame 世界和 SQL 世界接起來的那一層。它很適合這種情境：

- 你已經在 PySpark notebook 裡
- 資料是 DataFrame
- 但某些轉換、分析或 window logic 用 SQL 更直觀

Key point: Spark SQL 不是另一個獨立平台，而是建立在 Spark execution engine 上的查詢介面。`spark.sql()` 和 DataFrame API 最終是在同一個分散式運算環境裡工作。

## The Core Workflow

最典型的節奏是：

1. 用 `spark.read...` 載入 DataFrame
2. 把 DataFrame 註冊成 temp view
3. 用 `spark.sql()` 查詢
4. 拿回 DataFrame 繼續做後續轉換

```python
df = spark.read.csv("trainsched.txt", header=True)
df.createOrReplaceTempView("schedule")

result = spark.sql("""
    SELECT train_id, time
    FROM schedule
    WHERE station = 'San Jose'
""")

result.show()
```

可以把 temp view 想成：

- DataFrame 的 SQL 別名
- session 內短生命週期的查詢入口

## Loading Data for Spark SQL

Spark SQL 常處理的不只 CSV。

### CSV

```python
df = spark.read.csv(filename)
df = spark.read.csv(filename, header=True)
```

### Text Files

```python
df = spark.read.text("sherlock.txt")
print(df.first())
print(df.count())
```

`read.text()` 讀進來後通常是一個叫做 `value` 的單欄 DataFrame，每列對應原始檔案的一行。

### Parquet

```python
df = spark.read.load("sherlock.parquet")
```

Key point: Parquet 比 CSV 更接近 Spark 的原生工作方式，因為它有 schema、壓縮友善，而且通常更適合分散式分析。

## Temp Views and Querying

把 DataFrame 註冊成 temp view 後，就可以直接用 SQL：

```python
df.createOrReplaceTempView("schedule")
spark.sql("SELECT * FROM schedule LIMIT 5").show()
```

這個模式很適合：

- 快速做 ad hoc exploration
- 把多步 DataFrame 操作改寫成較短的 SQL
- 寫 window function 或 aggregation 邏輯

## Schema and Table Inspection

當你接手一個 temp view 或 table，常見第一步不是直接查資料，而是先看結構：

```python
spark.sql("SHOW COLUMNS FROM tablename").show()
spark.sql("DESCRIBE tablename").show()
spark.sql("SELECT * FROM tablename LIMIT 0").show()
```

這類查詢很實用，因為它們能快速回答：

- 有哪些欄位
- 欄位型別是什麼
- 不必把整張表真的拉出來看

## SQL and DataFrame API Are Interchangeable Building Blocks

Spark 裡很少需要死守某一邊。

常見混用模式像這樣：

```python
result = (
    spark.sql("SELECT train_id AS train, station FROM schedule LIMIT 5")
    .where("station IS NOT NULL")
)
```

或反過來：

```python
df_filtered = df.where("station IS NOT NULL")
df_filtered.createOrReplaceTempView("schedule_filtered")
```

Tip: 真正實用的心智模型不是「我要選 SQL 還是 DataFrame API」，而是「哪一段用哪種語法最清楚」。

## Window Functions

Spark SQL 很適合寫 window logic，例如：

- `ROW_NUMBER()`
- `LEAD()`
- `LAG()`

```python
query = """
SELECT *,
       ROW_NUMBER() OVER(PARTITION BY train_id ORDER BY time) AS id
FROM schedule
"""

spark.sql(query).show()
```

### `LEAD()` Example

```python
query = """
SELECT train_id, station, time,
       LEAD(time, 1) OVER (PARTITION BY train_id ORDER BY time) AS time_next
FROM schedule
"""

spark.sql(query).show()
```

這類查詢很適合：

- 排序後看下一筆或上一筆
- 建站點順序、事件序列、session path
- 做每組內的排名與編號

## SQL Window vs PySpark Window API

同一件事也可以用 PySpark API 表達：

```python
from pyspark.sql import Window
from pyspark.sql.functions import row_number

window = Window.partitionBy("train_id").orderBy("time")
df = df.withColumn("id", row_number().over(window))
```

可以先這樣理解對應關係：

- SQL `OVER (...)`
- PySpark `Window...`

如果團隊比較習慣 SQL，window function 用 `spark.sql()` 往往更易讀；如果你已經在 DataFrame pipeline 中，PySpark API 可能更連續。

## Text Processing in Spark SQL Workflows

這門課有一個實用方向是：先把純文字檔讀成 DataFrame，再用 Spark functions 做清理與切詞。

例如：

```python
from pyspark.sql.functions import lower, regexp_replace, split, explode

df2 = df.select(lower("value").alias("v"))
df3 = df2.select(regexp_replace("v", "don't", "do not").alias("v"))
df4 = df3.select(split("v", "[ ]").alias("words"))
df5 = df4.select(explode("words").alias("word"))
```

這類流程的關鍵不是 NLP 很高級，而是：

- 先維持在 Spark DataFrame 裡
- 用內建函式逐步做 transformation
- 最後才把 token / row-level 結果拿去聚合

## Extract, Transform, Select

這門課把 Spark SQL workflow 拆成一個很實用的順序：

1. extract: 從 CSV、text、parquet 等來源讀資料
2. transform: 清理、切分、補欄位、改格式
3. select: 用 SQL 或 DataFrame API 取出你真正要的結果

這很像 ETL，但更偏 notebook / analysis workflow 的最小版本。

## Caching in Spark SQL Workflows

當同一個 DataFrame 或 temp view 會被反覆查詢時，cache 才開始有價值：

```python
df.cache()
df.unpersist()
```

這門課還提到一個容易被忽略的點：

- Spark 會很積極地管理記憶體
- cached data 不是永遠保證存在
- eviction 常是 `LRU` 風格，而且在各 worker 上分別發生

Warning: `cache()` 不是「鎖定記憶體」。它比較像向 Spark 表示「這份資料值得優先保留」，但是否真的留得住，仍然受 worker 記憶體壓力影響。

## When Spark SQL Is a Good Fit

Spark SQL 特別適合：

- 資料本來就在 Spark 裡
- 你想用 SQL 寫聚合、過濾、window logic
- 團隊對 SQL 比較熟
- 查詢需要分散式執行，而不是單機 pandas

但如果需求只是小表、單機分析、簡單轉換，直接用 pandas / DuckDB / 普通 SQL engine 往往更輕。

## Spark SQL vs Databricks SQL

這兩者很容易被混淆，但層次不同：

| Concept | What it emphasizes |
| --- | --- |
| Spark SQL | Spark 裡的 SQL 查詢介面，常透過 `spark.sql()` 在 notebook / PySpark 流程中使用 |
| Databricks SQL | Databricks 平台上的 SQL-first analytics layer，偏 warehouse、dashboard、BI 與 table maintenance |

簡單說：

- Spark SQL 比較像 engine 內的 query language
- Databricks SQL 比較像平台上的 SQL 工作面

## Related Notes

- [Spark and PySpark](spark-and-pyspark.md)
- [Databricks SQL](databricks-sql.md)
- [Processing and Pipelines](processing-and-pipelines.md)
