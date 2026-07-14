# Statsmodels

This folder contains structured notes and examples for **Statsmodels**, a Python library for statistical modeling and inference.

## 建議閱讀順序

1. [Linear Regression](linear-regression.md): 先理解 formula API、summary table 與係數解讀。
2. [Diagnostics](diagnostics.md): 不要等模型出問題才回頭補殘差、影響點與 leverage。
3. [Metrics](metrics.md): 把回歸與分類常見評估指標放回 inference 脈絡中理解。
4. [Logistic Regression](logistic-regression.md): 當目標變成二元分類時，再看機率輸出與 pseudo R²。
5. [ANOVA](anova.md): 當問題回到 group comparison、factor effect 與 post-hoc testing 時使用。

## 主題地圖

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

## 這一章要解決什麼

- 如果我想看係數、p-values、confidence intervals 與完整 summary table，該怎麼開始？
- 什麼情況適合用 Statsmodels，而不是只用 Scikit-learn 的 estimator API？
- 做完模型後，還需要看哪些 diagnostics 才能判斷結果是否可信？

[Back to Packages](../README.md)
