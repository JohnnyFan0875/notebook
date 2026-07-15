# Descriptive Statistics

**Descriptive statistics** summarize and organize data so that patterns, trends, and relationships can be easily understood.  
It provides the foundation for all later inferential methods by helping us explore and describe data before drawing conclusions.

**Key point**

- Descriptive statistics is for describing and summarizing what the data looks like.
- Once you start generalizing beyond the observed data, you have moved into **inferential statistics**.

## Why This Order?

The sections follow a natural data exploration workflow:

```
What type of data do I have?
        ↓
Describe each variable individually (Univariate)
        ↓
Explore relationships between variables (Bivariate)
```

This order matters because **data type determines which statistics are valid**.   Applying the wrong method to the wrong data type is one of the most common mistakes in practice.

## Sections

| Section                                                          | Focus                                                                 | Key Questions Answered                                    |
| ---------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------- |
| [**Data Types & Measurement Scales**](./data-types.md)           | NOIR framework, valid operations, and practical type checking         | What kind of data is this? What operations are valid?     |
| [**Univariate – Categorical Data**](./univariate-categorical.md) | Frequency tables, proportions, cross-tabulation, and category plots   | How are categories distributed? What's the most common?   |
| [**Univariate – Numerical Data**](./univariate-numerical.md)     | Center, spread, shape, and numerical distribution summaries           | Where is the center? How spread out? What shape?          |
| [**Bivariate Analysis**](./bivariate.md)                         | Relationships across numerical, categorical, and mixed variable pairs | Are these two variables related? How strongly?            |
| [**Data Quality**](./data-quality.md)                            | Missing data, outliers, duplicates, and invalid values                | Are missing values, outliers, and invalid values handled? |

## Notes by Section

### Univariate – Numerical Data

Three sub-topics together describe a numerical variable:

| Sub-topic            | Measures                                                       |
| -------------------- | -------------------------------------------------------------- |
| **Central Tendency** | Mean (arithmetic, geometric, harmonic, weighted), Median, Mode |
| **Variability**      | Range, Variance, SD, SE (vs SD), IQR, CV, outlier detection    |
| **Shape**            | Skewness, Kurtosis (excess), visual normality checks           |

### Bivariate Analysis

Common pairings by data type:

| Combination               | Methods                                        |
| ------------------------- | ---------------------------------------------- |
| Numerical × Numerical     | Pearson r, Spearman ρ, Kendall τ, scatter plot |
| Categorical × Categorical | Cross-tabulation, grouped bar chart            |
| Numerical × Categorical   | Group comparison, boxplot by group             |
| Multiple variables        | Correlation matrix, heatmap, pairplot          |

### Data Quality

| Check          | Why It Matters                                     |
| -------------- | -------------------------------------------------- |
| Missing data   | Can bias summaries and reduce power                |
| Outliers       | Can distort means, SD, correlation, and regression |
| Duplicates     | Can overweight repeated records                    |
| Invalid values | Can create impossible or misleading results        |

## Visualization Quick Reference

| Chart              | Best For                                     | Data Type             |
| ------------------ | -------------------------------------------- | --------------------- |
| Bar chart          | Category counts / proportions                | Categorical           |
| Pie chart          | Part-of-whole (≤ 5 categories only)          | Categorical           |
| Histogram          | Distribution shape                           | Numerical             |
| Boxplot            | Spread, median, outliers, group comparison   | Numerical             |
| Scatter plot       | Relationship between two numerical variables | Numerical × Numerical |
| Q–Q plot           | Visual normality check                       | Numerical             |
| Heatmap            | Correlation matrix overview                  | Numerical × Numerical |
| Missingness matrix | Pattern of missing data                      | Any dataset           |
