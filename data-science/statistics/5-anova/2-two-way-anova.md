# 2. Two-Way ANOVA

**Two-way ANOVA** tests two categorical factors at the same time and checks whether they interact.

> 📌 **中文重點**：Two-way ANOVA 不只看 A 因子和 B 因子各自有沒有影響，也看「A 的效果是否會因 B 的組別而改變」。

---

## Effects

| Effect | Question |
| ------ | -------- |
| Main effect A | Does factor A affect the outcome? |
| Main effect B | Does factor B affect the outcome? |
| Interaction A x B | Does the effect of A depend on B? |

---

## When to Use

| Requirement | Example |
| ----------- | ------- |
| Numerical outcome | Score, sales, recovery time |
| Two categorical factors | Treatment and gender |
| Independent observations | Each row is one independent subject |
| Need interaction insight | Treatment works differently by subgroup |

---

## Python

```python
import statsmodels.api as sm
from statsmodels.formula.api import ols

model = ols("score ~ C(treatment) * C(gender)", data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)
```

---

## Interpretation Order

| Step | Why |
| ---- | --- |
| Check interaction first | It changes how main effects should be read |
| If interaction is significant | Compare simple effects within each subgroup |
| If interaction is not significant | Interpret main effects more directly |

> ⚠️ **Common mistake**：若 interaction 顯著，不要只報告 main effect。這時候平均效果可能會掩蓋不同 subgroup 的差異。

