# Exact Tests

Exact tests compute **true p-values** using discrete probability distributions,  
without relying on large-sample (normal or chi-square) approximations.  
They are most useful when **sample sizes are small** (usually count < 5) or **expected frequencies are low**.

## Exact Binomial Test

- **Purpose:** Tests whether an observed proportion differs from a hypothesized probability ($p₀$).
- **Distribution:** Binomial  
  The probability of observing exactly x successes is given by the **binomial distribution**
- **Use case:** One-sample categorical (success/failure) data.
- **Alternative to:** One-sample proportion z-test (approximation).

### Hypotheses

- **Null hypothesis (H₀):** The true proportion of successes ($p = p₀$)
- **Alternative hypothesis (H₁):** The true proportion of successes differs from p₀ ($p \neq p_0$)

### Formula

$$
P(X = x) = \binom{n}{x} p_0^x (1 - p_0)^{n-x}
$$

- **n:** total number of trials
- **x:** number of observed successes
- **p₀:** hypothesized probability of success

The **p-value** is the sum of probabilities for outcomes as extreme (or more extreme) than the observed x, depending on the alternative hypothesis.

### Python Example

```python
from scipy.stats import binomtest

# Example: 12 successes in 20 trials, expected p = 0.5
result = binomtest(k=12, n=20, p=0.5, alternative='two-sided')
print(f"p-value = {result.pvalue:.4f}")
```

p-value = 0.5034 > 0.05 → fail to reject H₀. The observed success rate is consistent with $p₀$ = 0.5.

### One-tailed vs Two-tailed Tests

| Type             | Alternative Hypothesis | Use When                                       |
| ---------------- | ---------------------- | ---------------------------------------------- |
| **Two-tailed**   | $p ≠ p₀$               | Suspect any deviation from expected proportion |
| **Left-tailed**  | $p < p₀$               | Suspect fewer successes than expected          |
| **Right-tailed** | $p > p₀$               | Suspect more successes than expected           |

## Fisher’s Exact Test

- **Purpose:** Tests whether there is a **nonrandom association between two categorical variables** in a **2×2 contingency table**.
- **Distribution:** Hypergeometric  
  The probability of observing the data under the null hypothesis of independence follows the hypergeometric distribution.
- **Use case:** Two categorical variables, small samples, or any cell with expected frequency < 5.
- **Alternative to:** Chi-square test of independence (approximation).

### Hypotheses

- **Null hypothesis (H₀):** The two categorical variables are independent (no association). [Odds ratio (OR)](./odds-ratio.md) = 1
- **Alternative hypothesis (H₁):** The two variables are associated (dependent).

### Formula

For a 2×2 contingency table:

|             | Success | Failure | Total |
| ----------- | ------- | ------- | ----- |
| **Group 1** | a       | b       | a + b |
| **Group 2** | c       | d       | c + d |
| **Total**   | a + c   | b + d   | N     |

The probability of obtaining this specific table under the null hypothesis is given by the **hypergeometric distribution**:

$$
P = \frac{(a+b)!(c+d)!(a+c)!(b+d)!}{a!b!c!d!N!}
$$

The **p-value** is obtained by summing probabilities of all tables as extreme (or more extreme) than the observed one, depending on the test direction.

### Python Example

```python
from scipy.stats import fisher_exact

# whether two treatments have different success rates.
# Example 2x2 contingency table
# [[Group1 success, Group1 failure], [Group2 success, Group2 failure]]
table = [[8, 2],
         [1, 9]]

oddsratio, p_value = fisher_exact(table, alternative='two-sided')
print(f"Odds Ratio = {oddsratio:.3f}, p-value = {p_value:.4f}")
```

Odds Ratio = 36.000, p-value = 0.0022 < 0.05 → reject H₀, indicating a significant association between variables.

### One-tailed vs Two-tailed Tests

| Type           | Alternative Hypothesis     | Use When                                                                    |
| -------------- | -------------------------- | --------------------------------------------------------------------------- |
| **One-tailed** | Directional association    | You expect a relationship in a specific direction (e.g., Group 1 > Group 2) |
| **Two-tailed** | Nondirectional association | You want to test for any association (positive or negative)                 |

### Relationship to Two-Group Proportion Tests

Fisher’s Exact Test can also be interpreted as an **exact test for equality of two proportions**:

- It compares whether the probability of “success” ($p_1$) in **Group 1** equals that in **Group 2** ($p_2$).
- When sample sizes are small, Fisher’s test provides an **exact p-value** without relying on the normal approximation used in the [two-sample proportion z-test](./proportion-tests.md#two-sample-proportion-test).
- When sample sizes are large, both tests **converge to the same result**.

| Comparison           | **Fisher’s Exact Test**               | **Two-Sample Proportion z-test** |
| -------------------- | ------------------------------------- | -------------------------------- |
| **Distribution**     | Hypergeometric (exact)                | Normal (approximation)           |
| **Assumptions**      | Small samples, any expected count < 5 | Large samples, np ≥ 5            |
| **Null hypothesis**  | $p_1 = p_2$                           | $p_1 = p_2$                      |
| **Recommended when** | Sample size is small                  | Sample size is large             |

**Python Example:**  
Using the same 2×2 contingency table shown above, Fisher’s test provides the exact p-value for testing whether the two success proportions differ.

| Group           | Success | Failure | Total |
| --------------- | ------- | ------- | ----- |
| **Treatment A** | 8       | 2       | 10    |
| **Treatment B** | 1       | 9       | 10    |

### Association Between Two Categorical Variables (r×c Table)

For larger contingency tables (e.g., 2×3, 3×3), Fisher’s Exact Test is extended using the **multivariate hypergeometric distribution**.

The general probability of observing an r×c table with fixed row and column totals is:

$$
P = \frac{\prod_{i=1}^{r} (n_{i+}!)}{N!} \times \frac{\prod_{j=1}^{c} (n_{+j}!)}{\prod_{i=1}^{r}\prod_{j=1}^{c} n_{ij}!}
$$

**Python Example:**

```python
from statsmodels.stats.contingency_tables import Table

result = Table(your_table).test_nominal_association()
print(result)
```

## Summary Comparison

| Test                    | Distribution   | Data Type                    | Alternative Approximation    | Recommended When                     |
| ----------------------- | -------------- | ---------------------------- | ---------------------------- | ------------------------------------ |
| **Exact Binomial Test** | Binomial       | One-sample proportion        | One-sample proportion z-test | Small n, binary data                 |
| **Fisher’s Exact Test** | Hypergeometric | Two-sample categorical (2×2) | Chi-square test              | Small samples or expected counts < 5 |
