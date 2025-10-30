# Odds Ratio (OR)

The **odds ratio (OR)** is a measure of association commonly used in case–control studies, epidemiology, and genetics.  
It compares the odds of an event occurring in one group to the odds of it occurring in another.

## Definition

$$
\text{Odds} = \dfrac{p}{1-p}
$$

$$
\text{Odds ratio} = \dfrac{\text{odds in group 1}}{\text{odds in group 2}}
$$

- $p$: probability of an event
- Often visualized on a **logarithmic scale** (log-odds), which linearizes the relationship.

## Formula

For a binary exposure and a binary outcome (2 × 2 Contingency Table):

|               | Case (disease=Yes) | Control (disease=No) |
| ------------- | ------------------ | -------------------- |
| **Exposed**   | a                  | b                    |
| **Unexposed** | c                  | d                    |

- a = number of cases with exposure
- b = number of controls with exposure
- c = number of cases without exposure
- d = number of controls without exposure

$$
\text{Odds ratio (OR)} = \frac{a/c}{b/d} = \frac{ad}{bc}
$$

### Standard Error of Log(OR)

The standard error (SE) of the log odds ratio is useful for confidence intervals:

$$
SE = \sqrt{\left(\frac{1}{a} + \frac{1}{b} + \frac{1}{c} + \frac{1}{d}\right)}
$$

### Confidence Interval

A 95% confidence interval (CI) for OR is:

$$
\ln(OR) \pm 1.96 \times SE
$$

Exponentiate the bounds to return to the odds ratio scale:

$$
CI = \left( e^{\ln(OR) - 1.96 \times SE}, \; e^{\ln(OR) + 1.96 \times SE} \right)
$$

## Interpretation

- **OR = 1** → No association.
- **OR > 1** → Exposure increases odds of outcome.
- **OR < 1** → Exposure decreases odds of outcome.

## Python Example

```python
import numpy as np

# Example 2x2 table
a, b, c, d = 30, 10, 20, 40

# Odds ratio
or_value = (a*d) / (b*c)

# Standard error of log(OR)
se = np.sqrt(1/a + 1/b + 1/c + 1/d)

# 95% confidence interval
log_or = np.log(or_value)
ci_lower = np.exp(log_or - 1.96 * se)
ci_upper = np.exp(log_or + 1.96 * se)

print("Odds Ratio:", or_value)
print("95% CI:", (ci_lower, ci_upper))
```

## Relationship to Logistic Regression

Logistic regression models the **log odds** of the outcome:

$$
\log\left(\frac{p}{1-p}\right) = \beta_0 + \beta_1 X_1 + \dots + \beta_k X_k
$$

- $p$: probability of the outcome
- $\beta_0$: intercept
- $\beta_i$: coefficient for predictor \(X_i\)

The exponentiated coefficients, $e^{\beta_i}$, are **odds ratios**, representing the multiplicative change in odds for a one-unit increase in predictor $X_i$.
