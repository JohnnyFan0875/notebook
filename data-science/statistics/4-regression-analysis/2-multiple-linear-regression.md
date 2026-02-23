# 2. Multiple Linear Regression

Multiple linear regression extends the simple case to **two or more predictor variables**. The goal remains the same — predict Y — but now you can control for multiple factors simultaneously and assess each variable's unique contribution.

> 📌 **核心概念**：多元回歸的係數代表「在控制其他變數不變的情況下，該變數對 Y 的獨立影響」。這個「all else equal」的條件使多元回歸比簡單回歸更接近現實世界的分析需求。

---

## 2.1 The Regression Equation

$$Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \cdots + \beta_k X_k + \varepsilon$$

| Symbol          | Meaning                                                                   |
| --------------- | ------------------------------------------------------------------------- |
| $\beta_0$       | Intercept — predicted Y when all X variables equal 0                      |
| $\beta_j$       | Partial slope for $X_j$ — effect of $X_j$ on Y, **holding all other X constant** |
| $k$             | Number of predictor variables                                             |
| $\varepsilon$   | Residual / error term                                                     |

The key phrase is **"holding all other variables constant"** (ceteris paribus). This is what allows multiple regression to isolate each predictor's effect.

---

## 2.2 Python Implementation

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf
from sklearn.datasets import load_iris

iris = load_iris(as_frame=True)
df = iris.frame
df.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'target']

# Fit model with multiple predictors
model = smf.ols(
    'petal_length ~ sepal_length + sepal_width + petal_width',
    data=df
).fit()

print(model.summary())
```

**Reading the coefficient table:**

| Variable     | Coef   | Std Err | t     | p-value | Interpretation                       |
| ------------ | ------ | ------- | ----- | ------- | ------------------------------------ |
| Intercept    | −0.263 | 0.368   | −0.71 | 0.477   | Baseline (not meaningful here)       |
| sepal_length | 0.729  | 0.064   | 11.38 | <0.001  | +0.729 cm petal length per 1 cm sepal length, *controlling for others* |
| sepal_width  | −0.648 | 0.067   | −9.62 | <0.001  | −0.648 cm petal length per 1 cm sepal width, *controlling for others* |
| petal_width  | 1.447  | 0.065   | 22.27 | <0.001  | +1.447 cm petal length per 1 cm petal width, *controlling for others* |

---

## 2.3 R² vs Adjusted R²

Adding more predictors **always increases R²**, even if the new variable is meaningless. Adjusted R² penalizes unnecessary predictors.

$$R^2_{\text{adj}} = 1 - \frac{(1 - R^2)(n - 1)}{n - k - 1}$$

| Metric           | When to Use                                             | Behavior When Adding a Useless Variable |
| ---------------- | ------------------------------------------------------- | --------------------------------------- |
| **R²**           | One or a few predictors; quick measure of overall fit   | Always increases (even slightly)        |
| **Adjusted R²**  | Comparing models with **different** numbers of predictors | Decreases if the new variable doesn't help |

> 💡 **Range note**: R² is always between 0 and 1. Adjusted R² can be **negative** — this happens when the model fits worse than simply predicting the mean for every observation, which is a strong signal the model is inappropriate.

### Concrete Example

| Model   | Predictors | R²   | Adjusted R² | Verdict                                      |
| ------- | ---------- | ---- | ----------- | -------------------------------------------- |
| Model 1 | 1          | 0.80 | 0.79        | Efficient baseline                           |
| Model 2 | 10         | 0.85 | 0.75        | Higher R² is misleading — complexity hurts  |

R² favors Model 2 (0.85 > 0.80), but Adjusted R² correctly identifies Model 1 (0.79 > 0.75) as the better, more generalizable model.

```python
print(f"R²:          {model.rsquared:.4f}")
print(f"Adjusted R²: {model.rsquared_adj:.4f}")
```

---

## 2.4 Multicollinearity

**Multicollinearity** occurs when predictor variables are highly correlated with each other. This does not affect prediction accuracy but makes individual coefficient estimates **unstable and unreliable**.

### Detecting Multicollinearity: Variance Inflation Factor (VIF)

$$\text{VIF}_j = \frac{1}{1 - R^2_j}$$

where $R^2_j$ is the R² from regressing $X_j$ on all other predictors.

| VIF Value   | Interpretation                                 |
| ----------- | ---------------------------------------------- |
| 1           | No multicollinearity                           |
| 1–5         | Low — acceptable                               |
| 5–10        | Moderate — investigate                         |
| > 10        | High multicollinearity — take action           |

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

X = df[['sepal_length', 'sepal_width', 'petal_width']]
X_const = pd.DataFrame({'const': 1, **X})

vif_data = pd.DataFrame({
    'Variable': X.columns,
    'VIF': [variance_inflation_factor(X_const.values, i+1)
            for i in range(X.shape[1])]
})
print(vif_data.round(2))
```

### Dealing with Multicollinearity

| Strategy              | When to Use                                  |
| --------------------- | -------------------------------------------- |
| Remove one of the correlated variables | They measure nearly the same thing |
| Combine into a composite (e.g., PCA)  | Both carry useful information       |
| Ridge / Lasso regression              | Regularization handles it automatically |
| Collect more data                     | Sometimes stabilizes estimates      |

---

## 2.5 Categorical Predictors: Dummy Coding

Linear regression requires numerical inputs. Categorical variables must be converted to **dummy variables** (also called indicator variables or one-hot encoding).

For a variable with $k$ categories, you create $k-1$ dummy variables. The omitted category becomes the **reference group**.

```python
# pandas automatically handles this with C() notation in statsmodels
# Or use pd.get_dummies()

# Example: add species as a categorical predictor
model_cat = smf.ols(
    'petal_length ~ sepal_length + C(target)',
    data=df
).fit()
print(model_cat.summary())
```

**Interpreting dummy variable coefficients:**

If `target` has categories 0 (setosa), 1 (versicolor), 2 (virginica), and setosa is the reference:
- `C(target)[T.1]` = difference in predicted petal_length between versicolor and setosa
- `C(target)[T.2]` = difference in predicted petal_length between virginica and setosa

> ⚠️ **Dummy variable trap**: Including all $k$ dummies for a $k$-category variable causes **perfect multicollinearity** (the dummies sum to 1 = the intercept). Always use $k-1$ dummies. pandas and statsmodels handle this automatically.

---

## 2.6 Model Selection

### Information Criteria

| Criterion | Formula (simplified)                      | Prefer   | Penalizes |
| --------- | ----------------------------------------- | -------- | --------- |
| **AIC**   | $-2\ln(L) + 2k$                          | Lower    | Model complexity lightly |
| **BIC**   | $-2\ln(L) + k\ln(n)$                     | Lower    | Model complexity more heavily |

```python
print(f"AIC: {model.aic:.2f}")
print(f"BIC: {model.bic:.2f}")
```

### Stepwise Selection (Forward / Backward)

```python
# Manual backward elimination — remove highest p-value predictor iteratively
# (statsmodels does not have built-in stepwise; implement manually or use sklearn)

import statsmodels.formula.api as smf

def backward_elimination(df, target, predictors, threshold=0.05):
    while True:
        formula = f"{target} ~ {' + '.join(predictors)}"
        model = smf.ols(formula, data=df).fit()
        p_values = model.pvalues.drop('Intercept')
        max_p = p_values.max()
        if max_p > threshold:
            remove = p_values.idxmax()
            predictors.remove(remove)
            print(f"Removed: {remove} (p={max_p:.4f})")
        else:
            break
    return model

final_model = backward_elimination(
    df, 'petal_length',
    ['sepal_length', 'sepal_width', 'petal_width']
)
print(final_model.summary())
```

> 💡 **Automatic stepwise selection has limitations**: it can produce unstable models and overfit. Prefer using domain knowledge + AIC/BIC comparison, or regularization methods (Ridge, Lasso) for high-dimensional data.

---

## 2.7 Assumptions

Multiple linear regression shares all assumptions with simple linear regression, plus one additional assumption:

| # | Assumption              | Additional Notes for Multiple Regression        |
| - | ----------------------- | ----------------------------------------------- |
| 1 | Linearity               | Each $X_j$ should have a linear relationship with Y (partial regression plots help) |
| 2 | Independence            | Residuals should not be correlated with each other |
| 3 | Homoscedasticity        | Variance of residuals constant across all levels of every predictor |
| 4 | Normality of residuals  | Q–Q plot; matters less with large n (CLT)       |
| 5 | **No multicollinearity**| **New for multiple regression** — check VIF < 10 |

```python
# Diagnostic plots (same as simple regression — see Section 1.7)
fitted    = model.fittedvalues
residuals = model.resid

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].scatter(fitted, residuals, alpha=0.5)
axes[0].axhline(0, color='red', linestyle='--')
axes[0].set_xlabel('Fitted Values')
axes[0].set_ylabel('Residuals')
axes[0].set_title('Residuals vs Fitted')

from scipy import stats
stats.probplot(residuals, dist='norm', plot=axes[1])
axes[1].set_title('Q–Q Plot of Residuals')

plt.tight_layout()
plt.show()
```

---

## 2.8 Coefficient Plot (Visualizing Effect Sizes)

```python
import matplotlib.pyplot as plt

coefs = model.params.drop('Intercept')
ci    = model.conf_int().drop('Intercept')

fig, ax = plt.subplots(figsize=(7, 4))
ax.errorbar(
    x=coefs.values,
    y=coefs.index,
    xerr=[coefs - ci[0], ci[1] - coefs],
    fmt='o', color='steelblue', ecolor='gray', capsize=5
)
ax.axvline(0, color='red', linestyle='--', linewidth=1)
ax.set_xlabel('Coefficient Value')
ax.set_title('Regression Coefficients with 95% CI')
plt.tight_layout()
plt.show()
```

> 💡 If a confidence interval **crosses zero**, the predictor is **not statistically significant** at the 5% level — its true effect could be positive, negative, or zero.

---

## 2.9 Key Takeaways

| Concept                 | Key Point                                                                            |
| ----------------------- | ------------------------------------------------------------------------------------ |
| **Partial coefficient** | Represents the effect of $X_j$ holding all other predictors constant                 |
| **Adjusted R²**         | Use this (not R²) when comparing models with different numbers of predictors         |
| **Multicollinearity**   | Inflates standard errors; check VIF — if VIF > 10, take action                      |
| **Dummy coding**        | Use $k-1$ dummies for a $k$-category variable; choose reference group carefully      |
| **Model selection**     | Prefer AIC/BIC and domain knowledge over automatic stepwise methods                  |
| **Assumptions**         | Linearity, independence, homoscedasticity, normality of residuals, no multicollinearity |

---

**← Previous:** [Simple Linear Regression](./1-simple-linear-regression.md)  
**→ Next:** [Logistic Regression](./3-logistic-regression.md)
