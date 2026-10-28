[Machine Learning](../README.md) › [基礎概念](README.md) › 評估思維

# 評估思維 (Evaluation Mindset)

好的評估不只是挑一個指標，而是讓**驗證流程反映你真正要做的決策**。評估設計要在比較模型之前定好，不是之後。

## 四個原則

| 原則 | 做法 | 筆記 |
| --- | --- | --- |
| 指標對齊目標 | 依錯誤代價選指標，不是預設用 accuracy | [ML 方法速查](../model-selection.md#3-選評估指標) |
| 切分對齊部署 | 時間、分組、來源的切法要模擬上線情境 | [資料切分與洩漏](../workflow/data-splitting-and-leakage.md) |
| 和 baseline 比 | 多數類別、平均值、簡單線性模型 | [Baseline 與錯誤分析](../evaluation/baselines-and-error-analysis.md) |
| 看失敗模式 | 不只看平均，也看哪些子群、哪些案例錯 | [Baseline 與錯誤分析](../evaluation/baselines-and-error-analysis.md) |

## 常見錯誤

| 錯誤 | 後果 | 改正 |
| --- | --- | --- |
| [不平衡資料](../evaluation/class-imbalance.md) 只看 accuracy | 全猜多數類別也有 95% | PR-AUC、recall、F1 |
| 分組或時間資料用隨機切分 | 分數虛高 | `GroupKFold`、`TimeSeriesSplit` |
| 只用單一分數挑模型 | 忽略變異與子群差異 | 報告 CV 平均 ± 標準差、子群表現 |
| 調參時反覆看測試集 | 測試集失去獨立性 | 測試集只用一次 |
| 差距小於 CV 標準差就宣稱「比較好」 | 只是雜訊 | 用同一組 folds 比較、看差異的分布 |

## 該問的問題

| 問題 | 影響 |
| --- | --- |
| 哪種錯誤代價最高？（漏診 vs 誤診） | 指標選擇、[閾值](../evaluation/classification-thresholds-and-calibration.md) |
| 哪些子群最重要？ | 是否需要分層報告、公平性檢查 |
| 決策需要機率還是排序？ | 要不要檢查校準 (calibration) |
| 只能處理前 k% 嗎？（篩檢名額、行銷預算） | 用 [Gains / Lift](../evaluation/gains-and-lift-curves.md)、precision@k |
| 離線分數與真實結果相關嗎？ | 是否需要 A/B 測試或前瞻性驗證 |

> 生醫情境下，「AUC 0.85」本身沒有意義；要問的是在臨床可接受的偽陽性率下抓到多少病人、和現行做法相比改善多少。

見 [問題定義](../workflow/problem-framing.md)、[泛化](generalization.md)。
