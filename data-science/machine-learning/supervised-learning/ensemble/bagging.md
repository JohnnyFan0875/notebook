# Bagging Ensemble Learning



Bagging (Bootstrap Aggregating) is an ensemble method that improves model stability and accuracy by combining predictions from multiple base estimators trained on bootstrapped subsets of the data.

- **BaggingClassifier** for [classification](../classification/README.md) tasks.
- **BaggingRegressor** for [regression](../regression/README.md) tasks.

## Bagging Classifier

```python
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, StratifiedKFold
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score

# Load dataset
data = load_iris()
X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Base estimator (commonly DecisionTreeClassifier)
base_estimator = DecisionTreeClassifier(random_state=42)

bagging = BaggingClassifier(
    base_estimator=base_estimator,
    random_state=42,
    oob_score=True  # Out-of-bag evaluation
)

# Hyperparameter grid
param_grid = {
    'n_estimators': [10, 50, 100],    # Number of base estimators
    'max_samples': [0.5, 0.7, 1.0],   # Proportion of samples per estimator
    'max_features': [0.5, 0.7, 1.0],  # Proportion of features per estimator
    'bootstrap': [True, False]        # Sampling with or without replacement
}

# Grid search
grid_search = GridSearchCV(
    estimator=bagging,
    param_grid=param_grid,
    cv=5,
    n_jobs=-1,
    verbose=2
)
grid_search.fit(X_train, y_train)

best_params_ = grid_search.best_params_
best_model = grid_search.best_estimator_
best_score = grid_search.best_score_

# Evaluate
y_pred = best_model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_pred)
oob_score = best_model.oob_score_  # OOB score (accuracy for classification)

# Cross-validation
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(best_model, X, y, cv=cv, scoring='accuracy')

print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"OOB Score: {oob_score:.4f}")
print(f"Cross-Validation Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
```

**Critical Notes:**

- **Out-of-Bag (OOB) score** gives an unbiased estimate of model performance without needing a separate validation set.
- Bagging reduces **variance**, especially helpful for unstable models like [decision treeS](../classification/decision-tree.md).
- If `bootstrap=False`, it becomes **pasting** (sampling without replacement).

## Bagging Regressor

```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import BaggingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Generate regression dataset
X, y = make_regression(n_samples=200, n_features=10, noise=0.2, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Base estimator (commonly DecisionTreeRegressor)
base_estimator = DecisionTreeRegressor(random_state=42)

bagging_reg = BaggingRegressor(
    base_estimator=base_estimator,
    n_estimators=100,
    random_state=42,
    oob_score=True  # OOB R² score for regression
)

# Train
bagging_reg.fit(X_train, y_train)

# Predictions
y_pred = bagging_reg.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
oob_r2 = bagging_reg.oob_score_

cv_scores = cross_val_score(bagging_reg, X, y, cv=5, scoring='r2')

print(f"Test MSE: {mse:.4f}")
print(f"Test R²: {r2:.4f}")
print(f"OOB R² Score: {oob_r2:.4f}")
print(f"Cross-Validation R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
```

**Critical Notes:**

- For regression, OOB score corresponds to **R²**.
- Bagging reduces variance but may not reduce bias—if the base learner is too simple, performance might still be limited.
- Increasing `n_estimators` generally improves stability but increases computation time.

## Key Takeaways

- Bagging improves stability by aggregating predictions from multiple bootstrapped datasets.
- Works well with high-variance models like **[decision trees](../classification/decision-tree.md)**.
- Use **OOB scores** for an internal unbiased validation.
- For classification: OOB score ≈ accuracy. For regression: OOB score ≈ R².

## Related Concepts

- [Decision Tree (Classification)](../classification/decision-tree.md)
- [Bias–Variance Tradeoff](../../foundations/bias-variance-tradeoff.md)
- [Random Forest](random-forest.md)
- [Cross-Validation Methods](../../workflow/cross-validation.md)

[Back to Ensemble Methods](README.md)
