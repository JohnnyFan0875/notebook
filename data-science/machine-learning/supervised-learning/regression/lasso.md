# Lasso Regression

Lasso Regression (Least Absolute Shrinkage and Selection Operator) is a [linear regression](linear.md) model that includes **L1 [regularization](../../foundations/regularization.md)**. It penalizes the absolute values of coefficients, which can shrink some coefficients to zero, effectively performing **[feature selection](../../preprocessing/feature-selection.md)**.

## 1. Import Required Libraries

```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
```

## 2. Generate Sample Data

```python
X, y = make_regression(n_samples=100, n_features=5, noise=0.1, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

## 3. Feature Scaling

```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

**Critical Note:**
Scaling is highly recommended for Lasso Regression because the penalty term depends on the magnitude of coefficients. Without scaling, features with larger scales dominate the penalty.

## 4. Define Model and Hyperparameter Grid

```python
lasso = Lasso()

param_grid = {'alpha': np.logspace(-4, 4, 100)}  # Range of penalty values
```

- `alpha`: [Regularization](../../foundations/regularization.md) strength.
  - Small alpha → less penalty → similar to OLS regression.
  - Large alpha → stronger penalty → more coefficients shrink to zero.

## 5. Grid Search with Cross-Validation

```python
grid_search = GridSearchCV(
    estimator=lasso,
    param_grid=param_grid,
    cv=5,
    scoring='neg_mean_squared_error'
)
grid_search.fit(X_train_scaled, y_train)

best_params_ = grid_search.best_params_
best_model = grid_search.best_estimator_
best_model_coef = best_model.coef_
best_score = grid_search.best_score_
```

- `best_params_`: Optimal alpha value.
- `best_model_coef`: Shows which features are important. Some may be exactly `0`.
- `best_score`: Best [cross-validation](../../workflow/cross-validation.md) performance.

## 6. Cross-Validation Performance

```python
cv_scores = cross_val_score(
    best_model, X_train_scaled, y_train,
    cv=5, scoring='neg_mean_squared_error'
)
```

## 7. Evaluate on Test Data

```python
y_pred = best_model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)

print("Test MSE:", mse)
print("Best alpha:", best_params_)
print("Best coefficients:", best_model_coef)
```

## 8. Predict on New Data

```python
new_data = np.random.rand(5, 5)  # 5 new data points, 5 features
new_data_scaled = scaler.transform(new_data)
predictions = best_model.predict(new_data_scaled)

print("Predictions:", predictions)
```

## 9. Visualizing Coefficients

```python
plt.bar(range(len(best_model_coef)), best_model_coef)
plt.xlabel("Feature Index")
plt.ylabel("Coefficient Value")
plt.title("Lasso Regression Coefficients")
plt.show()
```

## Key Takeaways

- Lasso is useful when you suspect **many features are irrelevant**.
- Lasso performs **automatic [feature selection](../../preprocessing/feature-selection.md)** by shrinking some coefficients to zero.
- Use **[cross-validation](../../workflow/cross-validation.md)** to tune `alpha`.
- Always scale features before applying Lasso.
- If all coefficients shrink too much, try reducing `alpha`.

## Related Concepts

- [Regularization](../../foundations/regularization.md)
- [Elastic Net Regression](elastic-net.md)
- [Feature Scaling](../../preprocessing/feature-scaling.md)
- [Hyperparameter Tuning](../../workflow/hyperparameter-tuning.md)

[Back to Regression](README.md)
