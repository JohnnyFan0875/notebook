# Adaboosting



Adaptive Boosting (AdaBoost) is an ensemble method that combines multiple weak learners (often shallow [decision tree](../classification/decision-tree.md)s) sequentially, where each new learner focuses on correcting the mistakes of the previous ones.

- **AdaBoostClassifier** for [classification](../classification/README.md) tasks.
- **AdaBoostRegressor** for [regression](../regression/README.md) tasks.

## AdaBoost Classifier

```python
import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Load dataset
digits = load_digits()
X = digits.data
y = digits.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Base estimator (usually weak, e.g., decision stump)
base_estimator = DecisionTreeClassifier(max_depth=1)

# AdaBoost classifier
ada_boost = AdaBoostClassifier(base_estimator=base_estimator, random_state=42)

# Hyperparameter grid
param_grid = {
    'n_estimators': [50, 100, 150],  # Number of weak learners
    'learning_rate': [0.01, 0.1, 1.0]  # Shrinks contribution of each weak learner
}

# Grid search
grid_search = GridSearchCV(
    ada_boost,
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)
grid_search.fit(X_train, y_train)

best_params_ = grid_search.best_params_
best_model = grid_search.best_estimator_
best_score = grid_search.best_score_

# Predictions
y_pred = best_model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_pred)

# Cross-validation
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(best_model, X, y, cv=cv, scoring='accuracy')

print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Cross-Validation Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
```

**Critical Notes:**

- AdaBoost works best with **weak learners** (e.g., decision stumps).
- `n_estimators` too large can lead to [overfitting](../../foundations/overfitting-underfitting.md); tune carefully.
- A smaller `learning_rate` often requires more estimators but may improve [generalization](../../foundations/generalization.md).

## AdaBoost Regressor

```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Generate regression dataset
X, y = make_regression(n_samples=200, n_features=10, noise=0.3, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Base estimator (usually weak)
base_estimator = DecisionTreeRegressor(max_depth=3)

# AdaBoost Regressor
ada_reg = AdaBoostRegressor(
    base_estimator=base_estimator,
    n_estimators=100,
    learning_rate=0.1,
    random_state=42
)

# Train
ada_reg.fit(X_train, y_train)

# Predictions
y_pred = ada_reg.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

cv_scores = cross_val_score(ada_reg, X, y, cv=5, scoring='r2')

print(f"Test MSE: {mse:.4f}")
print(f"Test R²: {r2:.4f}")
print(f"Cross-Validation R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
```

**Critical Notes:**

- For regression, AdaBoost minimizes **loss functions** like squared error or absolute error.
- Sensitive to **outliers** since each learner tries to correct errors from previous ones.
- Tune both `learning_rate` and `n_estimators` together for best results.

## Key Takeaways

- AdaBoost focuses sequentially on misclassified/mispredicted samples.
- Works best with **simple base estimators**.
- For classification: commonly use decision stumps (`max_depth=1`).
- For regression: shallow trees (`max_depth` small) often work well.
- Careful tuning of `n_estimators` and `learning_rate` is crucial to avoid [overfitting](../../foundations/overfitting-underfitting.md).

## Related Concepts

- [Decision Tree (Classification)](../classification/decision-tree.md)
- [Hyperparameter Tuning](../../workflow/hyperparameter-tuning.md)
- [Bias–Variance Tradeoff](../../foundations/bias-variance-tradeoff.md)
- [Gradient Boosting](gradient-boosting.md)

[Back to Ensemble Methods](README.md)
