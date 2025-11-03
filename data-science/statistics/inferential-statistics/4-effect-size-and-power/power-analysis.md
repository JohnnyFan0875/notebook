# Power

Statistical **power** is the probability of correctly rejecting the null hypothesis when it is false — in other words, the ability of a test to detect a true effect.  
在原假設為假時，正確拒絕原假設的機率，代表統計檢定發現真實差異的能力。

$$
\text{Power} = 1 - \beta
$$

- $\beta$ = probability of a [**Type II error**](./README.md#type-i-and-type-ii-errors) (false negative).

## 1. Concept Overview

Statistical power quantifies the **sensitivity** of a hypothesis test.  
It measures how likely the test will find a statistically significant result when the effect is real.

- **High power (≥ 0.8)** → reliable detection of true effects.
  - Power = 0.8: An 80% chance of detecting a true effect if it exists.
- **Low power (< 0.5)** → increased risk of false negatives (missing true effects).

Power analysis is usually performed **before data collection** to estimate the sample size required to achieve a target power.

## 2. Relationship with Effect Size, α, Sample Size, and Variability

Power depends on four fundamental components:

| Component                                                   | Symbol   | Effect on Power | Explanation                                                       |
| ----------------------------------------------------------- | -------- | --------------- | ----------------------------------------------------------------- |
| [**Effect Size**](../inferential-statistics/effect-size.md) | δ or _d_ | ↑               | Larger true effects are easier to detect.                         |
| **Sample Size**                                             | _n_      | ↑               | Larger samples produce smaller standard error.                    |
| [**Significance Level**](./significance-level.md)           | α        | ↑               | Larger α increases chance to reject H₀ (but raises Type I error). |
| **Variability**                                             | σ or _s_ | ↓               | Higher variability makes effects harder to detect.                |

Mathematically, for a one-sample z-test:

$$
\text{Power} = 1 - \Phi \!\left(z_{1-\alpha} - \frac{\delta \sqrt{n}}{\sigma}\right)
$$

where $\Phi$ is the cumulative standard normal distribution.

## 4. Interpretation

- **Target:** Power ≥ 0.8 (80%) is generally acceptable.
- **Underpowered studies** → risk failing to detect true effects.
- **Overpowered studies** → can yield statistically significant but trivial results.
- Increasing sample size improves power but does **not** change the true effect size.

**Always report:**

- Effect size used in power analysis (with justification)
- α level and chosen test type
- Sample size per group
- Achieved or target power

## 5. Python Example

```python
from statsmodels.stats.power import TTestIndPower

# Initialize power analysis
power_analysis = TTestIndPower()

# Calculate power
power = power_analysis.solve_power(effect_size=0.5, nobs1=30, alpha=0.05)

print(f"Power: {power:.3f}")

# Calculate numbers required
n_required = power_analysis.solve_power(effect_size=0.5, alpha=0.05, power=0.8)

print(f"Required Sample Size per Group: {n_required:.2f}")
```

```python
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()
effect_sizes = np.linspace(0.1, 1.0, 50)
powers = [analysis.solve_power(effect_size=d, nobs1=30, alpha=0.05) for d in effect_sizes]

plt.plot(effect_sizes, powers)
plt.xlabel("Effect Size (Cohen's d)")
plt.ylabel("Power (1 - β)")
plt.title("Relationship Between Effect Size and Statistical Power")
plt.show()
```

## 6. Summary

| Factor             | Effect on Power | Explanation                                    |
| ------------------ | --------------- | ---------------------------------------------- |
| Effect size ↑      | Power ↑         | Larger difference → easier detection           |
| Sample size ↑      | Power ↑         | Smaller standard error                         |
| Variability ↑      | Power ↓         | More noise reduces sensitivity                 |
| α (significance) ↑ | Power ↑         | Easier to reject H₀ but increases Type I error |
