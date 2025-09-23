# Significance and Confidence Level

## Significance Level (α)

The **significance level (α)** is a threshold used in hypothesis testing to decide whether to reject the null hypothesis \(H_0\).

### Definition

- **α (alpha):** The probability of rejecting the null hypothesis when it is actually true.  
  → This is a **Type I error** (false positive).
- It represents the **risk you are willing to take** of making a false positive error.
- The value of α is determined **before** running the test.

Common choices:

- α = 0.05 (5% risk)
- α = 0.01 (1% risk)

### Relationship with Confidence Level

- Confidence level = \(1 − α\).
- Example: If α = 0.05 → confidence level = 95%.
- Interpretation: If the study were repeated many times, about 95% of confidence intervals would contain the true parameter.

### Familywise Error Rate (Multiple Tests)

When performing multiple hypothesis tests, the chance of at least one false positive increases.

- Probability of **not** making a false positive in one test: \(1 − α\).
- Probability of **not** making a false positive in all \(k\) tests: \((1 − α)^k\).
- Probability of making **at least one false positive** across \(k\) tests:  
  \[
  1 − (1 − α)^k
  \]

### Choosing α

- **Exploratory studies:** Higher α (0.1) may be acceptable.
- **Confirmatory or critical studies (e.g., clinical trials):** Lower α (0.01 or 0.001) is preferred.
- Always justify your chosen α level in the study context.

### Summary

- α sets the decision threshold for rejecting \(H_0\).
- Smaller α reduces false positives but increases the chance of false negatives (Type II error).
- Balance between Type I and Type II errors depends on the research question.

## Confidence Level (1 − α)

The **confidence level** represents the degree of certainty that a particular estimate includes the true population parameter.

### Definition

- Confidence level = \(1 − α\), where α is the significance level.
- Common choices:
  - 95% confidence level → α = 0.05
  - 99% confidence level → α = 0.01
- Interpretation:
  - If we repeat the same study many times, approximately 95% (or 99%) of the calculated confidence intervals would contain the true parameter.
  - It does **not** mean that there is a 95% probability the true parameter is in a specific interval (the parameter is fixed, the interval varies).

### Confidence Interval of the Mean

- Please refer to [confidence interval](confidence-interval.md#formula-for-the-mean)
