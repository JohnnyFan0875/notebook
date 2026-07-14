# Hypothesis Testing Framework

**Hypothesis testing** is a formal procedure for using sample data to evaluate a claim about a population. It doesn't prove anything with certainty — it evaluates whether the evidence is strong enough to reject a specific assumption.

Key point: Core thinking: The logic of the hypothesis test is similar to the "presumption of innocence." Let's first assume "no effect" (null hypothesis), and then ask: If this hypothesis is true, how low is the chance of seeing sample data like this? If the probability is too low, we "reject the null hypothesis."

## The Logic: Proof by Contradiction

Hypothesis testing follows a logical structure borrowed from mathematics:

1. **Assume the null hypothesis (H₀) is true** — there is no effect, no difference
2. **Compute how likely the observed data is** under this assumption
3. **If the data would be very unlikely under H₀**, we have evidence against it — reject H₀
4. **If the data is reasonably likely under H₀**, we fail to reject it — not enough evidence

Warning: "Fail to reject H₀" is not the same as "prove H₀ is true." Absence of evidence ≠ evidence of absence.

## Null and Alternative Hypotheses

| Hypothesis | Symbol | Description | Example |
| ------------------------------------- | ---------- | -------------------------------------------------- | ---------------------------- |
| **Null Hypothesis** | H₀ | The default claim; assumes no effect or difference | μ = 5.0 (mean equals 5.0) |
| **Alternative Hypothesis** | H₁ (or Hₐ) | What you want to detect; the "interesting" claim | μ ≠ 5.0, μ > 5.0, or μ < 5.0 |

### One-Tailed vs. Two-Tailed Tests

| Test Type | H₁ Form | Use When |
| ---------------------- | ------- | ------------------------------------------------------------ |
| **Two-tailed** | μ ≠ μ₀ | You care about differences in **either** direction (default) |
| **One-tailed (right)** | μ > μ₀ | You only care about increases |
| **One-tailed (left)** | μ < μ₀ | You only care about decreases |

Tip: When in doubt, use two-tailed tests. One-tailed tests require a strong, pre-registered scientific reason — using them simply to get a smaller p-value is p-hacking.

## Test Statistic, Critical Region, and p-value

These three ideas are closely related but easy to blur together:

| Concept | What it is | Role |
| ------- | ---------- | ---- |
| **Test statistic** | A standardized summary computed from the sample | Converts raw data into a comparable scale |
| **Critical region** | Values extreme enough to reject H₀ at level α | Decision rule before seeing data |
| **p-value** | Tail probability beyond the observed statistic under H₀ | Data-driven measure of extremeness |

For a two-sided t-test, the logic is:

1. Compute a t-statistic.
2. Ask where it falls relative to the t-distribution under H₀.
3. Reject if it lands in the extreme tails, or equivalently if `p < alpha`.

Tip: In modern software workflows, people often skip directly to the p-value. That is fine operationally, but understanding the critical-region logic makes the meaning of the test much clearer.

## The p-value

The **p-value** is the probability of observing data as extreme as (or more extreme than) what was observed, _assuming H₀ is true_.

\[
p = P(\text{data this extreme} \mid H_0 \text{ is true})
\]

| p-value | Interpretation |
| ----------------- | ----------------------------------------------------------------------------- |
| Small (e.g. 0.01) | If H₀ were true, this result would be very rare → evidence against H₀ |
| Large (e.g. 0.40) | If H₀ were true, this result would not be surprising → no evidence against H₀ |

### Common Misconceptions About p-values

| ❌ Incorrect Interpretation | ✅ Correct Interpretation |
| ------------------------------------------------ | --------------------------------------------------------------------------- |
| p = 0.03 means H₀ has a 3% chance of being true | If H₀ were true, we'd see data this extreme only 3% of the time |
| p = 0.03 means H₁ has a 97% chance of being true | p-value says nothing about the probability of H₁ |
| p > 0.05 means there is no effect | It means we lack sufficient evidence to reject H₀ |
| A smaller p-value means a larger effect | p-value is affected by sample size; large n → small p even for tiny effects |

Warning: The p-value tells you about the compatibility of the data with H₀ — not the size or importance of the effect. Always pair with effect size and CI.

## A Better Decision Habit

Instead of asking only "Is p < 0.05?", ask four questions together:

1. What is the estimated effect?
2. How uncertain is it?
3. Is the result statistically compatible with H₀?
4. Would the effect matter in practice if it were real?

This habit prevents the common mistake of treating statistical significance as the same thing as scientific or business importance.

## Significance Level (α)

**α (alpha)** is the threshold we set _before_ looking at the data. If p < α, we reject H₀.

| Common α values | Context |
| --------------- | ---------------------------------------------------------- |
| 0.05 (5%) | Standard threshold in most fields |
| 0.01 (1%) | More stringent; medical/pharmaceutical research |
| 0.10 (10%) | Exploratory research; used when false negatives are costly |
| 0.001 (0.1%) | Physics, genomics (large-scale testing) |

Tip: α should be set before data collection, not chosen to make your results look significant. Changing α after seeing the data is a form of p-hacking.

## Statistical Significance vs. Practical Significance

These are not the same:

| Situation | Interpretation |
| --------- | -------------- |
| Small p-value, tiny effect | Real but maybe not important |
| Large p-value, moderate effect | Possibly important, but evidence too weak or sample too small |
| Small p-value, large effect | Strong evidence and likely practical relevance |
| Large p-value, tiny effect | No compelling evidence and probably low practical importance |

Tip: The goal of inference is not to collect asterisks. It is to learn whether the effect is real enough, large enough, and precise enough to act on.

## Type I and Type II Errors

Every decision in hypothesis testing carries a risk of being wrong. There are four possible outcomes:

| Outcome | True Condition | Test Result | Interpretation | Type |
| ------------------ | ---------------------- | ------------------------------------------ | ---------------------------------- | ------------------------ |
| **True Positive** | Hₐ (difference exists) | Reject H₀ (conclude difference exists) | Correctly detects a real effect | ✅ Correct |
| **False Positive** | H₀ (no difference) | Reject H₀ (conclude difference exists) | Incorrectly concludes a difference | ❌ **Type I error (α)** |
| **True Negative** | H₀ (no difference) | Fail to reject H₀ (conclude no difference) | Correctly concludes no difference | ✅ Correct |
| **False Negative** | Hₐ (difference exists) | Fail to reject H₀ (conclude no difference) | Fails to detect a real effect | ❌ **Type II error (β)** |

Summarized as a decision matrix:

|  | H₀ is actually **True** | H₀ is actually **False** |
| --------------------- | -------------------------------- | --------------------------------- |
| **Reject H₀** | ❌ Type I Error (False Positive) | ✅ Correct (True Positive) |
| **Fail to Reject H₀** | ✅ Correct (True Negative) | ❌ Type II Error (False Negative) |

| Error Type | Symbol | Probability | Plain Language | Example |
| --------------- | ------ | -------------------- | --------------------------------------------- | ----------------------------- |
| **Type I (α)** | α | = significance level | Concluding there's an effect when there isn't | Convicting an innocent person |
| **Type II (β)** | β | Depends on power | Missing a real effect | Acquitting a guilty person |
| **Power (1−β)** | 1−β | We want this high | Correctly detecting a real effect | Convicting the guilty |

**Concrete example** (common convention):

- α = 0.05 → 5% chance of false positive
- β = 0.20 → 20% chance of false negative
- Power = 1 − β = **0.80** → 80% chance of detecting a true effect

Tip: Trade-off: Lowering α (to reduce Type I errors) increases β (more Type II errors). There's no free lunch. The solution is to increase sample size, which reduces both simultaneously.

### Practical Implications by Field

| Field | Lower α preferred | Lower β (higher power) preferred |
| ------------------------ | ---------------------------------------- | ----------------------------------- |
| **Clinical trials** | To avoid claiming ineffective drugs work | To avoid missing beneficial effects |
| **Exploratory research** | Moderate α (0.05–0.10) acceptable | Focus on power for discovery |
| **Quality control** | Strict α (0.01 or less) | Depends on cost of missed defects |

## When "Not Significant" Does Not Mean "No Difference"

One of the most common bad conclusions is:

> "The p-value was greater than 0.05, so the two groups are the same."

That statement is usually too strong. A non-significant test may simply reflect:

- too little data
- too much noise
- an effect smaller than expected
- a poorly matched test or violated assumptions

If the research question is really about showing similarity or non-inferiority, the correct framework is often **equivalence testing** or **non-inferiority testing**, not a standard null-hypothesis significance test.

Tip: Standard NHST is built to detect evidence against "no effect". It is not built to prove that two things are close enough to be treated as practically equivalent.

## Statistical Power and Effect Size

### Statistical Power

**Power** = P(reject H₀ | H₀ is false) = probability of correctly detecting a real effect.

\[
\text{Power} = 1 - \beta
\]

| Power Level | Interpretation |
| ----------- | -------------------------------------------------- |
| < 0.50 | Underpowered — likely to miss real effects |
| 0.80 | Conventional minimum — detects 80% of real effects |
| > 0.90 | Well-powered — used in high-stakes research |

Warning: Overpowered studies: With extremely large n, even trivially small effects become statistically significant. High power is good — but always pair with effect size to judge practical relevance.

Tip: Increasing sample size improves power, but does not change the true effect size. A larger n makes the test more sensitive, not the effect more meaningful.

**Factors that increase power:**

| Factor | Direction | Effect on Power |
| ---------------------- | ---------- | ------------------------------------------ |
| Sample size (n) | ↑ Increase | ↑ Power increases |
| Effect size | ↑ Larger | ↑ Power increases |
| Significance level (α) | ↑ Relax | ↑ Power increases (but more Type I errors) |
| Variability (σ) | ↓ Decrease | ↑ Power increases |

### Power Analysis

Power analysis is performed **before data collection** to determine the minimum sample size needed to achieve a target power given an expected effect size and α.

**Always report in any study:**

- Effect size assumed (with justification)
- α level and test type (one- vs. two-tailed)
- Sample size per group
- Target or achieved power

```python
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()

# Given effect size and n → what power do we have?
power = analysis.solve_power(effect_size=0.5, nobs1=30, alpha=0.05)
print(f"Power with n=30: {power:.3f}")

# Given effect size and target power → how many samples do we need?
n_required = analysis.solve_power(effect_size=0.5, alpha=0.05, power=0.8)
print(f"Required n per group: {n_required:.1f}")
```

```python
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()
effect_sizes = np.linspace(0.1, 1.0, 50)
powers = [analysis.solve_power(effect_size=d, nobs1=30, alpha=0.05) for d in effect_sizes]

plt.plot(effect_sizes, powers, color='steelblue')
plt.axhline(0.8, color='coral', linestyle='--', label='Power = 0.80 (target)')
plt.xlabel("Effect Size (Cohen's d)")
plt.ylabel("Power (1 − β)")
plt.title("Power vs. Effect Size (n=30, α=0.05)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### Effect Size

Effect size measures the **magnitude** of the effect — how big is the difference, independent of sample size. Statistical significance tells us _whether_ an effect exists; effect size tells us _how big_ it is.

| Measure | Formula | Used For | Small / Medium / Large |
| -------------- | --------------------- | -------------------------------- | ---------------------- |
| **Cohen's d** | (μ₁ − μ₂) / σ_pooled | Comparing two means | 0.2 / 0.5 / 0.8 |
| **r** | Pearson correlation | Linear relationship | 0.1 / 0.3 / 0.5 |
| **η² (eta²)** | SS_between / SS_total | ANOVA | 0.01 / 0.06 / 0.14 |
| **odds ratio** | (a/b) / (c/d) | Categorical, logistic regression | Context-dependent |

**Two common mismatches to watch for:**

✅ Significant + small effect size: A real difference exists, but the magnitude may be practically irrelevant — often caused by a very large sample size inflating sensitivity.

Warning: Not significant + large effect size: The difference is meaningful, but the test failed to detect it — often due to small sample size, high variability, or insufficient power.

Tip: A larger effect size makes detection easier → smaller samples needed to achieve the same power. Always report both p-value and effect size.

## p-Hacking and Optional Stopping

Many false discoveries come not from bad formulas, but from bad research behavior.

Common forms of p-hacking:

- trying several outcomes and only reporting the significant one
- stopping data collection the moment `p < 0.05`
- switching from two-sided to one-sided after seeing the result
- trying many covariate combinations until one "works"

Warning: These behaviors silently inflate the Type I error rate far above the nominal α. The reported p-value no longer means what it claims to mean.

Better habits:

- pre-specify the primary outcome
- pre-specify alpha and tail direction
- run a power analysis before collecting data
- report all major analyses, not just the favorable one

```python
from scipy import stats
import numpy as np

# Cohen's d: effect size for two group means
def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    s1, s2 = group1.std(ddof=1), group2.std(ddof=1)
    s_pooled = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
    return (group1.mean() - group2.mean()) / s_pooled

from sklearn.datasets import load_iris
import pandas as pd

iris = load_iris(as_frame=True)
df = iris.frame
df['species'] = iris.target_names[iris.target]

setosa     = df[df['species'] == 'setosa']['sepal length (cm)']
versicolor = df[df['species'] == 'versicolor']['sepal length (cm)']

t_stat, p_val = stats.ttest_ind(setosa, versicolor)
d = cohens_d(setosa, versicolor)

print(f"t-statistic = {t_stat:.4f}")
print(f"p-value     = {p_val:.4e}")
print(f"Cohen's d   = {d:.4f}  ({'large' if abs(d) >= 0.8 else 'medium' if abs(d) >= 0.5 else 'small'})")
```

## The Steps of Hypothesis Testing

### Multiple Comparisons

When you run many tests, the chance of at least one false positive increases. Adjust p-values when testing many hypotheses at once.

Key point: When you run many tests at once, the probability of getting at least one false positive rises above your nominal α level. Multiple-comparison correction is used to control the overall error rate.

| Situation | Common Correction | Notes |
| --------- | ----------------- | ----- |
| Few planned comparisons | Bonferroni | Simple but conservative |
| Many pairwise tests | Holm | Good default; less conservative |
| Exploratory many-feature testing | FDR / Benjamini-Hochberg | Controls expected false discoveries |
| After ANOVA | Tukey or Games-Howell | Use ANOVA-specific post-hoc tests |

A complete hypothesis test always follows these steps — skipping any step risks misleading conclusions.

| Action | Example |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| **State H₀ and H₁** | H₀: μ = 5.0 vs. H₁: μ ≠ 5.0 |
| **Set significance level α** | α = 0.05 |
| **Check assumptions** | Normality, sample size, independence → see [Assumption Checks](./assumption-checks.md) |
| **Choose and compute the test statistic** | t = (x̄ − μ₀) / SE → see the t-score vs. z-score comparison in the confidence interval notes |
| **Compute the p-value** | p = 0.023 |
| **Make a decision: reject or fail to reject H₀** | p < α → Reject H₀ |
| **Report effect size and CI** | d = 0.72, 95% CI: [5.71, 5.97] |
| **Adjust for multiple tests if needed** | Holm, Tukey, or FDR |
| **Interpret in context** | "Sepal lengths differ significantly by species" |

## A Compact Reporting Pattern

Good reporting usually fits this template:

```text
The treatment group had a higher mean score than control
(mean difference = 4.8, 95% CI [1.9, 7.6]),
t(58) = 3.31, p = .002, Cohen's d = 0.85.
```

This gives the reader:

- direction of the effect
- size of the effect
- uncertainty of the effect
- statistical evidence against H₀

## Key Takeaways

| Concept | Key Point |
| ------------------------------- | ------------------------------------------------------------------------------------- |
| **H₀ is assumed true** | We test whether data is inconsistent with it — we never prove H₁ directly |
| **p-value ≠ probability of H₀** | p-value is about the data, not directly about the hypothesis |
| **α is set in advance** | Never adjust α after seeing the data |
| **Two types of error** | Type I (false positive) controlled by α; Type II (false negative) controlled by β |
| **Power matters** | Underpowered studies miss real effects — calculate sample size before collecting data |
| **Effect size is required** | Statistical significance ≠ practical significance; always report both |
| **Multiple testing matters** | Many tests increase false positives; adjust p-values when needed |
