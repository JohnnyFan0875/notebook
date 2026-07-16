# Descriptive Statistics

**Descriptive statistics** summarize and organize data so that patterns, trends, and relationships can be easily understood.  
It provides the foundation for all later inferential methods by helping us explore and describe data before drawing conclusions.

**Key point**

- Descriptive statistics is for describing and summarizing what the data looks like.
- Once you start generalizing beyond the observed data, you have moved into **inferential statistics**.

## Why This Order?

The sections follow a natural data exploration workflow:

```
Is the dataset analysis-ready?
        ↓
What type of data do I have?
        ↓
Describe each variable individually (Univariate)
        ↓
Explore relationships between variables (Bivariate)
```

This order matters because **basic data quality issues can invalidate later summaries**, and **data type determines which statistics are valid**. Applying the wrong method to the wrong data type is one of the most common mistakes in practice.

## Sections

| Section                                                          | Focus                                                                 | Key Questions Answered                                    |
| ---------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------- |
| [**Data Quality**](./data-quality.md)                            | Missing data, outliers, duplicates, and invalid values                | Is the dataset analysis-ready? What needs checking first? |
| [**Data Types & Measurement Scales**](./data-types.md)           | NOIR framework, valid operations, and practical type checking         | What kind of data is this? What operations are valid?     |
| [**Univariate – Categorical Data**](./univariate-categorical.md) | Frequency tables, proportions, cross-tabulation, and category plots   | How are categories distributed? What's the most common?   |
| [**Univariate – Numerical Data**](./univariate-numerical.md)     | Center, spread, shape, and numerical distribution summaries           | Where is the center? How spread out? What shape?          |
| [**Bivariate Analysis**](./bivariate.md)                         | Relationships across numerical, categorical, and mixed variable pairs | Are these two variables related? How strongly?            |

## Notes by Section

### Data Quality

| Check Area                 | What to Review                                                |
| -------------------------- | ------------------------------------------------------------- |
| **Missing data**           | Missing counts, missing rates, concentration by group or time |
| **Outliers**               | Visual flags, IQR screen, whether values are real or errors   |
| **Duplicates**             | Repeated rows, repeated identifiers, accidental double-counts |
| **Invalid values / units** | Impossible ranges, wrong units, encoded missing placeholders  |
| **Useful visuals**         | Missingness matrix, boxplot for quick anomaly screening       |
| **Triage before modeling** | Fix quality issues before interpreting summaries or models    |

### Data Types & Measurement Scales

| Topic                 | What It Covers                                               |
| --------------------- | ------------------------------------------------------------ |
| **NOIR scales**       | Nominal, Ordinal, Interval, Ratio                            |
| **Representation**    | Structured vs unstructured data                              |
| **Numerical subtype** | Continuous vs discrete                                       |
| **Practical typing**  | pandas dtypes, coded variables, identifiers, metadata checks |
| **Chart selection**   | Bar chart for categorical; histogram / boxplot for numerical |
| **Type error risks**  | Why wrong typing contaminates later analysis                 |

### Univariate – Categorical Data

| Sub-topic                   | Measures / Ideas                               |
| --------------------------- | ---------------------------------------------- |
| **Frequency table**         | Count, proportion, percentage                  |
| **Ordinal handling**        | Ordered categories, cumulative percentage      |
| **Visualization**           | Vertical bar, horizontal bar, pie, ordered bar |
| **Category interpretation** | Relative frequency, rare categories, grouping  |

### Univariate – Numerical Data

| Sub-topic            | Measures                                             |
| -------------------- | ---------------------------------------------------- |
| **Central Tendency** | Mean, Median, Mode                                   |
| **Variability**      | Range, Variance, SD, SE, IQR, CV, outlier            |
| **Shape**            | Skewness, Kurtosis (excess), visual normality checks |
| **Visualization**    | Histogram, boxplot, Q–Q plot                         |

### Bivariate Analysis

| Combination               | Methods                                        |
| ------------------------- | ---------------------------------------------- |
| Numerical × Numerical     | Pearson r, Spearman ρ, Kendall τ, scatter plot |
| Categorical × Categorical | Cross-tabulation, grouped bar chart            |
| Numerical × Categorical   | Group comparison, boxplot by group             |
| Multiple variables        | Correlation matrix, heatmap, pairplot          |
