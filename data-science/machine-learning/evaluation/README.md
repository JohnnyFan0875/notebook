# Evaluation

評估是機器學習最容易產生錯覺的地方。模型分數高，不代表它真的能在真實世界表現好；你還需要確認指標選得對、驗證方式合理，並知道模型錯在哪裡。

## 內容地圖

- [MSE and RMSE](mse-rmse.md): 連續目標的誤差量測。
- [Confusion Metrics](confusion-metrics.md): 分類問題的 precision、recall、specificity 與 F1。
- [ROC Curve and AUC](roc-auc.md): 觀察不同 threshold 下的辨識能力。
- [Cumulative Gains and Lift Curves](gains-and-lift-curves.md): 把排序能力翻成 top-list coverage 與 hit-rate efficiency。
- [Classification Thresholds and Calibration](classification-thresholds-and-calibration.md): 把分數轉成決策時最關鍵的一步。
- [Class Imbalance](class-imbalance.md): 當正負樣本差很多時，如何避免被 accuracy 誤導。
- [Baselines and Error Analysis](baselines-and-error-analysis.md): 建立比較基準，並回頭看模型在哪些切片失敗。

## 先想清楚的三件事

1. 這是排序問題、機率估計問題，還是最終二元決策問題？
2. 錯判的成本是否對稱？例如漏掉病患與多抓可疑案例，代價通常不同。
3. 驗證資料是否真的模擬了上線情境？

## 評估檢查清單

- 指標是否對應實際目標？
- 是否有與簡單 baseline 比較？
- 是否檢查不同群體、時間段或區間的誤差？
- 是否把 threshold 與 calibration 分開思考？

[Back to Machine Learning](../README.md)
