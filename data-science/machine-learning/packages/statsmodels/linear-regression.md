# Statsmodels: Linear Regression

## Import and Setup

```python
import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
```

## Fitting a Linear Regression Model

```python
# Example dataset
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [2, 4, 5, 4, 5]
})

# Fit linear regression model
model = ols("y ~ x", data=df).fit()
```

- The formula syntax (`y ~ x`) means: regress `y` on `x`.
- Multiple predictors can be included with `+`, e.g., `y ~ x1 + x2`.

## Model Parameters

```python
intercept, slope = model.params
print(intercept, slope)
# Example output: 2.2, 0.6
```

- `params`: estimated [regression](../../supervised-learning/regression/README.md) coefficients (intercept and slope).
- Interpretation: a one-unit increase in `x` is associated with an additive change of `slope` units in `y`, under the fitted linear model.

## Model Summary

```python
print(model.summary())
```

- Produces a detailed statistical summary including coefficients, R-squared, F-statistic, p-values, and confidence intervals.

## Predictions

```python
# Fitted values for original data
df["fitted"] = model.fittedvalues

# Residuals (y - df["fitted"])
df["residuals"] = model.resid

# Predict for new data
new_data = pd.DataFrame({"x": [6, 7, 8]})
predictions = model.predict(new_data)
print(predictions)
```

- `fittedvalues`: predicted values for training data.
- `resid`: residuals (errors).
- `predict(new_data)`: predictions for new observations.

## Model Fit Metrics

| Metric                                   | Reference                                                                                     |
| ---------------------------------------- | --------------------------------------------------------------------------------------------- |
| R-squared (Coefficient of Determination) | [R-squared (Coefficient of Determination)](metrics.md#r-squared-coefficient-of-determination) |
| Mean Squared Error ([MSE](../../evaluation/mse-rmse.md))                 | [Mean Squared Error (MSE)](metrics.md#mean-squared-error-mse)                                 |
| Root Mean Squared Error ([RMSE](../../evaluation/mse-rmse.md))           | [Root Mean Squared Error (RMSE)](metrics.md#root-mean-squared-error-rmse)                     |

## Leverage and Influence Diagnostics

| Diagnostic      | Reference                                        |
| --------------- | ------------------------------------------------ |
| Leverage        | [Leverage](diagnostics.md#leverage)              |
| Cook's Distance | [Cook's Distance](diagnostics.md#cooks-distance) |

## Visual Example

```python
import matplotlib.pyplot as plt

plt.scatter(df["x"], df["y"], label="Observed")
plt.plot(df["x"], df["fitted"], color="red", label="Fitted line")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()
```

- This shows the data points and the regression line estimated by statsmodels.

## Key Takeaways

- Use `ols("y ~ x", data=df).fit()` for [linear regression](../../supervised-learning/regression/linear.md) in statsmodels.
- `summary()` gives detailed statistical diagnostics.
- `params`, `fittedvalues`, `resid`, `rsquared`, and `mse_resid` provide insight into model quality.
- `get_influence()` yields leverage and influence measures.
- Statsmodels is particularly useful when you need **interpretability and statistical inference**, not just predictions.

## Related Concepts

- [Statsmodels Documentation](README.md)
- [Linear Regression](../../supervised-learning/regression/linear.md)
- [MSE, RMSE](../../evaluation/mse-rmse.md)
- [Regression Diagnostics](diagnostics.md)

[Back to Statsmodels Documentation](README.md)
