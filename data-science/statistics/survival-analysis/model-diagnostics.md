# Model Diagnostics in Survival Analysis

Model diagnostics are essential for ensuring that survival analysis models (e.g., Cox proportional hazards, parametric models) are valid and interpretable. Diagnostics help detect violations of assumptions, influential observations, and overall model performance.

## 1. Proportional Hazards Assumption (Cox Model)

The Cox model assumes that **hazard ratios are constant over time**.

### Methods to Check:

- **Schoenfeld Residuals**

  - Test correlation between residuals and time.
  - A non-significant result suggests proportional hazards assumption holds.

```r
# R example
cox_model <- coxph(Surv(time, status) ~ age + treatment, data = clinical_data)
cox.zph(cox_model)  # Test proportional hazards
plot(cox.zph(cox_model))  # Visualize
```

- **Log-minus-log plots**

  - Plot log(-log(survival)) against log(time) for groups.
  - Parallel curves suggest proportional hazards.

## 2. Goodness of Fit

- **Likelihood ratio test, Wald test, Score test**
  Evaluate overall significance of covariates.

- **Akaike Information Criterion (AIC)**
  Compare non-nested models; lower AIC indicates better fit.

- **Concordance index (C-index)**
  Probability that predicted risk correctly ranks two randomly chosen individuals.
  Similar to AUC in ROC analysis.

```r
summary(cox_model)$concordance
```

## 3. Residual Analysis

Residuals can highlight deviations, non-linearity, or outliers.

- **Martingale residuals**
  Assess functional form of covariates.
  Non-random patterns suggest non-linearity.

- **Deviance residuals**
  Symmetric around zero if model fits well.
  Large values indicate influential observations.

- **Score residuals**
  Detect influential observations for specific covariates.

## 4. Influence Diagnostics

- **dfbeta / dfbetas**
  Measure change in regression coefficients if one subject is removed.

- **Delta-beta plots**
  Identify influential data points.

```r
# R example
residuals(cox_model, type = "dfbeta")
```

## 5. Checking Functional Form of Covariates

- Continuous covariates should have a **linear relationship** with log hazard.
- Use **Martingale residuals plots** or **restricted cubic splines** to test non-linearity.

```r
# Example: Using splines in R
cox_model <- coxph(Surv(time, status) ~ pspline(age), data = clinical_data)
```

## 6. Calibration

- Compare predicted vs. observed survival probabilities.
- Calibration plots help assess whether the model systematically over- or under-predicts risk.

## 7. Model Validation

- **Internal validation**: Bootstrapping, cross-validation.
- **External validation**: Apply model to independent cohort.
- Ensures generalizability of prognostic models.

## Summary

- **Check proportional hazards assumption** with Schoenfeld residuals and plots.
- **Evaluate fit** with likelihood tests, AIC, and C-index.
- **Inspect residuals** for non-linearity and influential points.
- **Validate models** internally and externally to ensure robustness.
