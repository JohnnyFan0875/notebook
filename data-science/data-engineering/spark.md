# Spark and PySpark

Spark 是分散式資料處理引擎。前半是 PySpark 的核心心智模型（RDD、DataFrame、lazy evaluation、清理與特徵工程），後半是 Spark SQL（`spark.sql()`、temp view、window functions）。R 介面見 [Spark with sparklyr](sparklyr.md)；單機放不下但不需要叢集時，先看 [Scalable Processing and Out-of-Core Workflows](scalable-processing-and-out-of-core.md)。

## Why Spark Shows Up in Data Engineering

當資料量、資料速度或運算需求超過單機工具能舒服處理的範圍時，團隊就會開始考慮 distributed processing。

Spark 常出現的原因不是它「比較潮」，而是它剛好補上了這幾件事：

- 可以在 cluster 上平行處理大量資料
- 同時支援 batch 與接近 real-time 的工作流
- 能從多種資料來源讀取資料
- 提供比底層 MapReduce 更一致、較高階的開發體驗

## Big Data in Practice

big data 不只是資料很多，而是資料的規模、型態或速度讓傳統工具不再划算或不再可靠。

實務上常用三個角度理解：

- `Volume`: 資料量很大
- `Variety`: 資料來源與格式很多
- `Velocity`: 資料到來速度快

一旦這三件事開始影響成本、延遲或可靠性，資料工程就會從「寫幾支腳本」變成「設計整個處理系統」。

## Core Computing Terms

這幾個詞很容易混在一起，但其實各自有重點：

| Term | 直覺理解 |
| --- | --- |
| Cluster computing | 把多台機器的資源湊在一起工作 |
| Parallel computing | 同時做多個計算 |
| Distributed computing | 多個網路節點一起完成任務 |
| Batch processing | 把工作切成批次後處理 |
| Real-time processing | 資料進來後盡快處理 |

Spark 常被放進來的場景，通常同時牽涉 cluster、parallel 與 distributed 這三層。

## Spark vs. Hadoop/MapReduce

Spark 不是第一個大數據框架，但它在很多現代工作流中比傳統 MapReduce 更常見。

| System | Practical Character |
| --- | --- |
| Hadoop / MapReduce | 可擴充、容錯，但較偏傳統 batch 模式 |
| Apache Spark | 更通用、記憶體運算更強，常用於 batch 與近即時處理 |

如果用很粗的方式理解：

- MapReduce 比較像較底層的大規模批次計算模型
- Spark 比較像現代資料團隊常用的 general-purpose processing engine

## What Spark Is Good At

Spark 的常見優勢包括：

- distributed cluster computing
- in-memory computation
- 支援 Python、Scala、Java、R 與 SQL
- 同一套生態可以處理 ETL、SQL、streaming 與機器學習

這不代表它永遠最快，而是它在「單一平台處理多種大規模任務」這件事上很有吸引力。

## Deployment Modes

Spark 的一個實務優點，是 local 與 cluster 的工作方式相對連續。

### Local Mode

- 單機執行
- 適合測試、除錯、教學與原型

### Cluster Mode

- 在多台預先配置的機器上執行
- 更適合 production 與大規模資料

一個很重要的心智模型是：

- 很多 Spark workflow 可以先在 local 開發
- 再搬到 cluster 執行
- 程式本身不一定需要大改

## PySpark Entry Points

在 PySpark 裡，常見有兩個入口概念：

### SparkContext

`SparkContext` 是進入 Spark 世界的基本入口。

- 常見預設變數是 `sc`
- 負責連到 Spark cluster
- 傳統上常用來建立與操作 RDD

如果把 Spark 想成一個分散式運算環境，`SparkContext` 很像你拿到的入口鑰匙。

### SparkSession

`SparkSession` 是 DataFrame API 的主要入口。

- 常見預設變數是 `spark`
- 用來建立 DataFrame
- 能註冊表格與執行 SQL
- 現代 Spark 工作流通常更常從這裡開始

簡單來說：

- `sc` 比較偏 RDD 世界
- `spark` 比較偏 DataFrame / SQL 世界

一個最常見的起手式是：

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("MySparkApp").getOrCreate()
```

可以先這樣理解：

- `.builder`: 開始設定 session
- `.appName(...)`: 幫這次應用命名
- `.getOrCreate()`: 若已有 session 就重用，沒有就建立新的

Tip: 初學時常會看到 `getOrCreate()`。它的重點不是特別高深，而是避免同一環境重複建立 session。

## RDD: The Lower-Level Abstraction

RDD 是 `Resilient Distributed Dataset`。

這個名字其實已經把重點講完了：

- `Resilient`: 能承受部分失敗
- `Distributed`: 分散在多台機器上
- `Dataset`: 是可被切分與處理的資料集合

RDD 比較像 Spark 的基礎抽象。它常被拿來教 Spark 的分散式思維，也很適合理解 partition、lazy evaluation 和 transformations / actions。

### Creating RDDs

常見來源包括：

- 把現有 Python collection 平行化
- 從外部資料讀進來，例如文字檔
- 從既有 RDD 派生新 RDD
- 從 HDFS 或 S3 等外部儲存讀取

### Partitioning

partition 是大型分散式資料集的邏輯切分單位。

它很重要，因為：

- partition 決定資料如何被分散
- 影響平行度
- 也影響執行效率與資源利用

一個常見原則是：Spark 處理的是 partitioned data，而不是整份資料一次塞進同一顆 CPU。

### Transformations and Actions

RDD 操作通常分成兩類：

- `transformations`: 產生新的 RDD
- `actions`: 真正觸發計算或回傳結果

常見的 transformation 包括：

- `map()`
- `filter()`
- `flatMap()`
- `union()`

常見的 action 包括：

- `collect()`
- `count()`
- `first()`
- `take()`
- `reduce()`

### Lazy Evaluation

RDD transformation 很重要的一個特性是 lazy evaluation。

意思是：

- 你先描述要怎麼轉換資料
- Spark 先記住這些步驟
- 直到 action 發生時，才真正執行計算

這種設計有助於：

- 延後不必要的計算
- 讓 Spark 有機會最佳化執行計畫
- 把多個步驟合併成較有效率的資料流

## DataFrames: The Higher-Level Abstraction

DataFrame 是現在更常見的 Spark 資料處理介面。

它可以被理解成：

- immutable
- distributed
- 有 named columns 的資料集合

與 RDD 相比，DataFrame 更貼近表格資料與分析工作流，也更容易利用 schema 與 Spark SQL 的最佳化能力。

### Why DataFrames Often Win

DataFrame 很常成為首選，因為它：

- 對 structured data 更自然
- 也能處理部分 semi-structured data，例如 JSON
- 能用 SQL 或 expression-style API 操作
- 有 schema，因此 Spark 較容易做查詢與執行最佳化

### Creating DataFrames

常見方式有兩種：

1. 從既有 RDD 建立
2. 直接從 CSV / JSON / TXT 等資料來源讀取

實務上第二種通常更常見，特別是在 ETL 或分析資料工作流裡。

### Schema Matters

schema 不只是欄位名稱列表而已，它還描述：

- 欄位型別
- 欄位結構
- 缺失值或資料格式的預期

這對 Spark 很重要，因為 schema 能幫助：

- query optimization
- 型別一致性
- 跨步驟資料品質控制

### Common DataFrame Operations

DataFrame 也同樣有 transformations 與 actions。

常見 transformation 包括：

- `select()`
- `filter()`
- `groupBy()`
- `orderBy()`
- `dropDuplicates()`
- `withColumnRenamed()`

常見 action 或常用檢視方法包括：

- `show()`
- `head()`
- `count()`
- `describe()`
- `columns`
- `printSchema()`

對大多數 data engineering workflow 來說，DataFrame API 通常比直接玩 RDD 更接近實際任務。

其中有一個特別值得提醒的 action 是 `collect()`：

- 它會把分散式結果拉回 driver
- 適合小結果、除錯或少量檢查
- 不適合直接對大表使用

Warning: `collect()` 很方便，但如果結果其實很大，它等於把 Spark 好不容易分散處理的資料一次搬回單機記憶體，常常會直接變成新的瓶頸。

### Data Cleaning with DataFrames

在 Spark 裡做資料清理，通常不是另外一套工具，而是把 schema、DataFrame transformations 與輸出格式串成穩定流程。

常見清理動作包括：

- 重新格式化文字
- 補或改欄位型別
- 做欄位計算
- 過濾垃圾資料、缺值或不合理資料

實作上最常見的 DataFrame 操作有：

- `filter()` / `where()`
- `select()`
- `withColumn()`
- `drop()`

處理缺值時，`df.na` 這組 helper 很常用：

- `df.na.drop()`: 丟掉含 null 的列
- `df.na.fill({"age": 0})`: 用指定值補某欄位的 null

如果只是想保留某欄不為 null 的資料，也常會看到：

```python
from pyspark.sql.functions import col

df_cleaned = df.where(col("columnName").isNotNull())
```

Key point: 在 Spark 裡做 missing-data cleaning，盡量保持在 DataFrame expression 裡完成，不要太早把資料拉回 Python 端逐列處理。

如果任務是整理表格資料，這通常會比先轉成 Python list 再逐列處理更符合 Spark 的工作方式。

### Why Explicit Schema Matters

Spark 可以推斷 schema，但在資料清理流程裡，明確定義 schema 往往更可靠。

schema 除了描述欄位名稱，也描述：

- data type
- nullable 預期
- 欄位結構，例如陣列或巢狀欄位

在實務上，先定義 schema 的常見好處是：

- 匯入更快
- 一開始就做型別與結構檢查
- 比較容易提早擋掉格式不對的資料
- 中間落地成 Parquet 等格式後，不必反覆重新猜 schema

如果完全沒有 schema，代價通常是：

- 匯入時較難做驗證
- 中間檔或下游步驟要再次推斷或重建欄位定義
- 除錯時不容易判斷問題出在資料本身還是型別推斷

### Common Cleaning Patterns

Spark 清理資料時，常見模式包括：

- 用 `filter()` 移除 null、空字串或明顯錯誤值
- 用 `withColumn()` 做 cast、字串轉換或衍生欄位
- 用 `upper()`、`split()` 等內建函式整理字串
- 對陣列欄位用 `size()`、`getItem()` 取長度或元素
- 用 `when()` / `otherwise()` 寫欄位級的條件邏輯

一個實用原則是：能用 Spark 內建 expression 完成的清理，通常先不要急著寫自訂 Python 迴圈。

### UDFs as a Fallback

當清理規則真的無法直接用內建函式表達時，才考慮 UDF。

UDF 的角色比較像補位：

- 封裝特殊商業規則
- 處理比較難直接用 SQL-style expression 表達的邏輯
- 讓欄位轉換可以重複使用

但在 notebook 與 production workflow 裡，都應該先優先考慮原生 Spark functions，因為它們通常更容易維護，也比較貼近 Spark 的最佳化路徑。

### Caching in Cleaning Workflows

清理流程常常需要反覆檢查同一份中介 DataFrame，這時 caching 才開始有價值。

cache 的典型用途是：

- 同一份資料會被多次 action 或多個分支重用
- 重跑上游轉換成本很高
- 你正在除錯某段清理流程，想減少重算時間

常見做法是：

- 先呼叫 `cache()`
- 用 `count()` 或其他 action materialize
- 用 `is_cached` 檢查狀態
- 做完後用 `unpersist()` 釋放資源

但不要把 cache 當成預設設定。資料太大、記憶體不足，或只能落到慢磁碟時，cache 反而可能沒帶來好處。很多情況下，把中介結果寫成 Parquet 重新讀回來，會比盲目 cache 更穩定。

### Feature Engineering in PySpark

PySpark 的特徵工程通常不是一個單一函式，而是把 DataFrame API 與 `pyspark.ml.feature` 元件串起來。

常見流程大致是：

1. 先理解欄位與分析目標
2. 移除無關、常數、錯誤或重複資料
3. 處理缺值與型別
4. 建立衍生特徵
5. 把欄位組裝成模型可吃的 `features` 向量

### Early Checks Before Building Features

在 Spark workflow 裡，幾個很實際的起手式包括：

- 用 `spark.version` 確認執行環境
- 先 `select()` 關鍵欄位做 spot check
- 用 `dropDuplicates()` 清理重複資料
- 用 `isNull()`、`count()` 或抽樣視覺化了解 missingness

其中一個容易忽略的點是：`dropDuplicates()` 在 PySpark 裡不保證保留哪一筆，所以如果重複列之間其實有品質差異，應該先定義更明確的保留規則。

### Common PySpark Feature Operations

建立特徵時，最常見的操作包括：

- 用 `withColumn()` 建立 arithmetic features
- 用 `log()` 對偏態數值做轉換
- 用 `Binarizer` 把 numeric signal 轉成 yes / no
- 用 `Bucketizer` 把連續值分箱
- 用 `StringIndexer` 處理類別標籤
- 用 `OneHotEncoder` 把 indexed category 轉成向量
- 用 `VectorAssembler` 把多個欄位組成 `features`

這些工具的重要性不只在於「會用 API」，而是它們讓同一套轉換邏輯能在訓練與推論時一致重現。

### Missing Data and Sampling in Spark

大型資料集不一定適合每一步都完整畫圖或完整匯出，所以 Spark 實務上常會：

- 先 `select()` 少數欄位
- `sample()` 一小部分資料
- 再轉成 pandas 做快速 heatmap 或人工檢查

這種做法的重點不是把 Spark 退回 pandas，而是用小樣本加快資料理解與缺值診斷。

### Time-Aware Splits

如果資料有明確時間軸，Spark 內部也應該用時間來切 train / test，而不是一律隨機切分。

常見做法是：

- 先找資料的最早與最晚日期
- 用 `datediff()` 算跨度
- 用 `date_add()` 決定切分點
- 讓 train 只包含切分日前資料，test 只包含切分日後資料

這能降低 temporal leakage，特別是在房價、交易、需求或事件資料裡很重要。

## RDD vs. DataFrame

| Aspect | RDD | DataFrame |
| --- | --- | --- |
| 抽象層級 | 較低 | 較高 |
| 資料形狀 | 比較自由 | 偏表格、欄位明確 |
| 最佳化能力 | 較少 | 較能利用 schema 與 SQL 優化 |
| 常見用途 | 理解分散式資料模型、特殊低階處理 | ETL、分析、特徵整理、SQL-style workflow |

很粗略地說：

- 想理解 Spark 基本運作，可以學 RDD
- 真正在專案裡做大多數表格資料工作，通常會更常用 DataFrame

## PySpark MLlib in Context

Spark 不只做資料處理，也有 `MLlib` 這個機器學習元件。

它的價值不在於「一定比 scikit-learn 好」，而在於：

- scikit-learn 偏單機
- MLlib 更適合 cluster 上的大規模資料流程
- 能和 Spark 的資料處理、feature pipeline、SQL workflow 串在一起

常見能力包括：

- classification / regression
- collaborative filtering
- clustering
- featurization
- ML pipelines

## When Spark Is a Good Fit

Spark 特別適合：

- 資料量已經大到單機處理不划算
- ETL 需要平行化
- 要從 HDFS、S3 或分散式儲存讀資料
- 想把 SQL、資料轉換、部分機器學習工作放在同一平台

但不是每個專案都需要 Spark。

如果資料量還小、單機 pandas 足夠、團隊沒有 cluster 維運能力，那 Spark 可能只是增加複雜度。

## Practical Reminders

- Spark 的核心價值是 distributed processing，不是單純把 pandas 換個 API。
- local mode 與 cluster mode 的切換很重要，因為它讓開發與 production 比較能接起來。
- RDD 幫助理解 Spark 基本模型，但多數表格資料任務通常更適合 DataFrame。
- partition 會影響平行度與效能，因此不是只要能跑就好。
- lazy evaluation 是 Spark 行為的關鍵，很多效能與除錯問題都和「何時真的執行」有關。

## Spark SQL

Spark SQL 是 Spark 裡把 DataFrame 世界和 SQL 世界接起來的那一層。它很適合這種情境：

- 你已經在 PySpark notebook 裡
- 資料是 DataFrame
- 但某些轉換、分析或 window logic 用 SQL 更直觀

Key point: Spark SQL 不是另一個獨立平台，而是建立在 Spark execution engine 上的查詢介面。`spark.sql()` 和 DataFrame API 最終是在同一個分散式運算環境裡工作。

### The Core Workflow

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

### Loading Data for Spark SQL

Spark SQL 常處理的不只 CSV。

#### CSV

```python
df = spark.read.csv(filename)
df = spark.read.csv(filename, header=True)
```

#### Text Files

```python
df = spark.read.text("sherlock.txt")
print(df.first())
print(df.count())
```

`read.text()` 讀進來後通常是一個叫做 `value` 的單欄 DataFrame，每列對應原始檔案的一行。

#### Parquet

```python
df = spark.read.load("sherlock.parquet")
```

Key point: Parquet 比 CSV 更接近 Spark 的原生工作方式，因為它有 schema、壓縮友善，而且通常更適合分散式分析。

### Temp Views and Querying

把 DataFrame 註冊成 temp view 後，就可以直接用 SQL：

```python
df.createOrReplaceTempView("schedule")
spark.sql("SELECT * FROM schedule LIMIT 5").show()
```

這個模式很適合：

- 快速做 ad hoc exploration
- 把多步 DataFrame 操作改寫成較短的 SQL
- 寫 window function 或 aggregation 邏輯

### Schema and Table Inspection

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

### SQL and DataFrame API Are Interchangeable Building Blocks

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

### Window Functions

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

#### `LEAD()` Example

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

### SQL Window vs PySpark Window API

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

### Text Processing in Spark SQL Workflows

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

### Extract, Transform, Select

這門課把 Spark SQL workflow 拆成一個很實用的順序：

1. extract: 從 CSV、text、parquet 等來源讀資料
2. transform: 清理、切分、補欄位、改格式
3. select: 用 SQL 或 DataFrame API 取出你真正要的結果

這很像 ETL，但更偏 notebook / analysis workflow 的最小版本。

### Caching in Spark SQL Workflows

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

### When Spark SQL Is a Good Fit

Spark SQL 特別適合：

- 資料本來就在 Spark 裡
- 你想用 SQL 寫聚合、過濾、window logic
- 團隊對 SQL 比較熟
- 查詢需要分散式執行，而不是單機 pandas

但如果需求只是小表、單機分析、簡單轉換，直接用 pandas / DuckDB / 普通 SQL engine 往往更輕。

### Spark SQL vs Databricks SQL

這兩者很容易被混淆，但層次不同：

| Concept | What it emphasizes |
| --- | --- |
| Spark SQL | Spark 裡的 SQL 查詢介面，常透過 `spark.sql()` 在 notebook / PySpark 流程中使用 |
| Databricks SQL | Databricks 平台上的 SQL-first analytics layer，偏 warehouse、dashboard、BI 與 table maintenance |

簡單說：

- Spark SQL 比較像 engine 內的 query language
- Databricks SQL 比較像平台上的 SQL 工作面
