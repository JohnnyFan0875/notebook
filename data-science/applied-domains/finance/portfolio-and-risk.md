[Data Science](../../README.md) › [應用領域](../README.md) › [Finance](README.md) › 投資組合與風險

# Portfolio and Risk

投資組合分析、量化風險管理與股價模擬三篇合併而成：先看報酬、波動與分散（組合層級），再把不確定性轉成 VaR / CVaR 等可監控的風險量，最後用模擬把波動度變成價格區間。通用方法見 [蒙地卡羅模擬](../../statistics/probability-and-distributions/monte-carlo-simulation.md)、[時間序列](../../statistics/time-series-analysis/README.md)。

## Portfolio Analysis

portfolio analysis 處理的不是單一資產好不好，而是一組資產放在一起之後，風險、報酬、分散效果與相對基準表現會變成什麼樣子。單看個股常容易忽略配置問題，但真正的投資結果通常是 weights 決定的。

Key point: portfolio analysis 的核心不是挑出「最好」的資產，而是理解資產如何一起工作，以及權重如何改變整體風險與報酬。

### What a Portfolio Is

portfolio 是一組投資部位的集合，可能包含:

- stocks
- bonds
- commodities
- currencies
- funds or ETFs

這裡最重要的觀念不是資產類別本身，而是它們如何被組合，以及這種組合如何影響總體結果。

### Portfolio vs. Fund vs. Index

這三個詞很常一起出現，但角色不同:

- portfolio: 一組實際持有或設計的投資配置
- fund: 由投資人共同出資、經理人管理的投資池
- index: 用來代表市場或市場某一部分的基準組合

這個 distinction 很重要，因為很多分析其實是在問:

- 我的 portfolio 相對於某個 benchmark index 表現如何？
- 我是在做 active allocation，還是盡量貼近 index？

### Active vs. Passive Investing

portfolio analysis 很多時候都要先回答自己的框架是什麼:

- passive investing: 盡量貼近 benchmark
- active investing: 刻意偏離 benchmark，追求超額報酬

這會直接影響你後面要看的指標:

- passive 更在意 tracking error
- active 更在意 active return、active weights 與 factor bets

### Why Diversification Matters

diversification 的價值不只是「多買幾檔」，而是讓不同風險來源不要在同一時間全部發作。

好的分散通常意味著組合中資產在以下面向具有差異:

- industry
- country
- business cycle exposure
- risk level
- factor exposure

因此分散效果來自相關性結構，而不只是持有數量。

### Portfolio Weights

portfolio weights 描述每個資產占整體組合的比重。它們是 portfolio analysis 的真正控制桿，因為:

- 同一批資產，不同 weights 會產生完全不同的風險報酬輪廓
- weights 反映投資策略，也反映主動押注的位置

常見配置思路包括:

- equal-weighted
- market-cap weighted
- optimized weights based on risk-return objectives

### Portfolio Returns

portfolio return 通常就是 individual asset returns 的加權和。從價格資料出發，最常見流程是:

1. 先把 prices 轉成 returns
2. 再用 weights 對 returns 加權
3. 視需要繼續算 cumulative return 或 annualized return

這裡要特別小心，不同 return 定義回答的是不同問題，不應混著解讀。

如果是多期 portfolio，還要再分清楚兩種權重邏輯:

- buy-and-hold weights: 權重會隨資產表現自然漂移
- rebalanced weights: 權重在固定頻率下被拉回目標配置

這個 distinction 很重要，因為同一組資產、同一組初始 weights，在不同 rebalancing rule 下會走出不同的績效與風險路徑。

### Mean, Cumulative, and Annualized Returns

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

### Portfolio Risk: Variance, Volatility, and Correlation

portfolio risk 不是把每個資產風險做加權平均就好，因為相關性會改變總體波動。

要理解 portfolio volatility，通常需要一起看:

- each asset's variance
- pairwise covariance / correlation
- portfolio weights

這也是為什麼 covariance matrix 在 portfolio analysis 裡是中心工具。

### Risk-Adjusted Return

單看報酬率通常不夠，因為高報酬可能只是高風險的結果。risk-adjusted return 的重點是問:

- 這份報酬是否值得它承擔的風險？

這種比較方式讓不同策略、不同波動程度的 portfolio 可以放在同一個框架下評估。

### Sharpe Ratio

Sharpe ratio 是最常見的 risk-adjusted metric。它用超額報酬除以 total volatility，回答的是:

- 每承擔一單位總波動，拿到多少超額報酬？

Sharpe ratio 好用的地方是簡潔，但它也預設:

- volatility 可合理代表風險
- upside 和 downside fluctuation 一視同仁

這在非對稱分布下不一定足夠。

這裡的「超額報酬」不是 total return，而是:

- excess return = portfolio return - risk-free rate

同樣 10% 的 portfolio return，在不同 risk-free environment 下，對投資人代表的 reward 其實不同。這也是為什麼 Sharpe ratio、CAPM 和很多 factor model 都先把 risk-free rate 扣掉。

### Sortino Ratio and Downside Risk

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

### Maximum Drawdown

maximum drawdown 問的是: 從歷史高點到後續低點，最大的累積跌幅是多少？

這個指標很受歡迎，因為它比 daily volatility 更貼近投資人實際痛感。它也提醒我們:

- 一條波動不大的策略，仍可能有很難熬的 prolonged drawdown
- recovery time 本身也是風險的一部分

### Non-Normal Returns

portfolio returns 在現實裡很少完美 normal，因此只看 mean 和 standard deviation 常會漏掉重要資訊。常見要補看的分布形狀包括:

- skewness
- kurtosis

如果分布偏左、tail 很厚，很多「表面上不錯」的 risk-adjusted metrics 其實可能低估真正 downside。

實務上這也是為什麼 portfolio monitoring 常不會只停在 Sharpe ratio，而會把 downside deviation、VaR、ES、drawdown 一起放進 dashboard。

### Benchmarks, Active Return, and Tracking Error

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

### Active Weights

active weights 是 portfolio weights 減 benchmark weights。它直接揭露你在哪些資產、產業或風格上做了偏離。

這很重要，因為很多表現差異其實不是來自選股能力，而是來自:

- sector overweight / underweight
- country bet
- style tilt

### Factor Exposures

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

### Factor Models and Performance Attribution

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

### Estimating Beta in Practice

beta 的常見估法至少有兩條路:

- covariance approach: `Cov(portfolio, market) / Var(market)`
- regression approach: 用 portfolio excess return 對 market excess return 做 OLS

兩者在簡單設定下通常會得到接近結果，但 regression 形式更容易延伸到:

- alpha estimation
- R-squared / adjusted R-squared
- multi-factor extensions

如果 beta 很高但 R-squared 很低，代表「有市場暴露」不等於「大部分波動都能被市場解釋」。這在實務上很重要，因為 exposure strength 和 explanatory power 不是同一件事。

### Efficient Frontier and Portfolio Optimization

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

### Maximum Sharpe vs. Minimum Volatility

兩個最常見的優化點是:

- maximum Sharpe portfolio
- minimum volatility portfolio

兩者都在 efficient frontier 上，但服務不同需求:

- max Sharpe 偏向追求最好的風險報酬比
- min volatility 偏向先控制風險，再接受較低報酬

沒有哪個永遠更好，關鍵在投資人的 objective 和 risk appetite。

### Better Estimates for Risk and Return

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

### Rolling Analysis and Time Variation

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

### Risk Contribution and Risk Budgeting

portfolio risk 不只可以問「總波動多少」，也可以問「每個部位對總風險貢獻多少」。

- marginal risk contribution: 權重多增加一點時，總風險怎麼變
- component risk contribution: 每個資產實際分到多少組合風險
- percent risk contribution: 每個資產占總風險的比例

這個框架很適合拆解一個看似分散的 portfolio，因為名目 weights 很平均，不代表 risk budget 也平均。高波動或高相關資產，常會吃掉遠高於權重占比的風險。

### Estimation Error and Backtest Discipline

portfolio optimization 很容易看起來很厲害，直到你把它放進 out-of-sample 才發現結果不穩。原因通常不是 optimizer 壞掉，而是 expected return 與 covariance estimate 本身就有 estimation error。

因此比起只看 in-sample efficient frontier，更重要的是:

- 把資料切成 estimation sample 與 evaluation sample
- 嚴格避免 look-ahead bias
- 用 out-of-sample 結果檢查配置是否真的可用

如果回測時用了未來才知道的資訊，再漂亮的 Sharpe ratio 也沒有決策價值。好的 portfolio analysis 不只是在算最優權重，也是在檢查這些權重是否能在真實時間序列裡活下來。

### R Workflow Notes

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

### Backtesting and Professional Tools

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

### A Practical Portfolio Analysis Workflow

1. 先定義 portfolio、benchmark 與 weights。
2. 從價格資料算 returns、cumulative return 與 annualized return。
3. 用 covariance / correlation 看 portfolio risk。
4. 再看 Sharpe、Sortino、drawdown 等 risk-adjusted metrics。
5. 若有 benchmark，補看 active return、tracking error 與 active weights。
6. 若想知道表現來源，做 factor exposure 與 factor attribution。
7. 若想重新設計組合，先決定 moments 的估計方式，再進入 efficient frontier 與 optimization。
8. 若策略需要持續調整 weights，做 periodic rebalancing 的 out-of-sample backtest。

### Common Mistakes

- 把平均報酬直接拿來比較不同期間策略，卻沒有做 annualization。
- 以為多持有幾檔就一定有 diversification，卻沒有看相關性。
- 只看 Sharpe ratio，沒有看 drawdown 或 downside risk。
- 把 active return 和 tracking error 混在一起解讀。
- 用最佳化模型產出的 weights 當成真理，卻沒有懷疑輸入的 `mu` 和 `Sigma`。
- 直接拿 sample covariance 做高維最佳化，卻忽略 estimation error 會被 optimizer 放大。
- 做了回測，卻沒有把 rebalance rule、training window 與 solver choice 一起記錄清楚。

### Practical Reminders

- 在 portfolio 層級，weights 本身就是投資觀點的表達。
- 一個「好看」的 optimized portfolio，可能只是因為輸入估計太樂觀。
- 若你想快速看清一個策略的真實體感，通常先看 cumulative return、drawdown 和 exposure，再看單一 summary ratio。

## Quantitative Risk Management

quantitative risk management 關心的不是「市場會不會有風險」，而是如何把不確定性轉成可以估計、比較、監控與決策的量。對金融投資組合來說，這通常意味著先理解報酬與損失分布，再決定要用什麼風險指標和管理框架。

Key point: risk management 不是只算一個數字，而是把 risk factors、loss distribution、risk appetite 與 decision rule 串成一套流程。

### What Risk Management Is Trying to Do

在金融投資組合裡，未來報酬永遠不確定。risk management 的角色不是消除這些不確定性，而是:

- 量化可能損失
- 辨識主要風險來源
- 控制部位暴露
- 在既定 risk appetite 下做更好的投資決策

因此風險管理同時是一個 measurement problem，也是一個 decision problem。

### Risk Factors vs. Risk-Factor Returns

很多時候，真正進入模型的不是 risk factor level 本身，而是它們的變化量，也就是 returns。

常見定義包括:

- simple returns
- relative returns
- log-returns

其中 log-returns 很常用，因為:

- 小變動下和 relative returns 很接近
- 多期 aggregation 可直接相加
- 在某些經典模型下有較方便的統計性質

### Aggregating Returns Across Horizons

risk management 很少只看單日風險。你常常需要從 daily returns 走到 weekly、monthly 或更長 horizon。

這時候至少要清楚:

- 你在聚合的是哪種 return
- 時間尺度 बदल後，normality、dependence 與 tail behavior 會不會也改變

這也是為什麼風險分析裡的 time horizon choice 不是技術細節，而是模型假設的一部分。

### Volatility as a First Risk Measure

volatility 是最常見的第一步風險指標。它描述報酬圍繞平均值的分散程度，也常被拿來當作 portfolio uncertainty 的 proxy。

它的優點是:

- 計算直觀
- 易於比較不同資產或策略
- 和 covariance matrix 以及 modern portfolio theory 可以自然接軌

但 volatility 也有侷限:

- 對 upside / downside fluctuation 一視同仁
- 不直接告訴你 tail loss 有多嚴重
- 依賴分布與穩定性假設

如果要把 daily volatility 轉成 annualized volatility，常見做法是乘上 `sqrt(T)`。這個 scaling rule 很方便，但背後其實假設:

- 報酬近似獨立
- 波動在該 horizon 內沒有劇烈 regime shift

因此它比較像 baseline approximation，而不是任何情況都精準成立的定律。

### Risk Factors and Risk Exposure

要做真正的 risk management，不能只停在「波動大不大」，還要問:

- 是哪些 factor 在驅動風險？
- portfolio 對這些 factor 暴露多大？

常見 risk factors 包括:

- market-wide movements
- interest rate changes
- inflation shifts
- sector-specific shocks
- issuer-specific default risk

其中一些是 systematic risk，另一些是 idiosyncratic risk。真正重要的是辨認哪些因子會在壞時候一起發作。

### Loss Distribution

一旦 risk management 的問題從「報酬波動多大」轉成「最糟會賠多少」，重心就會落到 loss distribution。

這裡的關鍵轉換是:

- 不只看 average return
- 也要看 losses 的整體分布
- 特別是 distribution 的 tail

因為很多金融風險不是日常小波動，而是少數極端事件決定生死。

### Value at Risk

VaR 問的是: 在某個 confidence level 下，損失大致不會超過多少？

例如 95% VaR 可以理解成:

- 95% 的情況下，損失不會超過某個門檻
- 但剩下 5% 的 tail，可能更糟

VaR 很常用，因為它直觀、好溝通，也常用於風控報表與監理語境。

但它不是完整答案，因為它只告訴你 cutoff，不告訴你超過 cutoff 之後會有多慘。

實務上至少可以區分三種常見思路:

- historical VaR: 直接用歷史分位數當作 loss cutoff
- parametric VaR: 假設某個分布，例如 Normal，再用參數估計分位數
- Monte Carlo VaR: 先模擬大量可能情境，再從模擬損失中讀出分位數

這三種方法的主要差別，不在公式複不複雜，而在你願意把多少結構假設放進 loss distribution。

### Conditional Value at Risk

CVaR 又常被叫 expected shortfall。它問的是:

- 一旦損失已經超過 VaR 門檻，那 tail 裡的平均損失是多少？

這使它在 tail-risk 管理上通常比 VaR 更有資訊量，因為它真的在看尾部的嚴重程度，而不只是邊界位置。

如果用 historical method，CVaR 的直觀做法通常就是:

1. 先找出 VaR cutoff
2. 只留下比 cutoff 更差的那一段損失
3. 對這段 tail losses 取平均

這也是為什麼 CVaR 常被視為 tail severity 的指標，而不只是 tail boundary 的補充說明。

### Risk Exposure Depends on More Than Loss Size

一個風險情境值不值得在意，不只看 loss measure 本身，也要看:

- 該損失發生的機率
- 決策者的 risk tolerance / risk appetite

也就是說，風險暴露不是單一數字，而是 probability、severity 和 preference 的結合。

### Choosing a Loss Distribution

很多 quant risk problem 最後都會落到: 你假設損失服從什麼分布？

常見起點包括:

- Normal distribution
- Student's t distribution
- historical empirical distribution
- Monte Carlo generated distribution

其中 t-distribution 常被拿來描述 fat tails，因為它比 Normal 更容易產生大損失。這對金融 returns 很常更貼近現實。

### Normality Is Convenient, Not Guaranteed

Normal distribution 在風險管理裡很常出現，因為它:

- 參數少
- 容易估計
- 計算 VaR / CVaR 很方便

但金融 returns 經常表現出:

- heavier tails
- volatility clustering
- occasional skewness

所以 normality 比較像 baseline approximation，而不是預設真相。

### Checking Distributional Assumptions

如果你想知道資料離 normal 有多遠，常見的檢查方式包括:

- histogram 與 fitted density 對照
- Q-Q plot
- skewness and kurtosis
- Jarque-Bera type tests

這些工具的角色不是替你選模型，而是提醒你 tail behavior 和 shape 可能已經和常態假設偏離。

### Stylized Facts of Financial Returns

很多金融 return series 反覆出現一些經典現象:

- tails 比 normal 更重
- volatility 會隨時間改變
- raw returns 的 serial correlation 通常不強
- absolute returns 常有明顯 serial correlation
- extremes 常成群出現
- 聚合到較長 horizon 時，分布有時會比較接近 normal

這些 stylized facts 幾乎就是 quant risk 建模的背景常識。忽略它們，模型通常會過度簡化。

### Dependence, Serial Correlation, and Volatility Clustering

即使平均報酬本身沒有很明顯的自相關，risk 仍可能高度依賴時間，因為 volatility clustering 很常見:

- 平靜期之後還是平靜
- 劇烈波動之後常接著劇烈波動

這就是為什麼只看 return autocorrelation 不夠，也常要看:

- absolute returns
- squared returns
- rolling volatility

### Historical Simulation

historical simulation 是很實務的一種方法: 不先假設 parametric distribution，而是直接重採樣或重放歷史 risk-factor moves，觀察它們對當前 portfolio 的影響。

它的好處是:

- 直觀
- 容易溝通
- 不需要先強加 Normal 或 t 假設

但它也隱含一個強前提:

- 過去看到的風險情境，對未來仍有代表性

所以 historical simulation 本身仍然繞不開 stationarity 問題。

但它也有一個很重要的優勢: 如果歷史資料本身就含有偏態、厚尾或不對稱，historical VaR / CVaR 會直接把這些形狀保留下來，而不會先被 Normal 假設抹平。

### Monte Carlo Simulation

Monte Carlo risk analysis 的核心想法不是「算更複雜」，而是:

1. 先指定或估計一個可抽樣的分布
2. 產生大量模擬 returns 或 risk-factor shocks
3. 把每個情境映射成 portfolio P&L
4. 再從模擬分布裡讀出 VaR、CVaR 或其他 tail measure

它的價值在於能處理歷史上沒出現過、但模型認為合理的情境。不過一旦模擬分布設錯，再多次抽樣也只是把錯誤假設放大。

### Stationarity and Structural Breaks

幾乎所有風險估計技術，都在某種程度上依賴 stationarity 假設，也就是:

- 分布不隨時間改變
- 過去資料仍能代表未來資料

問題在於金融市場常常不 stationary。危機、政策變化、制度切換都可能造成 structural breaks。當 break 發生時，過去估計出的 volatility、covariance 或 tail behavior 可能瞬間失效。

### Detecting Breaks and Volatility Shifts

structural breaks 可以透過:

- visual inspection
- regression-based tests such as Chow test
- rolling window volatility

來輔助辨認。

這些方法的價值不在於神準找出單一 break point，而在於提醒你:

- 分布可能已經變了
- 同一套 historical risk estimate 可能不再適用
- 需要重新分段估計，或改用更能處理時變 volatility 的模型

### Backtesting Risk Measures

風險模型不能只計算，還要回頭檢查它在歷史資料上的表現。這就是 backtesting 的意義。

對 VaR 來說，一個很自然的問題是:

- 如果你說 95% VaR 是某個門檻，那實際上是不是大約只有 5% 的歷史損失超過它？

如果 exceedance 太多，模型可能低估尾部；如果太少，模型可能太保守或分布假設不對。

同理，若你把 one-day risk 用 `sqrt(horizon)` 放大到多日 horizon，也應該回頭檢查這個 scaling 在真實資料上是否合理，而不是直接把它當成永遠成立的 forecast rule。

### Extreme Value Theory

當真正關心的是 tail losses 時，EVT 提供了比整體分布更聚焦的框架。它不是試圖把所有資料都擬合得很好，而是專注在極端損失。

兩個常見思路是:

- block maxima
- peaks over threshold

這些方法的目標，是更可靠地刻畫稀有但關鍵的 tail events。

### VaR and CVaR From EVT

一旦 tail distribution 被擬合出來，就可以用它來估:

- 高信賴水準的 VaR
- 對應 tail 的 CVaR

這在資本準備、reserve requirement、stress loss coverage 等場景特別重要，因為真正需要留 buffer 的，通常就是極端虧損而不是一般波動。

### Option Portfolios Add Extra Risk Dimensions

若 portfolio 裡有 options，風險管理會更複雜，因為 portfolio value 不再只被 underlying price 影響，還會被:

- implied volatility
- time to maturity
- interest rates

共同影響。

這代表 loss operator 可能不再是簡單線性 mapping，而是帶有 option pricing nonlinearity 的函數。

### Implied Volatility as a Risk Factor

對 option portfolio 來說，volatility 不只是描述性統計，而可能本身就是直接進入定價的風險因子。

直覺上:

- implied volatility 上升，option value 常上升
- market stress 時，underlying price 與 implied vol 可能一起劇烈變動

因此 option risk management 通常至少要同時看 price factor 和 vol factor，而不能只盯 underlying。

### Kernel Density Estimation

如果不想太快假設某個 parametric distribution，KDE 提供了一個比較柔性的 non-parametric 方式去平滑 histogram、逼近 loss density。

它的優點是:

- 不必先硬指定 Normal 或 t
- 能保留資料形狀的更多細節

但它也依賴:

- bandwidth choice
- sample size
- tail data 是否充足

所以 KDE 很適合 exploratory density estimation，但對極端尾部仍可能資料不足。

### Neural Networks for Risk Management

這門課還把一個更進階方向點出來: 用 neural network 直接學習 `prices -> portfolio weights` 的 mapping，讓 portfolio optimization 更即時。

這種方法的吸引力在於:

- 市場資料更新後可快速輸出新 weights
- 省去每次都做完整 optimization 的成本

但本質上，它沒有消除 risk management 問題，只是把 decision rule 用另一種函數近似方式表達。

### A Practical Risk Management Workflow

1. 先定義 portfolio 和主要 risk factors。
2. 計算 return、volatility、covariance，建立第一層風險視角。
3. 決定要用 historical、parametric 還是 Monte Carlo 的 loss distribution。
4. 計算 VaR / CVaR，必要時納入 EVT 或 KDE 等 tail-focused 方法。
5. 用 backtesting 檢查模型是否低估或高估 tail risk。
6. 若市場 regime 改變，重新評估 stationarity 與 structural breaks。
7. 把結果回連到 risk appetite、capital buffer 和 portfolio weights 調整。

### Common Mistakes

- 把 volatility 當成完整風險定義，忽略 tail losses。
- 直接套 Normal 分布，沒有檢查 fat tails 是否更合理。
- 沒有區分 risk factor levels 與 returns，就直接把資料餵進模型。
- 只檢查 raw returns 的自相關，卻忽略 absolute returns 的 clustering。
- 忘記 stationarity 只是工作假設，不是市場保證。
- 看見一個漂亮的 VaR 數字，就以為尾部風險已被理解。
- 沒有做 backtesting，就把模型拿去做真實部位控制。
- 用 `sqrt(T)` 放大 volatility 或 VaR，卻沒有檢查獨立同分布近似是否還站得住腳。

### Practical Reminders

- risk model 的價值，不在於看起來高級，而在於能不能在壞時候提供可靠訊號。
- 很多風險失敗不是因為完全沒模型，而是因為把模型假設當成現實本身。
- 若你只能多做一件事，通常是把 tail、breaks 與 backtesting 看得比平均值更重。

## Stock Price Simulation and Volatility

當金融模型開始碰到股票價格時，最麻煩的地方通常不是公式本身，而是不確定性。價格會上下波動、報酬率分布不對稱，而且今天看起來合理的路徑，明天就可能完全改觀。

Key point: 對股票價格做模型時，重點不是預測單一路徑，而是把波動、可能區間與機率分布表達清楚。

### Why Volatility Matters

股票價格難建模，最核心的原因是 volatility。它描述的是價格或報酬率在時間上的變動程度，也直接影響:

- 價格路徑看起來有多不穩定
- 未來區間有多寬
- 同樣的 expected return 會對應多大的風險

如果模型只放 expected return，卻沒有把 volatility 放進去，結果通常會看起來過度平滑，也過度自信。

### Relative Price and Daily Return

在日資料裡，常見第一步不是直接對原始價格做分析，而是先轉成相對價格或報酬率。

常見想法包括:

- relative price: 當日價格相對於前一日價格的變化
- log return: 對價格比值取自然對數

這樣做的好處是:

- 更容易比較不同時間段的變化
- 更方便和常見的連續複利模型對接
- 後續做描述統計與模擬時較自然

### Descriptive Statistics as Model Inputs

在簡化的 stock model 裡，平均報酬與標準差常是最基本的兩個輸入。

- mean: 提供平均成長或漂移方向
- standard deviation: 提供日常波動強度

這兩個量不一定能完整描述市場，但通常足夠作為第一版 simulation model 的起點。

### Annualizing Volatility

當你從 daily return 出發時，常需要把波動度轉到年化尺度，因為很多估值、風險管理或策略比較都在年尺度上討論。

直覺上:

- 日波動度反映短期變動
- 年化波動度讓不同資產或不同模型更容易在同一尺度上比較

實務上一定要先確認你使用的時間單位是一致的，否則 mean、volatility、time horizon 會互相錯位。

### Expected Return vs. Realized Return

模型裡常會區分:

- expected return: 理論上或長期平均的報酬
- realized return: 特定樣本期間實際觀察到的報酬

這個 distinction 很重要，因為 simulation 常會用 estimated return 當作輸入，但最後產出的單一路徑只是許多可能結果之一，不應被誤當成預言。

### Simulating a Simple Stock Path

一個簡化模型的核心通常是:

1. 設定初始價格
2. 給定 expected return 與 volatility
3. 為每一天抽取一個隨機 shock
4. 用新的 shock 推進下一天價格

這種模型的價值，不在於精準預測 Apple 明天收多少，而在於幫你理解:

- 高 volatility 會讓路徑多分散
- horizon 越長，不確定性累積越快
- 一樣的平均報酬，在不同風險下會對應完全不同的 price range

### Random Normals and Lognormal Prices

許多入門 stock simulation 會先假設 log returns 近似 normal，因而讓價格本身呈現 lognormal 結構。

這個假設的好處是:

- 價格不會掉到負數
- 模型和連續複利表示法相容
- 更容易計算 price range 與 probability distribution

但它仍然只是簡化。真實市場可能有 fat tails、volatility clustering、regime shifts 等現象，不會完全服從這個框架。

### Price Ranges Instead of Point Forecasts

當模型帶入 lognormal price assumption 後，輸出最好不要只停在「最終價格會是多少」，而要往前一步問:

- 合理區間大概在哪裡
- 極端但仍 plausible 的結果有多遠
- 目前市場價格落在這個分布的哪個位置

這比單點預測更誠實，也更符合不確定性的本質。

### Cumulative vs. Density Probability

在價格機率模型裡，常會同時看到兩種觀點:

- cumulative probability: 某個價格以下的累積機率
- density probability: 某個價格附近的相對機率密度

兩者用途不同:

- cumulative view 適合回答「價格低於某門檻的機率有多大」
- density view 適合回答「哪一段區間最可能出現」

如果把這兩種圖混著看，常會誤讀模型的含義。

### What the Most Likely Price Really Means

「最可能價格」不等於「一定會發生的價格」。在連續分布裡，它比較像機率密度最高的附近區間，而不是某個神奇的精準點。

因此在做圖或報告時，與其執著於單一最可能值，不如更明確地展示:

- 中心區間
- tail risk
- 分布偏態

### Spreadsheet Modeling Still Needs Statistical Discipline

即使用的是 Google Sheets，而不是 Python 或 R，模型品質仍然取決於統計與金融概念是否一致。

至少要檢查:

- mean、volatility、time step 是否使用同一尺度
- log / exp 轉換前後是否還保持定義一致
- random function 的輸出是否真的對應你假設的分布

工具不同，不代表可以省略建模紀律。

### Common Mistakes

- 直接用價格而不是報酬率做波動推估，卻沒有先處理尺度問題
- 把單次 simulation path 當成最可能真實未來
- 年化與日化參數混用
- 只看 expected return，不看 volatility 對區間寬度的影響
- 把 lognormal convenience 當成真實市場完整描述

### Practical Reminders

- stock simulation 比較適合拿來理解風險輪廓，不適合包裝成精準預測。
- 若模型輸出看起來過度平滑，先懷疑是不是波動度或隨機項被處理得太弱。
- 一張好的 price probability 圖，通常比一個單點價格更有決策價值。
