# Power Query

Power Query 是 Power BI 的資料擷取與清理層：連資料來源、選 storage mode、把清理與轉換記成可重跑的 `Applied Steps`（底層是 M language）。本篇依序是連線、清理、重塑。模型與 DAX 見 [Power BI Modeling and DAX](power-bi-modeling-and-dax.md)。

## Data Connections

Power BI 的連線層可以先理解成：  
它決定資料從哪裡來、怎麼被載入、什麼時候刷新，以及哪些能力能在模型與報表層使用。


### Why This Layer Matters

很多報表問題表面上看起來像視覺化或 DAX 問題，但根源其實在連線層：

- 資料來源選錯
- storage mode 不合適
- refresh 策略不穩
- gateway 或 credentials 沒設好

所以在 Power BI 裡，連線不是單純的「把資料接進來」，而是整個 consumption workflow 的上游設計。

### Data Sources in Power BI

Power BI 可以接很多類型的 data source，常見包括：

- databases
- CSV / Excel files
- web services
- data lakes

可以先把它們區分成兩層：

- `data source`: 原始資料所在的位置
- `dataset` 或後續模型資產: Power BI 內被整理、載入、消費的資料集合

這個區分很重要，因為你不是直接把報表建立在所有原始資料之上，而是先決定應該怎麼把來源轉成可分析的輸入。

### Internal vs External Data

來源還可以用一個很實用的角度來切：

- internal data
- external data

internal data 比較接近公司自己的營運資料。  
external data 則可能是市場、人口、地理、第三方服務或其他外部脈絡。

在 BI 場景裡，兩者常常會被一起用：

- internal data 提供績效與交易真相
- external data 提供比較背景與解釋脈絡

### Desktop vs Service in Connection Workflows

在 Power BI 的連線工作裡，Desktop 和 Service 分工很明確：

- `Power BI Desktop`: 載入、轉換、操作資料
- `Power BI Service`: 分享資產、管理 refresh、處理 gateway 與雲端分發

這也是為什麼很多 connection 設定不是只在 Desktop 完成。  
本機把資料接好之後，真正穩定運作還要看 Service 端的 refresh 與 access configuration。

### Storage Modes

Power BI 常見的 storage modes 有三種：

- `Import`
- `DirectQuery`
- `Live`

它們不是單純技術選項，而是不同的資料存取策略。

### Import Mode

`Import` 是最常見的預設模式。

它的特性可以先理解成：

- 把資料帶進 Power BI
- 可以做完整 transformation
- 通常能使用較完整的 Power BI capabilities

這種模式的好處，是模型與報表的操作通常比較完整，對多數中小型分析流程也比較直覺。

代價則是：

- 資料要被載入
- 新鮮度依賴 refresh
- 資料量變大時，模型與刷新成本會上升

### DirectQuery Mode

`DirectQuery` 的核心心智模型是：

- Power BI 不把所有資料完整載入本地模型
- 需要時再對 data source 發 query

它比較適合：

- 部分支援的資料來源
- 資料量很大
- 希望減少匯入資料體積

但它通常代表更多上游依賴：

- source system 的效能
- query latency
- 連線穩定性

所以 `DirectQuery` 常不是「更進階就一定更好」，而是用更高的上游耦合換取更少的匯入負擔。

### Live Connections

課程把 `Live` 視為第三種較少見的連線方式。  
實務上可以先把它理解成：Power BI 連到已存在的外部模型或分析資產，而不是自己把資料完整建進來。

對 notebook 來說，先記住它和 `Import` / `DirectQuery` 的差別在於：

- control boundary 不同
- 本地模型可操作空間通常較少
- 更依賴外部模型本身的設計

### How to Choose a Storage Mode

一個簡化判斷法：

- 如果你需要完整轉換與建模彈性，先優先想 `Import`
- 如果資料量很大且來源支援，才考慮 `DirectQuery`
- 如果已有外部集中模型，才考慮 `Live`

先選擇操作邊界，再選擇視覺化與 DAX 設計，通常比較不會走反。

### Parameters in Power Query

Power Query 的 parameters 可以先理解成可管理的輸入值。

它們常見用途包括：

- filtering
- custom function inputs
- changing data source functions
- dynamic server / database selection

parameter 通常有：

- name
- value
- type

它們的價值不是語法本身，而是讓 query 與 connection 設定更可重用，不必把環境細節硬寫死在每個步驟裡。

### Incremental Refresh

當資料量開始變大，完整 refresh 很容易變慢，也會增加資料庫負擔。  
這時 `incremental refresh` 就很重要。

它的核心概念是：

- 不必每次都重刷全部資料
- 只刷新新增或變動的部分
- 舊資料可以被保留或封存

這通常適合：

- very large datasets
- historical data
- 定期刷新但變動集中在近期資料的情境

常見好處包括：

- lower refresh times
- less database resource consumption

### Incremental Refresh Dependencies

incremental refresh 並不是只勾選一個選項就結束。  
這份課程特別提醒它常依賴：

- parameters 做動態查詢
- Power BI Service 的對應帳號能力
- 已正確設定的 data gateway

這說明 refresh 問題通常不是單純模型問題，而是 Desktop、Service、source system 與 gateway 一起組成的部署問題。

### Gateways and Scheduled Refresh

當資料來源不在 Power BI 原生可直接雲端存取的位置時，gateway 很常是關鍵元件。

對 notebook 來說，先記住兩件事：

- gateway 讓 Service 能穩定碰到某些資料來源
- scheduled refresh 決定 imported data 何時重新同步

所以 Power BI Service 的價值不只是分享報表，也包含：

- dataset / reporting management
- gateway connections
- scheduled refreshes

### Performance and Connection Choices

當模型變大之後，連線策略也會直接變成效能問題。

來源裡提到幾個很實用的方向：

- 匯入時先去掉不必要的 rows / columns
- 盡量選對 data types
- 先做 group / summarize，避免模型背太細的明細

這些做法其實都在做同一件事：

- 讓模型存更少資料
- 降低 refresh 成本
- 讓後續 aggregation 更快

#### DirectQuery Optimization

如果使用 `DirectQuery`，效能瓶頸常常不在 Power BI 本身，而在上游資料庫。

比較實務的提醒包括：

- limit parallel queries
- write efficient SQL
- use appropriate indexes
- only request the right columns and rows

這再次說明：`DirectQuery` 不是只有連上就好，而是會把 source system 的查詢品質直接暴露到報表體驗上。

### Near Real-Time Refresh Features

如果報表需要更接近即時的資料更新，Power BI 還有一些和 `DirectQuery` 綁得很緊的能力。

#### Automatic Page Refresh

`automatic page refresh` 可以控制 report 對新資料重新查詢的頻率。

來源裡最重要的限制是：

- 它只適用於 `DirectQuery` sources
- refresh interval 應該配合資料實際到達頻率

這代表如果上游資料每 15 分鐘才更新一次，把頁面設成每秒查一次通常只會增加負擔，不會帶來更有意義的 freshness。

#### Change Detection

`change detection` 可以先理解成：

- 追蹤某個欄位聚合值或既有 measure 是否改變
- 有變化時再觸發相關資料與 visuals 更新

這種做法的重點不是「永遠更快」，而是：

- 把刷新條件綁到真正有變化的訊號
- 避免無意義地一直重新查詢

#### Operational Cautions

這份課程還補了幾個很實務的提醒：

- 用 `Performance Analyzer` 檢查每次查詢成本
- 每一個開著報表的使用者，都可能觸發各自獨立的 refresh activity
- 容量、workspace 與授權層級會影響可用刷新能力與頻率

最後一點特別重要，因為 near real-time refresh 不是單純的報表設定，還會受到：

- storage mode
- source performance
- service-side capacity

一起限制。

### M Language and Connection Debugging

Power Query 背後的語言是 `M language`。

在 data connection 的脈絡裡，它的意義通常是：

- 當 GUI 操作不夠清楚時，可以往底層看 query code
- 連線或匯入階段出錯時，常需要讀 M code
- query steps 的可維護性會直接影響排錯效率

課程也提醒：

- M code is case-sensitive
- 有標準函式庫可以使用

這讓 Power Query 不只是圖形化 ETL，而是一個有程式語言底層的可重現連線層。

### Practical Heuristics

- 先分清楚 source 在哪裡，再談報表怎麼設計。
- 大多數情況先從 `Import` 思考，不要一開始就假設 `DirectQuery` 比較高級。
- 如果 refresh 成本開始變高，先檢查能不能改成 incremental refresh。
- 如果想做 near real-time report，先確認 `DirectQuery`、source throughput 與 capacity 是否真的撐得住。
- parameters 很適合把 server、database、date range 這類會變動的值抽離出來。
- 連線穩不穩，常常取決於 Service、gateway、credentials 與 source system，不只是在 Desktop 能不能打開。

### Mental Model

一句話總結：

Power BI 的 data connection layer，可以先理解成 `source selection + storage mode + refresh strategy + service-side connectivity` 的組合決策。

## Data Preparation

在 Power BI 裡，資料準備通常不是報表之前的一段雜務，而是整個 BI workflow 的第一個穩定化步驟。  
如果欄位型別錯、文字值不一致、欄位命名混亂，後面的 model、DAX 與 report 都會變得脆弱。

### A Simple Workflow

在 Power BI Desktop 裡，常見流程可以先想成：

1. connect data
2. open Power Query
3. check data types and column names
4. inspect quality with preview features
5. apply text / numerical / date transformations
6. `Close & Apply`

重點不是做很多 transformation，而是把清理步驟變成可重跑的 recipe。

### What Clean Data Means Here

在 Power BI / Power Query 的脈絡裡，乾淨資料通常至少包含：

- missing values 已被辨識
- typos 與 data entry errors 已被修正
- duplicated data 已被處理
- irrelevant data 被排除
- outliers 已被檢查
- 每個欄位有正確 data type
- column / table names 簡短且可讀

這些條件看起來基礎，但它們會直接影響後面：

- relationship 能不能建立
- measures 結果會不會失真
- visual filters 能不能正常運作

### Power Query as a Repeatable Cleaning Layer

Power Query 的重要性不只在於它能清資料，而是它會把每一步 transformation 保留成 `Applied Steps`。

這代表：

- 你不是手動修一次資料而已
- refresh 時會重新套用同樣步驟
- 清理流程可以被檢查、調整與重跑

這是 Power BI 很重要的工程化特性。  
比起在 Excel 裡手動改值，`Applied Steps` 更接近一條可重現的 preparation pipeline。

### Data Types Come Early

Power Query 會自動推測欄位型別，但這一步不應該完全交給自動判斷。

常見型別包括：

- numerical
- date / time
- text
- logical
- binary

型別如果一開始判錯，後面很容易連鎖出問題：

- date 被當成 text，時間排序與 date functions 都會失效
- 數值被當成 text，無法正確聚合
- categorical code 被當成數值，容易被誤算平均

Tip: 匯入後先確認型別，通常比做任何視覺化還重要。

### Data Preview Features

Power Query 的 `View` ribbon 底下有一組很實用的 preview features：

- `Column distribution`
- `Column quality`
- `Column profile`

它們可以先當成資料檢查儀表板，而不是進階功能。

### Why Preview Matters

data preview 的價值主要有三個：

- 幫你提早看到 errors 與 inconsistencies
- 幫你確認某個 transformation 之後資料變成什麼樣子
- 幫你判斷下一步該做哪種清理

預設 profile 常只基於前 `1000` rows，所以它很適合快速診斷，但不代表一定等於完整資料分布。

### Cleaning Text Columns

文字欄位是最容易把報表和模型搞亂的來源之一。  
Power Query 裡的 clean text 通常意味著：

- 沒有 typo
- 表示方式一致
- capitalization 一致
- 沒有 leading / trailing whitespace
- 沒有 control characters
- 一欄只放一種資訊

最後一點很重要。  
如果一個欄位同時塞 `City, State`、`First Last`、或多段混合訊息，後面做分群、篩選、關聯都會比較痛苦。

### Practical Text Transformations

在 `Transform` ribbon 裡，常用的文字清理包括：

- format / capitalization 調整
- `Trim`
- `Clean`
- split column
- merge columns

其中兩個最值得養成習慣：

- `Trim`: 移除前後空白
- `Clean`: 移除換行、carriage return 等 control characters

如果資料來源很多，`Trim + Clean` 幾乎可以當成文字欄位的預設第一輪處理。

### Cleaning Numerical Columns

數值欄位的清理重點通常不是把數字「變漂亮」，而是確保它們可被可靠地聚合、比較與建模。

常見檢查包括：

- missing values
- obvious errors
- outliers
- precision 是否合理

Power Query 常見的數值 transformation 包括：

- absolute value
- logarithm
- multiply by scalar
- add scalar
- rounding

這些操作通常不是為了炫技，而是為了讓數值更符合業務定義或分析需求。  
例如單位換算、把負號修正為絕對值、或把過度細碎的小數整理成合理精度。

### Working with Date Columns

在 Power Query 裡，date / time 是獨立型別，不只是格式化後的字串。

當欄位型別正確後，常見可用 transformation 包括：

- extract year / quarter / month / week / day
- start or end of year / quarter / month / week
- age extraction

這些操作很常用，因為很多後續分析都依賴時間層次：

- 年 -> 季 -> 月
- cohort / aging
- period-based aggregation

如果日期在 preparation 階段就處理乾淨，後面建立 hierarchy、calendar logic 或 time-based reporting 會順很多。

### Practical Heuristics

- 先修型別與欄位命名，再做複雜 transformation。
- `Applied Steps` 要保持可讀，不要讓清理流程變成黑箱。
- 先用 preview features 找問題，再決定要不要 split、replace、filter 或 recast。
- `Trim` 與 `Clean` 很適合當文字欄位的第一輪標準化。
- 一欄盡量只存一件事，這樣 model 與 filter 才不容易失真。
- date 欄位要盡早轉成真正的 date / time type，不要拖到報表層。

### Mental Model

一句話總結：

Power BI 的 data preparation，可以先理解成用 Power Query 把原始資料轉成 `typed + profiled + transformed + repeatable` 的分析輸入層。

## Data Transformation

在 Power BI 裡，data transformation 比單純清理再進一步。  
它關心的不只是把欄位修乾淨，還包含資料 shape、表與表的組合方式、衍生欄位，以及什麼時候要往 `M code` 層看。


### Reshaping Data

很多資料不是內容錯，而是 shape 不適合分析流程。  
課程把這件事先拆成兩種常見結構：

- long format
- wide format

可以先用一個簡化方式理解：

- `long`: 類別值會重複出現在前面欄位，通常比較容易被系統做聚合、分組與視覺化
- `wide`: 一列裡會展開較多數值欄位，通常比較接近人讀表格的習慣

關鍵不是哪一種永遠比較好，而是哪一種更適合你下一步要做的事情。

### Pivot and Unpivot

Power Query 裡最重要的 reshape 操作之一就是：

- `pivot`: long -> wide
- `unpivot`: wide -> long

這兩個操作很常出現在：

- 報表匯出表格太寬
- Excel source 用月份當欄名
- 多個 measure 被分散成多欄，但分析時其實需要 tidy 結構

實務上，很多 Power BI 模型會更偏好能被穩定聚合與切分的 long-ish 結構，而不是過度為人工閱讀優化的寬表。

### Aggregation and Grouping

transformation 不只是在移動欄位，也常包含先做 aggregation。

在 Power Query 的脈絡裡，`Group By` 可以先理解成：

- 先選定 key
- 再把對應列做彙總
- 產生更高層級的分析表

這適合用在：

- 先把明細壓成 customer / product / date 層級
- 先做中間表，再交給模型層
- 降低後續重複計算負擔

### Combining Data

Power Query 裡另一個非常核心的 transformation 類別，是把多個 queries 或 tables 組起來。  
最常見的兩種就是：

- `append`
- `merge`

### Append Queries

`append` 的心智模型是 vertical stacking。

也就是：

- 把多張結構相近的表往下堆
- 增加 rows
- 不改變主要欄位意義

常見使用情境：

- 多個月份的檔案
- 多個門市的同型報表
- 單一檔案放不下的大量同構資料

append 時最需要先檢查的是 schema：

- column names 是否一致
- column count 是否一致
- data types 是否一致

如果欄位對不起來，Power Query 很容易補出 `null`，但那通常不是解法，而是提醒你 schema 還沒對齊。

### Merge Queries

`merge` 的心智模型是 horizontal enrichment。

也就是：

- 根據共同 key 把另一張表的欄位接進來
- 增加 columns
- 用 lookup / relationship-like 的方式補資料

它通常適合：

- 把 lookup table 接回明細表
- 將多張關聯表先整理成較平坦的輸入
- 在模型層之前先補足描述欄位

但 merge 的前提永遠是 key 品質穩定。  
如果 key 型別不同、拼寫不一致、或 cardinality 本來就沒想清楚，後面就會出現缺值、重複列或錯誤匹配。

### Flat Table vs Model Design

課程提到 merge 可以把表組成較 flat 的 structure。  
這在某些前處理情境很有用，但不代表所有表都應該被壓平到只剩一張。

比較穩的做法通常是：

- transformation 階段只做必要整併
- 分清楚哪些欄位適合提前補齊
- 不要因為方便就把模型層應該表達的結構全部抹平

也就是說，Power Query 可以幫你整理 shape，但資料模型該不該維持多表結構，仍然要回到 semantic model 的需求判斷。

### Custom Columns

當內建 transformation 不夠時，Power Query 可以新增 `custom columns`。

這些欄位：

- 用 `M language` 撰寫
- 可以引用多個欄位
- 可以做更進階的 conditional logic
- 能延伸既有 transformation 的能力

它很適合拿來做：

- row-level business rules
- 條件分類
- 依多欄位組合建立新特徵

### Common Operations in Custom Columns

課程整理了幾類常見操作：

- numerical: `+ - * / ^`
- text: `&`
- comparisons: `< > <> <= >= =`
- conditional logic: `if ... then ... else`
- boolean logic: `AND OR NOT`

這些操作看起來簡單，但其實已經足夠應付很多匯入階段的衍生欄位需求。

### Mind the Data Types

custom column 最常見的問題不是語法長，而是 data types 不一致。

常見風險包括：

- 把 text 當 number 算
- 日期還沒轉型就先比較
- null handling 沒想清楚

如果型別沒先穩住，M code 很容易報錯，或更糟的是產出表面合理、實際錯誤的結果。

### Advanced Editor

當 transformation 開始變多，只看 Applied Steps 有時不夠。  
這時 `Advanced Editor` 就很重要。

它讓你：

- 看到 query 的底層程式碼
- 直接編輯 M code
- 理解每個 transformation 如何被表達

一個很重要的觀念是：

- 你在 Power Query 做的每個 transformation，都會被翻成 M code
- 反過來，調整 M code 也會回到 query steps 的邏輯

可以把 `Advanced Editor` 理解成 GUI 與 code 之間的橋。

### M Code vs DAX

Power BI 很容易把 `M` 和 `DAX` 混在一起，但它們負責的層次不同。

| Layer | Main Purpose | Typical Actions |
| ----- | ------------ | --------------- |
| `M language` | load / transform data | rename, filter, pivot, unpivot, group, custom columns |
| `DAX` | analyze on top of model | measures, calculated columns, filter context, summarization |

一個簡化判斷法：

- 如果你要改的是資料本身的 shape 或欄位內容，優先想 `M`
- 如果你要改的是模型上的分析計算，優先想 `DAX`

課程也特別點出：

- `M` 是 case-sensitive
- `DAX` 不區分大小寫

### Applied Steps and M Code

Power Query 很值得保留的一個工程特性，是 step 與 code 的對應關係。

這代表：

- transformation 不是黑箱
- GUI 操作不是一次性手動點擊
- 你可以從 steps 回推 query 邏輯

當 query 出錯時，能不能讀懂 steps 與 M code，常常比會不會背更多按鈕更重要。

### Practical Heuristics

- 先問資料 shape 適不適合分析，再問圖表怎麼畫。
- `append` 是堆 rows，`merge` 是補 columns，不要混用。
- schema 不一致時先修欄名與型別，不要讓 `null` 悄悄吞掉問題。
- custom columns 適合 row-level 邏輯，但不要把整個分析層都塞進 M code。
- 要改資料就想 `M`，要改模型上的計算就想 `DAX`。
- transformation steps 變複雜後，要敢打開 `Advanced Editor` 看底層。

### Mental Model

一句話總結：

Power BI 的 data transformation，可以先理解成把 raw tables 轉成 `right shape + right joins + right derived columns` 的 Power Query 重塑層。
