# Financial Statements for Forecasting

forecasting 在 corporate finance 裡，常常不是先從統計模型開始，而是先把公司已經存在的財報結構看懂。因為很多營運預測、估值模型與敏感度分析，最後都要回到 financial statements 才能落地。

Key point: 財報不只是歷史紀錄，也是 forecast model 的骨架。好的 forecasting 不是憑感覺延伸數字，而是沿著 income statement、balance sheet 與 cash flow logic 去推導。

## Why Financial Statements Matter in Forecasting

financial statements 對 forecasting 的價值通常有三層：

- 提供統一結構，知道哪些欄位是收入、成本、資產、負債與股東權益
- 暴露關鍵驅動因子，讓 forecast 建立在 revenue、margin、working capital 或 financing assumptions 上
- 幫助檢查模型是否自洽，而不是只產出看起來合理的單一答案

如果 forecasting 離開財報結構，模型很容易只剩下一串沒有會計邏輯支撐的成長率。

## The Three-Statement View

最常見的核心框架是三表：

- income statement: 一段期間內賺了多少錢
- balance sheet: 某個時點上擁有什麼、欠什麼
- cash flow statement: 期間內現金如何進出

forecasting 時，這三張表不應被分開看。因為:

- 營收與成本會影響利潤
- 利潤、資本支出與融資決策會影響現金
- 現金、應收、存貨、負債與權益最後會回到 balance sheet

## Income Statement as the Operating Forecast

很多 forecast model 會先從 income statement 開始，因為它最直接承接營運假設。

常見的簡化結構包括：

- sales / revenue
- COGS
- gross profit
- operating expenses
- net profit

其中一個很實用的初學者拆法是：

- direct costs: 直接和銷售或產出綁在一起的成本，例如材料、直接人工、工廠成本
- indirect costs: 比較偏向支援營運的費用，例如 admin、insurance、training、R&D 等

這個區分的好處不是絕對正確，而是它能幫助你判斷哪些欄位應該跟量一起動，哪些欄位比較像固定成本或半固定成本。

## Gross Profit vs. Net Profit

對 forecasting 來說，gross profit 和 net profit 回答的是不同問題：

- gross profit: 核心產品或服務在扣掉直接成本後，還剩多少經濟空間
- net profit: 在把營運支援費用與其他間接費用也算進來後，最後留下多少

如果 forecast 只看 net profit，而不拆 gross margin 與 opex 結構，很多經營變化會被蓋掉，例如：

- 價格上調但原料成本也同步上升
- 營收成長但 support function expansion 讓 opex 提前膨脹

## Balance Sheet as the Constraint Layer

balance sheet 對 forecasting 的價值，在於它讓模型不只會長出損益，還會暴露資本需求與資金來源。

最基本的 identity 是：

```text
assets = liabilities + equity
equity = assets - liabilities
```

這個關係看似入門，但實務上很重要，因為它提醒你：

- 增加資產通常需要現金、負債或權益支持
- 預測成長時，不能只把收入往上拉，卻忽略存貨、應收或融資需求
- equity 不是憑空出現，而是資產扣掉負債後的剩餘索取

## Balance Sheet Definitions That Matter

在 forecast 語境裡，可以先用最簡潔的方式理解：

- asset: 能帶來未來經濟利益的資源
- liability: 需要償付或履行的經濟義務
- equity: 資產扣掉負債後，屬於股東的剩餘權益

這些定義之所以重要，不是因為考試會背，而是它們直接影響 forecast driver 的分類與連結邏輯。

## Cash Flow Statement as the Reality Check

income statement 可以顯示公司「賺錢」，但 cash flow statement 才會回答：

- 現金真的有沒有進來
- 營運、投資與融資活動各自怎麼貢獻現金變化

在 forecasting 裡，cash flow statement 常扮演兩個角色：

- 驗證 model 沒有只做 accrual profit，卻忽略現金壓力
- 連接 capital expenditure、debt financing、dividends 與 ending cash

如果模型 forecast 出高獲利，但現金長期為負，通常就表示 working capital、capex 或 financing 假設還沒有接好。

## Fiscal Year, Quarters, and Reporting Periods

forecasting 不能只看數值，也要看 period definition。很多公司不是用 calendar year，而是用 fiscal year。

- calendar year: 1 月到 12 月
- fiscal year: 公司自行定義的完整報導年度，可能從任何月份開始

例如某些公司會用 `1 July - 30 June` 作為完整財年。這件事會直接影響：

- historical trend comparison
- quarter labeling
- annualization logic
- 同業比較時的期間對齊

Key point: 先確認 period，再比較數字。否則「年增率」和「季度表現」可能其實在比不同季節結構。

## Working With Quarters and Monthly Buckets

季度與月份不是只是報表排版問題，它們決定你 forecast 的 granularity。

- 年度 forecast: 適合高層級規劃
- 季度 forecast: 適合 board reporting、earnings expectation、季節性觀察
- 月度 forecast: 適合現金管理、短期營運與 budget control

資料顆粒度越細，模型通常越貼近營運，但也更容易因假設過多而脆弱。

## Assumptions Drive the Model

forecast 最後一定要回到 assumptions。這些 assumptions 可以來自：

- historical trend
- management guidance
- market sentiment
- demand / supply view
- explicit probability weighting

好的 assumptions 不是「保證正確」，而是：

- 來源清楚
- 可被修改
- 知道它會影響哪些 downstream outputs

## Dependencies and Sensitivities

forecast model 很少只有單一變數。多數欄位其實彼此相依：

- sales 變動會影響 COGS
- capex 變動會影響 depreciation 與 cash
- working capital 假設會影響 cash flow 與 funding need

因此 forecasting 不能只填一串 numbers，還要把 dependency logic 接起來。

sensitivity analysis 則是另一層問題：

- 如果某個 assumption 改變，結果會動多少？

這能幫你看出：

- 哪些 inputs 是主要風險來源
- 模型結論對哪些假設過度脆弱
- 哪些欄位值得做 scenario range，而不只是單點估計

## A Practical Forecasting Workflow

1. 先確認 reporting period: calendar year 還是 fiscal year。
2. 把 historical financial statements 整理成可讀的結構。
3. 先從 income statement 驅動欄位建立營運 forecast。
4. 再把 working capital、capex、debt / equity 等項目接回 balance sheet 與 cash flow。
5. 最後做 scenario 與 sensitivity check，而不是只留 base case。

## Common Mistakes

- 把 fiscal year 當成 calendar year，導致比較基準錯位。
- 只 forecast 收入與淨利，卻沒有把 balance sheet 和 cash flow 接起來。
- 把 direct cost 與 indirect opex 混在一起，失去 driver clarity。
- 假設散落在模型各處，之後很難做 scenario 或 sensitivity update。
- 忽略 statement linkage，讓模型能算但會計上不自洽。
