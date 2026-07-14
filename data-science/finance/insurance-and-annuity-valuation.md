# Insurance and Annuity Valuation

insurance products 和一般債券或專案估值最大的不同，不在於折現本身，而在於現金流是否會發生，取決於人是否存活、何時死亡，以及契約是否含有保證期間或遞延條件。

Key point: 保險與年金估值可以先想成「狀態依賴的折現現金流」。折現率處理時間價值，survival / mortality probabilities 決定哪些 cash flows 真的有機會發生。

## Start With Cash-Flow Vectors

這類產品最適合用 cash-flow vector 來想。

- `c_k`: 第 `k` 期發生的現金流
- `v^k`: 第 `k` 期的 discount factor
- `p`: 存活機率
- `q`: 死亡機率

一般金融裡，我們常把現金流當成已知。保險精算裡，還要再問:

- 這筆錢是在活著時支付，還是死亡時支付？
- 是每期都保證支付，還是要滿足 survival condition？
- 契約是否有 deferment、guarantee period 或 term limit？

## Random Lifetime Changes The Valuation Problem

對年齡 `x` 的個體，未來壽命可以視為一個 random variable。這會讓 valuation 從單純的 PV 變成 expected present value, EPV。

直覺上:

- survival-contingent cash flow: 要乘上存活到該期的機率
- death-contingent cash flow: 要乘上該期死亡的機率

這也是為什麼保險估值不只需要利率，還需要 life table。

## Life Tables Turn Demography Into Model Inputs

life table 提供的不是單一死亡率，而是一整套年齡相關的 survival / mortality input，例如:

- `q_x`: 年齡 `x` 到 `x+1` 的死亡機率
- `p_x = 1 - q_x`: 一年存活機率
- `l_x`: 存活到年齡 `x` 的人數
- `e_x`: 年齡 `x` 的剩餘預期壽命

對估值最常用的是把它們轉成:

- `k p_x`: 從現在起存活 `k` 年的機率
- `k q_x`: 在延後 `k` 年後於下一期死亡的機率

一旦這兩組機率算出來，很多產品其實都能寫成向量乘法。

## EPV Is The Core Pricing Language

保險與年金產品最核心的式子都長得像:

- `EPV = sum(benefit_k * discount_k * probability_k)`

差別只在 `probability_k` 用的是哪一種機率:

- annuity: 常乘 `k p_x`
- life insurance: 常乘 `k q_x`
- guaranteed portion: 直接當成確定現金流，不乘 survival probability

這讓一個很複雜的契約，也能拆成幾段簡單 cash-flow blocks 來算。

## Life Annuities

life annuity 的付款通常發生在被保險人仍然活著時，因此估值重點是 survival-contingent cash flow。

典型特徵:

- 每期固定支付金額
- 只要 annuitant 存活就繼續付
- 可以從退休後某期開始支付

所以一個 life annuity 的價值，通常是:

- 每期 benefit
- 乘上對應 discount factor
- 再乘上該期存活機率

## Guaranteed Periods Create Two Layers Of Value

很多年金不是純 life-contingent，而是前幾年保證支付，之後才改成 survival-contingent。

這種設計最好拆成兩段:

- guaranteed annuity: 不論是否存活都支付
- nonguaranteed life annuity: 只有存活才支付

估值上最重要的觀念是:

- guaranteed 部分用普通 PV
- life-contingent 部分用 EPV
- 產品總價值是兩者相加

這種拆法很實用，因為它可以把保證期間、退休金保底、遺屬保護等條款都整理得很清楚。

## Premiums Are Priced By Actuarial Equivalence

premium calculation 的核心不是「公司想收多少」，而是先建立 actuarial equivalence:

- premiums 的 EPV
- 應該對上 benefits 的 EPV

如果 premium 本身也只有在存活時才繳，那 premium stream 也要被當成 life annuity 來折現。

這個想法很重要，因為它把 pricing 問題轉成:

- 已知 benefits，求 premium
- 或已知 premium pattern，求對應 benefits 是否可負擔

## Life Insurance Benefits Depend On Death Timing

life insurance 和 annuity 剛好相反。它最核心的是 death-contingent payoff。

估值時常要問:

- 如果在某段期間死亡，賠多少？
- 如果一直活著直到 term 結束，是否就不賠？
- 是否有 waiting period 或 deferment？

因此 death benefit 的 EPV，通常會把每期 benefit 向量乘上:

- discount factors
- deferred mortality probabilities `k q_x`

## Common Product Shapes

幾種最常見的型態包括:

- whole life insurance: 終身有效，只要未來某期死亡就給付
- term life insurance: 只在前 `n` 年內死亡才給付
- deferred whole life insurance: 前 `u` 年不給付，之後恢復終身保障

把這三種放在一起看，差異其實主要來自 benefit vector:

- whole life: 幾乎每個未來期別都有 benefit
- term life: 只有前段期間有 benefit
- deferred whole life: 前段為 0，之後才有 benefit

這就是為什麼保險產品設計很適合向量化思考。

## Combined Benefits Are Modular

更真實的保單常同時包含:

- 某段期間的死亡保障
- 某個年齡後開始的年金給付
- 前幾年保證支付

這時不要硬背封閉公式，通常更穩的方法是:

1. 先把產品拆成多個 benefit components。
2. 各自寫出 benefit vector。
3. 判斷每一段是要乘 survival probability、mortality probability，還是不用乘。
4. 分別計算 PV / EPV 後再加總。

這種 modular thinking 比死記公式更適合真實產品。

## Why This Matters Outside Actuarial Work

即使你不是做傳統保險，這個框架仍然很有價值，因為它其實是在教一種更一般化的建模方式:

- cash flow 不一定是 deterministic
- probability weights 不一定來自市場價格，也可能來自人口或事件機率
- valuation 可以拆成「金額 x 時點 x 狀態機率」

這個思路也會出現在:

- credit products 的 default-timing cash flow
- churn / retention 模型下的 customer lifetime value
- healthcare utilization 與 pension liability projection

## R Workflow Intuition

這份材料在 R 裡最常見的結構是:

- 從 `life_table` 抽出 `q_x`、`p_x`
- 用 `cumprod()` 生成 survival probabilities
- 建立 `discount_factors`
- 用 `rep()`、`c()` 等方式定義 benefit vector
- 用 `sum(benefits * discount_factors * probabilities)` 算 EPV

這裡真正重要的不是語法，而是你是否能把契約條件翻成正確的向量。

## Common Failure Modes

這個主題很常出錯在:

- 把 guaranteed cash flow 和 contingent cash flow 混在一起
- survival probability 與 deferred mortality probability 用錯
- discount period 對齊錯位一格
- benefit starts / ends 的時間點沒有對齊
- 只看 expected value，沒有意識到模型高度依賴 mortality table 與 interest-rate assumption

如果一個保險估值結果怪怪的，通常先回頭檢查的不是公式，而是 cash-flow timing 與 probability alignment。
