# Statsmodels: Regression Diagnostics

Diagnostics are tools to evaluate whether regression model assumptions hold and to identify influential observations. Unlike **metrics** (which summarize overall fit quality), diagnostics focus on **individual observations** and assumption checks.

## Import and Setup

```python
import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
```

Example dataset:

```python
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5, 20],  # Note: outlier at x=20
    'y': [1, 2, 1.3, 3.75, 2.25, 7]
})

model = ols("y ~ x", data=df).fit()
```

## Residuals

```python
residuals = model.resid
fitted = model.fittedvalues
```

- **Residuals**: differences between observed and predicted values.
- Plot residuals vs fitted values to check linearity and homoscedasticity.

```python
import matplotlib.pyplot as plt

plt.scatter(fitted, residuals)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel("Fitted values")
plt.ylabel("Residuals")
plt.show()
```

- If residuals show a pattern → model assumptions may be violated.

## Leverage

Leverage measures how far an observation’s predictors are from the mean of predictor values.

```python
influence = model.get_influence()
df_influence = influence.summary_frame()

# Leverage values
df["leverage"] = df_influence["hat_diag"]
```

- High leverage points can disproportionately affect the regression line.
- High leverage points are far from the mean of predictors.

- Although an **influential point** will often have **high leverage**, a high leverage point is **not necessarily influential**  
  ([source](https://stats.stackexchange.com/questions/65912/precise-meaning-of-and-comparison-between-influential-point-high-leverage-point)).

  - In the example below:

    - The **blue line** is the regression line based on all the data.
    - The **red line** is the regression line excluding the point at the top right.

  - ![Image](https://i.sstatic.net/7c5BB.png)

  - That point clearly has **high leverage** because it is far from the rest of the data.
  - However, since it still follows the overall pattern of the data, removing it barely changes the regression line.
  - Thus, it is **high leverage but not influential**.

## Cook’s Distance

Cook’s distance combines residual size and leverage to measure influence.

```python
df["cooks_d"] = df_influence["cooks_d"]
```

- Rule of thumb: points with Cook’s D > 4/n may be influential.
- Influential points (high Cook’s distance) strongly affect the regression line.

## DFBETAs

DFBETAs measure the effect of removing one observation on each regression coefficient.

```python
dfbetas = influence.dfbetas
print(dfbetas)
```

- Large absolute DFBETA values indicate an observation strongly affects a specific coefficient.

## DFFITS

DFFITS measures how much a predicted value changes when an observation is removed.

```python
dffits = influence.dffits[0]
print(dffits)
```

- Rule of thumb: |DFFITS| > 2 \* sqrt(p/n) indicates an influential point (p = number of predictors, n = sample size).

## Influence Plot

Statsmodels provides a built-in influence plot:

```python
from statsmodels.graphics.regressionplots import influence_plot

influence_plot(model)
plt.show()
```

- Visualizes leverage (x-axis), standardized residuals (y-axis), and Cook’s distance (bubble size).

## Key Takeaways

- **Residuals**: check linearity and homoscedasticity.
- **Leverage**: identifies points with unusual predictor values.
- **Cook’s Distance**: identifies influential observations.
- **DFBETAs and DFFITS**: quantify influence on coefficients and fitted values.
- **Influence plots**: provide a combined diagnostic view.

Diagnostics help ensure regression assumptions are valid and results are not driven by a few extreme observations.
