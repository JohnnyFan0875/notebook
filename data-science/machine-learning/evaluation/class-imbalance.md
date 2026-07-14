# Class Imbalance

Class imbalance happens when one class is much rarer than another.
This is common in fraud detection, disease screening, failures, and churn.

## Why It Matters

- [Accuracy](confusion-metrics.md) can look high even when the model is useless.
- Minority-class recall may collapse.
- Random [train-test split](../preprocessing/train-test-split.md)s can create unstable estimates on small datasets.

## Better Evaluation Choices

- [Precision](confusion-metrics.md)
- [Recall](confusion-metrics.md)
- [F1-score](confusion-metrics.md)
- PR-[AUC](roc-auc.md)
- Class-specific confusion matrix analysis

## Interview Fast Answer

這也是高頻題。

如果被問「accuracy 為什麼不夠」，最穩的回答通常是：

- 在 imbalance 問題裡，多數類別可能太容易猜中
- 高 accuracy 不代表 minority class 有被抓到
- 所以要看 recall、precision、F1、PR-AUC 或 class-specific confusion matrix

## Common Mitigation Strategies

- [Stratified splitting](../workflow/cross-validation.md)
- Class weights
- Resampling: oversampling, undersampling, SMOTE
- [Threshold tuning](classification-thresholds-and-calibration.md)
- Collect more minority-class data if possible

## Important Caution

Apply resampling only on the training data, ideally inside a cross-validation workflow.
Do not resample the full dataset before splitting.

## Common Interview Traps

- 在嚴重 imbalance 問題裡還用 accuracy 當主要指標
- 先對 full dataset 做 SMOTE / oversampling 再切資料
- classification task 卻不用 stratified split

## Related Concepts

- [Confusion Matrix](confusion-metrics.md)
- [Classification Thresholds and Calibration](classification-thresholds-and-calibration.md)
- [Cross-Validation Methods](../workflow/cross-validation.md)
- [Logistic Regression](../supervised-learning/classification/logistic-regression.md)

[Back to Evaluation](README.md)
