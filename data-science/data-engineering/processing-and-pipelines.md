# Processing and Pipelines

## What a Data Pipeline Does

Data pipeline 的目標，是把資料從一個系統穩定搬到另一個系統，並在過程中完成必要的清理、轉換與交付。

理想的 pipeline 應該要能：

- 自動化資料流動
- 減少人工介入
- 提供最新、正確、相關的資料
- 支援重跑與監控

## ETL and Pipelines

ETL 是最常見的資料移動框架之一：Extract → Transform → Load。pipeline 是更廣的概念：它不只描述 ETL，也描述整條資料如何在多個系統之間移動與協調。ETL 的重點不是每一步都很複雜，而是每一步都要能被明確描述、重現與自動化。

### ETL and ELT

ETL 與 ELT 都是在搬資料，但轉換發生的位置不同。

| Pattern | Flow | 常見場景 |
| --- | --- | --- |
| ETL | extract -> transform -> load | 先在外部程式整理資料，再載入目標系統 |
| ELT | extract -> load -> transform | 先把資料載入 warehouse 或 lakehouse，再利用平台算力轉換 |

實務上可以這樣理解：

- ETL 比較像先把資料洗乾淨，再交給下游。
- ELT 比較像先把資料送進分析平台，再在平台內部整理。
- ETL 常同時處理 tabular 與 non-tabular sources。
- ELT 則更常出現在以 warehouse 為核心、資料格式較偏 tabular 的分析環境。

### From Business Need to ETL

很多 ETL 專案其實都從一個很簡單的需求開始，例如：

- 取得 rating data
- 清理並算出 top recommended items
- 每天重新計算
- 提供給 dashboard 或應用程式

這類需求之所以屬於 data engineering，是因為它不只是一次分析，而是要穩定地每天重做，並讓下游可以持續依賴結果。

### The Three Stages

#### Extract

從來源系統取出資料。

來源可能是：

- 資料庫 tables
- flat files
- API responses
- web data

#### Transform

把原始資料轉成下游可用的形式。

常見工作包括：

- 清理錯誤值
- 合併多個來源
- 補欄位與計算指標
- 建立推薦、彙總或特徵表

如果來源含有 JSON、API responses 或其他半結構化資料，transform 往往還包含：

- parsing nested fields
- 補上 metadata
- 把非表格格式整理成穩定 schema

#### Load

把結果寫入目標系統，供下游使用。

常見目標包括：

- analytics tables
- dashboard backend
- feature store 或模型輸入表

常見做法是把整理後的 DataFrame 寫入 SQL table、warehouse table 或其他可查詢儲存層。重點不只是寫成功，而是讓下游可以穩定取得同樣結構的資料。

在 Python workflow 裡，load 階段也常會明確決定：

- 寫入哪個 table 或 destination
- `append`、`replace` 或 upsert 的策略
- 是否保留 index、主鍵或時間欄位

### ETL vs. One-Off Analysis

一次性分析比較常問：

- 這次能不能算出答案？

ETL 比較常問：

- 這個流程明天還能不能穩定再跑一次？
- 如果來源延遲或格式改了，怎麼辦？
- 下游是不是能持續拿到一致結果？

### Practical Reminders

- 一個 ETL workflow 的價值，在於穩定重跑，不在於第一次成功。
- 轉換步驟最好能明確區分 raw data 與 curated output，避免覆蓋原始資料。
- 如果結果要每日更新、服務 dashboard 或產品功能，它通常就已經不是單純分析腳本，而是 pipeline。

## Batch vs. Stream

### Batch Processing

Batch processing 會把資料累積到一個區間後再一起處理。

適合：

- 定時報表
- 每日或每小時彙總
- 對即時性要求不高的轉換工作

更精確一點地說，batch 常見特徵是：

- 一次處理一組資料，而不是無限持續讀入
- 常由固定 interval 或明確起始事件觸發
- 一次執行通常有相對清楚的開始與結束
- 單次執行實例常被稱為一個 job

這也是為什麼 batch 很適合報表、檔案處理與定時整併任務。

### Stream Processing

Stream processing 會在資料持續到來時逐步處理。

適合：

- 即時監控
- 事件驅動流程
- 需要低延遲反應的系統

實務上，不是所有資料都該做 streaming。streaming 的複雜度更高，只有在延遲要求真的重要時才值得。

### Event-Based vs. Streaming

event-based computing 和 streaming 很接近，但不完全一樣。

- event-based: 某個事件發生時觸發任務
- streaming: 持續處理一個 open-ended 的事件流，通常沒有明確終點

一個 event trigger 仍然可以啟動 batch job，所以「事件驅動」不自動等於「真正串流」。

常見例子包括：

- 新檔案到達後觸發一次匯入
- 使用者點擊事件持續寫入 clickstream
- 感測器資料不斷送進監控系統

理解這個差異很重要，因為很多系統其實只是 event-triggered batch，而不是 low-latency streaming architecture。

## Scheduling

很多 pipeline 的可靠性，其實取決於 scheduling，而不是轉換程式本身。

常見觸發方式包括：

- 手動執行
- 固定時間排程
- 條件成立後觸發，例如新資料到達

像 Airflow、Luigi 這類 orchestrator 的價值，不只是「定時執行」，而是把依賴關係、重試、監控與失敗處理串在一起。

## Scheduling vs. Orchestration

這兩個詞常一起出現，但不完全一樣。

- **Scheduling** 著重在什麼時間觸發任務。
- **Orchestration** 著重在多個任務之間如何協調、排序、依賴與重試。

可以把 scheduling 想成「發車時間表」，而 orchestration 是「整個運輸系統的調度」。

## Orchestration Basics

以 Airflow 這類工具來看，常見核心概念包括：

- task: 基本執行單位
- dependency: 決定任務先後順序
- DAG: 用來描述 workflow 與依賴關係的有向無環圖

當 workflow 變複雜時，orchestration 的價值通常來自：

- 協調多個 jobs
- 自動處理複雜 workflow
- 減少人工操作
- 提供可觀察性與失敗管理

## Testing Pipelines

pipeline 進入日常運作後，可靠性往往比第一次跑通更重要，所以 testing 不該只留給 application code。

### Why Testing Matters

- 確認 extract、transform、load 都真的按預期發生
- 在部署後降低維護成本
- 提早發現 data quality 問題
- 讓資料使用者能持續拿到可信結果

### Common Testing Layers

#### End-to-End Testing

把整條 pipeline 從來源跑到目的地，確認它能重複執行，並且下游真的拿得到結果。

實務上通常會一起檢查：

- repeated runs 是否穩定
- pipeline checkpoints 是否產出合理資料
- 下游 consumer 是否能存取結果
- peer review 後是否仍符合需求

#### Checkpoint Validation

不要只看最後一張表。很多問題其實在中途就出現了。

常見檢查點包括：

- extract 後 row count 是否合理
- transform 後 schema 是否符合預期
- load 後資料是否真的寫進目標系統
- 載入前後資料是否一致，或至少滿足既定容忍範圍

#### Unit Testing

把 extract、transform、load 拆成可測試函式後，就能用 unit tests 驗證個別步驟。

- 檢查輸出型別是否正確
- 檢查欄位是否存在
- 檢查特定轉換規則是否成立
- 把 pipeline logic 拉近一般軟體工程 workflow，例如 `pytest`

### Test and Production Environments

測試環境與正式環境最好分開，否則驗證流程本身就可能污染正式資料。

- 在 test environment 驗證 schema、logic 與 load 行為
- 在 production environment 控制權限、監控與寫入範圍
- 若需要人工 spot check，也應優先在測試資料或 staging destination 進行

## Parallel and Cloud Processing

當資料量變大，常見做法是增加平行化與雲端資源。

### Parallel Processing

好處：

- 更快處理大量資料
- 提升吞吐量

風險：

- 協調成本更高
- 失敗模式更複雜
- 不是所有任務都能自然平行化

### Cloud Processing

把計算資源放到雲端，常見優點是：

- 可以租用而不是一次買斷
- 更容易依需求擴充
- 不需要自己維護全部硬體

但也要考慮：

- 長期成本
- vendor lock-in
- 跨雲整合與資料移動成本

## Spark-Native Pipeline Pattern

如果 pipeline 主要發生在 Spark 內部，一條常見路徑可以整理成：

1. 用明確 schema 從 CSV、JSON、database 或 API 匯入資料
2. 用 `filter()`、`withColumn()`、`drop()` 等 transformations 清理與轉換資料
3. 在中間檢查 schema、row count 與關鍵商業規則
4. 視需要把中介結果落地成 Parquet
5. 輸出到下游檔案、資料庫或後續分析流程

這個流程看起來很基本，但它有兩個很實務的價值：

- 把資料清理、驗證與輸出放進同一個可重跑的 execution path
- 讓中間結果不只是「看起來對」，而是能被下游穩定接手

### Parsing Messy Inputs

很多 pipeline 問題不是出在轉換邏輯，而是來源資料本身很髒。

常見情況包括：

- 空白列
- 註解列
- header 與實際欄位不一致
- 一列裡還包著巢狀分隔資料
- delimiter 不規則

Spark 讀取 CSV 時，幾個實用選項特別重要：

- `comment='#'` 可以略過註解列
- `header=True` 可以把首列當欄名，但若已明確定義 schema，就不要同時過度依賴推斷
- `sep` 會影響 Spark 如何拆欄；若原始字串裡還有內嵌分隔符，有時反而要先保留成單欄，再做第二段解析

### Validation Inside the Pipeline

validation 不該只發生在最後輸出前。對 Spark workflow 來說，至少要在幾個關鍵點確認：

- 匯入後 schema 是否符合預期
- 清理後 row count 是否合理
- 關鍵欄位的缺值、型別或範圍規則是否被滿足
- 複雜商業規則是否能用 Spark transformations 或 join-based checks 被驗證

這種做法的重點不是把 pipeline 變得很學術，而是避免錯誤資料一路被放大到下游。

## Common Transformation Operations

很多資料轉換其實不神祕，反覆出現的就是幾種基本操作：

- 刪除空白列或 null-heavy rows
- 去除重複資料
- 取代錯誤值或補預設值
- 修正資料型別
- 篩選需要的子集
- 做 aggregation
- 合併多張表

真正的差異，通常不是操作名稱，而是你在哪個工具裡完成它。

## Low-Code, SQL, and Spark as Three Transformation Surfaces

在像 Microsoft Fabric 這類平台裡，常見會同時存在三種轉換介面：

- `Dataflows / Power Query`: 適合低程式碼的清理、型別整理、merge、filter
- `SQL`: 適合 table-oriented aggregation、join 與 warehouse-style transformation
- `Spark / notebooks`: 適合程式化處理、較大資料量與更自由的邏輯控制

選哪一個不該只看個人偏好，還要看：

- 資料量
- 團隊技能
- 是否需要重用與版本控制
- 是否需要 GUI-friendly maintenance

## Cleaning Rows and Values

最常見的資料清理，就是先處理 row-level 問題。

例如：

- 全空白列通常可以直接移除
- 重複列若不處理，後續 aggregation 很容易被放大
- 某些固定錯誤值、placeholder 或空字串，可能要統一替換

在 Spark 裡，常見手段包括：

- `dropna()` 處理 null rows
- `dropDuplicates()` 去重
- `replace()` 取代值

而在 Dataflows / Power Query 裡，這些動作通常會對應到可視化 transformation。

## Type Correction Is a Pipeline Concern

型別整理不要被當成最後才修的小事。

如果欄位型別不對，後面的：

- join
- filter
- aggregation
- semantic modeling

都可能出現難追的錯誤。

所以 pipeline 很適合在早期就明確做：

- integer / decimal casting
- date / time conversion
- categorical normalization

這一步越早做，下游越穩。

## Filtering and Aggregation

filter 與 aggregation 是把原始資料轉成分析資料的核心。

filter 的作用是：

- 限縮範圍
- 排除不需要的資料
- 聚焦到特定狀態、區域或時間窗

aggregation 的作用則是：

- 降低資料粒度
- 產生 summary
- 為報表或 feature generation 準備可消費結果

在 SQL 裡，aggregation 常透過 `GROUP BY` 與 `SUM`、`COUNT`、`AVG` 等函式完成；在 Spark 裡則常用 `groupBy().agg()`。

## Joining and Merging Data

很多分析資料產品最後都會走到 join。

join 的常見用途包括：

- 把交易資料接上維度描述
- 把多個來源拼成同一份分析表
- 建立 star schema 的 fact / dimension 關聯

常見 join 類型包括：

- inner join
- left join
- right join
- full outer join

選錯 join 類型，結果不一定會報錯，但 row count 和 business meaning 很可能已經偏掉，所以 join 後最好檢查：

- row count
- unmatched keys
- duplicate amplification

## Split-Apply-Combine and Chunk Aggregation

當資料無法一次完整放進記憶體時，常見做法不是硬把全部載入，而是把運算改寫成 split-apply-combine。

這個模式可以先簡化成：

1. 把資料切成 partitions 或 chunks
2. 對每個 partition 做同樣的計算
3. 把 partial results 合併

它特別適合：

- count
- sum
- many group-wise summaries
- 可分解的 regression / matrix 子運算

但要注意，不是所有統計量都能直接這樣拆。例如 exact median 這類需要看完整資料排序的運算，就不如 count 或 average 那麼容易用簡單 partial results 得到。

### Designing Partial Results

要讓 chunk pipeline 可擴充，partial result 的設計很重要。

例如平均數通常不會在每個 chunk 直接算出 local mean 後再平均，而是更穩定地保留：

- partial sum
- partial count

最後再從 combined sum 和 count 算出 global mean。

這種思維的重點是：combine step 要保留足夠資訊，而不是只保留看起來像最終答案的東西。

## Profiling Before and After Transformation

轉換不是做完就好，profiling 幾乎應該伴隨整個流程。

可以觀察的訊號包括：

- row count
- null ratio
- distinct values
- distribution changes
- unexpected type drift

這樣做的價值是讓清理與轉換不只是「成功執行」，而是能被驗證真的把資料往更可用的方向推進。

## Practical Reminders

- pipeline 的價值在於可靠交付，不只是在 notebook 或 script 裡把資料轉成功一次。
- batch 與 stream 不是誰比較進階，而是回應不同延遲需求。
- scheduling 是資料系統的骨架，沒有排程與依賴管理，很多自動化都只是表面上的。
- 測試 pipeline 時，不要只驗證程式碼是否執行，還要驗證資料是否真的以正確結構出現在正確位置。
- GUI、SQL、Spark 不是互斥關係，而是同一條資料流程上不同層級的轉換介面。
- 如果資料已經大到記憶體吃不下，先想 partition strategy 和 combine logic，通常比先想語法更重要。

[Back to Data Engineering](README.md)
