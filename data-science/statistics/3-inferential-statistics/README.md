# Inferential Statistics

**Inferential statistics** uses sample data to draw conclusions about a larger population. Unlike descriptive statistics (which only summarizes what you observe), inferential statistics quantifies uncertainty and tests hypotheses — enabling you to make evidence-based decisions.

> 📌 **核心原則**：推論統計的核心是「用樣本推論母體」。我們永遠無法百分之百確定，但可以量化不確定性，並在可接受的錯誤率下做出結論。

---

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

---

## Overview of Topics

| #   | Section                                                                 | Level       | Key Questions Answered                                         |
| --- | ----------------------------------------------------------------------- | ----------- | -------------------------------------------------------------- |
| 1   | [**Sampling & Estimation**](./1-sampling-estimation.md)                 | Foundation  | How do we estimate population parameters from a sample?        |
| 2   | [**Confidence Intervals**](./2-confidence-intervals.md)                 | Core        | What range of values is the true parameter likely to fall in?  |
| 3   | [**Hypothesis Testing Framework**](./3-hypothesis-testing.md)           | Core        | How do we decide if an effect is real or due to chance?        |
| 4   | [**Common Statistical Tests**](./4-statistical-tests.md)               | Application | Which test do I use, and how do I run it in Python?            |

---

## What's Inside Each Section

### 1. Sampling & Estimation

- Population vs. sample — key terminology
- Sampling methods (random, stratified, cluster)
- Point estimates and why they're never exactly right
- The Central Limit Theorem — why sample means are normally distributed
- Standard Error (SE): how much estimates vary across samples

### 2. Confidence Intervals

- What a confidence interval (CI) actually means — and common misconceptions
- Constructing CIs for means and proportions
- How sample size and confidence level affect interval width
- Interpreting CIs vs. p-values

### 3. Hypothesis Testing Framework

- Null and alternative hypothesis (H₀ vs. H₁)
- p-value: what it is and what it is not
- Significance level (α) and how to choose it
- Type I error (false positive) and Type II error (false negative)
- Statistical power and effect size

### 4. Common Statistical Tests

Organized by data type and number of groups:

| Scenario                                 | Test                          |
| ---------------------------------------- | ----------------------------- |
| One sample mean vs. known value          | One-sample t-test             |
| Two independent group means              | Independent samples t-test    |
| Two related/paired group means           | Paired t-test                 |
| One proportion vs. known value           | One-proportion z-test         |
| Two proportions                          | Two-proportion z-test         |
| Association between categorical variables| Chi-square test of independence|

---

## Visualization Quick Reference

| Chart / Tool              | Best For                                              |
| ------------------------- | ----------------------------------------------------- |
| Error bar plot            | Visualizing point estimates with confidence intervals |
| Power curve               | Showing trade-off between sample size and power       |
| p-value distribution plot | Understanding null hypothesis behavior                |
| Sampling distribution     | Illustrating Central Limit Theorem                    |

---

## Key Concepts at a Glance

| Concept               | Symbol  | Plain Language                                                  |
| --------------------- | ------- | --------------------------------------------------------------- |
| Significance level    | α       | The maximum acceptable probability of a false positive          |
| p-value               | p       | Probability of seeing data this extreme if H₀ were true         |
| Confidence level      | 1 − α   | How often the interval would contain the true value if repeated |
| Standard Error        | SE      | How much a sample statistic varies from sample to sample        |
| Effect size           | d, r, η²| Magnitude of the effect, independent of sample size             |
| Statistical power     | 1 − β   | Probability of detecting a real effect when it exists           |

---

## Key Takeaway

> Inferential statistics answers: **"What can my sample tell me about the world?"**  
> Always pair a p-value with an effect size and confidence interval — a result can be statistically significant but practically meaningless (or vice versa).

---

**← Previous module:** [Descriptive Statistics](../descriptive-statistics/README.md)  
**Next module →:** Regression Analysis *(coming soon)*
