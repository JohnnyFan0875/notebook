# Statsmodels Documentation

This folder contains structured notes and examples for **Statsmodels**, a Python library for statistical modeling and inference.

## Table of Contents

### [Linear Regression](linear-regression.md)

- Ordinary Least Squares (OLS) [regression](../../supervised-learning/regression/README.md)
- Model fitting with formula API
- Parameters, summary, predictions
- Evaluation metrics: [MSE, RMSE, R²](metrics.md)
- Diagnostics: [Leverage, Cook’s Distance](diagnostics.md)

### [Logistic Regression](logistic-regression.md)

- [Logistic regression](../../supervised-learning/classification/logistic-regression.md) for binary [classification](../../supervised-learning/classification/README.md)
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

- **[Linear regression](../../supervised-learning/regression/linear.md) metrics**: [MSE](../../evaluation/mse-rmse.md), [RMSE](../../evaluation/mse-rmse.md), MAE, R², Adjusted R²
- **[Logistic regression](../../supervised-learning/classification/logistic-regression.md) metrics**: Pseudo R², [confusion matrix](../../evaluation/confusion-metrics.md), classification metrics

### [Diagnostics](diagnostics.md)

- Residual analysis
- Leverage
- Cook’s Distance
- DFBETAs
- DFFITS
- Influence plots

## Statsmodels vs. Scikit-learn

| Aspect        | Statsmodels                                                               | [Scikit-learn](../scikit-learn/README.md)                                      |
| ------------- | ------------------------------------------------------------------------- | ------------------------------------------------- |
| **Focus**     | Statistical inference, hypothesis testing, detailed summaries             | Predictive modeling, machine learning [pipeline](../../workflow/pipeline-basic.md)s   |
| **API**       | Formula-based (similar to R): `ols('y ~ x', data=df).fit()`               | Object-oriented: `LinearRegression().fit(X, y)`   |
| **Outputs**   | Rich statistical output (p-values, confidence intervals, test statistics) | Prediction-focused, fewer statistical diagnostics |
| **Metrics**   | Built-in regression metrics (`mse_resid`, `rsquared`, etc.)               | Metrics available via `sklearn.metrics`           |
| **Use Cases** | Research, academic analysis, when interpretability and inference matter   | Production ML, [cross-validation](../../workflow/cross-validation.md), model deployment |

## Key Takeaways

- Use **Statsmodels** when you need detailed **statistical inference** (p-values, CIs, ANOVA, diagnostics).
- Use **Scikit-learn** when your focus is on **prediction, [pipeline](../../workflow/pipeline-basic.md)s, and deployment**.
- They can be complementary: fit models in Statsmodels for inference, then use Scikit-learn for prediction [pipeline](../../workflow/pipeline-basic.md)s and validation.

[Back to Packages](../README.md)
