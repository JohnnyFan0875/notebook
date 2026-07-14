# One-Sample & Paired Tests

This section covers non-parametric tests used when you have **one sample** compared to a fixed value, or **two paired measurements** on the same subjects.

Key point: Parametric equivalents: One-sample t-test → Sign Test or Wilcoxon Signed-Rank Test; Paired t-test → Wilcoxon Signed-Rank Test.

## The Sign Test

The **simplest** non-parametric test. It only uses the **direction** of differences (positive or negative), ignoring the magnitude.

### When to Use
- Testing whether the median of a population equals a specific value
- The weakest but most assumption-free option
- Useful when only the direction of change matters (not how much)

### Hypotheses

| Type | H₀ | H₁ |
| ------------- | ------------------------------------ | ------------------------------------------- |
| Two-tailed | Median = M₀ | Median ≠ M₀ |
| One-tailed | Median ≤ M₀  (or Median ≥ M₀) | Median > M₀  (or Median < M₀) |

### How It Works

1. Subtract the hypothesized median (M₀) from each observation
2. Record the sign of each difference (+, −, or 0)
3. Discard ties (zero differences)
4. Count the number of positive signs (S)
5. Under H₀, S follows a Binomial(n, 0.5) distribution

```python
import numpy as np
from scipy import stats

data = np.array([85, 92, 78, 95, 88, 70, 91, 84, 76, 89])
M0 = 80  # hypothesized median

differences = data - M0
positives = np.sum(differences > 0)
negatives  = np.sum(differences < 0)
n_effective = positives + negatives  # exclude ties

# Two-tailed p-value using binomial distribution
p_value = 2 * min(
    stats.binom.cdf(positives, n_effective, 0.5),
    stats.binom.cdf(negatives, n_effective, 0.5)
)

print(f"Positives: {positives}, Negatives: {negatives}")
print(f"p-value (two-tailed): {p_value:.4f}")
```

Warning: The Sign Test throws away information about the *size* of differences. Use the Wilcoxon Signed-Rank Test if the magnitude matters — it almost always does.

## Wilcoxon Signed-Rank Test

The **standard non-parametric alternative** to both the one-sample t-test and the paired t-test. It uses both the direction **and** magnitude of differences — making it much more powerful than the Sign Test.

### When to Use
- **One-sample**: testing whether a population median equals M₀, when normality is violated
- **Paired samples**: comparing two related measurements on the same subjects (before/after, left/right, matched pairs)
- Data is at least ordinal
- Differences are approximately symmetric around the median (but not necessarily normal)

### How It Works

1. Calculate differences: dᵢ = xᵢ − M₀ (or dᵢ = xᵢ − yᵢ for paired data)
2. Discard zero differences (ties)
3. Rank the **absolute values** of differences (|dᵢ|)
4. Assign the original sign to each rank
5. Calculate W⁺ (sum of positive ranks) and W⁻ (sum of negative ranks)
6. The test statistic W = min(W⁺, W⁻)

Under H₀, the positive and negative ranks should be roughly balanced. A very small W indicates the differences systematically favor one direction.

### One-Sample Example

```python
import numpy as np
from scipy import stats

data = np.array([85, 92, 78, 95, 88, 70, 91, 84, 76, 89])
M0 = 80

# One-sample: test against hypothesized median
stat, p_value = stats.wilcoxon(data - M0, alternative='two-sided')

print(f"Wilcoxon W = {stat:.3f}")
print(f"p-value    = {p_value:.4f}")

if p_value < 0.05:
    print("Reject H₀: median is significantly different from", M0)
else:
    print("Fail to reject H₀: no significant difference from", M0)
```

### Paired-Sample Example

```python
import numpy as np
from scipy import stats

# Before and after treatment scores
before = np.array([72, 68, 75, 80, 65, 71, 78, 69, 74, 70])
after  = np.array([78, 72, 80, 85, 70, 74, 82, 75, 79, 76])

stat, p_value = stats.wilcoxon(before, after, alternative='two-sided')

print(f"Wilcoxon W = {stat:.3f}")
print(f"p-value    = {p_value:.4f}")

# Effect size: r = Z / sqrt(n)
n = len(before)
# scipy doesn't return Z directly; approximate via normal approximation for larger n
import scipy.stats as st
z_approx = st.norm.ppf(p_value / 2)  # two-tailed approximation
r = abs(z_approx) / np.sqrt(n)
print(f"Effect size r ≈ {r:.3f}")
```

### Effect Size Interpretation

| r Value | Interpretation |
| --------- | ----------------- |
| 0.1–0.3 | Small effect |
| 0.3–0.5 | Medium effect |
| > 0.5 | Large effect |

Tip: Always report effect size alongside the p-value. Statistical significance tells you the effect probably exists; effect size tells you if it matters. p-value tells you if the effect exists and effect size tells you if it matters. Report both.

## Choosing Between Sign Test and Wilcoxon Signed-Rank

| Criterion | Sign Test | Wilcoxon Signed-Rank |
| -------------------------------------- | ----------------- | ------------------------- |
| Uses magnitude of differences | ❌ No | ✅ Yes |
| Statistical power | Lower | Higher |
| Assumption about differences | None | Symmetry around median |
| Handles many tied values gracefully | ✅ Better | ⚠️ Adjusted, but weaker |
| Sample size requirement | Any | n ≥ 10 recommended |
| Recommended default | Only if ties dominate | ✅ Prefer this |

## Visualizing Paired Data

Always visualize before testing. For paired data, the goal is to show the **direction and magnitude** of individual changes.

```python
import matplotlib.pyplot as plt
import numpy as np

before = np.array([72, 68, 75, 80, 65, 71, 78, 69, 74, 70])
after  = np.array([78, 72, 80, 85, 70, 74, 82, 75, 79, 76])
n = len(before)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# ── Left: Paired line plot (spaghetti plot) ──
for i in range(n):
    color = 'steelblue' if after[i] > before[i] else 'tomato'
    axes[0].plot([0, 1], [before[i], after[i]], color=color, alpha=0.6, linewidth=1.5)
axes[0].plot([0, 1], [before.mean(), after.mean()],
             color='black', linewidth=2.5, linestyle='--', label='Mean')
axes[0].set_xticks([0, 1])
axes[0].set_xticklabels(['Before', 'After'])
axes[0].set_title('Paired Observations')
axes[0].set_ylabel('Score')
axes[0].legend()

# ── Right: Distribution of differences ──
diffs = after - before
axes[1].hist(diffs, bins=8, color='steelblue', edgecolor='white')
axes[1].axvline(0, color='red', linestyle='--', label='No change')
axes[1].axvline(diffs.mean(), color='black', linestyle='-', label=f'Mean diff = {diffs.mean():.1f}')
axes[1].set_title('Distribution of Differences (After − Before)')
axes[1].set_xlabel('Difference')
axes[1].legend()

plt.tight_layout()
plt.show()
```

## Assumptions Summary

| Assumption | Sign Test | Wilcoxon Signed-Rank |
| ------------------------ | --------- | -------------------- |
| Data is at least ordinal | ✅ | ✅ |
| Differences are symmetric | Not required | Required (approximately) |
| Independence of pairs | ✅ | ✅ |
| No assumption on distribution | ✅ | ✅ |

Warning: Independence of observations is still required — paired tests handle within-subject dependence, but different pairs must be independent from each other.

## Key Takeaways

| Concept | Key Point |
| ---------------------------- | ----------------------------------------------------------------------- |
| **Sign Test** | Only uses direction; very simple but low power |
| **Wilcoxon Signed-Rank** | Uses direction + magnitude; the standard non-parametric paired test |
| **Prefer Wilcoxon** | Unless ties completely dominate the data |
| **Effect size** | Always report r alongside p-value |
| **Visualize first** | Paired line plots show individual trajectories; difference histograms show symmetry |

## Signed-Rank vs. Sign Test

Use Wilcoxon signed-rank when the size of paired differences is meaningful and roughly symmetric. Use the sign test when only the direction of change is trustworthy or when difference magnitudes are too distorted by ties or measurement coarseness.
