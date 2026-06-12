# Simple Linear Regression

Simple linear regression models the relationship between **one predictor variable (X)** and **one continuous outcome variable (Y)** using a straight line. It is the foundation of all regression methods.

Key point: Precondition: Before establishing a regression model, please use a scatter plot to confirm that there is indeed a linear trend between X and Y. Blindly applying linear regression to nonlinear relationships will yield biased results.

## The Regression Equation

\[
Y = \beta_0 + \beta_1 X + \varepsilon
\]

| Symbol | Meaning |
| ----------- | ---------------------------------------------------------------- |
| $Y$ | Outcome / response variable (what you're predicting) |
| $X$ | Predictor / explanatory variable |
| $\beta_0$ | Intercept — predicted value of Y when X = 0 |
| $\beta_1$ | Slope — how much Y changes for a one-unit increase in X |
| $\varepsilon$ | Residual / error — the part of Y not explained by X |

The fitted (predicted) values drop the error term:

\[
\hat{Y} = \hat{\beta}_0 + \hat{\beta}_1 X
\]

## Ordinary Least Squares (OLS)

OLS finds the line that **minimizes the sum of squared residuals (SSR)**:

\[
\text{SSR} = \sum_{i=1}^{n} (Y_i - \hat{Y}_i)^2
\]

Intuitively: for every data point, compute the vertical distance between the actual value and the line. Square each distance (to penalize large errors and remove sign), then minimize the total.

The closed-form solutions are:

\[
\hat{\beta}_1 = \frac{\sum(X_i - \bar{X})(Y_i - \bar{Y})}{\sum(X_i - \bar{X})^2} = r \cdot \frac{S_Y}{S_X}
\]

\[
\hat{\beta}_0 = \bar{Y} - \hat{\beta}_1 \bar{X}
\]

Tip: The slope is directly related to the Pearson correlation coefficient r. If r = 0, the slope is also 0 — meaning X provides no linear predictive value.

## Python Implementation

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import statsmodels.formula.api as smf

# Load data
iris = load_iris(as_frame=True)
df = iris.frame
df.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'target']

# ── Method 1: statsmodels (gives full statistical output) ──
model = smf.ols('petal_length ~ sepal_length', data=df).fit()
print(model.summary())

# ── Method 2: scikit-learn (machine learning workflow) ──
X = df[['sepal_length']]
y = df['petal_length']

lr = LinearRegression()
lr.fit(X, y)

print(f"Intercept (β₀): {lr.intercept_:.4f}")
print(f"Slope (β₁):     {lr.coef_[0]:.4f}")
print(f"R²:             {lr.score(X, y):.4f}")
```

**Key output from `model.summary()`:**

| Term | Value | Interpretation |
| ----------- | ------ | ----------------------------------------------- |
| Intercept | −7.101 | Predicted petal length when sepal length = 0 cm (not meaningful here) |
| sepal_length | 1.858 | For every 1 cm increase in sepal length, petal length increases by 1.858 cm |
| R² | 0.760 | 76% of variation in petal length is explained by sepal length |
| p-value | < 0.001 | The slope is statistically significant |

## Interpreting the Coefficients

### Intercept (β₀)

The predicted value of Y when X = 0. This is often **not meaningful in practice** (e.g., a sepal length of 0 cm is impossible). Focus on the slope instead.

### Slope (β₁)

- **Positive slope** (β₁ > 0): Y increases as X increases
- **Negative slope** (β₁ < 0): Y decreases as X increases
- **Magnitude**: a one-unit increase in X is associated with a β₁-unit change in Y, **all else equal**

Warning: "Associated with" ≠ "causes". Regression quantifies association, not causation.

## Model Fit: R²

\[
R^2 = 1 - \frac{\text{SSR}}{\text{SST}} = 1 - \frac{\sum(Y_i - \hat{Y}_i)^2}{\sum(Y_i - \bar{Y})^2}
\]

| Component | Meaning |
| --------- | ----------------------------------------- |
| SST | Total variation in Y around its mean |
| SSR | Variation in Y **not** explained by X |
| SSM | Variation in Y explained by X = SST − SSR |

| R² Range | Interpretation |
| --------- | ---------------------------------------- |
| 1.0 | Perfect fit (should be suspicious in real data) |
| 0.7–0.9 | Strong fit (common in physical sciences) |
| 0.4–0.6 | Moderate fit (common in social sciences) |
| < 0.3 | Weak fit — X explains little of Y |
| 0.0 | X provides no linear predictive value |

Tip: R² tells you proportion of variance explained — it does not tell you if the model assumptions are met or if the model is appropriate. A perfect R² with assumption violations is worthless.

## Assumptions of Linear Regression

These assumptions apply to the **residuals** (ε), not the raw data.

| Assumption | How to Check |
| ----------------------- | --------------------------------- |
| **Linearity** | Scatter plot of X vs Y; Residuals vs Fitted plot |
| **Independence** | Study design; Durbin-Watson test |
| **Homoscedasticity** | Residuals vs Fitted — should show no funnel shape |
| **Normality of residuals** | Q–Q plot; Shapiro-Wilk test |
| **No influential outliers** | Cook's Distance; leverage plots |

Key point: Mnemonic: LINE (Linearity, Independence, Normality, Equal variance)

## Diagnostic Plots

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import statsmodels.formula.api as smf

model = smf.ols('petal_length ~ sepal_length', data=df).fit()

fitted  = model.fittedvalues
residuals = model.resid
std_resid = (residuals - residuals.mean()) / residuals.std()

fig, axes = plt.subplots(2, 2, figsize=(12, 9))

# 1. Residuals vs Fitted
axes[0, 0].scatter(fitted, residuals, alpha=0.5)
axes[0, 0].axhline(0, color='red', linestyle='--')
axes[0, 0].set_xlabel('Fitted Values')
axes[0, 0].set_ylabel('Residuals')
axes[0, 0].set_title('Residuals vs Fitted')

# 2. Q–Q plot
stats.probplot(residuals, dist='norm', plot=axes[0, 1])
axes[0, 1].set_title('Q–Q Plot of Residuals')

# 3. Scale-Location (homoscedasticity check)
axes[1, 0].scatter(fitted, np.sqrt(np.abs(std_resid)), alpha=0.5)
axes[1, 0].set_xlabel('Fitted Values')
axes[1, 0].set_ylabel('√|Standardized Residuals|')
axes[1, 0].set_title('Scale-Location')

# 4. Histogram of residuals
axes[1, 1].hist(residuals, bins=20, edgecolor='black', color='steelblue')
axes[1, 1].set_xlabel('Residuals')
axes[1, 1].set_title('Distribution of Residuals')

plt.tight_layout()
plt.show()
```

### Reading the Diagnostic Plots

| Plot | Good Sign | Warning Sign |
| ---------------------- | --------------------------------- | ------------------------------------- |
| **Residuals vs Fitted** | Random scatter around 0 | Curved pattern (non-linearity); funnel shape (heteroscedasticity) |
| **Q–Q Plot** | Points fall on the diagonal line | Heavy tails or S-curve (non-normality) |
| **Scale-Location** | Flat horizontal band | Upward/downward trend (unequal variance) |
| **Residuals Histogram** | Approximately bell-shaped | Skewed; multiple peaks |

## Visualization: Regression Line

```python
import seaborn as sns

sns.regplot(
    x='sepal_length',
    y='petal_length',
    data=df,
    scatter_kws={'alpha': 0.5},
    line_kws={'color': 'red'}
)
plt.title(f'Simple Linear Regression  (R² = {model.rsquared:.3f})')
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Petal Length (cm)')
plt.show()
```

Tip: The shaded band around the regression line is the 95% confidence interval for the mean prediction. A wider band indicates more uncertainty — usually at the extremes of X.

## Confidence Interval vs. Prediction Interval

These are related but not interchangeable:

| Interval | Answers |
| -------- | ------- |
| **Confidence interval for the mean** | Where is the true regression line likely to be at this X? |
| **Prediction interval** | Where is a new individual observation likely to fall at this X? |

Prediction intervals are always wider because they include both:

1. uncertainty about the fitted line
2. irreducible observation-level noise

```python
new_data = pd.DataFrame({'sepal_length': [5.0, 6.0, 7.0]})
pred_frame = model.get_prediction(new_data).summary_frame(alpha=0.05)

print(pred_frame[[
    'mean',
    'mean_ci_lower', 'mean_ci_upper',
    'obs_ci_lower',  'obs_ci_upper'
]].round(3))
```

Tip: If the model will be used for forecasting individual outcomes, the prediction interval is usually the more honest quantity to communicate.

## Making Predictions

```python
# Predict petal length for new sepal lengths
new_data = pd.DataFrame({'sepal_length': [5.0, 6.0, 7.0]})
predictions = model.predict(new_data)

for sl, pl in zip(new_data['sepal_length'], predictions):
    print(f"Sepal length = {sl} cm → Predicted petal length = {pl:.2f} cm")
```

Warning: Extrapolation warning: Do not use the model to predict Y for X values ​​far outside the range of your training data.

## Influence and Leverage

Not all observations affect the regression line equally.

| Concept | Meaning |
| ------- | ------- |
| **Leverage** | An observation has an unusual X value |
| **Influence** | Removing the observation would noticeably change the fitted model |

High leverage is not automatically bad. It becomes a problem when a high-leverage point also has a large residual and ends up pulling the regression line disproportionately.

```python
influence = model.get_influence()
influence_frame = influence.summary_frame()

print(influence_frame[['hat_diag', 'cooks_d']].head())
```

Tip: A good diagnostic workflow is: first look at residual plots, then inspect leverage and Cook's distance for points that may be driving the fit.

## Key Takeaways

| Concept | Key Point |
| ------------------------ | ----------------------------------------------------------------------------- |
| **OLS goal** | Minimize sum of squared residuals — finds the best-fit line |
| **Slope interpretation** | One-unit increase in X → β₁-unit change in Y (holding everything else constant) |
| **R²** | Proportion of variance in Y explained by X — higher is better, but context matters |
| **Assumptions** | Check residual plots AFTER fitting — assumptions apply to residuals, not raw data |
| **Extrapolation** | Never predict beyond the range of your observed data |
| **Causation** | Regression ≠ causation — association only |
