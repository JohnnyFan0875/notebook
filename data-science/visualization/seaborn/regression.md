# Seaborn: Regression Plots

Regression plots in Seaborn allow visualization of relationships between variables along with fitted regression models and diagnostic checks. Common functions include **regplot**, **residplot**, and **lmplot**.

---

## Import Packages and Example Dataset

```python
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Example dataset: Iris
iris = sns.load_dataset("iris")
```

---

## Basic Regression Plot

```python
sns.regplot(x="sepal_length", y="petal_length", data=iris)
plt.title("Regression Plot: Sepal vs Petal Length")
plt.show()
```

- Adds a linear regression line with a 95% confidence interval (default).
- `ci=None`: removes confidence interval.
- `order=n`: fits a polynomial regression of order _n_.

---

## Logistic Regression

If the dependent variable is binary, set `logistic=True`.

```python
# Example dataset: Tips
tips = sns.load_dataset("tips")

sns.regplot(x="total_bill", y="smoker", data=tips, logistic=True, ci=None)
plt.title("Logistic Regression Example")
plt.show()
```

- Fits a logistic regression curve.
- Useful for binary classification relationships.

## Residual Plot

Residual plots help assess model fit.

```python
sns.residplot(x="sepal_length", y="petal_length", data=iris, lowess=True)
plt.xlabel("Fitted values (Sepal Length)")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.show()
```

- `lowess=True`: adds a locally weighted smoothing line.
- Ideally, residuals should be randomly scattered around 0.

## Quantile-Quantile (QQ) Plot

For normality checks, QQ plots compare residual quantiles to a normal distribution.

```python
import statsmodels.api as sm

model = sm.OLS(iris["petal_length"], sm.add_constant(iris["sepal_length"])).fit()
sm.qqplot(model.resid, line="45")
plt.title("QQ Plot of Residuals")
plt.show()
```

- If residuals follow a straight line, normality assumption holds.

## Scale-Location Plot

- **Purpose**: Displays fitted values (x-axis) vs. square root of standardized residuals (y-axis).
- **Homoscedasticity Check**: The red line should be roughly horizontal, indicating constant variance across fitted values.
- **Definition**: Homoscedasticity means equal or similar variances across different groups.
- **Residual Pattern**: Residuals should be randomly scattered around the red line with roughly equal variability at all fitted values.

```python
model_norm_residuals = model.get_influence().resid_studentized_internal
model_norm_residuals_abs_sqrt = np.sqrt(np.abs(model_norm_residuals))

sns.regplot(x=model.fittedvalues,
            y=model_norm_residuals_abs_sqrt,
            ci=None,
            lowess=True)

plt.xlabel("Fitted values")
plt.ylabel("Sqrt(|Standardized Residuals|)")
plt.title("Scale-Location Plot")
plt.show()
```

- Red line should be roughly horizontal if variance is constant.

---

## LM Plot

`lmplot` is a higher-level interface combining regression plots with FacetGrid.

```python
sns.lmplot(x="sepal_length", y="petal_length",
           data=iris, hue="species", ci=None)
plt.title("LM Plot by Species")
plt.show()
```

- Similar to `regplot`, but supports faceting with `col`/`row`.
- Use `hue` for subgroup regression lines.

---

## Key Takeaways

- `regplot`: basic regression fits (linear, polynomial, logistic).
- `residplot`: visualize residuals for model diagnostics.
- `lmplot`: regression fits across multiple facets/groups.
- Supplement with **QQ plots** and **Scale-Location plots** for deeper diagnostic checks.
- Useful for both **exploring relationships** and **validating assumptions**.
