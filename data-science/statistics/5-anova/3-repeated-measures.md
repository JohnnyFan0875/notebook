# 3. Repeated Measures

**Repeated-measures ANOVA** compares means when the same subject is measured multiple times.

> 📌 **中文重點**：同一個人重複測量時，資料不是獨立的。不能把它當成一般 one-way ANOVA。

---

## When to Use

| Situation | Example |
| --------- | ------- |
| Same subject, multiple times | Before, after 1 week, after 1 month |
| Same subject, multiple conditions | Placebo, low dose, high dose |
| Numerical outcome | Blood pressure, test score, reaction time |

---

## Key Assumption

| Assumption | Meaning | If Violated |
| ---------- | ------- | ----------- |
| Sphericity | Differences between condition pairs have similar variance | Use Greenhouse-Geisser correction |

For beginners, remember the practical point: repeated data needs repeated-measures methods or mixed models.

---

## Python

```python
import pingouin as pg

# df columns: subject, condition, score
result = pg.rm_anova(
    data=df,
    dv="score",
    within="condition",
    subject="subject",
    detailed=True
)

print(result)
```

---

## Alternatives

| Case | Better Method |
| ---- | ------------- |
| Only two time points | Paired t-test |
| Missing repeated observations | Linear mixed model |
| Ordinal or highly non-normal data | Friedman test |

