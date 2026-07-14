# Introduction

**ANOVA** compares means across three or more groups. It asks whether group differences are larger than the random variation within groups.

Key point: ANOVA tells you whether at least one group mean differs, but it does not identify which groups differ. If the omnibus test is significant, follow it with an appropriate post-hoc comparison.

## Where ANOVA Fits in the Big Picture

ANOVA is part of the broader family of linear models. Conceptually, it is doing the same job as regression: explaining variation in a numerical outcome. The difference is that the predictors are categorical group labels rather than continuous covariates.

This is why ANOVA should not be memorized as an isolated recipe. It is better understood as a structured way to compare explained variation against unexplained variation.

## Quick Guide

| Need | Use | Core Idea |
| ---- | --- | --------- |
| Compare 3+ independent groups | One-way ANOVA | One categorical factor |
| Test two factors together | Two-way ANOVA | Main effects + interaction |
| Same subject measured repeatedly | Repeated-measures ANOVA | Accounts for within-subject dependence |
| Find which groups differ | Post-hoc tests | Pairwise tests with p-value correction |

## Sections

| Section | Question |
| --------- | ---------- |
| [One-Way ANOVA](./one-way-anova.md) | Do 3+ independent group means differ? |
| [Two-Way ANOVA](./two-way-anova.md) | Do two factors affect the outcome? |
| [Repeated-Measures ANOVA](./repeated-measures-anova.md) | Do repeated measurements differ over time or condition? |
| [Post-hoc & Effect Size](./post-hoc-effect-size.md) | Which groups differ, and how large is the effect? |

## Must-Know Formula

\[
F = \frac{MS_{between}}{MS_{within}}
\]

| Term | Meaning |
| ---- | ------- |
| `MS_between` | Variation explained by group differences |
| `MS_within` | Random variation inside groups |
| Large F | Group means differ more than expected by noise |

## Assumptions

| Assumption | Check | If Violated |
| ---------- | ----- | ----------- |
| Independent observations | Study design | Use paired/repeated or mixed models |
| Approximate normality | Histogram, Q-Q plot, Shapiro-Wilk | Use Kruskal-Wallis or transform |
| Equal variances | Levene's test | Use Welch's ANOVA |

Tip: Start with a boxplot or violin plot before running ANOVA. A quick visual check of the group distributions often catches problems before the formal test does.

## Interpretation Order

When reading ANOVA output, this order usually prevents confusion:

1. confirm the study design matches the ANOVA type
2. inspect group plots and sample sizes
3. read the omnibus F test
4. if significant, move to post-hoc comparisons
5. report an effect size, not just a p-value

Warning: A significant ANOVA result does not automatically imply a large or practically important difference. Always pair the test result with the observed group means and an effect-size measure.

## Common Mistakes

| Mistake | Why it is a problem |
| ------- | ------------------- |
| Running many t-tests instead of one ANOVA | Inflates Type I error |
| Interpreting ANOVA without checking plots | Can miss outliers, skew, or unequal spread |
| Reporting only p-values | Hides the size and direction of group differences |
| Ignoring unequal variances | Standard ANOVA can become unreliable |
