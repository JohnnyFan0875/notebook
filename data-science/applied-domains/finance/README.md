[Data Science](../../README.md) › [應用領域](../README.md) › Finance

# Finance

用金融資料作為統計、時間序列與分類模型的應用場景。金融資料高度噪音、非平穩，不同頻率下的結論可能完全不同。

| 筆記 | 內容 | 可遷移的方法 |
| --- | --- | --- |
| [Financial Concepts](financial-concepts.md) | 貨幣時間價值、折現、債券、duration / convexity、金融資料清理 | 現金流折現、敏感度分析 |
| [Portfolio and Risk](portfolio-and-risk.md) | 報酬與波動、分散、Sharpe、factor model、efficient frontier、VaR / CVaR、EVT、股價模擬 | 共變異矩陣、蒙地卡羅模擬、厚尾分布 |
| [Trading Strategies and Backtesting](trading-strategies-and-backtesting.md) | 指標、訊號、benchmark、drawdown | 回測紀律、過擬合 |
| [Credit Risk Modeling](credit-risk-modeling.md) | PD、logistic / XGBoost、校準、核貸門檻 | 分類模型評估、閾值與成本 |
| [Insurance and Annuity Valuation](insurance-and-annuity-valuation.md) | life table、EPV、年金、壽險 | 存活分析 |

金融報酬率的自相關（動能、均值回歸、波動聚集）見 [時間序列：自相關](../../statistics/time-series-analysis/autocorrelation.md#金融情境動能與均值回歸)。

## 閱讀提醒

- 價格序列與報酬率序列的性質不同，不要混著判讀。
- 統計顯著不一定代表可交易，也要考慮交易成本與穩定性。
- 研究交易規則時，先和最簡單的 buy-and-hold benchmark 比。
- 現金流受存活、死亡或違約影響時，把 timing 與 state probability 分開建模。
