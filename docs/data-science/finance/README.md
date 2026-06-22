# Finance

這個章節用金融資料作為統計與時間序列概念的應用場景。閱讀時請特別注意：金融資料往往高度噪音、非平穩，而且不同頻率下的結論可能完全不同。

## Topics

- [Autocorrelation](autocorrelation.md)
- [Bond Valuation and Interest Rate Risk](bond-valuation-and-interest-rate-risk.md)
- [Credit Risk Modeling](credit-risk-modeling.md)
- [Financial Data Ingestion and Cleaning](financial-data-ingestion-and-cleaning.md)
- [Fundamental Financial Concepts](fundamental-financial-concepts.md)
- [Insurance and Annuity Valuation](insurance-and-annuity-valuation.md)
- [Trading Strategies and Backtesting](trading-strategies-and-backtesting.md)
- [Stock Price Simulation and Volatility](stock-price-simulation-and-volatility.md)
- [Corporate Finance](corporate-finance/README.md)

## Submodules

| Module | Focus | Main Questions |
| --- | --- | --- |
| [Bond Valuation and Interest Rate Risk](bond-valuation-and-interest-rate-risk.md) | present value、zero coupon、coupon bonds、yield、duration、DV01、convexity | 債券價格怎麼來？利率變動時，債券和 fixed-income portfolio 會怎麼動？ |
| [Credit Risk Modeling](credit-risk-modeling.md) | PD、default labeling、logistic regression、XGBoost、calibration、acceptance threshold | 我們該放款給誰？模型機率如何轉成核貸、拒貸與預期損失控制？ |
| [Financial Data Ingestion and Cleaning](financial-data-ingestion-and-cleaning.md) | CSV cleaning、dtype、datetime index、market data sources、descriptive checks、grouped summaries | 金融資料要從哪裡來？匯入後先檢查什麼？怎麼避免把髒資料直接帶進報酬或風險模型？ |
| [Fundamental Financial Concepts](fundamental-financial-concepts.md) | time value of money、compounding、discounting、ROI、mortgage cash flow、WACC intuition、wealth accumulation | 一筆錢跨時間怎麼比較？利率、折現與現金流之間的基本邏輯是什麼？ |
| [Insurance and Annuity Valuation](insurance-and-annuity-valuation.md) | life table、survival probability、mortality probability、EPV、annuity、term insurance、premium equivalence | 當現金流是否發生取決於生存或死亡時，該怎麼把折現與機率結合起來做產品估值？ |
| [Trading Strategies and Backtesting](trading-strategies-and-backtesting.md) | trading vs. investing、technical indicators、signals、benchmarking、strategy optimization、drawdown review | 一個交易規則要怎麼從技術指標走到可評估的歷史回測？回測結果又該怎麼避免只看報酬？ |
| [Stock Price Simulation and Volatility](stock-price-simulation-and-volatility.md) | volatility、log returns、lognormal prices、simple simulation、probability ranges | 股票價格的不確定性要怎麼建模？為什麼要看區間和分布，而不是單一路徑？ |
| [Corporate Finance](corporate-finance/README.md) | capital budgeting、funding、capital structure、dividends、buybacks | 公司該不該投資？資金該由誰提供？多餘現金應不應該還給股東？ |

## 閱讀提醒

- 價格序列與報酬率序列的性質不同，不要混著判讀。
- 在金融情境中，統計顯著不一定代表可交易，也要考慮交易成本與穩定性。
- 如果在研究交易規則，請先和最簡單的 buy-and-hold benchmark 比，再談策略是否有價值。
- 如果現金流會受到存活、死亡或違約狀態影響，請把 timing 與 state probability 分開建模。

## 建議閱讀順序

1. 先看 [Corporate Finance](corporate-finance/README.md)，建立公司層級的資本配置視角。
2. 再看 [Fundamental Financial Concepts](fundamental-financial-concepts.md)，先把 time value of money、compounding 與現金流折現的語言打穩。
3. 再看 [Financial Data Ingestion and Cleaning](financial-data-ingestion-and-cleaning.md)，先把市場資料的來源、欄位型別與清理流程釐清。
4. 再看 [Credit Risk Modeling](credit-risk-modeling.md)，理解機率模型如何接到核貸 threshold、錯誤成本與 portfolio 風險。
5. 再看 [Autocorrelation](autocorrelation.md)，理解金融時間序列和市場資料的統計特性。
6. 再看 [Bond Valuation and Interest Rate Risk](bond-valuation-and-interest-rate-risk.md)，建立 fixed-income 的 discounting 與利率風險直覺。
7. 再看 [Insurance and Annuity Valuation](insurance-and-annuity-valuation.md)，把折現現金流的想法延伸到 survival- and death-contingent products。
8. 接著看 [Stock Price Simulation and Volatility](stock-price-simulation-and-volatility.md)，把 volatility、price path 與機率區間連回實際建模。
9. 再看 [Trading Strategies and Backtesting](trading-strategies-and-backtesting.md)，把 indicators、signals、benchmark 與 drawdown review 串成完整交易研究流程。
