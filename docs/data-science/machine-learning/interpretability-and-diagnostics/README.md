# Interpretability and Diagnostics

這一章處理兩個常被混在一起、但其實不同的問題：

- 模型為什麼做出這個預測？
- 模型整體行為是否穩定、可信、沒有藏著資料或流程問題？

## 內容

- [Model Interpretability](model-interpretability.md): 係數、特徵重要度、permutation importance、PDP / ICE 與 SHAP 的使用時機。
- [Model Diagnostics](model-diagnostics.md): 從殘差、錯誤切片、資料漂移到校準檢查。
- [Statsmodels Package Notes](../packages/statsmodels/README.md): 當你需要更完整的統計摘要與診斷工具。

## 閱讀提醒

- interpretability 不等於 causality，重要變數不代表因果變數。
- diagnostics 不只看模型，也要看資料與前處理流程。
- 若模型結果無法解釋，先檢查資料切分、欄位定義與 leakage，再考慮更換演算法。

[Back to Machine Learning](../README.md)
