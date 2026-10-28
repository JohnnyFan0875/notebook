[Machine Learning](../README.md) › 模型評估

# 模型評估 (Evaluation)

評估是最容易產生錯覺的地方：分數高不代表能在真實世界用。要確認**指標選對**、**驗證方式合理**、**知道模型錯在哪**，還要知道分數本身有多不確定。

## 先想清楚三件事

| 問題 | 決定 |
| --- | --- |
| 這是排序、機率估計，還是二元決策問題？ | 看 AUC / gains、校準，還是固定閾值下的混淆矩陣 |
| 錯誤成本對稱嗎？（漏診 vs 誤報） | 指標與 [閾值](classification-thresholds-and-calibration.md) |
| 驗證資料是否模擬了上線情境？ | 見 [資料切分與洩漏](../workflow/data-splitting-and-leakage.md) |

## 建議順序

```
Baseline → 迴歸指標 / 混淆矩陣 → ROC-AUC → 閾值與校準 → 類別不平衡 → Gains / Lift → 指標的不確定性
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Baseline 與錯誤分析](baselines-and-error-analysis.md) | Dummy 模型、錯誤切片 | 模型比「什麼都不學」好多少？錯在哪？ |
| [迴歸指標](mse-rmse.md) | MSE、RMSE、MAE、R²、MAPE | 連續預測差多少？ |
| [混淆矩陣指標](confusion-metrics.md) | Precision、recall、specificity、F1、MCC | 分類錯成什麼樣子？ |
| [ROC 與 AUC](roc-auc.md) | ROC 曲線、AUC 的意義、Youden | 模型排序能力好不好？ |
| [閾值與校準](classification-thresholds-and-calibration.md) | 調閾值、校準曲線、Brier score | 分數怎麼變成決策？機率可信嗎？ |
| [類別不平衡](class-imbalance.md) | PR-AUC、class weight、重抽樣 | 正類很少時怎麼評估、怎麼訓練？ |
| [Gains 與 Lift](gains-and-lift-curves.md) | 累積增益、提升度 | 只能處理前 k% 時，模型值多少？ |
| [指標的不確定性](metric-uncertainty.md) | 信賴區間、bootstrap、配對比較 | 分數差 0.02 是真的進步還是雜訊？ |

## 評估檢查清單

| 檢查 | 筆記 |
| --- | --- |
| 指標對應實際目標？ | [ML 方法速查](../model-selection.md#3-選評估指標) |
| 和簡單 baseline 比過？ | [Baseline](baselines-and-error-analysis.md) |
| 看過不同群體、時間、區間的誤差？ | [錯誤分析](baselines-and-error-analysis.md) |
| 閾值與校準分開考慮？ | [閾值與校準](classification-thresholds-and-calibration.md) |
| 報告了不確定性？ | [指標的不確定性](metric-uncertainty.md) |
