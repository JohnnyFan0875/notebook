# Train-Test Split

### Overview

- The **train-test split** is a fundamental step in supervised machine learning.
- It divides your dataset into a **training set** (used to fit the model) and a **test set** (used to evaluate performance on unseen data).
- Helps assess the model’s ability to [**generalize**](../foundations/generalization.md) to new, unseen data.

### Best Practices

- Perform the split **before fitting any preprocessing step that learns from data**.
- Then fit imputers, scalers, encoders, and feature selectors on the **training set only**.
- Apply the fitted preprocessing objects to validation and test data afterward.
- Use `random_state` for reproducibility.
- Typical split ratios:
  - 80/20 (training/testing) → common default.
  - 70/30 → if dataset is large enough.
  - 90/10 → when dataset is very large, and a small test set is sufficient.
- For **[imbalanced](../evaluation/class-imbalance.md) datasets**, consider **stratified sampling** (`stratify=y`) to preserve class proportions.
- For **grouped data**, split by entity rather than by row.
- For **time-dependent data**, preserve temporal order instead of shuffling.

### Example in scikit-learn

```python
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# X: features, y: labels
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,      # 20% test data
    random_state=42,    # reproducible split
    stratify=y          # optional: keeps class proportions the same
)

imputer = SimpleImputer(strategy="median")
scaler = StandardScaler()

X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
```

### Related Concepts

- **Validation set**: Sometimes data is split into three parts (train, validation, test). The validation set is used for [hyperparameter tuning](../workflow/hyperparameter-tuning.md), while the test set is reserved for final evaluation.
- [**Cross-validation**](../workflow/cross-validation.md): Instead of a single split, multiple train-test splits are averaged to give a more robust estimate of performance.
- [**Pipeline**](../workflow/pipeline-basic.md): A safer way to ensure preprocessing is fit only on training data.

> Split first, fit preprocessing second. Doing the reverse usually causes leakage.

[Back to Preprocessing](README.md)
