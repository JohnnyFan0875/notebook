# Introduction to Survival Analysis

**Survival analysis** is a statistical framework for modeling and interpreting **time-to-event data** — that is, data describing the duration until a defined event occurs.  
Typical events include death, disease recurrence, recovery, equipment failure, or any transition of clinical or biological state.

Unlike classical regression models, survival analysis must account for **censoring**, where the exact event time is unknown for some individuals.  
Correctly handling censored observations allows the analysis to make full use of incomplete but valuable information.

## Why Survival Analysis?

Many biomedical and epidemiological studies are interested not only in **whether** an event occurs, but also **when** it occurs.

| Challenge                                                     | Why ordinary regression fails                              |
| ------------------------------------------------------------- | ---------------------------------------------------------- |
| Some participants never experience the event during follow-up | Their information is partially censored                    |
| Follow-up durations differ between individuals                | Time must be explicitly modeled                            |
| Hazard (risk) changes over time                               | Requires time-dependent modeling, not a single probability |

Survival methods address these challenges by estimating the probability of survival over time and identifying factors that influence risk.

## Core Concepts

| Concept               | Definition                                                            | Typical Symbol       |
| --------------------- | --------------------------------------------------------------------- | -------------------- |
| **Event**             | Outcome of interest (death, relapse, recovery)                        | —                    |
| **Time-to-event**     | Duration between study entry and event or censoring                   | \(T\)                |
| **Censoring**         | Incomplete observation of event time                                  | —                    |
| **Survival function** | Probability of surviving beyond time \(t\)                            | \(S(t) = P(T > t)\)  |
| **Hazard function**   | Instantaneous risk of event at time \(t\), given survival up to \(t\) | \(h(t)\)             |
| **Cumulative hazard** | Total accumulated risk up to time \(t\)                               | \(H(t) = -\ln S(t)\) |

Together, these functions describe both the **shape** and **timing** of risk in a population.

## Common Analytical Approaches

| Category            | Method                                                                    | Description                                                        |
| ------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Non-parametric**  | [Kaplan–Meier estimator](../models/kaplan-meier-and-logrank.md)           | Estimates survival probabilities without assuming a distribution.  |
| **Semi-parametric** | [Cox proportional hazards model](../models/cox-model.md)                  | Evaluates covariate effects under proportional hazards assumption. |
| **Parametric**      | [Weibull, Exponential, Log-normal models](../models/parametric-models.md) | Assume specific distributions for event times.                     |

These methods can be complemented by diagnostic and visualization tools that assess model fit and interpretability.

## Structure of This Section

This survival-analysis guide is organized into three thematic parts:

1. **Basics (`basics/`)**

   - [Introduction](./introduction.md)
   - [Censoring Types](./censoring-types.md)
   - [Summary Measures](./summary-measures.md)

2. **Models (`01_models/`)**

   - [Kaplan–Meier & Log-rank](../models/kaplan-meier-and-logrank.md)
   - [Cox Model](../models/cox-model.md)
   - [Parametric Models](../models/parametric-models.md)
   - [Model Diagnostics](../models/model-diagnostics.md)

3. **Reporting & Interpretation (`02_reporting/`)**
   - [Visualization](../reporting/visualization.md)
   - [Interpretation](../reporting/interpretation.md)

## Key Takeaways

- Survival analysis focuses on **time until event**, not just event occurrence.
- **Censoring** is central — properly handled, it preserves statistical power.
- **Kaplan–Meier**, **Cox**, and **parametric models** form the backbone of most analyses.
- Visual and diagnostic tools ensure **interpretability** and **model validity**.

> Survival analysis bridges biostatistics, clinical research, and machine learning — forming the foundation for modern risk prediction and outcome modeling.
