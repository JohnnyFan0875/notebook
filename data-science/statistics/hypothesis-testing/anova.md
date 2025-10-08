# ANOVA (Analysis of Variance)

ANOVA (Analysis of Variance) is used to compare the means of **three or more groups**.  
It evaluates whether at least one group mean differs from the others.

## Hypotheses

- **Null hypothesis (H₀):** All group means are equal.
- **Alternative hypothesis (Hₐ):** At least one group mean differs.

## Assumptions

- Independence of observations
- Normality within each group
- Equal variances across groups
  - If violated → use **Welch’s ANOVA** (unequal variances)
  - If non-normal → use **Kruskal–Wallis test** (non-parametric alternative)

## Test Statistic

The **F-test** is the core statistic in ANOVA.  
It compares **between-group variance** to **within-group variance** to evaluate whether the observed differences among group means are larger than would be expected by chance.

$$
F = \frac{MS*{\text{between}}}{MS*{\text{within}}}
$$

- $MS\_{\text{between}}$: variance between group means
- $MS\_{\text{within}}$: variance within groups

### Distribution and Degrees of Freedom

The **F-statistic** follows the F-distribution, which is **right-skewed** and defined by two parameters:

$$
F(df_1 = k - 1,\; df_2 = N - k)
$$

where:

- $k$: number of groups
- $N$: total sample size

The critical value depends on the chosen significance level (α).  
A larger F-value (relative to this cutoff) indicates that **between-group variation exceeds within-group variation**.

### Interpretation

| F value     | Meaning                                                                      |
| ----------- | ---------------------------------------------------------------------------- |
| **F ≈ 1**   | Group means are similar → fail to reject H₀                                  |
| **F >> 1**  | Between-group variance is much larger than within-group variance → reject H₀ |
| **p-value** | Probability of obtaining this F-ratio under H₀                               |

- If **p ≤ α** (commonly 0.05), reject H₀ — meaning at least one group differs significantly.
- However, ANOVA does **not** indicate _which_ groups differ; follow-up [**post-hoc tests**](#post-hoc-analysis) are required.
- With more groups → more pairwise comparisons → higher chance of Type I error (false positives). Adjustments are required.

## Python Example

```python
import pandas as pd
from scipy import stats
import pingouin as pg

group_1 = [23, 21, 19, 22, 20, 23, 21, 20, 22, 21]
group_2 = [30, 28, 29, 32, 31, 30, 33, 29, 30, 32]
group_3 = [25, 24, 23, 26, 25, 27, 24, 23, 22, 25]

# One-way ANOVA (scipy)
f_statistic, p_value = stats.f_oneway(group_1, group_2, group_3)
print(f_statistic, p_value)

# One-way ANOVA with pingouin
data = group_1 + group_2 + group_3
groups = (['Group 1'] * len(group_1) +
          ['Group 2'] * len(group_2) +
          ['Group 3'] * len(group_3))
df = pd.DataFrame({'data': data, 'group': groups})

pg.anova(data=df, dv="data", between="group")
```

## Two-Way ANOVA (Factorial ANOVA)

- **Purpose:** Tests the effect of **two independent variables (factors)** on a dependent variable, and whether there is an **interaction effect** between them.
- **Null hypotheses (H₀):**
  1. No main effect of Factor A.
  2. No main effect of Factor B.
  3. No interaction effect between Factor A and Factor B.

**Test statistic (for each factor):**
\[
F = \frac{MS*{\text{factor}}}{MS*{\text{error}}}
\]

- Interaction term tests whether the effect of one factor depends on the level of the other factor.

**Python Example (statsmodels):**

```python
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Example data
df = pd.DataFrame({
    "score": [85, 90, 78, 88, 76, 95, 89, 84],
    "treatment": ["A","A","B","B","A","A","B","B"],
    "gender": ["M","F","M","F","M","F","M","F"]
})

model = ols('score ~ C(treatment) * C(gender)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)
```

## Post-hoc Analysis

When ANOVA is significant, **post-hoc tests** identify which groups differ.

- **Purpose:** Perform pairwise comparisons while controlling for inflated Type I error (false positives) from multiple testing.
- **Common methods:**

### Tukey’s Honest Significant Difference (HSD) Test

```python
from statsmodels.stats.multicomp import pairwise_tukeyhsd

tukey_results = pairwise_tukeyhsd(df['data'], df['group'], alpha=0.05)
print(tukey_results)

# Example output:
# Tukey's HSD Test Results:
#    pairwise_comparisons  |   p-adj
#    --------------------------------
#     Group 1 vs Group 2   |  0.0024
#     Group 1 vs Group 3   |  0.10
#     Group 2 vs Group 3   |  0.03
```

### Bonferroni Correction

- Adjusts significance level when performing multiple t-tests.
- More conservative but reduces false positives.

```python
from statsmodels.stats.multitest import multipletests

comparisons = [('Group 1', 'Group 2'), ('Group 1', 'Group 3'), ('Group 2', 'Group 3')]
p_values = []

for group1, group2 in comparisons:
    group1_data = eval(group1.lower().replace(' ', '_'))
    group2_data = eval(group2.lower().replace(' ', '_'))
    t_stat, p_val = stats.ttest_ind(group1_data, group2_data)
    p_values.append(p_val)

corrected_p_values = multipletests(p_values, alpha=0.05, method='bonferroni')[1]

for (group1, group2), corrected_p_val in zip(comparisons, corrected_p_values):
    print(f"{group1} vs {group2}: corrected p-value = {corrected_p_val:.4f}")
```

## Effect Size in ANOVA

- Effect size measures the **strength of the relationship** between independent variables (factors) and the dependent variable in ANOVA.
- It complements the F-test and p-value, which only tell us whether an effect exists, by showing **how large or meaningful** the effect is.
- Always report effect size with ANOVA results to provide practical significance, not just statistical significance.

### Eta squared (η²)

\[
\eta^2 = \frac{SS*{\text{between}}}{SS*{\text{total}}}
\]

- **SS_between**: Sum of squares between groups (variation explained by the independent variable).
- **SS_total**: Total sum of squares (total variation in the data).
- Interpretation: Proportion of total variance in the dependent variable explained by the factor(s).
- Useful in one-way ANOVA.

### Partial eta squared (η²ₚ)

\[
\eta^2*p = \frac{SS*{\text{effect}}}{SS*{\text{effect}} + SS*{\text{error}}}
\]

- **SS_effect**: Sum of squares for the specific factor or interaction.
- **SS_error**: Sum of squares for the error (residuals).
- Interpretation: Proportion of variance explained by a particular factor, **controlling for other factors**.
- Commonly reported in **two-way ANOVA** or higher designs where multiple factors exist.
- Preferred in factorial ANOVA.

### Interpretation (Cohen’s guidelines)

- Small effect: η² ≈ 0.01
- Medium effect: η² ≈ 0.06
- Large effect: η² ≈ 0.14

📌 **Summary:**

- ANOVA tests whether there is a difference among groups, but not which groups differ.
- Post-hoc analysis (Tukey’s HSD, Bonferroni, etc.) is essential when ANOVA is significant.
- Always check assumptions (normality, independence, equal variances).
- Use `Welch’s ANOVA` if variances are unequal, or Kruskal–Wallis for non-parametric data.
