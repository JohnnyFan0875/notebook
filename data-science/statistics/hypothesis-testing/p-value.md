# p-value

The **p-value** is a probability that helps evaluate evidence against the null hypothesis \(H_0\).

## Definition

- The probability of obtaining a result at least as extreme as the one observed, **assuming \(H_0\) is true**.
- Provides a measure of evidence **against \(H_0\)**.
- Reference: [towardsdatascience](https://towardsdatascience.com/what-is-p-value-370056b8244d/)

## Decision Rule

- If **p ≤ α** → Reject the null hypothesis (evidence is strong against \(H_0\)).
- If **p > α** → Fail to reject the null hypothesis (evidence is weak against \(H_0\)).

## Example (using z-score)

- Suppose confidence level = 95% → significance level α = 0.05.
- Critical z-values: \(\pm 1.96\).
- If observed z-score = 2 (right-tailed):
  - The area beyond z=2 is smaller than beyond z=1.96.
  - So \(p < α = 0.05\).
  - Specifically, \(p ≈ 0.025\) (2.5% in right tail).
  - → Reject \(H_0\).

📌 **Caution:**

- A small p-value ≠ probability that \(H_0\) is false.
- A large p-value does not prove \(H_0\) true — it means insufficient evidence to reject.

## Formulas

For a test statistic \(T\) under the null distribution:

\[
p = P(\; T \;\geq\; T\_{obs} \;|\; H_0 \text{ is true})
\]

- **Right-tailed:**  
  \[
  p = P(T \geq t\_{obs})
  \]

- **Left-tailed:**  
  \[
  p = P(T \leq t\_{obs})
  \]

- **Two-tailed:**  
  \[
  p = 2 \times P(T \geq |t\_{obs}|)
  \]

## From t-score (Student’s t-distribution)

```python
from scipy import stats

t_score = 2.1
df = 20  # degrees of freedom

# Right-tailed
p_right = 1 - stats.t.cdf(t_score, df)

# Left-tailed
p_left = stats.t.cdf(t_score, df)

# Two-tailed
p_two = 2 * (1 - stats.t.cdf(abs(t_score), df))

print(p_right, p_left, p_two)
```

## From z-score (using Normal distribution)

```python
from scipy import stats

z_score = 2.0

# right-tailed (positive z-score)
p_right = 1 - stats.norm.cdf(z_score)

# left-tailed (negative z-score)
p_left = stats.norm.cdf(z_score)

# two-tailed
p_two = 2 * (1 - stats.norm.cdf(abs(z_score)))

print(p_right, p_left, p_two)
```

## Relationship with Statistical Power

- While the p-value measures evidence against H₀ in one test, power measures the ability of the test to correctly detect true effects (true positives).
- Plase see [Power of a Test](power-effect-size.md#power-of-a-test)
