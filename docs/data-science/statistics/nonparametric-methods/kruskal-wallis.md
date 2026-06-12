# Multiple Groups: Kruskal-Wallis Test

The **Kruskal-Wallis Test** is the non-parametric alternative to **one-way ANOVA**. It tests whether three or more independent groups come from the same distribution.

Key point: Parametric equivalent: One-way ANOVA Key point: Think of it as: An extension of Mann-Whitney U to three or more groups — all based on ranks.

## When to Use Kruskal-Wallis

| Condition | Reason |
| -------------------------------------------- | ------------------------------------------------------------- |
| Comparing 3+ independent groups | Mann-Whitney U only handles 2 groups |
| Data is not normally distributed | One-way ANOVA requires normality in each group |
| Data is ordinal | ANOVA means are not meaningful for ordinal data |
| Small samples per group | Normality hard to verify; CLT doesn't fully apply |
| Outliers are present | Rank-based methods are robust to extreme values |

Warning: Like Mann-Whitney U, Kruskal-Wallis does not assume normality, but it does assume that the groups have similar shapes (just possibly different locations) when interpreting results as a median comparison.

## How It Works

1. **Pool** all observations and **rank** them from 1 to N (total observations)
2. **Sum the ranks** within each group: R₁, R₂, ..., Rₖ
3. Compute the test statistic H:

\[
H = \frac{12}{N(N+1)} \sum_{i=1}^k \frac{R_i^2}{n_i} - 3(N+1)
\]

where N = total observations, k = number of groups, nᵢ = size of group i, Rᵢ = rank sum of group i.

4. Under H₀, H approximately follows a **Chi-square distribution** with k − 1 degrees of freedom (for n ≥ 5 per group)

### Hypotheses

- **H₀**: All groups come from identical populations (same distribution)
- **H₁**: At least one group has a different distribution

Tip: A significant result tells you *something* is different — but not *which* groups differ. Post-hoc tests are needed to pinpoint where the differences lie.

## Python Implementation

```python
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Example: comparing satisfaction scores across 3 teaching methods
method_a = np.array([72, 68, 75, 80, 65, 71, 78])
method_b = np.array([85, 90, 82, 88, 79, 91, 84])
method_c = np.array([76, 74, 79, 83, 77, 80, 75])

# ── Kruskal-Wallis Test ──
stat, p_value = stats.kruskal(method_a, method_b, method_c)

print(f"Kruskal-Wallis H = {stat:.3f}")
print(f"p-value          = {p_value:.4f}")
print(f"df               = {3 - 1}")

print(f"\nMedian A: {np.median(method_a):.1f}")
print(f"Median B: {np.median(method_b):.1f}")
print(f"Median C: {np.median(method_c):.1f}")

if p_value < 0.05:
    print("\n→ Reject H₀: at least one group differs significantly")
    print("→ Proceed to post-hoc tests (Dunn's Test)")
else:
    print("\n→ Fail to reject H₀: no significant differences detected")
```

## Effect Size: η² (Eta Squared)

\[
\eta^2 = \frac{H - k + 1}{N - k}
\]

where H is the Kruskal-Wallis statistic, k is number of groups, N is total sample size.

```python
n_total = len(method_a) + len(method_b) + len(method_c)
k = 3

eta_squared = (stat - k + 1) / (n_total - k)
print(f"Effect size η² = {eta_squared:.3f}")
```

| η² Value | Interpretation |
| ---------- | --------------- |
| 0.01–0.06 | Small effect |
| 0.06–0.14 | Medium effect |
| > 0.14 | Large effect |

## Post-hoc Tests: Dunn's Test

When Kruskal-Wallis is significant, Dunn's Test performs **pairwise comparisons** with correction for multiple testing.

Warning: Why correction? Performing multiple comparisons inflates the Type I error rate. If α = 0.05 and you make 3 comparisons, the probability of at least one false positive is much higher than 5%.

```python
# Install if needed: pip install scikit-posthocs
import scikit_posthocs as sp

# Prepare data in long format
all_data = np.concatenate([method_a, method_b, method_c])
groups   = (['A'] * len(method_a) +
             ['B'] * len(method_b) +
             ['C'] * len(method_c))

df_long = pd.DataFrame({'Score': all_data, 'Method': groups})

# Dunn's Test with Bonferroni correction
dunn_result = sp.posthoc_dunn(
    df_long, val_col='Score', group_col='Method', p_adjust='bonferroni'
)
print("Dunn's Test p-values (Bonferroni corrected):")
print(dunn_result.round(4))
```

**Available correction methods:**

| Method | Description | Use When |
| --------------- | ---------------------------------------- | ---------------------------------- |
| **Bonferroni** | Most conservative; multiply p by k | Small number of comparisons |
| **Holm** | Less conservative; stepwise Bonferroni | General use; recommended default |
| **BH (FDR)** | Controls False Discovery Rate | Many comparisons (e.g., genomics) |
| **None** | No correction | Only for exploration; not reporting |

Tip: Recommended default: Use `p_adjust='holm'` for most practical situations — it's less conservative than Bonferroni while still controlling Type I error.

## Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

method_a = np.array([72, 68, 75, 80, 65, 71, 78])
method_b = np.array([85, 90, 82, 88, 79, 91, 84])
method_c = np.array([76, 74, 79, 83, 77, 80, 75])

all_data = np.concatenate([method_a, method_b, method_c])
groups   = ['A'] * len(method_a) + ['B'] * len(method_b) + ['C'] * len(method_c)
df_long  = pd.DataFrame({'Score': all_data, 'Method': groups})

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# ── Boxplot with jitter ──
sns.boxplot(x='Method', y='Score', data=df_long, palette='Set2', ax=axes[0])
sns.stripplot(x='Method', y='Score', data=df_long, color='black',
              alpha=0.6, jitter=True, ax=axes[0])
axes[0].set_title('Score by Teaching Method (Boxplot)')

# ── Violin plot ──
sns.violinplot(x='Method', y='Score', data=df_long, palette='Set2',
               inner='quartile', ax=axes[1])
axes[1].set_title('Score by Teaching Method (Violin Plot)')

plt.tight_layout()
plt.show()
```

## Kruskal-Wallis vs One-Way ANOVA

| Criterion | One-Way ANOVA | Kruskal-Wallis |
| --------------------------------- | -------------------------- | -------------------------- |
| Assumes normality | ✅ Yes | ❌ No |
| Assumes equal variance | ✅ Yes | Similar shape (recommended) |
| Handles ordinal data | ❌ No | ✅ Yes |
| Sensitive to outliers | Yes | No |
| Statistical power (when normal) | Higher | ~95% as efficient |
| Post-hoc test | Tukey HSD, Bonferroni | Dunn's Test |
| Effect size | η² or ω² | η² (Kruskal-Wallis version) |

## Complete Workflow Example

```python
import numpy as np
from scipy import stats
import scikit_posthocs as sp
import pandas as pd

method_a = np.array([72, 68, 75, 80, 65, 71, 78])
method_b = np.array([85, 90, 82, 88, 79, 91, 84])
method_c = np.array([76, 74, 79, 83, 77, 80, 75])

# Step 1: Kruskal-Wallis
stat, p = stats.kruskal(method_a, method_b, method_c)
print(f"H = {stat:.3f}, p = {p:.4f}")

# Step 2: Effect size
N = len(method_a) + len(method_b) + len(method_c)
eta2 = (stat - 3 + 1) / (N - 3)
print(f"η² = {eta2:.3f}")

# Step 3: Post-hoc (only if p < 0.05)
if p < 0.05:
    df_long = pd.DataFrame({
        'Score':  np.concatenate([method_a, method_b, method_c]),
        'Method': ['A']*7 + ['B']*7 + ['C']*7
    })
    dunn = sp.posthoc_dunn(df_long, val_col='Score',
                            group_col='Method', p_adjust='holm')
    print("\nDunn's Test (Holm corrected):")
    print(dunn.round(4))
```

## Key Takeaways

| Concept | Key Point |
| ----------------------------- | ----------------------------------------------------------------------------- |
| **Kruskal-Wallis** | Rank-based test for 3+ independent groups; extends Mann-Whitney U |
| **Significant H ≠ pairwise** | Overall significance doesn't tell you *which* pairs differ |
| **Always follow up** | Significant Kruskal-Wallis → run Dunn's Test with correction |
| **Correction matters** | Holm is a good default; Bonferroni is safe but conservative |
| **Effect size** | Report η² regardless of sample size |
| **Visualize by group** | Boxplots or violin plots are essential for communicating group differences |

## After a Significant Kruskal–Wallis Test

The correct next step is a multiplicity-controlled pairwise comparison such as Dunn's test, not a pile of unadjusted Mann–Whitney tests.

Tip: The workflow is parallel to ANOVA: omnibus first, pairwise follow-up second.
