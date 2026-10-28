[Data Science](../../README.md) › [應用領域](../README.md) › [Finance](README.md) › 金融基本概念

# Financial Concepts

貨幣時間價值、債券估值與利率風險，以及金融資料特有的清理問題。一般的 CSV / dtype / 日期處理見 [Importing Data](../../python-foundations/importing-data.md)、[Datetime](../../python-foundations/datetime.md)。

## Fundamental Financial Concepts

很多 finance 問題表面上長得不一樣，但骨架常常是同一套: 一筆錢跨時間怎麼比較？報酬率怎麼累積？未來現金流今天值多少？一個決策到底是創造價值，還是只是把時間往後拖？

Key point: 金融概念的共同底層，其實是 time、cash flow、rate 這三件事如何一起作用。

### Return on Investment

最基本的投資報酬概念，是看一筆資產從初始價值走到最終價值後，成長了多少。

- initial value: 進場時投入多少
- final value: 期末拿回多少
- return: 兩者之間的相對變化

這種 ROI 觀念很直觀，但它只是一個起點，因為單看總報酬還沒有回答:

- 花了多久才得到這個報酬
- 中間有沒有現金流
- 報酬是一次跳出來，還是逐期複利累積

### Time Value of Money

time value of money 的核心很簡單:

- 今天的一塊錢，通常比未來的一塊錢更有價值

原因不只是一句「可以拿去投資」，而是它同時反映:

- opportunity cost
- inflation
- uncertainty
- liquidity preference

一旦接受這件事，finance 幾乎所有估值問題都會變成:

- 把未來現金流折回今天
- 或把今天的資金投影到未來

### Compounding

compounding 的關鍵不是「利息會變多」而已，而是:

- 利息本身也會再產生利息

這讓成長過程從線性變成乘法累積。也因此:

- 持有期越長，複利效果越明顯
- compounding frequency 越高，累積結果通常越大

這也是為什麼看起來很小的 rate difference，拉長時間後可能會造成很大的 wealth gap。

### Annual Rate vs. Periodic Rate

很多金融產品不直接用同一個計息頻率。你常常需要在 annual rate 和 monthly / quarterly / daily rate 之間換算。

這裡最重要的不是背公式，而是記住:

- 名目年利率不一定等於逐期真正發生的成長率
- 不同 payment frequency 下，等價的 periodic rate 會不同

如果沒有先把 rate frequency 對齊，後面的 mortgage payment、discount factor 或 cumulative growth 幾乎都會算錯。

### Present Value and Future Value

present value 問的是:

- 未來某筆金額，放到今天值多少？

future value 問的是:

- 今天某筆金額，以某個 rate 成長到未來會變多少？

這兩者其實是一體兩面:

- 往未來推，是 compounding
- 往今天折，是 discounting

理解這個對偶關係之後，很多看似不同的 finance 問題都會變得很像。

### Discounting Cash Flows

只要現金流發生在不同時間點，就不能直接把名目金額相加。你必須先處理時間尺度。

discounting 的目的，是把:

- 早拿到的錢
- 晚拿到的錢

放回同一個今天的尺度上比較。

這也是為什麼 NPV、bond valuation、capital budgeting、retirement projection，本質上都在做同一件事，只是 cash flow pattern 不同。

### Project Evaluation Basics

在專案評估裡，最常見的幾個指標是:

- NPV
- IRR
- EAA

這門基礎課的價值，不在於重新推一遍公式，而是提醒幾個判讀原則:

- NPV 比較接近「增加多少價值」
- IRR 比較接近「隱含報酬率是多少」
- EAA 適合拿來比較壽命不同的專案

### Cost of Capital

折現率不是憑感覺填一個數字。很多 corporate finance 問題會用 cost of capital 當成 required return 的起點。

直覺上它回答的是:

- 這家公司動用一塊資金，投資人最低期待它回收多少報酬？

當資金來源同時包含 debt 和 equity 時，常見合成方式就是 WACC。它不是神奇參數，而是把:

- debt financing cost
- equity financing cost
- capital structure weights

合在一起，作為整體資本成本的近似。

### Debt, Equity, and Claims

debt 和 equity 的差別，不只是名稱不同，而是對現金流的 claim 順序不同。

- debt holders: 先拿固定承諾現金流
- equity holders: 拿剩餘索取權

因此:

- debt 的 downside protection 通常較高
- equity 的 upside participation 通常較大

這個 distinction 會一路影響:

- cost of capital
- valuation logic
- risk exposure

### Mortgage as a Cash Flow Structure

mortgage 是 time value of money 很好的實物例子，因為它把幾個抽象概念都具體化了:

- down payment
- loan principal
- periodic interest rate
- fixed periodic payment
- amortization through time

同一筆 monthly payment，早期通常更多是在付 interest，後期才越來越多是在還 principal。這也說明了:

- 現金流結構和餘額演變，是兩件要一起看的事

### Home Equity and Underwater Mortgage

如果把 mortgage 放到資產負債觀點來看，還要再區分:

- house value
- outstanding loan balance
- home equity

當房屋價值低於剩餘貸款時，就會出現 underwater mortgage。這提醒我們:

- 資產價格路徑
- 負債攤還速度

是兩條不同動態，不能只看其中一邊。

### Wealth Accumulation

wealth accumulation 問的不是單一年度賺多少，而是:

- 一連串 savings、growth rates、expenses、inflation 交互作用後，淨財富路徑會怎麼走

這類問題通常要一起考慮:

- income growth
- recurring expenses
- emergency buffer
- tax drag
- inflation
- compounding on invested assets

因此它比單一 NPV 題目更像一個 multi-period budgeting problem。

### Forecasting With Growth Rates

當你已經有 growth assumptions 時，常見做法是沿著時間把:

- cumulative growth path
- projected value path

一路滾出來。

這種 forecast 最容易犯的錯，是把 rate 當成會直接相加的東西。只要 growth 是跨期持續累積，通常就該用 multiplicative thinking，而不是單純線性外推。

### Rational Economic Decisions

finance 的很多「理性決策」其實不是要你追求最高名目金額，而是要求你把以下幾件事一起納入:

- time horizon
- risk
- financing cost
- scale
- cash flow timing

這也是為什麼看起來很賺的提案，折現之後可能沒有那麼有吸引力；而看起來普通的穩定現金流，放到長期 wealth accumulation 裡卻可能很有價值。

### A Practical Mental Model

1. 先辨認問題裡的 cash flows 發生在什麼時間點。
2. 再確認使用的是 annual rate 還是 periodic rate。
3. 決定你要把資金往未來投影，還是往今天折現。
4. 如果有 debt / equity 結構，再把資本成本納入。
5. 最後才比較不同方案的 value、return 或 affordability。

### Common Mistakes

- 把總報酬直接拿來比較不同持有期間。
- 沒有對齊 compounding frequency 就直接套用 rate。
- 把 nominal cash flows 直接相加，沒有先折現。
- 只看 mortgage payment 金額，沒有看 principal 和 interest 的分解。
- 用單一高報酬數字說服自己，卻沒有把風險與資本成本一起放進來。

### Practical Reminders

- 如果你搞清楚 time、cash flow、rate，很多 finance 題目會突然變得很像。
- 折現不是數學花招，而是把不同時間點的金額拉回同一尺度。
- 對長期決策來說，compounding 和 inflation 通常都不能忽略。

## Bond Valuation and Interest Rate Risk

債券看起來常像「固定拿利息、到期拿回本金」的簡單工具，但一旦把價格、殖利率、duration 與 convexity 放在一起看，就會發現 fixed income 的核心其實是 discounting 和 interest-rate risk。

Key point: bond valuation 的本質，是把一串已知或可預期的 cash flows 用適當殖利率折現回今天，然後分析價格對利率變化有多敏感。

> 貨幣時間價值、複利與多筆現金流折現見本篇上半部 [Fundamental Financial Concepts](#fundamental-financial-concepts)。

### Core Bond Characteristics

在開始估值前，先分清楚 bond contract 的幾個基本元素:

- issuer: 誰借錢
- principal / par / face value: 到期返還的本金
- coupon rate: 發行人承諾支付的利息率
- payment frequency: 年付、半年付、季付等
- maturity: 本金何時返還

這些條件會直接決定 cash flow pattern，也就直接決定估值方式。

### Keep the Scope of the Bond Clear

很多入門 bond model 會先假設:

- fixed coupon
- fixed maturity
- no embedded options

這個限制很重要，因為 callable、putable、convertible 或其他帶 option 的 bonds，會讓 cash flow amount 和 timing 都變得不再固定，分析也會明顯更複雜。

### Present Value and Zero Coupon Bonds

zero coupon bond 最容易看出債券估值的本質，因為它只有一筆未來 cash flow:

- 到期時拿回 face value
- 中間沒有 coupon

因此它的價格就是那筆 face value 的 present value。這種 bond 也很適合拿來理解 yield 和 maturity 如何共同影響價格。

### Coupon Bonds as a Bundle of Discounted Cash Flows

coupon-paying bond 則可以理解成:

- 多筆中間 coupon cash flows
- 再加上一筆 maturity 時的 principal repayment

實務上，很有幫助的一個心智模型是把一張附息債拆成一組 zero coupon cash flows。這會讓 pricing logic 變得非常清楚:

- 每筆 coupon 都各自折現
- 到期本金也要折現
- 全部加總就是 bond price

### Yield to Maturity

yield to maturity 可以理解成: 如果你以當前價格買入並持有到到期，這張債券隱含的年化回報率大概是多少。

對 zero coupon bond 來說，yield 常可直接由 price 和 face value 反推。對 coupon bond 來說，yield 則通常需要數值法或 trial-and-error 求解，因為它同時出現在多期折現項裡。

### Yield Is More Than Just a Number

估值裡用到的 yield，不只是 market quote，而是多種風險補償的合成結果。很常見的拆法是:

- risk-free rate
- credit spread
- 其他可能的 risk premia

直覺上，risk-free rate 提供時間價值的基準，而 spread 則補償違約、流動性、call risk 或其他額外風險。

### Risk-Free Yield and Spread

如果想把 yield 背後的邏輯說清楚，可以先用這兩層去想:

- risk-free yield: 通常用相似 maturity 的 government bond 當 baseline
- spread: 反映相對於 baseline 額外要求的回報

因此兩張 maturity 類似但信用風險不同的 bonds，就算 coupon 一樣，折現率也不會一樣。

### Credit Ratings and Comparable Yields

實務估值中，若手上 bond 沒有足夠流動交易價格，常會參考:

- 同信用等級 bonds 的市場殖利率
- 相近 maturity 的 benchmark curve
- 同產業或同 issuer type 的 comparable bonds

這背後其實就是 fixed-income 版本的 comparable pricing，只是比較對象變成相似 credit profile 和 maturity bucket。

### Price and Yield Move Inversely

這是 fixed income 最重要的直覺之一:

- yield 上升，discount rate 上升，price 下跌
- yield 下降，discount rate 下降，price 上升

這個關係也帶出 premium、discount、par 的基本判讀:

- premium bond: price above par，通常代表 coupon 高於 yield
- discount bond: price below par，通常代表 coupon 低於 yield
- par bond: price around par，通常代表 coupon 約等於 yield

### Estimating Yield From Price

如果 bond 已知價格，但你想反推它的 YTM，本質上是在找那個能讓 discounted cash flows 恰好等於 market price 的折現率。

對 coupon bond 來說，這通常要靠:

- iterative guessing
- root finding
- 金融函數內建的 numerical solver

Key point: price 決定時，yield 往往不是代數解，而是數值解。

### The Price-Yield Curve Is Not Linear

bond price 和 yield 的關係不是一條直線，而是一條彎曲曲線。這件事很重要，因為它告訴我們:

- 同樣大小的利率變動，價格反應未必對稱
- 線性近似只在小幅利率變動時比較可靠

這也正是 duration 和 convexity 存在的原因。

### Duration as Interest Rate Sensitivity

duration 常被當成「殖利率變動 1% 時，債券價格大概變動多少百分比」的近似量。它是 interest-rate sensitivity 的一階近似。

duration 有兩種很有用的直覺:

- price sensitivity view: 利率變動時，價格會怎麼動
- weighted-average timing view: 你平均要多久才拿回投資

兩種理解方式都指向同一個核心: cash flows 越晚拿回、越依賴遠期折現，通常越怕利率變化。

### What Increases Duration

一般來說，下列條件會讓 duration 變高:

- 較長的 maturity
- 較低的 coupon
- 較低的 yield level

這些條件的共通點是: 讓更多價值集中在較遠的未來，因此對 discount rate 的改變更敏感。

### Dollar Duration and DV01

把 duration 從百分比敏感度轉成金額敏感度後，常用的量是:

- dollar duration
- DV01

它們都在回答一個更貼近風險管理的問題:

- 利率變動一點點，我的 portfolio 會賺或賠多少錢？

其中 DV01 特別常用，因為它把風險標準化成「殖利率變動 1 basis point 時的價格變動」。

### Duration-Based Hedging

當投資組合對利率很敏感時，可以用 DV01 去做 hedging。核心做法是:

1. 算出現有 portfolio 的 DV01
2. 算出 hedge instrument 的 DV01
3. 找到能互相抵消的部位數量

這樣做不能消除所有風險，但能先把一階的 interest-rate exposure 壓低。

### Duration Is Only a Linear Approximation

duration 很好用，但它是線性的。當 yield change 變大時，duration-only prediction 會開始偏離真實價格變化，因為真正的 price-yield relation 是 curved。

這就是 duration 的主要限制:

- 對小幅變動通常不錯
- 對大幅變動可能失真

### Convexity Measures Curvature

convexity 可以理解成 price-yield curve 的彎曲程度，也是一個二階效果。

它的實務價值在於:

- 改善 price-change approximation
- 更完整地衡量 interest-rate risk
- 解釋為什麼債券價格上漲與下跌的幅度常不對稱

正 convexity 常被視為一種好處，因為:

- yield 下降時，價格上升通常比線性預測更多
- yield 上升時，價格下跌通常比線性預測更少

### Small vs. Large Yield Changes

在小幅 yield moves 下，duration 的線性近似通常還算好用，而且上升與下降的效果看起來相對接近。

但當 yield move 變大時，bond price reaction 會開始明顯不對稱:

- yield 下降時，價格上漲幅度可能大於線性預期
- yield 上升時，價格下跌幅度通常小於同幅度下降時的漲幅

這種 asymmetry 正是 convexity 想捕捉的現象。

### What Increases Convexity

在一般直覺下，convexity 會隨這些條件增加:

- 較長 maturity
- 較低 coupon
- 較低 yield

這和 duration 的方向很像，但 convexity 更直接反映「曲率有多大」，而不只是 slope。

### Combining Duration and Convexity

做 bond price prediction 時，最常見的進階做法是:

- 先用 duration 提供一階 price change
- 再加上 convexity adjustment 補二階曲率效果

這樣通常會比單用 duration 更接近實際 repricing 結果，尤其在 yield move 比較大時更明顯。

### A Practical Fixed-Income Workflow

1. 先確認 bond 的 cash flow structure: zero coupon 還是 coupon-paying。
2. 用 yield 和 payment timing 折現得到價格。
3. 再從價格反推出 yield 或比較不同 bonds 的 YTM。
4. 用 duration 衡量一階利率敏感度。
5. 用 DV01 轉成 portfolio 可操作的金額風險。
6. 若需要更準確 price prediction，再加上 convexity。

### Common Mistakes

- 把 coupon rate 和 yield to maturity 混為一談
- 忘記 compounding frequency 和 payment frequency 要一致
- 沒有先確認 bond 是否帶 embedded options，就直接套 option-free pricing 直覺
- 估 yield 時忽略 risk-free baseline 和 spread 的區分
- 用 duration 預測大幅利率變動，卻沒有加 convexity adjustment
- 只看價格高低，不看 premium / discount 背後是 coupon 與 yield 的相對位置
- 做 hedging 時只看面額，不看 DV01

### Practical Reminders

- bond 不是「固定收益所以固定風險」，它對利率其實可能很敏感。
- 在 fixed income 裡，現金流時點本身就是風險來源的一部分。
- 如果你想知道 portfolio 對利率變動的真實暴露，DV01 往往比單純的 price 或 yield 更有操作意義。

## Financial Data: 金融特有的清理問題

金融分析常常不是從模型開始，而是從資料開始出錯。價格欄位、日期欄位、缺值、ticker mapping、資料頻率，只要有一個地方沒先處理好，後面的 return、risk、factor exposure 幾乎都會被帶偏。

Key point: 在金融情境裡，資料匯入不是前置雜務，而是模型品質的一部分。

### Why Financial Data Needs Extra Care

金融資料看起來像一般表格，但通常比一般商業資料更敏感，因為:

- time index 直接決定報酬順序
- missing values 可能代表停牌、上市時間不同或資料源缺漏
- column meaning 可能看似相近，實際卻完全不同
- 不同來源的頻率與曆法不一定一致

如果這些差異沒先釐清，後面算出來的 volatility、correlation 或 drawdown 都可能只是資料問題的投影。

### Financial Data Sources

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

### Price Tables vs. Metadata Tables

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

### Time Index Discipline

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

### Multi-Asset Data Structures

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

### Column Extraction and Instrument Semantics

對 OHLC 資料來說，取哪一欄本身就是研究設計的一部分。

常見問題包括:

- 你要的是 raw close 還是 adjusted close？
- 你要的是 intraday range 還是 end-of-period level？
- 你是在比較價格路徑，還是在比較 total return path？

如果沒有先說清楚，後面即使只是 `Close` 換成 `Adjusted`，結論都可能變掉。

### Corporate Actions and Adjusted Data

股票拆分與股利會讓原始價格序列出現結構性跳點，因此 price history 不能只看「欄位名字像 close」就直接拿來算長期報酬。

至少要區分:

- raw OHLC prices
- split-adjusted prices
- split-and-dividend-adjusted close

對 total return 類分析來說，corporate action adjustment 幾乎不是可選項，而是基本清理步驟。否則很多表面上的崩跌或跳漲，其實只是 split 或 ex-dividend effect。

### Common Mistakes

- 把 `object` 欄位直接當數值欄位使用。
- 還沒確認日期與對齊規則，就直接計算 returns。
- 把 price table 和 metadata table 混成同一種分析對象。
- 只看 summary statistics，沒有回頭看圖。
- 抓到多資產價格後，沒有先釐清欄位結構就直接做加總或相關性。
- 把不同來源的更新頻率差異，誤判成經濟現象。
- 直接拿 raw close 算長期表現，卻忽略 split 和 dividend adjustment。
- 把 irregular time series 強行補齊，卻沒有說明 fill 方法代表的經濟意義。
