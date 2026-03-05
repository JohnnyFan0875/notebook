# Survival Analysis

**Survival analysis** is a collection of statistical methods for analyzing **time-to-event data** — data where the outcome of interest is *when* something happens, not just *whether* it happens. It handles the unique challenge of **censoring**: observations where the event has not yet occurred by the time data collection ends.

> 📌 **核心問題**：存活分析回答的不是「有多少人發生了事件？」，而是「事件發生的時間點是何時，以及哪些因子影響了它的快慢？」這個「時間」維度是一般迴歸和分類方法無法直接處理的。

---

## Why Survival Analysis?

Standard regression cannot handle time-to-event data correctly for two reasons:

**1. Censoring**: If a study ends before a participant experiences the event, you don't know *when* they would have experienced it — only that they hadn't yet. Ignoring censored observations systematically biases results.

**2. Time-varying hazard**: The risk of an event is not constant over time. Standard logistic regression treats the outcome as binary and ignores timing entirely.

---

## Where Survival Analysis Appears

| Domain              | Event of Interest                         | Time Variable                      |
| ------------------- | ----------------------------------------- | ---------------------------------- |
| Medicine            | Death, relapse, disease onset             | Days from diagnosis to event       |
| Engineering         | Component failure                         | Operating hours until failure      |
| Business / SaaS     | Customer churn, subscription cancellation | Days since signup                  |
| HR / Workforce      | Employee attrition                        | Months from hire to resignation    |
| Finance             | Loan default                              | Months from origination to default |
| E-commerce          | First purchase, conversion                | Days from first visit              |

---

## Section Overview

| #   | Section                                                              | Level       | Key Questions Answered                                                   |
| --- | -------------------------------------------------------------------- | ----------- | ------------------------------------------------------------------------ |
| 1   | [**Core Concepts & Censoring**](./1-core-concepts.md)               | Foundation  | What is survival data? What is censoring? How do I structure the data?   |
| 2   | [**Survival & Hazard Functions**](./2-survival-hazard-functions.md) | Foundation  | How do I describe the survival process mathematically?                   |
| 3   | [**Kaplan-Meier Estimator**](./3-kaplan-meier.md)                   | Core        | How do I estimate and visualize survival curves from data?               |
| 4   | [**Log-Rank Test**](./4-log-rank-test.md)                           | Core        | How do I compare survival curves between two or more groups?             |
| 5   | [**Cox Proportional Hazards Model**](./5-cox-ph-model.md)           | Core        | How do covariates affect the hazard? What are hazard ratios?             |
| 6   | [**Model Diagnostics & Violations**](./6-diagnostics.md)            | Applied     | Is the proportional hazards assumption met? How do I check and fix it?   |
| 7   | [**Parametric Models**](./7-parametric-models.md)                   | Applied     | When and how to use Weibull, Exponential, Log-normal models?             |
| 8   | [**Interpretation**](./8-interpretation.md)                         | Applied     | How do I translate statistical outputs into meaningful conclusions?       |
| 9   | [**Visualization**](./9-visualization.md)                           | Applied     | What plots should I produce and how should I read them?                  |

---

## Analytical Workflow

```
Data Preparation  →  Descriptive Analysis  →  Model Fitting
(Section 1)          (Sections 2–4)           (Sections 5, 7)
                      KM curves, censoring      Cox / Parametric
                           ↓                         ↓
                  Diagnostics & Validation  →  Visualization & Interpretation
                  (Section 6)                  (Sections 8, 9)
```

---

## Visualization Quick Reference

| Chart                    | Best For                                                   | Section |
| ------------------------ | ---------------------------------------------------------- | ------- |
| Kaplan-Meier curve       | Visualizing overall or group-specific survival over time   | 3, 9    |
| Log-log plot             | Checking the proportional hazards assumption visually      | 6, 9    |
| Forest plot              | Displaying hazard ratios and confidence intervals          | 5, 9    |
| Schoenfeld residual plot | Diagnosing time-varying coefficients in Cox model          | 6, 9    |
| Cumulative hazard plot   | Alternative to KM; linear for exponential distributions    | 2, 9    |
| Calibration plot         | Comparing predicted vs. observed survival                  | 6, 9    |

---

## Key Takeaway

> Survival analysis answers: **"When does the event happen, and what factors speed it up or slow it down?"**  
> The defining challenge is censoring — observations where the event has not yet occurred carry real information and must not be discarded.
