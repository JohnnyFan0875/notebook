[Computing](../README.md) › 程式語言

# 程式語言 (Programming Languages)

Python 與 R 以外的語言筆記。Python、R 是資料工作的主力，放在 [Data Science](../../data-science/README.md)；這裡的語言多半是在特定情境遇到：JVM 生態系（Java、Scala）與高效能科學運算（Julia）。編譯、直譯與 JIT 的差別見 [電腦架構與程式執行](../computer-science-foundations/computer-architecture-and-program-execution.md#從原始碼到執行)。

## 語言比較

| 語言 | 型別 | 執行模型 | 典型用途 | 生資 / 資料情境 |
| --- | --- | --- | --- | --- |
| [Python](../../data-science/python-foundations/README.md) | 動態 | 直譯（位元組碼）；重運算交給 C 擴充（NumPy） | 資料分析、ML、腳本、API | pandas、scanpy、Snakemake、多數生資腳本 |
| [R](../../data-science/r-foundations/README.md) | 動態 | 直譯 | 統計、視覺化、報告 | Bioconductor（DESeq2、edgeR）、tidyverse |
| [Java](java/README.md) | 靜態 | 位元組碼 + JVM（JIT） | 企業後端、大型系統、Android | GATK、Picard、IGV、Nextflow 的執行環境 |
| [Scala](scala-fundamentals.md) | 靜態（型別推斷） | JVM | 分散式資料處理、函數式系統 | Spark、Glow / Hail |
| [Julia](julia-fundamentals.md) | 動態（可標註） | JIT（LLVM） | 數值模擬、最佳化、微分方程 | BioJulia、需要快速迴圈的模擬 |
| C / C++ / Rust | 靜態 | 編譯成機器碼 | 系統程式、效能關鍵工具 | samtools / htslib、BWA、minimap2 |
| Bash | 動態（全是字串） | 直譯 | 串接命令列工具、自動化 | [Shell 腳本](../operating-system/shell-scripting.md)、pipeline 膠水程式碼 |

| 問題 | 選擇 |
| --- | --- |
| 一般資料分析、ML | Python 或 R |
| 統計方法、Bioconductor 套件 | R |
| 要跑既有的 JVM 生資工具 | 不必寫 Java，但要懂 `-Xmx` 與錯誤訊息（[Java 效能](java/java-performance-and-concurrency.md#jvm-記憶體與-gc)） |
| Spark 大規模處理 | PySpark；需要型別安全或內部 API 時用 Scala |
| 自己寫的模擬太慢、Python 迴圈無法向量化 | Julia，或 Python + Numba |
| 串接命令列工具 | Bash；步驟多時改用 [工作流引擎](../workflow-engines/README.md) |

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Java](java/README.md) | 8 篇：基礎、控制流程、OOP、集合與例外、核心 API、I/O 與 Stream、測試、效能與並行 | 怎麼寫與維護 Java 程式？JVM 工具怎麼調？ |
| [Scala 基礎](scala-fundamentals.md) | `val` / `case class` / 模式比對 / `Option`、sbt、Spark 範例 | 為什麼 Spark 用 Scala？何時值得學？ |
| [Julia 基礎](julia-fundamentals.md) | 安裝與環境、型別、陣列與廣播、多重分派、DataFrames | Julia 怎麼寫？和 Python 差在哪？ |
| [Julia 進階模式](julia-intermediate-patterns.md) | 迭代、tuple / Dict / struct、函式簽章、`@btime`、缺值處理、互通 | 怎麼寫出快又清楚的 Julia？ |
