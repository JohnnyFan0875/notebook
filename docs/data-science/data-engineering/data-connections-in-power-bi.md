# Data Connections in Power BI

Power BI 的連線層可以先理解成：  
它決定資料從哪裡來、怎麼被載入、什麼時候刷新，以及哪些能力能在模型與報表層使用。

如果 [Data Preparation in Power BI](data-preparation-in-power-bi.md) 比較偏清理與轉換，那這篇更偏資料來源、storage mode、refresh 與 connection settings。

## Why This Layer Matters

很多報表問題表面上看起來像視覺化或 DAX 問題，但根源其實在連線層：

- 資料來源選錯
- storage mode 不合適
- refresh 策略不穩
- gateway 或 credentials 沒設好

所以在 Power BI 裡，連線不是單純的「把資料接進來」，而是整個 consumption workflow 的上游設計。

## Data Sources in Power BI

Power BI 可以接很多類型的 data source，常見包括：

- databases
- CSV / Excel files
- web services
- data lakes

可以先把它們區分成兩層：

- `data source`: 原始資料所在的位置
- `dataset` 或後續模型資產: Power BI 內被整理、載入、消費的資料集合

這個區分很重要，因為你不是直接把報表建立在所有原始資料之上，而是先決定應該怎麼把來源轉成可分析的輸入。

## Internal vs External Data

來源還可以用一個很實用的角度來切：

- internal data
- external data

internal data 比較接近公司自己的營運資料。  
external data 則可能是市場、人口、地理、第三方服務或其他外部脈絡。

在 BI 場景裡，兩者常常會被一起用：

- internal data 提供績效與交易真相
- external data 提供比較背景與解釋脈絡

## Desktop vs Service in Connection Workflows

在 Power BI 的連線工作裡，Desktop 和 Service 分工很明確：

- `Power BI Desktop`: 載入、轉換、操作資料
- `Power BI Service`: 分享資產、管理 refresh、處理 gateway 與雲端分發

這也是為什麼很多 connection 設定不是只在 Desktop 完成。  
本機把資料接好之後，真正穩定運作還要看 Service 端的 refresh 與 access configuration。

## Storage Modes

Power BI 常見的 storage modes 有三種：

- `Import`
- `DirectQuery`
- `Live`

它們不是單純技術選項，而是不同的資料存取策略。

## Import Mode

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

## DirectQuery Mode

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

## Live Connections

課程把 `Live` 視為第三種較少見的連線方式。  
實務上可以先把它理解成：Power BI 連到已存在的外部模型或分析資產，而不是自己把資料完整建進來。

對 notebook 來說，先記住它和 `Import` / `DirectQuery` 的差別在於：

- control boundary 不同
- 本地模型可操作空間通常較少
- 更依賴外部模型本身的設計

## How to Choose a Storage Mode

一個簡化判斷法：

- 如果你需要完整轉換與建模彈性，先優先想 `Import`
- 如果資料量很大且來源支援，才考慮 `DirectQuery`
- 如果已有外部集中模型，才考慮 `Live`

先選擇操作邊界，再選擇視覺化與 DAX 設計，通常比較不會走反。

## Parameters in Power Query

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

## Incremental Refresh

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

## Incremental Refresh Dependencies

incremental refresh 並不是只勾選一個選項就結束。  
這份課程特別提醒它常依賴：

- parameters 做動態查詢
- Power BI Service 的對應帳號能力
- 已正確設定的 data gateway

這說明 refresh 問題通常不是單純模型問題，而是 Desktop、Service、source system 與 gateway 一起組成的部署問題。

## Gateways and Scheduled Refresh

當資料來源不在 Power BI 原生可直接雲端存取的位置時，gateway 很常是關鍵元件。

對 notebook 來說，先記住兩件事：

- gateway 讓 Service 能穩定碰到某些資料來源
- scheduled refresh 決定 imported data 何時重新同步

所以 Power BI Service 的價值不只是分享報表，也包含：

- dataset / reporting management
- gateway connections
- scheduled refreshes

## Performance and Connection Choices

當模型變大之後，連線策略也會直接變成效能問題。

來源裡提到幾個很實用的方向：

- 匯入時先去掉不必要的 rows / columns
- 盡量選對 data types
- 先做 group / summarize，避免模型背太細的明細

這些做法其實都在做同一件事：

- 讓模型存更少資料
- 降低 refresh 成本
- 讓後續 aggregation 更快

### DirectQuery Optimization

如果使用 `DirectQuery`，效能瓶頸常常不在 Power BI 本身，而在上游資料庫。

比較實務的提醒包括：

- limit parallel queries
- write efficient SQL
- use appropriate indexes
- only request the right columns and rows

這再次說明：`DirectQuery` 不是只有連上就好，而是會把 source system 的查詢品質直接暴露到報表體驗上。

## Near Real-Time Refresh Features

如果報表需要更接近即時的資料更新，Power BI 還有一些和 `DirectQuery` 綁得很緊的能力。

### Automatic Page Refresh

`automatic page refresh` 可以控制 report 對新資料重新查詢的頻率。

來源裡最重要的限制是：

- 它只適用於 `DirectQuery` sources
- refresh interval 應該配合資料實際到達頻率

這代表如果上游資料每 15 分鐘才更新一次，把頁面設成每秒查一次通常只會增加負擔，不會帶來更有意義的 freshness。

### Change Detection

`change detection` 可以先理解成：

- 追蹤某個欄位聚合值或既有 measure 是否改變
- 有變化時再觸發相關資料與 visuals 更新

這種做法的重點不是「永遠更快」，而是：

- 把刷新條件綁到真正有變化的訊號
- 避免無意義地一直重新查詢

### Operational Cautions

這份課程還補了幾個很實務的提醒：

- 用 `Performance Analyzer` 檢查每次查詢成本
- 每一個開著報表的使用者，都可能觸發各自獨立的 refresh activity
- 容量、workspace 與授權層級會影響可用刷新能力與頻率

最後一點特別重要，因為 near real-time refresh 不是單純的報表設定，還會受到：

- storage mode
- source performance
- service-side capacity

一起限制。

## M Language and Connection Debugging

Power Query 背後的語言是 `M language`。

在 data connection 的脈絡裡，它的意義通常是：

- 當 GUI 操作不夠清楚時，可以往底層看 query code
- 連線或匯入階段出錯時，常需要讀 M code
- query steps 的可維護性會直接影響排錯效率

課程也提醒：

- M code is case-sensitive
- 有標準函式庫可以使用

這讓 Power Query 不只是圖形化 ETL，而是一個有程式語言底層的可重現連線層。

## Practical Heuristics

- 先分清楚 source 在哪裡，再談報表怎麼設計。
- 大多數情況先從 `Import` 思考，不要一開始就假設 `DirectQuery` 比較高級。
- 如果 refresh 成本開始變高，先檢查能不能改成 incremental refresh。
- 如果想做 near real-time report，先確認 `DirectQuery`、source throughput 與 capacity 是否真的撐得住。
- parameters 很適合把 server、database、date range 這類會變動的值抽離出來。
- 連線穩不穩，常常取決於 Service、gateway、credentials 與 source system，不只是在 Desktop 能不能打開。

## Relation to Other Notes

- 如果你想看資料接進來之後怎麼清理，可以接著看 [Data Preparation in Power BI](data-preparation-in-power-bi.md)。
- 如果你想看整理後的資料如何成為可治理的分析層，可以接著看 [Semantic Models and Power BI](semantic-models-and-power-bi.md)。

## Mental Model

一句話總結：

Power BI 的 data connection layer，可以先理解成 `source selection + storage mode + refresh strategy + service-side connectivity` 的組合決策。
