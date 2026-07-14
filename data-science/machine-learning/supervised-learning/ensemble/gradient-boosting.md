# Gradient Boosting

Gradient Boosting is an ensemble technique that builds models sequentially, where each new model tries to correct the errors of the previous ones using gradient descent on the loss function.

- **GradientBoostingClassifier** for [classification](../classification/README.md) tasks.
- **GradientBoostingRegressor** for [regression](../regression/README.md) tasks.

## Gradient Boosting Classifier

```python
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score

# Load dataset
data = load_iris()
X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Gradient Boosting Classifier
gb_clf = GradientBoostingClassifier()

# Hyperparameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.05, 0.1, 0.2],
    'max_depth': [3, 4, 5],
    'subsample': [0.8, 1.0],
    'min_samples_split': [2, 5]
}

# Grid search
grid_search = GridSearchCV(
    estimator=gb_clf,
    param_grid=param_grid,
    cv=StratifiedKFold(n_splits=5),
    scoring='accuracy',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

best_params_ = grid_search.best_params_
best_model = grid_search.best_estimator_
best_score = grid_search.best_score_

# Predictions
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Cross-validation
cv_scores = cross_val_score(best_model, X_train, y_train, cv=5, scoring='accuracy')

print(f"Test Accuracy: {accuracy:.4f}")
print(f"Cross-Validation Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
```

**Critical Notes:**

- Gradient Boosting is sensitive to **learning_rate**: smaller values require more estimators but may generalize better.
- `subsample < 1.0` introduces randomness (stochastic gradient boosting), reducing [overfitting](../../foundations/overfitting-underfitting.md).
- Deep trees can lead to [overfitting](../../foundations/overfitting-underfitting.md); tune `max_depth` carefully.

## Gradient Boosting Regressor

```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Generate regression dataset
X, y = make_regression(n_samples=200, n_features=10, noise=0.2, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Gradient Boosting Regressor
gb_reg = GradientBoostingRegressor()

# Hyperparameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.05, 0.1, 0.2],
    'max_depth': [3, 4, 5],
    'subsample': [0.8, 1.0],
    'min_samples_split': [2, 5]
}

# Grid search
grid_search = GridSearchCV(
    estimator=gb_reg,
    param_grid=param_grid,
    cv=5,
    scoring='r2',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

best_params_ = grid_search.best_params_
best_model = grid_search.best_estimator_
best_score = grid_search.best_score_

# Predictions
y_pred = best_model.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Cross-validation
cv_scores = cross_val_score(best_model, X_train, y_train, cv=5, scoring='r2')

print(f"Test MSE: {mse:.4f}")
print(f"Test R²: {r2:.4f}")
print(f"Cross-Validation R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
```

**Critical Notes:**

- Gradient Boosting Regressor can overfit if `n_estimators` and `max_depth` are too large.
- Use **early stopping** (via `validation_fraction` + `n_iter_no_change`) to prevent [overfitting](../../foundations/overfitting-underfitting.md).
- Smaller `learning_rate` with larger `n_estimators` often yields better results.

## Key Takeaways

- Gradient Boosting builds models sequentially, focusing on previous errors.
- Requires careful tuning of `n_estimators`, `learning_rate`, and `max_depth`.
- Subsampling makes the method more robust and reduces [overfitting](../../foundations/overfitting-underfitting.md).
- Strong [baseline](../../evaluation/baselines-and-error-analysis.md) model for both classification and regression tasks.

## Related Concepts

- [Bias–Variance Tradeoff](../../foundations/bias-variance-tradeoff.md)
- [Hyperparameter Tuning](../../workflow/hyperparameter-tuning.md)
- [AdaBoosting](adaboost.md)
- [Random Forest](random-forest.md)

[Back to Ensemble Methods](README.md)
