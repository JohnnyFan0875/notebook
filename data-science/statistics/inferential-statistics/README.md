# Inferential Statistics

**Inferential statistics** uses sample data to draw conclusions about a larger population. Unlike descriptive statistics (which only summarizes what you observe), inferential statistics quantifies uncertainty and tests hypotheses — enabling you to make evidence-based decisions.

Key point: Inferential statistics uses samples to say something about a population. We never get certainty, but we can quantify uncertainty and make decisions with explicit error rates.

## Start Here If...

This module is the right entry point when your question sounds like one of these:

- "How uncertain is this estimate?"
- "Could this observed difference be just noise?"
- "Which statistical test fits this design?"
- "How do I compare several groups without fooling myself?"

## Why This Order?

```
What is the population parameter I want to estimate?
        ↓
Estimate it with confidence intervals (Point Estimate + Uncertainty)
        ↓
Test a specific hypothesis (Is there a real effect, or just noise?)
        ↓
Understand the risks of being wrong (Type I & Type II errors)
        ↓
Choose the right test based on data type and assumptions
```

This order matters because **hypothesis testing without understanding confidence intervals and error types leads to misinterpretation** — the most common mistake in applied statistics.

In this notebook, ANOVA now lives inside inferential statistics because it is one of the core group-comparison frameworks in the same overall toolkit.

## Overview of Topics

| Section | Level | Key Questions Answered |
| ----------------------------------------------------------------------- | ----------- | -------------------------------------------------------------- |
| [**Sampling & Estimation**](./sampling-estimation.md) | Foundation | How do we estimate population parameters from a sample? |
| [**Confidence Intervals**](./confidence-intervals.md) | Core | What range of values is the true parameter likely to fall in? |
| [**Hypothesis Testing Framework**](./hypothesis-testing.md) | Core | How do we decide if an effect is real or due to chance? |
| [**ANOVA Overview**](./anova-overview.md) | Core | How do we compare three or more means in a structured way? |
| [**One-Way ANOVA**](./one-way-anova.md) | Application | Do three or more independent group means differ? |
| [**Two-Way ANOVA**](./two-way-anova.md) | Application | How do two factors and their interaction affect an outcome? |
| [**Repeated-Measures ANOVA**](./repeated-measures-anova.md) | Application | How do repeated observations from the same subject differ? |
| [**Post-hoc Tests & Effect Size**](./post-hoc-effect-size.md) | Application | Which groups differ, and how large is the effect? |
| [**Common Statistical Tests**](./statistical-tests.md) | Application | Which test do I use, and how do I run it in Python? |
| [**Assumption Checks**](./assumption-checks.md) | Application | How do I verify normality, equal variance, and independence? |

## What's Inside Each Section

### Sampling & Estimation

- Population vs. sample — key terminology
- Sampling methods (random, stratified, cluster)
- Point estimates and why they're never exactly right
- The Central Limit Theorem — why sample means are normally distributed
- Standard Error (SE): how much estimates vary across samples
- Bootstrap: estimating uncertainty by resampling

### Confidence Intervals

- What a confidence interval (CI) actually means — and common misconceptions
- Constructing CIs for means and proportions
- How sample size and confidence level affect interval width
- Interpreting CIs vs. p-values

### Hypothesis Testing Framework

- Null and alternative hypothesis (H₀ vs. H₁)
- p-value: what it is and what it is not
- Significance level (α) and how to choose it
- Type I error (false positive) and Type II error (false negative)
- Statistical power and effect size

### ANOVA

- Omnibus testing for three or more means
- One-way, two-way, and repeated-measures designs
- Post-hoc comparisons after a significant global test
- Effect sizes such as η² and partial η²

### Assumption Checks

- Three core assumptions: independence, normality, equal variance
- Normality: visual (histogram, Q–Q plot) + formal (Shapiro–Wilk, K–S, Anderson–Darling)
- Variance: Levene's, Bartlett's, Brown–Forsythe — when to use each
- Independence: Durbin–Watson (autocorrelation), Runs test (randomness)
- t-score vs. z-score — when to use each and how to compute critical values
- Full pre-test checklist

### Common Statistical Tests

Organized by data type and number of groups:

| Scenario | Test |
| ---------------------------------------- | ----------------------------- |
| One sample mean vs. known value | One-sample t-test |
| Two independent group means | Independent samples t-test |
| Two related/paired group means | Paired t-test |
| One proportion vs. known value | One-proportion z-test |
| Two proportions | Two-proportion z-test |
| Association between categorical variables | Chi-square test of independence |

## Visualization Quick Reference

| Chart / Tool | Best For |
| ------------------------- | ----------------------------------------------------- |
| Error bar plot | Visualizing point estimates with confidence intervals |
| Power curve | Showing trade-off between sample size and power |
| p-value distribution plot | Understanding null hypothesis behavior |
| Sampling distribution | Illustrating Central Limit Theorem |
| Bootstrap distribution | Showing uncertainty from resampling |

## Key Concepts at a Glance

| Concept | Symbol | Plain Language |
| --------------------- | ------- | --------------------------------------------------------------- |
| Significance level | α | The maximum acceptable probability of a false positive |
| p-value | p | Probability of seeing data this extreme if H₀ were true |
| Confidence level | 1 − α | How often the interval would contain the true value if repeated |
| Standard Error | SE | How much a sample statistic varies from sample to sample |
| Effect size | d, r, η² | Magnitude of the effect, independent of sample size |
| Statistical power | 1 − β | Probability of detecting a real effect when it exists |
| Bootstrap | — | Repeated resampling to estimate uncertainty |

## Key Takeaway

Inferential statistics answers: "What can my sample tell me about the world?" Always pair a p-value with an effect size and confidence interval — a result can be statistically significant but practically meaningless (or vice versa).

## Suggested Paths Through This Module

If you are studying for understanding:

1. sampling and estimation
2. confidence intervals
3. hypothesis testing
4. assumption checks
5. ANOVA and post-hoc comparisons

If you are solving a practical analysis problem:

1. identify the parameter or comparison you care about
2. inspect assumptions and study design
3. choose the test
4. report effect size and uncertainty with the result
