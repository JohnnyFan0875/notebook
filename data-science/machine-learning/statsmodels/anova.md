# Statsmodels: ANOVA (Analysis of Variance)

Analysis of Variance (ANOVA) tests whether the means of two or more groups are significantly different. It is commonly used when comparing treatments, categories, or experimental conditions.

## Import and Setup

```python
import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
```

## One-Way ANOVA

**Example:** test if three groups have different means.

```python
# Example dataset
df = pd.DataFrame({
    'score': [5, 6, 7, 8, 5, 6, 7, 6, 7],
    'group': ['A','A','A','B','B','B','C','C','C']
})

# Fit linear model
model = ols('score ~ C(group)', data=df).fit()

# Perform ANOVA
table = anova_lm(model, typ=2)
print(table)
```

- `C(group)`: tells statsmodels that `group` is categorical.
- `anova_lm`: generates ANOVA table (Sum of Squares, df, F-statistic, p-value).

**Interpretation:**

- If p-value < 0.05 → reject null hypothesis, group means are significantly different.

## Two-Way ANOVA

**Example:** include two categorical factors and their interaction.

```python
# Example dataset
df = pd.DataFrame({
    'score': [5,6,7,8,6,7,9,5,6,8,7,9],
    'treatment': ['A','A','A','A','B','B','B','B','C','C','C','C'],
    'gender':    ['M','F','M','F','M','F','M','F','M','F','M','F']
})

# Fit two-way ANOVA model with interaction
model = ols('score ~ C(treatment) * C(gender)', data=df).fit()

# Perform ANOVA
table = anova_lm(model, typ=2)
print(table)
```

- `*` includes both main effects and the interaction between treatment and gender.
- The ANOVA table shows whether each factor and the interaction are significant.

## ANCOVA (Analysis of Covariance)

ANCOVA tests group differences while controlling for continuous covariates.

```python
# Example dataset
df = pd.DataFrame({
    'score': [10,12,13,15,14,16,17,18],
    'treatment': ['A','A','B','B','C','C','C','C'],
    'age': [23,25,22,30,28,26,29,31]
})

# Fit ANCOVA model (treatment = categorical, age = covariate)
model = ols('score ~ C(treatment) + age', data=df).fit()

# Perform ANOVA
table = anova_lm(model, typ=2)
print(table)
```

- `C(treatment)`: categorical treatment variable.
- `age`: continuous covariate.
- The ANOVA table separates treatment effect from age effect.

## Key Notes

- `anova_lm(model, typ=2)` → Type II sums of squares (commonly used).
  Other options: `typ=1` (sequential), `typ=3` (marginal).
- ANOVA assumes: normality, homogeneity of variances, independence.
- For post-hoc comparisons (pairwise group tests), use `statsmodels.stats.multicomp.pairwise_tukeyhsd`.

## Key Takeaways

- **One-way ANOVA**: compare means across multiple groups.
- **Two-way ANOVA**: include two categorical factors and their interaction.
- **ANCOVA**: include categorical factors and adjust for continuous covariates.
- Statsmodels makes it easy via `ols()` for model fitting and `anova_lm()` for hypothesis testing.
