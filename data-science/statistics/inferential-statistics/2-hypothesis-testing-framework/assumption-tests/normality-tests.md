# Normality Tests

Normality tests assess whether a dataset is drawn from a normally distributed population.  
This assumption is critical for **parametric tests** such as t-tests and ANOVA.

## Why Important?

- Many parametric tests assume the data (or residuals) follow a **normal distribution**.
- Violating this assumption can:
  - Affect the validity of p-values.
  - Inflate **Type I** or **Type II** error rates.
- For large samples (n ≥ 30), the [Central Limit Theorem (CLT)](./README.md#general-notes) often compensates for minor non-normality.

## Hypotheses

- **Null hypothesis (H₀):** Data are normally distributed.
- **Alternative hypothesis (Hₐ):** Data are not normally distributed.

## Shapiro–Wilk Test

- **Purpose:** Tests whether a sample comes from a normally distributed population.
- **Recommended for:** Small to moderate sample sizes (n ≤ 2000).
- **Basis:** Compares the order statistics of the sample to those expected under normality.

### Python Example

```python
from scipy import stats

data = [12.1, 12.4, 12.6, 12.8, 13.0, 13.1, 13.5]
statistic, p_value = stats.shapiro(data)
print("Shapiro–Wilk test statistic:", statistic)
print("p-value:", p_value)
```

### Interpretation

| p-value      | Interpretation                                     |
| ------------ | -------------------------------------------------- |
| **p > 0.05** | Fail to reject H₀ → data are approximately normal. |
| **p ≤ 0.05** | Reject H₀ → data deviate from normality.           |

## Kolmogorov–Smirnov Test

- **Purpose:** Compares the **empirical distribution** of a sample with a **reference (normal) distribution**.
- **Recommended for:** Larger samples or as a general-purpose goodness-of-fit test.
- **Note:** Use with caution — when mean and variance are estimated from data, apply the **Lilliefors correction** (available in `statsmodels`).

### Python Example

```python
from scipy import stats
import numpy as np

data = np.random.normal(loc=0, scale=1, size=50)
statistic, p_value = stats.kstest(data, 'norm', args=(np.mean(data), np.std(data, ddof=1)))
print("Kolmogorov–Smirnov test statistic:", statistic)
print("p-value:", p_value)
```

### Interpretation

| p-value      | Interpretation                                                      |
| ------------ | ------------------------------------------------------------------- |
| **p > 0.05** | Fail to reject H₀ → data are consistent with a normal distribution. |
| **p ≤ 0.05** | Reject H₀ → data significantly deviate from normality.              |

## Summary

| Test                   | Recommended Sample Size  | Key Feature                           | Sensitive To                          |
| ---------------------- | ------------------------ | ------------------------------------- | ------------------------------------- |
| **Shapiro–Wilk**       | n ≤ 2000                 | Compares order statistics             | Non-normality in small samples        |
| **Kolmogorov–Smirnov** | Any (better for large n) | Compares empirical vs theoretical CDF | Deviations in cumulative distribution |

## 📌 Guidelines

- Use Shapiro–Wilk for small samples.
- Use K–S test for larger samples or to compare any distribution.
- For visual confirmation, pair with a [Q–Q plot](../../visualization/seaborn/regression.md#quantile-quantile-qq-plot) or histogram.
- If normality is violated → use non-parametric tests (e.g., Mann–Whitney, Kruskal–Wallis).
