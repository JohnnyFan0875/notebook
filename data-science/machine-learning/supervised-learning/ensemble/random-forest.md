# Random Forest



Random Forest is an ensemble learning method that builds multiple [decision tree](../classification/decision-tree.md)s and aggregates their predictions. It combines the ideas of **[bagging](bagging.md)** and **feature randomness**, making it robust and less prone to [overfitting](../../foundations/overfitting-underfitting.md).

- **RandomForestClassifier** for [classification](../classification/README.md) tasks.
- **RandomForestRegressor** for [regression](../regression/README.md) tasks.

## Random Forest Classifier

```python
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
data = load_iris()
X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Random Forest Classifier
rf = RandomForestClassifier(random_state=42, oob_score=True)

# Hyperparameter grid
param_grid = {
    'n_estimators': [10, 50, 100],     # Number of trees
    'max_depth': [None, 10, 20],       # Max tree depth
    'min_samples_split': [2, 5, 10],   # Min samples to split an internal node
    'min_samples_leaf': [1, 2, 4],     # Min samples at a leaf node
    'bootstrap': [True, False]         # Bootstrap sampling
}

# Grid search
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1)
grid_search.fit(X_train, y_train)

best_params_ = grid_search.best_params_
best_model = grid_search.best_estimator_
best_score = grid_search.best_score_

# Predictions
y_pred = best_model.predict(X_test)

# Feature importance
feature_importance = best_model.feature_importances_

# Accuracy and OOB score
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

- Random Forest reduces variance but may still overfit with too many deep trees. Use `max_depth` and `min_samples_leaf` to control complexity.
- `feature_importances_` can be used to interpret which features contribute most to predictions.
- OOB (Out-of-Bag) score provides an unbiased estimate of accuracy.

## Random Forest Regressor

```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Generate regression dataset
X, y = make_regression(n_samples=200, n_features=10, noise=0.2, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest Regressor
rf_reg = RandomForestRegressor(
    n_estimators=100,
    max_depth=None,
    random_state=42,
    oob_score=True
)

# Train
rf_reg.fit(X_train, y_train)

# Predictions
y_pred = rf_reg.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
oob_r2 = rf_reg.oob_score_  # OOB R² score for regression

# Cross-validation
cv_scores = cross_val_score(rf_reg, X, y, cv=5, scoring='r2')

print(f"Test MSE: {mse:.4f}")
print(f"Test R²: {r2:.4f}")
print(f"OOB R² Score: {oob_r2:.4f}")
print(f"Cross-Validation R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
```

**Critical Notes:**

- Random Forest regression outputs are averages of multiple [decision tree](../classification/decision-tree.md)s, reducing variance.
- OOB R² provides an internal performance estimate without requiring a validation set.
- Increasing `n_estimators` improves stability but adds computation time.

## Key Takeaways

- Random Forest combines bagging with feature randomness for robustness.
- For classification: OOB score ≈ accuracy. For regression: OOB score ≈ R².
- Useful for feature importance analysis and handling high-dimensional datasets.
- Always tune hyperparameters (`n_estimators`, `max_depth`, `min_samples_leaf`) for best performance.

## Related Concepts

- [Decision Tree (Classification)](../classification/decision-tree.md)
- [Decision Tree (Regression)](../regression/decision-tree.md)
- [Model Interpretability](../../interpretability-and-diagnostics/model-interpretability.md)
- [Bias–Variance Tradeoff](../../foundations/bias-variance-tradeoff.md)

[Back to Ensemble Methods](README.md)
