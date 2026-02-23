# Non-parametric Methods

**Non-parametric methods** are statistical techniques that do **not** assume the data follows a specific distribution (such as the normal distribution). They are based on ranks or signs rather than raw values, making them more flexible and robust when parametric assumptions fail.

> 📌 **核心原則**：Non-parametric 方法不代表「沒有假設」，而是假設更少、限制更寬鬆。當資料不符合常態性、樣本數極小、或有嚴重離群值時，這些方法是參數方法的替代選擇。

---

## When to Use Non-parametric Methods?

Before applying any test, check whether parametric assumptions hold. If **any** of the following conditions apply, consider a non-parametric alternative:

| Condition                                  | Why It Matters                                                         |
| ------------------------------------------ | ---------------------------------------------------------------------- |
| Data is clearly non-normal                 | Parametric tests (t-test, ANOVA) assume normality in small samples     |
| Sample size is very small (n < 30)         | Central Limit Theorem doesn't fully apply; normality can't be assumed  |
| Data is ordinal (e.g., Likert scale)       | Intervals between values are unequal — mean is not meaningful          |
| Severe outliers are present                | Outliers heavily distort means and variances                           |
| Variance is unequal across groups          | Homoscedasticity assumption of parametric tests is violated            |

> 💡 **Non-parametric vs Parametric**: Non-parametric methods generally have **lower statistical power** than their parametric counterparts when parametric assumptions *are* met. Use parametric methods when appropriate — non-parametric methods are the fallback, not the default.

---

## Overview of Topics

| #   | Section                                                                       | Parametric Equivalent       | Key Question Answered                                  |
| --- | ----------------------------------------------------------------------------- | --------------------------- | ------------------------------------------------------ |
| 1   | [**When & Why Non-parametric**](./1-when-and-why.md)                         | —                           | When should I abandon parametric methods?              |
| 2   | [**One-Sample & Paired Tests**](./2-one-sample-and-paired.md)                 | One-sample t-test, Paired t | Is this sample different from a known value or itself? |
| 3   | [**Two Independent Samples**](./3-two-independent-samples.md)                 | Independent t-test          | Do two groups differ?                                  |
| 4   | [**Multiple Groups: Kruskal-Wallis**](./4-kruskal-wallis.md)                  | One-way ANOVA               | Do three or more groups differ?                        |
| 5   | [**Categorical Association: Chi-Square**](./5-chi-square.md)                  | —                           | Are two categorical variables related?                 |
| 6   | [**Correlation: Spearman & Kendall**](./6-rank-correlation.md)                | Pearson r                   | How strongly are two variables related (non-linearly)? |

---

## Parametric vs Non-parametric: Quick Reference

| Goal                                      | Parametric Method       | Non-parametric Alternative          |
| ----------------------------------------- | ----------------------- | ------------------------------------ |
| Compare one sample to a known value       | One-sample t-test       | Wilcoxon Signed-Rank Test            |
| Compare two paired measurements           | Paired t-test           | Wilcoxon Signed-Rank Test            |
| Compare two independent groups            | Independent t-test      | Mann-Whitney U Test                  |
| Compare three or more groups              | One-way ANOVA           | Kruskal-Wallis Test                  |
| Post-hoc after multi-group comparison     | Tukey HSD               | Dunn's Test                          |
| Correlation between two variables         | Pearson r               | Spearman ρ, Kendall τ                |
| Association between two categorical vars  | —                       | Chi-Square Test                      |
| Test for goodness of fit                  | —                       | Chi-Square Goodness of Fit           |

---

## What's Inside Each Section

### 1. When & Why Non-parametric
- How to detect normality violations (visual + formal)
- The cost of using non-parametric methods (power loss)
- Decision flowchart: parametric or non-parametric?

### 2. One-Sample & Paired Tests
- **Sign Test**: simplest, uses only direction (+ or −)
- **Wilcoxon Signed-Rank Test**: uses magnitude of differences; the standard paired non-parametric test

### 3. Two Independent Samples
- **Mann-Whitney U Test** (Wilcoxon Rank-Sum): compares rank distributions of two independent groups
- Effect size: rank-biserial correlation

### 4. Multiple Groups: Kruskal-Wallis
- Extension of Mann-Whitney to 3+ groups
- **Dunn's Test** for post-hoc pairwise comparisons with correction
- Effect size: η² (eta squared)

### 5. Categorical Association: Chi-Square
- **Chi-Square Test of Independence**: are two categorical variables associated?
- **Chi-Square Goodness of Fit**: does observed frequency match expected distribution?
- **Fisher's Exact Test**: better alternative when sample sizes are small
- Effect size: Cramér's V

### 6. Rank Correlation
- **Spearman ρ**: rank-based correlation, detects monotonic relationships
- **Kendall τ**: concordance-based, better for small samples with ties
- When to use each vs Pearson r

---

## Visualization Quick Reference

| Chart                          | Best For                                              |
| ------------------------------ | ----------------------------------------------------- |
| Boxplot                        | Comparing group distributions visually                |
| Violin plot                    | Showing full distribution shape per group             |
| Ranked data scatter plot       | Visualizing rank-based relationships                  |
| Mosaic plot / grouped bar      | Visualizing categorical association                   |
| Q–Q plot + Shapiro-Wilk result | Assessing normality before choosing a method          |

---

## Key Takeaway

> Non-parametric methods answer the same questions as parametric ones — **but with fewer assumptions**.  
> Always check assumptions first. Use non-parametric methods when data violates normality, is ordinal, has small n, or contains severe outliers.  
> 先檢查假設，再選方法。Non-parametric 是工具箱中不可或缺的備用方案，但不是預設首選。
