# ANOVA

**ANOVA** compares means across three or more groups. It asks whether group differences are larger than the random variation within groups.

> 📌 **中文重點**：ANOVA 回答「至少有一組平均數不同嗎？」但不會直接告訴你是哪幾組不同。若 ANOVA 顯著，下一步一定要做 post-hoc test。

---

## Quick Guide

| Need | Use | Core Idea |
| ---- | --- | --------- |
| Compare 3+ independent groups | One-way ANOVA | One categorical factor |
| Test two factors together | Two-way ANOVA | Main effects + interaction |
| Same subject measured repeatedly | Repeated-measures ANOVA | Accounts for within-subject dependence |
| Find which groups differ | Post-hoc tests | Pairwise tests with p-value correction |

---

## Sections

| # | Section | Question |
|---|---------|----------|
| 1 | [One-Way ANOVA](./1-one-way-anova.md) | Do 3+ independent group means differ? |
| 2 | [Two-Way ANOVA](./2-two-way-anova.md) | Do two factors affect the outcome? |
| 3 | [Repeated Measures](./3-repeated-measures.md) | Do repeated measurements differ over time/condition? |
| 4 | [Post-hoc & Effect Size](./4-post-hoc-effect-size.md) | Which groups differ, and how large is the effect? |

---

## Must-Know Formula

$$F = \frac{MS_{between}}{MS_{within}}$$

| Term | Meaning |
| ---- | ------- |
| `MS_between` | Variation explained by group differences |
| `MS_within` | Random variation inside groups |
| Large F | Group means differ more than expected by noise |

---

## Assumptions

| Assumption | Check | If Violated |
| ---------- | ----- | ----------- |
| Independent observations | Study design | Use paired/repeated or mixed models |
| Approximate normality | Histogram, Q-Q plot, Shapiro-Wilk | Use Kruskal-Wallis or transform |
| Equal variances | Levene's test | Use Welch's ANOVA |

> 💡 **Practical default**：先畫 boxplot/violin plot，再跑 ANOVA。統計檢定前一定要先看分布。

