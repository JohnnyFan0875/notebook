# Statistics Notebook

This repository is a structured statistics notebook for beginner data analysts. It focuses on practical understanding: when to use each method, how to interpret results, what assumptions to check, and which formulas are worth remembering.

> 📌 **中文重點**：這份筆記的目標不是推導所有統計理論，而是幫助初學資料分析人員建立「看懂資料、選對方法、正確解讀」的能力。

---

## Learning Path

| Step | Module                                                                     | Why It Comes Here                                               |
| ---- | -------------------------------------------------------------------------- | --------------------------------------------------------------- |
| 1    | [Descriptive Statistics](./1-descriptive-statistics/README.md)             | Understand data types, summaries, plots, and data quality       |
| 2    | [Probability & Distributions](./2-probability-and-distributions/README.md) | Build the probability foundation for inference                  |
| 3    | [Inferential Statistics](./3-inferential-statistics/README.md)             | Learn sampling, confidence intervals, p-values, and assumptions |
| 4    | [Regression Analysis](./4-regression-analysis/README.md)                   | Model relationships and prediction                              |
| 5    | [ANOVA](./5-anova/README.md)                                               | Compare means across multiple groups                            |
| 6    | [Non-parametric Methods](./6-non-parametric-methods/README.md)             | Use robust alternatives when assumptions fail                   |
| 7    | [Bayesian Statistics](./7-bayesian-statistics/README.md)                   | Update beliefs with data and quantify uncertainty differently   |
| 8    | [Time Series Analysis](./8-time-series-analysis/README.md)                 | Analyze ordered observations over time                          |
| 9    | [Multivariate Analysis](./9-multivariate-analysis/README.md)               | Work with many variables at once                                |
| 10   | [Experimental Design](./10-experimental-design/README.md)                  | Plan valid studies and experiments                              |
| 11   | [Survival Analysis](./11-survival-analysis/README.md)                      | Analyze time-to-event data and censoring                        |

---

## Module Map

| Module                      | Main Questions                                                          |
| --------------------------- | ----------------------------------------------------------------------- |
| Descriptive Statistics      | What does my data look like? Are there missing values or outliers?      |
| Probability & Distributions | How do random variables behave? Which distribution fits this situation? |
| Inferential Statistics      | What can a sample tell me about a population?                           |
| Regression Analysis         | How does Y change with one or more predictors?                          |
| ANOVA                       | Do three or more group means differ? Which groups differ?               |
| Non-parametric Methods      | What should I use when normality or equal variance assumptions fail?    |
| Bayesian Statistics         | How should prior knowledge and new evidence be combined?                |
| Time Series Analysis        | What patterns exist over time, and how can we forecast?                 |
| Multivariate Analysis       | How do many variables relate or form structure together?                |
| Experimental Design         | How should data be collected to support valid conclusions?              |
| Survival Analysis           | When does an event happen, and what affects its timing?                 |

---

## How to Read

| If You Want To...         | Start With                                                                    |
| ------------------------- | ----------------------------------------------------------------------------- |
| Learn from the beginning  | Follow the Learning Path above                                                |
| Choose a statistical test | [Common Statistical Tests](./3-inferential-statistics/4-statistical-tests.md) |
| Check assumptions         | [Assumption Checks](./3-inferential-statistics/5-assumption-checks.md)        |
| Compare multiple groups   | [ANOVA](./5-anova/README.md)                                                  |
| Handle messy data         | [Data Quality](./1-descriptive-statistics/5-data-quality.md)                  |
| Build prediction models   | [Regression Analysis](./4-regression-analysis/README.md)                      |

---

## Style Guide

| Principle       | How This Notebook Applies It                                          |
| --------------- | --------------------------------------------------------------------- |
| Beginner-first  | Concepts before formulas; formulas only when commonly used            |
| Table-heavy     | Comparisons and decision rules are summarized in tables               |
| Bilingual hints | Important ideas include concise Chinese notes                         |
| Practical focus | Python examples and interpretation guidance are included              |
| Quarto-ready    | Module README files can become overview pages in a future Quarto book |

---

## Quarto Note

This notebook is currently Markdown-first. When converted to Quarto, chapter order should be defined explicitly in `_quarto.yml`; Quarto will not automatically treat every `README.md` as a section homepage unless it is listed in the book configuration.

Recommended future structure:

```yaml
book:
  title: "Statistics Notebook"
  chapters:
    - index.qmd
    - part: "Descriptive Statistics"
      chapters:
        - 1-descriptive-statistics/README.md
        - 1-descriptive-statistics/1-data-types.md
        - 1-descriptive-statistics/2-univariate-categorical.md
```
