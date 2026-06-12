# Repeated-Measures ANOVA

**Repeated-measures ANOVA** compares means when the **same subjects** are measured under multiple conditions or across multiple time points.

Key point: Repeated measurements are not independent. The main advantage of repeated-measures designs is that each subject acts as their own partial control, which often reduces unexplained variability and increases power.

## When to Use

| Situation | Example |
| --------- | ------- |
| Same subject, multiple time points | before treatment, week 1, month 1 |
| Same subject, multiple conditions | placebo, low dose, high dose |
| Numerical outcome | blood pressure, score, reaction time |

If there are only two repeated measurements, a paired t-test is often enough. If there are missing repeated observations or more complex nesting, mixed models are usually better.

## Why Not Use One-Way ANOVA?

Standard one-way ANOVA assumes all observations are independent. Repeated-measures data violates that assumption because measurements from the same subject tend to be correlated.

Ignoring this structure can:

- underestimate or misrepresent error
- distort p-values
- waste the within-subject information that makes the design valuable

## Core Idea

Repeated-measures ANOVA partitions variability into:

- **between-subject variation**: stable differences across people
- **within-subject condition variation**: differences due to time or condition
- **residual variation**: leftover noise

This is why repeated-measures designs are often more efficient than independent-group designs.

## Hypotheses

For a within-subject factor with \(k\) conditions:

| Hypothesis | Meaning |
| ---------- | ------- |
| \(H_0\) | all condition means are equal |
| \(H_1\) | at least one condition mean differs |

## The Key Assumption: Sphericity

Sphericity means that the **variance of the pairwise differences** between conditions is roughly equal.

Examples of pairwise differences:

- condition 1 minus condition 2
- condition 1 minus condition 3
- condition 2 minus condition 3

If those difference variances are very unequal, the standard F test becomes too liberal.

| Assumption | Meaning | If violated |
| ---------- | ------- | ----------- |
| Sphericity | pairwise difference variances are similar | use Greenhouse-Geisser or Huynh-Feldt correction |

Tip: Sphericity is special to repeated-measures ANOVA. It is one of the main reasons this design has its own analysis framework.

## Example with Simulated Data

```python
import numpy as np
import pandas as pd
import pingouin as pg

rng = np.random.default_rng(42)
n_subjects = 20

rows = []
for subject in range(n_subjects):
    baseline = rng.normal(100, 8)
    scores = {
        "baseline": baseline + rng.normal(0, 3),
        "week_1": baseline - 4 + rng.normal(0, 3),
        "month_1": baseline - 8 + rng.normal(0, 3),
    }
    for condition, score in scores.items():
        rows.append({
            "subject": subject,
            "condition": condition,
            "score": score
        })

df = pd.DataFrame(rows)

result = pg.rm_anova(
    data=df,
    dv="score",
    within="condition",
    subject="subject",
    detailed=True
)
print(result)
```

## Checking Sphericity

```python
spher = pg.sphericity(data=df, dv="score", within="condition", subject="subject")
print(spher)
```

If sphericity is violated, look at the corrected p-values from Greenhouse-Geisser or Huynh-Feldt output rather than the uncorrected F test alone.

## Visualizing Repeated Data

Two plots are especially useful:

1. subject trajectories
2. mean profile with uncertainty

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 4))
sns.lineplot(
    data=df,
    x="condition",
    y="score",
    units="subject",
    estimator=None,
    alpha=0.25,
    color="gray"
)
sns.pointplot(
    data=df,
    x="condition",
    y="score",
    errorbar=("ci", 95),
    color="steelblue"
)
plt.title("Repeated Measurements by Subject")
plt.tight_layout()
plt.show()
```

Tip: Subject-level lines show whether the average trend is consistent across individuals or driven by only a few participants.

## Effect Size

Repeated-measures ANOVA commonly reports **partial eta squared**.

```python
print(result[["Source", "F", "p-unc", "ng2"]])
```

Depending on the package, you may see:

- `np2`: partial eta squared
- `ng2`: generalized eta squared

Tip: Generalized eta squared is often easier to compare across designs because it is less sensitive to the specific ANOVA structure.

## When to Prefer a Mixed Model

Repeated-measures ANOVA is useful, but it becomes restrictive when:

- there are missing observations
- observation times are uneven
- subjects have different numbers of measurements
- you need both within- and between-subject predictors

In those cases, a **linear mixed model** is usually the better framework.

## Alternatives

| Case | Better method |
| ---- | ------------- |
| Only two time points | paired t-test |
| Missing repeated observations | linear mixed model |
| Ordinal or highly non-normal repeated data | Friedman test |
| Time-varying slopes or irregular timing | mixed model / longitudinal model |

## Common Mistakes

| Mistake | Why it matters | Better approach |
| ------- | -------------- | --------------- |
| Treating repeated rows as independent | invalid standard errors | use repeated-measures methods |
| Ignoring sphericity | inflated Type I error | apply GG/HF correction |
| Reporting only omnibus significance | hides pattern across time | add plots and pairwise follow-up |
| Forcing complete-case ANOVA when many values are missing | wastes data and may bias results | consider mixed models |

## Reporting Template

```text
A repeated-measures ANOVA tested whether mean score changed across three visits.
There was a significant effect of condition,
F(2, 38) = 15.21, p < .001, generalized eta² = .24.
Scores decreased from baseline to week 1 and declined further by month 1.
Mauchly's test indicated that sphericity was not violated.
```

## Key Takeaways

| Concept | Key point |
| ------- | --------- |
| **Same subject, multiple measurements** | This is the core repeated-measures design |
| **Dependence is expected** | Repeated data should not be analyzed as independent groups |
| **Sphericity matters** | Use corrected p-values if it fails |
| **Plots are essential** | Subject trajectories often reveal the real pattern |
| **Mixed models are the flexible extension** | Especially for missing or irregular repeated data |
