# Power Query in Excel

Power Query 是 Excel 裡比較接近 `repeatable data workflow` 的那一層。  
如果一般 worksheet 擅長手動輸入、公式分析與表格檢視，那 Power Query 更像是把資料匯入、清理、轉換、再載入的流程固定下來。

它最適合的不是一次性的手動修表，而是：

- 同一份資料會反覆更新
- 清理步驟每次都差不多
- 資料來自多個來源
- 想把 transformation 留下可重跑的紀錄

## Core Idea

可以把 Power Query 想成 Excel 裡的輕量 ETL 工具：

- `Extract`: 從 workbook、`CSV`、text file、資料夾或其他來源讀資料
- `Transform`: 清理、改型別、篩選、合併、衍生欄位、重塑結構
- `Load`: 把結果載回 worksheet、table，或往 Power Pivot 之類的下游模型送

它的價值不是「功能比公式多」，而是讓清理流程變成可重播，而不是每次重做。

## Workbook vs Power Query Editor

這兩層最好分工看待：

- `Excel workbook`: 適合輸入、檢查、分析、報表與視覺化
- `Power Query Editor`: 適合資料匯入、前處理、清理與轉換

實務上可以把它們想成：

- workbook 負責消費資料
- Power Query 負責整理資料

當同一份 raw data 需要反覆手動清理時，通常代表邏輯應該往 Power Query 移。

## Why It Matters

Power Query 特別適合這幾種情境：

- 每週都要匯入一批結構相近的報表
- 來源資料欄位很多，但真正要分析的只有一部分
- 資料需要先過濾、改欄名、改型別、去錯誤值後才能用
- 需要合併多張表或多個檔案
- 想保留一條別人也看得懂的資料清理路徑

如果流程每次都靠複製貼上、刪欄、手動排序、再改格式，長期通常會不穩。

## Main Transformation Categories

Power Query 常見操作可以先分成幾類：

### Import and Load

- 從多個來源讀資料
- 決定是只建立 connection，還是直接載入 workbook
- 把整理後的表送回 Excel

### Cleaning and Typing

- 修正欄位名稱
- 設定正確 data type
- 處理空值、錯誤值與格式不一致
- 排序與篩選

這一步很重要，因為後面的 grouping、join 與 aggregation 都建立在型別正確之上。

### Row and Column Transformations

- 保留或移除欄位
- 調整欄位順序
- 拆分欄位或合併欄位
- 建立 custom columns
- 對欄位做文字、日期或數值轉換

可以把它理解成把 raw schema 改造成 analysis-friendly schema。

### Shaping and Grouping

- `shaping`: 把資料重組成更適合分析的結構
- `grouping`: 依特定欄位做聚合與摘要

常見例子包括：

- wide / long 結構調整
- 依類別加總
- 依 key 匯總成單一列

### Joining Queries

- merge queries
- append queries
- 整合多份來源資料

這讓 Excel 不再只是單表操作，而能開始做比較像資料整併流程的工作。

## Combining Queries

當 Power Query 進到比較實務的資料整併階段，最常卡住的是 `append` 和 `merge` 的差別。

### Append vs Merge

- `append`: 把欄位結構相容的資料表往下堆疊
- `merge`: 依共同 key 把另一張表的欄位水平接進來

可以用一句話記：

- append 是 vertical stacking
- merge 是 horizontal enrichment

如果你的目標是把多個月份、分店、批次的同型資料合成一張大表，通常用 append。  
如果你的目標是幫既有資料補上 lookup table 的欄位，通常用 merge。

### Join Types Matter

merge 不只是把兩張表接起來而已，`join type` 會決定哪些列被保留、哪些列被排除。

實務上最常先理解的是：

- `left outer join`: 保留主表全部列，再盡量接上符合的資料
- 其他 join types: 視你要保留哪一側資料、是否只要交集而定

比起死背名稱，更重要的是先問：

- 主表是誰
- 哪些列一定要保留
- 沒對上的 key 要怎麼處理

### Merge Heuristics

做 merge 前，至少先確認兩件事：

- 兩邊用來 match 的 shared column 是否為同一個 data type
- preview 結果是否符合預期，不要只看有沒有成功跑完

很多 merge 問題不是 join 功能錯，而是 key 型別不同、key 品質不穩，或主從表邏輯一開始就沒想清楚。

## Applied Steps Is the Real Feature

Power Query 最值得養成的觀念，是把每次操作都視為一個 `step`。

`Applied Steps` 的價值在於：

- 顯示轉換順序
- 讓你知道結果是怎麼來的
- 可以回頭修改其中某一步
- 讓別人比較容易 review

這比 worksheet 裡很多隱性手動操作更容易維護。  
如果你重視可追溯性，Applied Steps 幾乎就是 Power Query 的核心。

## Documentation Mindset

在一般 Excel 工作流裡，很多清理其實沒有明確紀錄。  
Power Query 則鼓勵把整理流程留在 query 本身。

比較好的工作方式通常是：

1. 先保留 raw source。
2. 在 Power Query 中完成主要清理與重塑。
3. 只把整理後的結果載入分析用 worksheet。

這樣做的好處是，raw data、transformation、analysis output 之間的界線會更清楚。

## Power-User Features

剛開始不需要先學太深，但可以知道這些能力存在：

- `Query Dependencies Viewer`: 看 query 之間的依賴關係
- `Advanced Editor`: 直接查看或修改 query 腳本
- `M language`: Power Query 背後的轉換語言與函數系統

這些功能的定位比較像：

- 日常使用先靠介面完成大部分工作
- 當流程變複雜、需要重用邏輯時，再往 `M` 與 Advanced Editor 深入

## M and Advanced Editor

Power Query 的每個 Applied Step 背後，其實都會生成 `M code`。

幾個值得知道的事：

- 很多操作不是黑箱，它們背後都有可查看的程式化表示
- `Formula bar` 可以看單一步驟
- `Advanced Editor` 可以看整段 query
- `M` 是 case-sensitive

這代表你平常就算主要用圖形介面，也是在逐步生成可讀的 transformation script。

### Minimal Mental Model of M

Power Query 的 `let ... in ...` 結構，可以先這樣理解：

- `let`: 定義一連串步驟或變數
- `in`: 指定最後哪一步是輸出

每一步通常都建立在前一步之上，所以 query 本質上很像一條具名 transformation pipeline。

這個心智模型很重要，因為它能幫你理解：

- 為什麼 Applied Steps 有順序
- 為什麼改前面一步會影響後面
- 為什麼 query 比手動清理更可維護

## Query Parameters and Reuse

當 query 開始需要重複使用時，`Query Parameters` 會很有價值。

它的定位是：

- 把某些值抽成可傳入的 placeholder
- 讓 query 更 flexible
- 支援 dynamic filters
- 幫 custom functions 或多情境重用做準備

如果你每次都只是改日期、路徑、地區、門檻值之類的小參數，與其複製一份 query，不如考慮 parameter 化。

## Custom Columns and Conditional Logic

中階使用時，Power Query 常見的另一個升級點是：

- 建立 `custom columns`
- 用 nested conditional logic 做分類
- 在需要時加入 indexing

這些做法的重點不只是「多做一欄」，而是把原始資料轉成更接近 business-ready 的欄位。

如果某個分類邏輯每次都要在 Excel sheet 裡重新寫 `IF`，它常常也適合前移到 Power Query。

## Relation to Power Pivot

Power Query 與 Power Pivot 通常是上下游關係：

- `Power Query`: 整理資料
- `Power Pivot`: 建模、關聯、度量與分析

如果你已經開始碰到多表分析、模型關聯或量值設計，通常 Power Query 會先把資料準備好，再交給 Power Pivot。更完整的定位可以再看 [Power Pivot in Excel](power-pivot-in-excel.md)。

## When to Use It

適合用 Power Query 的訊號：

- 同一套清理規則要重跑很多次
- 公式已經變得太長、太碎、太難追
- 匯入來源很多，手動整理太花時間
- 想把 preprocessing 從分析頁面分離出去

不一定要用 Power Query 的情況：

- 只是一次性的小表修正
- 完全是人工輸入表單
- 分析非常簡單，手動整理成本很低

## Practical Heuristics

- 先把 Power Query 當成資料前處理層，不要把分析邏輯全塞進去。
- 優先修正欄位名稱與 data type，這通常是後面穩定度的基礎。
- 如果你每次更新資料都在重做一樣的清理步驟，盡早把它 query 化。
- Applied Steps 要保持可讀，不要讓流程長到自己都看不懂。
- append 前先看 schema 是否一致；merge 前先看 key 與 data type 是否一致。
- 能用 parameter 解掉的重複 query，就不要靠複製多份流程維護。
- 當需求開始進到模型關聯與量值設計時，考慮和 Power Pivot 分工。

## Mental Model

一句話總結：

Power Query 不是拿來取代 Excel，而是把 Excel 中最容易反覆出錯的資料整理工作，變成可重跑、可追蹤、可維護的流程。
