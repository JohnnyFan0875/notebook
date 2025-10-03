# Cox Proportional Hazards Model

- A semi-parametric model used to evaluate the effect of covariates (e.g., SNPs, age, sex) on survival.
- Assumes proportional hazards (the hazard ratio between groups is constant over time).
- Provides hazard ratios (HRs) and confidence intervals.


The **Cox proportional hazards model (CoxPH)** is a semi-parametric method used to examine the effect of one or more covariates on survival time. It is widely applied in biomedical research, especially when evaluating prognostic factors and treatment effects.

---

## Model Overview

The hazard function for subject _i_ at time _t_ is modeled as:

$$
h_i(t) = h_0(t) \exp(\beta_1 x_{i1} + \beta_2 x_{i2} + \cdots + \beta_p x_{ip})
$$

Where:

- \(h*i(t)\): hazard for subject \_i* at time _t_
- \(h_0(t)\): baseline hazard function (unspecified, non-parametric)
- \(x\_{ij}\): covariates (e.g., age, sex, SNP, treatment)
- \(\beta_j\): regression coefficients estimated from the data

The **hazard ratio (HR)** for a one-unit increase in covariate \(x_j\) is:

$$
HR = e^{\beta_j}
$$

---

## Key Assumptions

1. **Proportional hazards**: The hazard ratio between two groups is constant over time.
2. **Linearity**: Log hazard is a linear function of covariates.
3. **Independent censoring**: Censoring is unrelated to survival probability.

---

## Example in R

```r
library(survival)
library(survminer)

# Fit Cox model
cox_model <- coxph(Surv(time, status) ~ age + sex + treatment, data = clinical_data)

# Summary of results
summary(cox_model)

# Test proportional hazards assumption
cox.zph(cox_model)

# Plot survival curves adjusted for covariates
ggadjustedcurves(cox_model, data = clinical_data, variable = "treatment")
```

## Example in Python

```python
from lifelines import CoxPHFitter
import pandas as pd

# Example dataset
df = pd.DataFrame({
    "time": [5, 6, 6, 2, 4],
    "status": [1, 0, 1, 1, 1],
    "age": [65, 70, 50, 60, 80],
    "sex": [1, 0, 1, 0, 1],       # 1=male, 0=female
    "treatment": [1, 1, 0, 0, 1]  # 1=treated, 0=control
})

cph = CoxPHFitter()
cph.fit(df, duration_col="time", event_col="status")
cph.print_summary()
```

## Interpretation of Results

- Hazard Ratio (HR):

  - HR > 1: covariate increases risk (shorter survival).
  - HR < 1: covariate decreases risk (longer survival).
  - HR = 1: no effect.

- Confidence interval (CI): If CI excludes 1, the effect is statistically significant.
- p-value: Tests null hypothesis 𝛽 = 0

## Model Diagnostics

- Schoenfeld residuals: Check proportional hazards assumption.
- Martingale residuals: Assess non-linearity of covariates.
- Deviance residuals: Identify influential observations.
- Concordance index (C-index): Measures predictive accuracy.

## Extensions

- Time-dependent covariates: Allow effects that vary over time.
- Stratified Cox model: Adjust for categorical variables that violate proportional hazards.
- Penalized Cox models (LASSO, Ridge): Handle high-dimensional omics data.

## Applications

- Evaluating prognostic biomarkers (e.g., SNPs, gene signatures).
- Estimating treatment effects while adjusting for confounders.
- Building risk prediction models in oncology and clinical epidemiology.
