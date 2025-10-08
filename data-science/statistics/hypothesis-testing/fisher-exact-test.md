# Fisher’s Exact Test

> **See also:** [Chi-Square Test](./chi-square.md) for large samples
> **See also:** [Proportion Tests](./proportion-tests.md) for comparisons of proportions

## 1. Overview

**Fisher’s Exact Test** is a **nonparametric test** used to determine whether there is a **nonrandom association between two categorical variables** in a **2×2 contingency table**, especially when sample sizes are small and the expected counts are less than 5.

It computes the _exact probability_ of observing the data (or more extreme data) under the null hypothesis of independence.

## 2. Hypotheses

- **Null hypothesis (H₀):** The two categorical variables are independent (no association).
- **Alternative hypothesis (H₁):** The two variables are associated (dependent).

## 3. When to Use

| Use Fisher’s Exact Test when...   | Instead of...          |
| --------------------------------- | ---------------------- |
| Sample size is small (< 20)       | Chi-square test        |
| Any expected cell count < 5       | Chi-square test        |
| Data form a 2×2 contingency table | z-test for proportions |

## 4. Formula

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

To obtain the p-value, Fisher’s Exact Test sums the probabilities of all tables **as extreme or more extreme** than the observed one (depending on one-tailed or two-tailed setup).

## 5. Example (Python)

```python
from scipy.stats import fisher_exact

# Example 2x2 contingency table
# [[Group1 success, Group1 failure], [Group2 success, Group2 failure]]
table = [[8, 2], [1, 9]]

oddsratio, p_value = fisher_exact(table, alternative='two-sided')
print(f"Odds Ratio = {oddsratio:.3f}, p-value = {p_value:.4f}")
```

**Output example:**

```
Odds Ratio = 36.000, p-value = 0.0022
```

Interpretation: _p_ < 0.05 → reject H₀, indicating a significant association between variables.

## 6. One-tailed vs Two-tailed Tests

| Type           | Use When                                                                 | Example                                    |
| -------------- | ------------------------------------------------------------------------ | ------------------------------------------ |
| **One-tailed** | You expect association in a specific direction (e.g., Group 1 > Group 2) | Drug increases cure rate                   |
| **Two-tailed** | You are testing any association (no direction specified)                 | Drug has any effect (positive or negative) |

## 7. Advantages and Limitations

**Advantages:**

- Exact p-values (not approximated).
- Valid even with small samples or sparse data.
- No distributional assumptions (nonparametric).

**Limitations:**

- Computationally intensive for large tables (>2×2).
- For larger samples, use [**Chi-square test**](./chi-square.md) (similar results, faster).

## 8. Summary

- Use **Fisher’s Exact Test** for small-sample **categorical data** in 2×2 tables.
- It tests **independence** between two categorical variables.
- It relies on the **hypergeometric distribution**, not the chi-square approximation.
- For larger tables or datasets, use the **Chi-square Test** as an alternative.
