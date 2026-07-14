# Customer Churn Analysis in Power BI

customer churn analysis 在 Power BI 裡，通常不是先上模型，而是先把：

- churn 怎麼定義
- 分析問題怎麼切
- 報表敘事怎麼安排

這三件事整理清楚。

如果 [Financial Analysis in Power BI](financial-analysis-in-power-bi.md) 比較偏 KPI 與 decision support，這篇比較偏 retention / attrition 問題如何被做成一個可探索、可溝通的 Power BI case study。

## Why This Matters

很多團隊看到 churn 問題時，第一反應是直接做分類模型。  
但實務上，第一輪更常需要先回答：

- churn rate 大概多少
- 哪些 segment churn 特別高
- 客戶離開的主因是什麼
- 哪些地區或方案異常

也就是說，churn 問題常常先從 descriptive 和 diagnostic analytics 開始，而不是直接 predictive modeling。

## Start With a Clear Churn Definition

來源材料最值得保留的提醒之一是：`churn` 不是固定公式，而是 business definition。

最簡化的版本可以先寫成：

- `churn rate = customers lost / total customers`

但真正的定義會受下列因素影響：

- industry
- revenue model
- product usage pattern
- observation window

例如：

- telecom 可以把取消服務視為 churn
- e-commerce 可能把一段時間內完全沒再下單視為 churn
- subscription SaaS 可能同時區分 logo churn 和 revenue churn

如果定義沒有先講清楚，後面的 churn rate、segment comparison 和 intervention priority 都會失真。

## The Leaky Bucket Mental Model

這份 case study 用了一個很直觀的 framing：

- leaky bucket problem

意思是：

- 新客持續流入
- 但舊客也持續流失

所以成長不只是 acquisition 問題，也是一個 retention 問題。  
這個 framing 很適合放在 dashboard 首頁，因為它會把使用者注意力從「新增多少客戶」拉回「留下了多少價值」。

## Ask Better Questions Before Building Visuals

case study 前半段的分析流程很簡單，但很實用：

1. 先檢查 duplicate / missing values
2. 用其他內部資料來源做 sense check
3. 先問對問題
4. 再做第一批 visualizations
5. 之後才做更進一步分析、dashboard 整理與 stakeholder communication

這個順序的重要性在於：

- 不要先做圖再回頭想問題
- 不要還沒確認資料合理就開始解釋原因
- 不要把 exploratory visuals 直接當 final report

如果想先補這個問題定義流程，可以一起看 [Forming Analytical Questions](../data-communication/forming-analytical-questions.md)。

## A Snapshot Dataset Has Hard Limits

來源資料有一個很重要的限制：

- one row per customer
- snapshot at a specific moment in time

這代表它很適合做：

- overall churn rate
- segment comparison
- churn reason breakdown
- state / plan / demographic drill-down

但不特別適合直接回答：

- churn 是什麼時候開始升高的
- 某個 cohort 的 retention curve 怎麼變
- 介入前後是否改善

因為 snapshot data 缺少完整的 time path。

所以看到 customer-level snapshot 時，最好先問：

- 這是 current-state comparison，還是 longitudinal retention data

如果真正想看 cohort retention，接著看 [Cohort Analysis](../data-manipulation-and-eda/cohort-analysis.md) 會更合適。

## Useful Columns in a Churn Table

這份案例把欄位大致分成：

- unique identifier
- churn label
- demographic fields
- plan / product fields
- billing and usage measures
- customer service interactions

像下面這些欄位在 churn 分析裡很常見：

- `Customer ID`
- `Churn Label`
- `Age`, `Gender`, `State`
- `Unlimited Data`, `International Plan`
- `Monthly Charge`, `Total Charges`
- `Extra Data Charges`, `Extra International Charges`
- `Customer Service Calls`

這些欄位之所以有用，不是因為欄位越多越好，而是因為它們分別對應不同的解釋方向：

- demographic differences
- product fit
- price pressure
- overage pain points
- service friction

## Descriptive Insights Come First

這份案例中，先找到的幾個 insight 很典型：

- 整體 churn rate 約 `27%`
- 約 `45%` 的 churn reason 與 competitors 有關
- California 的 churn rate 異常高，超過 `60%`

這些發現很有代表性，因為它們剛好對應三種不同層次：

- overall baseline
- reason category
- geography outlier

這是一個很好的第一輪分析順序。  
先知道整體問題多大，再看原因類別，最後找最異常的 segment。

## Segment Analysis Usually Beats One Global Number

單看整體 churn rate 很容易把訊號沖淡。  
更實務的做法通常是沿著幾個維度切：

- state / region
- age group
- plan type
- international plan
- unlimited data
- service-call intensity

這樣比較能分辨：

- 是不是某個方案設計有問題
- 是不是某個地區競爭壓力特別大
- 是不是高客服接觸客群的體驗特別差

也就是把「客戶為什麼走」轉成更可追查的切面。

## Churn Reasons Need Business Interpretation

看到 competitor-related churn 很高，不代表答案只是「對手比較強」。

更好的下一步通常是把 competitor churn 再往下拆：

- price sensitivity
- plan mismatch
- poor support experience
- coverage or service quality

所以 churn reason category 是 diagnosis 的入口，不是 diagnosis 的終點。

## Structure the Report as a Story

這份 case study 後半段最有價值的部分，是報表敘事而不是新分析技巧。

它強調幾件事：

- 不要把 visual 隨機分散在不同頁
- 要把可以一起回答同一類問題的圖放在同一頁
- 要建立給 stakeholder 看的 narrative
- 不同頁面最好有不同主題

可以把這個想成：

- page 1: overview
- page 2: churn reasons
- page 3: geography / segment drill-down
- page 4: plan and service behavior

這樣使用者會比較清楚：

- 先看什麼
- 再往哪裡追
- 每一頁在回答哪一個子問題

## A Good Churn Report Layout

對 churn case study 來說，一個很實用的多頁 report 結構是：

1. overview page: overall churn, key KPIs, top findings
2. reason page: churn categories, competitor-related share, service-related share
3. segment page: geography, age, plan, contract, usage pattern
4. action page: 哪些客群優先介入、可能的 retention strategy

這種 layout 的好處是：

- 先給高層摘要
- 再提供可追問的分析頁
- 最後把 insight 拉回 decision

## Interactivity Should Support Questions

來源後半段也強調：

- interactivity makes a report powerful

但真正重要的是：

- 互動要服務分析問題
- 不要只是因為 Power BI 能做就全部打開

對 churn report 來說，最有價值的互動通常是：

- state / segment slicers
- drill-down to more detailed customer groups
- cross-filtering across reason, geography, and plan
- page navigation that follows the analysis story

如果互動沒有對應明確問題，報表就很容易變成：

- 看起來很炫
- 但難以導出決策

## Bookmarks and Buttons Are Optional Multipliers

這份課程把 bookmarks 和 buttons 放在 optional future work，也很合理。

對 churn report 來說，它們比較像：

- 幫 narrative 做 state switching
- 幫使用者做 guided navigation

但前提是：

- 問題結構先清楚
- 頁面主題先清楚
- 核心 visuals 先能單獨成立

如果基礎 report 還沒站穩，先上 bookmarks / buttons 通常只會增加複雜度。

## Practical Heuristics

- 先定義 churn，再計算 churn，不要反過來。
- snapshot dataset 適合 segment comparison，不適合直接假裝自己有完整 retention timeline。
- 第一頁先放 overall churn 與 top findings，不要一開始就丟使用者進細節。
- churn reason 要再往下拆成 business drivers，不要把 reason label 當最終解釋。
- 一頁一主題，讓 report 頁面和 stakeholder 問題對齊。

## Related Notes

- 問題定義與分析類型： [Forming Analytical Questions](../data-communication/forming-analytical-questions.md)
- retention 視角： [Cohort Analysis](../data-manipulation-and-eda/cohort-analysis.md)
- Power BI 報表能力： [Reports in Power BI](reports-in-power-bi.md)
- Power BI 報表設計： [Report Design in Power BI](report-design-in-power-bi.md)

## Mental Model

一句話總結：

在 Power BI 裡做 churn analysis，第一步通常不是預測誰會走，而是先把 `definition + segment insight + report narrative` 做成一個能支援追問與溝通的分析介面。
