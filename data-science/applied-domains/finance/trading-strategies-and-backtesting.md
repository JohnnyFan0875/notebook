# Trading Strategies and Backtesting

trading strategy 和 portfolio analysis 很像，但焦點不完全相同。portfolio analysis 更常問的是「一組資產的配置是否合理」，trading strategy 則更常問「什麼時候進場、出場，規則長期跑起來會變成什麼樣子」。

Key point: 好的交易研究不是先追求漂亮報酬曲線，而是先把 `data -> indicator -> signal -> position -> backtest -> benchmark -> risk review` 這條鏈條定義清楚。

## Trading vs. Investing

trading 通常有幾個典型特徵:

- holding period 較短
- 更關注短中期價格趨勢、反轉或波動
- 可以同時設計 long 與 short 規則

investing 則通常比較像:

- holding period 較長
- 更看重 fundamentals、cash flow 與 business quality
- 多數情境以 long-only 為主

這個 distinction 很重要，因為它會影響:

- 你需要的資料頻率
- 你容忍的 turnover
- 你該看的 benchmark 與 risk metric

除了時間尺度之外，trading 還常分成兩種很不一樣的邏輯:

- divergence / momentum / trend-following: 假設目前方向會延續
- convergence / reversion / cycle trading: 假設偏離終究會回來

這個分類很有用，因為同樣叫做「交易策略」，背後的賺錢方式和風險體感可能完全不同。

## From Price Data To Returns

交易研究通常不是直接盯著價格本身，而是先把價格序列整理成更適合分析的形式，例如:

- daily returns
- cumulative returns
- rolling mean 或 moving average
- 不同頻率的 resampling，例如 hourly 轉 weekly

這一步的目的不是只是「算出一欄新資料」，而是把原始市場價格轉成比較容易辨認訊號的特徵。

提醒: 不同頻率下的型態可能完全不同。日資料上的訊號，不一定能直接搬到週資料或小時資料。

## Technical Indicators Are Feature Engineering For Market Data

technical indicators 可以先當成市場資料上的 feature engineering 來理解。它們不是預言機，而是把歷史價格、成交量或波動特徵轉成更容易觀察的訊號。

常見類型包括:

- trend indicators: 例如 moving averages，用來看方向或趨勢強度
- momentum indicators: 例如 RSI，用來看價格變動速度
- volatility indicators: 例如 Bollinger Bands，用來看價格偏離程度
- oscillator indicators: 常用固定尺度表達短期過熱或過冷狀態

把 technical indicators 視為 feature engineering 有一個好處: 你比較不會把它們誤解成保證有效的交易法則，而會自然追問:

- 這個指標到底在摘要什麼資訊？
- 它對哪種市場 regime 比較敏感？
- 它跟我的 decision rule 之間是什麼關係？

## Moving Averages And Trend-Following Signals

moving average 是最常見的交易指標之一。它的核心想法很直覺:

- 用 rolling window 平滑掉短期噪音
- 用價格與平均線的相對位置判斷趨勢方向

典型訊號像是:

- `price > SMA`: 視為多頭訊號
- `price < SMA`: 視為減碼、空手或空頭訊號

這類規則的優點是容易理解、容易實作，也適合拿來建立第一個 backtesting workflow。但它的限制也很明顯:

- 訊號通常有 lag
- 盤整市場容易被 whipsaw
- lookback window 一改，結果可能差很多

## RSI And Mean Reversion Logic

Relative Strength Index, RSI, 是常見的 momentum indicator，但它常被拿來做 mean reversion 的 decision rule。

常見口訣是:

- RSI > 70: 可能過熱，接近 overbought
- RSI < 30: 可能過冷，接近 oversold

實務上這不代表看到 70 或 30 就一定要反向交易，而是代表:

- 你可以把它當成風險提示
- 你可以把它和其他條件一起組合成 entry / exit rule

這種規則的研究重點不是門檻本身，而是:

- 門檻是否和資產特性相符
- 訊號是否會過度頻繁
- 是否真的形成可交易的 out-of-sample pattern

很多 oscillator 類指標的真正角色，不是單獨決定方向，而是提供「等 pullback 再進場」的 timing filter。

## Combining Signals Usually Beats Blindly Trusting One Indicator

單一訊號很容易過度敏感，因此實務上常會組合多個條件。

一個很典型的思路是:

- 用長週期 moving averages 定義大方向
- 再用短週期 oscillator 找較好的進場點

例如:

- 只有在 `SMA50 > SMA200` 時，才接受某個 oversold oscillator 的進場訊號

這種設計背後的想法不是讓規則變複雜，而是把兩件事拆開:

- regime filter: 現在是否處於較適合做多或做空的環境？
- entry timing: 在既定方向下，現在是不是較好的切入點？

如果沒有先分清楚這兩層，很多策略其實只是把不同概念硬塞進同一條線。

## A Signal Is Not Yet A Strategy

signal 只是觸發條件，strategy 則還要補齊執行與持有規則。

例如同樣一個 `price > SMA` 訊號，仍然可以對應很多不同策略:

- 訊號成立時全倉持有，不成立時空手
- 訊號成立時持有 50%，不成立時轉現金
- 訊號成立時做多，不成立時反手做空

所以從 signal 走到 strategy，至少還要定義:

- target position 或 target weight
- rebalancing frequency
- 是否允許 short
- 是否和其他風控條件聯動

再往下一層，還要有 rules 真的把訊號轉成交易行為。換句話說:

- indicator: 從資料算出特徵
- signal: 根據條件判斷該不該動作
- rule: 決定如何下單、加碼、減碼、出場或取消其他掛單

這也是為什麼 strategy implementation 往往比做出 indicator 更麻煩，因為真正的複雜度通常藏在 execution logic。

這也是很多新手容易混淆的地方: indicator、signal 和 strategy 並不是同一件事。

## A Practical Backtesting Workflow

回測的目的是把規則放到歷史資料裡，檢查它如果真的照做，結果會是什麼。

一個實用流程通常是:

1. 取得並清理價格資料。
2. 計算 returns 與 indicators。
3. 把 indicators 轉成 signal。
4. 把 signal 轉成 positions 或 weights。
5. 跑回測並產生 cumulative performance。
6. 拿 benchmark 做比較。
7. 最後再做 risk review，而不是只看報酬。

如果用像 `bt` 這類套件，常見結構會長得像:

- `SelectWhere()` 或等價邏輯: 根據訊號選資產或選時點
- `WeighTarget()` 或等價邏輯: 把訊號轉成權重
- `Backtest()` / `run()`: 實際執行歷史模擬

工具本身不是重點，重點是研究流程必須能清楚回答「這個規則是怎麼從資料一步一步走到績效」。

如果你在 R 生態工作，常見工具分工會像這樣:

- `quantmod`: 抓取與瀏覽金融時間序列，例如 `getSymbols()`
- `TTR`: 計算常見 technical indicators，例如 `SMA()`
- `quantstrat` 一類框架: 把 indicator、signal、rule 串成交易系統

這些工具名稱不是一定要背，但知道資料、指標與執行框架是三層不同工作，會讓研究流程清楚很多。

提醒: 價格欄位也要選對。很多 equity backtest 會偏向使用 adjusted close，而不是裸 close，因為股利與 split 會扭曲長期比較。

## Benchmarking Matters

沒有 benchmark，很多策略看起來都會比實際更有說服力。

對主動交易策略來說，常見 benchmark 包括:

- 同一資產的 buy-and-hold
- broad equity index，例如 S&P 500
- 更簡單、參數更少的 baseline strategy

benchmark 的用途不是讓策略一定要每段時間都贏，而是幫你回答:

- 這個主動規則是否真的有額外價值？
- 如果只是長期持有，結果是否已經差不多？
- 為了追求超額報酬，你到底付出了多少風險與複雜度？

如果你的策略只比 benchmark 多一點點報酬，卻換來更深的 drawdown、更多 turnover 或更差的穩定性，通常就不值得。

## Strategy Optimization Needs Restraint

常見問題是: `SMA 20`、`SMA 50`、`SMA 100` 到底哪個好？

這時通常會做 strategy optimization，也就是:

- 嘗試一組參數
- 分別跑 backtest
- 比較績效差異

這個步驟本身沒有錯，但風險在於很容易開始 overfit。

Warning: 如果你只是反覆試參數，最後挑歷史上表現最好的一組，結果常常只是把 noise 誤認成規律。

比較健康的做法通常是:

- 先用 domain intuition 縮小參數範圍
- 盡量減少 moving parts，不要每一層都放自由參數
- 把 optimization 當成 sensitivity analysis，不是尋找神奇數字
- 盡量保留 out-of-sample 或 walk-forward 驗證

## What To Review After A Backtest

回測結束後，最不該做的事就是只看 total return。

至少應該一起看:

- total return
- CAGR
- daily / monthly / yearly mean return
- daily / monthly / yearly volatility
- Sharpe ratio
- Sortino ratio
- max drawdown
- average drawdown
- drawdown duration
- best / worst day、month、year

這些指標一起看，才能把同一條績效曲線拆成:

- 賺了多少
- 波動有多大
- 最痛的虧損有多深
- 壞時期會拖多久

尤其 drawdown days 很重要，因為投資人常不是死在單日波動，而是死在長時間都回不來。

如果策略是以交易損益序列或 P&L 為主來監控，也常會直接從 P&L 計算:

- annualized Sharpe
- max drawdown
- profit-to-drawdown 類比率
- percent positive
- average win / loss ratio

這些指標不是 portfolio analysis 才重要，對交易系統更常是第一層健康檢查。

## Trend Systems And Reversion Systems Fail Differently

trend-following 與 mean reversion 常有完全不同的 performance signature。

trend-following 系統常見特徵是:

- percent positive 可能不高
- average win / loss ratio 可能比較高
- 靠少數大行情把整體績效拉起來

mean reversion 系統常見特徵是:

- percent positive 可能比較高
- average win / loss ratio 可能比較低
- 多數時候小賺，但偶爾遇到單邊趨勢時受傷

這個對照很重要，因為它提醒我們:

- 低勝率不一定是壞策略
- 高勝率也不代表尾端風險可接受

策略的好壞，必須連同 payoff shape 一起看，而不是只看 win rate。

## Visual Inspection Still Matters

summary metrics 很重要，但第一輪 review 常常還是先看圖最有效。

實務上可以優先看:

- price 與 indicator 疊圖
- signal / position timeline
- cumulative P&L
- drawdown path

如果你在 R 內工作，像 `chart.Posn()`、`add_TA()` 這類工具的價值就在於讓你快速確認:

- 訊號是不是出現在你以為的位置
- position 是否有照規則切換
- 指標與價格互動是否符合直覺

很多回測錯誤不是統計問題，而是欄位對錯、訊號偏移一根 bar、或規則沒有真的照想像執行。這些錯誤通常看圖比看 summary table 更早發現。

## Common Failure Modes

交易策略研究很容易掉進幾個陷阱:

- 把 indicator 當成因果解釋，而不是歷史模式摘要
- 只看 in-sample 最佳參數
- 拿絕對報酬炫耀，卻不和 benchmark 比
- 忽略 drawdown 與 recovery time
- 忽略交易成本、slippage 與執行限制
- 在不同資料頻率與市場 regime 之間直接搬用同一組規則

很多「看起來有效」的策略，問題不在數學錯，而是在研究設計太寬鬆。

## Suggested Reading Path

如果你是從這個 finance 模組一路往下讀，這一頁最適合放在:

1. [Financial Data Ingestion and Cleaning](financial-data-ingestion-and-cleaning.md) 之後，因為回測前一定要先處理市場資料。
2. [Stock Price Simulation and Volatility](stock-price-simulation-and-volatility.md) 附近，因為交易訊號和 volatility、price path 直覺高度相關。
3. [Portfolio Analysis](portfolio-analysis.md) 之前或之後都可以，取決於你想先看單策略規則，還是先看多資產配置。
