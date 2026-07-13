# Pandas: Handling Missing Data

Missing data is not just a cleaning nuisance. It can change summary statistics, distort model behavior, and hide important patterns in how the data was collected.

## Practical Workflow

When missing values show up, a reliable order of operations is:

1. Standardize all missing markers to real null values like `NaN` / `pd.NA`.
2. Measure how much data is missing and where it appears.
3. Decide whether the missingness is ignorable, informative, or structurally meaningful.
4. Choose deletion, imputation, or interpolation based on that pattern.
5. Validate that the treated dataset still behaves reasonably.

This is the part many people skip: filling values should be the middle of the workflow, not the first step.

## Example Dataset

```python
import seaborn as sns
import pandas as pd
import numpy as np

iris = sns.load_dataset("iris").copy()
iris.loc[0, "sepal_length"] = np.nan
iris.loc[5, "sepal_width"] = np.nan
iris.loc[10, "petal_length"] = np.nan
```

## Step 1: Normalize Missing Markers

Real datasets often use placeholders like `"."`, `"NA"`, `"-"`, or even `0` to mean "missing". Converting them early avoids mixing real values with sentinel values.

```python
df = pd.read_csv("data.csv", na_values=[".", "NA", "missing"])

# If 0 really means "measurement not recorded"
df["glucose"] = df["glucose"].replace(0, np.nan)
```

- `na_values=` helps during import.
- `.replace(..., np.nan)` is useful when the file has hidden missing-value conventions.
- Only replace values like `0` when domain knowledge says they are impossible or placeholders.

## Step 2: Detect Missing Data

```python
df.isna().head()
df.isna().sum()
df.isna().mean().sort_values(ascending=False)
df.isna().any()

# Rows containing at least one missing value
df[df.isna().any(axis=1)]
```

- `.isna().sum()` gives counts.
- `.isna().mean()` is a quick way to compute missing-value percentages by column.
- Sorting the percentages helps you find the columns that deserve attention first.

If a dataset has columns that are completely empty, it is often worth identifying them separately:

```python
df.isna().all()
df.columns[df.isna().all()]
```

These columns are different from "partially missing" columns because they carry no observed information at all.

## Step 3: Understand the Missingness Mechanism

Before choosing a method, ask why values are missing.

### MCAR, MAR, MNAR

- `MCAR` (Missing Completely at Random): missingness is unrelated to observed or unobserved values.
- `MAR` (Missing at Random): missingness depends on other observed variables.
- `MNAR` (Missing Not at Random): missingness depends on the value itself or another unobserved mechanism.

Examples:

- `MCAR`: a sensor randomly fails for a few timestamps.
- `MAR`: income is missing more often for people in a certain occupation field.
- `MNAR`: people with very high debt are less likely to report debt.

This distinction matters because:

- deletion is safest when values are close to `MCAR`
- simple imputation is often acceptable for light `MCAR` / `MAR`
- `MNAR` usually means the missingness itself carries signal and should be treated carefully

## Graphical Analysis with `missingno`

When the pattern is not obvious from counts alone, `missingno` is helpful.

```python
import missingno as msno

msno.bar(df)
msno.matrix(df)
msno.heatmap(df)
msno.dendrogram(df)
```

- `msno.bar(df)` compares completeness by column.
- `msno.matrix(df)` shows row-wise gaps and whether missingness looks random or clustered.
- `msno.heatmap(df)` shows correlations in missingness between columns.
- `msno.dendrogram(df)` groups columns with similar missingness structure.

If two columns tend to be missing together, that often suggests process-related dependency rather than pure randomness.

## Fill Missing Values with Pandas

```python
df.fillna(0)

df["sepal_length"] = df["sepal_length"].fillna(df["sepal_length"].mean())

df = df.fillna({
    "sepal_length": df["sepal_length"].mean(),
    "sepal_width": df["sepal_width"].median(),
})

df = df.ffill()
df = df.bfill()
```

- Mean works best for roughly symmetric numeric data.
- Median is usually safer when outliers exist.
- Mode or constant fill is common for categorical variables.
- Forward / backward fill is mainly for ordered data such as time series.

## Statistical Imputation with `SimpleImputer`

For reproducible preprocessing pipelines, prefer `sklearn.impute.SimpleImputer`.

```python
from sklearn.impute import SimpleImputer

mean_imputer = SimpleImputer(strategy="mean")
median_imputer = SimpleImputer(strategy="median")
mode_imputer = SimpleImputer(strategy="most_frequent")
constant_imputer = SimpleImputer(strategy="constant", fill_value=0)

df_imputed = pd.DataFrame(
    mean_imputer.fit_transform(df),
    columns=df.columns,
    index=df.index,
)
```

- `strategy="mean"` and `strategy="median"` are for numeric columns.
- `strategy="most_frequent"` is useful for discrete columns.
- `strategy="constant"` is explicit but can inject bias if the fill value is not meaningful.

Simple imputation is easy to explain, but it can shrink variance and weaken real relationships between features.

## Drop Missing Data Carefully

```python
df.dropna()
df.dropna(axis=1)
df.dropna(subset=["petal_length"])
df.dropna(axis=1, how="all")
```

Two mental models are useful:

- `Listwise deletion`: remove any row that has a missing value in the required columns.
- `Pairwise deletion`: compute each statistic using the rows available for the specific columns involved.

Notes:

- listwise deletion is simple and predictable, but can throw away a lot of data
- pairwise deletion preserves more observations, but different calculations may use different row sets
- deletion is most defensible when missingness is approximately `MCAR`

If missingness depends on observed or hidden structure, deletion can create bias instead of removing noise.

Two practical patterns are worth separating:

- `df.dropna(subset=[...])`: remove rows only when fields that are required for a downstream task are missing
- `df.dropna(axis=1, how="all")`: remove columns that are entirely empty

This distinction matters because a column that is 100% null is usually schema clutter, while a row missing one critical timestamp or key field may be invalid for a specific analysis but still informative in other contexts.

## Interpolation

Interpolation uses neighboring values rather than global statistics.

```python
df.interpolate(method="linear", inplace=True)

ts = ts.interpolate(method="time")
ts = ts.interpolate(method="nearest")
ts = ts.interpolate(method="quadratic")
```

- `linear` is the common default for continuous numeric series.
- `time` uses the datetime index spacing.
- `nearest` copies from the closest available observation.
- `quadratic` or other higher-order methods can fit smoother curves, but also overfit small gaps.

Interpolation is most appropriate for ordered measurements, not arbitrary table columns.

## Advanced Imputation

When simple methods are too crude, model-based imputers can use other columns to predict missing values.

### KNN Imputation

```python
from fancyimpute import KNN

knn_imputer = KNN()
df_knn = pd.DataFrame(
    knn_imputer.fit_transform(df),
    columns=df.columns,
    index=df.index,
)
```

- KNN finds similar rows using non-missing features.
- It works best when nearby observations are genuinely comparable.
- Feature scaling matters, because distance-based methods are sensitive to magnitude.

### MICE / Iterative Imputation

```python
from fancyimpute import IterativeImputer

mice_imputer = IterativeImputer()
df_mice = pd.DataFrame(
    mice_imputer.fit_transform(df),
    columns=df.columns,
    index=df.index,
)
```

- MICE models each incomplete column using the others.
- It is often more robust than one-shot mean filling.
- It is slower, more complex, and still relies on assumptions about feature relationships.

For categorical data, advanced imputers usually require encoding to numeric values first.

## Compare Imputation Results

Do not choose an imputation method only because it "fills everything".

Useful checks include:

- comparing missingness percentages before and after treatment
- comparing distributions with histograms or KDE plots
- checking whether correlations changed sharply
- measuring downstream model performance across multiple imputations

In practice, the best imputation is the one that preserves the structure you care about, not the one with the fanciest algorithm.

## Key Takeaways

- Standardize sentinel values before analysis.
- Count missingness, then inspect its pattern, not just its total amount.
- Distinguish `MCAR`, `MAR`, and `MNAR` before choosing deletion or imputation.
- Use `missingno` when missingness relationships are hard to see numerically.
- Prefer interpolation for ordered series, not generic tabular gaps.
- Validate imputed data with distributions, correlations, or downstream task metrics.
