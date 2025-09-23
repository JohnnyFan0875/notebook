# Power and Effect Size

Statistical **power** and **effect size** are key components of hypothesis testing.  
They complement significance testing (p-values, α) by quantifying the ability to detect true effects and the size of those effects.

## Power of a Test

- **Definition:** Probability of correctly rejecting the null hypothesis when it is false (detecting a true effect).
- **Formula:**  
  \[
  \text{Power} = 1 - \beta
  \]  
  where \(\beta\) = probability of a **Type II error** (failing to reject a false null).

- **Typical target:** 0.80 (80%) → means an 80% chance of detecting a true effect if it exists.

- **Determinants of power:**
  - Sample size (\(n\)) ↑ → power ↑
  - Effect size ↑ → power ↑
  - Significance level (α) ↑ → power ↑ (but increases Type I error risk)
  - Variability (σ or s) ↓ → power ↑

📌 **Key Point:** Increasing sample size improves power but does **not** change the true effect size.

### Example in Python

```python
from statsmodels.stats.power import TTestIndPower

# Initialize power analysis
power_analysis = TTestIndPower()

# Calculate power
power = power_analysis.solve_power(effect_size=0.5, nobs1=30, alpha=0.05)

print(f"Power: {power:.3f}")
```

## Effect Size

- **Definition:** A measure of how large or meaningful an effect is, beyond just statistical significance.
- Statistical significance tells us _whether_ an effect exists, while effect size tells us _how big_ that effect is.

### Key Points

- A **larger effect size** makes it easier to detect a true effect → smaller sample sizes needed.
- **Statistically significant + small effect size:**
  - A real difference exists, but the magnitude is small.
  - May have limited practical or real-world importance (sometimes due to very large sample size).
- **Not statistically significant + large effect size:**
  - The difference or relationship is meaningful, but the test fails to detect it.
  - Often due to small sample size, high variability, or low statistical power.
- Larger sample sizes, larger effect sizes, and higher α increase power.

### Common Measures of Effect Size

1. **Cohen’s d (two groups, mean difference):**

\[
d = \frac{\bar{x}\_1 - \bar{x}\_2}{s_p}
\]

where \(s_p\) is the pooled standard deviation.

- Small ≈ 0.2
- Medium ≈ 0.5
- Large ≈ 0.8

2. **Pearson’s r (correlation strength):**

\[
r = \frac{\text{Cov}(X,Y)}{\sigma_X \sigma_Y}
\]

- Small ≈ 0.1
- Medium ≈ 0.3
- Large ≈ 0.5

3. **Eta squared (η²) (ANOVA, variance explained):**

\[
\eta^2 = \frac{SS*{\text{between}}}{SS*{\text{total}}}
\]

- Small ≈ 0.01
- Medium ≈ 0.06
- Large ≈ 0.14

### Example in Python

```python
import numpy as np

# Cohen's d example
group1 = np.array([23, 21, 19, 22, 20])
group2 = np.array([30, 28, 29, 32, 31])

mean_diff = np.mean(group1) - np.mean(group2)
pooled_std = np.sqrt(((len(group1)-1)*np.var(group1, ddof=1) +
                      (len(group2)-1)*np.var(group2, ddof=1)) /
                      (len(group1)+len(group2)-2))

cohens_d = mean_diff / pooled_std
print("Cohen's d:", cohens_d)
```
