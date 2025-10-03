# Introduction to Survival Analysis

**Survival analysis** is a branch of statistics that deals with **time-to-event data**.  
The “event” could be death, disease recurrence, equipment failure, or any other outcome of interest.  
Unlike traditional statistical methods, survival analysis must account for **censoring** — when the exact event time is not fully observed.

## Why Use Survival Analysis?

- Many biomedical and clinical studies focus not only on **whether** an event occurs, but also on **when** it occurs.
- Standard regression or mean comparisons are not suitable because:
  - Not all participants experience the event during the study period.
  - Censored observations must still contribute information up to their last known time.
- Survival methods make full use of available data, providing unbiased estimates.

## Core Quantities

- **Survival function, $ S(t) $**  
  The probability of surviving longer than time \( t \):

  $$
  S(t) = P(T > t)
  $$

- **Hazard function, $ h(t) $**  
  The instantaneous risk of event occurrence at time \( t \), given survival up to that time.

- **Cumulative hazard, $ H(t) $**  
  The accumulated risk up to time \( t \), related to survival by:
  $$
  S(t) = e^{-H(t)}
  $$

## Key Features of Survival Data

1. **Time-to-event variable**: Duration between defined start (e.g., diagnosis) and event.
2. **Censoring**: Event not observed for all participants (e.g., lost to follow-up).
3. **Covariates**: Risk factors or predictors (e.g., age, treatment, biomarkers).

## Common Methods

- **Kaplan–Meier estimator**: Non-parametric estimate of the survival curve.
- **Log-rank test**: Compares survival distributions between groups.
- **Cox proportional hazards model**: Semi-parametric regression for covariate effects.
- **Parametric models**: Assume distributions such as exponential, Weibull, or log-normal.

## Applications

- **Clinical trials**: Comparing overall survival or progression-free survival between treatments.
- **Epidemiology**: Studying prognostic factors in disease cohorts.
- **Reliability engineering**: Estimating product lifetimes or machine failure times.
- **Genomics**: Linking genetic markers or expression signatures with patient survival.

## Structure of This Guide

This documentation covers:

1. [Censoring Types](censoring-types.md)
2. [Kaplan–Meier Estimator](kaplan-meier.md)
3. [Log-rank Test](log-rank-test.md)
4. [Cox Model](cox-model.md)
5. [Model Diagnostics](model-diagnostics.md)
6. [Summary Measures](summary-measures.md)
7. [Visualization](visualization.md)
8. [Interpretation](interpretation.md)

- Survival time analysis is a statistical approach used to evaluate the duration between a defined starting point (e.g., diagnosis, treatment initiation) and the occurrence of an event of interest (e.g., death, disease recurrence, treatment failure). Unlike classical regression models, survival analysis must account for **censoring**, where the event has not occurred for some subjects at the time of analysis.

- **Event**: The outcome of interest (e.g., death, relapse, progression).
- **Time-to-event**: The duration from a defined start point until the event occurs or the subject is censored.
- **Censoring**: Subjects who do not experience the event during the study period or are lost to follow-up.
- **Hazard function**: The instantaneous event rate at a given time, conditional on survival up to that time.
- **Survival function (S(t))**: The probability that a subject survives longer than time `t`.

## Model Evaluation

- Proportional hazards assumption: Tested using Schoenfeld residuals.
- Concordance index (C-index): Measures model discrimination ability (similar to AUC in ROC analysis).
- Calibration plots: Compare predicted vs. observed survival probabilities.
