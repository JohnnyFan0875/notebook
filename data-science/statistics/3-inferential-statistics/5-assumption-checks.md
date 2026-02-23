# 5. Assumption Checks

Before running any parametric test (t-test, ANOVA, regression), you must verify that its assumptions hold. Skipping this step can produce invalid p-values, inflated Type I errors, or misleading conclusions.

> 📌 **核心原則**：先檢查假設，再跑檢定。假設違反時，優先考慮資料轉換（log、Box–Cox），或改用無母數方法。

---

## 5.0 The Three Core Assumptions

| Assumption         | Required By                  | Check Method                           | If Violated                        |
| ------------------ | ---------------------------- | -------------------------------------- | ---------------------------------- |
| **Normality**      | t-tests, ANOVA               | Shapiro–Wilk, Q–Q plot                 | Transform data / use non-parametric|
| **Equal Variance** | Student's t-test, one-way ANOVA | Levene's / Bartlett's test          | Welch's t-test / Welch's ANOVA     |
| **Independence**   | All parametric tests         | Study design / Durbin–Watson / Runs test | Paired tests, mixed models, ARIMA |

> 💡 **Practical order of checking**: Independence → Normality → Equal Variance.  
> Independence is a design issue — if violated, the other checks are moot.

---

## 5.1 Normality Tests

Normality tests assess whether a dataset is drawn from a normally distributed population.

**Hypotheses:**
- **H₀**: Data are normally distributed.
- **Hₐ**: Data are not normally distributed.

### Visual Checks (Always Start Here)

Visual inspection should always precede formal tests — they reveal shape, skewness, and outliers that a single p-value can't communicate.

#### Histogram

```python
import matplotlib.pyplot as plt

plt.hist(data, bins=10, edgecolor='black')
plt.title('Histogram')
plt.show()
```

#### Q–Q (Quantile–Quantile) Plot

Compares sample quantiles against theoretical normal quantiles. Points should lie on the 45° line.

```python
import scipy.stats as stats
import matplotlib.pyplot as plt

stats.probplot(data, dist="norm", plot=plt)
plt.title('Q–Q Plot')
plt.show()
```

**Interpretation:**

| Pattern in Q–Q plot          | Meaning                     |
| ---------------------------- | --------------------------- |
| Points follow the line       | Approximately normal        |
| Curved tails (bow shape)     | Skewness                    |
| S-shaped curve               | Heavy or light tails        |
| Points diverge at both ends  | Outliers or non-normality   |

### Shapiro–Wilk Test

Recommended for small to moderate samples (n ≤ 2000). Compares the order statistics of the sample to those expected under normality.

```python
from scipy import stats

statistic, p_value = stats.shapiro(data)
print(f"Shapiro–Wilk: W={statistic:.4f}, p={p_value:.4f}")
```

| p-value       | Interpretation                               |
| ------------- | -------------------------------------------- |
| **p > 0.05**  | Fail to reject H₀ → approximately normal     |
| **p ≤ 0.05**  | Reject H₀ → data deviate from normality      |

> ⚠️ **Large sample caution**: For n > 200, Shapiro–Wilk will almost always reject normality even for trivially small deviations. With large n, CLT usually applies — prioritize visual checks over p-values.

### Kolmogorov–Smirnov Test

Compares the empirical distribution to a reference distribution. More suitable for large samples; apply the Lilliefors correction when estimating mean and variance from data.

```python
import numpy as np
from scipy import stats

statistic, p_value = stats.kstest(data, 'norm', args=(np.mean(data), np.std(data, ddof=1)))
print(f"K–S: statistic={statistic:.4f}, p={p_value:.4f}")
```

### Anderson–Darling Test

More powerful than K–S; gives extra weight to deviations in the **tails**. Useful when tail behavior matters (e.g., extreme-value analysis).

```python
from scipy import stats

result = stats.anderson(data, dist='norm')
print(f"Statistic: {result.statistic:.4f}")
for sl, cv in zip(result.significance_level, result.critical_values):
    print(f"  α={sl}%: critical value={cv:.4f}  →  {'Reject H₀' if result.statistic > cv else 'Fail to reject H₀'}")
```

If **statistic > critical value** at a given significance level → reject H₀.

### Summary: Which Normality Test to Use?

| Test               | Recommended For          | Key Feature                          |
| ------------------ | ------------------------ | ------------------------------------ |
| Histogram          | Any n                    | Intuitive shape inspection           |
| Q–Q Plot           | Any n                    | Best for spotting tail deviations    |
| Shapiro–Wilk       | n ≤ 2000                 | Best power for small samples         |
| Kolmogorov–Smirnov | Large n (general-purpose)| Compares empirical vs. theoretical CDF |
| Anderson–Darling   | Any n                    | Extra sensitivity to tail deviations |

### If Normality is Violated

1. **Transform the data**: `log(x)`, `sqrt(x)`, or Box–Cox transformation.
2. **Use non-parametric tests**: Mann–Whitney U, Wilcoxon signed-rank, Kruskal–Wallis.
3. **Rely on CLT**: For n ≥ 30, minor deviations from normality are often acceptable.

---

## 5.2 Variance Tests (Homoscedasticity)

Equal variance (homoscedasticity) means variance is constant across groups. Required by Student's t-test and one-way ANOVA.

**Hypotheses:**
- **H₀**: Variances across all groups are equal.
- **Hₐ**: At least one group has a different variance.

### Levene's Test

Robust to non-normality. **Preferred default** when you're unsure about the distributional shape.

```python
from scipy import stats

statistic, p_value = stats.levene(group1, group2, group3)
print(f"Levene's: stat={statistic:.4f}, p={p_value:.4f}")
```

### Bartlett's Test

More statistically powerful when data **are** normally distributed, but sensitive to departures from normality.

```python
statistic, p_value = stats.bartlett(group1, group2, group3)
print(f"Bartlett's: stat={statistic:.4f}, p={p_value:.4f}")
```

### Brown–Forsythe Test

Uses the **median** instead of the mean to compute deviations — more robust than Levene's when data are skewed or contain outliers.

```python
from pingouin import homoscedasticity
import pandas as pd

df = pd.DataFrame({
    "group": ["A"]*5 + ["B"]*5 + ["C"]*5,
    "value": [20,22,21,19,23, 30,29,31,32,28, 15,17,16,14,18]
})

result = homoscedasticity(df, dv="value", group="group", method="bf")
print(result)
```

### Summary: Which Variance Test to Use?

| Test             | When to Use                                       |
| ---------------- | ------------------------------------------------- |
| Levene's         | Default; robust when normality is uncertain       |
| Bartlett's       | Data are confirmed approximately normal           |
| Brown–Forsythe   | Data are skewed or contain outliers               |

**Interpretation (all three tests):**

| p-value       | Interpretation                                               |
| ------------- | ------------------------------------------------------------ |
| **p > 0.05**  | Fail to reject H₀ → variances are equal (homoscedastic)     |
| **p ≤ 0.05**  | Reject H₀ → variances differ → use Welch's variant          |

### If Variances are Unequal

- For two groups → use **Welch's t-test** (`equal_var=False` in scipy)
- For three or more groups → use **Welch's ANOVA** (`pingouin.welch_anova`)

---

## 5.3 Independence Tests

Independence means that the outcome of one observation does not influence another. It is a **design assumption** — the most fundamental of the three.

**Hypotheses (for residual-based tests):**
- **H₀**: Observations (or residuals) are independent.
- **Hₐ**: Observations are correlated / autocorrelated.

### Common Sources of Non-Independence

| Source                   | Example                                         |
| ------------------------ | ----------------------------------------------- |
| Repeated measures        | Before/after measurements on the same subjects  |
| Clustered data           | Patients nested within hospitals                |
| Time-series correlation  | Daily measurements of the same variable         |
| Spatial correlation      | Sensor readings from geographically close sites |

### Design-Based Independence (Best Approach)

Independence is best guaranteed by **random sampling** and **random assignment** — not by a statistical test. If your study design is sound, this assumption is met by construction.

### Durbin–Watson Test (Autocorrelation in Residuals)

Tests for serial correlation in residuals of regression or time-series models.

```python
from statsmodels.stats.stattools import durbin_watson
import statsmodels.api as sm

X = sm.add_constant([1, 2, 3, 4, 5])
y = [2, 4, 5, 4, 5]
model = sm.OLS(y, X).fit()

dw = durbin_watson(model.resid)
print(f"Durbin–Watson: {dw:.4f}")
```

| DW Value | Interpretation           |
| -------- | ------------------------ |
| ≈ 2      | No autocorrelation ✅    |
| < 2      | Positive autocorrelation |
| > 2      | Negative autocorrelation |

### Runs Test (Randomness of Residuals)

Tests whether a sequence of residuals or binary outcomes is random.

```python
from statsmodels.sandbox.stats.runs import runstest_1samp
import numpy as np

residuals = np.array([0.5, -0.2, 0.1, -0.4, 0.3, -0.1])
stat, p_value = runstest_1samp(residuals)
print(f"Runs test: stat={stat:.4f}, p={p_value:.4f}")
```

| p-value       | Interpretation                                       |
| ------------- | ---------------------------------------------------- |
| **p > 0.05**  | Fail to reject H₀ → sequence is random (independent) |
| **p ≤ 0.05**  | Reject H₀ → residuals show non-random pattern        |

### If Independence is Violated

| Cause                   | Remedy                                               |
| ----------------------- | ---------------------------------------------------- |
| Repeated measures       | Paired t-test, Wilcoxon signed-rank, mixed models    |
| Clustered data          | Multilevel models, GEE (Generalized Estimating Equations) |
| Time-series correlation | ARIMA or time-series regression models               |
| Spatial correlation     | Spatial autocorrelation models (Moran's I)           |

---

## 5.4 Full Pre-Test Checklist

Use this checklist before running any parametric test:

```
□ 1. Independence
      - Random sampling / random assignment used?
      - If time-series or repeated measures: run Durbin–Watson or Runs test

□ 2. Normality (per group)
      - Visual: histogram + Q–Q plot
      - Formal: Shapiro–Wilk (n ≤ 2000) or Anderson–Darling
      - n ≥ 30? CLT may compensate for mild violations

□ 3. Equal Variance (for 2+ group comparisons)
      - Run Levene's test (default) or Bartlett's (if confirmed normal)
      - p ≤ 0.05? → use Welch's variant

□ 4. Outcome variable is continuous (for t-tests / ANOVA)
      - Ordinal or non-continuous? → consider non-parametric tests
```

---

## 5.5 t-score and z-score Reference

Both standardize how far a sample mean $\bar{x}$ is from a hypothesized population mean $\mu$, measured in units of standard error (SE).

### z-score (population σ known)

$$z = \frac{\bar{x} - \mu}{\sigma / \sqrt{n}}$$

**Use when**: n ≥ 30 and population standard deviation σ is known.

### t-score (population σ unknown)

$$t = \frac{\bar{x} - \mu}{s / \sqrt{n}}$$

**Use when**: σ is unknown (the typical case). Uses sample SD $s$.  
The t-distribution has heavier tails than normal to account for the added uncertainty from estimating σ. As n → ∞, t → z.

### Critical Values by Test Type

| Test Type                    | Formula                               | 95% Example           |
| ---------------------------- | ------------------------------------- | --------------------- |
| **Two-tailed** (default)     | `stats.norm.ppf(1 - α/2)`            | ±1.96                 |
| **Right-tailed** (μ > μ₀)    | `stats.norm.ppf(1 - α)`              | +1.645                |
| **Left-tailed** (μ < μ₀)     | `stats.norm.ppf(α)`                  | −1.645                |

```python
from scipy import stats

alpha = 0.05
z_two   = stats.norm.ppf(1 - alpha/2)   # ±1.96
z_right = stats.norm.ppf(1 - alpha)     # +1.645
z_left  = stats.norm.ppf(alpha)         # -1.645

t_crit = stats.t.ppf(1 - alpha/2, df=29)  # for n=30, two-tailed
```

### When to Use t vs. z

| Condition                         | Use    |
| --------------------------------- | ------ |
| σ known, n ≥ 30                   | z-test |
| σ unknown (almost always)         | t-test |
| n → large, σ unknown              | t-test (converges to z automatically) |

> 💡 **Default rule**: Always use t. It is always valid and converges to z for large n.

---

## 5.6 Key Takeaways

| Assumption       | Default Test       | Fallback if Violated               |
| ---------------- | ------------------ | ---------------------------------- |
| Independence     | Study design       | Paired tests / mixed models        |
| Normality        | Shapiro–Wilk + Q–Q | Log transform / non-parametric     |
| Equal variance   | Levene's test      | Welch's t-test / Welch's ANOVA     |

> **Core message**: Checking assumptions is not a formality — it is what makes your conclusions valid. A test that doesn't meet its assumptions may still produce a p-value, but that p-value cannot be trusted.

---

**← Previous:** [Common Statistical Tests](./4-statistical-tests.md)  
**↑ Back to:** [Inferential Statistics – README](./README.md)
