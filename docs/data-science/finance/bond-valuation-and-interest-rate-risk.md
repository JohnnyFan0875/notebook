# Bond Valuation and Interest Rate Risk

債券看起來常像「固定拿利息、到期拿回本金」的簡單工具，但一旦把價格、殖利率、duration 與 convexity 放在一起看，就會發現 fixed income 的核心其實是 discounting 和 interest-rate risk。

Key point: bond valuation 的本質，是把一串已知或可預期的 cash flows 用適當殖利率折現回今天，然後分析價格對利率變化有多敏感。

## Core Bond Characteristics

在開始估值前，先分清楚 bond contract 的幾個基本元素:

- issuer: 誰借錢
- principal / par / face value: 到期返還的本金
- coupon rate: 發行人承諾支付的利息率
- payment frequency: 年付、半年付、季付等
- maturity: 本金何時返還

這些條件會直接決定 cash flow pattern，也就直接決定估值方式。

## Keep the Scope of the Bond Clear

很多入門 bond model 會先假設:

- fixed coupon
- fixed maturity
- no embedded options

這個限制很重要，因為 callable、putable、convertible 或其他帶 option 的 bonds，會讓 cash flow amount 和 timing 都變得不再固定，分析也會明顯更複雜。

## Time Value of Money Is the Foundation

債券估值離不開 time value of money。無論是零息債還是附息債，本質上都只是未來 cash flows 的 present value。

從這個角度看:

- future value 是資金往未來累積後的價值
- present value 是把未來 cash flow 折回今天
- 利率或 yield 就是把時間與風險轉成 discount factor 的橋樑

這也是為什麼簡單利息、複利、compounding frequency 這些看似入門的概念，實際上都直接影響 bond pricing。

## Simple vs. Compound Interest

simple interest 只對原始本金計息；compound interest 則會讓利息本身繼續生利息。對債券和所有 fixed-income valuation 來說，複利觀念通常更重要，因為市場上的 discounting 大多隱含 compounding。

直覺上:

- compounding frequency 越高，在同樣名目年利率下，future value 越高
- 反過來看 present value，discounting 的效果也會受 compounding convention 影響

## Multiple Cash Flows Matter

投資實務裡，現金流通常不只一筆。這使得很多問題不再只是單一 `PV` 或 `FV`，而是:

- 一連串 cash flows 各自複利或折現
- 最後把所有未來值或 present values 加總

這也是為什麼金融函數像 `fv()`、`pv()`、`pmt()`、`nper()`、`rate()` 很有用。它們的價值不是取代理解，而是幫你把現金流時間結構寫得更乾淨。

## Present Value and Zero Coupon Bonds

zero coupon bond 最容易看出債券估值的本質，因為它只有一筆未來 cash flow:

- 到期時拿回 face value
- 中間沒有 coupon

因此它的價格就是那筆 face value 的 present value。這種 bond 也很適合拿來理解 yield 和 maturity 如何共同影響價格。

## Coupon Bonds as a Bundle of Discounted Cash Flows

coupon-paying bond 則可以理解成:

- 多筆中間 coupon cash flows
- 再加上一筆 maturity 時的 principal repayment

實務上，很有幫助的一個心智模型是把一張附息債拆成一組 zero coupon cash flows。這會讓 pricing logic 變得非常清楚:

- 每筆 coupon 都各自折現
- 到期本金也要折現
- 全部加總就是 bond price

## Yield to Maturity

yield to maturity 可以理解成: 如果你以當前價格買入並持有到到期，這張債券隱含的年化回報率大概是多少。

對 zero coupon bond 來說，yield 常可直接由 price 和 face value 反推。對 coupon bond 來說，yield 則通常需要數值法或 trial-and-error 求解，因為它同時出現在多期折現項裡。

## Yield Is More Than Just a Number

估值裡用到的 yield，不只是 market quote，而是多種風險補償的合成結果。很常見的拆法是:

- risk-free rate
- credit spread
- 其他可能的 risk premia

直覺上，risk-free rate 提供時間價值的基準，而 spread 則補償違約、流動性、call risk 或其他額外風險。

## Risk-Free Yield and Spread

如果想把 yield 背後的邏輯說清楚，可以先用這兩層去想:

- risk-free yield: 通常用相似 maturity 的 government bond 當 baseline
- spread: 反映相對於 baseline 額外要求的回報

因此兩張 maturity 類似但信用風險不同的 bonds，就算 coupon 一樣，折現率也不會一樣。

## Credit Ratings and Comparable Yields

實務估值中，若手上 bond 沒有足夠流動交易價格，常會參考:

- 同信用等級 bonds 的市場殖利率
- 相近 maturity 的 benchmark curve
- 同產業或同 issuer type 的 comparable bonds

這背後其實就是 fixed-income 版本的 comparable pricing，只是比較對象變成相似 credit profile 和 maturity bucket。

## Price and Yield Move Inversely

這是 fixed income 最重要的直覺之一:

- yield 上升，discount rate 上升，price 下跌
- yield 下降，discount rate 下降，price 上升

這個關係也帶出 premium、discount、par 的基本判讀:

- premium bond: price above par，通常代表 coupon 高於 yield
- discount bond: price below par，通常代表 coupon 低於 yield
- par bond: price around par，通常代表 coupon 約等於 yield

## Estimating Yield From Price

如果 bond 已知價格，但你想反推它的 YTM，本質上是在找那個能讓 discounted cash flows 恰好等於 market price 的折現率。

對 coupon bond 來說，這通常要靠:

- iterative guessing
- root finding
- 金融函數內建的 numerical solver

Key point: price 決定時，yield 往往不是代數解，而是數值解。

## The Price-Yield Curve Is Not Linear

bond price 和 yield 的關係不是一條直線，而是一條彎曲曲線。這件事很重要，因為它告訴我們:

- 同樣大小的利率變動，價格反應未必對稱
- 線性近似只在小幅利率變動時比較可靠

這也正是 duration 和 convexity 存在的原因。

## Duration as Interest Rate Sensitivity

duration 常被當成「殖利率變動 1% 時，債券價格大概變動多少百分比」的近似量。它是 interest-rate sensitivity 的一階近似。

duration 有兩種很有用的直覺:

- price sensitivity view: 利率變動時，價格會怎麼動
- weighted-average timing view: 你平均要多久才拿回投資

兩種理解方式都指向同一個核心: cash flows 越晚拿回、越依賴遠期折現，通常越怕利率變化。

## What Increases Duration

一般來說，下列條件會讓 duration 變高:

- 較長的 maturity
- 較低的 coupon
- 較低的 yield level

這些條件的共通點是: 讓更多價值集中在較遠的未來，因此對 discount rate 的改變更敏感。

## Dollar Duration and DV01

把 duration 從百分比敏感度轉成金額敏感度後，常用的量是:

- dollar duration
- DV01

它們都在回答一個更貼近風險管理的問題:

- 利率變動一點點，我的 portfolio 會賺或賠多少錢？

其中 DV01 特別常用，因為它把風險標準化成「殖利率變動 1 basis point 時的價格變動」。

## Duration-Based Hedging

當投資組合對利率很敏感時，可以用 DV01 去做 hedging。核心做法是:

1. 算出現有 portfolio 的 DV01
2. 算出 hedge instrument 的 DV01
3. 找到能互相抵消的部位數量

這樣做不能消除所有風險，但能先把一階的 interest-rate exposure 壓低。

## Duration Is Only a Linear Approximation

duration 很好用，但它是線性的。當 yield change 變大時，duration-only prediction 會開始偏離真實價格變化，因為真正的 price-yield relation 是 curved。

這就是 duration 的主要限制:

- 對小幅變動通常不錯
- 對大幅變動可能失真

## Convexity Measures Curvature

convexity 可以理解成 price-yield curve 的彎曲程度，也是一個二階效果。

它的實務價值在於:

- 改善 price-change approximation
- 更完整地衡量 interest-rate risk
- 解釋為什麼債券價格上漲與下跌的幅度常不對稱

正 convexity 常被視為一種好處，因為:

- yield 下降時，價格上升通常比線性預測更多
- yield 上升時，價格下跌通常比線性預測更少

## Small vs. Large Yield Changes

在小幅 yield moves 下，duration 的線性近似通常還算好用，而且上升與下降的效果看起來相對接近。

但當 yield move 變大時，bond price reaction 會開始明顯不對稱:

- yield 下降時，價格上漲幅度可能大於線性預期
- yield 上升時，價格下跌幅度通常小於同幅度下降時的漲幅

這種 asymmetry 正是 convexity 想捕捉的現象。

## What Increases Convexity

在一般直覺下，convexity 會隨這些條件增加:

- 較長 maturity
- 較低 coupon
- 較低 yield

這和 duration 的方向很像，但 convexity 更直接反映「曲率有多大」，而不只是 slope。

## Combining Duration and Convexity

做 bond price prediction 時，最常見的進階做法是:

- 先用 duration 提供一階 price change
- 再加上 convexity adjustment 補二階曲率效果

這樣通常會比單用 duration 更接近實際 repricing 結果，尤其在 yield move 比較大時更明顯。

## A Practical Fixed-Income Workflow

1. 先確認 bond 的 cash flow structure: zero coupon 還是 coupon-paying。
2. 用 yield 和 payment timing 折現得到價格。
3. 再從價格反推出 yield 或比較不同 bonds 的 YTM。
4. 用 duration 衡量一階利率敏感度。
5. 用 DV01 轉成 portfolio 可操作的金額風險。
6. 若需要更準確 price prediction，再加上 convexity。

## Common Mistakes

- 把 coupon rate 和 yield to maturity 混為一談
- 忘記 compounding frequency 和 payment frequency 要一致
- 沒有先確認 bond 是否帶 embedded options，就直接套 option-free pricing 直覺
- 估 yield 時忽略 risk-free baseline 和 spread 的區分
- 用 duration 預測大幅利率變動，卻沒有加 convexity adjustment
- 只看價格高低，不看 premium / discount 背後是 coupon 與 yield 的相對位置
- 做 hedging 時只看面額，不看 DV01

## Practical Reminders

- bond 不是「固定收益所以固定風險」，它對利率其實可能很敏感。
- 在 fixed income 裡，現金流時點本身就是風險來源的一部分。
- 如果你想知道 portfolio 對利率變動的真實暴露，DV01 往往比單純的 price 或 yield 更有操作意義。
