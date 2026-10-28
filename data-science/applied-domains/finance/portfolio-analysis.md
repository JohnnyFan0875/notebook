# Portfolio Analysis

portfolio analysis 處理的不是單一資產好不好，而是一組資產放在一起之後，風險、報酬、分散效果與相對基準表現會變成什麼樣子。單看個股常容易忽略配置問題，但真正的投資結果通常是 weights 決定的。

Key point: portfolio analysis 的核心不是挑出「最好」的資產，而是理解資產如何一起工作，以及權重如何改變整體風險與報酬。

## What a Portfolio Is

portfolio 是一組投資部位的集合，可能包含:

- stocks
- bonds
- commodities
- currencies
- funds or ETFs

這裡最重要的觀念不是資產類別本身，而是它們如何被組合，以及這種組合如何影響總體結果。

## Portfolio vs. Fund vs. Index

這三個詞很常一起出現，但角色不同:

- portfolio: 一組實際持有或設計的投資配置
- fund: 由投資人共同出資、經理人管理的投資池
- index: 用來代表市場或市場某一部分的基準組合

這個 distinction 很重要，因為很多分析其實是在問:

- 我的 portfolio 相對於某個 benchmark index 表現如何？
- 我是在做 active allocation，還是盡量貼近 index？

## Active vs. Passive Investing

portfolio analysis 很多時候都要先回答自己的框架是什麼:

- passive investing: 盡量貼近 benchmark
- active investing: 刻意偏離 benchmark，追求超額報酬

這會直接影響你後面要看的指標:

- passive 更在意 tracking error
- active 更在意 active return、active weights 與 factor bets

## Why Diversification Matters

diversification 的價值不只是「多買幾檔」，而是讓不同風險來源不要在同一時間全部發作。

好的分散通常意味著組合中資產在以下面向具有差異:

- industry
- country
- business cycle exposure
- risk level
- factor exposure

因此分散效果來自相關性結構，而不只是持有數量。

## Portfolio Weights

portfolio weights 描述每個資產占整體組合的比重。它們是 portfolio analysis 的真正控制桿，因為:

- 同一批資產，不同 weights 會產生完全不同的風險報酬輪廓
- weights 反映投資策略，也反映主動押注的位置

常見配置思路包括:

- equal-weighted
- market-cap weighted
- optimized weights based on risk-return objectives

## Portfolio Returns

portfolio return 通常就是 individual asset returns 的加權和。從價格資料出發，最常見流程是:

1. 先把 prices 轉成 returns
2. 再用 weights 對 returns 加權
3. 視需要繼續算 cumulative return 或 annualized return

這裡要特別小心，不同 return 定義回答的是不同問題，不應混著解讀。

如果是多期 portfolio，還要再分清楚兩種權重邏輯:

- buy-and-hold weights: 權重會隨資產表現自然漂移
- rebalanced weights: 權重在固定頻率下被拉回目標配置

這個 distinction 很重要，因為同一組資產、同一組初始 weights，在不同 rebalancing rule 下會走出不同的績效與風險路徑。

## Mean, Cumulative, and Annualized Returns

portfolio analysis 裡最常混淆的幾個概念包括:

- average return
- cumulative return
- annual return
- annualized return

它們差異的核心在於:

- 是否有考慮 compounding
- 時間尺度是否可比

如果比較不同持有期間或不同策略，annualized return 往往比簡單平均值更有意義，因為它把時間尺度和 compounding 一起納入。

這裡也常要區分:

- arithmetic mean return: 適合描述單期平均表現
- geometric mean return: 適合描述多期複利成長結果

幾何平均通常比較貼近投資人真正拿到的 wealth path，因為它會把波動造成的 compounding drag 算進去。

## Portfolio Risk: Variance, Volatility, and Correlation

portfolio risk 不是把每個資產風險做加權平均就好，因為相關性會改變總體波動。

要理解 portfolio volatility，通常需要一起看:

- each asset's variance
- pairwise covariance / correlation
- portfolio weights

這也是為什麼 covariance matrix 在 portfolio analysis 裡是中心工具。

## Risk-Adjusted Return

單看報酬率通常不夠，因為高報酬可能只是高風險的結果。risk-adjusted return 的重點是問:

- 這份報酬是否值得它承擔的風險？

這種比較方式讓不同策略、不同波動程度的 portfolio 可以放在同一個框架下評估。

## Sharpe Ratio

Sharpe ratio 是最常見的 risk-adjusted metric。它用超額報酬除以 total volatility，回答的是:

- 每承擔一單位總波動，拿到多少超額報酬？

Sharpe ratio 好用的地方是簡潔，但它也預設:

- volatility 可合理代表風險
- upside 和 downside fluctuation 一視同仁

這在非對稱分布下不一定足夠。

這裡的「超額報酬」不是 total return，而是:

- excess return = portfolio return - risk-free rate

同樣 10% 的 portfolio return，在不同 risk-free environment 下，對投資人代表的 reward 其實不同。這也是為什麼 Sharpe ratio、CAPM 和很多 factor model 都先把 risk-free rate 扣掉。

## Sortino Ratio and Downside Risk

如果你認為真正需要在意的是 downside 而不是全部波動，Sortino ratio 會更貼近這個想法。它把 denominator 換成 downside deviation，因此更聚焦在「壞的波動」。

這對下列情境尤其有用:

- returns 明顯偏態
- 大家更在意 loss control than upside fluctuation
- 風險管理語境重視 downside protection

同一類概念也延伸到:

- semi-deviation: 只衡量 downside 波動
- Value at Risk (VaR): 在某個信心水準下，單期可能遭遇的損失門檻
- Expected Shortfall (ES, CVaR): 超過 VaR 之後，尾端損失的平均嚴重程度

VaR 比較像門檻，ES 則更能描述 tail risk 的破壞力，因此在 fat-tail 或非對稱報酬下通常更值得一起看。

## Maximum Drawdown

maximum drawdown 問的是: 從歷史高點到後續低點，最大的累積跌幅是多少？

這個指標很受歡迎，因為它比 daily volatility 更貼近投資人實際痛感。它也提醒我們:

- 一條波動不大的策略，仍可能有很難熬的 prolonged drawdown
- recovery time 本身也是風險的一部分

## Non-Normal Returns

portfolio returns 在現實裡很少完美 normal，因此只看 mean 和 standard deviation 常會漏掉重要資訊。常見要補看的分布形狀包括:

- skewness
- kurtosis

如果分布偏左、tail 很厚，很多「表面上不錯」的 risk-adjusted metrics 其實可能低估真正 downside。

實務上這也是為什麼 portfolio monitoring 常不會只停在 Sharpe ratio，而會把 downside deviation、VaR、ES、drawdown 一起放進 dashboard。

## Benchmarks, Active Return, and Tracking Error

一旦 portfolio 是拿來對比 benchmark，就需要再多一層相對分析。

- active return: portfolio 相對 benchmark 的超額報酬
- tracking error: portfolio 與 benchmark return 差異的波動程度

這兩個指標分別適合不同任務:

- active manager 想知道自己是否真的創造 alpha
- passive manager 想知道自己是否忠實追蹤 benchmark

如果是更完整的 benchmark-relative review，也常一起看:

- information ratio: active return 相對於 tracking error 的效率
- maximum relative drawdown: portfolio 相對 benchmark 最難熬的落後區段

這些指標比單看 absolute return 更能反映「你偏離 benchmark 之後，到底換到了什麼」。

## Active Weights

active weights 是 portfolio weights 減 benchmark weights。它直接揭露你在哪些資產、產業或風格上做了偏離。

這很重要，因為很多表現差異其實不是來自選股能力，而是來自:

- sector overweight / underweight
- country bet
- style tilt

## Factor Exposures

portfolio analysis 不只看 holdings，也常看 factor exposures。這是在回答:

- portfolio 的表現和哪些 common factors 一起移動？
- portfolio 的風險是市場風險、value、quality、momentum 還是其他因子在驅動？

最直接的做法通常是:

- 看相關性
- 看 rolling correlation
- 用 regression 估 factor betas

若先從最簡單的單因子世界開始，beta 可以理解成:

- portfolio 對 broad market excess return 的敏感度

beta 大於 1，代表組合相對市場更放大；beta 小於 1，代表市場波動傳遞到組合時比較被稀釋。這種 market beta 觀點，就是從 CAPM 走向多因子模型的起點。

## Factor Models and Performance Attribution

像 Fama-French 這類多因子模型的實用價值，在於把報酬拆成:

- 可由 common factors 解釋的部分
- 尚未被解釋的 alpha

這讓 portfolio analysis 從「賺了多少」進一步走到「為什麼賺、靠什麼賺」。

在單因子 CAPM 裡，常見寫法是:

- portfolio excess return = alpha + beta * market excess return + residual

這個式子最有用的地方，不是它一定完全正確，而是它把三件事拆開了:

- risk-free rate 是 baseline
- beta 是 systematic market exposure
- alpha 是模型沒解釋掉的部分

如果再往上擴展到 Fama-French 3-factor，則會多出:

- SMB exposure: 對 small minus big 因子的暴露
- HML exposure: 對 high minus low 因子的暴露

這讓 portfolio analysis 不只知道「像不像市場」，還能知道它偏向什麼風格。

## Estimating Beta in Practice

beta 的常見估法至少有兩條路:

- covariance approach: `Cov(portfolio, market) / Var(market)`
- regression approach: 用 portfolio excess return 對 market excess return 做 OLS

兩者在簡單設定下通常會得到接近結果，但 regression 形式更容易延伸到:

- alpha estimation
- R-squared / adjusted R-squared
- multi-factor extensions

如果 beta 很高但 R-squared 很低，代表「有市場暴露」不等於「大部分波動都能被市場解釋」。這在實務上很重要，因為 exposure strength 和 explanatory power 不是同一件事。

## Efficient Frontier and Portfolio Optimization

當問題從描述現況變成設計更好的配置時，就會進入 portfolio optimization。

Markowitz framework 的經典問題是:

- 對給定風險，最大化期望報酬
- 對給定期望報酬，最小化風險

把不同 target return 或 target risk 下的最優解連起來，就得到 efficient frontier。

在這類問題裡，目標函數與限制式通常要一起說清楚。常見組合像是:

- objective: maximize expected return
- objective: minimize variance
- objective: maximize Sharpe ratio
- constraint: fully invested
- constraint: long-only
- constraint: target return fixed

沒有把 constraints 講清楚的 optimal portfolio，通常都只是數學解，不一定是可投資解。

## Maximum Sharpe vs. Minimum Volatility

兩個最常見的優化點是:

- maximum Sharpe portfolio
- minimum volatility portfolio

兩者都在 efficient frontier 上，但服務不同需求:

- max Sharpe 偏向追求最好的風險報酬比
- min volatility 偏向先控制風險，再接受較低報酬

沒有哪個永遠更好，關鍵在投資人的 objective 和 risk appetite。

## Better Estimates for Risk and Return

portfolio optimization 的脆弱點，常常不是解法，而是輸入:

- expected returns
- covariance matrix

若單純用長期歷史平均與 sample covariance，可能對 regime shifts 不夠敏感。常見改良包括:

- exponentially weighted mean returns
- exponentially weighted covariance
- semicovariance for downside-focused risk

這些做法都是在承認一件事: 最近的資料往往比很久以前的資料更 relevant。

更進一步來看，sample mean 和 sample covariance 常常是最方便的起點，但未必是最穩的起點。當資產數變多、樣本數不夠長時，估計誤差很容易被 optimizer 放大。

因此實務上常見替代思路包括:

- shrinkage estimators: 把極端 sample estimate 往更穩定的 target 拉回
- factor models: 用較少因子近似高維 covariance 結構
- Black-Litterman style views: 把市場隱含均衡與主觀觀點合併
- robust statistics: 降低 outlier 或非典型樣本對 moments 的破壞

這些方法的共同目的不是讓模型更華麗，而是讓 optimized weights 不要對資料噪音過度敏感。

## Rolling Analysis and Time Variation

portfolio performance 很少是靜態的。均值、波動、相關性、Sharpe ratio，甚至 factor exposure 都可能隨時間改變，因此單一整段 sample 的 summary 常會把 regime change 蓋掉。

rolling analysis 的核心做法是:

1. 選一個固定 window
2. 在每個時間點只用最近那段資料估計指標
3. 觀察指標如何隨時間漂移

window 太短會讓估計很 noisy，window 太長又可能把舊 regime 混進來。rolling window 的選擇，本質上是在 stability 與 responsiveness 之間做取捨。

如果 rolling analysis 進一步用在 optimization，就會變成很典型的實務流程:

1. 用 training window 估 moments
2. 在 rebalance date 算出新 weights
3. 在下一段持有期間套用這組 weights
4. 重複整個流程並比較 out-of-sample path

這比一次性靜態最佳化更接近真實投資管理。

## Risk Contribution and Risk Budgeting

portfolio risk 不只可以問「總波動多少」，也可以問「每個部位對總風險貢獻多少」。

- marginal risk contribution: 權重多增加一點時，總風險怎麼變
- component risk contribution: 每個資產實際分到多少組合風險
- percent risk contribution: 每個資產占總風險的比例

這個框架很適合拆解一個看似分散的 portfolio，因為名目 weights 很平均，不代表 risk budget 也平均。高波動或高相關資產，常會吃掉遠高於權重占比的風險。

## Estimation Error and Backtest Discipline

portfolio optimization 很容易看起來很厲害，直到你把它放進 out-of-sample 才發現結果不穩。原因通常不是 optimizer 壞掉，而是 expected return 與 covariance estimate 本身就有 estimation error。

因此比起只看 in-sample efficient frontier，更重要的是:

- 把資料切成 estimation sample 與 evaluation sample
- 嚴格避免 look-ahead bias
- 用 out-of-sample 結果檢查配置是否真的可用

如果回測時用了未來才知道的資訊，再漂亮的 Sharpe ratio 也沒有決策價值。好的 portfolio analysis 不只是在算最優權重，也是在檢查這些權重是否能在真實時間序列裡活下來。

## R Workflow Notes

如果用 R 做 portfolio analysis，`PerformanceAnalytics` 是常見工具箱，常搭配:

- `Return.calculate()` 把價格資料轉成報酬
- `Return.portfolio()` 根據 weights 聚合成 portfolio return

工具本身不重要，重要的是流程要一致: 先定義 return convention、再定義 weights 與 rebalancing rule、最後才比較 performance metrics。這樣不同策略的結果才有可比性。

如果進一步做 portfolio optimization，另一個常見工具箱是 `PortfolioAnalytics`。它的典型 workflow 可以拆成三步:

1. portfolio specification: 定義 assets、constraints 與 objectives
2. run optimization: 選 solver，求解 weights
3. analyze results: 檢查權重、風險報酬位置與回測表現

這種拆法的好處是，你可以清楚分離:

- 你想要什麼 objective
- 你允許什麼 constraints
- 你用了什麼估計方法與 solver

一旦三者混在一起，之後很難回頭判斷結果到底是策略觀點、估計假設，還是求解器行為造成的。

## Backtesting and Professional Tools

portfolio analysis 最後常需要回到實務工具與流程，例如:

- backtesting strategy performance
- holdings and sector exposure tear sheets
- risk / return attribution dashboards
- optimization backtests with periodic rebalancing

工具本身不是重點，重點是你有沒有把 portfolio 的 performance、risk、exposure 和 benchmark relation 放進同一個 review workflow。

在 optimization 類策略裡，還要再多看幾個 execution detail:

- rebalance frequency
- training period length
- rolling window length
- solver stability

這些設定不是 implementation trivia，而是策略定義本身。季度再平衡和月度再平衡，可能就已經是兩個不同策略。

## A Practical Portfolio Analysis Workflow

1. 先定義 portfolio、benchmark 與 weights。
2. 從價格資料算 returns、cumulative return 與 annualized return。
3. 用 covariance / correlation 看 portfolio risk。
4. 再看 Sharpe、Sortino、drawdown 等 risk-adjusted metrics。
5. 若有 benchmark，補看 active return、tracking error 與 active weights。
6. 若想知道表現來源，做 factor exposure 與 factor attribution。
7. 若想重新設計組合，先決定 moments 的估計方式，再進入 efficient frontier 與 optimization。
8. 若策略需要持續調整 weights，做 periodic rebalancing 的 out-of-sample backtest。

## Common Mistakes

- 把平均報酬直接拿來比較不同期間策略，卻沒有做 annualization。
- 以為多持有幾檔就一定有 diversification，卻沒有看相關性。
- 只看 Sharpe ratio，沒有看 drawdown 或 downside risk。
- 把 active return 和 tracking error 混在一起解讀。
- 用最佳化模型產出的 weights 當成真理，卻沒有懷疑輸入的 `mu` 和 `Sigma`。
- 直接拿 sample covariance 做高維最佳化，卻忽略 estimation error 會被 optimizer 放大。
- 做了回測，卻沒有把 rebalance rule、training window 與 solver choice 一起記錄清楚。

## Practical Reminders

- 在 portfolio 層級，weights 本身就是投資觀點的表達。
- 一個「好看」的 optimized portfolio，可能只是因為輸入估計太樂觀。
- 若你想快速看清一個策略的真實體感，通常先看 cumulative return、drawdown 和 exposure，再看單一 summary ratio。
