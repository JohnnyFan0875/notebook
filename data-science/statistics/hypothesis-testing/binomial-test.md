# Binomial Test

## 1. Overview

The **Binomial Test** is a **nonparametric exact test** used to determine whether the proportion of successes in a binary outcome (success/failure) differs from a hypothesized proportion (p₀).

It is particularly useful when the sample size is small, and the normal approximation (z-test for proportions) is not reliable.

## 2. Hypotheses

- **Null hypothesis (H₀):** The true proportion of successes = p₀
  ( H_0: p = p_0 )

- **Alternative hypothesis (H₁):** The true proportion of successes differs from p₀
  ( H_1: p \neq p_0 )

Depending on the question, the test may be **two-tailed**, **left-tailed**, or **right-tailed**.

## 3. When to Use

| Use Binomial Test when...         | Instead of...                     |
| --------------------------------- | --------------------------------- |
| Sample size is small              | One-sample z-test for proportions |
| Expected counts < 5               | Normal approximation              |
| Data are binary (success/failure) | t-test (continuous data)          |

## 4. Formula

Given:

- **n:** total number of trials
- **x:** number of observed successes
- **p₀:** hypothesized probability of success

The probability of observing exactly x successes is given by the **binomial distribution**:

[
P(X = x) = \binom{n}{x} p_0^x (1 - p_0)^{n-x}
]

The **p-value** is the sum of probabilities for outcomes as extreme (or more extreme) than the observed x, depending on the alternative hypothesis.

## 5. Example (Python)

```python
from scipy.stats import binomtest

# Example: 12 successes in 20 trials, expected p = 0.5
result = binomtest(k=12, n=20, p=0.5, alternative='two-sided')
print(f"p-value = {result.pvalue:.4f}")
```

**Output example:**

```
p-value = 0.5034
```

Interpretation: p > 0.05 → fail to reject H₀. The observed success rate is consistent with p₀ = 0.5.

## 6. Example Interpretation

| Result                 | Interpretation                                                |
| ---------------------- | ------------------------------------------------------------- |
| **p ≤ α (e.g., 0.05)** | Significant difference; observed proportion ≠ hypothesized p₀ |
| **p > α**              | No significant difference; observed data consistent with p₀   |

## 7. One-tailed vs Two-tailed Tests

| Type             | Alternative Hypothesis | Use When                                           |
| ---------------- | ---------------------- | -------------------------------------------------- |
| **Two-tailed**   | p ≠ p₀                 | You suspect any deviation from expected proportion |
| **Left-tailed**  | p < p₀                 | You expect fewer successes than expected           |
| **Right-tailed** | p > p₀                 | You expect more successes than expected            |

## 8. Advantages and Limitations

**Advantages:**

- Exact p-values (no large-sample approximation required)
- Simple and robust for binary data
- Works well with small samples

**Limitations:**

- Only applicable for binary outcomes
- Computationally demanding for very large n
- Less intuitive when n is large (prefer z-test)

## 9. Comparison to Other Tests

| Test                                               | Data Type              | Purpose                                     | Sample Size | Notes                       |
| -------------------------------------------------- | ---------------------- | ------------------------------------------- | ----------- | --------------------------- |
| **Binomial Test**                                  | Binary (single sample) | Compare observed proportion to hypothesized | Small       | Exact p-value               |
| [**Z-test for Proportion**](./proportion-tests.md) | Binary (single sample) | Same as above                               | Large       | Normal approximation        |
| [**Fisher’s Exact Test**](./fisher-exact-test.md)  | 2×2 categorical        | Compare two proportions                     | Small       | Exact test for independence |
| [**Chi-square Test**](./chi-square.md)             | Categorical            | Compare multiple proportions                | Large       | Approximate test            |

## 10. Summary

- The **Binomial Test** checks if an observed proportion differs from a hypothesized one.
- It uses the **binomial distribution** for exact inference.
- Recommended for **small samples or binary outcomes**.
- For large samples, use a **z-test for proportions** instead.
