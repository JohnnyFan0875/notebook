# Capital Budgeting

Capital budgeting 處理的是「要不要把資本投入某個專案」。核心不是把公式算對而已，而是把未來現金流、時間價值、風險與資本限制放到同一個決策框架裡。

Key point: 任何專案評估方法，本質上都在比較「今天付出的資金」和「未來拿回來的現金流」是否值得。

## Why Present Value Comes First

未來的一塊錢不等於今天的一塊錢，因為資金有機會成本，也有風險與通膨的不確定性。因此 corporate finance 會先把未來現金流折回今天，再做比較。

直覺上可以這樣理解:

- cash flow 越晚收到，今天的價值通常越低
- discount rate 越高，未來現金流被打折得越多
- 同樣總額的現金流，回收越早通常越有價值

## Common Decision Metrics

### Payback Period

payback 看的是多久能回本。

它的優點是直觀，特別適合快速比較流動性壓力或回收速度。它的限制也很明顯:

- 忽略回本之後的現金流
- 通常沒有完整反映 money time value
- 容易偏好短期專案，低估長期但高價值的投資

所以 payback 比較像第一輪篩選工具，不應單獨作為最終決策標準。

### Net Present Value

NPV 是把所有未來現金流折現後，加總再扣掉初始投入。

- `NPV > 0`: 專案在假設的折現率下能創造價值
- `NPV = 0`: 大致只是打平資本成本
- `NPV < 0`: 專案沒有覆蓋資本成本

如果目標是最大化公司價值，NPV 通常是最核心的 decision metric，因為它直接對應價值增加多少，而不只是報酬率看起來高不高。

### Internal Rate of Return

IRR 是讓 NPV 恰好等於零的折現率，也可以理解成這個專案隱含的報酬率。

它的優點是容易和 hurdle rate 或 WACC 比較:

- `IRR > required return`: 專案通常可接受
- `IRR < required return`: 專案通常應拒絕

但 IRR 也有幾個常見陷阱:

- 非正常現金流可能出現多個 IRR
- 互斥專案之間，IRR 高不一定代表創造價值最多
- 專案規模不同時，單看報酬率容易誤判

實務上，IRR 適合做輔助比較，但當 IRR 和 NPV 結論衝突時，通常優先回到 NPV。

### XNPV and XIRR

一般的 NPV / IRR 假設現金流間隔規則，但很多真實專案的現金流日期並不整齊。這時候要改用 XNPV / XIRR，把實際日期也納入折現。

這在下列情境尤其重要:

- 資本支出不是固定每年發生
- 現金流回收時間不規則
- 需要和 spreadsheet 或實務財務模型對齊

## Profitability Index and Capital Rationing

當資本有限、不是每個正 NPV 專案都能做時，只看絕對 NPV 可能不夠。這時 profitability index 可以幫助比較「每一單位投入資本，能帶來多少現值」。

它比較像在回答:

- 哪些專案單位資本效率更高
- 當預算受限時，應該優先排哪些專案

不過要注意，profitability index 適合在資本 rationing 下做排序，不代表可以完全取代 NPV。

## Common Allocation Metrics

當公司同時面對多個候選專案時，常見做法不是只算一個指標，而是把幾個維度一起看:

- value creation: NPV 是否真的增加公司價值
- return efficiency: IRR 或 profitability index 是否達到門檻
- liquidity pressure: payback 是否太慢
- capital usage: 專案是否吃掉過多稀缺資本

這也是為什麼資本預算常常不是單一公式決策，而是 ranking problem。

## A Good Project Evaluation Workflow

1. 先整理專案的初始投入、後續現金流與時間點。
2. 根據風險與資本成本選折現率。
3. 先算 NPV，確認是否創造價值。
4. 再看 IRR、payback、profitability index，補充報酬率、回收速度與排序資訊。
5. 如果專案彼此互斥或資本受限，回到 portfolio 層級重新排序。

## Common Mistakes

- 把高 IRR 當成一定比高 NPV 更好。
- 用不規則現金流，卻還是套普通 NPV / IRR。
- 折現率沿用固定數字，沒有反映風險與資金來源。
- 只看會不會回本，沒有看回本之後總共創造多少價值。

## Practical Reminders

- NPV 比較接近「價值增加多少」，IRR 比較接近「報酬率看起來如何」。
- 若專案規模不同、期間不同或現金流不規則，越要小心單一指標誤導。
- spreadsheet 很容易把公式算出來，但真正困難的通常是現金流假設和 discount rate 是否合理。
