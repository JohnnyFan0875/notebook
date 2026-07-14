# Statsmodels: Regression Metrics

## Mean Squared Error (MSE)

- **Definition**: Average of squared differences between observed and predicted values. Penalizes large errors heavily.

```python
mse = model.mse_resid
print(mse)
```

- For linear models: `model.mse_resid` is readily available.
- Lower [MSE](../../evaluation/mse-rmse.md) indicates better fit.

Formula:
$[MSE](../../evaluation/mse-rmse.md) = \frac{1}{n}\sum_{i=1}^n (y_i - \hat{y}_i)^2$

## Root Mean Squared Error (RMSE)

- **Definition**: Square root of [MSE](../../evaluation/mse-rmse.md), interpretable in the same units as the dependent variable.

```python
rmse = np.sqrt(model.mse_resid)
print(rmse)
```

Alternative with `statsmodels.tools.eval_measures`:

```python
from statsmodels.tools.eval_measures import rmse
y_true = df["y"]
y_pred = model.predict(df)
print(rmse(y_true, y_pred))
```

## R-squared (Coefficient of Determination)

- **Definition**: Proportion of variance in the dependent variable explained by the model.

```python
r2 = model.rsquared
print(r2)
```

Formula:
$R^2 = 1 - \frac{SS_{res}}{SS_{tot}}$

- R² close to 1 → strong fit.
- R² close to 0 → weak fit.

## Adjusted R-squared

- Adjusts R² for the number of predictors, preventing inflation with too many variables.

```python
adj_r2 = model.rsquared_adj
print(adj_r2)
```

Formula:
$R^2_{adj} = 1 - (1 - R^2) \cdot \frac{n-1}{n-p-1}$

where:

- $n$ = number of observations
- $p$ = number of predictors

## Mean Absolute Error (MAE)

- **Definition**: Average absolute difference between observed and predicted values.

```python
mae = np.mean(np.abs(df["y"] - model.predict(df)))
print(mae)
```

- Less sensitive to outliers than [MSE](../../evaluation/mse-rmse.md).

Formula:
$MAE = \frac{1}{n}\sum_{i=1}^n |y_i - \hat{y}_i|$

## Pseudo R-squared (for Logistic Regression)

- [Logistic regression](../../supervised-learning/classification/logistic-regression.md) does not have a true R². Several pseudo R² measures exist (McFadden’s R² is most common).

```python
pseudo_r2 = model.prsquared
print(pseudo_r2)
```

- Interpretation: closer to 1 indicates better model fit.

## Classification Metrics (for Logistic Regression)

For [classification](../../supervised-learning/classification/README.md) models, beyond pseudo R², we use **[confusion matrix](../../evaluation/confusion-metrics.md) and derived scores**:

```python
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

actual = df["y"]
predicted_class = np.round(model.predict(df))

print(confusion_matrix(actual, predicted_class))
print("Accuracy:", accuracy_score(actual, predicted_class))
print("Precision:", precision_score(actual, predicted_class))
print("Recall:", recall_score(actual, predicted_class))
print("F1 Score:", f1_score(actual, predicted_class))
```

- **Accuracy**: proportion of correct predictions.
- **Precision**: proportion of predicted positives that are true positives.
- **Recall (Sensitivity)**: proportion of actual positives correctly identified.
- **F1 Score**: harmonic mean of precision and recall.

## Key Takeaways

- **[Linear regression](../../supervised-learning/regression/linear.md) metrics**: [MSE](../../evaluation/mse-rmse.md), [RMSE](../../evaluation/mse-rmse.md), MAE, R², Adjusted R².
- **[Logistic regression](../../supervised-learning/classification/logistic-regression.md) metrics**: pseudo R², [confusion matrix](../../evaluation/confusion-metrics.md), accuracy, precision, recall, F1.
- Use metrics in context:

  - R² and Adjusted R² for model explanatory power.
  - [MSE](../../evaluation/mse-rmse.md)/[RMSE](../../evaluation/mse-rmse.md)/MAE for error magnitude.
  - Confusion matrix and classification metrics for classification tasks.

- Always complement numerical metrics with **residual diagnostics and influence analysis**.

## Related Concepts

- [Statsmodels Documentation](README.md)
- [MSE, RMSE](../../evaluation/mse-rmse.md)
- [Confusion Matrix](../../evaluation/confusion-metrics.md)
- [ROC curve, AUC](../../evaluation/roc-auc.md)

[Back to Statsmodels Documentation](README.md)
