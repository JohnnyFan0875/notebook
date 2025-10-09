# Hypothesis Testing

Hypothesis testing is a framework to decide whether observed data provides enough evidence to reject a null hypothesis H₀.

## General Notes

- **Null hypothesis (H₀):** No effect or no difference.
- **Alternative hypothesis (Hₐ):** There is an effect or difference.
- **p-value:** Probability of observing the data (or something more extreme) if H₀ is true.
- **α (significance level):** Threshold (commonly 0.05) to decide whether to reject H₀.
- **Test statistic:** A standardized value (z, t, or F) used to compute the p-value.

## Type I and Type II Errors

| 概念               | 真實狀況    | 檢定結果               | 結果解釋           | 類型                  |
| ------------------ | ----------- | ---------------------- | ------------------ | --------------------- |
| **True Positive**  | Hₐ (有差異) | 拒絕 H₀ (認為有差異)   | 正確偵測到效果存在 | 正確                  |
| **False Positive** | H₀ (無差異) | 拒絕 H₀ (認為有差異)   | 錯誤地以為有差異   | **Type I error (α)**  |
| **True Negative**  | H₀ (無差異) | 不拒絕 H₀ (認為無差異) | 正確判定無差異     | 正確                  |
| **False Negative** | Hₐ (有差異) | 不拒絕 H₀ (認為無差異) | 錯誤地忽略真實差異 | **Type II error (β)** |

## Assumptions

- **Randomness:** Samples are random subsets of larger populations
- **Independence:** Each observation is independent (except paired tests)
- **Sample size:** Large enough for the Central Limit Theorem (CLT) to apply

## Basic Concepts

- [Significance (α) & Confidence Levels (1 - α)](significance-and-confidence-levels.md)
- [Confidence Intervals (CI)](confidence-interval.md)
- [t-score vs z-score](t-z-score.md)
- [p-value](p-value.md)
- [Power & Effect Size](power-effect-size.md)

## Parametric vs Non-parametric Tests

Statistical tests are broadly classified based on the assumptions they make about data distribution:

| Type                     | Description                                                                                                                                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Parametric Tests**     | Assume data follow a specific distribution (usually normal) and rely on parameters like mean and standard deviation. Use when normality and equal variance assumptions are met; generally more powerful when valid. |
| **Non-parametric Tests** | Make minimal distributional assumptions and are suitable for ordinal, skewed, or small-sample data. Use when data violate parametric assumptions; analyze medians or ranks rather than means.                       |

## Choosing the Right Test

The table below summarizes **which test to use** depending on study design, number of groups, and assumptions.

| Scenario                                 | Parametric Test                                                                                                                                            | Non-parametric / Exact Alternative                                                 | Notes                                                 |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------- |
| One group mean vs population mean        | [One-sample t-test / z-test](./t-tests.md#one-sample-t-test)                                                                                               | –                                                                                  | z-test if σ known and n ≥ 30; otherwise t-test        |
| Two independent groups (equal variances) | [Independent two-sample t-test](./t-tests.md#two-sample-t-test-independent-samples)                                                                        | [Mann–Whitney U](./non-parametric-tests.md#mannwhitney-u-test-wilcoxonmannwhitney) | Use Welch’s t-test if variances unequal               |
| Two related groups (paired data)         | [Paired t-test](./t-tests.md#paired-sample-t-test-dependent-samples)                                                                                       | [Wilcoxon signed-rank](./non-parametric-tests.md#wilcoxon-signed-rank-test)        | Example: before–after measurements                    |
| ≥ 3 independent groups                   | [One-way ANOVA](./anova.md)                                                                                                                                | [Kruskal–Wallis](./non-parametric-tests.md#kruskalwallis-test)                     | Post-hoc tests (Tukey, Bonferroni) if significant     |
| Two factors (with interaction)           | [Two-way ANOVA](./anova.md#two-way-anova-factorial-anova)                                                                                                  | –                                                                                  | Report effect sizes (η², η²ₚ)                         |
| Categorical proportions (1 group)        | [One-sample proportion z-test](./proportion-tests.md#one-sample-proportion-test)                                                                           | [Exact Binomial Test](binomial-test.md)                                            | Large sample → z-test; small sample → binomial        |
| Categorical proportions (2 groups)       | [Two-sample proportion z-test](./proportion-tests.md#two-sample-proportion-test)                                                                           | [Fisher’s Exact Test](fisher-exact-test.md)                                        | Related: [odds-ratio](../odds-ratio.md)               |
| Categorical association (r×c table)      | [Chi-square test of independence](./chi-square.md#chi-square-test-of-independence)                                                                         | [Fisher’s Exact Test](fisher-exact-test.md)                                        | df = (r−1)(c−1). Fisher's Exact Test for small counts |
| Distribution fit                         | [Chi-square goodness-of-fit](./chi-square.md#chi-square-goodness-of-fit)                                                                                   | –                                                                                  | Tests if observed = expected distribution             |
| Equality of variances                    | [Levene’s](./variance-tests.md#levenes-test) / [Bartlett’s](./variance-tests.md#bartletts-test) / [Brown–Forsythe](./variance-tests.md#brownforsythe-test) | –                                                                                  | Levene for robustness, Bartlett for normal data       |

## Critical Notes

- Always check assumptions: normality, independence, equal variance.
- Use non-parametric or exact alternatives for small samples or non-normal data.
- For multiple comparisons, apply corrections (Bonferroni, Tukey).
- For small-sample categorical data, prefer **Exact Binomial** or **Fisher’s Exact Test** over asymptotic z or χ² methods.
