# Survival Analysis

**Survival analysis** is a collection of statistical methods for analyzing **time-to-event data** — data where the outcome of interest is *when* something happens, not just *whether* it happens. It handles the unique challenge of **censoring**: observations where the event has not yet occurred by the time data collection ends.

> 📌 **核心問題**：存活分析回答的不是「有多少人發生了事件？」，而是「事件發生的時間點是何時，以及哪些因子影響了它的快慢？」這個「時間」維度是一般迴歸和分類方法無法直接處理的。

---

## Why Survival Analysis?

Standard regression cannot handle time-to-event data correctly for two reasons:

**1. Censoring**: If a study ends before a participant experiences the event, you don't know *when* they would have experienced it — only that they hadn't yet. Ignoring censored observations (or treating them as "no event") systematically biases results.

**2. Time-varying hazard**: The risk of an event is not constant over time. Standard logistic regression treats the outcome as binary and ignores the timing entirely.

```
Without survival analysis:                With survival analysis:
  "60% of patients survived"               "Median survival = 18 months"
  (ignores when they survived until)       (accounts for when events occurred
                                            and censored observations)
```

---

## Where Survival Analysis Appears

| Domain              | Event of Interest                       | Time Variable                    |
| ------------------- | --------------------------------------- | -------------------------------- |
| Medicine            | Death, relapse, disease onset           | Days from diagnosis to event     |
| Engineering         | Component failure                       | Operating hours until failure    |
| Business / SaaS     | Customer churn, subscription cancellation | Days since signup               |
| HR / Workforce      | Employee attrition                      | Months from hire to resignation  |
| Finance             | Loan default                            | Months from origination to default |
| E-commerce          | First purchase, conversion              | Days from first visit            |

---

## Overview of Topics

| #   | Section                                                                | Level       | Key Questions Answered                                                  |
| --- | ---------------------------------------------------------------------- | ----------- | ----------------------------------------------------------------------- |
| 1   | [**Core Concepts & Censoring**](./1-core-concepts.md)                 | Foundation  | What is survival data? What is censoring? How do I structure the data?  |
| 2   | [**Survival & Hazard Functions**](./2-survival-hazard-functions.md)   | Foundation  | How do I describe the survival process mathematically?                  |
| 3   | [**Kaplan-Meier Estimator**](./3-kaplan-meier.md)                     | Core        | How do I estimate and visualize survival curves from data?              |
| 4   | [**Log-Rank Test**](./4-log-rank-test.md)                             | Core        | How do I compare survival curves between two or more groups?            |
| 5   | [**Cox Proportional Hazards Model**](./5-cox-ph-model.md)             | Core        | How do covariates affect the hazard? What are hazard ratios?            |
| 6   | [**Model Diagnostics & Violations**](./6-diagnostics.md)              | Applied     | Is the proportional hazards assumption met? How do I check and fix it?  |

---

## What's Inside Each Section

### 1. Core Concepts & Censoring

- Survival time, event indicator, and the (time, event) data structure
- Right censoring, left censoring, and interval censoring
- Administrative censoring vs. loss to follow-up
- How to structure survival data in Python with `lifelines`

### 2. Survival & Hazard Functions

Three mathematically related functions that together describe the survival process:

| Function           | Symbol   | Answers                                               |
| ------------------ | -------- | ----------------------------------------------------- |
| Survival function  | S(t)     | What fraction survives past time t?                   |
| Hazard function    | h(t)     | What is the instantaneous risk of the event at t?     |
| Cumulative hazard  | H(t)     | How much total hazard has accumulated by time t?      |

### 3. Kaplan-Meier Estimator

- Non-parametric estimation of the survival curve
- Handling ties and censored observations
- Confidence intervals and median survival time
- Plotting with `lifelines`

### 4. Log-Rank Test

- Comparing two or more survival curves
- The null hypothesis and test statistic
- Weighted variants (Gehan-Breslow, Tarone-Ware, Peto)
- Limitations: when log-rank is not appropriate

### 5. Cox Proportional Hazards Model

- The semi-parametric baseline hazard + covariate structure
- Estimating and interpreting hazard ratios (HR)
- Continuous and categorical predictors
- Time-dependent covariates

### 6. Model Diagnostics & Violations

- The proportional hazards (PH) assumption: what it means and why it matters
- Schoenfeld residuals test
- Log-log plots
- What to do when PH assumption is violated: stratified Cox, time-varying coefficients, accelerated failure time (AFT) models

---

## Visualization Quick Reference

| Chart                     | Best For                                                   |
| ------------------------- | ---------------------------------------------------------- |
| Kaplan-Meier curve        | Visualizing overall or group-specific survival over time   |
| Log-log plot              | Checking the proportional hazards assumption visually      |
| Forest plot               | Displaying hazard ratios and confidence intervals          |
| Schoenfeld residual plot  | Diagnosing time-varying coefficients in Cox model          |
| Cumulative hazard plot    | Alternative to KM; linear for exponential distributions    |

---

## Key Takeaway

> Survival analysis answers: **"When does the event happen, and what factors speed it up or slow it down?"**  
> The defining challenge is censoring — observations where the event hasn't occurred yet carry real information and must not be discarded.
