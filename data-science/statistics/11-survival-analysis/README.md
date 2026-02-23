# Survival Analysis

**Survival analysis** is a cornerstone of biostatistics and reliability research, designed to study **time-to-event data** — how long it takes for a defined outcome to occur (e.g., death, disease recurrence, mechanical failure).  
Unlike classical regression, it accounts for **censoring**, where the exact event time is unknown for some individuals, and models how risk evolves over time.

This section of the documentation provides a comprehensive yet practical guide to survival analysis, covering theory, modeling, diagnostics, and interpretation — from foundational concepts to applied biomedical use cases.

## Overview

| Theme                | Description                                                       |
| -------------------- | ----------------------------------------------------------------- |
| **Purpose**          | Quantify and model the duration until an event occurs.            |
| **Typical outcomes** | Death, relapse, recovery, device failure, progression.            |
| **Core challenge**   | Handling **censored** data and **time-dependent** risk.           |
| **Applications**     | Clinical trials, epidemiology, genomics, engineering reliability. |

Survival analysis helps answer questions such as:

- What is the **probability of survival** at a given time?
- Which factors **increase or decrease risk**?
- Do different groups (e.g., treatment vs. control) show **significant survival differences**?

## Module Structure

This guide is organized into three sections, reflecting the typical analytical workflow —  
from understanding core principles to modeling and communicating results.

### **1. Basics (`basics/`)**

Foundational theory and essential concepts.

- [Introduction](./basics/introduction.md) — What survival analysis is and why it matters
- [Censoring Types](./basics/censoring-types.md) — Right, left, and interval censoring
- [Summary Measures](./basics/summary-measures.md) — Median survival, RMST, hazard ratios

### **2. Models (`models/`)**

Statistical models used to estimate survival and evaluate covariate effects.

- [Kaplan–Meier & Log-rank](./models/kaplan-meier-and-logrank.md) — Non-parametric estimation and comparison
- [Cox Proportional Hazards Model](./models/cox-model.md) — Semi-parametric regression for relative risk
- [Parametric Models](./models/parametric-models.md) — Weibull, exponential, and log-normal frameworks
- [Model Diagnostics](./models/model-diagnostics.md) — Assumption checks, residuals, and validation

### **3. Reporting & Visualization (`reporting/`)**

Guidelines for presenting, validating, and interpreting survival analysis results.

- [Visualization](./reporting/visualization.md) — KM plots, hazard curves, and diagnostic visuals
- [Interpretation](./reporting/interpretation.md) — Translating statistical results into biological or clinical meaning

## Analytical Workflow Summary

```text
Data Preparation  →  Exploratory Analysis  →  Model Fitting
                   (KM curves, censoring)     (Cox / Parametric)
                   ↓                          ↓
            Diagnostics & Validation  →  Visualization & Interpretation
```
