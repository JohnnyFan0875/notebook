# 1. One-Way ANOVA

**One-way ANOVA** compares the means of three or more independent groups using one categorical factor.

> 📌 **中文重點**：One-way ANOVA 適合「一個分組變數、三組以上、結果是數值型」的情境。

---

## When to Use

| Requirement | Example |
| ----------- | ------- |
| Numerical outcome | Test score, revenue, blood pressure |
| One categorical factor | Treatment group A/B/C |
| Independent groups | Each person belongs to only one group |
| 3+ groups | More than two means to compare |

---

## Hypotheses

| Hypothesis | Meaning |
| ---------- | ------- |
| H0: all means are equal | No group mean differs |
| H1: at least one mean differs | Some group mean is different |

ANOVA does **not** tell which groups differ. Use post-hoc tests after a significant result.

---

## Core Formula

$$F = \frac{MS_{between}}{MS_{within}}$$

| F value | Interpretation |
| ------- | -------------- |
| F around 1 | Group means are similar |
| F much larger than 1 | Evidence that at least one group differs |

---

## Python

```python
from scipy import stats
import pandas as pd
import pingouin as pg

group_a = [23, 21, 19, 22, 20, 23, 21, 20, 22, 21]
group_b = [30, 28, 29, 32, 31, 30, 33, 29, 30, 32]
group_c = [25, 24, 23, 26, 25, 27, 24, 23, 22, 25]

f_stat, p_value = stats.f_oneway(group_a, group_b, group_c)
print(f"F = {f_stat:.4f}, p = {p_value:.4f}")

df = pd.DataFrame({
    "score": group_a + group_b + group_c,
    "group": ["A"] * 10 + ["B"] * 10 + ["C"] * 10
})

print(pg.anova(data=df, dv="score", between="group", detailed=True))
```

---

## Decision Guide

| Result | Next Step |
| ------ | --------- |
| p < 0.05 | Run post-hoc tests |
| p >= 0.05 | Report no clear evidence of mean difference |
| Variances unequal | Use Welch's ANOVA |
| Data ordinal or very non-normal | Use Kruskal-Wallis |

