# Decision Tree (Regression)

[Decision Tree](../classification/decision-tree.md)s 也可以用在回歸問題。和線性回歸不同，回歸樹不是擬合一條平滑直線，而是把特徵空間切成多個區塊，讓每個區塊輸出一個常數預測值。

This note focuses on **regression trees**: piecewise-constant prediction, regression loss, and how tree depth affects numeric prediction. For the class-prediction variant, see [Decision Tree (Classification)](../classification/decision-tree.md).

在 [scikit-learn](../../packages/scikit-learn/README.md) 中，對應類別是 `DecisionTreeRegressor`。

## Core Idea

- 反覆選擇切分點，讓每個節點內的目標值更一致。
- 常見目標是最小化 Mean Squared Error ([MSE](../../evaluation/mse-rmse.md)) 或其他回歸損失。
- 最終預測通常呈現階梯狀，而不是平滑曲線。

## Key Parameters

- **`max_depth`**: controls tree depth and helps prevent [overfitting](../../foundations/overfitting-underfitting.md)
- **`min_samples_split`** and **`min_samples_leaf`**: require enough samples before splitting or keeping a leaf
- **`criterion`**: split quality metric (`squared_error`, `absolute_error`, `friedman_mse`, `poisson`)

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

## How to Interpret Results

- 如果資料中有明顯非線性或交互作用，回歸樹常比單純線性模型更容易抓到結構。
- 如果預測曲線看起來非常鋸齒或在訓練集超準，通常代表樹太深了。
- 單棵樹的解釋性高，但預測穩定性通常不如 ensemble。

## Critical Notes

- **[Overfitting](../../foundations/overfitting-underfitting.md) risk**: trees can overfit noisy regression data without constraints
- **Interpretability**: still interpretable, but predictions are step-like rather than smooth
- **Better alternatives**: ensembles like [Random Forest](../ensemble/random-forest.md) or [Gradient Boosting](../ensemble/gradient-boosting.md) often perform better on tabular data

## Common Pitfalls

- 沒有限制樹深度或 leaf 大小。
- 把單棵回歸樹的高訓練分數誤認為泛化能力。
- 忽略樹模型對資料微小變動可能相當敏感。 

## Related Concepts

- [MSE, RMSE](../../evaluation/mse-rmse.md)
- [Hyperparameter Tuning](../../workflow/hyperparameter-tuning.md)
- [Random Forest](../ensemble/random-forest.md)
- [Generalization](../../foundations/generalization.md)

[Back to Regression](README.md)
