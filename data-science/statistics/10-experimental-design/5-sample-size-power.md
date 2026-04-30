# 5. Sample Size & Statistical Power

One of the most important — and most neglected — steps in experimental design is determining **how many observations you need**. Too few and you miss real effects; too many and you waste resources.

> 📌 **為什麼在收集資料前就要計算樣本數**：事後發現樣本數不足，實驗就只能重做。事後追加樣本（p-hacking by optional stopping）是一種嚴重的研究誤行為，會讓型一誤差膨脹。樣本數計算必須在實驗開始前完成。

---

## 5.1 The Error Framework: α, β, and Power

When you run a hypothesis test, there are four possible outcomes:

|                          | H₀ Is True (no real effect)  | H₀ Is False (real effect exists) |
| ------------------------ | ----------------------------- | ---------------------------------- |
| **Reject H₀**            | ❌ Type I Error (α)            | ✅ Correct (Power = 1−β)           |
| **Fail to reject H₀**   | ✅ Correct                     | ❌ Type II Error (β)               |

| Symbol       | 中文        | Definition                                                       | Typical Value |
| ------------ | ----------- | ---------------------------------------------------------------- | ------------- |
| **α**        | 型一誤差    | Probability of rejecting H₀ when it is actually true (false positive) | 0.05     |
| **β**        | 型二誤差    | Probability of failing to reject H₀ when it is actually false (false negative) | 0.20 |
| **Power (1−β)** | 統計檢力 | Probability of correctly detecting a real effect                 | 0.80          |

> 💡 **The α = 0.05 convention is arbitrary**. Use α = 0.01 in high-stakes applications (e.g., drug approval) or when multiple tests increase false positive risk. Use α = 0.10 in exploratory research where missing real effects is costly. 顯著水準 0.05 只是慣例，應根據研究背景和錯誤的成本來決定。

---

## 5.2 Effect Size

Effect size quantifies the **magnitude** of a difference or relationship — separate from whether it is statistically significant. It is the most important input to power calculations.

### Common Effect Size Measures

| Measure    | Used For                         | Formula                              | Small | Medium | Large |
| ---------- | -------------------------------- | ------------------------------------ | ----- | ------ | ----- |
| **Cohen's d** | Comparing two means            | d = (μ₁ − μ₂) / σ_pooled            | 0.2   | 0.5    | 0.8   |
| **Cohen's f** | ANOVA (multiple groups)        | f = σ_means / σ_within               | 0.1   | 0.25   | 0.4   |
| **Cohen's w** | Chi-square tests               | Based on effect in contingency table  | 0.1   | 0.3    | 0.5   |
| **r**      | Correlation                      | Pearson or point-biserial r           | 0.1   | 0.3    | 0.5   |

> ⚠️ Cohen's benchmarks (small/medium/large) are context-free defaults. A "small" effect in medical research (preventing 1 in 1000 deaths) may be clinically critical. Always define what effect size is **practically meaningful** in your domain before running power calculations.  
> 什麼叫「有意義」的效果大小，應根據領域和實際成本判斷，而不是套用 Cohen 的標準分類。

```python
import numpy as np
from scipy import stats

def cohen_d(group1, group2):
    """Cohen's d for two independent groups."""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_sd = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    return (np.mean(group1) - np.mean(group2)) / pooled_sd

np.random.seed(0)
control   = np.random.normal(100, 15, 30)
treatment = np.random.normal(108, 15, 30)

d = cohen_d(treatment, control)
t_stat, p_val = stats.ttest_ind(treatment, control)

print(f"Mean difference: {treatment.mean() - control.mean():.2f}")
print(f"Cohen's d:       {d:.3f}  ({'small' if abs(d) < 0.5 else 'medium' if abs(d) < 0.8 else 'large'})")
print(f"t-test: t = {t_stat:.3f}, p = {p_val:.4f}")
```

---

## 5.3 Power Analysis in Python

The `statsmodels` library provides power analysis functions for common tests.

### 5.3.1 Independent Samples t-test

The most common scenario: comparing two group means.

```python
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()

# Scenario 1: What sample size do I need?
n = analysis.solve_power(
    effect_size=0.5,    # Cohen's d (medium effect)
    alpha=0.05,
    power=0.80,
    ratio=1.0,          # equal group sizes
    alternative='two-sided'
)
print(f"Required n per group: {np.ceil(n):.0f}")

# Scenario 2: What power do I have given my n?
power = analysis.solve_power(
    effect_size=0.5,
    alpha=0.05,
    nobs1=30,           # n in group 1
    ratio=1.0,
    alternative='two-sided'
)
print(f"Power with n=30 per group: {power:.3f}")

# Scenario 3: What effect size can I detect?
es = analysis.solve_power(
    alpha=0.05,
    power=0.80,
    nobs1=50,
    ratio=1.0,
    alternative='two-sided'
)
print(f"Detectable effect size with n=50: {es:.3f}")
```

### 5.3.2 One-Way ANOVA (Multiple Groups)

```python
from statsmodels.stats.power import FTestAnovaPower

analysis_anova = FTestAnovaPower()

# Required n per group for ANOVA with 3 groups
n_anova = analysis_anova.solve_power(
    effect_size=0.25,   # Cohen's f (medium)
    alpha=0.05,
    power=0.80,
    k_groups=3
)
print(f"Required n per group (3-group ANOVA): {np.ceil(n_anova):.0f}")
```

### 5.3.3 Chi-Square Test of Independence

```python
from statsmodels.stats.power import GofChisquarePower

analysis_chi = GofChisquarePower()

n_chi = analysis_chi.solve_power(
    effect_size=0.3,   # Cohen's w (medium)
    alpha=0.05,
    power=0.80,
    n_bins=4           # number of categories
)
print(f"Required n (chi-square, 4 categories): {np.ceil(n_chi):.0f}")
```

---

## 5.4 Power Curves

A power curve visualizes how power changes as a function of sample size — essential for communicating with stakeholders and making resource decisions.

```python
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()
sample_sizes = np.arange(10, 201, 5)

effect_sizes = [0.2, 0.5, 0.8]   # small, medium, large
colors = ['#3B82F6', '#F59E0B', '#EF4444']

fig, ax = plt.subplots(figsize=(8, 5))

for es, color in zip(effect_sizes, colors):
    powers = [
        analysis.solve_power(effect_size=es, alpha=0.05, nobs1=n, ratio=1.0)
        for n in sample_sizes
    ]
    label = f"d = {es} ({'small' if es == 0.2 else 'medium' if es == 0.5 else 'large'})"
    ax.plot(sample_sizes, powers, label=label, color=color, linewidth=2)

ax.axhline(0.80, color='gray', linestyle='--', linewidth=1, label='Power = 0.80')
ax.axhline(0.95, color='gray', linestyle=':',  linewidth=1, label='Power = 0.95')
ax.set_xlabel('Sample Size per Group')
ax.set_ylabel('Statistical Power (1−β)')
ax.set_title('Power Curves — Independent t-test (α = 0.05)')
ax.legend()
ax.set_ylim(0, 1.05)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

> 💡 **Reading the power curve**: Find the effect size you care about, then read across to find the n that gives you power ≥ 0.80. The flattening of curves at large n shows diminishing returns — going from n=200 to n=400 buys much less power than going from n=20 to n=40.

---

## 5.5 Factors That Increase Required Sample Size

| Factor                              | Effect on n | Intuition                                            |
| ----------------------------------- | ----------- | ---------------------------------------------------- |
| Smaller effect size (d ↓)           | n ↑         | Harder to detect subtle differences                  |
| Stricter α (e.g., 0.05 → 0.01)     | n ↑         | Need more evidence to reject H₀                     |
| Higher desired power (0.80 → 0.95)  | n ↑         | Want to be more confident of detecting real effects  |
| Higher population variance (σ ↑)    | n ↑         | More noise requires larger signal-to-noise ratio     |
| Two-sided vs. one-sided test        | n ↑ (two-sided) | Two-sided tests distribute α across both tails  |
| Unequal group sizes                 | n ↑ (total) | Balanced designs are most efficient                  |
| Multiple comparisons (k groups ↑)   | n ↑         | Stricter α per test to control familywise error      |

```python
# Demonstrating the effect of variance on required n
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()

# Mean difference is fixed at 5 units
# What happens to required n as population SD increases?
mean_diff = 5
sds = [5, 10, 15, 20, 25]

print("SD  | Cohen's d | Required n per group (power=0.80)")
print("----|-----------|-----------------------------------")
for sd in sds:
    d = mean_diff / sd
    n = analysis.solve_power(effect_size=d, alpha=0.05, power=0.80, ratio=1.0)
    print(f"{sd:3d} | {d:.3f}     | {int(np.ceil(n))}")
```

**Output:**

```
SD  | Cohen's d | Required n per group (power=0.80)
----|-----------|-----------------------------------
  5 | 1.000     | 17
 10 | 0.500     | 64
 15 | 0.333     | 145
 20 | 0.250     | 253
 25 | 0.200     | 394
```

---

## 5.6 Post-hoc Power Analysis — When NOT to Use It

> ⚠️ **Post-hoc power analysis** (computing power after a non-significant result using the observed effect size) is controversial and generally **misleading**. If the test was not significant, the observed effect size is a noisy estimate; a post-hoc power calculation using it will almost always show low power — but this tells you nothing useful.  
>  
> **What to do instead**: Report your confidence interval. A wide CI tells stakeholders the study was under-powered without the circularity of post-hoc power.  
> 事後再用觀測到的效果大小計算檢力，結果幾乎一定是「檢力不足」，這是邏輯上的循環，沒有實質資訊。請改為報告信賴區間的寬度。

```python
from scipy import stats
import numpy as np

# Underpowered study: n=10 per group
np.random.seed(2)
n = 10
g1 = np.random.normal(100, 15, n)
g2 = np.random.normal(106, 15, n)

t, p = stats.ttest_ind(g1, g2)
diff = g2.mean() - g1.mean()

# Pooled SE for CI
se = np.sqrt(g1.var(ddof=1)/n + g2.var(ddof=1)/n)
ci_low, ci_high = diff - 1.96*se, diff + 1.96*se

print(f"Mean difference: {diff:.2f}")
print(f"p-value:         {p:.4f}  (not significant)")
print(f"95% CI:          [{ci_low:.2f}, {ci_high:.2f}]")
print(f"\nThe wide CI tells us this study cannot rule out effects")
print(f"ranging from {ci_low:.1f} to {ci_high:.1f} — much more informative")
print(f"than saying 'post-hoc power was low'.")
```

---

## 5.7 Practical Sample Size Cheat Sheet

| Test                          | Python Function                          | Effect Size Measure |
| ----------------------------- | ---------------------------------------- | ------------------- |
| Independent t-test            | `TTestIndPower().solve_power()`          | Cohen's d           |
| Paired t-test                 | `TTestPower().solve_power()`             | Cohen's d           |
| One-way ANOVA                 | `FTestAnovaPower().solve_power()`        | Cohen's f           |
| Chi-square goodness of fit    | `GofChisquarePower().solve_power()`      | Cohen's w           |
| Correlation (Pearson r)       | `TTestPower().solve_power()` (convert r→d) | r                 |
| Proportion test               | `proportion_effectsize()` + `NormalIndPower()` | h              |

```python
# Proportion test example: comparing two conversion rates
from statsmodels.stats.proportion import proportion_effectsize
from statsmodels.stats.power import NormalIndPower

# Current conversion rate: 10%; expect treatment to lift to 15%
es_prop = proportion_effectsize(0.10, 0.15)
n_prop = NormalIndPower().solve_power(
    effect_size=es_prop,
    alpha=0.05,
    power=0.80,
    ratio=1.0
)
print(f"Effect size h: {es_prop:.3f}")
print(f"Required n per group: {int(np.ceil(n_prop))}")
```

---

## 5.8 Key Takeaways

| Concept                       | Key Point                                                                 |
| ----------------------------- | ------------------------------------------------------------------------- |
| **Power = 1−β**               | The probability of detecting a real effect; target ≥ 0.80               |
| **Effect size is primary**    | Define the minimum meaningful effect first, then solve for n              |
| **α and power tradeoff**      | Stricter α requires larger n to maintain the same power                  |
| **Calculate before collecting** | Post-hoc sample size justifications are circular and misleading        |
| **Balanced designs**          | Equal group sizes maximize power for a given total n                      |
| **Report CIs, not post-hoc power** | A wide CI communicates under-precision without the logical circularity |

---
