# Post-hoc & Effect Size

ANOVA tells whether a difference exists somewhere. **Post-hoc tests** identify which groups differ, and **effect size** tells how large the difference is.

Key point: A significant ANOVA is only the start. You still need to answer two separate questions: which groups differ, and are those differences large enough to matter?

## Why ANOVA Alone Is Incomplete

Suppose a one-way ANOVA rejects:

\[
H_0:\ \mu_1 = \mu_2 = \mu_3
\]

This only tells you that **at least one** group mean differs. It does **not** tell you:

- whether group A differs from B
- whether B differs from C
- whether the observed difference is small or practically important

That is exactly why post-hoc testing and effect size reporting belong in the same workflow.

## Post-hoc Tests

| Method | Use When |
| ------ | -------- |
| Tukey HSD | Default after one-way ANOVA with equal variances |
| Games-Howell | Variances or sample sizes are unequal |
| Bonferroni | Conservative manual correction |
| Holm | Less conservative than Bonferroni; good default for many tests |

### Practical Decision Rule

| Situation | Recommended follow-up |
| --------- | --------------------- |
| Standard one-way ANOVA, variances roughly equal | Tukey HSD |
| Unequal variances or clearly unequal sample sizes | Games-Howell |
| A small number of planned comparisons | Holm or Bonferroni |
| Many exploratory pairwise tests | Holm or FDR-style control |

Tip: "Post-hoc" does not mean "optional after significance". If your research question is about specific group differences, the pairwise follow-up is part of the actual answer.

## Worked Example with a Built-in Dataset

The example below uses `seaborn`'s built-in `tips` dataset and compares `total_bill` across days of the week.

```python
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multicomp import pairwise_tukeyhsd

tips = sns.load_dataset("tips").dropna(subset=["total_bill", "day"])

# Omnibus ANOVA
anova_model = smf.ols("total_bill ~ C(day)", data=tips).fit()
anova_table = sm.stats.anova_lm(anova_model, typ=2)
print(anova_table)

# Post-hoc Tukey HSD
tukey = pairwise_tukeyhsd(
    endog=tips["total_bill"],
    groups=tips["day"],
    alpha=0.05
)
print(tukey)
```

### Reading a Tukey Table

Each row compares one pair of groups:

| Column | Meaning |
| ------ | ------- |
| `meandiff` | Difference in sample means |
| `p-adj` | Multiplicity-adjusted p-value |
| `lower`, `upper` | Simultaneous confidence interval for the difference |
| `reject` | Whether that pair is significant at the chosen alpha |

Tip: The confidence interval is often the most informative column. If it is narrow and far from zero, the pairwise difference is both statistically clear and directionally interpretable.

## Effect Size

| Measure | Formula | Use |
| ------- | ------- | --- |
| eta squared, eta2 | SS_between / SS_total | One-way ANOVA |
| partial eta squared, eta2p | SS_effect / (SS_effect + SS_error) | Two-way or repeated ANOVA |
| omega squared, omega2 | Bias-corrected eta2 | Better for small samples |

Common rule of thumb:

| Size | eta2 / eta2p |
| ---- | ------------ |
| Small | 0.01 |
| Medium | 0.06 |
| Large | 0.14 |

### Why Report More Than One Effect Size?

- `eta2` is easy to explain: proportion of total variance explained by group membership.
- `partial eta2` is common in factorial ANOVA because it isolates each effect relative to its own error term.
- `omega2` is often preferred for one-way ANOVA because it is less upward-biased in smaller samples.

## Computing Effect Sizes from ANOVA Output

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf
import seaborn as sns

tips = sns.load_dataset("tips").dropna(subset=["total_bill", "day"])

model = smf.ols("total_bill ~ C(day)", data=tips).fit()
anova = sm.stats.anova_lm(model, typ=2)

ss_between = anova.loc["C(day)", "sum_sq"]
ss_error = anova.loc["Residual", "sum_sq"]
ss_total = ss_between + ss_error
df_between = anova.loc["C(day)", "df"]
ms_error = anova.loc["Residual", "sum_sq"] / anova.loc["Residual", "df"]

eta2 = ss_between / ss_total
omega2 = (ss_between - df_between * ms_error) / (ss_total + ms_error)

print(f"eta²   = {eta2:.4f}")
print(f"omega² = {omega2:.4f}")
```

### Pairwise Effect Size

Once you identify the significant pairs, it is often useful to quantify each pairwise contrast with an effect size such as **Cohen's d**.

```python
import numpy as np

def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    s1, s2 = group1.std(ddof=1), group2.std(ddof=1)
    s_pooled = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
    return (group1.mean() - group2.mean()) / s_pooled

sat = tips.loc[tips["day"] == "Sat", "total_bill"]
sun = tips.loc[tips["day"] == "Sun", "total_bill"]

print(f"Cohen's d (Sat vs Sun) = {cohens_d(sat, sun):.3f}")
```

Tip: Omnibus effect size and pairwise effect size answer different questions. `eta2` describes the overall group structure; Cohen's d describes the size of a specific contrast.

## Visualizing Group Differences

Plots make post-hoc results easier to interpret than raw tables.

```python
import matplotlib.pyplot as plt
import scipy.stats as stats

summary = (
    tips.groupby("day")["total_bill"]
    .agg(["mean", "std", "count"])
    .assign(se=lambda d: d["std"] / np.sqrt(d["count"]))
)
summary["tcrit"] = stats.t.ppf(0.975, summary["count"] - 1)
summary["err"] = summary["tcrit"] * summary["se"]

plt.figure(figsize=(7, 4))
plt.errorbar(
    x=summary.index,
    y=summary["mean"],
    yerr=summary["err"],
    fmt="o",
    capsize=6,
    color="steelblue"
)
plt.ylabel("Mean total bill")
plt.title("Group Means with 95% Confidence Intervals")
plt.tight_layout()
plt.show()
```

Tip: This plot is useful for communication, but formal pairwise conclusions should still come from Tukey / Games-Howell / Holm-adjusted comparisons rather than visual overlap alone.

## Reporting Template

```text
A one-way ANOVA showed a significant group effect,
F(2, 27) = 18.42, p < .001, eta2 = .58.
Tukey post-hoc tests showed that group B was higher than groups A and C.
```

## Stronger Reporting Template

```text
A one-way ANOVA showed that mean total_bill differed by day,
F(3, 240) = 3.45, p = .018, eta2 = .041, omega2 = .028.
Tukey HSD indicated that Saturday was higher than Thursday
(mean difference = 3.21, 95% CI [0.44, 5.98], p-adj = .016, d = 0.42),
while the remaining pairwise contrasts were not statistically significant.
```

## Common Mistakes

| Mistake | Fix |
| ------- | --- |
| Stop after significant ANOVA | Run post-hoc tests |
| Report p-value only | Add effect size |
| Run many t-tests without correction | Use Tukey, Holm, or Bonferroni |
| Ignore unequal variance | Use Welch ANOVA or Games-Howell |
| Report only omnibus eta2 | Add pairwise effect sizes for meaningful contrasts |
