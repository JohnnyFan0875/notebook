# Classification

Classification predicts a discrete label such as spam / not spam, churn / no churn, or disease class.

## Topics

- [Logistic Regression](logistic-regression.md)
- [K-Nearest Neighbors (KNN)](knn.md)
- [Decision Tree](decision-tree.md)
- [Support Vector Machine (SVM)](svm.md)

## Notes

- Start with logistic [regression](../regression/README.md) as a strong [baseline](../../evaluation/baselines-and-error-analysis.md).
- Use KNN and SVM when scaling and distance behavior matter.
- Use trees when interpretability and non-linear splits are useful.

## Beginner Reminders

- Classification models often output scores or probabilities before they become decisions.
- Accuracy alone is usually not enough, especially with imbalanced classes.
- Think about [thresholds](../../evaluation/classification-thresholds-and-calibration.md) together with the model, not after the fact.

[Back to Supervised Learning](../README.md)
