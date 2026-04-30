# Feature Selection



## Overview

- **Feature selection** is the process of identifying and selecting the most relevant features (variables) from a dataset for use in model training.
- Goals:
  - Reduce **[overfitting](../foundations/overfitting-underfitting.md)** by eliminating irrelevant/noisy features.
  - Improve **accuracy** by focusing on informative features.
  - Reduce **computational cost** by working with fewer variables.

## Main Approaches

### 1. Filter Methods

- Evaluate the relevance of features independently of the machine learning model.
- Typically use **statistical tests** or **information-theoretic measures**.
- Examples:
  - **Correlation matrix**: Remove features highly correlated with each other.
  - **Chi-squared test** (for categorical data).
  - **Mutual information** (captures non-linear relationships).

```python
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectKBest, chi2

X, y = load_iris(return_X_y=True)
selector = SelectKBest(score_func=chi2, k=2)
X_new = selector.fit_transform(X, y)
print("Selected features (indices):", selector.get_support(indices=True))
```

### 2. Wrapper Methods

- Use a machine learning model to evaluate subsets of features.
- Computationally more expensive since they involve **repeated model training**.
- Examples:
  - **Recursive Feature Elimination (RFE)**.
  - Stepwise selection.

```python
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=200)
rfe = RFE(model, n_features_to_select=2)
rfe = rfe.fit(X, y)
print("Selected features (indices):", rfe.get_support(indices=True))
```

### 3. Embedded Methods

- Perform feature selection **during model training**.
- Feature importance is a natural byproduct of the algorithm.
- Examples:
  - **LASSO [regression](../supervised-learning/regression/README.md) (L1 penalty)**.
  - **Decision tree / Random forest feature importances**.

```python
from sklearn.linear_model import Lasso
import numpy as np

lasso = Lasso(alpha=0.1)
lasso.fit(X, y)
print("Feature coefficients:", np.round(lasso.coef_, 3))
```

---

### Critical Notes

- **[Data leakage](../foundations/data-leakage.md)**: Always perform feature selection **inside the [cross-validation](../workflow/cross-validation.md) loop** (not before splitting train/test data).
- **Interpretability**: Feature importance scores can differ depending on the method and the model. Interpret with caution.
- **Dimensionality reduction ≠ feature selection**: Techniques like [PCA](../unsupervised-learning/dimensionality-reduction/pca.md) create new features, while feature selection keeps a subset of the original ones.
- **Balance**: Removing too many features may underfit, while keeping too many may overfit.

---

> Feature selection is an essential preprocessing step in machine learning [pipeline](../workflow/pipeline-basic.md)s. Combining multiple approaches (e.g., filter + embedded) often yields the most robust results.

## Related Concepts

- [Regularization](../foundations/regularization.md)
- [Feature Engineering Principles](../foundations/feature-engineering-principles.md)
- [Data Leakage](../foundations/data-leakage.md)
- [Pipeline Basics](../workflow/pipeline-basic.md)

[Back to Preprocessing](README.md)
