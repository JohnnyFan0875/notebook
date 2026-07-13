# Introduction

This section covers core statistics topics, including descriptive statistics, probability, inference, regression, ANOVA, non-parametric methods, Bayesian statistics, time series, multivariate analysis, experimental design, and survival analysis.

**Note:**

- Statistics is not just a collection of tests.
- A good workflow moves from understanding the data, to choosing an appropriate model, to checking assumptions, and finally to interpreting results in context.
- Many statistical mistakes happen because people jump straight to a favorite test. In practice, most good analysis starts with **data quality checks and visual exploration**.

## Modules

| Module                                                                   | Core Topics                                                      | Main Questions                                                                |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| [Descriptive Statistics](./descriptive-statistics/README.md)             | Data types, summaries, plots, and data quality                   | What does my data look like? Are there missing values or outliers?            |
| [Probability & Distributions](./probability-and-distributions/README.md) | Random variables, probability rules, and common distributions    | How do random variables behave? Which distribution fits this situation?       |
| [Inferential Statistics](./inferential-statistics/README.md)             | Sampling, confidence intervals, p-values, assumptions, and ANOVA | What can a sample tell me about a population, and how do group means compare? |
| [Regression Analysis](./regression-analysis/README.md)                   | Linear and logistic models, interpretation, and diagnostics      | How does Y change with one or more predictors?                                |
| [Non-parametric Methods](./nonparametric-methods/README.md)              | Rank-based tests and assumption-robust alternatives              | What should I use when normality or equal variance assumptions fail?          |
| [Bayesian Statistics](./bayesian-statistics/README.md)                   | Priors, likelihoods, posteriors, and MCMC                        | How should prior knowledge and new evidence be combined?                      |
| [Time Series Analysis](./time-series-analysis/README.md)                 | Trend, seasonality, autocorrelation, and forecasting             | What patterns exist over time, and how can we forecast?                       |
| [Multivariate Analysis](./multivariate-analysis/README.md)               | PCA, clustering, regression, and diagnostics                     | How do many variables relate or form structure together?                      |
| [Experimental Design](./experimental-design/README.md)                   | Study planning, bias control, and sample size                    | How should data be collected to support valid conclusions?                    |
| [Survival Analysis](./survival-analysis/README.md)                       | Time-to-event data, censoring, and hazard modeling               | When does an event happen, and what affects its timing?                       |

## Three Habits to Keep Throughout

| Habit                               | Why it matters                                                                         |
| ----------------------------------- | -------------------------------------------------------------------------------------- |
| Visualize before testing            | Plots often reveal structure, outliers, skew, and design problems faster than p-values |
| Check assumptions after fitting     | Most assumptions concern residuals, dependence, or model form, not just raw data       |
| Report effect size with uncertainty | Statistical significance alone rarely answers whether the result is important          |
