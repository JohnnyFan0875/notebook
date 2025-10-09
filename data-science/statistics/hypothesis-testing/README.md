# Hypothesis Testing

Hypothesis testing is a framework to decide whether observed data provides enough evidence to reject a null hypothesis H₀.

## General Notes

- **Null hypothesis (H₀):** No effect or no difference.
- **Alternative hypothesis (Hₐ):** There is an effect or difference.
- **p-value:** Probability of observing the data (or something more extreme) if H₀ is true.
- **α (significance level):** Threshold (commonly 0.05) to decide whether to reject H₀.
- **Test statistic:** A standardized value (z, t, or F) used to compute the p-value.

## Assumptions

- **Randomness:** Samples are random subsets of larger populations
- **Independence:** Each observation is independent (except paired tests)
- **Sample size:** Large enough for the Central Limit Theorem (CLT) to apply

## Basic Concepts

| Concept                                                                   | Description                                                                                                                |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| [Significance & Confidence Levels](significance-and-confidence-levels.md) | Define how sure we are about our statistical conclusions by setting thresholds for error tolerance and certainty.          |
| [Confidence Intervals](confidence-interval.md)                            | Provide a range of values within which the true population parameter is likely to fall with a given level of confidence.   |
| [t-score vs z-score](t-z-score.md)                                        | Compare standardized test statistics that differ based on whether population variance is known or estimated from a sample. |
| [p-value](p-value.md)                                                     | Quantifies the probability of observing results at least as extreme as the data, assuming the null hypothesis is true.     |
| [Power & Effect Size](power-effect-size.md)                               | Measure a test’s ability to detect true effects and the magnitude of those effects in practical terms.                     |

## Parametric vs Non-parametric Tests

Statistical tests are broadly classified based on the assumptions they make about data distribution:

| Type                     | Description                                                                                                                         | Typical Examples                                                           |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Parametric Tests**     | Assume data follow a specific distribution (usually normal) and use parameters like mean and standard deviation to draw inferences. | t-test, ANOVA, z-test, Pearson correlation                                 |
| **Non-parametric Tests** | Make fewer assumptions about the data distribution and are suitable for ordinal or non-normal data.                                 | Mann–Whitney U, Wilcoxon signed-rank, Kruskal–Wallis, Spearman correlation |

**Key Points:**

- Use parametric tests when assumptions of normality and equal variance are met.
- Use non-parametric tests for skewed, ordinal, or small-sample data.
- Non-parametric methods analyze ranks or medians rather than means.

## Choosing the Right Test

The table below summarizes **which test to use** depending on study design, number of groups, and assumptions.

| Scenario                                 | Parametric Test                                                                                                                                            | Non-parametric / Exact Alternative                                                 | Notes                                             |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------- |
| One group mean vs population mean        | [One-sample t-test / z-test](./t-tests.md#one-sample-t-test)                                                                                               | –                                                                                  | z-test if σ known and n ≥ 30; otherwise t-test    |
| Two independent groups (equal variances) | [Independent two-sample t-test](./t-tests.md#two-sample-t-test-independent-samples)                                                                        | [Mann–Whitney U](./non-parametric-tests.md#mannwhitney-u-test-wilcoxonmannwhitney) | Use Welch’s t-test if variances unequal           |
| Two related groups (paired data)         | [Paired t-test](./t-tests.md#paired-sample-t-test-dependent-samples)                                                                                       | [Wilcoxon signed-rank](./non-parametric-tests.md#wilcoxon-signed-rank-test)        | Example: before–after measurements                |
| ≥ 3 independent groups                   | [One-way ANOVA](./anova.md)                                                                                                                                | [Kruskal–Wallis](./non-parametric-tests.md#kruskalwallis-test)                     | Post-hoc tests (Tukey, Bonferroni) if significant |
| Two factors (with interaction)           | [Two-way ANOVA](./anova.md#two-way-anova-factorial-anova)                                                                                                  | –                                                                                  | Report effect sizes (η², η²ₚ)                     |
| Categorical proportions (1 group)        | [One-sample proportion z-test](./proportion-tests.md#one-sample-proportion-test)                                                                           | [Exact Binomial Test](binomial-test.md)                                            | Large sample → z-test; small sample → binomial    |
| Categorical proportions (2 groups)       | [Two-sample proportion z-test](./proportion-tests.md#two-sample-proportion-test)                                                                           | [Fisher’s Exact Test](fisher-exact-test.md)                                        | Related: [odds-ratio](../odds-ratio.md)           |
| Categorical association (r×c table)      | [Chi-square test of independence](./chi-square.md#chi-square-test-of-independence)                                                                         | [Fisher’s Exact Test](fisher-exact-test.md) (for small counts)                     | df = (r−1)(c−1)                                   |
| Distribution fit                         | [Chi-square goodness-of-fit](./chi-square.md#chi-square-goodness-of-fit)                                                                                   | –                                                                                  | Tests if observed = expected distribution         |
| Equality of variances                    | [Levene’s](./variance-tests.md#levenes-test) / [Bartlett’s](./variance-tests.md#bartletts-test) / [Brown–Forsythe](./variance-tests.md#brownforsythe-test) | –                                                                                  | Levene for robustness, Bartlett for normal data   |

## Critical Notes

- Always check assumptions: normality, independence, equal variance.
- Use non-parametric or exact alternatives for small samples or non-normal data.
- Report: test name, statistic, degrees of freedom, p-value, and effect size (Cohen’s d, η², etc.).
- For multiple comparisons, apply corrections (Bonferroni, Tukey).
- For small-sample categorical data, prefer **Exact Binomial** or **Fisher’s Exact Test** over asymptotic z or χ² methods.
