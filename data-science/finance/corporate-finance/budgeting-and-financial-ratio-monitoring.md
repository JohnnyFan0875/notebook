# Budgeting and Financial Ratio Monitoring

很多公司不是先做複雜估值，才開始看數字，而是先透過 budget、actuals、KPI 與比率監控，判斷公司目前的財務狀況是否健康。這種工作常會落在 BI dashboard、monthly review 或 board reporting 裡。

Key point: budgeting 和 ratio monitoring 的重點，不只是把數字放上報表，而是讓管理者能快速回答「目前偏離了什麼」「偏離是否危險」「接下來要不要調整」。

## Budget vs. Forecast vs. Actual

這三個詞很常一起出現，但用途不同：

- budget: 在某個期間開始前先定義的計畫數字
- forecast: 根據最新資訊持續更新的未來估計
- actual: 期間結束後真正發生的數字

如果沒有分清楚這三者，很多管理討論會混亂。例如：

- 把 budget 當成最新預期，忽略環境已經改變
- 把 actual miss 視為執行失敗，但其實是假設本身早就過時

## Why Budgeting Matters

budget 可以理解成正式的財務計畫。它通常用來：

- 對齊年度目標
- 提前配置資源
- 降低財務 surprises
- 協調不同部門的行動

它的價值不在於「一定猜中」，而在於先把公司打算如何分配資源與承擔風險說清楚。

## Budgeted Financial Statements

很多 budget 不是只有費用表，而是直接延伸成 budgeted statements，例如：

- budgeted income statement
- budgeted balance sheet
- budgeted cash flow

這樣做的好處是，模型不只知道「明年想花多少」，也知道這些計畫對資產、負債、權益與現金會造成什麼影響。

例如公司預計明年多借一筆貸款投資新設備，這不只是 expense plan，而是會同時影響：

- 資產增加
- 負債增加
- balance sheet 結構改變

## Actual vs. Budget Analysis

`actual vs. budget` 是最基本也最實用的管理檢查之一。它在問的是：

- 發生的數字和原本的計畫差多少？
- 差異是 timing、volume、price、cost 還是執行問題？
- 這個偏差是否代表接下來應該更新 forecast？

這種分析的價值包括：

- 檢查執行效率
- 回頭驗證 budget 假設是否合理
- 提供下一輪 forecast 的修正依據

如果只看 absolute miss，而不追差異來源，dashboard 很快就會淪為事後報數。

## Forecasting in a Monitoring Cycle

forecast 通常比 budget 更常更新，常見頻率是 monthly 或 quarterly。

它和 budget 的差別在於：

- budget 比較像固定起點
- forecast 比較像動態修正

因此很多管理節奏其實是：

1. 先定年度 budget
2. 每月或每季看 actual
3. 根據偏差與新資訊更新 forecast
4. 再用最新 forecast 決定是否調整行動

## KPIs as Management Signals

KPI 是一組用來判斷公司是否朝目標前進的指標。它們不一定很多，但應該明確、可解釋，而且能連回決策。

好的 KPI 通常有幾個特徵：

- 定義清楚
- 和業務目標直接相關
- 能被穩定計算
- 一旦偏離，就知道誰該採取什麼行動

如果一個指標只適合放在 dashboard 上展示，卻無法驅動任何管理反應，那它通常不是強 KPI。

## Financial Ratio Analysis

financial ratio analysis 是用財報欄位之間的關係，快速檢查公司是否健康。常見用途包括：

- 看短期償債能力
- 看營運效率
- 看獲利能力

這些 ratio 的重點不只是公式，而是它們把原始財報數字轉成更容易比較的訊號。

## A Useful Ratio Family Map

把 ratio 先分家族，通常比一口氣背很多公式更有用：

- liquidity ratios: 看短期義務撐不撐得住
- leverage ratios: 看公司用多少 debt 與 equity 在撐資產
- solvency ratios: 看整體財務結構是否過度脆弱
- profitability ratios: 看收入最終能留下多少經濟成果

這個分類的價值在於，你不會把所有 ratio 都混成「好像越高越好」。

例如：

- current ratio 太低可能危險，但太高也可能代表資產閒置
- leverage ratio 偏高不一定錯，要看產業與資本密集度
- profitability ratio 變高也要追問，是 pricing power、成本下降，還是一次性因素

## Liquidity Ratios

liquidity ratios 關心的是公司短期內能不能履行義務。它們比較像「先撐得住嗎」的問題，而不是「長期值不值得投」。

### Current Ratio

current ratio 比較 current assets 與 current liabilities：

```text
current ratio = current assets / current liabilities
```

它回答的是：

- 以目前可在一年內動用的資源，能不能覆蓋一年內要還的義務？

高低沒有放諸四海皆準的單一門檻，還要看產業、營運模式與現金週轉速度。

### Acid-Test Ratio

acid-test ratio 又常叫 quick ratio。它比 current ratio 更保守，因為它比較少依賴存貨變現。

它適合回答：

- 如果不把較慢變現的項目算得太樂觀，公司短期流動性還夠不夠？

因此當公司存貨占 current assets 很大時，acid-test 往往比 current ratio 更有警示力。

### Operating Cash Flow Ratio

有些流動性問題只看 balance sheet 還不夠，因為帳上 current assets 不等於真的能快速轉成可用現金。

operating cash flow ratio 會直接把 core business 產生的 cash 拿來對照 current liabilities：

```text
operating cash flow ratio = cash flow from operating activities / current liabilities
```

它比較像在問：

- 公司靠營運本身產生的現金，能不能支撐短期義務？

如果 current ratio 看起來不差，但 operating cash flow ratio 長期偏弱，通常表示：

- 帳面流動性還行
- 但現金造血能力可能沒有那麼強

## Leverage and Solvency Ratios

除了 current ratio，還有幾個很常一起看的結構性 ratio：

- debt-to-equity = total liabilities / shareholders' equity
- equity multiplier = total assets / shareholders' equity
- debt-to-assets = total liabilities / total assets

可以用很粗略的方式理解：

- debt-to-equity: 負債相對股東資本有多高
- equity multiplier: 資產規模相對股東投入被放大多少
- debt-to-assets: 整體資產有多少比例是用負債撐起來

這些比率最好一起看，而不是分開單讀。因為它們都在描述同一件事的不同切面：

- 公司資產結構有多仰賴外部債務
- 權益緩衝夠不夠厚
- 一旦景氣或現金流轉差，結構是否容易受壓

## Profitability Ratios in a Monitoring Context

在財報監控裡，profitability ratio 常常不是拿來做學術定義，而是拿來回答：

- 核心產品還有沒有足夠 margin
- 營收成長有沒有真的轉成經濟成果
- 公司和同業相比，是高毛利低效率，還是低毛利高周轉

很常見的入門組合包括：

```text
gross margin = (revenue - cost of goods sold) / revenue
operating margin = (revenue - operating expenses) / revenue
cash flow to net income ratio = cash flow from operating activities / net income
```

其中 `cash flow to net income ratio` 很值得和會計上的獲利指標一起看。它能幫助你判斷：

- 帳上獲利有多少真的轉成營運現金
- 利潤品質是否穩定
- 獲利改善是不是主要靠 accrual 調整撐出來

## Company View vs. Industry View

單看一家公司的 ratio，很容易過度解讀。更穩健的做法通常是同時看兩個視角：

- within-company trend: 自己和自己比，看時間序列是否改善或惡化
- industry comparison: 和同業比，看目前水位是否異常

例如某公司的 current ratio 從 `1.4` 升到 `1.8`，表面上看像改善；但如果同業平均一直在 `2.5` 左右，就可能只是從偏弱變成沒那麼弱。

Key point: ratio 的資訊量，來自比較，不只來自公式。

## A Practical Pandas Pattern for Ratio Monitoring

把 ratio 做成可重複維護的 workflow，通常比手動算單一欄位更重要。

常見做法是：

1. 先把 statement lines 整理成欄位一致的 DataFrame。
2. 用欄位間除法建立 ratio columns。
3. 以 `groupby()` 或 `pivot_table()` 彙總 company、industry、year。
4. 再把結果送去 bar chart 或 scatter plot 做比較。

例如 current ratio 可以直接由 statement lines 算出：

```python
balance_sheet["current_ratio"] = (
    balance_sheet["Total Current Assets"]
    / balance_sheet["Total Current Liabilities"]
)
```

如果你有多個 ratio 要重複計算，把 numerator / denominator / ratio name 抽成規則通常更容易維護，而不是每次手寫一行新除法。

接著可以做 grouped summary：

```python
balance_sheet.groupby("comp_type")["current_ratio"].mean()
balance_sheet.groupby(["Year", "comp_type"])["current_ratio"].mean()
```

或用 `pivot_table()` 整理 company 與 industry 平均：

```python
plot_dat.pivot_table(
    index=["comp_type", "company"],
    values=["Gross Margin", "Operating Margin", "Debt-to-equity", "Equity Multiplier"],
    aggfunc="mean",
).reset_index()
```

重點不是語法本身，而是這個流程能把 ratio analysis 從「一次性算表」變成「可反覆更新的 monitoring pipeline」。

### Inventory Turnover and Days in Inventory

inventory turnover 關心的是存貨在一段期間內被賣掉多少次。它比較像效率與流動性之間的橋樑：

- turnover 高，表示存貨周轉較快
- turnover 低，可能代表存貨積壓、需求放緩或採購節奏不對

很多人也會把它轉成 `days in inventory`：

```text
days in inventory = 365 / inventory turnover
```

這樣更容易從管理語言理解：

- 平均要幾天才能把一批存貨消化掉？

## Dashboard Use, Not Just Ratio Calculation

把 ratio 放進 dashboard 的目的，不是單獨展示公式，而是支援比較：

- current period vs prior period
- actual vs budget
- actual vs forecast
- company vs target threshold

如果 dashboard 只顯示一個 ratio 數值，卻沒有比較基準，使用者通常很難知道它到底是好是壞。

## Practical Design for Finance Dashboards

財務監控 dashboard 常見的高價值做法包括：

- 最上層先放核心 KPI 與 warning signal
- 中層放 actual vs budget / forecast variance
- 下層再放 ratio breakdown 與 supporting detail

這樣能讓使用者先知道「是否異常」，再往下追「為什麼異常」。

## Common Mistakes

- 把 budget、forecast、actual 混成同一種數字。
- 只看 variance，卻不區分是 volume、price、timing 還是 accounting reclassification。
- 只顯示 ratio，沒有時間比較或目標基準。
- 用單一流動性 ratio 做過度結論，忽略行業特性與營運脈絡。
- dashboard 放太多 KPI，但沒有哪幾個真的對應管理行動。

## A Practical Monitoring Workflow

1. 先明確定義 budget、forecast 與 actual 的期間與口徑。
2. 先檢查核心財報是否一致，再計算 KPI 與 ratios。
3. 對每個 dashboard 指標都提供比較基準。
4. 若 actual vs budget 偏差持續出現，更新 assumptions 與 rolling forecast。
5. 用 ratio 當警示訊號，但回到 underlying statement lines 找原因。
