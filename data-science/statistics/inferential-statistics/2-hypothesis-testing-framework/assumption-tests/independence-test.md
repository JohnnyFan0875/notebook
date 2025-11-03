# Independence Test

The **independence test** evaluates whether observations or variables are statistically independent. Independence means that the occurrence or value of one observation does not influence another. This assumption is crucial for most parametric tests (e.g., t-tests, ANOVA, regression) and is often validated by study design or residual analysis.

## 1. Concept Overview

| Aspect          | Description                                                                                   |
| --------------- | --------------------------------------------------------------------------------------------- |
| **Definition**  | Independence means that the outcome of one observation is not related to another.             |
| **Importance**  | Violating independence can inflate Type I error rates and bias parameter estimates.           |
| **How checked** | Mainly by study design (randomization), time-series diagnostics, or correlation of residuals. |

## 2. Sources of Dependence

- **Repeated measures**: Same subjects measured multiple times (e.g., before and after treatment).
- **Clustered data**: Observations grouped within clusters (e.g., patients within hospitals).
- **Time-series correlation**: Successive measurements correlated over time.
- **Spatial correlation**: Observations close in space (e.g., geographic data) are related.

## 3. Methods for Testing Independence

### A. Design-Based Independence (Preferred)

- Achieved by **random sampling** and **random assignment**.
- Ensure that each observation is drawn independently from the population.
- Example: Independent participants randomly assigned to treatment or control groups.

### B. Residual Independence (Model Diagnostics)

For regression or ANOVA models, independence is tested using residuals.

#### Durbin–Watson Test (for autocorrelation)

Tests for serial correlation in residuals of regression models (especially time-series data).

- **Null hypothesis (H₀):** Residuals are independent.
- **Alternative hypothesis (Hₐ):** Residuals are autocorrelated.

```python
from statsmodels.stats.stattools import durbin_watson
import statsmodels.api as sm

# Example: Linear regression model
X = sm.add_constant([1, 2, 3, 4, 5])
y = [2, 4, 5, 4, 5]
model = sm.OLS(y, X).fit()
dw = durbin_watson(model.resid)
print("Durbin–Watson statistic:", dw)
```

**Interpretation:**

| DW value | Interpretation           |
| -------- | ------------------------ |
| ≈ 2      | No autocorrelation       |
| < 2      | Positive autocorrelation |
| > 2      | Negative autocorrelation |

#### Runs Test (for randomness)

Tests whether a sequence of residuals or binary outcomes occurs randomly.

```python
from statsmodels.sandbox.stats.runs import runstest_1samp
import numpy as np

residuals = np.array([0.5, -0.2, 0.1, -0.4, 0.3, -0.1])
stat, p_value = runstest_1samp(residuals)
print("Runs test statistic:", stat)
print("p-value:", p_value)
```

**Interpretation:**

- p > 0.05 → Fail to reject H₀ → sequence is random (independent)
- p ≤ 0.05 → Reject H₀ → residuals show non-random pattern (dependence)

## 4. Remedies for Non-Independence

| Cause                       | Common Solutions                                                              |
| --------------------------- | ----------------------------------------------------------------------------- |
| **Repeated measures**       | Use paired tests (e.g., paired t-test, Wilcoxon signed-rank) or mixed models  |
| **Clustered data**          | Use multilevel (hierarchical) or generalized estimating equation (GEE) models |
| **Time-series correlation** | Apply autoregressive (ARIMA) or time-series regression models                 |
| **Spatial correlation**     | Use spatial autocorrelation models (e.g., Moran’s I, spatial lag models)      |

## 5. Summary

- Independence is a **design assumption**, not just a statistical property.
- Always ensure randomization during sampling and assignment.
- When data are dependent, use statistical models that account for this structure.

**Key takeaway:** Violating independence undermines the validity of hypothesis tests — always diagnose it before inference.
