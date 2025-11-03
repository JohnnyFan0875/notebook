# Hypothesis Testing

Hypothesis testing is a framework to decide whether observed data provides enough evidence to reject a null hypothesis H₀.

## General Notes

- **Null hypothesis (H₀):** No effect or no difference.
- **Alternative hypothesis (Hₐ):** There is an effect or difference.
- **Test statistic:** A standardized value (z, t, or F) used to compute the p-value.
- **Central Limit Theorem (CLT)**: When the sample size is sufficiently large (typically n ≥ 30), the sampling distribution of the sample mean approximates a normal distribution, regardless of the population’s original shape.

## Type I and Type II Errors

| Concept            | True Condition         | Test Result                                | Interpretation                     | Type                  |
| ------------------ | ---------------------- | ------------------------------------------ | ---------------------------------- | --------------------- |
| **True Positive**  | Hₐ (difference exists) | Reject H₀ (conclude difference exists)     | Correctly detects a real effect    | Correct               |
| **False Positive** | H₀ (no difference)     | Reject H₀ (conclude difference exists)     | Incorrectly concludes a difference | **Type I error (α)**  |
| **True Negative**  | H₀ (no difference)     | Fail to reject H₀ (conclude no difference) | Correctly concludes no difference  | Correct               |
| **False Negative** | Hₐ (difference exists) | Fail to reject H₀ (conclude no difference) | Fails to detect a real effect      | **Type II error (β)** |

## Assumptions

- **Randomness:** Samples are random subsets of larger populations
- **Independence:** Each observation is independent (except paired tests)
- **Sample size:** Large enough for the Central Limit Theorem (CLT) to apply

## Basic Concepts

| Term                                                                                  | Meaning                                                                                                                                                 | Note                                                             |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| [Significance (α)](significance-levels.md) | Determines how much probability of error (Type I error) is acceptable.                                       | Affects the setting of confidence intervals and critical values. |
| [t-score vs z-score](t-z-score.md)                                                    | How many standard errors the sample mean (or observation) is away from the population mean                                                              | Used for calculating p-values and confidence intervals.          |
| [F-score](anova.md#test-statistic)                                                    | Ratio of variances that compares explained variability (between groups or model) to unexplained variability (within groups or residuals).               | Used in ANOVA and regression to test overall model significance. |
| [p-value](p-value.md)                                                                 | Measures the probability of observing such an extreme result assuming H₀ is true; compared against α to decide whether to reject H₀.                    | Related to statistical power (1 − β).                            |
| [Power & Effect Size](power-effect-size.md)                                           | Power = 1 − β represents the probability of correctly rejecting H₀ when it is false; effect size describes how large or meaningful the difference is.   | Provides practical interpretation of statistical results.        |
| [Odds Ratio (OR)](odds-ratio.md)                                                      | Ratio of the odds of an event occurring in one group to the odds in another group; quantifies the strength of association between exposure and outcome. | Commonly used in case–control studies and logistic regression.   |

## Choosing the Right Test

Selecting the correct test depends on:

- the **type of dependent variable** (continuous vs categorical),
- whether assumptions like **normality** and **equal variances** are met,
- whether data are **independent or paired**.

### Assumption Tests (Diagnostic Tests)

Before choosing a statistical test, it’s essential to check whether your data meet key assumptions such as **normality**, **equal variances**, and **independence**. These are diagnostic checks — not hypothesis tests themselves.

| Assumption                        | Test(s)                                                                                                                                            | Purpose                                     | Recommended Use                           |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- | ----------------------------------------- |
| **Normality**                     | [Shapiro–Wilk](normality-tests.md#shapirowilk-test), [K–S test](normality-tests.md#kolmogorovsmirnov-test)                                         | Tests if data follow a normal distribution. | Shapiro–Wilk for small to medium samples. |
| **Equal variances (homogeneity)** | [Levene’s](variance-tests.md#levenes-test), [Brown–Forsythe](variance-tests.md#brownforsythe-test), [Bartlett’s](variance-tests.md#bartletts-test) | Tests equality of variances across groups.  | Use Bartlett only if normality is met.    |
| **Independence**                  | – (usually by design); optionally **Durbin–Watson** or **Runs test**                                                                               | Ensures each observation is independent.    | For time-series or repeated-measure data. |

**Note:**  
If assumptions are violated, use non-parametric alternatives (Mann–Whitney, Kruskal–Wallis, etc.) or robust methods (Welch’s ANOVA).

### Continuous or Ordinal Data

Used when the dependent variable is **numeric (interval/ratio)** or **ordinal (ordered category)**.

#### Parametric vs Non-parametric Tests

Statistical tests are broadly classified based on the assumptions they make about data distribution:

| Type                     | Description                                                                                                                                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Parametric Tests**     | Assume data follow a specific distribution (usually normal) and rely on parameters like mean and standard deviation. Use when normality and equal variance assumptions are met; generally more powerful when valid. |
| **Non-parametric Tests** | Make minimal distributional assumptions and are suitable for ordinal, skewed, or small-sample data. Use when data violate parametric assumptions; analyze medians or ranks rather than means.                       |

#### Common Tests

| Scenario                                 | Parametric Test                                                                     | Non-parametric / Exact Alternative                                                                     | Notes                                             |
| ---------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| One group mean vs population mean        | [One-sample t-test / z-test](./t-tests.md#one-sample-t-test)                        | [One-Sample Wilcoxon Signed-Rank Test](./non-parametric-tests.md#one-sample-wilcoxon-signed-rank-test) | z-test if σ known and n ≥ 30; otherwise t-test    |
| Two independent groups (equal variances) | [Independent two-sample t-test](./t-tests.md#two-sample-t-test-independent-samples) | [Mann–Whitney U](./non-parametric-tests.md#mannwhitney-u-test-wilcoxonmannwhitney)                     | Use Welch’s t-test if variances unequal           |
| Two related groups (paired data)         | [Paired t-test](./t-tests.md#paired-sample-t-test-dependent-samples)                | [Wilcoxon signed-rank](./non-parametric-tests.md#wilcoxon-signed-rank-test)                            | Example: before–after measurements                |
| ≥ 3 independent groups                   | [One-way ANOVA](./anova.md)                                                         | [Kruskal–Wallis](./non-parametric-tests.md#kruskalwallis-test)                                         | Post-hoc tests (Tukey, Bonferroni) if significant |
| Two factors (with interaction)           | [Two-way ANOVA](./anova.md#two-way-anova-factorial-anova)                           | Aligned Rank Transform ANOVA (ART ANOVA) / PERMANOVA                                                   | Report effect sizes (η², η²ₚ)                     |

### Categorical or Count Data

Used when the dependent variable is **categorical (nominal)** or represents **counts or proportions**.  
Tests are based on binomial or multinomial distributions — no assumption of normality.

#### Common Tests

| Scenario                                                      | Common Test                                                                                                                                                                        | Type                  |
| ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| One group proportion                                          | [Exact Binomial Test](./exact-test.md#exact-binomial-test) / [One-sample proportion z-test](./proportion-tests.md#one-sample-proportion-test)                                      | Exact / Approximation |
| Two group proportions                                         | [Fisher’s Exact Test](./exact-test.md#fishers-exact-test) / [Two-sample proportion z-test](./proportion-tests.md#two-sample-proportion-test)                                       | Exact / Approximation |
| Association between two categorical variables (r×c table)     | [Chi-square Test of Independence](./chi-square.md#chi-square-test-of-independence) / [Fisher’s Exact Test](./exact-test.md#association-between-two-categorical-variables-rc-table) | Approximation / Exact |
| Goodness-of-fit (observed vs expected frequency distribution) | [Chi-square Goodness-of-Fit](./chi-square.md#chi-square-goodness-of-fit)                                                                                                           | Approximation         |

#### Exact vs Approximation

| Type              | Typical Distribution      | Meaning                                                                                | Example Tests                  | Recommended When                  |
| ----------------- | ------------------------- | -------------------------------------------------------------------------------------- | ------------------------------ | --------------------------------- |
| **Exact**         | Binomial / Hypergeometric | Compute the _true probability (p-value)_ using the exact discrete distribution         | Exact Binomial, Fisher’s Exact | Small sample, low expected counts |
| **Approximation** | Normal / Chi-square       | Use a _continuous approximation_ (e.g., normal or chi-square) to estimate the p-value. | Proportion z-test, Chi-square  | Large sample, expected counts ≥ 5 |

## Critical Notes

- Always check assumptions: normality, independence, equal variance.
- Use non-parametric or exact alternatives for small samples or non-normal data.
- For multiple comparisons, apply corrections (Bonferroni, Tukey).
- For small-sample categorical data, prefer **Exact Binomial** or **Fisher’s Exact Test** over asymptotic z or χ² methods.
