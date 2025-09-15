# Statsmodels Documentation

This folder contains structured notes and examples for **Statsmodels**, a Python library for statistical modeling and inference.

## Table of Contents

### [Linear Regression](linear-regression.md)

- Ordinary Least Squares (OLS) regression
- Model fitting with formula API
- Parameters, summary, predictions
- Evaluation metrics: [MSE, RMSE, R²](metrics.md)
- Diagnostics: [Leverage, Cook’s Distance](diagnostics.md)

### [Logistic Regression](logistic-regression.md)

- Logistic regression for binary classification
- Predicted probabilities and class labels
- Confusion matrix, accuracy, precision, recall, F1-score
- Pseudo R²
- Diagnostics: [Leverage, Cook’s Distance](diagnostics.md)

### [ANOVA](anova.md)

- One-way ANOVA
- Two-way ANOVA
- ANCOVA (Analysis of Covariance)
- Post-hoc tests (Tukey HSD)

### [Metrics](metrics.md)

- **Linear regression metrics**: MSE, RMSE, MAE, R², Adjusted R²
- **Logistic regression metrics**: Pseudo R², confusion matrix, classification metrics

### [Diagnostics](diagnostics.md)

- Residual analysis
- Leverage
- Cook’s Distance
- DFBETAs
- DFFITS
- Influence plots

## Statsmodels vs. Scikit-learn

| Aspect        | Statsmodels                                                               | Scikit-learn                                      |
| ------------- | ------------------------------------------------------------------------- | ------------------------------------------------- |
| **Focus**     | Statistical inference, hypothesis testing, detailed summaries             | Predictive modeling, machine learning pipelines   |
| **API**       | Formula-based (similar to R): `ols('y ~ x', data=df).fit()`               | Object-oriented: `LinearRegression().fit(X, y)`   |
| **Outputs**   | Rich statistical output (p-values, confidence intervals, test statistics) | Prediction-focused, fewer statistical diagnostics |
| **Metrics**   | Built-in regression metrics (`mse_resid`, `rsquared`, etc.)               | Metrics available via `sklearn.metrics`           |
| **Use Cases** | Research, academic analysis, when interpretability and inference matter   | Production ML, cross-validation, model deployment |

## Key Takeaways

- Use **Statsmodels** when you need detailed **statistical inference** (p-values, CIs, ANOVA, diagnostics).
- Use **Scikit-learn** when your focus is on **prediction, pipelines, and deployment**.
- They can be complementary: fit models in Statsmodels for inference, then use Scikit-learn for prediction pipelines and validation.
