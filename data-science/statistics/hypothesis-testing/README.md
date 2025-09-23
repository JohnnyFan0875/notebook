# Hypothesis Testing

Hypothesis testing is a framework to decide whether observed data provides enough evidence to reject a null hypothesis \(H_0\).

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

## Choosing the Right Test

The table below summarizes **which test to use** depending on study design, number of groups, and assumptions.

| Scenario                                 | Parametric Test                        | Non-parametric Alternative        | Notes                                             |
| ---------------------------------------- | -------------------------------------- | --------------------------------- | ------------------------------------------------- |
| One group mean vs population mean        | One-sample **t-test** / **z-test**     | –                                 | z-test if σ known and n ≥ 30; otherwise t-test    |
| Two independent groups (equal variances) | Independent two-sample **t-test**      | Mann–Whitney U                    | Use Welch’s t-test if variances unequal           |
| Two related groups (paired data)         | Paired **t-test**                      | Wilcoxon signed-rank              | Example: before–after measurements                |
| ≥ 3 independent groups                   | One-way **ANOVA**                      | Kruskal–Wallis                    | Post-hoc tests (Tukey, Bonferroni) if significant |
| Two factors (with interaction)           | Two-way **ANOVA**                      | –                                 | Report effect sizes (η², η²ₚ)                     |
| Categorical proportions (1 group)        | One-sample **proportion z-test**       | Exact binomial test               | Large sample → z-test; small sample → binomial    |
| Categorical proportions (2 groups)       | Two-sample **proportion z-test**       | Fisher’s exact test               | Related: [odds-ratio.md](../odds-ratio.md)        |
| Categorical association (r×c table)      | **Chi-square test of independence**    | Fisher’s exact (for small counts) | df = (r−1)(c−1)                                   |
| Distribution fit                         | **Chi-square goodness-of-fit**         | –                                 | Tests if observed = expected distribution         |
| Equality of variances                    | Levene’s / Bartlett’s / Brown–Forsythe | –                                 | Levene for robustness, Bartlett for normal data   |

## Contents

- [Significance & Confidence Levels](significance-and-confidence-levels.md)

  - α (significance level), confidence level (1−α), familywise error, multiple testing corrections.

- [Confidence Intervals](confidence-interval.md)

  - CI formulas, margin of error, interpretation, analytical & simulation examples.

- [t-score vs z-score](t-z-score.md)

  - Standardization, formulas, critical values, when to use t vs z.

- [p-value](p-value.md)

  - Definition, decision rules, calculation from t/z, Python code, relation to power.

- [Power & Effect Size](power-effect-size.md)

  - Statistical power (1−β), determinants (n, effect size, α, variance), effect size measures (Cohen’s d, Pearson’s r, η²).

- [t-tests](t-tests.md)

  - One-sample, independent two-sample, paired t-tests; formulas, assumptions, Welch’s test, Python examples.

- [Proportion Tests](proportion-tests.md)

  - One-sample and two-sample z-tests for proportions, formulas, assumptions, Python examples.

- [ANOVA](anova.md)

  - One-way ANOVA, F-statistic, assumptions, post-hoc tests (Tukey HSD, Bonferroni), Python examples.

- [Variance Tests](variance-tests.md)

  - Homogeneity of variance, Levene’s test, Bartlett’s test, when to use Welch’s ANOVA/t-test.

- [Chi-square Tests](chi-square.md)

  - Test of independence (r×c tables), goodness-of-fit, expected frequencies, degrees of freedom, Python examples.

- [Non-parametric Tests](non-parametric-tests.md)
  - Wilcoxon signed-rank, Mann–Whitney U, Kruskal–Wallis; use cases when normality/equal variance assumptions fail.

## Critical Notes

- Always check assumptions: normality, independence, equal variance.
- Use non-parametric alternatives for small samples or non-normal data.
- Report: test name, statistic, degrees of freedom, p-value, and effect size (Cohen’s d, η², etc.).
- For multiple comparisons, apply corrections (Bonferroni, Tukey).
