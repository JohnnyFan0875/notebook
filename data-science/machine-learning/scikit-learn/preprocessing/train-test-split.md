# Train-Test Split

### Overview

- The **train-test split** is a fundamental step in supervised machine learning.
- It divides your dataset into a **training set** (used to fit the model) and a **test set** (used to evaluate performance on unseen data).
- Helps assess the model’s ability to **generalize** to new, unseen data.

### Best Practices

- Perform the split **after all preprocessing** (e.g., missing value imputation, feature encoding, scaling) but **before model training** to avoid **data leakage**.
- Use `random_state` for reproducibility.
- Typical split ratios:
  - 80/20 (training/testing) → common default.
  - 70/30 → if dataset is large enough.
  - 90/10 → when dataset is very large, and a small test set is sufficient.
- For **imbalanced datasets**, consider **stratified sampling** (`stratify=y`) to preserve class proportions.

### Example in scikit-learn

```python
from sklearn.model_selection import train_test_split
import numpy as np

# X: features, y: labels
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,      # 20% test data
    random_state=42,    # reproducible split
    stratify=y          # optional: keeps class proportions the same
)
```

### Related Concepts

- **Validation set**: Sometimes data is split into three parts (train, validation, test). The validation set is used for hyperparameter tuning, while the test set is reserved for final evaluation.
- **Cross-validation**: Instead of a single split, multiple train-test splits are averaged to give a more robust estimate of performance.

> Use train-test split to fairly evaluate your model’s predictive performance and reduce the risk of overfitting.
