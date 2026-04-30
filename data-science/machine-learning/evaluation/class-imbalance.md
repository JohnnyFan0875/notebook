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

## Common Mitigation Strategies

- [Stratified splitting](../workflow/cross-validation.md)
- Class weights
- Resampling: oversampling, undersampling, SMOTE
- [Threshold tuning](classification-thresholds-and-calibration.md)
- Collect more minority-class data if possible

## Important Caution

Apply resampling only on the training data, ideally inside a cross-validation workflow.
Do not resample the full dataset before splitting.

## Related Concepts

- [Confusion Matrix](confusion-metrics.md)
- [Classification Thresholds and Calibration](classification-thresholds-and-calibration.md)
- [Cross-Validation Methods](../workflow/cross-validation.md)
- [Logistic Regression](../supervised-learning/classification/logistic-regression.md)

[Back to Evaluation](README.md)
