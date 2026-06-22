# Marketing Analytics

這個章節整理 marketing 與 customer decision 場景中常見的資料建模問題，例如價格變動、促銷曝光、品牌選擇、response probability 與 campaign effectiveness。

Key point: marketing analytics 不是把模型硬套到商業資料上，而是把「可操作的決策槓桿」和「可以量化的反應」連起來。常見槓桿包括 price、display、coupon、feature、channel 與 targeting rule。

## Topics

- [Market Response Models](market-response-models.md)
- [Choice Modeling](choice-modeling.md)
- [Campaign Measurement](campaign-measurement.md)

## Main Questions

| Topic | Focus | Main Question |
| --- | --- | --- |
| [Market Response Models](market-response-models.md) | sales response、log-linear demand、binary choice、marginal effects、carryover | 價格、促銷與展示活動改變時，銷量或購買機率會怎麼變？ |
| [Choice Modeling](choice-modeling.md) | multinomial logit、conjoint、market share prediction、preference heterogeneity | 當顧客面對多個選項時，哪些產品特徵會影響被選中的機率？ |
| [Campaign Measurement](campaign-measurement.md) | KPI design、funnel、channel attribution、integrated campaign workflow | 一個 campaign 到底有沒有對 business 產生影響，該怎麼分層衡量？ |

## Recommended Learning Path

1. 先看 [Market Response Models](market-response-models.md)，建立需求反應、價格效果與 binary response 的基本語言。
2. 再看 [Choice Modeling](choice-modeling.md)，理解多選項情境下的 utility、share 與 product design 問題。
3. 接著看 [Campaign Measurement](campaign-measurement.md)，把模型、channel、KPI 與 business impact 串成同一個 campaign workflow。
4. 再回頭搭配 [Regression Analysis](../statistics/regression-analysis/README.md) 與 [Classification Thresholds and Calibration](../machine-learning/evaluation/classification-thresholds-and-calibration.md)，把統計模型和實際決策門檻連起來。

## Reading Reminders

- marketing response 常常是 observational pattern，不要直接把模型係數當成 causal lift。
- 價格、促銷與展示效果通常會彼此交纏，單看一個係數很容易誤解真實商業效果。
