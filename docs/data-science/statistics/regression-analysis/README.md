# Introduction

**Regression analysis** models the relationship between variables to understand how changes in one or more **predictor variables** (X) relate to changes in an **outcome variable** (Y). Unlike correlation, regression gives you a predictive equation and quantifies the effect of each variable.

Key point: Regression is used to build predictive equations and estimate how strongly predictors relate to an outcome. It goes beyond correlation, but it still does not prove causation by itself.

## The Core Mindset

Regression is easiest to learn when you separate three jobs that people often mix together:

1. **description**: how are X and Y associated in this dataset?
2. **prediction**: how well can X help predict Y for new observations?
3. **explanation**: after adjusting for other variables, what does each coefficient mean?

These goals overlap, but they are not identical. A model that predicts well is not automatically easy to interpret, and a model with interpretable coefficients is not automatically causal.

## Why This Order?

The sections follow a natural progression from the simplest case to more complex models:

```
Two continuous variables? → Simple Linear Regression
Multiple predictors?      → Multiple Linear Regression
Binary outcome?           → Logistic Regression
```

Before fitting any regression model, you should already have done **descriptive statistics** and **bivariate analysis** (scatter plots, correlation) to understand your data.

## Overview of Topics

| Section | Level | Key Questions Answered |
| -------------------------------------------------------------------------------- | ------------ | ------------------------------------------------------------------- |
| [**Simple Linear Regression**](./simple-linear-regression.md) | Foundation | How does X predict Y? What is the best-fit line? |
| [**Multiple Linear Regression**](./multiple-linear-regression.md) | Intermediate | How do multiple X variables jointly predict Y? |
| [**Logistic Regression**](./logistic-regression.md) | Intermediate | How do predictors relate to a binary outcome (Yes/No)? |

## What's Inside Each Section

### Simple Linear Regression

- The regression equation: Y = β₀ + β₁X + ε
- Ordinary Least Squares (OLS): what it minimizes and why
- Interpreting intercept (β₀) and slope (β₁)
- Model fit: R², Residual Standard Error
- Key assumptions and how to check them (residual plots, Q–Q plot)

### Multiple Linear Regression

- Extending to multiple predictors: Y = β₀ + β₁X₁ + β₂X₂ + … + ε
- Interpreting coefficients (holding other variables constant)
- Adjusted R² vs R²
- Multicollinearity: VIF and why it matters
- Model selection: forward / backward / stepwise
- Categorical predictors: dummy coding

### Logistic Regression

- When to use: binary outcomes (0/1, Yes/No, Pass/Fail)
- The logit transformation and odds ratio interpretation
- Model fit: Log-likelihood, AIC, pseudo-R²
- Classification metrics: Confusion matrix, Accuracy, Precision, Recall, AUC-ROC
- Assumptions and diagnostics

## Visualization Quick Reference

| Chart | Best For |
| --------------------------- | ---------------------------------------------------- |
| Scatter plot + regression line | Simple linear regression fit |
| Residuals vs Fitted plot | Checking linearity and homoscedasticity |
| Q–Q plot of residuals | Checking normality of residuals |
| Coefficient plot | Comparing effect sizes in multiple regression |
| Confusion matrix heatmap | Evaluating logistic regression classification |
| ROC curve | Comparing model discrimination ability |
| Correlation heatmap | Detecting multicollinearity before model fitting |

## Key Assumptions Overview

| Assumption | Simple LR | Multiple LR | Logistic |
| --------------------- | --------- | ----------- | -------- |
| Linearity | ✅ | ✅ | ✅ (log-odds) |
| Independence | ✅ | ✅ | ✅ |
| Homoscedasticity | ✅ | ✅ | ❌ (not required) |
| Normality of residuals | ✅ | ✅ | ❌ (not required) |
| No multicollinearity | — | ✅ | ✅ |

Key point: Always check assumptions after fitting the model, not before. The assumptions are about the residuals, not the raw data.

## A Recommended Reading Order

If you are working on an actual dataset, this reading and analysis order is usually effective:

1. start with scatter plots, distributions, and missingness checks
2. fit the simplest defensible model first
3. inspect residuals and diagnostics
4. only then add complexity such as more predictors or classification thresholds

Tip: Many regression problems become easier when you first write down the exact prediction question, target variable, and what each row of the dataset represents.

## Common Interpretation Traps

| Trap | Better interpretation |
| ---- | --------------------- |
| "A significant coefficient proves causation" | Significance only shows association under the model and assumptions |
| "High R² means the model is good" | Also inspect residuals, generalization, and whether the form makes sense |
| "A non-significant coefficient means no relationship exists" | It may reflect low power, collinearity, noise, or misspecification |
| "Logistic regression coefficient equals probability change" | Logistic coefficients act on log-odds; convert to odds ratios or predicted probabilities |

## Key Takeaway

Regression analysis answers: "How can I predict Y, and how much does each X contribute?" Always visualize your data first, check assumptions after fitting, and remember that a good R² does not guarantee a good model.
