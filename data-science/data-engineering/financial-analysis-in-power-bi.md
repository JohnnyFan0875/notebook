# Financial Analysis in Power BI

在 Power BI 裡做 financial analysis，不只是把收入、成本和利潤畫成幾張圖，而是把財務指標、時間序列、情境假設與資本配置決策放進同一個分析介面。

如果 [Trend Analysis in Power BI](trend-analysis-in-power-bi.md) 比較偏時間序列探索，這篇比較偏財務指標如何被做成 dashboard、what-if model 與 decision support。

## Why This Matters

財務報表和 BI 報表最大的差別，不只是格式，而是使用目的不同：

- accounting statement 比較偏正式揭露
- Power BI dashboard 比較偏持續監控、拆解與互動分析

因此 financial dashboard 真正要回答的通常不是「數字是多少」，而是：

- 哪些 KPI 現在偏離目標
- 變化是來自 volume、price、cost 還是 mix
- 在不同假設下，結果會怎麼改變
- 如果資本有限，哪些專案應該優先

## Financial Dashboards Start With Business Questions

財務 dashboard 的第一步不是選圖，而是先定義：

- audience 是誰
- 他們要做什麼決策
- 哪些指標真的會改變行動

同一份資料，對不同角色的 dashboard 會長得很不一樣：

- CFO 可能先看 revenue, margin, cash generation, capital allocation
- business unit leader 可能更在意 segment profitability 和 variance
- operator 可能更需要異常、成本失控或 pipeline 風險訊號

所以 financial dashboard 的本質，不是把財務指標全部堆上去，而是把 decision surface 設計清楚。

## KPI and OKR Framing

來源材料很適合保留的一點是：`KPI` 和 `OKR` 最好一起看。

可以先用這個方式分工：

- `KPI`: 持續監控的財務結果
- `OKR`: 這一段期間想推動的方向與目標

例如：

- KPI: gross margin, net income, revenue growth, retention
- OKR: 提升 enterprise segment profitability、降低 churn、改善 working capital efficiency

如果沒有這層 framing，dashboard 很容易變成：

- 指標很多
- 使用者看得到數字
- 但不知道哪一些變化值得採取行動

## Core Profitability Metrics

financial analysis 的基本骨架通常還是從 profitability 開始：

- revenue: 企業在一段期間內創造的收入
- expenses: 為了營運所發生的成本與費用
- net income: 收入扣掉成本費用後的剩餘結果
- profit margin: 利潤相對於收入的比例

在 Power BI 裡，這些指標通常不會只以單一 card 出現，而是會被放進：

- period-over-period comparison
- segment / region / product breakdown
- budget vs actual comparison
- variance bridge

如果只有單點數字，使用者只能看到結果；如果能搭配拆解與比較，才比較接近分析。

## Common Financial KPI Families

除了利潤本身，常見的 KPI 還包括：

- total revenue
- revenue per customer
- revenue growth
- retention
- satisfaction proxy metrics

這些指標不一定都屬於正式財報指標，但很常是財務 dashboard 裡的 leading indicator。  
也就是說，它們不只是描述結果，還是在提示未來的收入品質與續航力。

## Power BI Model Design for Finance

這份材料反覆假設資料會被整理成適合分析的模型。對 financial dashboard 來說，這通常表示：

- fact table 放交易、訂單、費用、現金流或預算
- dimension table 放日期、產品、客戶、區域、部門

也就是偏 star schema 的設計。

這很重要，因為：

- 財務指標常需要跨多維度切分
- 同一個 measure 會被很多 visuals 重複使用
- what-if 與 scenario model 通常也要建立在穩定的 measure layer 上

如果模型本身不穩，後面的 margin、forecast 或 NPV 都很難可信。

## Scenario Analysis and What-If Thinking

financial analysis 很常不是問「現在多少」，而是問：

- 如果銷售成長 5%，結果會怎麼變
- 如果成本上升 3%，margin 會掉多少
- 如果折現率改變，專案順位會不會重排

這就是 scenario analysis 的典型場景。

可以先把它理解成：

- 指定一組假設
- 觀察 dependent variable 怎麼跟著改變

在 Power BI 裡，這類需求常會被做成：

- parameter-driven what-if analysis
- scenario selector
- best / base / worst case comparison

如果 [DAX in Power BI](dax-in-power-bi.md) 是在講怎麼定義 measure，這裡比較像是把 measure 放進互動式假設框架。

## Scenario Analysis vs. Sensitivity Analysis

這份來源有一個很值得保留的區分：scenario analysis 和 sensitivity analysis 不完全一樣。

### Scenario Analysis

scenario analysis 比較像：

- 一次指定一組完整假設
- 看某個結果在這個情境下會是多少

例如：

- sales growth = 8%
- discount rate = 10%
- churn = 4%

然後觀察：

- revenue forecast
- operating profit
- project NPV

### Sensitivity Analysis

sensitivity analysis 則比較像：

- 固定大部分條件
- 只改某個 input 的範圍
- 看結果如何連續變化

例如：

- discount rate 從 8% 到 14%
- 看 NPV 如何改變

所以兩者差別可以簡單記成：

- scenario analysis: 比較幾個離散情境
- sensitivity analysis: 觀察單一輸入對結果的斜率與脆弱度

## Forecasting in Financial Dashboards

來源內容把 forecasting 放在 scenario analysis 脈絡裡，這很合理，因為很多財務預測本來就是：

- 根據歷史資料
- 加上一組成長或風險假設
- 產生未來路徑

常見方法包括：

- straight-line forecasting
- moving average
- regression-based estimation

在 Power BI 裡，這些方法不一定都要完全手工實作，但至少要知道它們背後在回答的問題不同：

- straight line 比較像延續既有趨勢
- moving average 比較偏平滑與短期基準
- regression 比較偏用其他變數解釋結果

如果你想先補時間序列、rolling average 和 seasonality 的底層觀念，可以接著看 [Trend Analysis in Power BI](trend-analysis-in-power-bi.md)。

## Seasonality Matters in Financial Forecasting

financial forecast 很容易被季節性誤導。

例如：

- retail holiday demand
- quarter-end booking behavior
- 季度結算造成的現金流波動

如果模型忽略 seasonality，很容易把短期高峰誤判成長期成長。  
這也是為什麼在 Power BI 裡做 forecasting，不應只看單條線延伸出去，而要先問：

- 目前看到的是 trend 還是 seasonality
- 歷史資料粒度是否一致
- 可不可以把特殊事件與正常週期拆開

## Time Value of Money as a Bridge Concept

來源裡花了不少篇幅介紹：

- future value
- present value
- compounding
- annuities

這些都很重要，但 notebook 裡已經有比較完整的 finance 筆記：

- [Fundamental Financial Concepts](../finance/fundamental-financial-concepts.md)
- [Insurance and Annuity Valuation](../finance/insurance-and-annuity-valuation.md)

對 Power BI 來說，更重要的是知道這些概念會怎麼進入報表：

- 折現後的 project comparison
- 儲蓄或投資路徑 projection
- payment stream 的 valuation
- 使用 `PV` / `FV` / `XIRR` 類邏輯做 scenario comparison

也就是說，Power BI 不是要取代財務理論，而是把理論做成可以被互動式操作的 decision model。

## Capital Budgeting in Power BI

financial analysis 的另一個高價值應用，是把 capital budgeting 做成可互動的比較介面。

如果專案很多、資本有限，報表常要支援：

- 比較多個 project 的現金流
- 調整折現率或 hurdle rate
- 重排專案優先順序
- 看資本受限下的取捨

這時最常見的指標包括：

- `NPV`
- `IRR`
- `XIRR()`
- profitability index
- payback period
- discounted payback period

更完整的 corporate finance 決策框架可再參考 [Capital Budgeting](../finance/corporate-finance/capital-budgeting.md)。

## NPV and Discount Rates

`NPV` 在 Power BI 報表裡很適合被做成：

- project ranking table
- discount-rate sensitivity chart
- scenario comparison card

但真正重要的不是只有公式，而是要讓使用者看到：

- 哪些專案只在樂觀折現率下才成立
- 哪些專案對 cost of capital 特別敏感
- 若資本成本上升，投資順位如何改變

也因此，`discount rate` 不應被當成隨手填入的參數，而是：

- opportunity cost
- cost of capital
- 風險要求報酬

在模型中的具體表達。

## IRR, XIRR, and Irregular Cash Flows

來源提到 `XIRR()`，這在 Power BI 特別值得記住。

很多真實專案的現金流日期並不整齊，所以：

- 一般 `IRR` 假設較規則的期距
- `XIRR()` 則更適合有實際日期欄位的現金流

這種差異會直接影響：

- 專案報酬率解讀
- 不同專案間的可比性
- 和 spreadsheet / finance model 對齊的能力

如果資料已經整理成 cash flow fact table，`XIRR()` 會比手工把不規則日期硬湊成固定期別更自然。

## Profitability Index and Capital Constraints

當資本不是無限時，只看 `NPV` 不一定夠。

`profitability index` 比較像是在問：

- 每投入一單位資本，可以換到多少價值

這很適合在：

- 預算固定
- 專案互斥
- 需要排序

的情境下做補充判讀。

所以在 dashboard 裡，PI 常比較適合和：

- NPV
- initial investment
- payback

一起看，而不是單獨作為唯一決策標準。

## Payback Metrics Are Useful but Incomplete

`payback period` 的價值在於直觀：

- 多久能回本

這對現金壓力大、流動性敏感的決策很有幫助。  
但它的限制也要在報表裡被說清楚：

- 不一定反映 time value of money
- 忽略回本之後的現金流
- 可能錯誤偏好短期專案

因此更穩的做法通常是：

- 用 payback 當第一層風險或流動性篩選
- 再回到 NPV / IRR 看是否真的創造價值

## A Practical Dashboard Layout

如果要把這份內容收斂成一個 financial analysis dashboard，可以考慮這種結構：

1. 首頁先放核心 KPI：revenue, margin, net income, growth
2. 第二層放 variance 和 trend：actual vs budget、MoM / QoQ / YoY、seasonality cue
3. 第三層放 scenario tools：what-if parameters、sensitivity table、best/base/worst case
4. 第四層放 investment view：project cash flows、NPV、IRR、XIRR、payback

這樣的好處是：

- 先監控結果
- 再解釋變化
- 最後支援決策

## Practical Heuristics

- financial dashboard 先從 decision-making audience 出發，不要先從圖表庫出發。
- KPI 最好和 OKR 或 target 一起出現，不然容易只剩下被動監看。
- scenario analysis 適合比較幾組假設；sensitivity analysis 適合看輸入變動的脆弱度。
- forecasting 前先確認 trend、seasonality 和粒度是否分清楚。
- 財務理論可以留給 finance 筆記；Power BI 筆記更應強調這些概念如何被做成互動式模型與報表。

## Mental Model

一句話總結：

在 Power BI 裡做 financial analysis，本質上是把 `financial metrics + time series + assumptions + capital decisions` 轉成可互動、可拆解、可比較的分析介面。
