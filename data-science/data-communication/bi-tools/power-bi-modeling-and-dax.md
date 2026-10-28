# Power BI Modeling and DAX

先建立 Power BI 的整體地圖（Desktop / Service、views、互動），再看 semantic model（relationships、RLS / OLS）與 DAX（context、measures、`CALCULATE()`）。資料前處理見 [Power Query](power-query.md)，報表設計見 [Power BI Reports](power-bi-reports.md)。

## Power BI Overview

Power BI 可以先理解成一個把資料整理、資料模型、視覺化與分享串起來的 BI 工作流。  
它不只是畫圖工具，而是讓資料從 `dataset -> model -> report -> shared consumption` 走完最後一段。

### Why It Matters

很多團隊以為 BI 工具只是報表外觀問題，但實際上 Power BI 同時碰到：

- data preparation
- data modeling
- interactive reporting
- cloud sharing and distribution

所以它的價值不只是「做 dashboard」，而是把資料轉成能被業務使用的分析介面。

### Core Components

#### Power BI Desktop

`Power BI Desktop` 是本機端的分析與報表製作工具。

它通常負責：

- 載入資料
- 使用 Power Query Editor 做清理與轉換
- 建立模型
- 製作報表

可以把它理解成主要的 authoring environment。  
很多資料準備與報表設計工作，都是在 Desktop 完成。

#### Power BI Service

`Power BI Service` 是 cloud-based 的分享與分發層。

它比較偏向：

- publish reports
- share and distribute content
- 協作與報表消費

簡單說：

- Desktop 偏建立
- Service 偏發布與使用

如果你想把資料來源、storage mode、gateway 與 refresh 這一層拆開來看，可以接著讀 [Power Query: Data Connections](power-query.md#data-connections)。

### A Simple Working Model

Power BI 的入門流程可以先想成：

1. 載入一個或多個 datasets
2. 用 Power Query Editor 清理資料
3. 建立基本 data model
4. 在 Report view 建第一份互動式報表
5. 用 Service 分享給其他人

這個流程看起來簡單，但它已經包含了 BI 工作裡最核心的幾個層次。

### Views in Power BI

課程裡反覆出現的三個 view 很值得先記住：

- `Table view`: 看資料表內容與欄位
- `Model view`: 看 tables 與 relationships
- `Report view`: 建立與編輯視覺化

這三個 view 其實就是三種思考層次：

- data
- structure
- presentation

如果報表有問題，先判斷它是資料內容、模型結構，還是視覺呈現的問題，通常會比較快找到根源。

### Data Preparation Is Part of BI

Power BI 不是把髒資料直接拿來畫圖。

在匯入階段，dataset 常見問題包括：

- 多餘欄位
- 不一致格式
- 多餘字元
- blank rows

所以資料清理不是前置雜事，而是 BI workflow 的一部分。  
Power Query Editor 在這裡扮演的角色，和 Excel / Fabric / Power Query 系列工具是一致的。

如果想把這一層再拆細來看，可以接著讀 [Power Query: Data Preparation](power-query.md#data-preparation)。

### Visualizing Data

Power BI 的核心輸出是互動式視覺化，但真正重要的不是圖表數量，而是：

- 有沒有對應正確問題
- 能不能支援探索
- 篩選與互動是否合理

如果你想把 `report`、`dashboard`、bookmark state、tooltip 與 Q&A 這一層拆開來看，可以接著讀 [Power BI Reports](power-bi-reports.md#report-structure-and-navigation)。

常見視覺化類型包括：

- table
- matrix
- card
- multi-row card
- gauge chart
- KPI

這些元件各自適合不同任務：

- table / matrix 適合明細與交叉檢視
- card 類適合單一指標摘要
- gauge / KPI 類適合目標與表現差距

### Filtering and Interactivity

Power BI 的強項之一是讓使用者不是只看靜態圖，而是可以互動式地縮小問題範圍。

常見過濾層級有：

- `visual-level filters`
- `page-level filters`
- `report-level filters`

可以把它們理解成不同作用範圍的控制：

- 只影響單一 visual
- 影響同一頁
- 影響整份報表

這個分層很重要，因為很多報表混亂，不是因為圖做不好，而是因為 filter scope 沒設清楚。

#### Controlling Interactions

互動不一定越多越好。

有些情況下，你反而要：

- 關掉某些 visual interaction
- 避免使用者誤以為所有圖都應該互相影響

所以 interactivity 應該被設計，不應該只是預設開著。

### Hierarchies and Drill-Down

Power BI 很常搭配：

- hierarchies
- drill-down paths
- sorting

這些能力的價值在於，使用者可以從較高層摘要一路往下看細節，而不是在同一層級塞滿所有資訊。

如果資料本身有天然層次，例如：

- 年 -> 季 -> 月
- 地區 -> 城市 -> 門市
- 類別 -> 子類別 -> 產品

那 hierarchy 和 drill-down 通常會比把全部欄位直接攤平更自然。

### Report Design Is Not the Same as Data Modeling

Power BI 很容易讓人混淆兩件事：

- 建模
- 做報表

這兩者當然相關，但最好分開思考：

- model 決定數字是否可信、欄位是否能重用
- report 決定資訊是否容易被理解與操作

這也是為什麼 Power BI 工作流通常不是從「選哪個圖」開始，而是從資料與模型是否穩開始。

如果你想把報表層的 progressive disclosure、themes、bookmarks 與 mobile layout 拆開來看，可以接著讀 [Power BI Reports: Design](power-bi-reports.md#report-design)。

### Relation to Semantic Models


兩篇的分工可以簡單記成：

- `Power BI Overview`: 平台元件、工作流、視覺化與互動
- `Semantic Models and Power BI`: relationships、security、semantic layer 與可治理的分析模型

### Practical Heuristics

- 先確認資料與模型正確，再優化圖表外觀。
- 不要把所有互動都打開；先決定哪些 visual 應該互相影響。
- 選圖表前先問：使用者是要看明細、比較、趨勢，還是 KPI。
- filter scope 要明確，不然使用者很容易誤判數字變化原因。
- Desktop 和 Service 最好分工理解，不要把「做報表」和「分享報表」混成同一件事。

### Mental Model

一句話總結：

Power BI 是把資料清理、模型、互動式視覺化與分享交付串成同一條分析消費流程的 BI 平台。

## Semantic Models


### Why a Semantic Layer Exists

資料被擷取、清理、落地之後，還不代表分析者就能直接安全地使用它。

semantic model 的角色，是把底層資料整理成：

- 比較容易理解的 business-facing structure
- 可建立 relationships 的分析模型
- 能被 Power BI 或其他 BI 工具穩定消費的語意層

可以把它理解成：semantic layer 站在 raw tables 和最終報表之間，負責把技術性資料結構轉成較適合分析的邏輯資料表示。

### What a Semantic Model Does

semantic model 常見功能包括：

- 簡化複雜資料結構
- 建立跨表 relationships
- 讓 measures、filters、hierarchies 更容易重複使用
- 把權限與資料可見性控制放到報表層之前

如果沒有這一層，很多報表雖然也能做出來，但會變成每一份報表都各自重做邏輯，維護成本很快失控。

### Lakehouse, Warehouse, and Auto-Creation

在像 Microsoft Fabric 這類平台裡，semantic model 常能和 lakehouse 或 warehouse 更直接連動。

課程裡強調的一個重點是：

- semantic model 可以在建立 lakehouse / warehouse 時被自動建立

這代表語意層不再只是 BI 工具外掛，而是更早就進入資料平台設計的一部分。

### Relationships Matter

semantic model 最重要的工作之一，是把多張表之間的欄位關係明確化。

常見做法是：

- 找出 matching columns
- 用這些欄位建立 relationships
- 讓不同 tables 的資料能被一起分析

這一步的價值不只是 join 比較方便，而是讓報表與下游分析不必每次都重新猜資料該怎麼拼。

在 Power BI 實務裡，這通常代表：

- fact table 與 dimension table 的角色要清楚
- key 要能穩定建立 relationships
- 模型形狀最好盡量接近 star schema
- cross-filtering direction 要盡量可預期

不是所有可連的表都應該直接連上去；過度複雜的關聯網路會讓 filter propagation 和報表解讀都更難。

#### Filter Direction

relationship 不只是「有沒有連上」，還包含 filter 如何傳播。

在 Power BI 裡，最常見的穩定做法是：

- filter 從 dimension 傳到 fact
- 盡量維持 single-direction relationships

這樣的好處是：

- filter path 較容易推理
- 報表結果較不容易出現意外傳播
- model behavior 更接近 star schema 的直覺

bi-directional filtering 並不是不能用，但它通常應該被視為例外，而不是預設。

#### Bi-Directional Filtering as an Exception

bi-directional filtering 最常被拿來處理的一種需求，是：

- 只顯示與目前情境相關的 slicer entries

但它也會帶來代價：

- relationship path 更容易變複雜
- 兩表之間若出現多條路徑，模型推理會變難
- many-to-many 或複雜維度網路時更容易拖慢效能

所以比較穩的心法通常是：

- 先假設 single-direction
- 只有在特定互動需求真的需要時，才評估 bi-directional
- 如果可以用 measure 或更明確的邏輯替代，就盡量不要用雙向關係當萬用解法

#### Multiple Relationships and Role Semantics

有些模型會在同兩張表之間需要多個 relationships，例如：

- order date
- ship date
- delivery date

在 Power BI 裡，這通常代表：

- 可以建立多個 relationships
- 但同時間通常只會有一個 active relationship

這個限制其實是好事，因為它迫使模型把主要語意先講清楚，而不是讓多條關係同時模糊地生效。

#### Hierarchies Depend on Model Clarity

semantic model 也常負責提供 hierarchies，讓報表可以更自然地 drill down。

常見例子：

- year -> quarter -> month
- country -> state -> city
- category -> subcategory -> product

如果 hierarchy 的層級在業務世界本來就存在，通常可以把它視為 natural hierarchy。  
如果只是為了分析操作方便而組出多層切法，則更接近 artificial hierarchy。

兩者都能用，但前者通常比較容易被使用者理解。

### Reports Depend on Model Quality

Power BI 報表看起來像是視覺化問題，但實際上常受 semantic model 品質支配。

如果模型本身：

- relationships 不清楚
- 欄位命名不穩定
- measures 到處散落
- 權限邏輯沒有先設計

那報表再漂亮也很難長期維護。

所以「有效的 Power BI 報表」通常不是從畫圖開始，而是先從 model design 開始。

這也是為什麼在 Power BI 世界裡，常常會說：

- 好的 report 往往是好的 model 的結果
- 不好的 model 會把簡單視覺化也變成維護噩夢

### Security in Semantic Models

semantic layer 的另一個核心角色，是把資料安全控制推進到分析消費層。

課程特別提到兩種常見控制方式：

- `RLS`: Row-Level Security
- `OLS`: Object-Level Security

#### Row-Level Security

RLS 會限制使用者能看到哪些 rows。

它適合：

- 區域別資料隔離
- 業務單位各看各的數據
- 同一份模型服務多種角色，但每個角色只能看部分資料

在 Power BI / semantic model 世界裡，RLS 常透過角色與 DAX filters 配置。

如果需要做 dynamic RLS，常見做法是讓 DAX 依登入者身分決定可見資料範圍。  
來源內容特別提到 `USERPRINCIPALNAME()`：

- 會回傳使用者的 `UPN`
- 通常可視為 email address
- 在 Power BI Desktop 與 Service 之間的行為較一致

這讓模型可以依使用者身分套用不同過濾條件，形成 personalized dashboards，而不必為每個人各做一份報表。

#### RLS Depends on Service-Side Assignment

課程裡還補了一個很重要的實務分工：

- roles 常在 `Power BI Desktop` 定義
- 使用者或群組的指派常在 `Power BI Service` 完成

這提醒我們，RLS 不是單純的 DAX 技巧，而是：

- model design
- service deployment
- user/group management

一起成立才會真的生效。

#### RLS Limitations

RLS 雖然很重要，但不是零成本能力。

來源裡提到兩個很值得保留的限制：

- 額外的 row filtering 可能拖慢查詢效能
- 擁有較高資料集寫入 / 修改權限的人，通常不應被視為 RLS 的保護對象

所以比較穩的心法是：

- 用 RLS 保護 consumer-facing access
- 不要把它當成可以約束高權限作者的萬能機制

#### Object-Level Security

OLS 會限制整個 object 的存取，例如：

- 某張 table
- 某個 column

它適合拿來保護比較敏感的欄位或結構，而不只是把資料列做過濾。

#### Dataset Permissions

在 Service 端，semantic model 還有一層很實務的 `dataset permissions`。

來源把它拆成幾個常見能力：

- `Read`: 可用既有內容讀資料，但不代表能自由探索或發現所有相依內容
- `Build`: 可基於 dataset 建新內容
- `Reshare`: 可把存取再分享出去
- `Write`: 可修改 dataset metadata

這個拆法很有價值，因為它提醒我們：

- 看得到報表
- 能不能基於同一個模型再做新內容
- 能不能把權限再擴散給別人

其實是三件不同的事。

#### Workspace Role and Dataset Capability Are Related but Not Identical

workspace role 常會影響 dataset permission 的上限，但兩者不是同一句話。

實務上最好分開想：

- workspace role: 你在協作容器裡能做什麼
- dataset permission: 你對某個 semantic model 能做什麼

這樣比較不容易因為「他看得到 report」就誤以為「他也能 build 新報表」。

#### Sensitivity Labels

如果 semantic model 或報表承載敏感資訊，還可以再往上加一層 `sensitivity labels`。

這層的意義通常是：

- 標示內容敏感程度
- 配合組織的合規與保護流程
- 在匯出、分享或後續流通時保留保護語意

對 notebook 來說，最重要的不是操作步驟，而是先記住：

- security 不只是在 query 時過濾 rows
- 還包含內容離開報表之後，能不能被適當標示與保護

### Why This Matters for Data Engineering

semantic model 看起來比較像 BI 或 analytics engineering 的工作，但它和 data engineering 很有關係，因為：

- 上游 schema 設計會直接影響 relationship 建模
- 權限模型需要和 storage / governance 一起思考
- 若 ingestion 與 warehouse 建構不穩，semantic layer 也很難穩

換句話說，semantic layer 不是資料工程的外部世界，而是資料供應鏈的最後一段整理與控制。

### Practical Design Questions

在建立 semantic model 前，先回答這些問題通常很有幫助：

- 哪些 tables 應該直接暴露給報表使用
- 哪些欄位只是工程用途，不該出現在分析層
- relationships 應該如何定義才最符合 business logic
- 是否需要依角色做 row filtering
- 是否有敏感欄位需要用 OLS 隱藏

### Practical Reminders

- semantic model 的價值是降低報表重工，不只是多一層抽象。
- relationship 錯了，整份報表的數字都可能看起來合理卻完全錯。
- single-direction relationships 通常比雙向關係更穩，也更接近 star schema 的設計直覺。
- 若模型需要很多例外 filter paths，通常該先回頭檢查 schema 與 dimension 設計，而不是一直疊 relationship 設定。
- RLS 和 OLS 應該被當成分析層治理的一部分，而不是最後才補上的權限開關。
- 如果 lakehouse、warehouse、semantic model 是同一平台內協作，越早把命名、欄位與安全邊界講清楚，後面越省事。
- 在 Power BI 中，能用 star schema 清楚表達的模型，通常比讓 dimension 彼此互連的模型更穩。

## DAX

`DAX` 是 Power BI 模型層最重要的計算語言之一。  
如果 Power Query 負責整理資料，semantic model 負責定義結構，那 DAX 就是在這個模型上表達計算邏輯的主要語言。

### Why DAX Exists

Power BI 的很多分析需求，不只是把原始欄位直接顯示出來，而是要：

- 建立 reusable measures
- 依不同 filter 條件重新計算結果
- 透過 relationships 做跨表分析

這些都不是單純 spreadsheet 公式的問題，而是模型內計算的問題。  
DAX 的存在，就是為了讓這種計算可以建立在 `model + context` 上。

### What DAX Is Good At

可以先把 DAX 想成特別適合這幾種事：

- aggregations
- calculated columns
- calculated measures
- context-aware calculations
- relationship-aware calculations

在 Power BI 裡，真正麻煩的往往不是加總本身，而是「在什麼範圍下加總」以及「這個結果要跟哪個篩選情境一起變」。

### Context Is the Core Idea

課程裡最重要的提醒之一是：DAX 不是只會算，它會根據 selected data 改變結果。

來源內容整理出三種 context：

- `row context`
- `filter context`
- `query context`

先不用一開始把三者講到很細，但要先知道：

- DAX 結果會跟目前的列、篩選與查詢情境一起變
- 這就是為什麼同一個 measure 放到不同 visual、不同 slicer 條件下，結果會不一樣

如果沒有 context 這個心智模型，DAX 很容易看起來像「神秘地有時對、有時不對」。

### Filter Context

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

### Calculated Columns vs Measures

這是 DAX 入門時最值得先分清楚的地方。

#### Calculated Columns

- 逐列評估
- 會在既有 table 中新增一個欄位
- 通常在資料載入或 refresh 時計算

適合：

- 衍生分類欄位
- 補出 label
- 建立後續會被切分或關聯使用的欄位

#### Measures

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

### Why Explicit Measures Are Preferred

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

### CALCULATE Is a Key Function

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

### Why CALCULATE Matters

如果沒有 `CALCULATE()`，很多計算就只能被動接受目前 visual 上的篩選條件。  
有了它之後，你可以在 measure 裡主動改寫計算情境。

這讓 DAX 能做的事從單純彙總，擴展到：

- conditional measures
- region-specific logic
- business-rule driven calculations
- 更精準的 KPI 定義

### Variables Make Measures Easier to Read

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

### Common Function Families

這份來源最有價值的不是把函數表背完，而是幫你建立幾個常見函數族的使用感。

#### Filter-Shaping Functions

最常見的是：

- `CALCULATE()`
- `FILTER()`
- `ALL()`

它們常一起出現，因為都跟「目前要在哪個範圍下計算」有關。

##### FILTER

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

##### ALL

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

### Date-Oriented Calculations

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

#### Building Dates from Parts

`DATE()` 的定位很直接：

- 用 year / month / day 組出真正的 date value

如果來源資料的日期不是原生日期型別，而是拆成多欄或混雜字串，這會是很常見的第一步。

#### Extracting Date Parts from Text

`LEFT()`、`RIGHT()`、`MID()` 雖然是文字函式，但在 Power BI 裡常被拿來：

- 從固定格式日期字串抽出年、月、日
- 先把不乾淨的日期欄位整理成後續可轉型的中間結果

這也提醒一件事：

- 如果日期欄位本身不乾淨，很多 trend / period comparison 其實根本還沒準備好開始

#### Weekday as a Reporting Attribute

`WEEKDAY()` 常用來把 date 轉成 weekday number。  
這很適合：

- weekday pattern analysis
- 週內節奏比較
- 把日資料再切成更穩定的 reporting slice

### Period-over-Period Thinking

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

#### Relationship-Aware Functions

來源裡最值得先記的是：

- `RELATED()`
- `CROSSFILTER()`
- `USERELATIONSHIP()`

##### RELATED

`RELATED()` 用來從另一張相關表取值。

它通常出現在：

- 需要用 dimension 欄位去限制 fact table
- 需要在一張表內引用已建立 relationship 的另一張表欄位

如果 model relationship 沒設好，`RELATED()` 類用法通常也不會順。

##### CROSSFILTER

`CROSSFILTER(<col1>, <col2>, <direction>)` 用來在 calculation 中暫時指定 cross-filtering direction。

它的定位比較偏進階：

- 不只是算值
- 而是改寫 relationship 在該計算裡的過濾方向

實務上可以先把它當成：

- 處理特定 relationship behavior 的工具
- 不是日常第一個該拿出來用的函數

##### USERELATIONSHIP

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

#### Iterator Functions

來源裡很明確地把 `X` 類函數凸顯出來，這很值得保留。

常見包括：

- `SUMX()`
- `AVERAGEX()`
- `RANKX()`

這類函數的共同點是：

- 先逐列或逐項迭代一個 table
- 再對 expression 做計算

##### SUMX

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

##### RANKX

`RANKX()` 用來在一組集合內做排名。

它幾乎都需要你先想清楚：

- ranking universe 是誰
- 要不要用 `ALL()` 拿掉目前篩選

如果這兩件事沒先想清楚，排名很容易只是在目前局部視圖裡排序，而不是你真正想要的全域排序。

#### Counting and Table-Based Aggregation

`COUNTROWS(<table>)` 很常被低估。

它的價值不只是在「數筆數」，而是：

- 很適合搭配 filtered table
- 很適合在 model 裡表達事件數、符合條件筆數或 bridge / factless 關係數量

比起只對某欄做傳統 count，`COUNTROWS()` 往往更貼近模型層問題。

#### Time Intelligence

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

### Logical Branching with SWITCH

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

### Table Manipulation Functions

DAX 不只會回傳 scalar，也能回傳 table。  
這也是它和單純 worksheet 公式很不一樣的地方。

來源裡值得保留的兩個 table-manipulation function 是：

- `ADDCOLUMNS()`
- `SUMMARIZE()`

#### ADDCOLUMNS

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

#### SUMMARIZE

`SUMMARIZE(<table>, <groupBy_columnName>, <name>, <expression>)` 用來依群組產生 summary table。

它的定位比較像：

- 先 group by
- 再產生每組對應的彙總結果

這在需要建立 grouped analytical table 時很有用，但它也比較容易受 context 影響。

#### SUMMARIZE Best Practice

來源裡有一個很實務的提醒：

- 直接在 `SUMMARIZE()` 裡建立新欄位，可能因為 context 導致意外結果
- 建立新欄位時，通常更穩的做法是用 `ADDCOLUMNS(SUMMARIZE(...), ...)`

也就是說：

- `SUMMARIZE()` 比較偏定義 grouping shape
- `ADDCOLUMNS()` 比較偏把額外計算補上去

這種拆法通常比把所有事情一次塞進 `SUMMARIZE()` 更可控。

### Mental Model for Beginners

剛開始學 DAX 時，可以先用這個順序理解：

1. 先分清楚 column 和 measure
2. 再理解 context 為什麼會讓同一公式在不同地方結果不同
3. 最後再把 `CALCULATE()` 當成主動調整 filter context 的工具
4. 接著再學 `FILTER()`、`ALL()`、`SUMX()` 這些最常改變計算範圍與計算方式的函數
5. 當分支、時間累積或 summary table 開始出現時，再學 `SWITCH()`、`TOTALYTD()`、`ADDCOLUMNS()`、`SUMMARIZE()`

這樣通常會比一開始就背很多函數更穩。

### Relation to Semantic Models

DAX 幾乎不應該被脫離 semantic model 單獨理解。

因為：

- relationships 會影響計算範圍
- filter flow 會影響結果
- model 設計會決定 measures 是否可重用

所以 DAX 問題常常不是只有公式問題，也可能是模型問題。


### Relation to Power Pivot

如果你是從 Excel 生態進來，也可以對照 [Power Pivot in Excel](../../../productivity/microsoft-office/power-pivot-in-excel.md)。

兩者共通點是：

- 都使用 DAX
- 都建立在模型與 relationships 上
- 都會遇到 column / measure 的區分

差別比較多在平台與報表消費方式，而不是 DAX 的核心邏輯。

### Practical Heuristics

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

### Mental Model

一句話總結：

DAX 是 Power BI semantic model 上的計算語言，而它真正的難點與價值，都來自 context。
