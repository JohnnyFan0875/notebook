# Quantitative Risk Management

quantitative risk management 關心的不是「市場會不會有風險」，而是如何把不確定性轉成可以估計、比較、監控與決策的量。對金融投資組合來說，這通常意味著先理解報酬與損失分布，再決定要用什麼風險指標和管理框架。

Key point: risk management 不是只算一個數字，而是把 risk factors、loss distribution、risk appetite 與 decision rule 串成一套流程。

## What Risk Management Is Trying to Do

在金融投資組合裡，未來報酬永遠不確定。risk management 的角色不是消除這些不確定性，而是:

- 量化可能損失
- 辨識主要風險來源
- 控制部位暴露
- 在既定 risk appetite 下做更好的投資決策

因此風險管理同時是一個 measurement problem，也是一個 decision problem。

## Portfolio Return and Portfolio Risk

對多資產投資組合來說，return 通常可寫成資產報酬的加權和；risk 則常以 volatility 或 covariance structure 開始衡量。

這裡的核心不是單一資產波動，而是:

- individual variances
- cross-asset covariances
- portfolio weights

因為一個 portfolio 有多危險，不只看每個資產自身波動，還要看它們彼此如何一起動。

## Risk Factors vs. Risk-Factor Returns

很多時候，真正進入模型的不是 risk factor level 本身，而是它們的變化量，也就是 returns。

常見定義包括:

- simple returns
- relative returns
- log-returns

其中 log-returns 很常用，因為:

- 小變動下和 relative returns 很接近
- 多期 aggregation 可直接相加
- 在某些經典模型下有較方便的統計性質

## Aggregating Returns Across Horizons

risk management 很少只看單日風險。你常常需要從 daily returns 走到 weekly、monthly 或更長 horizon。

這時候至少要清楚:

- 你在聚合的是哪種 return
- 時間尺度 बदल後，normality、dependence 與 tail behavior 會不會也改變

這也是為什麼風險分析裡的 time horizon choice 不是技術細節，而是模型假設的一部分。

## Volatility as a First Risk Measure

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

## Risk Factors and Risk Exposure

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

## Factor Models

factor model 的目的，是把 portfolio returns 或 volatility 對應回少數幾個風險來源。

這類模型常透過 regression 建立:

- dependent variable: portfolio return 或資產報酬
- independent variables: market, macro, style, credit 或其他 risk factors

它的價值在於把「風險從哪來」說清楚，而不是只看到結果分布。

## Modern Portfolio Theory

MPT 提供了一個很經典的風險管理視角: 對給定風險，找最高期望報酬；或對給定期望報酬，找最低風險。

這帶出幾個核心概念:

- efficient portfolio
- minimum variance portfolio
- efficient frontier

即使你最後不用 Markowitz framework 做真實交易，這套語言仍然很重要，因為它把「調整 weights 就是在改變 risk exposure」這件事講得非常清楚。

## Loss Distribution

一旦 risk management 的問題從「報酬波動多大」轉成「最糟會賠多少」，重心就會落到 loss distribution。

這裡的關鍵轉換是:

- 不只看 average return
- 也要看 losses 的整體分布
- 特別是 distribution 的 tail

因為很多金融風險不是日常小波動，而是少數極端事件決定生死。

## Value at Risk

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

## Conditional Value at Risk

CVaR 又常被叫 expected shortfall。它問的是:

- 一旦損失已經超過 VaR 門檻，那 tail 裡的平均損失是多少？

這使它在 tail-risk 管理上通常比 VaR 更有資訊量，因為它真的在看尾部的嚴重程度，而不只是邊界位置。

如果用 historical method，CVaR 的直觀做法通常就是:

1. 先找出 VaR cutoff
2. 只留下比 cutoff 更差的那一段損失
3. 對這段 tail losses 取平均

這也是為什麼 CVaR 常被視為 tail severity 的指標，而不只是 tail boundary 的補充說明。

## Risk Exposure Depends on More Than Loss Size

一個風險情境值不值得在意，不只看 loss measure 本身，也要看:

- 該損失發生的機率
- 決策者的 risk tolerance / risk appetite

也就是說，風險暴露不是單一數字，而是 probability、severity 和 preference 的結合。

## Choosing a Loss Distribution

很多 quant risk problem 最後都會落到: 你假設損失服從什麼分布？

常見起點包括:

- Normal distribution
- Student's t distribution
- historical empirical distribution
- Monte Carlo generated distribution

其中 t-distribution 常被拿來描述 fat tails，因為它比 Normal 更容易產生大損失。這對金融 returns 很常更貼近現實。

## Normality Is Convenient, Not Guaranteed

Normal distribution 在風險管理裡很常出現，因為它:

- 參數少
- 容易估計
- 計算 VaR / CVaR 很方便

但金融 returns 經常表現出:

- heavier tails
- volatility clustering
- occasional skewness

所以 normality 比較像 baseline approximation，而不是預設真相。

## Checking Distributional Assumptions

如果你想知道資料離 normal 有多遠，常見的檢查方式包括:

- histogram 與 fitted density 對照
- Q-Q plot
- skewness and kurtosis
- Jarque-Bera type tests

這些工具的角色不是替你選模型，而是提醒你 tail behavior 和 shape 可能已經和常態假設偏離。

## Stylized Facts of Financial Returns

很多金融 return series 反覆出現一些經典現象:

- tails 比 normal 更重
- volatility 會隨時間改變
- raw returns 的 serial correlation 通常不強
- absolute returns 常有明顯 serial correlation
- extremes 常成群出現
- 聚合到較長 horizon 時，分布有時會比較接近 normal

這些 stylized facts 幾乎就是 quant risk 建模的背景常識。忽略它們，模型通常會過度簡化。

## Dependence, Serial Correlation, and Volatility Clustering

即使平均報酬本身沒有很明顯的自相關，risk 仍可能高度依賴時間，因為 volatility clustering 很常見:

- 平靜期之後還是平靜
- 劇烈波動之後常接著劇烈波動

這就是為什麼只看 return autocorrelation 不夠，也常要看:

- absolute returns
- squared returns
- rolling volatility

## Historical Simulation

historical simulation 是很實務的一種方法: 不先假設 parametric distribution，而是直接重採樣或重放歷史 risk-factor moves，觀察它們對當前 portfolio 的影響。

它的好處是:

- 直觀
- 容易溝通
- 不需要先強加 Normal 或 t 假設

但它也隱含一個強前提:

- 過去看到的風險情境，對未來仍有代表性

所以 historical simulation 本身仍然繞不開 stationarity 問題。

但它也有一個很重要的優勢: 如果歷史資料本身就含有偏態、厚尾或不對稱，historical VaR / CVaR 會直接把這些形狀保留下來，而不會先被 Normal 假設抹平。

## Monte Carlo Simulation

Monte Carlo risk analysis 的核心想法不是「算更複雜」，而是:

1. 先指定或估計一個可抽樣的分布
2. 產生大量模擬 returns 或 risk-factor shocks
3. 把每個情境映射成 portfolio P&L
4. 再從模擬分布裡讀出 VaR、CVaR 或其他 tail measure

它的價值在於能處理歷史上沒出現過、但模型認為合理的情境。不過一旦模擬分布設錯，再多次抽樣也只是把錯誤假設放大。

## Stationarity and Structural Breaks

幾乎所有風險估計技術，都在某種程度上依賴 stationarity 假設，也就是:

- 分布不隨時間改變
- 過去資料仍能代表未來資料

問題在於金融市場常常不 stationary。危機、政策變化、制度切換都可能造成 structural breaks。當 break 發生時，過去估計出的 volatility、covariance 或 tail behavior 可能瞬間失效。

## Detecting Breaks and Volatility Shifts

structural breaks 可以透過:

- visual inspection
- regression-based tests such as Chow test
- rolling window volatility

來輔助辨認。

這些方法的價值不在於神準找出單一 break point，而在於提醒你:

- 分布可能已經變了
- 同一套 historical risk estimate 可能不再適用
- 需要重新分段估計，或改用更能處理時變 volatility 的模型

## Backtesting Risk Measures

風險模型不能只計算，還要回頭檢查它在歷史資料上的表現。這就是 backtesting 的意義。

對 VaR 來說，一個很自然的問題是:

- 如果你說 95% VaR 是某個門檻，那實際上是不是大約只有 5% 的歷史損失超過它？

如果 exceedance 太多，模型可能低估尾部；如果太少，模型可能太保守或分布假設不對。

同理，若你把 one-day risk 用 `sqrt(horizon)` 放大到多日 horizon，也應該回頭檢查這個 scaling 在真實資料上是否合理，而不是直接把它當成永遠成立的 forecast rule。

## Extreme Value Theory

當真正關心的是 tail losses 時，EVT 提供了比整體分布更聚焦的框架。它不是試圖把所有資料都擬合得很好，而是專注在極端損失。

兩個常見思路是:

- block maxima
- peaks over threshold

這些方法的目標，是更可靠地刻畫稀有但關鍵的 tail events。

## VaR and CVaR From EVT

一旦 tail distribution 被擬合出來，就可以用它來估:

- 高信賴水準的 VaR
- 對應 tail 的 CVaR

這在資本準備、reserve requirement、stress loss coverage 等場景特別重要，因為真正需要留 buffer 的，通常就是極端虧損而不是一般波動。

## Option Portfolios Add Extra Risk Dimensions

若 portfolio 裡有 options，風險管理會更複雜，因為 portfolio value 不再只被 underlying price 影響，還會被:

- implied volatility
- time to maturity
- interest rates

共同影響。

這代表 loss operator 可能不再是簡單線性 mapping，而是帶有 option pricing nonlinearity 的函數。

## Implied Volatility as a Risk Factor

對 option portfolio 來說，volatility 不只是描述性統計，而可能本身就是直接進入定價的風險因子。

直覺上:

- implied volatility 上升，option value 常上升
- market stress 時，underlying price 與 implied vol 可能一起劇烈變動

因此 option risk management 通常至少要同時看 price factor 和 vol factor，而不能只盯 underlying。

## Kernel Density Estimation

如果不想太快假設某個 parametric distribution，KDE 提供了一個比較柔性的 non-parametric 方式去平滑 histogram、逼近 loss density。

它的優點是:

- 不必先硬指定 Normal 或 t
- 能保留資料形狀的更多細節

但它也依賴:

- bandwidth choice
- sample size
- tail data 是否充足

所以 KDE 很適合 exploratory density estimation，但對極端尾部仍可能資料不足。

## Neural Networks for Risk Management

這門課還把一個更進階方向點出來: 用 neural network 直接學習 `prices -> portfolio weights` 的 mapping，讓 portfolio optimization 更即時。

這種方法的吸引力在於:

- 市場資料更新後可快速輸出新 weights
- 省去每次都做完整 optimization 的成本

但本質上，它沒有消除 risk management 問題，只是把 decision rule 用另一種函數近似方式表達。

## A Practical Risk Management Workflow

1. 先定義 portfolio 和主要 risk factors。
2. 計算 return、volatility、covariance，建立第一層風險視角。
3. 決定要用 historical、parametric 還是 Monte Carlo 的 loss distribution。
4. 計算 VaR / CVaR，必要時納入 EVT 或 KDE 等 tail-focused 方法。
5. 用 backtesting 檢查模型是否低估或高估 tail risk。
6. 若市場 regime 改變，重新評估 stationarity 與 structural breaks。
7. 把結果回連到 risk appetite、capital buffer 和 portfolio weights 調整。

## Common Mistakes

- 把 volatility 當成完整風險定義，忽略 tail losses。
- 直接套 Normal 分布，沒有檢查 fat tails 是否更合理。
- 沒有區分 risk factor levels 與 returns，就直接把資料餵進模型。
- 只檢查 raw returns 的自相關，卻忽略 absolute returns 的 clustering。
- 忘記 stationarity 只是工作假設，不是市場保證。
- 看見一個漂亮的 VaR 數字，就以為尾部風險已被理解。
- 沒有做 backtesting，就把模型拿去做真實部位控制。
- 用 `sqrt(T)` 放大 volatility 或 VaR，卻沒有檢查獨立同分布近似是否還站得住腳。

## Practical Reminders

- risk model 的價值，不在於看起來高級，而在於能不能在壞時候提供可靠訊號。
- 很多風險失敗不是因為完全沒模型，而是因為把模型假設當成現實本身。
- 若你只能多做一件事，通常是把 tail、breaks 與 backtesting 看得比平均值更重。
