# Preprocessing

Preprocessing turns raw data into model-ready features.

## Topics

- [Train-Test Split](train-test-split.md)
- [Imputation](imputation.md)
- [Categorical Encoding](categorical-encoding.md)
- [Feature Scaling](feature-scaling.md)
- [Outlier Handling](outlier-handling.md)
- [Feature Selection](feature-selection.md)

## Notes

- Some preprocessing steps are model-sensitive. For example, [KNN](../supervised-learning/classification/knn.md) and [SVM](../supervised-learning/classification/svm.md) are more sensitive to scaling than tree-based models.
- Preprocessing should usually be placed inside a [pipeline](../workflow/pipeline-basic.md) to avoid leakage.
- The `train-test-split` note is kept here because it is tightly connected to preprocessing in day-to-day usage, but conceptually it belongs to the workflow layer.

[Back to Machine Learning](../README.md)
