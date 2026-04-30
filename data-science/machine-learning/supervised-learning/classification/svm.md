# Support Vector Machine (SVM)



Support Vector Machines are supervised learning models that try to find a decision boundary with the largest possible margin between classes.

## Core Idea

- The decision boundary is defined by a subset of training points called **support vectors**.
- A larger margin often improves [generalization](../../foundations/generalization.md).
- Kernels allow SVMs to model non-linear boundaries.

## Important Hyperparameters

- `C`: controls the tradeoff between margin size and training error
- `kernel`: `linear`, `rbf`, `poly`, or `sigmoid`
- `gamma`: controls how far the influence of each point reaches for kernels such as `rbf`

## Practical Notes

- SVM is sensitive to [feature scaling](../../preprocessing/feature-scaling.md).
- Linear SVM works well in high-dimensional settings, including some text problems.
- Kernel SVM can be powerful but may become slow on large datasets.

## Example

```python
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("model", SVC(kernel="rbf", C=1.0, gamma="scale", probability=True))
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
```

## When to Use

- Medium-sized datasets
- Clear margin-based classification problems
- High-dimensional tabular or text-like features

## Related Concepts

- [Feature Scaling](../../preprocessing/feature-scaling.md)
- [Hyperparameter Tuning](../../workflow/hyperparameter-tuning.md)
- [Regularization](../../foundations/regularization.md)
- [Confusion Matrix](../../evaluation/confusion-metrics.md)

[Back to Classification](README.md)
