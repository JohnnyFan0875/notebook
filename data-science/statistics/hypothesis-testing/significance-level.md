# Significance

The **significance level (α)** is a threshold used in hypothesis testing to decide whether to reject the null hypothesis $H_0$.  
接受多大的機率誤判。

## Definition

- **α (alpha):** The probability of rejecting the null hypothesis when it is actually true.  
  → This is a [**Type I error**](./README.md#type-i-and-type-ii-errors) (false positive).
- It represents the **risk you are willing to take** of making a false positive error.
- The value of α is determined **before** running the test.

Common choices:

- α = 0.05 (5% risk)
- α = 0.01 (1% risk)

## Familywise Error Rate (Multiple Tests)

When performing multiple hypothesis tests, the chance of at least one false positive increases.

- Probability of **not** making a false positive in one test: $1 − α$.
- Probability of **not** making a false positive in all $k$ tests: $(1 − α)^k$.
- Probability of making **at least one false positive** across $k$ tests: $1 − (1 − α)^k $

## Choosing α

- **Exploratory studies:** Higher α (e.g. 0.1) may be acceptable.
- **Confirmatory or critical studies (e.g., clinical trials):** Lower α (e.g. 0.01 or 0.001) is preferred.
- Always justify your chosen α level in the study context.

## Direction of the Test

The allocation of α depends on the alternative hypothesis:

| Test type             | Alternative hypothesis ($H_a$) | Tail(s) considered | How α is distributed   | Typical critical value (Z)         |
| --------------------- | ------------------------------ | ------------------ | ---------------------- | ---------------------------------- |
| **Right-tailed test** | $μ > μ_0$                      | Right tail only    | Entire α on right side | $z_{0.95} = +1.645$ (for α = 0.05) |
| **Left-tailed test**  | $μ < μ_0$                      | Left tail only     | Entire α on left side  | $z_{0.05} = −1.645$ (for α = 0.05) |
| **Two-tailed test**   | $μ ≠ μ_0$                      | Both tails         | α/2 on each side       | $z_{0.975} = ±1.96$ (for α = 0.05) |

- Right-sided test: looks for results significantly larger than expected.
- Left-sided test: looks for results significantly smaller than expected.
- Two-sided test: detects any significant difference, whether higher or lower.

Visually, α represents the **shaded area(s)** in the distribution tail(s) used to determine statistical significance.

<p align="center">
  <img src="https://analystprep.com/cfa-level-1-exam/wp-content/uploads/2019/08/page-171.jpg" width="450" height="300">
  <img src="https://analystprep.com/cfa-level-1-exam/wp-content/uploads/2019/08/page-172a.jpg" width="450" height="300">
  <img src="https://analystprep.com/cfa-level-1-exam/wp-content/uploads/2019/08/page-172a.jpg" width="450" height="300">
</p>

## Relationship with Confidence Level (1 − α)

The **confidence level** represents the degree of certainty that a particular estimate includes the true population parameter.

- Plase refer to [confidence level](../inferential-statistics/confidence-interval.md)
- Please refer to [confidence interval](../inferential-statistics/confidence-interval.md)

## Summary

- α sets the decision threshold for rejecting $H_0$.
- Smaller α reduces false positives but increases the chance of false negatives (Type II error).
- Balance between Type I and Type II errors depends on the research question.
