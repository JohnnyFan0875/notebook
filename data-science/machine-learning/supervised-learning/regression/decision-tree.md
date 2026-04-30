# Decision Tree (Regression)



[Decision Tree](../classification/decision-tree.md)s can also be applied to **regression** tasks. In [scikit-learn](../../packages/scikit-learn/README.md), this is implemented as:

- `DecisionTreeRegressor`

They split the data to minimize error metrics such as Mean Squared Error ([MSE](../../evaluation/mse-rmse.md)).

## Key Parameters

- **`max_depth`**: Controls tree depth, prevents [overfitting](../../foundations/overfitting-underfitting.md).
- **`min_samples_split`** and **`min_samples_leaf`**: Control minimum samples for splits and leaves.
- **`criterion`**: Split quality metric (`squared_error`, `absolute_error`, `friedman_mse`, `poisson`).

## Example: Regression

```python
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Example dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train regressor
regressor = DecisionTreeRegressor(max_depth=5, random_state=42)
regressor.fit(X_train, y_train)

# Predictions
y_pred_reg = regressor.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, y_pred_reg)
r2 = r2_score(y_test, y_pred_reg)
print(f"MSE: {mse}, R2: {r2}")
```

## Critical Notes

- **[Overfitting](../../foundations/overfitting-underfitting.md) risk**: Trees can overfit noisy regression data without constraints.
- **Interpretability**: Still interpretable, but regression trees may produce step-like predictions.
- **Better alternatives**: For continuous outcomes, ensembles like [Random Forest](../ensemble/random-forest.md) Regressor or [Gradient Boosting](../ensemble/gradient-boosting.md) Regressor often perform better.

## Related Concepts

- [MSE, RMSE](../../evaluation/mse-rmse.md)
- [Hyperparameter Tuning](../../workflow/hyperparameter-tuning.md)
- [Random Forest](../ensemble/random-forest.md)
- [Generalization](../../foundations/generalization.md)

[Back to Regression](README.md)
