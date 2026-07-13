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

## Interview Fast Answer

如果面試官問 linear regression 是什麼，通常不需要一開始就展開 OLS 推導。

先講到這個程度通常就夠高訊號：

- linear regression 用一條線描述 `X` 和連續型 `Y` 的關係
- `β₁` 表示 `X` 每增加一單位，`Y` 平均改變多少
- 它回答的是 association / prediction，不自動代表 causation

常見追問則是：

- assumptions 有哪些
- `R²` 在說什麼
- 係數的正負與大小怎麼解讀

## What "Linear" Actually Means

In regression, **linear** means **linear in the parameters** (`\beta_0`, `\beta_1`, ...), not necessarily that the raw input-output relationship always looks like a perfect straight line before any feature engineering.

These are still linear models:

\[
Y = \beta_0 + \beta_1 X + \varepsilon
\]

\[
Y = \beta_0 + \beta_1 X + \beta_2 X^2 + \varepsilon
\]

because the coefficients enter additively and are not multiplied by each other.

This is **not** linear in the parameters:

\[
Y = \beta_0 + e^{\beta_1 X}
\]

because the coefficient is inside a nonlinear transformation.

Key point: A polynomial regression can still belong to the linear-model family if it is linear in the coefficients. This matters because many linear-model tools and interpretations extend to transformed features.

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

### Interview Prompt: How Do You Explain R-squared?

一個很穩的短答可以是：

- `R²` 是模型解釋了多少 `Y` 的變異
- 它是 fit 指標，不是因果強度指標
- `R²` 高不代表模型就合理，還要看 residual diagnostics 和外部驗證

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

## Common Interview Traps

- 把 regression coefficient 解讀成 causation
- 只報 `R²`，不檢查 residual pattern
- 說 assumptions 是對 `X` 或 `Y` 原始值本身，而不是對 residuals
- 以為 p-value 小就代表模型一定好用

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

## R Workflow: `lm()`, `predict()`, `fitted()`, `residuals()`

If you are working in R, the basic simple-regression workflow is compact and very teachable:

```r
mdl_mass_vs_length <- lm(mass_g ~ length_cm, data = bream)

predict(mdl_mass_vs_length, newdata = explanatory_data)
fitted(mdl_mass_vs_length)
residuals(mdl_mass_vs_length)
```

Useful mental model:

- `predict()`: predictions for new rows
- `fitted()`: predictions for the original training rows
- `residuals()`: observed minus fitted on the training rows

This identity is worth remembering:

```text
response = fitted value + residual
```

In other words, the model splits each observed value into:

- the part explained by the line
- the leftover part the line did not explain

## R Workflow: `broom`

`summary(lm_object)` is useful, but `broom` becomes more practical once you want tidy outputs that can be piped or joined.

```r
library(broom)

tidy(mdl_mass_vs_length)
glance(mdl_mass_vs_length)
augment(mdl_mass_vs_length)
```

Typical roles:

- `tidy()`: coefficient table
- `glance()`: one-row model summary such as `r.squared`, `adj.r.squared`, `sigma`, `AIC`, `BIC`
- `augment()`: row-level diagnostics like `.fitted`, `.resid`, `.cooksd`, `.std.resid`

This is often the cleanest R-native bridge between "fit a model" and "analyze the model output as data".

## Residual Standard Error in Practice

R reports the residual scale in `summary(lm_object)` as the residual standard error, and `broom::glance()` exposes the same idea through `sigma`.

Key point: `R²` tells you explained variance, while residual standard error tells you the typical size of the leftover error in the outcome's original units.

That distinction matters because two models can have similar `R²`, but very different practical error magnitudes depending on the scale of Y.

## Regression to the Mean

The course material is also a good reminder that the phrase "regression" historically points to **regression to the mean**, not only to fitting lines.

Core idea:

- extreme observations often contain a large random component
- when measured again, they tend to move closer to the average
- that movement can happen even without any intervention

Warning: Do not confuse an apparent improvement after an extreme baseline with a real treatment effect. Sometimes you are only seeing regression to the mean.

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
