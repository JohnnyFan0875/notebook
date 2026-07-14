# Equity Valuation Models

當估值問題明確站在普通股股東角度時，模型重心就不再只是整個 enterprise 值多少，而是股東能拿到的 cash flow、應該要求多少報酬，以及最後換算出來的每股價值是否合理。

Key point: equity valuation 的核心是保持股東視角的一致性。cash flow 要屬於 equity，discount rate 也要是 cost of equity。

## Time Value of Money Still Comes First

股東今天手上的一塊錢，和未來某一年才可能收到的一塊錢，不是同一件事。原因不只是時間，而是還包含:

- 風險
- 不確定性
- 機會成本

因此 equity valuation 雖然常看起來像估值分支，但它的地基仍然是 time value of money。

## FCFE vs. FCFF

這是 equity valuation 裡很重要的分界線。

- FCFE: 屬於股東可支配的 free cash flow
- FCFF: 屬於整個 firm、尚未區分 debt 與 equity claim 的 free cash flow

直覺上:

- FCFE 更適合直接估 equity value
- FCFF 更適合先估 enterprise value，再扣回到 equity

兩種方法都可以合理，但不能把 FCFE 配 WACC，或把 FCFF 直接拿去配 cost of equity。層級一旦混掉，結果就會系統性偏誤。

## Building FCFE

FCFE 可以理解成在公司已經支付營運成本、稅、資本支出、營運資金需求，並納入 net borrowing 影響之後，剩下真正屬於股東的現金流。

常見直覺路徑是:

- 從 after-tax income 或 net income 出發
- 加回非現金項目
- 扣掉 capital expenditure
- 扣掉 additional working capital needs
- 再調整 net borrowing

這個做法強迫你直接回答一個問題: 在不影響公司既定營運與成長的前提下，股東究竟能拿走多少現金？

## The FCFE Model

FCFE valuation 的基本邏輯很簡單:

1. 預測明確 forecast period 的 FCFE
2. 折現這些 FCFE
3. 估 terminal value
4. 再把 terminal value 折現回今天

最後兩部分相加，就是 equity value。若要換成每股價值，再除以 shares outstanding。

## Terminal Value Under an Equity Framework

在 FCFE 模型裡，terminal value 常用 perpetuity with growth 的方式估計。這時要特別注意兩個條件:

- `cost of equity > growth rate`
- growth assumption 必須和公司長期可持續成長能力一致

這裡最常見的錯，不是公式算錯，而是用了一個在經濟上不可能長期維持的 growth rate。

## Checking the Perpetuity Growth Rate

一個很實用的 sanity check 是把 perpetuity growth rate 拆回基本面:

- growth 必須由 reinvestment 支撐
- growth 也要受到 long-run ROE 的約束

直覺上，長期可持續成長通常可以用 `reinvestment rate × ROE` 去理解。若模型假設的 terminal growth 高於這個能力邊界，或甚至高於總體經濟長期成長，估值就很可能過度樂觀。

## Dividend Discount Model

當股東真正拿到的現金主要來自 dividends，而 dividend policy 具有可預測性時，DDM 會是非常自然的 equity valuation 工具。

它的核心邏輯是:

- 股票價值等於未來 dividend stream 的 present value

常見形式包括:

- constant dividend stream
- constant-growth dividend model
- two-stage DDM

DDM 特別適合:

- 成熟企業
- 穩定配息公司
- 金融或公用事業等現金回饋政策相對明確的情境

但如果公司目前不配息，或 dividend policy 和經濟實質嚴重脫節，DDM 的解釋力就會下降。

## Two-Stage Thinking Matters

很多高成長公司在第一階段不配息，並不代表 DDM 完全不能用。更好的做法通常是把公司拆成:

1. 高成長但不回饋現金的前期
2. 成熟後開始穩定配息的後期

這種 two-stage thinking 的價值，不只是套公式，而是把公司生命周期放回估值邏輯裡。

## Cost of Equity and CAPM

equity valuation 的折現率通常不是 WACC，而是 cost of equity。CAPM 是最常見的起點:

- risk-free rate
- beta
- equity risk premium

它的目的，是把股東承擔的 systematic risk 轉成所要求的回報率。

即使你知道 CAPM 很簡化，它仍然提供了一個重要框架: 股東要求的回報應和承擔的 market risk 對應，而不是任意指定一個漂亮數字。

## Beta, Diversification, and Systematic Risk

beta 想回答的是: 這支股票對市場波動有多敏感。

它強調的是 systematic risk，而不是 company-specific noise。因為在分散投資的世界裡，投資人理論上不應因可分散風險而被補償。

這也是為什麼 beta 常會透過 stock return 對 market return 的 regression 估出來。

## Unlevering and Relevering Beta

在實務估值裡，單一公司的 observed beta 往往受當下資本結構影響。為了把 peer comparison 做得更乾淨，常會先:

1. unlever beta，移除 leverage effect
2. 再用目標資本結構 relever beta

這樣做的目的，是把 business risk 和 financing effect 分開。當 peer firms 槓桿程度差很多時，這一步尤其重要。

## Risk-Free Rate and Equity Risk Premium

CAPM 的另外兩個敏感輸入是:

- risk-free rate
- equity risk premium

這裡最重要的原則不是背哪個固定數字，而是 consistency:

- 若 risk-free rate 用長天期 Treasury proxy，ERP 的定義也要跟同一套 horizon 對齊
- 若 valuation 是長期視角，折現率輸入也不應只反映短期市場噪音

很多估值分歧，最後其實都來自這些 seemingly small input choices。

## Checking Projections Before Valuing

equity valuation 很容易出現一種錯覺: 只要折現公式正確，結果就可信。其實真正脆弱的地方常在 projections。

至少要做幾種檢查:

- visual inspection: 歷史與 forecast 連起來看是否出現不合理跳點
- trend analysis: 看成長、margin、working capital assumptions 是否突然失真
- internal consistency: revenue growth、reinvestment、ROE、terminal growth 是否互相支持

Garbage in, garbage out 在估值裡特別真。

## Relative Valuation From an Equity Lens

若站在 equity angle，常見的 multiples 是:

- P/E
- P/B

它們的好處是直觀，也更直接對應普通股股東關心的每股價格。但要注意:

- EPS 為負時，P/E 很容易失去意義
- book value 為負或失真時，P/B 也可能不可靠

## Regression-Based Multiples

如果 peer companies 並沒有「看起來一樣」，單純拿平均或中位數 multiple 可能太粗。這時可以用 regression-based approach，把估值 multiple 和其驅動因子連回去，例如:

- P/B vs. ROE
- P/E vs. growth

這種做法的價值在於:

- 比單純平均 multiple 更少主觀挑選空間
- 讓 risk、growth、profitability 的差異更明確地反映進估值

## From Equity Value to Implied Price

不論是 FCFE、DDM 還是 equity multiple，最後通常都會收斂到一個問題:

- 對應到每股，implied price 是多少？

這一步看起來簡單，但仍要小心:

- 使用的是哪一版 shares outstanding
- 是否考慮 dilution
- BVPS、EPS、dividend 等 metric 是否與 price 層級一致

## Practical Reminders

- 如果模型一開始就是 equity valuation，就從頭到尾都站在股東視角，不要半路切回 firm view。
- terminal growth 不只是數學輸入，它必須由 reinvestment capacity 和 ROE 支撐。
- observed beta、ERP、risk-free rate 都不是神聖常數；它們只是有理有據的估計值，應該被檢查而不是被神化。
