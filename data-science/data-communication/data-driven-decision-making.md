# Data-Driven Decision Making

data-driven decision making 的重點不是「凡事都用數據決定」，而是知道什麼問題需要 exploratory analysis，什麼問題需要 explanatory reasoning，什麼問題適合 predictive automation，並在採取行動前把風險、stakeholders 與限制一起納入。

Key point: 分析不是終點。真正的目標是讓 evidence 改善決策品質，同時避免把看起來客觀的模型結果直接變成不受檢查的自動化判斷。

## Not Every Analysis Serves The Same Decision

同樣是資料分析，目的其實可以差很多。

一個很實用的區分方式是：

| Type | Typical Perspective | Main Purpose |
| --- | --- | --- |
| Exploratory | strategic | confirm understanding and build expertise |
| Explanatory | strategic / tactical | understand relationships well enough to improve operations |
| Predictive | tactical | drive specific outcomes and sometimes automate decisions |

這個區分很重要，因為：

- exploratory work 不需要假裝自己已經可以自動決策
- explanatory work 不等於最強預測器
- predictive work 常常需要犧牲部分可解釋性來換操作性

## Exploratory, Explanatory, And Predictive Are Different Jobs

### Exploratory

探索式分析通常在問：

- 資料裡有什麼 pattern？
- 哪些現象值得進一步追？
- 我們對這個 domain 的理解是否完整？

它特別適合：

- 新領域
- 問題定義還很模糊
- 需要先建立共同語言的團隊

### Explanatory

解釋型分析通常在問：

- 哪些因素和結果有穩定關聯？
- 這些變數之間如何互相作用？
- 哪些機制值得放進營運流程或政策設計？

它特別適合：

- 需要說服 stakeholders
- 需要建立 operating logic
- 需要知道「為什麼」而不只是「會發生什麼」

### Predictive

預測型分析通常在問：

- 下一筆記錄最可能發生什麼？
- 哪些個體風險最高？
- 哪些 cases 應優先被處理？

它特別適合：

- 需要排序、分流、預警
- decision latency 很短
- 結果會直接進入 operational workflow

Warning: 如果團隊其實需要 explanation，卻只給一個 prediction score，常會讓人無法採取正確行動；反過來，如果團隊需要即時分流，只給一篇長篇解釋報告也不夠。

## Ask What The Decision Is Before Asking For The Model

在 data-driven decision making 裡，先問這些通常比先選模型更重要：

- 我們到底要做哪個決定？
- 這個決定是 strategic 還是 tactical？
- 這個結果是給人參考，還是要直接自動化？
- 如果模型錯了，代價在哪裡？

Tip: 一個 analysis 是否成功，不只看它準不準，也要看它是否剛好支援了正確層級的決策。

## Probe An Analysis From Three Angles

一個簡單但實用的 probing framework 可以從三個角度檢查分析：

### Data

- data 是怎麼收集的？
- 什麼時候收集的？
- data 是否可得、完整、及時？
- label 或 outcome 是否可靠？

### Decision Fit

- 這個分析真的對應到要解的問題嗎？
- 是 cost vs. benefit、risk vs. reward，還是 supply vs. demand 類型的決策？
- 結果會不會被誤用到超出它能回答的範圍？

### Impact

- 誰會受到這個分析結果影響？
- 有沒有法規或治理限制？
- 這件事可能怎麼出錯？
- 有沒有對 stakeholders 的意外副作用？

Key point: 這些問題不是 ethical appendix，而是 decision quality 的一部分。

## Prediction Can Automate Decisions, So The Standard Must Be Higher

predictive systems 常常最容易被接進 workflow，自動決定：

- 誰優先被審核
- 誰收到優惠
- 哪個 case 被標成高風險
- 哪個 lead 被交給 sales

也因為如此，predictive analysis 的要求通常更高：

- 要看 calibration 與 threshold
- 要看錯誤成本
- 要看 drift 與 feedback loop
- 要看是否該保留 human review

Warning: 一個看似準確的 predictive model，如果沒有考慮 false positives / false negatives 的不對稱成本，仍然可能讓決策變差。

## Maturity Often Progresses From Description To Prescription

很多組織的 data culture 不是一步到位，而是逐漸成熟：

1. descriptive: 先知道發生了什麼
2. diagnostic / explanatory: 再知道為什麼會這樣
3. predictive: 開始估計接下來可能發生什麼
4. prescriptive / automated: 最後才把模型接到具體決策

這個順序有用，因為：

- 沒有 descriptive baseline，prediction 很難被信任
- 沒有 explanatory understanding，prescription 很容易被誤用
- 沒有 governance，automation 很容易製造新風險

## A Practical Framework For Decision Types

很多 business decision 可以粗分成幾種常見張力：

- **cost vs. benefit**
- **risk vs. reward**
- **supply vs. demand**

而不同分析型態在這些決策裡扮演的角色不同：

- exploratory 幫你看清張力存在在哪裡
- explanatory 幫你理解哪些因素在推動這個張力
- predictive 幫你在當下對個別 cases 做更快判斷

這也是為什麼「哪種分析最好」通常是錯誤問題。更好的問題是：

- 現在這個決策需要哪一種 evidence？

## A Practical Workflow

1. 先明確寫出待決策問題，而不是只寫分析題目。
2. 判斷這個需求偏 exploratory、explanatory 還是 predictive。
3. 檢查 data 可得性、收集方式與時效性。
4. 明確列出受影響 stakeholders 與錯誤成本。
5. 決定結果是 human-in-the-loop 還是 automation。
6. 在交付分析時，同時交付適用範圍、風險與失效條件。

## Common Mistakes

- 還在探索問題時，就急著要求 predictive model。
- 需要 explanation 的場合，卻只提供 black-box score。
- 把 tactical prediction 當成 strategic truth。
- 忽略 stakeholders、法規或 unintended consequences。
- 沒有定義錯誤成本，就把模型直接接進流程。

## Related Topics

- [Forming Analytical Questions](./forming-analytical-questions.md)
- [Communicating Data Insights](./communicating-data-insights.md)
- [A/B Testing](../statistics/experimental-design/ab-testing.md)
- [Machine Learning](../machine-learning/README.md)
