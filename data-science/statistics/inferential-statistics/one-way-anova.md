# One-Way ANOVA

**One-way ANOVA** tests whether the means of **three or more independent groups** are equal when there is **one categorical grouping factor** and **one numerical outcome**.

Key point: One-way ANOVA is an omnibus test. Its job is to answer "Is there evidence that at least one group mean differs?" It does not, by itself, tell you which groups differ or how large those differences are.

## Why Not Just Run Many t-tests?

If you compare three groups with pairwise t-tests:

- A vs B
- A vs C
- B vs C

you inflate the chance of a false positive. One-way ANOVA controls the overall Type I error rate for the global question before you move to post-hoc comparisons.

Tip: ANOVA is usually the correct first step whenever the design is "one factor, three or more groups, numerical outcome".

## When to Use

| Requirement | Example |
| ----------- | ------- |
| Numerical outcome | exam score, blood pressure, total bill |
| One categorical factor | treatment A/B/C, department, day of week |
| Independent groups | each subject appears in only one group |
| 3 or more levels | more than two means to compare |

If you have only two groups, a t-test is the simpler equivalent. If you have repeated measurements on the same subjects, use repeated-measures ANOVA or a mixed model instead.

## Hypotheses

| Hypothesis | Meaning |
| ---------- | ------- |
| $H_0: \mu_1 = \mu_2 = \cdots = \mu_k$ | all group means are equal |
| $H_1:$ at least one mean differs | not all group means are the same |

ANOVA answers only the global question. After a significant result, the next step is post-hoc testing.

## The Core Logic

ANOVA compares two types of variability:

1. **Between-group variation**: how far group means are from the overall mean
2. **Within-group variation**: how spread out observations are inside each group

If between-group variation is large relative to within-group variation, the groups are unlikely to all come from the same population mean.

\[
F = \frac{MS_{between}}{MS_{within}}
\]

| F value | Interpretation |
| ------- | -------------- |
| Around 1 | between-group variation is similar to within-group noise |
| Much greater than 1 | evidence that at least one mean differs |

## ANOVA Table Anatomy

| Source | Meaning |
| ------ | ------- |
| **Between / Factor** | variation explained by group membership |
| **Within / Residual** | unexplained variation inside groups |
| **df** | degrees of freedom |
| **SS** | sum of squares |
| **MS** | mean square = SS / df |
| **F** | ratio of explained to unexplained variation |
| **p-value** | evidence against equal group means |

## Assumptions

| Assumption | What it means | How to check |
| ---------- | ------------- | ------------ |
| Independence | observations do not influence each other | study design |
| Approximate normality within groups | each group's residual pattern is roughly normal | histogram, Q-Q plot |
| Homogeneity of variance | groups have similar variance | Levene's test, residual plots |

Tip: Independence is the most important assumption. Mild normality violations are often tolerable with moderate sample sizes, but dependence in the data can invalidate the analysis.

## Example with a Built-in Dataset

The example below compares `total_bill` across days in `seaborn`'s built-in `tips` dataset.

```python
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf

tips = sns.load_dataset("tips").dropna(subset=["total_bill", "day"])

# scipy version
groups = [g["total_bill"].to_numpy() for _, g in tips.groupby("day")]
f_stat, p_value = stats.f_oneway(*groups)
print(f"scipy one-way ANOVA: F = {f_stat:.4f}, p = {p_value:.4f}")

# statsmodels version gives the ANOVA table
model = smf.ols("total_bill ~ C(day)", data=tips).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)
```

## Reading the Result

Suppose the ANOVA p-value is below 0.05:

- you reject the claim that all means are equal
- you still do **not** know which pairs differ
- you should move to post-hoc testing such as Tukey HSD

If the p-value is above 0.05:

- you do not have strong evidence that the group means differ
- this is **not** proof that the means are identical
- the study may still be underpowered

## Effect Size

ANOVA should not be reported with a p-value alone. Add an effect size such as **eta squared** or **omega squared**.

\[
\eta^2 = \frac{SS_{between}}{SS_{total}}
\]

```python
ss_between = anova_table.loc["C(day)", "sum_sq"]
ss_within = anova_table.loc["Residual", "sum_sq"]
ss_total = ss_between + ss_within

eta2 = ss_between / ss_total
print(f"eta² = {eta2:.4f}")
```

Rule-of-thumb interpretation:

| eta² | Interpretation |
| ---- | -------------- |
| 0.01 | small |
| 0.06 | medium |
| 0.14 | large |

Tip: The effect size answers "How much of the total variation is explained by group membership?" That is a different question from statistical significance.

## Visualizing Group Means

```python
import matplotlib.pyplot as plt
import numpy as np

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

Tip: This plot is good for communication, but do not use visual CI overlap as a substitute for the formal ANOVA or post-hoc analysis.

## What to Do After ANOVA

| Situation | Next step |
| --------- | --------- |
| p < 0.05 and variances roughly equal | Tukey HSD |
| p < 0.05 and variances unequal | Welch ANOVA + Games-Howell |
| severe non-normality or ordinal outcome | Kruskal-Wallis |
| repeated observations on same subject | repeated-measures ANOVA or mixed model |

## Common Mistakes

| Mistake | Why it's a problem | Better approach |
| ------- | ------------------ | --------------- |
| Many pairwise t-tests without correction | inflates false positives | ANOVA first, then post-hoc |
| Reporting ANOVA p-value only | hides effect magnitude | add eta² / omega² |
| Ignoring unequal variance | F test can mislead | use Welch ANOVA |
| Treating non-significant ANOVA as proof of equality | absence of evidence is not evidence of absence | discuss uncertainty and power |

## Reporting Template

```text
A one-way ANOVA showed that mean total_bill differed across days,
F(3, 240) = 3.45, p = .018, eta² = .041.
Follow-up Tukey tests indicated that Saturday was higher than Thursday,
while the other pairwise contrasts were not statistically significant.
```

## Key Takeaways

| Concept | Key point |
| ------- | --------- |
| **One factor, 3+ groups** | This is the core use case for one-way ANOVA |
| **Omnibus test** | ANOVA tells whether at least one mean differs, not which ones |
| **F ratio** | Compares between-group variation to within-group noise |
| **Assumptions matter** | Especially independence and equal variance |
| **Post-hoc testing** | Required after a significant global result |
| **Effect size** | Always report more than the p-value |
