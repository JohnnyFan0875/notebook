[Computing](../../README.md) › [程式語言](../README.md) › Java

# Java

靜態型別、在 JVM 上執行的通用語言。資料工作者最常在這些情境碰到它：執行 GATK / Picard / IGV 等 JVM 工具（調 `-Xmx`）、讀懂 Nextflow（Groovy）與 Spark（Scala / JVM）的錯誤訊息、維護既有的 Java 後端。

## 學習順序

```
基礎 → 控制流程與方法 → OOP → 集合與例外處理 → 核心 API → 檔案 I/O 與 Stream → 測試 → 效能與並行
```

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [基礎](java-fundamentals.md) | 程式結構、`javac` / `java`、基本型別 vs 參考型別、包裝類別、字串、陣列、運算子、package、`BigDecimal` | Java 程式怎麼寫、怎麼跑？型別怎麼運作？ |
| [控制流程與方法](java-control-flow-and-methods.md) | 方法、`static`、`if`、`switch`（含箭頭語法）、迴圈 | 怎麼組織邏輯與重複執行？ |
| [OOP](java-oop.md) | 類別、建構子、封裝、POJO 與 `record`、繼承、抽象類別 vs 介面、多型 | 怎麼用物件建模？ |
| [集合與例外處理](java-collections-and-exception-handling.md) | `List` / `Set` / `Map` / `Deque`、泛型、checked vs unchecked、`throws`、logging | 一群物件怎麼存？出錯怎麼處理？ |
| [核心 API](java-core-apis.md) | `java.time`、enum、`Optional`、遞迴 | 日期、固定選項、可能沒有值怎麼表示？ |
| [檔案 I/O 與 Stream](java-file-io-and-streams.md) | `Path` / `Files`、try-with-resources、gzip、`Iterator`、Stream API | 怎麼讀寫檔案？怎麼寫資料處理管線？ |
| [測試](java-testing.md) | JUnit、AAA、Mockito、參數化測試 | 怎麼確認程式正確？ |
| [效能與並行](java-performance-and-concurrency.md) | 選對集合、JVM heap 與 GC、`-Xmx`、執行緒池、虛擬執行緒、平行 stream | 程式為什麼慢？怎麼用多核心？ |

| Python 對照 | Java |
| --- | --- |
| `list` / `dict` / `set` | `ArrayList` / `HashMap` / `HashSet` |
| list comprehension、pandas 管線 | Stream API |
| `try` / `except` / `finally`、`with` | `try` / `catch` / `finally`、try-with-resources |
| `pytest` | JUnit |
| `@dataclass(frozen=True)` | `record` |
| `pip` / `uv` + `pyproject.toml` | Maven `pom.xml` / Gradle |
