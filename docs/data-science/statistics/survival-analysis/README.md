# Introduction

**Survival analysis** is a collection of statistical methods for analyzing **time-to-event data** — data where the outcome of interest is *when* something happens, not just *whether* it happens. It handles the unique challenge of **censoring**: observations where the event has not yet occurred by the time data collection ends.

Key point: Survival analysis does not just ask whether the event happened. It asks when the event happened, how risk changes over time, and what factors speed it up or slow it down. That time dimension is why ordinary regression or classification tools are not enough.

## Why Survival Analysis?

Standard regression cannot handle time-to-event data correctly for two reasons:

**1. Censoring**: If a study ends before a participant experiences the event, you don't know *when* they would have experienced it — only that they hadn't yet. Ignoring censored observations systematically biases results.

**2. Time-varying hazard**: The risk of an event is not constant over time. Standard logistic regression treats the outcome as binary and ignores timing entirely.

## Where Survival Analysis Appears

| Domain | Event of Interest | Time Variable |
| ------------------- | ----------------------------------------- | ---------------------------------- |
| Medicine | Death, relapse, disease onset | Days from diagnosis to event |
| Engineering | Component failure | Operating hours until failure |
| Business / SaaS | Customer churn, subscription cancellation | Days since signup |
| HR / Workforce | Employee attrition | Months from hire to resignation |
| Finance | Loan default | Months from origination to default |
| E-commerce | First purchase, conversion | Days from first visit |

## Section Overview

| Section | Level | Key Questions Answered |
| -------------------------------------------------------------------- | ----------- | ------------------------------------------------------------------------ |
| [**Core Concepts & Censoring**](./core-concepts.md) | Foundation | What is survival data? What is censoring? How do I structure the data? |
| [**Survival & Hazard Functions**](./survival-hazard-functions.md) | Foundation | How do I describe the survival process mathematically? |
| [**Kaplan-Meier Estimator**](./kaplan-meier.md) | Core | How do I estimate and visualize survival curves from data? |
| [**Log-Rank Test**](./log-rank-test.md) | Core | How do I compare survival curves between two or more groups? |
| [**Cox Proportional Hazards Model**](./cox-ph-model.md) | Core | How do covariates affect the hazard? What are hazard ratios? |
| [**Model Diagnostics & Violations**](./diagnostics.md) | Applied | Is the proportional hazards assumption met? How do I check and fix it? |
| [**Parametric Models**](./parametric-models.md) | Applied | When and how to use Weibull, Exponential, Log-normal models? |
| [**Interpretation**](./interpretation.md) | Applied | How do I translate statistical outputs into meaningful conclusions? |
| [**Visualization**](./visualization.md) | Applied | What plots should I produce and how should I read them? |

## Analytical Workflow

```
Data Preparation  →  Descriptive Analysis  →  Model Fitting
(Core concepts)      (Functions + KM + log-rank)      (Cox + parametric models)
                      KM curves, censoring      Cox / Parametric
                           ↓                         ↓
                  Diagnostics & Validation  →  Visualization & Interpretation
                     (Diagnostics)                 (Interpretation + visualization)
```

## Start Here If...

This module is the right home when:

- the outcome is time until event, not just yes/no
- some subjects have not had the event by study end
- you need to compare groups while respecting censoring
- you want both time-based summaries and hazard-based modeling

## Visualization Quick Reference

| Chart | Best For | Section |
| ------------------------ | ---------------------------------------------------------- | ------- |
| Kaplan-Meier curve | Visualizing overall or group-specific survival over time | 3, 9 |
| Log-log plot | Checking the proportional hazards assumption visually | 6, 9 |
| Forest plot | Displaying hazard ratios and confidence intervals | 5, 9 |
| Schoenfeld residual plot | Diagnosing time-varying coefficients in Cox model | 6, 9 |
| Cumulative hazard plot | Alternative to KM; linear for exponential distributions | 2, 9 |
| Calibration plot | Comparing predicted vs. observed survival | 6, 9 |

## Key Takeaway

Survival analysis answers: "When does the event happen, and what factors speed it up or slow it down?" The defining challenge is censoring — observations where the event has not yet occurred carry real information and must not be discarded.

## Deep-Study Priorities

The most effective study order is:

1. censoring and the `(T, delta)` structure
2. survival and hazard functions
3. KM and log-rank
4. Cox plus diagnostics

Tip: If the time axis and censoring logic are not intuitive yet, do not rush to the Cox model.

## Recommended Route

The cleanest route through this module is:

1. understand censoring and the data structure
2. learn survival and hazard functions
3. read Kaplan-Meier and log-rank together
4. move to Cox only after the descriptive picture is clear
5. treat diagnostics and interpretation as part of the model, not as optional extras
