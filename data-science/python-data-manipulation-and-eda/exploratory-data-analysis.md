# Exploratory Data Analysis (EDA)

```
to be added
df['col'].pct_change()
df['col'].diff()
```

**Exploratory Data Analysis (EDA)** is the initial step in data analysis where we examine datasets to summarize their key characteristics using statistical and visual methods. The goal is to understand the structure, detect anomalies, test assumptions, and uncover patterns or relationships that guide further analysis or modeling. EDA involves inspecting distributions, missing values, correlations, data types, and potential outliers to ensure data quality and analytic readiness.

| Category                        | Key Methods / Functions                                                                                                                                                          |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Dataset Overview**         | `.shape`, `.columns`, `.info()`, `.describe()`, `.head()`, `.tail()`, `.dtypes`, `df.nunique()`, `.index`                                                                        |
| **2. Summary Statistics**       | `.describe()`, `.mean()`, `.median()`, `.mode()`, `.std()`, `.var()`, `.min()`, `.max()`, `.quantile()`, `.sum()`, `.cumsum()`, `.cummax()`, `.cummin()`, `.cumprod()`, `.agg()` |
| **3. Missing Values**           | `.isna()`, `.isnull()`, `.sum()`, `.mean()`, `.value_counts(dropna=False)`, `missingno`                                                                                          |
| **4. Data Types & Conversion**  | `.astype()`, `pd.to_datetime()`, `.apply()`                                                                                                                                      |
| **5. Categorical Analysis**     | `.value_counts()`, `.unique()`, `pd.crosstab()`, `pd.get_dummies()`, `.value_counts(normalize=True)`                                                                             |
| **6. Numerical Analysis**       | `.hist()`, `.boxplot()`, `.plot()`, `.describe()`, `.corr()`, `sns.pairplot()`                                                                                                   |
| **7. Grouping & Aggregation**   | `.groupby()`, `.agg()`, `.pivot_table()`, `.crosstab()`                                                                                                                          |
| **8. Correlation & Covariance** | `.corr()`, `.cov()`, `sns.heatmap()`, `sns.clustermap()`                                                                                                                         |
| **9. Visualization**            | `matplotlib.pyplot`, `seaborn`, `plotly.express`, `pandas.plot()`                                                                                                                |
| **10. Outliers & Distribution** | `sns.boxplot()`, `sns.histplot()`, `sns.violinplot()`, `df.describe(percentiles=[...])`                                                                                          |
| **11. Data Validation**         | `.str.len()`, conditional filtering, type checks, value range sanity check                                                                                                       |

## Example Dataset

```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
iris = sns.load_dataset("iris")
```

## 1. Dataset Overview

```python
iris.shape               # Dimensions of the dataset
iris.columns             # Column names
iris.dtypes              # Data types per column
iris.head()              # First 5 rows
iris.tail()              # Last 5 rows
iris.info()              # Summary of data types and non-null counts
iris.describe()          # Summary stats for numeric columns
iris.nunique()           # Count of unique values per column
iris.index               # Index object of the DataFrame
```

## 2. Summary Statistics

```python
iris.mean(numeric_only=True)            # Compute the mean (average) for each numeric column
iris.median(numeric_only=True)          # Compute the median (middle value) for each numeric column
iris.mode(numeric_only=True)            # Compute the mode (most frequent value) for each numeric column
iris.std(numeric_only=True)             # Compute the standard deviation (spread from mean) for each numeric column
iris.var(numeric_only=True)             # Compute the variance (square of standard deviation) for each numeric column
iris.min(numeric_only=True)             # Find the minimum value for each numeric column
iris.max(numeric_only=True)             # Find the maximum value for each numeric column
iris.sum(numeric_only=True)             # Compute the sum of values for each numeric column
iris.quantile([0.25, 0.5, 0.75])        # Compute the 25th, 50th (median), and 75th percentiles (quartiles) for each numeric column
```

- Calculate interquartile range (IQR)

```python
q75 = iris["sepal_length"].quantile(0.75)
q25 = iris["sepal_length"].quantile(0.25)
iqr = q75 - q25
```

- Conditional mean calculation:

```python
# Mean sepal length of only virginica species
iris[iris["species"] == "virginica"]["sepal_length"].mean()
```

- Custom quantile aggregation and cumulative statistics:

```python
# Define custom aggregation functions
def pct30(column):
    return column.quantile(0.3)

def pct40(column):
    return column.quantile(0.4)

# Apply to single column
iris["sepal_length"].agg(pct30)

# Apply to multiple columns
iris[["sepal_length", "petal_length"]].agg(pct30)

# Multiple aggregations
iris["sepal_length"].agg([pct30, pct40])
```

- Cumulative statistics:

```python
# Cumulative sum of petal_length
iris["petal_length"].cumsum()

# Cumulative max
iris["petal_length"].cummax()

# Cumulative min
iris["petal_length"].cummin()

# Cumulative product
iris["petal_length"].cumprod()
```

## 3. Missing Values

```python
iris.isnull().sum()                # Count of missing values per column
iris.isnull().mean()               # Proportion of missing values per column
iris[iris.isnull().any(axis=1)]    # Rows with any missing values
```

- Visualize missing data with `missingno`:

```python
import missingno as msno

# Visualize missing values
msno.matrix(iris)
plt.show()

# Sort data and re-visualize
sorted_iris = iris.sort_values(by='sepal_length')
msno.matrix(sorted_iris)
plt.show()
```

## 4. Data Types & Conversion

```python
# Convert species to category
type(iris['species'])
iris['species'] = iris['species'].astype('category')

# Convert to datetime format (invalid entries become NaT)
iris["collected_date"] = pd.Series(["2023-01-01", "2023-01-02", "invalid", "2023-01-04", "2023-01-05"] * 30)[:150]  # Repeat pattern to match 150 rows
iris["collected_date"] = pd.to_datetime(iris["collected_date"], errors="coerce")
```

## 5. Categorical Analysis

```python
iris['species'].value_counts(sort=True)                 # Frequency of each category
iris['species'].value_counts(normalize=True)            # Proportion of each category
pd.crosstab(iris['species'], iris['sepal_width'] > 3.0) # Rows = species, Columns = whether sepal_width > 3.0; values = counts

# Crosstab with aggregation (e.g., median score per species × sepal width group)
iris["score"] = iris["sepal_length"] * 10 + iris["petal_length"]

pd.crosstab(
    iris["species"],
    iris["sepal_width"] > 3.0,
    values=iris["score"],
    aggfunc="median"
)
```

- Find inconsistent categories:

```python
# Simulate a known set of categories
known_species = ["setosa", "versicolor", "virginica"]

# Introduce a typo for demonstration
iris_with_typo = iris.copy()
iris_with_typo.loc[0, 'species'] = "setossa"

# Identify inconsistent categories
observed_species = set(iris_with_typo['species'])
inconsistent_species = observed_species.difference(known_species)

# Filter inconsistent and consistent rows
inconsistent_rows = iris_with_typo['species'].isin(inconsistent_species)
inconsistent_data = iris_with_typo[inconsistent_rows]
consistent_data = iris_with_typo[~inconsistent_rows]
```

## 6. Numerical Analysis

```python
iris.hist(figsize=(10, 6))
plt.tight_layout()

sns.boxplot(data=iris)
sns.pairplot(iris, hue='species')
```

## 7. Grouping & Aggregation

```python
# Mean petal length per species
iris.groupby('species')['petal_length'].mean()

# Summary stats per group
iris.groupby('species').agg({
    'sepal_length': ['mean', 'std'],
    'petal_length': ['mean', 'max']
})
```

## 8. Correlation & Covariance

```python
iris.corr(numeric_only=True)

# Visualize correlation
sns.heatmap(iris.corr(numeric_only=True), annot=True, cmap="coolwarm")
```

## 9. Visualization

```python
# Distribution plot
sns.histplot(data=iris, x="sepal_length", hue="species", kde=True)

# Scatter plot
sns.scatterplot(data=iris, x="sepal_length", y="petal_length", hue="species")

# Boxplot
sns.boxplot(x="species", y="sepal_length", data=iris)
```

## 10. Outliers & Distribution

```python
# Boxplot to detect outliers
sns.boxplot(data=iris, x='species', y='sepal_length')

# KDE and histogram
sns.histplot(data=iris, x='petal_width', kde=True)

# Violin plot
sns.violinplot(data=iris, x='species', y='petal_length')
```

## 11. Data Validation

- String length check and filtering (simulated example):

```python
# Simulate phone number column (e.g., for demonstration purposes)
iris["phone"] = ["0912345678", "0987654321", "0912", "0922333444", "0988123456"]

# Check length of phone number
sanity_check = iris["phone"].str.len()

# Flag suspicious entries (e.g., not length 10)
iris[sanity_check != 10]
```

- Conditional filtering for validation:

```python
# Check for species with petal_length < 1.0 (sanity check for outliers or anomalies)
iris[iris["petal_length"] < 1.0]
```
