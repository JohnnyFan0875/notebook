# HR Analytics in Power BI

HR analytics 在 Power BI 裡，通常不是單純把 headcount 做成幾張圖，而是把 workforce monitoring、attrition analysis 與 stakeholder-friendly reporting 串成同一份分析產品。

如果 [Customer Churn Analysis in Power BI](customer-churn-analysis-in-power-bi.md) 偏 customer attrition，這篇可以把它看成 employee attrition 與 workforce dashboard 的對應版本。

## Why This Matters

HR 團隊常同時有兩種需求：

- 持續監控人力現況
- 理解哪些因素和 attrition 有關

這兩種需求看起來接近，但其實對報表設計的要求不同：

- monitoring 比較偏 KPI dashboard
- attrition analysis 比較偏 diagnostic exploration

這也是來源裡一個很好的提醒：`report development` 不等於 `dataset analysis`。  
做 report 時，要先決定報表最終要支援哪一類問題。

## Start With Report Goals

這份 case study 把目標切得很清楚：

- primary goal: monitor key HR metrics on employees
- secondary goal: understand what factors impact attrition

這種拆法很實用，因為它讓頁面結構和分析層次自然分開：

- overview 頁先回答「現在 workforce 長怎樣」
- deeper analysis 頁再回答「哪些因素與 attrition 有關」

如果這兩層混在一起，報表很容易同時想做太多事。

## Report Development Is Not the Same as Dataset Analysis

來源明講了一句很值得保留的話：

- 這個 process 適用於 developing a report，不是 analyzing a dataset

意思是：

- dataset analysis 比較偏探索與理解資料
- report development 比較偏整理輸出、頁面結構與 stakeholder consumption

所以即使前面已經做過 EDA，到了報表階段還是要重新問：

- 哪些指標要留在首頁
- 哪些內容該拆成不同頁面
- 哪些視覺是給管理者快速掃描
- 哪些視覺是給分析者繼續追問

## Core HR Metrics for a Workforce Overview

這份案例中，第一輪 key insights 很典型：

- 累計曾任職人數約 `1,470+`
- 目前在職人數約 `1,200+`
- 最大部門是 Technology
- 整體 attrition rate 約 `16%`

這些指標之所以適合作為首頁，是因為它們各自回答不同面向：

- scale: 組織大概多大
- current state: 目前還有多少人在職
- structure: 人力分布在哪裡
- risk: 流失壓力多大

對 HR dashboard 來說，這比一開始就放很多細部 demographic breakdown 更穩。

## Attrition Is the HR Version of Churn

在 workforce analytics 裡，`attrition` 可以先理解成：

- 員工離開組織的比例

它和 customer churn 很像，但解讀上通常更敏感，因為它常牽涉：

- manager quality
- compensation fairness
- promotion opportunity
- workload and environment
- diversity and inclusion

所以 attrition dashboard 不只是在看數字，也常在看組織風險。

## Demographic and Compensation Views Need Care

案例後半段整理出一些常見的 workforce insights：

- 多數員工落在 `20-29` 歲
- 女性略多於男性
- non-binary 員工占一定比例
- 不同 ethnic groups 的平均薪資有差異

這類分析有價值，但需要比一般業務指標更小心：

- 它們很容易被過度簡化
- 小群體樣本數可能很小
- salary differences 可能混入職級、職能、年資等結構因素

因此比較穩的做法是把這類視覺定位成：

- equity signal
- representation snapshot
- further investigation trigger

而不是直接當成單一結論。

## Metadata Is a Real Productivity Tool

這份課程把 `metadata sheet` 稱為「best friend」，這個說法其實很實務。

在 HR analytics 裡，metadata 特別重要，因為欄位常同時包含：

- employee profile
- job / department structure
- review or performance events
- satisfaction scales
- compensation or attrition labels

如果沒有 metadata，常見問題會是：

- 欄位定義被誤解
- 類別值意義不清楚
- rating scale 被當成連續量亂解釋
- employee table 和 event table 的 grain 被混淆

所以 metadata 不只是文件，而是避免分析誤讀的控制面。

## A Useful Data Model for HR Analytics

來源案例的模型很有代表性：

- fact table 以 performance review 或 HR event 為中心
- dimension tables 包含 `Employee`, `EducationLevel`, `RatingLevel`, `SatisfiedLevel`, `Date`

這個設計很重要，因為 HR 資料很常同時有：

- employee-level profile
- repeated review / survey / event records
- reference tables for coded levels
- time dimension

也就是說，雖然商業使用者最後看到的是 HR dashboard，但底層仍然需要明確的 model grain。

## Snowflake Schema Can Be Reasonable Here

這份案例明確提到 `snowflake schema`。

對一般 BI 入門來說，我們常先推 star schema；但在 HR analytics 裡，snowflake 有時也合理，尤其當：

- dimension 本身還有層級或 lookup table
- rating / satisfaction / education level 被獨立管理
- 想保留較清楚的 reference structure

重點不是一定要 snowflake，而是要知道：

- employee demographic data
- performance review data
- coded category tables

之間的 grain 和 relationship 必須清楚。

## Fact vs. Snapshot Thinking

這份案例也提醒了一個很常被忽略的 distinction：

- employee profile snapshot
- review / performance fact records

如果我們只看單一員工主檔，適合回答的是：

- 現在人力組成如何
- 哪些部門最大
- attrition label 分布如何

如果我們看的是 repeated review facts，才比較能追：

- satisfaction 變化
- review outcomes
- 某些環境評分是否和 attrition 相關

把這兩種 grain 混在一起，是 HR dashboard 很常見的錯誤來源。

## A Practical HR Report Structure

對這類 HR report，一個很自然的頁面安排是：

1. workforce overview: active headcount, attrition rate, department mix
2. demographics: age, gender, representation
3. compensation and equity: salary distribution, group comparisons
4. attrition drivers: department, satisfaction, review or service signals

這樣的順序很合理，因為它先給：

- 組織現況
- 人口結構
- 公平性與薪資切面
- 最後才回到離職風險與解釋

## Sensitive Metrics Need Extra Interpretation Discipline

HR analytics 和一般營運 dashboard 最大的不同之一，是很多指標都碰到敏感人員資料。

這代表幾件事：

- 小樣本 subgroup 不宜過度解釋
- representation difference 不等於因果解釋
- salary gap 需要控制職位、等級、地區、年資等因素
- dashboard 的使用權限與分享範圍應更保守

所以 HR dashboard 應該同時被視為：

- analytical tool
- governance-sensitive asset

## Practical Heuristics

- 先分清楚報表是偏 workforce monitoring，還是偏 attrition diagnosis。
- 首頁先放 headcount、current employees、largest department、attrition rate 這種高層指標。
- metadata sheet 要視為分析工具，不只是附錄。
- 先確認資料 grain 是 employee snapshot 還是 review/event fact，再決定該怎麼建模。
- demographic 和 salary 視角很有價值，但一定要避免過度簡化或樣本數過小的誤讀。

## Related Notes

- report 能力： [Reports in Power BI](reports-in-power-bi.md)
- report 設計： [Report Design in Power BI](report-design-in-power-bi.md)
- customer attrition 對照案例： [Customer Churn Analysis in Power BI](customer-churn-analysis-in-power-bi.md)
- 分析問題定義： [Forming Analytical Questions](../data-communication/forming-analytical-questions.md)

## Mental Model

一句話總結：

在 Power BI 裡做 HR analytics，本質上是把 `workforce KPIs + attrition questions + careful data modeling + sensitive stakeholder communication` 整理成一份可持續使用的 HR 報表。
