# Model Diagnostics

診斷的目的，是確認模型是否真的在學合理訊號，而不是剛好在某個切分上得到好分數。當模型表現「異常地好」或「異常地差」時，diagnostics 通常比換演算法更重要。

## 先看哪三層

1. 資料層：欄位、缺失值、分布、重複值與 train/test 差異。
2. 預測層：分數分布、殘差、混淆矩陣、校準情況。
3. 切片層：不同群體、時間段、地區、價格區間或樣本量下的誤差。

## Regression Diagnostics

- residual plots
- heteroscedasticity checks
- influence and leverage analysis
- error by prediction range

## Classification Diagnostics

- confusion matrix
- precision and recall by [threshold](../evaluation/classification-thresholds-and-calibration.md)
- probability [calibration](../evaluation/classification-thresholds-and-calibration.md)
- error slices by subgroup

## Data Diagnostics

- missingness patterns
- distribution shift between train and test
- duplicate or near-duplicate rows
- feature drift over time

## 一個實務檢查順序

1. 先確認資料切分與 [pipeline](../workflow/pipeline-basic.md) 是否正確。
2. 再看整體分數與基準模型差多少。
3. 接著看錯誤主要集中在哪些切片。
4. 最後才決定是否需要改特徵、改 threshold 或換模型。

## 常見警訊

- 測試分數高得不合理，懷疑 leakage。
- 某個少數群體表現特別差，但整體平均掩蓋了問題。
- 模型在高值區間系統性低估，或在低值區間系統性高估。
- 預測機率很極端，但實際 precision 不穩，代表 calibration 可能有問題。

## Practical Habit

Whenever a model performs unexpectedly well or unexpectedly poorly, inspect both the data [pipeline](../workflow/pipeline-basic.md) and the error distribution before changing algorithms.

## Related Concepts

- [Baselines and Error Analysis](../evaluation/baselines-and-error-analysis.md)
- [Model Interpretability](model-interpretability.md)
- [Statsmodels Documentation](../packages/statsmodels/README.md)
- [Generalization](../foundations/generalization.md)

[Back to Interpretability and Diagnostics](README.md)
