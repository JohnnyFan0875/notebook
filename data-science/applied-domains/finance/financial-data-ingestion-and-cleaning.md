# Financial Data Ingestion and Cleaning

金融分析常常不是從模型開始，而是從資料開始出錯。價格欄位、日期欄位、缺值、ticker mapping、資料頻率，只要有一個地方沒先處理好，後面的 return、risk、factor exposure 幾乎都會被帶偏。

Key point: 在金融情境裡，資料匯入不是前置雜務，而是模型品質的一部分。

## Why Financial Data Needs Extra Care

金融資料看起來像一般表格，但通常比一般商業資料更敏感，因為:

- time index 直接決定報酬順序
- missing values 可能代表停牌、上市時間不同或資料源缺漏
- column meaning 可能看似相近，實際卻完全不同
- 不同來源的頻率與曆法不一定一致

如果這些差異沒先釐清，後面算出來的 volatility、correlation 或 drawdown 都可能只是資料問題的投影。

## Start With CSV Hygiene

很多金融 workflow 的第一步還是 CSV。這時最重要的不是先畫圖，而是先確認 DataFrame 和原始檔語意一致。

一開始至少要檢查:

- 欄名是否正確
- index 應不應該是 ticker、date 或 transaction id
- 數值欄位有沒有被讀成 `object`
- 遺漏值是自然缺值，還是解析失敗

在金融資料裡，`object` dtype 常常是一個警訊，因為它可能代表:

- 數字混入逗號或貨幣符號
- 百分比被當字串
- 缺值標記不一致
- 同一欄混進文字和數字

## Dtype Is Not Cosmetic

欄位 dtype 不是顯示細節，而是計算邏輯的一部分。常見欄位型別包括:

- `float64`: prices、returns、market cap、yield
- `int64`: count、ranking、year
- `datetime64[ns]`: trade date、listing date、last update
- `object`: ticker、company name、sector、industry

如果日期欄沒有先轉成 datetime，time-series slicing、rolling、resample 都容易出錯。如果數值欄沒有先轉乾淨，summary statistics 看起來能跑，結果也可能完全不可信。

## Financial Data Sources

金融資料通常同時來自多種來源，不同來源適合不同問題。

常見類型包括:

- equity and ETF prices: 例如 Yahoo Finance 類型來源
- macro and rates series: 例如 FRED
- international or development indicators: 例如 World Bank、OECD、Eurostat
- FX series: 例如 OANDA 類型來源
- exchange listings metadata: ticker、sector、industry、market cap、IPO year

重點不是記住哪個 library 可以抓，而是先分清楚你需要的是:

- price history
- macro series
- reference metadata
- cross-sectional listings

這四種資料在 shape、update cadence 和 quality checks 上都不一樣。

## Price Tables vs. Metadata Tables

金融資料通常至少分成兩大類:

- price table: 以 date 為主軸，重點是 OHLCV、adjusted close、returns
- metadata table: 以 security 為主軸，重點是 sector、industry、exchange、IPO year、market cap

這個 distinction 很重要，因為:

- price table 適合 time-series analysis
- metadata table 適合 cross-sectional grouping
- 真正的研究常常要把兩者接起來

例如:

- 先用 metadata 挑出某個 sector 的股票
- 再抓這批股票的價格資料
- 最後在時間序列上算 returns 或 portfolio exposure

在 market data 裡，OHLCV 的角色也要先分清楚:

- Open / High / Low / Close: 同一期間內不同位置的價格摘要
- Volume: 該期間的交易量
- Adjusted Close: 把 split 與 dividend effects 納進去之後，較適合直接拿來比較長期總報酬路徑的收盤價

如果你後面要算 technical indicators、intraday range 或 execution path，raw OHLC 常很重要；如果你要做長期報酬比較，adjusted series 往往更合理。

## Time Index Discipline

金融資料一旦有日期索引，很多後續操作都依賴 index 是否乾淨。

至少要確認:

- index 已排序
- 沒有重複 timestamp
- 頻率差異是預期的，不是漏資料造成
- 合併不同資料源前，曆法和對齊規則已先定義

例如股票價格和 FRED 利率序列常常不會天然對齊，因為市場休市日和宏觀資料更新頻率不同。這時不能直接把兩欄塞在一起就當成同一時間點觀測。

另一個常見情境是 irregular observations。成交資料、事件資料、某些 macro release 或 sparse fundamental updates，本來就不一定等距。這時要先決定:

- 要保留 irregular structure
- 還是先補成 regular grid 再進行後續分析

補齊成 regular sequence 之前，最好先說清楚缺口代表的是:

- 真正沒有交易
- 資料源沒有值
- 你想要的頻率比原始資料更密

## Multi-Asset Data Structures

一次抓多檔股票時，資料常會變成:

- wide table: 每個 ticker 一欄
- hierarchical columns: price field x ticker

這種結構很方便做:

- cross-sectional comparison
- return matrix construction
- portfolio weighting

但也代表你要先想清楚分析單位到底是:

- 一檔資產的一條時間序列
- 同一天很多資產的橫截面
- 某個欄位在多資產上的 panel

如果分析單位沒先講清楚，後面很容易在 `groupby`、`stack`、`pivot`、`resample` 之間搞混。

## Descriptive Checks Before Modeling

在把資料送進模型前，至少要先做一輪 descriptive review。

常見檢查包括:

- `info()` 看 non-null count 和 dtype
- `describe()` 看中心位置與分散程度
- quantiles 看 tail behavior
- histogram 或 KDE 看分布形狀
- line chart 看 trend、level shift 和缺口

這一步不是形式化暖身，而是用來回答:

- 這份資料大致長什麼樣子？
- 有沒有明顯 outlier 或奇怪的 scale？
- 分布是不是非常偏？
- 同一個 summary metric 背後，圖形是否其實完全不同？

同樣的 mean 和 std，可能對應到非常不同的時間序列路徑，所以金融資料特別需要把 numeric summary 和 visualization 一起看。

## Grouped Summaries and Cross-Sectional Views

除了時間序列，金融資料也常需要用 category 去切。

常見分組欄位包括:

- sector
- industry
- exchange
- IPO year

這類 grouped summary 很適合回答:

- 哪個 sector 公司數量最多？
- 不同 IPO cohort 的 market cap 差異有多大？
- 各交易所的上市公司規模分布是否不同？

這裡要注意，groupby 結果很容易被缺值和極端值主導，所以 grouped mean、median、count 最好一起看，而不是只看單一 aggregate。

## Visualization for Sanity Checks

金融資料視覺化不一定是為了發現 alpha，很多時候只是為了確認資料沒有先壞掉。

實用圖形包括:

- line chart: 看價格、利率或 macro series 的時間路徑
- histogram / KDE: 看分布和偏態
- countplot: 看 sector、industry 這類分類欄位的覆蓋
- grouped bar or sorted countplot: 看 cross-sectional composition

如果一張圖就能讓你發現:

- 某欄全是零
- 類別名稱重複但拼法不同
- 日期突然斷層
- 某些資產只有很短歷史

那這張圖就已經很值得。

## Framework Notes: Python vs. R

在 Python 裡，這類工作常以 pandas / pandas-datareader 為中心；在 R 裡，則很常看到 `xts`、`zoo`、`quantmod` 這條路線。

R workflow 裡幾個很常見的慣例是:

- `getSymbols()`: 從多種來源抓 market data
- `xts`: 以時間索引為核心的物件結構
- `OHLC` extractors，例如 `Op()`、`Hi()`、`Lo()`、`Cl()`、`Vo()`、`Ad()`

工具本身不是重點，重點是你要知道 framework 會把什麼假設包在預設裡，例如:

- 回傳的是不是 time-indexed object
- 資料來源是不是已經被設定成 default
- 取出的是 raw close 還是 adjusted close

## R-Specific Time-Series Workflow

如果使用 `quantmod` / `xts`，有幾個流程特別值得記住:

- `getSymbols()` 可以像一般函數回傳資料，也可以像 `load()` 一樣直接建立物件
- 同一個抽象介面底下，實際匯入邏輯會依資料源切到不同 method
- `setDefaults()` 可以替常用資料源設定預設值，減少重複參數

這種 workflow 很方便，但也因此更需要紀律，因為「資料怎麼被抓進來」有時不是在同一行程式裡完全顯示出來。

## Column Extraction and Instrument Semantics

對 OHLC 資料來說，取哪一欄本身就是研究設計的一部分。

常見問題包括:

- 你要的是 raw close 還是 adjusted close？
- 你要的是 intraday range 還是 end-of-period level？
- 你是在比較價格路徑，還是在比較 total return path？

如果沒有先說清楚，後面即使只是 `Close` 換成 `Adjusted`，結論都可能變掉。

## Corporate Actions and Adjusted Data

股票拆分與股利會讓原始價格序列出現結構性跳點，因此 price history 不能只看「欄位名字像 close」就直接拿來算長期報酬。

至少要區分:

- raw OHLC prices
- split-adjusted prices
- split-and-dividend-adjusted close

對 total return 類分析來說，corporate action adjustment 幾乎不是可選項，而是基本清理步驟。否則很多表面上的崩跌或跳漲，其實只是 split 或 ex-dividend effect。

## Text Files and One-Symbol-Per-File Conventions

本地文字檔匯入時，也要先想清楚檔案 layout 是否適合後續 workflow。

一個常見且穩定的設計是:

- one instrument per file
- date 在第一欄
- 後面是 open / high / low / close / volume / adjusted close
- 檔名直接對應 symbol

這種格式的好處是之後不管在 Python 還是 R，都比較容易自動化批次匯入與欄位標準化。

## A Practical Workflow

1. 先分清楚你要的是 price data、macro data 還是 metadata。
2. 匯入資料後先看 `info()`、`head()`、`tail()`、`describe()`。
3. 把日期欄轉成 datetime，確認 index 排序與唯一性。
4. 修正 dtype、缺值、欄名與單位表示。
5. 若要混合多來源資料，先定義對齊規則與觀測頻率。
6. 用圖和 quantiles 做第一輪 sanity check。
7. 再進入 returns、risk、factor 或 portfolio 分析。

如果是 time-indexed market data，再多補兩個檢查通常很值得:

8. 確認你實際使用的是 raw 還是 adjusted series。
9. 若資料本來 irregular，先定義是否要 regularize，再決定 fill 或 interpolation 規則。

## Common Mistakes

- 把 `object` 欄位直接當數值欄位使用。
- 還沒確認日期與對齊規則，就直接計算 returns。
- 把 price table 和 metadata table 混成同一種分析對象。
- 只看 summary statistics，沒有回頭看圖。
- 抓到多資產價格後，沒有先釐清欄位結構就直接做加總或相關性。
- 把不同來源的更新頻率差異，誤判成經濟現象。
- 直接拿 raw close 算長期表現，卻忽略 split 和 dividend adjustment。
- 把 irregular time series 強行補齊，卻沒有說明 fill 方法代表的經濟意義。

## Practical Reminders

- 金融資料清理做得好，後面的模型通常會簡單很多。
- 很多「市場異常」最後其實是欄位、日期或缺值處理異常。
- 如果你只能先做一件事，通常是確認 index、dtype 和 missingness。
