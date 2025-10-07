# Cox Proportional Hazards Model

The **Cox proportional hazards model (CoxPH)** is a semi-parametric regression method that evaluates how covariates affect the **hazard of an event over time**.  
It is one of the most widely used models in clinical and epidemiological research because it does not require specifying the baseline hazard function.

## 1. Model Concept

The Cox model assumes that each subject has a hazard function composed of two parts:

$$
h_i(t) = h_0(t) \exp(\beta_1 x_{i1} + \beta_2 x_{i2} + \cdots + \beta_p x_{ip})
$$

Where:

| Symbol      | Meaning                                                         |
| :---------- | :-------------------------------------------------------------- |
| \(h_i(t)\)  | Hazard (instantaneous event rate) for subject _i_ at time _t_   |
| \(h_0(t)\)  | Baseline hazard function (unspecified, non-parametric)          |
| \(x\_{ij}\) | Covariate _j_ for subject _i_ (e.g., age, sex, gene expression) |
| \(\beta_j\) | Regression coefficient for covariate _j_                        |

The model estimates **hazard ratios (HR)**, which quantify the _relative risk_ associated with a one-unit increase in each covariate:

$$
HR_j = e^{\beta_j}
$$

### Meaning of the Hazard Ratio (HR):

[HR Interpretation](../reporting/interpretation.md#3-hazard-ratios-cox-model)

## 2. Key Assumptions

| Assumption                | Description                                                              | Check                                     |
| ------------------------- | ------------------------------------------------------------------------ | ----------------------------------------- |
| **Proportional hazards**  | The ratio of hazards between two individuals remains constant over time. | Schoenfeld residuals, log-minus-log plots |
| **Linearity**             | Log-hazard is a linear function of continuous covariates.                | Martingale residuals                      |
| **Independent censoring** | Censoring is unrelated to the true survival time.                        | Study design assumption                   |

If the proportional hazards assumption is violated, consider:

- Stratified Cox models
- Time-dependent covariates
- Parametric or accelerated failure time (AFT) models

## 3. Fitting the Cox Model

### In R

```r
library(survival)
library(survminer)

# Example dataset
data(lung)

# Fit Cox model
cox_model <- coxph(Surv(time, status) ~ age + sex + ph.ecog, data = lung)
summary(cox_model)

# Check proportional hazards assumption
cox.zph(cox_model)

# Visualize adjusted survival curves
ggadjustedcurves(cox_model, data = lung, variable = "sex")
```

Output interpretation:

- coef (β) → log hazard ratio
- exp(coef) → hazard ratio (HR)
- p-value → significance of each covariate
- Concordance index (C-index) → model’s discriminative ability

### In Python

```python
from lifelines import CoxPHFitter
import pandas as pd
from lifelines.datasets import load_rossi

df = load_rossi()  # Example dataset

cph = CoxPHFitter()
cph.fit(df, duration_col='week', event_col='arrest')

cph.print_summary()   # Display coefficients, HR, p-values
cph.check_assumptions(df, p_value_threshold=0.05)
```

## 4. Model Interpretation

| Metric                           | Interpretation                                                        |
| -------------------------------- | --------------------------------------------------------------------- |
| **Hazard Ratio (HR)**            | HR > 1 → increased risk; HR < 1 → decreased risk; HR = 1 → no effect  |
| **95% Confidence Interval (CI)** | If CI excludes 1, the effect is statistically significant             |
| **p-value**                      | Tests ( H_0 : \beta = 0 ); p < 0.05 indicates significant association |
| **C-index**                      | Probability that predicted risk correctly ranks two individuals       |

**Example statement:**
“In multivariate Cox analysis, age (HR = 1.05, 95% CI = 1.02–1.08, p = 0.001) and poor performance status (HR = 1.75, 95% CI = 1.20–2.56, p = 0.004) were independently associated with higher mortality risk.”

## 5. Model Extensions

| Extension                                | Purpose                                                           |
| ---------------------------------------- | ----------------------------------------------------------------- |
| **Time-dependent covariates**            | Allow covariate effects to change over time.                      |
| **Stratified Cox model**                 | Control for categorical variables violating proportional hazards. |
| **Penalized Cox models (LASSO / Ridge)** | Handle high-dimensional omics data.                               |
| **Multistate Cox models**                | Model transitions between multiple event states.                  |

## 6. Diagnostics and Validation

Model validation ensures reliability and generalizability.

**Assumption check:**
`cox.zph()` in R or `check_assumptions()` in lifelines

**Goodness of fit:**
Likelihood ratio, Wald, and Score tests

**Performance metrics:**
C-index, AIC, calibration plots

**Influential observations:**
`dfbeta`, deviance residuals

For details, see _Model Diagnostics_.

## 7. Visualization

Common plots for interpreting Cox model results:

| Plot Type                    | Description                                     |
| ---------------------------- | ----------------------------------------------- |
| **Forest plot**              | Shows HRs with 95% CIs for covariates           |
| **Adjusted survival curves** | Visualize survival by covariate-adjusted groups |
| **Cumulative hazard curves** | Assess proportional hazards visually            |

**Example in R:**

```r
ggforest(cox_model, data = lung)
```

## 8. Summary

- The **Cox model** links covariates to the hazard of an event using proportional hazards.
- It estimates **hazard ratios (HR)**, providing interpretable measures of relative risk.
- Assumption checks and diagnostics are essential for credible inference.
- Extensions such as **penalized** or **time-dependent** Cox models enable modern applications in genomics and precision medicine.

> The Cox model remains the backbone of clinical risk modeling — balancing interpretability, flexibility, and statistical power.
