[Machine Learning](../README.md) › 模型評估

# 模型評估 (Evaluation)

評估是最容易產生錯覺的地方：分數高不代表能在真實世界用。要確認**指標選對**、**驗證方式合理**、**知道模型錯在哪**，還要知道分數本身有多不確定。評估設計要讓**驗證流程反映你真正要做的決策**，並在比較模型之前定好，不是之後。

## 先想清楚的問題

| 問題 | 決定 |
| --- | --- |
| 這是排序、機率估計，還是二元決策問題？ | 看 AUC / gains、校準，還是固定閾值下的混淆矩陣 |
| 錯誤成本對稱嗎？（漏診 vs 誤報） | 指標與 [閾值](classification-thresholds-and-calibration.md) |
| 驗證資料是否模擬了上線情境？ | 時間、分組、來源的切法，見 [切分策略](../preprocessing/train-test-split.md#切分策略) |
| 哪些子群最重要？ | 是否需要分層報告、公平性檢查 |
| 只能處理前 k% 嗎？（篩檢名額、行銷預算） | 用 [Gains / Lift](gains-and-lift-curves.md)、precision@k |
| 離線分數與真實結果相關嗎？ | 是否需要 A/B 測試或前瞻性驗證 |

> 生醫情境下，「AUC 0.85」本身沒有意義；要問的是在臨床可接受的偽陽性率下抓到多少病人、和現行做法相比改善多少。

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
| [Gains 與 Lift](gains-and-lift-curves.md)（選讀） | 累積增益、提升度 | 只能處理前 k% 時，模型值多少？ |
| [指標的不確定性](metric-uncertainty.md) | 信賴區間、bootstrap、配對比較 | 分數差 0.02 是真的進步還是雜訊？ |

## 評估檢查清單

| 檢查 | 筆記 |
| --- | --- |
| 指標對應實際目標？ | [ML 方法速查](../model-selection.md#3-選評估指標) |
| 和簡單 baseline 比過？ | [Baseline](baselines-and-error-analysis.md) |
| 看過不同群體、時間、區間的誤差？ | [錯誤分析](baselines-and-error-analysis.md) |
| 閾值與校準分開考慮？ | [閾值與校準](classification-thresholds-and-calibration.md) |
| 報告了不確定性？ | [指標的不確定性](metric-uncertainty.md) |

## 常見錯誤

| 錯誤 | 後果 | 改正 |
| --- | --- | --- |
| [不平衡資料](class-imbalance.md) 只看 accuracy | 全猜多數類別也有 95% | PR-AUC、recall、F1 |
| 分組或時間資料用隨機切分 | 分數虛高 | `GroupKFold`、`TimeSeriesSplit` |
| 只用單一分數挑模型 | 忽略變異與子群差異 | 報告 CV 平均 ± 標準差、子群表現 |
| 調參時反覆看測試集 | 測試集失去獨立性 | 測試集只用一次 |
| 差距小於 CV 標準差就宣稱「比較好」 | 只是雜訊 | 用同一組 folds 比較，見 [指標的不確定性](metric-uncertainty.md) |

見 [問題定義](../workflow/problem-framing.md)、[泛化](../foundations/generalization.md)、[資料洩漏](../foundations/data-leakage.md)。
