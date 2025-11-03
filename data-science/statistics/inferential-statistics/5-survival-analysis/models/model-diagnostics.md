# Model Diagnostics in Survival Analysis

Model diagnostics ensure that survival models — especially the **Cox proportional hazards (CoxPH)** and **parametric models** — are valid, well-fitted, and interpretable.  
They help verify assumptions, identify outliers or influential data points, and evaluate overall predictive accuracy.

## 1. Checking the Proportional Hazards (PH) Assumption

The Cox model assumes that the **hazard ratio between groups remains constant over time**.

### Concept

If proportional hazards hold, the relative risk (hazard ratio) does **not** change as time progresses.

### Diagnostic Methods

| Method                        | Purpose                                     | Interpretation                           |
| :---------------------------- | :------------------------------------------ | :--------------------------------------- |
| **Schoenfeld residuals**      | Test correlation between residuals and time | No correlation → PH assumption holds     |
| **Log-minus-log plots**       | Visual inspection of group survival         | Approximately parallel curves → PH holds |
| **Time-dependent covariates** | Quantitatively model non-proportionality    | Useful when assumption is violated       |

### Example in R

```r
library(survival)
cox_model <- coxph(Surv(time, status) ~ age + treatment, data = clinical_data)

# Schoenfeld residual test
cox.zph(cox_model)

# Visualize proportional hazards
plot(cox.zph(cox_model))
```

### Example in Python

```python
from lifelines import CoxPHFitter
import pandas as pd

df = pd.DataFrame({
    "time": [5,6,6,2,4],
    "status": [1,0,1,1,1],
    "age": [60,70,50,55,80],
    "treatment": [1,0,1,0,1]
})

cph = CoxPHFitter()
cph.fit(df, duration_col="time", event_col="status")
cph.check_assumptions(df, p_value_threshold=0.05)
```

## 2. Goodness of Fit

Assess how well the model captures overall patterns in the data.

| Test / Metric                          | Description                                                                                            |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Likelihood Ratio Test**              | Compares nested models; larger statistic → better fit                                                  |
| **Wald Test / Score Test**             | Evaluate significance of individual covariates                                                         |
| **Akaike Information Criterion (AIC)** | Compare non-nested models; lower AIC → preferred                                                       |
| **Concordance Index (C-index)**        | Probability that predicted risk correctly ranks two subjects; 0.5 = random, 1 = perfect discrimination |

**Example in R**

```r
summary(cox_model)$concordance
AIC(cox_model)
```

**Example in Python**

```python
cph.concordance_index_
```

## 3. Residual Diagnostics

Residuals identify non-linearity, outliers, or influential data points.

| Residual Type            | Purpose                                  | Interpretation                                      |
| ------------------------ | ---------------------------------------- | --------------------------------------------------- |
| **Martingale residuals** | Check linearity of continuous covariates | Random scatter → good functional form               |
| **Deviance residuals**   | Identify outliers                        | Large absolute values → potential influential cases |
| **Schoenfeld residuals** | Assess time-dependent effects            | Random around zero → proportional hazards satisfied |
| **Score residuals**      | Evaluate influence of covariates         | Extreme points → influential observations           |

**Example (R)**

```r
residuals(cox_model, type = "martingale")
residuals(cox_model, type = "deviance")
```

## 4. Influence Diagnostics

Evaluate the impact of individual observations on model coefficients.

| Metric               | Meaning                                                      |
| -------------------- | ------------------------------------------------------------ |
| **dfbeta / dfbetas** | Change in estimated coefficient if an observation is removed |
| **Delta-beta plots** | Visualize which cases drive parameter estimates              |
| **Cook’s distance**  | Overall influence on model fit                               |

**Example (R)**

```r
influence <- residuals(cox_model, type = "dfbeta")
plot(influence[, "treatment"], ylab = "dfbeta for treatment")
```

## 5. Functional Form of Covariates

Continuous predictors are assumed to have a **linear** relationship with the log hazard.
If non-linearity is present, transformations or spline terms should be considered.

**Example in R**

```r
cox_model <- coxph(Surv(time, status) ~ pspline(age), data = clinical_data)
```

**Example in Python**

```python
from lifelines import CoxPHFitter
from patsy import dmatrix

df["age_spline"] = dmatrix("bs(age, df=4, include_intercept=False)", df, return_type='dataframe')
cph = CoxPHFitter()
cph.fit(df, duration_col="time", event_col="status")
```

## 6. Calibration and Validation

Model validation ensures that predictions generalize beyond the training dataset.

| Type                    | Description                                               | Method                                 |
| ----------------------- | --------------------------------------------------------- | -------------------------------------- |
| **Internal validation** | Tests reproducibility using bootstrap or cross-validation | `bootcov()` in R, resampling in Python |
| **External validation** | Apply model to an independent cohort                      | Check C-index, calibration, and AUC    |
| **Calibration plots**   | Compare predicted vs. observed survival                   | Ideally close to 45° line              |

## 7. Summary Checklist

✅ **Proportional hazards assumption** — check Schoenfeld residuals and log–log plots
✅ **Model fit** — review likelihood ratio test, AIC, and C-index
✅ **Residuals** — inspect martingale and deviance residuals
✅ **Influential points** — use dfbeta or Cook’s distance
✅ **Calibration** — validate predictions internally and externally

A robust survival model is not only statistically significant but also **stable, interpretable, and generalizable**.
