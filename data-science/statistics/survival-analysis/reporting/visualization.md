# Visualization in Survival Analysis

Visualization is a key component of survival analysis.  
It transforms statistical estimates into interpretable graphics — enabling researchers to evaluate survival patterns, check model assumptions, and communicate findings effectively.

This section introduces the most common visualization techniques used in clinical and biomedical survival studies, with examples in **R** and **Python**.

## 1. Kaplan–Meier Curves

### Purpose

To display the estimated **survival probability over time** for one or more groups.

### Key Features

- Stepwise curve reflecting survival probability $ \hat{S}(t) $
- Vertical drops at event times
- Tick marks (or crosses) indicating censored observations
- Confidence intervals (optional shaded bands)
- Group comparisons annotated with log-rank p-values

### Example in R

```r
library(survival)
library(survminer)

fit <- survfit(Surv(time, status) ~ treatment, data = clinical_data)

ggsurvplot(fit,
           data = clinical_data,
           pval = TRUE,
           conf.int = TRUE,
           risk.table = TRUE,
           surv.median.line = "hv",
           xlab = "Time (months)",
           ylab = "Survival probability",
           ggtheme = theme_minimal())
```

### Example in Python

```python
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

kmf = KaplanMeierFitter()
kmf.fit(durations, event_observed, label="Treatment A")

kmf.plot_survival_function(ci_show=True)
plt.title("Kaplan–Meier Survival Curve")
plt.xlabel("Time (months)")
plt.ylabel("Survival probability")
plt.show()
```

Interpretation:

- The separation between curves indicates potential survival differences.
- The number-at-risk table below the plot clarifies how many subjects remain under observation at each time point.

## 2. Cumulative Hazard Plots

### Purpose

To visualize the **accumulated risk over time**, or to assess the **proportional hazards assumption** in Cox models.

The cumulative hazard is estimated via the **Nelson–Aalen estimator**:

$$
\hat{H}(t) = \sum_{t_i \le t} \frac{d_i}{n_i}
$$

Parallel cumulative hazard curves between groups suggest that the proportional hazards assumption is reasonable.

#### Example in R

```r
ggsurvplot(fit, fun = "cumhaz", data = clinical_data)
```

#### Example in Python

```python
from lifelines import NelsonAalenFitter

naf = NelsonAalenFitter()
naf.fit(durations, event_observed, label="Treatment A")

naf.plot()
plt.title("Cumulative Hazard Plot")
plt.xlabel("Time (months)")
plt.ylabel("Cumulative hazard")
plt.show()
```

## 3. Forest Plots

### Purpose

To summarize **hazard ratios (HRs)** from Cox regression models, showing effect sizes and confidence intervals for multiple covariates.

#### Example in R

```r
ggforest(cox_model, data = clinical_data)
```

Each line represents a covariate:

- The **box** marks the HR estimate.
- The **horizontal line** shows the 95% confidence interval.
- A **vertical line at HR = 1** indicates no effect.

#### Example in Python

```python
from lifelines import CoxPHFitter

cph = CoxPHFitter()
cph.fit(df, duration_col="time", event_col="status")
cph.plot()
plt.title("Forest Plot of Cox Model Hazard Ratios")
plt.show()
```

## 4. Residual and Diagnostic Plots

Diagnostic plots help evaluate **model fit** and **assumption validity**.

| Plot Type                | Purpose                    | Notes                                      |
| ------------------------ | -------------------------- | ------------------------------------------ |
| **Schoenfeld residuals** | Test proportional hazards  | Random scatter → assumption holds          |
| **Martingale residuals** | Assess covariate linearity | Non-random pattern → consider splines      |
| **Deviance residuals**   | Detect outliers            | Large values indicate influential subjects |

#### Example in R

```r
cox.zph(cox_model)      # Test proportional hazards
plot(cox.zph(cox_model))  # Schoenfeld residual plot
```

#### Example in Python

```python
from lifelines.statistics import proportional_hazard_test

results = proportional_hazard_test(cph, df, time_transform='rank')
results.print_summary()
```

## 5. Calibration and Validation Plots

### Purpose

To compare **predicted vs. observed survival probabilities** and assess **model calibration**.

- A perfectly calibrated model aligns predictions with the 45° diagonal.
- Deviations suggest over- or under-estimation of risk.

**In R:**
Use `rms::calibrate()` for calibration curves.

**In Python:**
Use `scikit-survival` functions such as `calibration_curve`.

These are often combined with **internal validation** (bootstrapping or cross-validation) to evaluate model generalizability.

## 6. Risk Tables and Heatmaps

### Risk Tables

Show the number of individuals **still at risk** at specified time intervals — an essential annotation below Kaplan–Meier plots.

### Heatmaps

Display **survival probabilities** across strata or risk scores (e.g., gene-expression clusters).
They are particularly useful in **omics-driven** or **multi-cohort** survival analyses.

## 7. Publication-Ready Figures: Best Practices

| Element                  | Recommendation                                                                        |
| ------------------------ | ------------------------------------------------------------------------------------- |
| **Color**                | Use consistent palette across analyses (e.g., Treatment A = blue, Treatment B = red). |
| **Axis labels**          | Include time units (months, years).                                                   |
| **Confidence intervals** | Display as shaded ribbons when relevant.                                              |
| **Legends**              | Clearly indicate groups and sample sizes.                                             |
| **Annotations**          | Include median survival and log-rank p-value.                                         |
| **Risk table**           | Add below survival plots for transparency.                                            |

## 8. Summary

- **Kaplan–Meier curves**: visualize group survival over time.
- **Cumulative hazard plots**: check proportional hazards assumption.
- **Forest plots**: summarize hazard ratios with confidence intervals.
- **Residual plots**: test model fit and detect violations.
- **Calibration and heatmaps**: communicate predictive accuracy and subgroup effects.

> Effective visualization bridges statistical modeling and clinical interpretation — transforming numerical results into insights that guide real-world decisions.
