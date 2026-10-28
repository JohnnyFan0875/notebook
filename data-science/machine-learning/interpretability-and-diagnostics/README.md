[Machine Learning](../README.md) › 可解釋性與診斷

# 可解釋性與診斷 (Interpretability and Diagnostics)

兩個常被混在一起的問題：**模型依據什麼做預測？**（可解釋性）與**模型整體行為是否可信、沒有藏著資料或流程問題？**（診斷）。

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [模型可解釋性](model-interpretability.md) | 係數、permutation importance、PDP / ICE、SHAP | 哪些特徵影響預測？怎麼影響？ |
| [模型診斷](model-diagnostics.md) | 殘差、錯誤切片、校準、分布偏移 | 模型在學合理的訊號嗎？哪裡會壞？ |

統計模型的係數推論與迴歸診斷見 [statsmodels](../packages/statsmodels/README.md)、[模型假設與診斷](../../statistics/multivariate-analysis/assumptions-diagnostics.md)。

## 閱讀提醒

| 提醒 | 說明 |
| --- | --- |
| 可解釋性 ≠ 因果 | 重要特徵不代表改變它就會改變結果，見 [干擾](../../statistics/experimental-design/confounding-bias.md) |
| 診斷不只看模型 | 也要看資料與前處理流程 |
| 結果無法解釋時 | 先查資料切分、欄位定義與 [洩漏](../foundations/data-leakage.md)，再考慮換演算法 |
