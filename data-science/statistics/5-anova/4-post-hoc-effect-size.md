# 4. Post-hoc & Effect Size

ANOVA tells whether a difference exists somewhere. **Post-hoc tests** identify which groups differ, and **effect size** tells how large the difference is.

> 📌 **中文重點**：p-value 只回答「有沒有證據」，effect size 才回答「差異有多大」。報告 ANOVA 時最好兩者都放。

---

## Post-hoc Tests

| Method | Use When |
| ------ | -------- |
| Tukey HSD | Default after one-way ANOVA with equal variances |
| Games-Howell | Variances or sample sizes are unequal |
| Bonferroni | Conservative manual correction |
| Holm | Less conservative than Bonferroni; good default for many tests |

```python
from statsmodels.stats.multicomp import pairwise_tukeyhsd

tukey = pairwise_tukeyhsd(
    endog=df["score"],
    groups=df["group"],
    alpha=0.05
)

print(tukey)
```

---

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

---

## Reporting Template

```text
A one-way ANOVA showed a significant group effect,
F(2, 27) = 18.42, p < .001, eta2 = .58.
Tukey post-hoc tests showed that group B was higher than groups A and C.
```

---

## Common Mistakes

| Mistake | Fix |
| ------- | --- |
| Stop after significant ANOVA | Run post-hoc tests |
| Report p-value only | Add effect size |
| Run many t-tests without correction | Use Tukey, Holm, or Bonferroni |
| Ignore unequal variance | Use Welch ANOVA or Games-Howell |

