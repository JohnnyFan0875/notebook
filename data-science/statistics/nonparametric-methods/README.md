# Non-parametric Methods

**Non-parametric methods** are statistical techniques that do **not** assume the data follows a specific distribution (such as the normal distribution). They are based on ranks or signs rather than raw values, making them more flexible and robust when parametric assumptions fail.

Key point: Non-parametric does not mean assumption-free. It means the assumptions are weaker and often more robust when data is non-normal, ordinal, very small, or heavily affected by outliers.

## When to Use Non-parametric Methods?

Before applying any test, check whether parametric assumptions hold. If **any** of the following conditions apply, consider a non-parametric alternative:

| Condition | Why It Matters |
| ------------------------------------------ | ---------------------------------------------------------------------- |
| Data is clearly non-normal | Parametric tests (t-test, ANOVA) assume normality in small samples |
| Sample size is very small (n < 30) | Central Limit Theorem doesn't fully apply; normality can't be assumed |
| Data is ordinal (e.g., Likert scale) | Intervals between values are unequal — mean is not meaningful |
| Severe outliers are present | Outliers heavily distort means and variances |
| Variance is unequal across groups | Homoscedasticity assumption of parametric tests is violated |

Tip: Non-parametric vs Parametric: Non-parametric methods generally have lower statistical power than their parametric counterparts when parametric assumptions *are* met. Use parametric methods when appropriate — non-parametric methods are the fallback, not the default.

## Start Here If...

This module is especially relevant when:

- your sample is small and normality is doubtful
- your data are ordinal rather than truly numerical
- outliers are dominating mean-based summaries
- a standard t-test or ANOVA feels fragile for the data you actually have

## Overview of Topics

| Section | Parametric Equivalent | Key Question Answered |
| ----------------------------------------------------------------------------- | --------------------------- | ------------------------------------------------------ |
| [**When & Why Non-parametric**](./when-and-why.md) | — | When should I abandon parametric methods? |
| [**One-Sample & Paired Tests**](./one-sample-and-paired.md) | One-sample t-test, Paired t | Is this sample different from a known value or itself? |
| [**Two Independent Samples**](./two-independent-samples.md) | Independent t-test | Do two groups differ? |
| [**Multiple Groups: Kruskal-Wallis**](./kruskal-wallis.md) | One-way ANOVA | Do three or more groups differ? |
| [**Categorical Association: Chi-Square**](./chi-square.md) | — | Are two categorical variables related? |
| [**Correlation: Spearman & Kendall**](./rank-correlation.md) | Pearson r | How strongly are two variables related (non-linearly)? |

## Parametric vs Non-parametric: Quick Reference

| Goal | Parametric Method | Non-parametric Alternative |
| ----------------------------------------- | ----------------------- | ------------------------------------ |
| Compare one sample to a known value | One-sample t-test | Wilcoxon Signed-Rank Test |
| Compare two paired measurements | Paired t-test | Wilcoxon Signed-Rank Test |
| Compare two independent groups | Independent t-test | Mann-Whitney U Test |
| Compare three or more groups | One-way ANOVA | Kruskal-Wallis Test |
| Post-hoc after multi-group comparison | Tukey HSD | Dunn's Test |
| Correlation between two variables | Pearson r | Spearman ρ, Kendall τ |
| Association between two categorical vars | — | Chi-Square Test |
| Test for goodness of fit | — | Chi-Square Goodness of Fit |

## What's Inside Each Section

### When & Why Non-parametric
- How to detect normality violations (visual + formal)
- The cost of using non-parametric methods (power loss)
- Decision flowchart: parametric or non-parametric?

### One-Sample & Paired Tests
- **Sign Test**: simplest, uses only direction (+ or −)
- **Wilcoxon Signed-Rank Test**: uses magnitude of differences; the standard paired non-parametric test

### Two Independent Samples
- **Mann-Whitney U Test** (Wilcoxon Rank-Sum): compares rank distributions of two independent groups
- Effect size: rank-biserial correlation

### Multiple Groups: Kruskal-Wallis
- Extension of Mann-Whitney to 3+ groups
- **Dunn's Test** for post-hoc pairwise comparisons with correction
- Effect size: η² (eta squared)

### Categorical Association: Chi-Square
- **Chi-Square Test of Independence**: are two categorical variables associated?
- **Chi-Square Goodness of Fit**: does observed frequency match expected distribution?
- **Fisher's Exact Test**: better alternative when sample sizes are small
- Effect size: Cramér's V

### Rank Correlation
- **Spearman ρ**: rank-based correlation, detects monotonic relationships
- **Kendall τ**: concordance-based, better for small samples with ties
- When to use each vs Pearson r

## Visualization Quick Reference

| Chart | Best For |
| ------------------------------ | ----------------------------------------------------- |
| Boxplot | Comparing group distributions visually |
| Violin plot | Showing full distribution shape per group |
| Ranked data scatter plot | Visualizing rank-based relationships |
| Mosaic plot / grouped bar | Visualizing categorical association |
| Q–Q plot + Shapiro-Wilk result | Assessing normality before choosing a method |

## Key Takeaway

Non-parametric methods answer many of the same questions as parametric ones, but with weaker and often more robust assumptions. Check assumptions first, then switch to non-parametric methods when the data truly calls for them. They are an essential backup tool, not the automatic default.

## Deep-Study Priorities

The most useful order in this module is:

1. decide whether parametric assumptions are good enough
2. map the study design to the right rank-based alternative
3. interpret what the rank-based test is actually testing

Tip: Non-parametric does not mean assumption-free. It usually means different assumptions and a different target of inference.

## Quick Navigation Rule

If your main task is:

1. deciding whether you need a rank-based method at all: start with [When & Why Non-parametric](./when-and-why.md)
2. comparing one sample or paired measurements: go to [One-Sample & Paired Tests](./one-sample-and-paired.md)
3. comparing independent groups: go to [Two Independent Samples](./two-independent-samples.md) or [Kruskal-Wallis](./kruskal-wallis.md)
4. analyzing counts or categories: go to [Chi-Square](./chi-square.md)
