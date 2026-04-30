# Descriptive Statistics

**Descriptive statistics** summarize and organize data so that patterns, trends, and relationships can be easily understood. It provides the foundation for all later inferential methods by helping us explore and describe data before drawing conclusions.

> 📌 **核心原則**：Descriptive statistics 只做「描述與摘要」，不涉及推論、假設檢定或預測。超出這個範圍的內容屬於 Inferential Statistics。

---

## Why This Order?

The sections follow a natural data exploration workflow:

```
What type of data do I have?
        ↓
Describe each variable individually (Univariate)
        ↓
Explore relationships between variables (Bivariate)
```

This order matters because **data type determines which statistics are valid**. Applying the wrong method to the wrong data type is one of the most common mistakes in practice.

---

## Overview of Topics

| #   | Section                                                            | Level           | Key Questions Answered                                  |
| --- | ------------------------------------------------------------------ | --------------- | ------------------------------------------------------- |
| 1   | [**Data Types & Measurement Scales**](./1-data-types.md)           | Foundation      | What kind of data is this? What operations are valid?   |
| 2   | [**Univariate – Categorical Data**](./2-univariate-categorical.md) | Single variable | How are categories distributed? What's the most common? |
| 3   | [**Univariate – Numerical Data**](./3-univariate-numerical.md)     | Single variable | Where is the center? How spread out? What shape?        |
| 4   | [**Bivariate Analysis**](./4-bivariate.md)                         | Two variables   | Are these two variables related? How strongly?          |
| 5   | [**Data Quality**](./5-data-quality.md)                            | Preparation     | Are missing values, outliers, and invalid values handled? |

---

## What's Inside Each Section

### 1. Data Types & Measurement Scales

- Nominal, Ordinal, Interval, Ratio (NOIR framework)
- Practical decision table: which stats are valid for each type
- How to check data types in Python/pandas

### 2. Univariate – Categorical Data

- Frequency tables, proportions, percentages
- Cross-tabulation (contingency table)
- Bar charts, pie charts, and when to use each

### 3. Univariate – Numerical Data

Three sub-topics that together fully describe a numerical variable:

| Sub-topic            | Measures                                                       |
| -------------------- | -------------------------------------------------------------- |
| **Central Tendency** | Mean (arithmetic, geometric, harmonic, weighted), Median, Mode |
| **Variability**      | Range, Variance, SD, SE (vs SD), IQR, CV, outlier detection    |
| **Shape**            | Skewness, Kurtosis (excess), visual normality checks           |

### 4. Bivariate Analysis

Organized by data type combinations:

| Combination               | Methods                                        |
| ------------------------- | ---------------------------------------------- |
| Numerical × Numerical     | Pearson r, Spearman ρ, Kendall τ, scatter plot |
| Categorical × Categorical | Cross-tabulation, grouped bar chart            |
| Numerical × Categorical   | Group comparison, boxplot by group             |
| Multiple variables        | Correlation matrix, heatmap, pairplot          |

### 5. Data Quality

| Check | Why It Matters |
| ----- | -------------- |
| Missing data | Can bias summaries and reduce power |
| Outliers | Can distort means, SD, correlation, and regression |
| Duplicates | Can overweight repeated records |
| Invalid values | Can create impossible or misleading results |

---

## Visualization Quick Reference

| Chart        | Best For                                     | Data Type             |
| ------------ | -------------------------------------------- | --------------------- |
| Bar chart    | Category counts / proportions                | Categorical           |
| Pie chart    | Part-of-whole (≤ 5 categories only)          | Categorical           |
| Histogram    | Distribution shape                           | Numerical             |
| Boxplot      | Spread, median, outliers, group comparison   | Numerical             |
| Scatter plot | Relationship between two numerical variables | Numerical × Numerical |
| Q–Q plot     | Visual normality check                       | Numerical             |
| Heatmap      | Correlation matrix overview                  | Numerical × Numerical |
| Missingness matrix | Pattern of missing data                 | Any dataset           |

---

## Key Takeaway

> Descriptive statistics answers: **"What does my data look like?"**  
> Always pair numerical summaries with visualization — numbers alone can be misleading.
