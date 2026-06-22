# Business Valuation

business valuation 嘗試回答的是: 這家公司的價值大概落在哪裡，以及這個判斷是由哪些假設撐起來的。它不是單一公式，而是一組把現金流、風險、可比公司與市場交易放在一起對照的框架。

Key point: valuation 既是 art 也是 science。公式提供結構，但最終結果仍高度依賴假設、比較對象與判斷邏輯。

## Why Perform Valuation

估值常出現在幾種情境:

- 投資人判斷一家公司是否值得買進或賣出
- 公司內部評估併購、出售、融資或策略選項
- 分析師比較市場價格與 intrinsic value 是否偏離
- 管理層評估資本配置與長期價值創造

估值不是只在 transaction 發生時才有用。很多時候，它也是一種把公司經濟邏輯講清楚的方式。

## Valuation Is an Art and a Science

science 的部分在於:

- 現金流、折現率、multiple 等都有可重複的結構
- 模型之間需要 numerator / denominator consistency
- EV、equity value、WACC、UFCF 等定義不能混用

art 的部分在於:

- 預測成長與 margin 本來就帶有主觀判斷
- comparable company 從來不會完全一樣
- terminal value、beta、risk premium 等假設很容易改變結果

所以一份 valuation 的重點，不只是最後那個數字，而是數字對假設有多敏感。

## Common Valuation Techniques

估值方法可以先分成兩大類:

- intrinsic valuation: 從公司自身未來現金流出發，典型做法是 DCF
- relative valuation: 拿公司和市場上的可比公司或可比交易做比較

實務上，兩類方法通常會一起使用，因為它們各自回答不同問題:

- DCF 比較像「如果這些假設成立，這家公司本質上值多少」
- multiples 比較像「市場現在願意給類似公司多少價格」

## Enterprise Value, Equity Value, and Consistency

估值裡最常見的錯誤之一，就是 enterprise value 與 equity value 沒有分清楚。

- enterprise value 對應整個營運資產
- equity value 對應最後屬於普通股股東的部分

這會直接影響 multiple 的選擇:

- EV multiple 要搭配對所有 capital providers 可用的 operating metric
- equity multiple 要搭配屬於股東的 metric

同一個原則也會延伸到 DCF:

- unlevered cash flow 應搭配 WACC
- levered or equity cash flow 應搭配 cost of equity

Key point: numerator 和 denominator 必須站在同一層級，不然估值看起來很精確，實際上卻在混算。

## DCF: A Structured Intrinsic Valuation

DCF 會把公司未來可創造的現金流折現回今天。

它通常有兩個主要部分:

1. explicit forecast period
2. terminal value

前半段描述接下來幾年的收入、成本、投資與現金流；後半段則處理 forecast horizon 之後的長期價值。很多模型裡，terminal value 會占很大比重，所以它不只是補充欄位，而是核心假設之一。

## Free Cash Flow and the Main DCF Logic

在企業估值裡，常見起點是 unlevered free cash flow，因為它代表在不考慮資本結構之前，營運資產能產生多少可分配現金。

直覺上可以把 UFCF 想成:

- 從營運獲利出發
- 扣掉稅
- 加回非現金費用
- 再扣掉 capital expenditure 與 working capital needs

這種做法的好處是:

- 可以先評估 business itself，而不是先被 financing choice 干擾
- 更自然地和 enterprise value / WACC 對齊

## Key DCF Assumptions

DCF 最大的力量，也是它最大的脆弱點，因為結果通常對幾個假設非常敏感:

- revenue growth
- operating margin
- reinvestment needs
- long-term growth rate
- discount rate

如果輸入假設過度樂觀，DCF 會給出非常漂亮、但沒有防禦力的結論。因此好的 valuation 不只是算 base case，也要意識到 sensitivity。

## WACC and the Spectrum of Risk

WACC 在 DCF 中常被拿來當折現率，因為它試圖反映整體資本提供者要求的報酬。

這背後其實是在做一件事: 把現金流放到適當的 risk bucket 裡。風險越高，投資人要求的回報越高，折現率也越高，估值自然越低。

cost of equity 的推估常會透過 CAPM、beta、equity risk premium 等觀念完成。即使模型形式很標準，輸入參數的選擇仍然需要大量 judgment。

## Terminal Value

terminal value 是把 explicit forecast period 之後的價值濃縮起來，常見做法至少有兩種思路:

- perpetual growth style
- exit multiple style

無論使用哪種方法，都要注意:

- long-term growth rate 不應脫離經濟現實
- exit multiple 不應與可比公司環境脫節
- terminal assumptions 要和前面的 forecast narrative 一致

如果前面幾年寫的是高成長轉成熟，但 terminal value 還隱含極高成長或過高 multiple，模型就會自相矛盾。

## From Enterprise Value to Value per Share

很多 DCF 一開始得到的是 enterprise value，而不是直接的每股價值。要走到 value per share，通常還要經過幾步:

1. 從 enterprise value 調整 net debt、cash 與其他 non-operating claims
2. 得到 equity value
3. 再除以 diluted shares outstanding

如果中間存在 preferred stock、minority interest、option dilution 或其他特殊項目，也要一併處理。

## DCF Advantages and Disadvantages

DCF 的優點:

- 迫使你把公司價值拆回現金流驅動因子
- 不會完全依賴當下市場情緒
- 對長期價值創造邏輯較有解釋力

DCF 的限制:

- 對假設高度敏感
- terminal value 常佔估值大部分
- 小幅調整 WACC 或 growth rate 就可能改變結論

所以 DCF 比較適合被當成 structured reasoning tool，而不是自動產生真值的機器。

## Relative Valuation

relative valuation 問的是: 市場目前怎麼給相似公司定價？

常見做法是選一組 comparable companies，觀察它們的 trading multiples，再把這些倍數套到目標公司。這種方法的強項在於:

- 容易和市場語言接軌
- 能快速反映當前市場條件
- 對 transaction、pitch、sanity check 很實用

但它的限制也很直接:

- 如果整個市場都被高估或低估，結果會一起偏掉
- 真正相似的 comps 很難找
- growth、margin、risk、capital intensity 不同時，倍數不可直接照搬

## Choosing the Appropriate Multiple

multiple 不應只因為常見就直接套用，而要看公司生命週期與可用財務指標。

思考原則通常包括:

- 公司是否獲利
- 現金流是否穩定
- 所處產業更重 growth 還是 earnings
- 指標屬於 enterprise 層級還是 equity 層級

這也是為什麼不同產業會偏好不同倍數，而且同一家公司在不同發展階段也可能適合不同比較方式。

## Selecting Comps

good comps 通常至少在幾個面向相近:

- business model
- end market
- growth profile
- margin structure
- geography
- size and capital intensity

bad comps 的問題通常不是「完全無法比較」，而是差異被忽略。只要比較對象在風險、成長、會計處理或資本結構上差太多，最後得到的倍數就容易失真。

## Comparable Companies and Precedent Transactions

兩者都屬於 relative valuation，但訊號來源不同。

- comparable companies: 看公開市場目前如何給相似公司定價
- precedent transactions: 看歷史交易中，買方曾為類似資產付出多少價格

precedent transactions 常可能隱含 control premium、synergy expectation 或景氣週期影響，因此通常會和 trading comps 有系統性差異。

## Football Field Chart

football field chart 不是一種新的估值方法，而是把不同方法得出的 valuation range 放在同一張圖上比較。

它的價值在於:

- 呈現 range，而不是假裝只有單一正確數字
- 讓 DCF、trading comps、precedent transactions 的差異並排可見
- 幫助討論市場價格落在整體估值區間的哪個位置

這種呈現方式也提醒一件事: valuation 更像是 plausible range management，而不是單點預言。

## A Practical Valuation Workflow

1. 先釐清你要估的是 enterprise value 還是 equity value。
2. 選擇和定義一致的 cash flow、multiple 與 discount rate。
3. 建立 DCF，明確分開 explicit forecast period 與 terminal value。
4. 用 trading comps 與 precedent transactions 做 cross-check。
5. 把結果整理成 valuation range，而不是只報一個孤立數字。

## Practical Reminders

- valuation consistency 比 model sophistication 更重要，因為層級一旦混掉，後面全部都會偏。
- 不要把 spreadsheet 的小數點精度誤認成真實世界的精度。
- 若不同方法給出的範圍差很多，先回頭檢查 assumptions 和 comps，而不是急著挑自己喜歡的答案。
