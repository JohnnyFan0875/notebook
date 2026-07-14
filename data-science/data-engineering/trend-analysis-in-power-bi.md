# Trend Analysis in Power BI

在 Power BI 裡，trend analysis 可以先理解成：

- 把資料放回時間順序
- 看變化方向、變化速度、週期性與異常點
- 再決定哪些訊號值得被做成比較、平滑、拆解或追因

如果 [Reports in Power BI](reports-in-power-bi.md) 偏互動式報表能力，這篇比較偏時間序列、趨勢視覺化與 exploratory analytics 的實務心法。

## Why This Matters

很多商業問題表面上看是單一 KPI 問題，但真正想問的其實是：

- 現在是在上升還是下降
- 這個變化是短期波動還是長期趨勢
- 是季節性現象，還是更長週期的循環
- 哪個維度最可能在驅動這個結果

所以 trend analysis 的核心，不是把線畫出來而已，而是把 `direction + timing + explanation` 放回同一個分析脈絡。

## What a Time Series Is

這份課程先從最基本的定義出發：

- time series 是依時間順序排列的一串資料點
- 通常會在連續、等間距或近似等間距的時間點上觀察

這個定義看起來很簡單，但它暗示了兩件事：

- 時間欄位必須可被正確排序
- 同一個序列的時間粒度要先講清楚

例如：

- 日
- 週
- 月
- 季

如果粒度混亂，後面的 trend、MoM、rolling average 都容易失真。

## Common Use Cases

來源裡整理了幾個很典型的 time series use case：

- cyclical patterns
- season-specific trends
- systemic challenges
- relationships with a target outcome
- forecasting preparation

把它翻成更實務的語言，大概就是：

- 看有沒有固定節奏
- 看波動是不是受季節或事件影響
- 看系統是否正在長期轉壞或轉好
- 看某個結果和其他變數是否一起變

## Period-over-Period Change

趨勢分析最常見的第一步，不是做複雜模型，而是先看 period-over-period change。

像課程裡提到的：

- `MoM change`

本質上就是：

- 本期值和前一期比較

這類指標的價值在於：

- 不只看絕對值
- 也看變化速度
- 更容易發現突然加速、放緩或反轉

可以把這類比較擴展成：

- `DoD`
- `WoW`
- `MoM`
- `QoQ`
- `YoY`

## Time-Series Patterns

這份課程有一個很值得保留的區分：`cyclical` 和 `seasonality` 不是同一件事。

### Cyclical

`cyclical` 可以先理解成：

- rise-and-fall patterns
- 沒有固定精準週期
- 常常比一年更長
- 較不易預測

這種變化比較像景氣循環、政策週期、長期需求波動。

### Seasonality

`seasonality` 則比較接近：

- 受季節或固定時點影響
- 有較穩定的重複節奏
- 常發生在一年內的固定區段

像：

- holiday spending
- quarter-end effects
- back-to-school demand

這個區分很重要，因為：

- cyclical 不一定能用固定週期去外推
- seasonality 則比較適合用固定節奏去比較

## Run Charts and Time-Series Visualization

課程把 `run chart` 當成 time-series 基本視覺。  
對 notebook 來說，可以先把它理解成：

- 依時間順序畫出單一指標
- 先看整體方向、波動與異常

它的價值不在 fancy，而在於：

- 最先暴露資料節奏
- 最容易讓使用者看到趨勢是否在改變

很多時候，一張簡單的 line / run chart 就足以回答：

- 這個指標現在往哪裡走
- 波動有沒有變大
- 是否出現結構性改變

## Rolling Averages and Smoothing

時間序列很容易被短期噪音干擾，所以課程引入了：

- `rolling averages`
- `smoothing`

rolling average 的核心目的不是改寫資料，而是：

- 暫時降低短期波動
- 讓底層趨勢比較容易被看見

這很適合：

- 資料點很多、波動很碎
- 使用者先想看方向，不是每個尖峰
- 想比較原始值與較平滑的趨勢線

## What Smoothing Is Good For

平滑通常比較適合拿來：

- 看長期方向
- 避免單點噪音搶走注意力
- 幫報表首頁提供較穩定的 trend cue

但也要知道代價：

- 太平滑會掩蓋重要異常
- 視窗大小不同，會改變解讀

所以 rolling average 最好不是取代原始序列，而是和原始線一起被對照。

## Anomalies in a Time Series

課程後半段也點出另一個很重要的分析目標：

- `anomalies`

也就是那些明顯偏離常態節奏的點或區段。

時間序列異常常代表：

- 資料品質問題
- 外部事件衝擊
- 業務流程改變
- 系統故障或異常操作

所以 anomaly 不一定只是 outlier，也可能是值得被追查的業務訊號。

## Decomposition Trees

這份課程不只談時間序列，還帶到 `decomposition tree`，這很適合留在同一篇裡，因為它常是 trend analysis 的下一步：

- 先發現某個時間趨勢有變
- 再追問是哪個維度在驅動它

### What a Decomposition Tree Does

課程給的定義可以先收斂成：

- 用多個維度逐步拆解 target metric
- 看哪些因素對結果影響最大

它很適合：

- ad hoc exploration
- root cause analysis
- identifying influential variables

## When to Use a Decomposition Tree

decomposition tree 特別適合這類情境：

- 指標變差了，但不知道是誰造成的
- 想從 region / product / segment / channel 一路往下拆
- 不想先寫死單一路徑，而是想互動式追問

所以它比較像：

- exploratory explanation tool

而不是：

- 正式預測模型
- 單純靜態 summary chart

## Reading a Decomposition Tree

即使來源大多是示意圖，背後最值得保留的心法還是很清楚：

- 先看 target metric
- 再看每一步拆解用了哪個維度
- 比較不同 branch 的貢獻差異
- 把「最大值 / 最小值 / explain by」這類互動當成追因入口

一個實務提醒是：

- decomposition tree 給的是可探索的 explanation path
- 不等於自動證明因果

它更像幫你縮小嫌疑範圍，而不是直接宣布真因。

## Key Influencers

第四章的 `key influencers` 其實也和 trend / explanation 很接近，所以適合一起收錄。

可以先把它理解成：

- 找出哪些 explanatory variables 和 target characteristic 有顯著關聯
- 比較不同變數的相對影響力

這類 visual 很適合：

- 找 driver
- 比較因素重要性
- 做 exploratory relationship analysis

## Trend Analysis Is Not Causality

無論是：

- MoM change
- run chart
- rolling average
- decomposition tree
- key influencers

都不該被直接當成因果證明。

它們更像是在回答：

- 發生了什麼
- 什麼一起變了
- 什麼值得下一步追查

真正的 causal claim，通常還要更多設計、控制或實驗證據。

## Practical Heuristics

- 先確認時間欄位與粒度正確，再做任何 trend analysis。
- 先看原始序列，再決定是否加 rolling average，不要一開始就只看平滑後結果。
- `seasonality` 和 `cyclical` 要分開想，因為可預測性不同。
- period-over-period 指標適合看變化速度，不適合單獨取代原始值。
- 如果趨勢異常，先查資料品質與事件背景，再談模型。
- 想追因時，decomposition tree 和 key influencers 很有價值，但它們比較像探索工具，不是因果保證。

## Relation to Other Notes

- 如果你想先理解 Power BI 的整體平台工作流，可以先看 [Power BI Overview](power-bi-overview.md)。
- 如果你想看報表互動與視覺化使用方式，可以接著看 [Reports in Power BI](reports-in-power-bi.md)。
- 如果你想看 DAX 的模型層計算與 context，可以接著看 [DAX in Power BI](dax-in-power-bi.md)。
- 如果你想看報表層 UX 與 layout 心法，可以接著看 [Report Design in Power BI](report-design-in-power-bi.md)。

## Mental Model

一句話總結：

Power BI 的 trend analysis，可以先理解成用 `time ordering + period comparison + smoothing + interactive explanation` 把時間序列變化講清楚。
