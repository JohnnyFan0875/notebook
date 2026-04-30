# 3. Two Independent Samples: Mann-Whitney U Test

The **Mann-Whitney U Test** (also called the Wilcoxon Rank-Sum Test) is the non-parametric alternative to the **independent samples t-test**. It tests whether two independent groups come from the same distribution — specifically whether one tends to have higher values than the other.

> 📌 **Parametric equivalent**: Independent samples t-test  
> 📌 **What it tests**: Whether the distribution of one group is stochastically greater than the other — often interpreted as a test of medians when distributions have similar shapes.

---

## 3.1 When to Use Mann-Whitney U

| Condition                                    | Reason                                               |
| -------------------------------------------- | ---------------------------------------------------- |
| Data is not normally distributed in one or both groups | Normality assumption of t-test is violated  |
| Sample sizes are small (n < 30 per group)    | CLT doesn't guarantee normality of sampling distribution |
| Data is ordinal (e.g., survey ratings)       | Means are not meaningful for ordinal scales          |
| Severe outliers are present                  | Outliers distort means and variances                  |
| Variances are highly unequal across groups   | Even with Welch's correction, extremes can be problematic |

---

## 3.2 How It Works

1. **Pool** all observations from both groups and **rank** them from lowest (1) to highest
2. **Sum the ranks** for each group separately → R₁ and R₂
3. **Calculate U statistics** for each group:

$$U_1 = n_1 n_2 + \frac{n_1(n_1 + 1)}{2} - R_1$$
$$U_2 = n_1 n_2 + \frac{n_2(n_2 + 1)}{2} - R_2$$

4. The test statistic is **U = min(U₁, U₂)**
5. Under H₀, the distribution of U is known — compare against critical values or use normal approximation for large samples

> 💡 **Intuition**: If the two groups were identical, we'd expect ranks to be distributed evenly between them. A very small U means one group dominates the low ranks (or high ranks) — evidence of a systematic difference.

---

## 3.3 Hypotheses

| Type                 | H₀                                               | H₁                                               |
| -------------------- | ------------------------------------------------ | ------------------------------------------------ |
| Two-tailed           | The two distributions are identical              | The distributions differ                         |
| One-tailed (greater) | Group A does not tend to have larger values      | Group A tends to have larger values than Group B |
| One-tailed (less)    | Group A does not tend to have smaller values     | Group A tends to have smaller values than Group B |

---

## 3.4 Python Implementation

```python
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

# Example: comparing test scores between two teaching methods
group_a = np.array([72, 68, 75, 80, 65, 71, 78, 69, 74, 70])
group_b = np.array([85, 90, 82, 88, 79, 91, 84, 87, 83, 86])

# ── Mann-Whitney U Test ──
stat, p_value = stats.mannwhitneyu(group_a, group_b, alternative='two-sided')

print(f"Mann-Whitney U = {stat:.3f}")
print(f"p-value        = {p_value:.4f}")
print(f"Median A = {np.median(group_a):.1f},  Median B = {np.median(group_b):.1f}")

if p_value < 0.05:
    print("→ Reject H₀: the two groups differ significantly")
else:
    print("→ Fail to reject H₀: no significant difference detected")
```

---

## 3.5 Effect Size: Rank-Biserial Correlation (r)

A significant p-value alone doesn't tell you how large the effect is. The **rank-biserial correlation** r is the standard effect size for Mann-Whitney U.

$$r = 1 - \frac{2U}{n_1 \cdot n_2}$$

Range: −1 to +1, where:
- r > 0: Group B tends to have higher values
- r < 0: Group A tends to have higher values
- |r| ≈ 0: No systematic difference

```python
n1 = len(group_a)
n2 = len(group_b)

# rank-biserial correlation
r = 1 - (2 * stat) / (n1 * n2)
print(f"Effect size r = {r:.3f}")
```

| |r| Value  | Interpretation  |
| ---------- | --------------- |
| 0.1–0.3    | Small effect    |
| 0.3–0.5    | Medium effect   |
| > 0.5      | Large effect    |

---

## 3.6 Checking Assumptions

Mann-Whitney U requires only two assumptions:

| Assumption                    | How to Check                              |
| ----------------------------- | ----------------------------------------- |
| **Independence** within and between groups | Study design — cannot be tested statistically |
| **Ordinal or continuous** data | Data type check                           |

> 💡 **Important nuance**: Mann-Whitney U technically tests whether one distribution is **stochastically larger** than the other — not strictly a test of medians. If the two distributions have different *shapes* (not just location), interpreting the result as a median comparison can be misleading. Always visualize the distributions first.  
> Mann-Whitney 嚴格來說測試的是「隨機優越性」，不是中位數差異。如果兩組分佈形狀差異很大，結果解讀需要特別謹慎。

---

## 3.7 Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

group_a = np.array([72, 68, 75, 80, 65, 71, 78, 69, 74, 70])
group_b = np.array([85, 90, 82, 88, 79, 91, 84, 87, 83, 86])

import pandas as pd
df = pd.DataFrame({
    'Score': np.concatenate([group_a, group_b]),
    'Group': ['A'] * len(group_a) + ['B'] * len(group_b)
})

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# ── Boxplot with jittered points ──
sns.boxplot(x='Group', y='Score', data=df, palette='Set2', ax=axes[0])
sns.stripplot(x='Group', y='Score', data=df, color='black', alpha=0.5,
              jitter=True, ax=axes[0])
axes[0].set_title('Score Distribution by Group\n(Boxplot + Jitter)')

# ── Violin plot ──
sns.violinplot(x='Group', y='Score', data=df, palette='Set2', inner='quartile', ax=axes[1])
axes[1].set_title('Score Distribution by Group\n(Violin Plot)')

plt.tight_layout()
plt.show()
```

---

## 3.8 Mann-Whitney U vs Independent t-test

| Criterion                              | Independent t-test         | Mann-Whitney U              |
| -------------------------------------- | -------------------------- | --------------------------- |
| Assumes normality                      | ✅ Yes                     | ❌ No                       |
| Assumes equal variance                 | Yes (Welch's version: No)  | ❌ No                       |
| Uses                                   | Raw values (means)         | Ranks                       |
| Sensitive to outliers                  | Yes                        | No                          |
| Handles ordinal data                   | ❌ Inappropriate           | ✅ Yes                      |
| Statistical power (when normal)        | Higher                     | ~95% as efficient           |
| Effect size metric                     | Cohen's d                  | Rank-biserial r             |

> 💡 **When data is normally distributed**, Mann-Whitney U has about 95% the power of the t-test — the power loss is minimal. In practice, it's a solid default for small samples.

---

## 3.9 Key Takeaways

| Concept                         | Key Point                                                                  |
| ------------------------------- | -------------------------------------------------------------------------- |
| **Mann-Whitney U**              | Non-parametric test for two independent groups                             |
| **Based on ranks**              | Converts raw values to ranks — outliers lose their extreme influence        |
| **Always report effect size**   | Rank-biserial r alongside U and p-value                                    |
| **Visualize distributions**     | Boxplots and violin plots reveal shape differences that medians don't show  |
| **Not strictly a median test**  | Technically tests stochastic dominance — shape matters too                  |

---