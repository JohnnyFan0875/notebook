# Proportion Tests

Proportion tests (z-test for proportions) are used when the data are **categorical (binomial: success/failure)** and we want to test whether a sample proportion differs from a hypothesized value, or whether two sample proportions differ.

As the sample size $n$ grows, the binomial distribution approaches a normal distribution (Central Limit Theorem).  
For small samples, use **exact tests** (Exact binomial test, Fisher’s exact test).

## One-Sample Proportion Test

- **Null hypothesis (H₀):** $p = p_0$  
  The population proportion equals the hypothesized proportion.
- **Alternative hypothesis (Hₐ):**
  - Two-tailed: $p \neq p_0$
  - Right-tailed: $p > p_0$
  - Left-tailed: $p < p_0$

**Assumption:**

$$
n\hat{p} \geq 5 \text{ or } 10 \quad \text{and} \quad n(1-\hat{p}) \geq 5 \text{ or } 10
$$

- n: Total number of observations
- $\hat{p}$: The proportion of “successes” observed in your data
- At least 5 or 10 expected “successes” and "failures"

**Python Example:**

```python
import numpy as np
from statsmodels.stats import proportion

p_0 = 0.5
count = np.array([60])   # number of successes
nobs = np.array([100])   # total sample size

z_stat, p_value = proportion.proportions_ztest(count, nobs, value=p_0)
print(z_stat, p_value)
```

## Two-Sample Proportion Test

### Hypotheses

- **Null hypothesis (H₀):** $p_1 = p_2$  
  The two population proportions are equal.

- **Alternative hypothesis (Hₐ):**
  - Two-tailed: $p_1 \neq p_2$
  - Right-tailed: $p_1 > p_2$
  - Left-tailed: $p_1 < p_2$

### Assumptions

Each group must satisfy:

$$
n_i \hat{p}\_i \geq 5 \text{ or } 10 \quad \text{and} \quad n_i (1 - \hat{p}\_i) \geq 5 \text{ or } 10
$$

### Test Statistic

$$
z = \frac{\hat{p}\_1 - \hat{p}\_2}{\sqrt{\hat{p}(1-\hat{p})\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}
$$

- $\hat{p}\_1 = x_1 / n_1$, $\hat{p}\_2 = x_2 / n_2$ → sample proportions
- $\hat{p} = (x_1 + x_2) / (n_1 + n_2)$ → pooled proportion

### Python Example

```python
import numpy as np
from statsmodels.stats import proportion

count = np.array([60, 50])   # successes in each group
nobs = np.array([100, 120])  # sample sizes for each group

z_stat, p_value = proportion.proportions_ztest(count, nobs)
print("z-statistic:", z_stat, "p-value:", p_value)
```

## Relationship to Odds Ratio

| Context / Concept                           | Measure Used                   | What It Quantifies                   | Typical Use Case                                 | Reason for Use                                                          |
| ------------------------------------------- | ------------------------------ | ------------------------------------ | ------------------------------------------------ | ----------------------------------------------------------------------- |
| **Proportion z-test / Fisher’s Exact Test** | Difference between proportions | Compares probabilities directly      | Experiments, surveys                             | Probabilities can be directly estimated from data.                      |
| **Odds Ratio (OR)**                         | Ratio of odds                  | Compares odds of outcome vs exposure | Case–control studies, logistic regression models | Probabilities cannot be directly estimated (sampling based on outcome). |

See [odds ratio](./odds-ratio.md) for details on calculation and interpretation.

## 📌 Summary

- `One-sample proportion test`: Compare a sample proportion to a hypothesized proportion.
- `Two-sample proportion test`: Compare proportions across two groups.
- For `small samples` or when assumptions fail → use binomial test or Fisher’s exact test.
- Proportion tests rely on `z-statistics` because of the normal approximation.
