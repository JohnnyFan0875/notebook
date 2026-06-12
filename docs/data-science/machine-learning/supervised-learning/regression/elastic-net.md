# Elastic Net Regression

Elastic Net combines **L1 [regularization](../../foundations/regularization.md)** from Lasso and **L2 regularization** from Ridge.
It is useful when you want both coefficient shrinkage and some [feature selection](../../preprocessing/feature-selection.md) behavior.

## Why Use Elastic Net

- Handles correlated predictors better than pure Lasso
- Can shrink coefficients while still setting some to zero
- Useful when there are many features and multicollinearity

## Key Hyperparameters

- `alpha`: overall [regularization](../../foundations/regularization.md) strength
- `l1_ratio`: mix between L1 and L2
  - `1.0` means Lasso-like
  - `0.0` means Ridge-like

## Example

```python
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNet

pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("model", ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=42))
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
```

## Practical Notes

- Standardize features before fitting.
- Tune both `alpha` and `l1_ratio`.
- Compare against Ridge and Lasso instead of assuming Elastic Net is always better.

## Related Concepts

- [Regularization](../../foundations/regularization.md)
- [Lasso Regression](lasso.md)
- [Ridge Regression](ridge.md)
- [Feature Scaling](../../preprocessing/feature-scaling.md)

[Back to Regression](README.md)
