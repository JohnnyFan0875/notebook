# Multiple Linear Regression

**Multiple linear regression** extends simple regression to model a continuous outcome as a linear function of **two or more predictors**. It is the most widely used statistical model in practice — foundational to econometrics, social science, epidemiology, and machine learning.

Key point: The core value of multiple regression: it allows you to estimate the independent effect of each predictor variable while "controlling other variables". This is the starting point for causal inference and a fundamental tool for understanding "net effect" and "confounding factors." The interpretation of each coefficient is: "With all other variables held constant, how much will the result change if this variable is increased by one unit?"

## The Model

\[
\hat{y} = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_p x_p + \varepsilon
\]

| Symbol | Name | Meaning |
| ------------ | ----------------- | ---------------------------------------------- |
| $\hat{y}$ | Fitted value | Model's predicted outcome |
| $\beta_0$ | Intercept | Expected y when all predictors = 0 |
| $\beta_j$ | Slope coefficient | Change in y per unit increase in xⱼ, **holding all other variables constant** |
| $\varepsilon$ | Error | The part of y not explained by the model |

Warning: The phrase "holding all other variables constant" is the single most important concept in multiple regression. It's what separates a partial effect from a simple correlation. Misunderstanding this leads to the most common misinterpretations of regression output. Without this condition, the meaning of the coefficient is completely different.

## Dataset

We use the **California Housing dataset** — a realistic regression problem with multiple numerical predictors.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

housing = fetch_california_housing(as_frame=True)
df = housing.frame
print(df.shape)
print(df.describe().round(2))
```

## Fitting OLS with statsmodels

Use **statsmodels** when you need full statistical output (standard errors, p-values, confidence intervals, F-test). Use **sklearn** when you need to integrate into a machine learning pipeline.

```python
import statsmodels.api as sm

# Select predictors
feature_cols = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms',
                'Population', 'AveOccup', 'Latitude', 'Longitude']
target_col   = 'MedHouseVal'

X = df[feature_cols]
y = df[target_col]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Add constant for intercept
X_train_sm = sm.add_constant(X_train)
X_test_sm  = sm.add_constant(X_test)

# Fit OLS
model = sm.OLS(y_train, X_train_sm)
result = model.fit()

print(result.summary())
```

**Key sections of the OLS summary:**

| Section | What to Check |
| --------------------- | ---------------------------------------------------------------------- |
| **R-squared** | Proportion of variance explained (0–1); higher is better |
| **Adj. R-squared** | R² penalized for number of predictors — use this for model comparison |
| **F-statistic / Prob(F)** | Overall model significance — is any predictor useful at all? |
| **coef (coefficient)** | Partial effect of each predictor |
| **P>\ | t\ | ** | Is this coefficient significantly different from zero? (< 0.05) |
| **[0.025   0.975]** | 95% confidence interval for each coefficient |
| **AIC / BIC** | Model selection criteria (lower = better) |

## Interpreting Coefficients

Coefficients only have clear interpretations when you understand the **units and scale** of each variable.

```python
# Display coefficient table with confidence intervals
coef_df = pd.DataFrame({
    'Coefficient':  result.params,
    'Std Error':    result.bse,
    't-stat':       result.tvalues,
    'p-value':      result.pvalues,
    'CI Lower':     result.conf_int()[0],
    'CI Upper':     result.conf_int()[1]
}).drop('const').round(4)

print(coef_df.sort_values('Coefficient', ascending=False).to_string())
```

**Coefficient plot — the clearest way to communicate regression results:**

```python
coefs = result.params.drop('const')
ci    = result.conf_int().drop('const')

fig, ax = plt.subplots(figsize=(8, 5))
y_pos = range(len(coefs))

ax.barh(y_pos, coefs.values,
        xerr=[(coefs.values - ci[0].values),
              (ci[1].values - coefs.values)],
        align='center', color=['tomato' if c > 0 else 'steelblue' for c in coefs],
        alpha=0.7, capsize=4)
ax.axvline(0, color='black', linewidth=1)
ax.set_yticks(y_pos)
ax.set_yticklabels(coefs.index)
ax.set_xlabel('Coefficient (with 95% CI)')
ax.set_title('OLS Coefficients — California Housing')
plt.tight_layout()
plt.show()
```

Tip: A coefficient whose 95% confidence interval does not cross zero is statistically significant at α = 0.05. The plot makes this immediately visible without reading p-values.

## Multicollinearity: VIF

Before trusting coefficient estimates, verify that predictors are not too highly correlated with each other.

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

X_vif = sm.add_constant(X_train)
vif = pd.DataFrame({
    'Feature': X_train.columns,
    'VIF':     [variance_inflation_factor(X_vif.values, i + 1)
                for i in range(len(X_train.columns))]
}).sort_values('VIF', ascending=False).round(2)

print(vif)
```

Warning: If VIF > 10 for any predictor, coefficients are unreliable. Consider: removing one of the correlated predictors, combining them (e.g., create a ratio), or switching to Ridge regression which handles multicollinearity more gracefully.

## Interaction Terms

An **interaction term** captures cases where the effect of one predictor depends on the value of another.

\[
\hat{y} = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \beta_3 (x_1 \times x_2) + \varepsilon
\]

The effect of x₁ on y is now: $\beta_1 + \beta_3 x_2$ — it changes depending on x₂.

```python
import statsmodels.formula.api as smf

# Use a subset for clarity
df_sub = df[['MedHouseVal', 'MedInc', 'HouseAge']].copy()

# Model with interaction term
model_interact = smf.ols('MedHouseVal ~ MedInc + HouseAge + MedInc:HouseAge',
                          data=df_sub).fit()
print(model_interact.summary().tables[1])
```

Tip: When to include interactions: Use interactions when you have a domain reason to believe the effect of X₁ *changes* at different levels of X₂. For example: "Does the effect of income on house value differ for older vs newer homes?" Test significance of the interaction term before including it.

## Variable Selection

With many potential predictors, choosing which to include is a key modeling decision.

### Method 1: Stepwise Selection (AIC-based)

```python
# Forward selection using AIC
def forward_selection(data, response, significance_level=None):
    """AIC-based forward selection."""
    remaining = set(data.columns) - {response}
    selected  = []
    current_aic = smf.ols(f'{response} ~ 1', data=data).fit().aic

    while remaining:
        aic_with_candidate = []
        for candidate in remaining:
            formula = f"{response} ~ {' + '.join(selected + [candidate])}"
            try:
                aic = smf.ols(formula, data=data).fit().aic
                aic_with_candidate.append((aic, candidate))
            except:
                pass
        aic_with_candidate.sort()
        best_aic, best_candidate = aic_with_candidate[0]
        if best_aic < current_aic:
            selected.append(best_candidate)
            remaining.remove(best_candidate)
            current_aic = best_aic
        else:
            break

    return selected

selected_vars = forward_selection(df[feature_cols + [target_col]], target_col)
print(f"Selected variables: {selected_vars}")
```

### Method 2: Regularization with LASSO and Ridge

LASSO (L1) and Ridge (L2) add a penalty term to the OLS loss function that shrinks coefficients toward zero.

| Method | Penalty | Effect on Coefficients | Best For |
| --------- | ----------- | ---------------------------------------------- | ------------------------------------- |
| **Ridge** | Σβⱼ² | Shrinks all coefficients proportionally | Many small predictors; multicollinearity |
| **LASSO** | Σ\ | βⱼ\ |  | Can shrink some coefficients exactly to **zero** | Automatic variable selection |
| **ElasticNet** | Mix of both | Between Ridge and LASSO | High-dimensional, correlated predictors |

```python
from sklearn.linear_model import Ridge, Lasso
from sklearn.model_selection import cross_val_score

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# LASSO — performs variable selection
lasso = Lasso(alpha=0.01, random_state=42)
lasso.fit(X_train_scaled, y_train)

coef_lasso = pd.Series(lasso.coef_, index=feature_cols)
print("LASSO coefficients (zero = excluded):")
print(coef_lasso.round(4))
print(f"\nNon-zero predictors: {(coef_lasso != 0).sum()} of {len(feature_cols)}")
```

Tip: Choosing alpha: Use cross-validation (`LassoCV`, `RidgeCV`) to select the regularization strength — don't tune alpha by hand on the test set.

## Prediction and Evaluation

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Predict on test set (using statsmodels result)
y_pred_sm = result.predict(X_test_sm)

mae  = mean_absolute_error(y_test, y_pred_sm)
rmse = np.sqrt(mean_squared_error(y_test, y_pred_sm))
r2   = r2_score(y_test, y_pred_sm)

print(f"Test MAE:  {mae:.4f}")
print(f"Test RMSE: {rmse:.4f}")
print(f"Test R²:   {r2:.4f}")

# Predicted vs actual plot
plt.figure(figsize=(7, 6))
plt.scatter(y_test, y_pred_sm, alpha=0.3, s=20, color='steelblue')
plt.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()], 'r--', linewidth=2, label='Perfect fit')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title(f'Predicted vs Actual  (Test R² = {r2:.3f})')
plt.legend()
plt.tight_layout()
plt.show()
```

Warning: Always evaluate on the test set, not training data. Training R² is always optimistic — it rewards complexity even when it doesn't generalize.

## Key Takeaways

| Concept | Key Point |
| ------------------------------------ | ----------------------------------------------------------------------------------- |
| **"All else equal" interpretation** | Every coefficient is a partial effect — its meaning depends on what else is in the model |
| **Adj. R² for model comparison** | Regular R² always increases with more predictors; adjusted R² penalizes complexity |
| **Check VIF before interpreting** | Multicollinear predictors have unstable, unreliable coefficients |
| **Interaction = conditional effect** | Include when the effect of X₁ plausibly differs across levels of X₂ |
| **LASSO for variable selection** | Shrinks unimportant coefficients exactly to zero — built-in selection |
| **Evaluate on test set** | Training R² is optimistic; test R² tells you how well the model generalizes |

## Multivariate Regression Is a Geometry Problem

With many predictors, interpretation becomes geometric:

- partial slopes depend on the full predictor space
- leverage becomes multivariate
- collinearity changes uncertainty shape

Tip: "Holding all else equal" is mathematically precise, but in real applications it may describe combinations that are rare or unrealistic.
