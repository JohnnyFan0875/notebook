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

## 1. Visual Inspection

Visual checks should always precede formal tests — they provide intuition and help detect outliers, skewness, or heavy tails that might not show up in numerical p-values.

### Histogram

- Shows overall shape and symmetry.
- A roughly bell-shaped curve suggests approximate normality.

```python
import matplotlib.pyplot as plt

plt.hist(data, bins=10, edgecolor='black')
plt.title('Histogram of Sample Data')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()
```

### Q–Q (Quantile–Quantile) Plot

- Compares sample quantiles to theoretical normal quantiles.
- Points should lie roughly on the 45° line if data are normally distributed.
- [seaborn Q-Q Plot](../../../../visualization/seaborn/regression.md#quantile-quantile-qq-plot)

```python
import scipy.stats as stats
import matplotlib.pyplot as plt

stats.probplot(data, dist="norm", plot=plt)
plt.title('Q–Q Plot for Normality Check')
plt.show()
```

Interpretation:

- Curved tails → skewness or heavy tails.
- S-shaped pattern → deviation from normality.

## 2. Shapiro–Wilk Test

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

## 3. Kolmogorov–Smirnov Test

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

## 4. Anderson–Darling Test

- **Purpose:** A more powerful test than K–S, giving extra weight to deviations in the tails.
- **Recommended for:** Small to moderate samples; widely used in applied sciences.
- **Null hypothesis (H₀):** Data follow a normal distribution.

### Python Example

```python
from scipy import stats

result = stats.anderson(data, dist='norm')
print(f"Statistic: {result.statistic}")
print("Critical values:", result.critical_values)
print("Significance levels:", result.significance_level)
```

### Interpretation

If the **test statistic > critical value** at a given significance level → reject H₀ (data are not normal).

Example output:

```
Statistic: 0.421
Critical values: [0.547, 0.622, 0.744, 0.866, 1.010]
Significance levels: [15., 10., 5., 2.5, 1.]
```

Here, 0.421 < 0.744 (5% level), so we **fail to reject H₀** → data are approximately normal.

## 5. Summary of Tests

| Type            | Test               | Recommended Sample Size  | Key Feature                  | Sensitive To                   |
| --------------- | ------------------ | ------------------------ | ---------------------------- | ------------------------------ |
| **Visual**      | Histogram          | Any                      | Simple shape inspection      | Skewness, outliers             |
| **Visual**      | Q–Q Plot           | Any                      | Compares quantiles visually  | Tails and asymmetry            |
| **Statistical** | Shapiro–Wilk       | n ≤ 2000                 | Compares order statistics    | Non-normality in small samples |
| **Statistical** | Kolmogorov–Smirnov | Any (better for large n) | Empirical vs theoretical CDF | Global deviations              |
| **Statistical** | Anderson–Darling   | Any                      | Weighted toward tails        | Tail deviations                |

## Practical Guidelines

- **Start with visual checks (histogram + Q–Q plot)** — they reveal shape and outliers.
- **Confirm with a statistical test** (Shapiro–Wilk for small n; Anderson–Darling for extra sensitivity).
- **For large samples (n ≥ 30)**, small deviations are often acceptable due to CLT.
- **If normality is violated:**

  - Apply a **transformation** (log, square-root, Box–Cox), or
  - Use **non-parametric tests** (Mann–Whitney, Kruskal–Wallis).
