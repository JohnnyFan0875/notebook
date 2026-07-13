# DAX in Power BI

`DAX` 是 Power BI 模型層最重要的計算語言之一。  
如果 Power Query 負責整理資料，semantic model 負責定義結構，那 DAX 就是在這個模型上表達計算邏輯的主要語言。

## Why DAX Exists

Power BI 的很多分析需求，不只是把原始欄位直接顯示出來，而是要：

- 建立 reusable measures
- 依不同 filter 條件重新計算結果
- 透過 relationships 做跨表分析

這些都不是單純 spreadsheet 公式的問題，而是模型內計算的問題。  
DAX 的存在，就是為了讓這種計算可以建立在 `model + context` 上。

## What DAX Is Good At

可以先把 DAX 想成特別適合這幾種事：

- aggregations
- calculated columns
- calculated measures
- context-aware calculations
- relationship-aware calculations

在 Power BI 裡，真正麻煩的往往不是加總本身，而是「在什麼範圍下加總」以及「這個結果要跟哪個篩選情境一起變」。

## Context Is the Core Idea

課程裡最重要的提醒之一是：DAX 不是只會算，它會根據 selected data 改變結果。

來源內容整理出三種 context：

- `row context`
- `filter context`
- `query context`

先不用一開始把三者講到很細，但要先知道：

- DAX 結果會跟目前的列、篩選與查詢情境一起變
- 這就是為什麼同一個 measure 放到不同 visual、不同 slicer 條件下，結果會不一樣

如果沒有 context 這個心智模型，DAX 很容易看起來像「神秘地有時對、有時不對」。

## Filter Context

`filter context` 是最常直接感受到的那種 context。

它可以先理解成：

- calculation 執行前，已經套在資料上的一組 filters

這些 filters 可能來自：

- row / column attributes
- slicer
- filter pane
- 其他 calculated measure 的邏輯

這也是 Power BI 和一般靜態計算最大的差別之一：  
數字不是孤立算出來的，而是永遠在某個篩選情境裡被計算。

## Calculated Columns vs Measures

這是 DAX 入門時最值得先分清楚的地方。

### Calculated Columns

- 逐列評估
- 會在既有 table 中新增一個欄位
- 通常在資料載入或 refresh 時計算

適合：

- 衍生分類欄位
- 補出 label
- 建立後續會被切分或關聯使用的欄位

### Measures

- 比較偏聚合與分析結果
- 不是新增實體欄位，而是新增可被 visual 使用的計算欄位
- 會跟目前的 filter / query context 一起變動

適合：

- sum
- ratio
- conditional KPI
- 依 slicer 或 report context 改變的摘要結果

一句話記：

- calculated column 比較像 row-wise derivation
- measure 比較像 context-aware aggregation

## Why Explicit Measures Are Preferred

在 Power BI 裡，很多欄位都可以被 visual 自動聚合，但來源課程特別強調：  
明確定義 `explicit measures` 往往比依賴隱式聚合更穩。

原因很實務：

- 名稱比較清楚
- 別人一看就知道它在算什麼
- 可以被其他 measures 重用
- 複雜模型比較容易維護

例如：

```dax
Total Sales = SUM(Orders[Sales])
Total Sales East = CALCULATE([Total Sales], Orders[Region] = "East")
```

這比讓報表直接拿 `Sales` 欄位再臨時決定是 `SUM`、`AVG` 還是其他聚合，更容易被理解與治理。

## CALCULATE Is a Key Function

在入門 DAX 裡，`CALCULATE()` 幾乎一定要理解。

它的典型形式是：

```dax
CALCULATE(<expression>[, <filter1> [, <filter2> [, ...]]])
```

來源內容強調了幾件事：

- `expression` 需要回傳單一值
- filters 需要能形成可計算的篩選條件
- filters 之間不應互相衝突

一個直觀範例是：

```dax
CALCULATE(SUM(Sales), Sales[Region] = "EMEA")
```

可以先把 `CALCULATE()` 理解成：

- 在修改或明確指定 filter context 後，再去算某個 expression

這也是很多「同一個指標在不同 business rule 下怎麼算」問題的入口。

## Why CALCULATE Matters

如果沒有 `CALCULATE()`，很多計算就只能被動接受目前 visual 上的篩選條件。  
有了它之後，你可以在 measure 裡主動改寫計算情境。

這讓 DAX 能做的事從單純彙總，擴展到：

- conditional measures
- region-specific logic
- business-rule driven calculations
- 更精準的 KPI 定義

## Variables Make Measures Easier to Read

當 measure 開始變複雜時，`VAR ... RETURN` 幾乎是最值得早點使用的技巧之一。

它的好處包括：

- 把中間結果命名
- 避免重複計算
- 讓公式更容易 review

例如：

```dax
Sales Growth =
VAR SalesPriorYear =
    CALCULATE([Sales], SAMEPERIODLASTYEAR('Date'))
RETURN
    [Sales] - SalesPriorYear
```

如果同一段邏輯會被後面多次引用，用 variable 通常比把整段公式複製很多次更穩。

## Common Function Families

這份來源最有價值的不是把函數表背完，而是幫你建立幾個常見函數族的使用感。

### Filter-Shaping Functions

最常見的是：

- `CALCULATE()`
- `FILTER()`
- `ALL()`

它們常一起出現，因為都跟「目前要在哪個範圍下計算」有關。

#### FILTER

`FILTER(<table>, <filter>)` 會回傳一個過濾後的 table。

常見搭配方式：

```dax
Total Sales Chuck =
CALCULATE(
    [Total Sales],
    FILTER(
        Fact_Orders,
        RELATED(Dim_Sales[Salesperson]) = "Chuck"
    )
)
```

這裡真正重要的不是語法本身，而是觀念：

- 先建立一個更窄的 table context
- 再在那個 context 上做計算

#### ALL

`ALL()` 常用來暫時拿掉某個欄位或 table 的篩選，讓你在更完整的集合上做比較。

例如：

```dax
Total Costs Rank =
RANKX(
    ALL(Dim_Sales[Region]),
    [Total Costs]
)
```

這裡的 `ALL(Dim_Sales[Region])` 很重要，因為 rank 要基於所有 region，而不是只基於目前 visual 已經被限制的那一小部分。

## Date-Oriented Calculations

當分析開始碰到 trend、period comparison 或 time-series reporting 時，DAX 常會和日期欄位綁得更緊。

來源裡提到幾個很基本但實用的函式：

- `DATE()`
- `LEFT()`
- `RIGHT()`
- `MID()`
- `WEEKDAY()`

這些函式本身不一定都是典型 time-intelligence 函式，但它們很常出現在：

- 從文字或零散欄位組出 date
- 抽取日期成分
- 先把時間欄位整理成可用形狀

### Building Dates from Parts

`DATE()` 的定位很直接：

- 用 year / month / day 組出真正的 date value

如果來源資料的日期不是原生日期型別，而是拆成多欄或混雜字串，這會是很常見的第一步。

### Extracting Date Parts from Text

`LEFT()`、`RIGHT()`、`MID()` 雖然是文字函式，但在 Power BI 裡常被拿來：

- 從固定格式日期字串抽出年、月、日
- 先把不乾淨的日期欄位整理成後續可轉型的中間結果

這也提醒一件事：

- 如果日期欄位本身不乾淨，很多 trend / period comparison 其實根本還沒準備好開始

### Weekday as a Reporting Attribute

`WEEKDAY()` 常用來把 date 轉成 weekday number。  
這很適合：

- weekday pattern analysis
- 週內節奏比較
- 把日資料再切成更穩定的 reporting slice

## Period-over-Period Thinking

Trend analysis 裡最常見的比較之一，是：

- 本期 vs 前一期

例如：

- `MoM`
- `QoQ`
- `YoY`

即使來源只明確提到 `MoM change`，背後更重要的心法是：

- trend 不只看 level
- 也要看 change

這種比較通常會變成 measure 設計問題，而不是單純 visual formatting 問題。

如果 date table、sorting 或 grain 沒先處理好，period-over-period calculations 也很容易出錯。

### Relationship-Aware Functions

來源裡最值得先記的是：

- `RELATED()`
- `CROSSFILTER()`
- `USERELATIONSHIP()`

#### RELATED

`RELATED()` 用來從另一張相關表取值。

它通常出現在：

- 需要用 dimension 欄位去限制 fact table
- 需要在一張表內引用已建立 relationship 的另一張表欄位

如果 model relationship 沒設好，`RELATED()` 類用法通常也不會順。

#### CROSSFILTER

`CROSSFILTER(<col1>, <col2>, <direction>)` 用來在 calculation 中暫時指定 cross-filtering direction。

它的定位比較偏進階：

- 不只是算值
- 而是改寫 relationship 在該計算裡的過濾方向

實務上可以先把它當成：

- 處理特定 relationship behavior 的工具
- 不是日常第一個該拿出來用的函數

#### USERELATIONSHIP

`USERELATIONSHIP()` 很適合處理 multiple relationships 的情境。

最典型的例子是同一張 fact table 同時有：

- order date
- ship date
- delivery date

在這種模型裡，通常只有一條 relationship 會是 active。  
`USERELATIONSHIP()` 的作用，就是在某個 calculation 中明確指定要改用哪一條關係。

可以先把它理解成：

- 不是建立 relationship
- 而是在 measure 裡啟用一條既有但非預設的 relationship

如果角色型日期很多，這個函數通常比把模型改成一堆雙向關係更乾淨。

### Iterator Functions

來源裡很明確地把 `X` 類函數凸顯出來，這很值得保留。

常見包括：

- `SUMX()`
- `AVERAGEX()`
- `RANKX()`

這類函數的共同點是：

- 先逐列或逐項迭代一個 table
- 再對 expression 做計算

#### SUMX

`SUMX(<table>, <expression>)` 很適合在「先逐列算，再加總」的情境。

例如：

```dax
Total Costs East SUMX =
SUMX(
    FILTER(
        Fact_Orders,
        Fact_Orders[Region] = "East"
    ),
    Fact_Orders[Sales] - Fact_Orders[Profit]
)
```

這和直接 `SUM()` 一個現成欄位不同，因為它是在每列先算出 `Sales - Profit`，再把結果加總。

#### RANKX

`RANKX()` 用來在一組集合內做排名。

它幾乎都需要你先想清楚：

- ranking universe 是誰
- 要不要用 `ALL()` 拿掉目前篩選

如果這兩件事沒先想清楚，排名很容易只是在目前局部視圖裡排序，而不是你真正想要的全域排序。

### Counting and Table-Based Aggregation

`COUNTROWS(<table>)` 很常被低估。

它的價值不只是在「數筆數」，而是：

- 很適合搭配 filtered table
- 很適合在 model 裡表達事件數、符合條件筆數或 bridge / factless 關係數量

比起只對某欄做傳統 count，`COUNTROWS()` 往往更貼近模型層問題。

### Time Intelligence

來源裡最實用的 time-intelligence 例子是：

```dax
SalesPriorYear =
CALCULATE([Sales], SAMEPERIODLASTYEAR('Date'))
```

這個例子很適合當入門心智模型，因為它同時告訴你：

- time intelligence 通常不是單靠日期欄就好
- 它常和 `CALCULATE()` 一起用
- 它本質上是在改寫比較基準的時間範圍

學 time intelligence 時，比起背一串函數名，先理解「這是在改時間 context」通常更重要。

進一步常見的累積函數還包括：

- `TOTALYTD()`
- `TOTALQTD()`
- `TOTALMTD()`

它們的共同定位是：

- 在既有 expression 上做 year / quarter / month to date 的累積
- 依賴正確的日期欄位與日期模型

例如：

```dax
Sum_YTD =
TOTALYTD(
    SUM(Fact_Table[Value]),
    Dim_Date[Date Key]
)
```

如果模型裡沒有穩定的 date dimension，time-intelligence 類函數通常也不會穩。

## Logical Branching with SWITCH

當條件分支開始變多時，`SWITCH()` 往往比層層 nested `IF()` 更可讀。

它適合兩種常見模式：

- 對固定離散值做映射
- 用 `SWITCH(TRUE(), ...)` 寫條件分段

例如依數值區間分類：

```dax
Performance =
SWITCH(
    TRUE(),
    [Total_Sales] < 25000, "Poor",
    [Total_Sales] < 50000, "Below expectations",
    [Total_Sales] < 75000, "Above expectations",
    "Exceptional"
)
```

或依類別直接指定結果：

```dax
Discount =
SWITCH(
    [Clothing Type],
    "Shoes", 0.15,
    "Pants", 0.20,
    "Belts", 0.30,
    "T-shirt", 0.25
)
```

如果需求本質是「把一組條件或類別映射成結果」，`SWITCH()` 通常比把邏輯拆成很多 `IF()` 更容易維護。

## Table Manipulation Functions

DAX 不只會回傳 scalar，也能回傳 table。  
這也是它和單純 worksheet 公式很不一樣的地方。

來源裡值得保留的兩個 table-manipulation function 是：

- `ADDCOLUMNS()`
- `SUMMARIZE()`

### ADDCOLUMNS

`ADDCOLUMNS(<table>, <name>, <expression>)` 會在既有 table 的基礎上附加新欄位。

例如：

```dax
ADDCOLUMNS(
    Fact_Table,
    "Profit",
    Revenue - Costs
)
```

可以先把它理解成：

- 保留原 table
- 再在同一個結果上補新的衍生欄位

### SUMMARIZE

`SUMMARIZE(<table>, <groupBy_columnName>, <name>, <expression>)` 用來依群組產生 summary table。

它的定位比較像：

- 先 group by
- 再產生每組對應的彙總結果

這在需要建立 grouped analytical table 時很有用，但它也比較容易受 context 影響。

### SUMMARIZE Best Practice

來源裡有一個很實務的提醒：

- 直接在 `SUMMARIZE()` 裡建立新欄位，可能因為 context 導致意外結果
- 建立新欄位時，通常更穩的做法是用 `ADDCOLUMNS(SUMMARIZE(...), ...)`

也就是說：

- `SUMMARIZE()` 比較偏定義 grouping shape
- `ADDCOLUMNS()` 比較偏把額外計算補上去

這種拆法通常比把所有事情一次塞進 `SUMMARIZE()` 更可控。

## Mental Model for Beginners

剛開始學 DAX 時，可以先用這個順序理解：

1. 先分清楚 column 和 measure
2. 再理解 context 為什麼會讓同一公式在不同地方結果不同
3. 最後再把 `CALCULATE()` 當成主動調整 filter context 的工具
4. 接著再學 `FILTER()`、`ALL()`、`SUMX()` 這些最常改變計算範圍與計算方式的函數
5. 當分支、時間累積或 summary table 開始出現時，再學 `SWITCH()`、`TOTALYTD()`、`ADDCOLUMNS()`、`SUMMARIZE()`

這樣通常會比一開始就背很多函數更穩。

## Relation to Semantic Models

DAX 幾乎不應該被脫離 semantic model 單獨理解。

因為：

- relationships 會影響計算範圍
- filter flow 會影響結果
- model 設計會決定 measures 是否可重用

所以 DAX 問題常常不是只有公式問題，也可能是模型問題。

如果你想先補模型層背景，可以先看 [Semantic Models and Power BI](semantic-models-and-power-bi.md)。

## Relation to Power Pivot

如果你是從 Excel 生態進來，也可以對照 [Power Pivot in Excel](/home/johnny_fan/project/notebook/docs/productivity/microsoft-office/power-pivot-in-excel.md)。

兩者共通點是：

- 都使用 DAX
- 都建立在模型與 relationships 上
- 都會遇到 column / measure 的區分

差別比較多在平台與報表消費方式，而不是 DAX 的核心邏輯。

## Practical Heuristics

- 先問需求是 row-wise derivation 還是 aggregation，再決定用 column 還是 measure。
- 優先建立 explicit measures，不要太依賴 visual 的隱式聚合。
- DAX 算錯時，先檢查 context，不要第一時間只懷疑函數語法。
- `CALCULATE()` 很重要，但別把它當萬能修補；模型與 relationships 先正確更重要。
- 當你需要「先逐列算、再聚合」時，優先想到 `X` 類 iterator functions。
- 當你需要比較全體排名、全體總和或基準值時，先想清楚是否需要 `ALL()`。
- 公式一長就用 `VAR`，通常比把相同邏輯重寫多次更好維護。
- 條件分支很多時，優先考慮 `SWITCH()`，通常比多層 `IF()` 更可讀。
- 需要建立 grouped summary table 時，先想 `SUMMARIZE()`，但新增欄位時常以 `ADDCOLUMNS(SUMMARIZE(...), ...)` 更穩。
- 如果一個指標需要跟 slicer、filter pane、visual scope 一起變，通常更像 measure 問題。
- DAX 最常見的難點不是函數數量，而是「目前到底在什麼 context 下計算」。

## Mental Model

一句話總結：

DAX 是 Power BI semantic model 上的計算語言，而它真正的難點與價值，都來自 context。
