# Statsmodels: Logistic Regression

## Import and Setup

```python
import pandas as pd
import numpy as np
from statsmodels.formula.api import logit
```

## Fitting a Logistic Regression Model

```python
# Example dataset
df = pd.DataFrame({
    'x': [2, 3, 5, 7, 9, 11, 13, 15],
    'y': [0, 0, 0, 1, 1, 1, 1, 1]     # binary outcome
})

# Fit logistic regression model
model = logit("y ~ x", data=df).fit()
```

- The formula syntax (`y ~ x`) means: predict binary `y` from predictor `x`.
- Logistic regression estimates the probability that `y=1` given `x`.

## Model Parameters

```python
intercept, slope = model.params
print(intercept, slope)
# Example output: -6.0, 0.5
```

- `params`: estimated coefficients.
- Interpretation: a one-unit increase in `x` multiplies the odds of `y=1` by `exp(slope)`.

## Model Summary

```python
print(model.summary())
```

- Includes coefficients, p-values, confidence intervals, pseudo R-squared, and likelihood ratio tests.

## Predictions

```python
# Predicted probabilities for original data
df["probability"] = model.predict(df)

# Most likely class (threshold = 0.5, <0.5=0, ≥0.5=1)
df["predicted_class"] = np.round(df["probability"])

print(df)
```

- `predict()`: returns probabilities of `y=1`.
- Applying a threshold (commonly 0.5) converts probabilities into class predictions.

## Confusion Matrix

```python
# Actual vs predicted
actual_response = df['y']
predict_response = df['predicted_class']

from sklearn.metrics import confusion_matrix
conf_matrix = confusion_matrix(actual_response, predict_response)
print(conf_matrix)
# [[TN FP]
#  [FN TP]]
```

- `TN`: True Negatives, `TP`: True Positives.
- `FP`: False Positives, `FN`: False Negatives.

```python
from statsmodels.graphics.mosaicplot import mosaic
mosaic({('Actual', i, 'Predicted', j): count
        for i, row in enumerate(conf_matrix)
        for j, count in enumerate(row)})
```

- Mosaic plot visualizes classification results.

## Model Fit Metrics

| Metric                         | Reference                                                                 |
| ------------------------------ | ------------------------------------------------------------------------- |
| Mean Squared Error (MSE)       | [Mean Squared Error (MSE)](metrics.md#mean-squared-error-mse)             |
| Root Mean Squared Error (RMSE) | [Root Mean Squared Error (RMSE)](metrics.md#root-mean-squared-error-rmse) |

> For logistic regression, deviance and pseudo R² are often more informative than MSE.

## Leverage and Influence Diagnostics

| Diagnostic      | Reference                                        |
| --------------- | ------------------------------------------------ |
| Leverage        | [Leverage](diagnostics.md#leverage)              |
| Cook's Distance | [Cook's Distance](diagnostics.md#cooks-distance) |

## Visual Example

```python
import matplotlib.pyplot as plt

# Plot data points
plt.scatter(df["x"], df["y"], label="Observed")

# Logistic curve
x_range = np.linspace(df["x"].min(), df["x"].max(), 100)
y_pred = model.predict(pd.DataFrame({"x": x_range}))
plt.plot(x_range, y_pred, color="red", label="Logistic curve")

plt.xlabel("x")
plt.ylabel("Probability of y=1")
plt.legend()
plt.show()
```

- The logistic curve shows the probability of class `1` as `x` increases.

## Key Takeaways

- Use `logit("y ~ x", data=df).fit()` for logistic regression in statsmodels.
- `summary()` provides statistical diagnostics.
- `predict()` gives probabilities, which can be converted into class labels.
- Confusion matrices and plots help evaluate classification accuracy.
- Diagnostics (`leverage`, `Cook’s distance`) help identify influential points.
- Logistic regression is best for binary outcomes, but can be extended to multinomial or ordinal cases with other `statsmodels` functions.
