# Fundamental Financial Concepts

很多 finance 問題表面上長得不一樣，但骨架常常是同一套: 一筆錢跨時間怎麼比較？報酬率怎麼累積？未來現金流今天值多少？一個決策到底是創造價值，還是只是把時間往後拖？

Key point: 金融概念的共同底層，其實是 time、cash flow、rate 這三件事如何一起作用。

## Return on Investment

最基本的投資報酬概念，是看一筆資產從初始價值走到最終價值後，成長了多少。

- initial value: 進場時投入多少
- final value: 期末拿回多少
- return: 兩者之間的相對變化

這種 ROI 觀念很直觀，但它只是一個起點，因為單看總報酬還沒有回答:

- 花了多久才得到這個報酬
- 中間有沒有現金流
- 報酬是一次跳出來，還是逐期複利累積

## Time Value of Money

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

## Compounding

compounding 的關鍵不是「利息會變多」而已，而是:

- 利息本身也會再產生利息

這讓成長過程從線性變成乘法累積。也因此:

- 持有期越長，複利效果越明顯
- compounding frequency 越高，累積結果通常越大

這也是為什麼看起來很小的 rate difference，拉長時間後可能會造成很大的 wealth gap。

## Annual Rate vs. Periodic Rate

很多金融產品不直接用同一個計息頻率。你常常需要在 annual rate 和 monthly / quarterly / daily rate 之間換算。

這裡最重要的不是背公式，而是記住:

- 名目年利率不一定等於逐期真正發生的成長率
- 不同 payment frequency 下，等價的 periodic rate 會不同

如果沒有先把 rate frequency 對齊，後面的 mortgage payment、discount factor 或 cumulative growth 幾乎都會算錯。

## Present Value and Future Value

present value 問的是:

- 未來某筆金額，放到今天值多少？

future value 問的是:

- 今天某筆金額，以某個 rate 成長到未來會變多少？

這兩者其實是一體兩面:

- 往未來推，是 compounding
- 往今天折，是 discounting

理解這個對偶關係之後，很多看似不同的 finance 問題都會變得很像。

## Discounting Cash Flows

只要現金流發生在不同時間點，就不能直接把名目金額相加。你必須先處理時間尺度。

discounting 的目的，是把:

- 早拿到的錢
- 晚拿到的錢

放回同一個今天的尺度上比較。

這也是為什麼 NPV、bond valuation、capital budgeting、retirement projection，本質上都在做同一件事，只是 cash flow pattern 不同。

## Project Evaluation Basics

在專案評估裡，最常見的幾個指標是:

- NPV
- IRR
- EAA

這門基礎課的價值，不在於重新推一遍公式，而是提醒幾個判讀原則:

- NPV 比較接近「增加多少價值」
- IRR 比較接近「隱含報酬率是多少」
- EAA 適合拿來比較壽命不同的專案

如果你要更完整的專案評估框架，可以再接著看 [capital-budgeting.md](corporate-finance/capital-budgeting.md)。

## Cost of Capital

折現率不是憑感覺填一個數字。很多 corporate finance 問題會用 cost of capital 當成 required return 的起點。

直覺上它回答的是:

- 這家公司動用一塊資金，投資人最低期待它回收多少報酬？

當資金來源同時包含 debt 和 equity 時，常見合成方式就是 WACC。它不是神奇參數，而是把:

- debt financing cost
- equity financing cost
- capital structure weights

合在一起，作為整體資本成本的近似。

## Debt, Equity, and Claims

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

## Mortgage as a Cash Flow Structure

mortgage 是 time value of money 很好的實物例子，因為它把幾個抽象概念都具體化了:

- down payment
- loan principal
- periodic interest rate
- fixed periodic payment
- amortization through time

同一筆 monthly payment，早期通常更多是在付 interest，後期才越來越多是在還 principal。這也說明了:

- 現金流結構和餘額演變，是兩件要一起看的事

## Home Equity and Underwater Mortgage

如果把 mortgage 放到資產負債觀點來看，還要再區分:

- house value
- outstanding loan balance
- home equity

當房屋價值低於剩餘貸款時，就會出現 underwater mortgage。這提醒我們:

- 資產價格路徑
- 負債攤還速度

是兩條不同動態，不能只看其中一邊。

## Wealth Accumulation

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

## Forecasting With Growth Rates

當你已經有 growth assumptions 時，常見做法是沿著時間把:

- cumulative growth path
- projected value path

一路滾出來。

這種 forecast 最容易犯的錯，是把 rate 當成會直接相加的東西。只要 growth 是跨期持續累積，通常就該用 multiplicative thinking，而不是單純線性外推。

## Rational Economic Decisions

finance 的很多「理性決策」其實不是要你追求最高名目金額，而是要求你把以下幾件事一起納入:

- time horizon
- risk
- financing cost
- scale
- cash flow timing

這也是為什麼看起來很賺的提案，折現之後可能沒有那麼有吸引力；而看起來普通的穩定現金流，放到長期 wealth accumulation 裡卻可能很有價值。

## A Practical Mental Model

1. 先辨認問題裡的 cash flows 發生在什麼時間點。
2. 再確認使用的是 annual rate 還是 periodic rate。
3. 決定你要把資金往未來投影，還是往今天折現。
4. 如果有 debt / equity 結構，再把資本成本納入。
5. 最後才比較不同方案的 value、return 或 affordability。

## Common Mistakes

- 把總報酬直接拿來比較不同持有期間。
- 沒有對齊 compounding frequency 就直接套用 rate。
- 把 nominal cash flows 直接相加，沒有先折現。
- 只看 mortgage payment 金額，沒有看 principal 和 interest 的分解。
- 用單一高報酬數字說服自己，卻沒有把風險與資本成本一起放進來。

## Practical Reminders

- 如果你搞清楚 time、cash flow、rate，很多 finance 題目會突然變得很像。
- 折現不是數學花招，而是把不同時間點的金額拉回同一尺度。
- 對長期決策來說，compounding 和 inflation 通常都不能忽略。
