# Visualization in Survival Analysis

Visualization is a critical step in survival analysis.
It allows researchers to understand survival patterns, compare groups, and check model assumptions.

## 1. Kaplan–Meier Curves

- **Purpose**: Show estimated survival probabilities over time.
- **Features**:

  - Stepwise curve.
  - Tick marks for censored cases.
  - Group comparisons with log-rank test.

```r
library(survival)
library(survminer)

fit <- survfit(Surv(time, status) ~ treatment, data = clinical_data)
ggsurvplot(fit, data = clinical_data, pval = TRUE, risk.table = TRUE,
           conf.int = TRUE, surv.median.line = "hv")
```

```python
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

kmf = KaplanMeierFitter()
kmf.fit(durations, event_observed, label="Treatment")
kmf.plot_survival_function(ci_show=True)
plt.title("Kaplan–Meier Curve")
plt.xlabel("Time")
plt.ylabel("Survival probability")
plt.show()
```

## 2. Cumulative Hazard Plots

- **Purpose**: Assess proportional hazards assumption.
- Estimated with the **Nelson–Aalen estimator**.
- Cox models assume parallel cumulative hazard curves between groups.

```r
ggsurvplot(fit, fun = "cumhaz", data = clinical_data)
```

```python
from lifelines import NelsonAalenFitter

naf = NelsonAalenFitter()
af.fit(durations, event_observed, label="Treatment")
af.plot()
plt.title("Cumulative Hazard Plot")
plt.xlabel("Time")
plt.ylabel("Cumulative hazard")
plt.show()
```

## 3. Forest Plots

- **Purpose**: Display hazard ratios (HR) from Cox regression.
- Provide effect sizes with confidence intervals.
- Useful for multivariable models with many covariates.

```r
ggforest(cox_model, data = clinical_data)
```

## 4. Residual Plots

- **Purpose**: Check Cox model assumptions.
- **Examples**:

  - Schoenfeld residual plots → proportional hazards.
  - Martingale residual plots → functional form of covariates.
  - Deviance residual plots → outliers.

```r
cox.zph(cox_model)   # Schoenfeld residuals
plot(cox.zph(cox_model))
```

## 5. Calibration Plots

- Compare **predicted vs. observed survival** probabilities.
- Detect under- or overestimation of risk.
- Often used in prognostic model validation.

## 6. Heatmaps and Risk Curves

- **Heatmaps**: Show survival probability across subgroups (e.g., gene expression clusters).
- **Risk curves**: Show number at risk over time below KM plots.

## 7. Publication-Ready Figures

Include:

- Confidence intervals.
- Number-at-risk tables.
- Group-specific colors/labels.
- Clearly state units of time (months, years).
- Provide both absolute (KM curves) and relative (HRs) measures.

## Summary

- **Kaplan–Meier curves**: overall and group comparisons.
- **Cumulative hazard plots**: check proportional hazards.
- **Forest plots**: display HRs.
- **Residual plots**: test model assumptions.
- **Calibration plots**: validate predictions.
