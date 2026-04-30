# Regression Analysis

**Regression analysis** models the relationship between variables to understand how changes in one or more **predictor variables** (X) relate to changes in an **outcome variable** (Y). Unlike correlation, regression gives you a predictive equation and quantifies the effect of each variable.

> 📌 **核心原則**：Regression 的目標是「建立預測模型」與「量化變數間的影響關係」。它比相關分析更進一步，但仍需謹慎解讀因果關係。

---

## Why This Order?

The sections follow a natural progression from the simplest case to more complex models:

```
Two continuous variables? → Simple Linear Regression
Multiple predictors?      → Multiple Linear Regression
Binary outcome?           → Logistic Regression
```

Before fitting any regression model, you should already have done **descriptive statistics** and **bivariate analysis** (scatter plots, correlation) to understand your data.

---

## Overview of Topics

| #   | Section                                                                          | Level        | Key Questions Answered                                              |
| --- | -------------------------------------------------------------------------------- | ------------ | ------------------------------------------------------------------- |
| 1   | [**Simple Linear Regression**](./1-simple-linear-regression.md)                  | Foundation   | How does X predict Y? What is the best-fit line?                    |
| 2   | [**Multiple Linear Regression**](./2-multiple-linear-regression.md)              | Intermediate | How do multiple X variables jointly predict Y?                      |
| 3   | [**Logistic Regression**](./3-logistic-regression.md)                            | Intermediate | How do predictors relate to a binary outcome (Yes/No)?              |

---

## What's Inside Each Section

### 1. Simple Linear Regression

- The regression equation: Y = β₀ + β₁X + ε
- Ordinary Least Squares (OLS): what it minimizes and why
- Interpreting intercept (β₀) and slope (β₁)
- Model fit: R², Residual Standard Error
- Key assumptions and how to check them (residual plots, Q–Q plot)

### 2. Multiple Linear Regression

- Extending to multiple predictors: Y = β₀ + β₁X₁ + β₂X₂ + … + ε
- Interpreting coefficients (holding other variables constant)
- Adjusted R² vs R²
- Multicollinearity: VIF and why it matters
- Model selection: forward / backward / stepwise
- Categorical predictors: dummy coding

### 3. Logistic Regression

- When to use: binary outcomes (0/1, Yes/No, Pass/Fail)
- The logit transformation and odds ratio interpretation
- Model fit: Log-likelihood, AIC, pseudo-R²
- Classification metrics: Confusion matrix, Accuracy, Precision, Recall, AUC-ROC
- Assumptions and diagnostics

---

## Visualization Quick Reference

| Chart                       | Best For                                             |
| --------------------------- | ---------------------------------------------------- |
| Scatter plot + regression line | Simple linear regression fit                      |
| Residuals vs Fitted plot    | Checking linearity and homoscedasticity              |
| Q–Q plot of residuals       | Checking normality of residuals                      |
| Coefficient plot            | Comparing effect sizes in multiple regression        |
| Confusion matrix heatmap    | Evaluating logistic regression classification        |
| ROC curve                   | Comparing model discrimination ability               |
| Correlation heatmap         | Detecting multicollinearity before model fitting     |

---

## Key Assumptions Overview

| Assumption            | Simple LR | Multiple LR | Logistic |
| --------------------- | --------- | ----------- | -------- |
| Linearity             | ✅         | ✅           | ✅ (log-odds) |
| Independence          | ✅         | ✅           | ✅        |
| Homoscedasticity      | ✅         | ✅           | ❌ (not required) |
| Normality of residuals| ✅         | ✅           | ❌ (not required) |
| No multicollinearity  | —         | ✅           | ✅        |

> 📌 Always check assumptions **after** fitting the model, not before. The assumptions are about the **residuals**, not the raw data.

---

## Key Takeaway

> Regression analysis answers: **"How can I predict Y, and how much does each X contribute?"**  
> Always visualize your data first, check assumptions after fitting, and remember that a good R² does not guarantee a good model.

---
