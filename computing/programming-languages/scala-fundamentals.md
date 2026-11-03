[Computing](../README.md) › [程式語言](README.md) › Scala 基礎

# Scala 基礎 (Scala Fundamentals)

Scala（scalable language）是在 JVM 上執行、結合物件導向與函數式的靜態型別語言。在資料工程中重要，主要因為 **Apache Spark 是用 Scala 寫的**：讀 Spark 原始碼與錯誤訊息、使用 PySpark 沒有的 API、維護 JVM 資料平台時會遇到。不是每個資料工程任務都需要 Scala，多數情境 PySpark 就夠。Spark 本身見 [資料工程](../../data-science/data-engineering/README.md)。

## 為什麼在資料工程出現

| 理由 | 說明 |
| --- | --- |
| Spark 原生語言 | API 最完整、型別安全的 Dataset API 只有 Scala / Java 有 |
| JVM 生態系 | 直接使用 Java 函式庫、成熟的部署與監控工具（Kafka、Flink 也是 JVM） |
| 函數式風格 | 不可變資料與高階函式，天然對應分散式的 `map` / `filter` / `reduce` |
| 靜態型別 + 型別推斷 | 編譯時抓錯，又不必到處寫型別 |

## 執行方式

| 方式 | 指令 | 適合 |
| --- | --- | --- |
| REPL | `scala` | 互動式探索 |
| 腳本 / 單檔 | `scala run hello.scala`（Scala 3.5+ 的 `scala` 指令即 Scala CLI） | 小工具、實驗 |
| 專案 | `sbt compile` / `sbt test` / `sbt run`（`build.sbt`） | 多檔案、依賴、測試、打包 |
| 舊式 | `scalac Game.scala` 後 `scala Game` | Scala 2 時代的寫法 |

| | 直譯 / REPL | 編譯成應用程式 |
| --- | --- | --- |
| 好處 | 回饋快 | 效能、專案結構、測試 |
| 代價 | 不像正式程式的結構 | 需要建置與編譯步驟（Scala 編譯較慢） |

> 版本：Scala 3 是目前主線；Spark 4 使用 Scala 2.13。Spark 專案的 Scala 版本要與 Spark 建置時的版本一致。

## 語法速覽

```scala
val name = "TP53"                 // val：不可變（優先使用）；型別推斷為 String
var count = 0                     // var：可變
val reads: Long = 1_200_000L      // 明確標註型別

def gcContent(seq: String): Double =                 // 方法：參數型別必寫，回傳型別可推斷
  seq.count(c => c == 'G' || c == 'C').toDouble / seq.length

val label = if count > 10 then "high" else "low"     // if 是運算式，有回傳值（Scala 3 語法）

case class Sample(id: String, tissue: String, readsM: Double)   // 不可變資料類別：自動產生 equals、toString、copy
val s = Sample("S1", "liver", 32.1)
val s2 = s.copy(readsM = 40.0)                                   // 複製並修改一個欄位

val samples = List(s, Sample("S2", "lung", 28.4), Sample("S3", "liver", 40.0))
samples.filter(_.tissue == "liver").map(_.readsM).sum            // 72.1：_ 是匿名函式參數的簡寫
samples.groupBy(_.tissue).view.mapValues(_.size).toMap           // Map(liver -> 2, lung -> 1)

def describe(x: Any): String = x match                           // 模式比對 (pattern matching)
  case Sample(id, "liver", _) => s"$id is liver"                 // s"..." 字串內插
  case n: Int if n > 0        => "positive int"
  case _                      => "other"

val maybe: Option[Sample] = samples.find(_.id == "S9")           // Option：可能沒有值，取代 null
maybe.map(_.readsM).getOrElse(0.0)                               // 0.0
```

| 概念 | Scala | 對應 |
| --- | --- | --- |
| 不可變變數 | `val` | Java `final`、Kotlin `val` |
| 資料類別 | `case class` | Java `record`、Python `@dataclass` |
| 可能沒有值 | `Option[T]`（`Some` / `None`） | Java `Optional`、Python `None` |
| 集合轉換 | `map`、`filter`、`groupBy`、`foldLeft` | Java Stream、pandas |
| 介面 + 混入 | `trait` | Java interface |
| 單例 | `object` | Java static 成員 |

## Spark 範例

```scala
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

val spark = SparkSession.builder.appName("qc").getOrCreate()
import spark.implicits._

val df = spark.read.option("header", "true").option("inferSchema", "true").csv("samples.csv")
df.filter($"reads_m" > 30)
  .groupBy("tissue")
  .agg(avg("reads_m").as("mean_reads"), count("*").as("n"))
  .show()

case class Sample(id: String, tissue: String, reads_m: Double)
val ds = df.as[Sample]            // Dataset[Sample]：欄位名稱或型別錯誤在編譯時就發現
```

同樣的 DataFrame 操作在 PySpark 幾乎逐行對應；Scala 的優勢在型別安全的 Dataset、UDF 效能（不必在 JVM 與 Python 之間序列化）與直接使用 Spark 內部 API。

## 何時值得學

| 情境 | 建議 |
| --- | --- |
| 用 Spark 做一般 ETL、分析 | PySpark 即可 |
| 要讀 Spark 原始碼、除錯 JVM stack trace | 讀得懂 Scala 就好 |
| 寫高效能 UDF、自訂 Spark 擴充、Spark 基因體工具（Glow、Hail 的 JVM 部分） | 學 Scala |
| 公司大量使用 JVM（Kafka、Flink、Akka） | 學 Scala |

> Scala 結合函數式與物件導向，表達力強但概念多（隱式轉換、型別類別、進階型別系統）；團隊的熟悉度往往比語言本身更重要。基因體資料的 Spark 應用見 [Spark for Genomics](../../data-science/data-engineering/spark-for-genomics.md)。
