# Financial Modeling Workflows

financial modeling 的目標不是把 spreadsheet 做得很複雜，而是把商業假設、財務邏輯與決策輸出放進一個可追蹤、可修改、可測試的結構裡。

Key point: 好的 financial model 不只是會算，而是讓使用者知道哪些是輸入、哪些是假設、哪些是公式推導出來的結果。

## What a Financial Model Is

financial model 可以理解成對真實財務情境的抽象表示。它通常會把歷史資料與前瞻假設串起來，用來回答像這樣的問題:

- 如果價格提高，獲利會怎麼變？
- 如果折現率改變，專案還值得投嗎？
- 在不同情境下，公司的 value range 會怎麼移動？

因此模型的價值不只是產出答案，也在於讓假設和結果之間的關係變得可見。

## Independent vs. Dependent Variables

建模時最好先分清楚兩種欄位:

- independent variables: 來自模型外部的輸入與假設
- dependent variables: 透過公式從模型內推導出的結果

這個區分很重要，因為它會直接影響:

- 哪些地方可以手動修改
- 哪些地方應該鎖定為公式
- 情境分析時該改哪些驅動因子

如果 inputs 和 formulas 混在一起，模型會很快失去可維護性。

## Model Transparency and Color Coding

很多 financial model 會用顏色區分 input、formula、link、check 等欄位。這不只是美觀，而是降低出錯率的一種工作流設計。

背後真正重要的原則是:

- 使用者能快速辨認哪裡是 assumptions
- 計算鏈條盡量一致，不要同時混手打數字和公式
- review 時能快速找到模型驅動因子

顏色只是工具，重點仍然是結構清楚。

## Forecasting From Financial Statements

很多模型會從最基本的 income statement 或 operating schedule 開始，逐步建立:

- revenue forecast
- cost or margin assumptions
- subtotal and net income logic
- supporting schedules

即使是簡單模型，也應該盡量把歷史資料、 assumptions 與 forecast 分開。這樣在更新資料或改情境時，才不需要重做整份模型。

如果你還在建立 statement-level 直覺，建議搭配 [financial-statements-for-forecasting.md](financial-statements-for-forecasting.md) 一起看，先把:

- income statement 的 driver
- balance sheet 的 constraint role
- cash flow statement 的 reality check
- fiscal year / quarter 的 period alignment

放回同一條 forecasting workflow。

## Dynamic Models and Reusable Inputs

好的模型通常會盡量讓關鍵假設集中管理，而不是散落在很多 worksheet 裡。常見做法包括:

- 用命名範圍管理核心 assumptions
- 讓報表或情境切換能透過 lookup or mapping 邏輯自動更新
- 避免同一個 input 在不同地方被重複手動輸入

這種設計的目的，是讓模型在規模變大時仍可被 audit、維護與重算。

另一個很常被低估的 input 管理問題，是 reporting period。模型若混用 calendar year、fiscal year、quarterly run-rate 與 YTD number，往往在最前面就已經對不齊。

## What-If Analysis

financial model 不是只算一個 base case。很多時候，真正的決策價值來自 what-if analysis，也就是問:

- 如果價格上升會怎樣？
- 如果折現率提高會怎樣？
- 如果成長率變慢會怎樣？

這種分析讓模型從靜態報表變成 decision-support tool。

## Scenario Analysis vs. Sensitivity Analysis

兩者常一起出現，但焦點不同。

### Scenario Analysis

scenario analysis 會一次改動一組互相一致的 assumptions，例如:

- base case
- upside case
- downside case

它適合描述完整商業情境，而不只是單一變數微調。

### Sensitivity Analysis

sensitivity analysis 會有系統地觀察某個輸入在一段範圍內變動時，輸出怎麼改變。

它適合回答:

- 哪個假設最影響結果
- 哪些變數是主要風險來源
- 模型結論是否對某個參數過度敏感

如果 scenario analysis 比較像在看故事線，sensitivity analysis 比較像在看結果對單一旋鈕的彈性。

很多 corporate forecast 還會把 assumptions 分成幾類：

- 可直接控制的經營假設，例如 price、headcount、capex plan
- 間接受影響的假設，例如 margin、collection cycle、inventory turns
- 外部假設，例如 market sentiment、demand environment、probability-weighted case mix

先分清楚 assumption type，敏感度分析才不會把所有旋鈕都當成同樣可控。

## Goal Seek, Data Tables, and Model Navigation

Spreadsheet 工具常見的價值不在於功能名稱，而在於它們支援的思考方式:

- Goal Seek: 從結果倒推需要什麼輸入
- Data Tables: 系統化掃描一維或二維輸入範圍
- Scenario Manager 類工具: 在多組 assumptions 間快速切換

這些工具的共同作用，是把「我覺得會怎樣」轉成可重複檢查的分析流程。

## Time Value of Money Inside a Model

financial modeling 裡常會直接使用 time value of money 的概念與函數，例如:

- FV: 把現在的資金推到未來
- PV: 把未來的資金折回今天
- ROI: 粗略比較每單位投入帶來多少收益

這些工具本身不難，真正重要的是:

- 期數是否定義一致
- 利率或 benchmark 是否合理
- cash flow 的 timing 是否被正確表示

## Capital Budgeting in a Spreadsheet Workflow

一旦模型開始處理專案投資決策，常見會接到:

- NPV / XNPV
- IRR / XIRR
- mutually exclusive project comparison
- date schedule construction

在 spreadsheet 實作上，一個很重要的習慣是把日期、現金流與 discount assumption 明確拆開，這樣才知道結果是因為 timing 改變，還是因為金額改變。

## The Golden Rule in Project Selection

在互斥專案之間，IRR 很有用，但不應取代 NPV 的核心地位。

實務上的簡化原則可以寫得很直接:

- 先確認 NPV 是否為正
- 如果只能選一個互斥專案，優先看哪個正 NPV 最大
- 再用 IRR、payback 或 scenario results 當補充資訊

Key point: NPV 較接近 value creation；其他指標常是輔助視角。

## Common Modeling Mistakes

- inputs、formulas、hard-coded numbers 混在一起
- 同一個 assumption 在多個地方重複輸入
- 只做 base case，沒有做 scenario 或 sensitivity check
- 把漂亮格式當成模型品質，卻沒有基本 consistency check
- 把 spreadsheet function 的結果當成黑盒，沒有先確認 timing 與 sign convention

## Practical Reminders

- 模型的第一責任是可讀、可改、可驗證，不是炫技。
- 如果使用者看不出哪些是假設，模型通常已經太脆弱。
- 越是用來做投資與估值決策的模型，越應該把 scenario analysis 當成基本配備，而不是可有可無的附加功能。
