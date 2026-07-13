# Power Pivot in Excel

Power Pivot 是 Excel 裡偏向 `data modeling` 與 `analytical model` 的那一層。  
如果 Power Query 主要負責資料匯入與清理，Power Pivot 更像是把多張表建立關聯、定義計算邏輯，再讓 PivotTable / dashboard 消費。

## What It Is

可以把 Power Pivot 想成：

- Excel add-in
- 用來建立資料模型
- 用來做跨表分析與計算
- 用來支撐互動式報表

它不是單純「更進階的 PivotTable」，而是讓 Excel 開始有比較接近 semantic model 的能力。

## When It Starts to Matter

Power Pivot 比較適合這些情境：

- 不是只有一張表，而是多張相關資料表
- 需要建立 relationships
- 需要跨表計算
- 想把 calculations 做成可重用的 measures
- 想讓 PivotTables、PivotCharts、slicers 與 KPI 都建立在同一個模型上

如果只是單表彙總，普通 PivotTable 通常就夠了。  
如果已經碰到多表分析與模型關聯，Power Pivot 就會開始變有價值。

## Core Workflow

Power Pivot 的典型工作流可以想成：

1. 用 Power Query 或其他方式把資料整理好
2. 載入 Data Model
3. 建立 tables 之間的 relationships
4. 定義 calculated columns 或 measures
5. 用 PivotTables / PivotCharts / slicers 做分析與 dashboard

這也是它和 Power Query 最自然的分工：

- `Power Query`: prepare data
- `Power Pivot`: model and calculate

## Data Modeling Mindset

Power Pivot 的核心不是介面，而是資料模型觀念。

### Relationships First

資料模型的第一步通常不是先寫公式，而是先想：

- 哪些表之間有關聯
- key 是什麼
- 主表與輔助表誰是誰

如果 relationships 沒定清楚，後面的 DAX 與報表結果通常也不穩。

### Fact and Dimension Tables

Power Pivot 很適合用 `fact` / `dimension` 的方式思考：

- `fact table`: 儲存事件、交易、量值
- `dimension table`: 儲存描述性欄位，例如產品、日期、地區、客戶

這種拆法的好處是：

- 比較容易維護
- 比較容易跨表彙總
- 比較容易避免同一份描述資料被重複塞進大表

### Star Schema

在 Excel 的 Power Pivot 世界裡，`star schema` 是很實用的結構：

- 中間是 fact table
- 周圍是多張 dimension tables
- 透過 relationships 連接

這樣的模型通常比把所有欄位硬拼成一張超寬表更穩，也更適合後續分析。

## DAX as the Calculation Layer

Power Pivot 的計算語言是 `DAX`，也就是 `Data Analysis Expressions`。

可以先把 DAX 想成：

- Microsoft 分析模型常見的計算語言
- 用來建立 calculations 與 measures
- 特別適合搭配 relationships 與聚合分析

它的重要性不只是函數多，而是它讓計算能建立在模型與篩選情境之上。

## Calculated Columns vs Measures

這是 Power Pivot 最關鍵的區分之一。

### Calculated Columns

- 在 row level 計算
- 會把結果存成 table 裡的新欄位
- 通常在資料載入時計算

適合：

- 建立分類欄位
- 建立 label
- 補出後續會被切分或關聯使用的欄位

### Measures

- 聚合多筆資料
- 在視覺化與查詢情境中計算
- 產生的是可放進 PivotTable 的 field，不是實體欄位

適合：

- `SUM`
- ratio
- conversion rate
- margin
- 各種依篩選情境改變的彙總指標

一句話記：

- column 比較像 row-wise derivation
- measure 比較像 context-aware aggregation

如果需求本質是「報表上要顯示什麼彙總結果」，通常應先想 measure，而不是先做一堆 calculated columns。

## Practical DAX Entry Point

剛開始不需要一口氣學很多 DAX。  
比較實務的入口通常是：

- 建立基本 measures
- 理解它們會被 PivotTable 的 filter / slicer 影響
- 學會在模型中引用相關欄位

來源內容裡提到的 `SUM()` 與 `RELATED()`，就很能代表兩種常見方向：

- `SUM()`: 做基本聚合
- `RELATED()`: 從相關表取值

這剛好也反映了 DAX 的兩個核心角色：

- aggregation
- relationship-aware calculation

## KPI and Dashboard Layer

Power Pivot 不只是在模型內算數字，也常被拿來支撐 dashboard。

常見輸出包括：

- PivotTables
- PivotCharts
- slicers
- KPIs

`KPI` 的重點不是只是多一個指標，而是把：

- performance
- target
- trend

放到同一個分析敘事裡。

當這些元件都接在同一個 data model 上時，dashboard 會比各自獨立維護的表格更一致。

## When It Is the Right Tool

適合用 Power Pivot 的訊號：

- 單一 workbook 裡已經有多張互相關聯的表
- 你想把計算邏輯從 worksheet 公式移到模型層
- 普通 PivotTable 已經不夠表達跨表分析
- 你需要 reusable measures，而不是每張表各寫一套公式

不一定要用 Power Pivot 的情況：

- 只有單表分析
- 只做簡單彙總
- 資料規模與模型需求都很小
- 團隊其實更適合直接進 Power BI 或資料庫分析流程

## Relation to Power Query

這兩者最好不要混為一談：

- `Power Query`: extract / transform / load
- `Power Pivot`: relationships / DAX / measures / dashboards

可以把它們看成同一條 Excel analytical workflow 的上下游：

`raw data -> Power Query -> Data Model -> Power Pivot -> PivotTable / dashboard`

## Practical Heuristics

- 先把資料整理乾淨，再進 Power Pivot 建模。
- 先想 relationships，再想 DAX。
- 能用 star schema 想清楚，就不要急著把所有欄位塞成一張大表。
- 當需求是彙總指標時，優先想 measure，不要先濫建 calculated columns。
- KPI 與 dashboard 的價值來自一致的模型，不是來自更多圖表。

## Mental Model

一句話總結：

Power Pivot 是 Excel 裡把多表資料、關聯與分析計算收斂成同一個模型層的工具，而 DAX 是這個模型層的主要語言。
