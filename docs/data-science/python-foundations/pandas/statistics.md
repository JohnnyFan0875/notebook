# Pandas: Statistics & Correlation

Pandas provides a rich set of statistical functions for analyzing numerical and categorical data. These include dataset overview, summary statistics, rolling/expanding calculations, differences, correlations, and covariance.

## Example Dataset

```python
import seaborn as sns
import pandas as pd

# Load iris dataset
iris = sns.load_dataset("iris").copy()
iris.head()
```

## Dataset Overview

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

```python
iris['species'].value_counts(sort=True)       # Frequency of each category
iris['species'].value_counts(normalize=True)  # Proportion of each category
```

For mixed-type datasets, `describe()` can be made more explicit:

```python
iris.describe(include='all')              # Include numeric and object/categorical columns
iris.describe(include=['float', 'object'])
iris.describe(percentiles=[0.1, 0.5, 0.9])
```

- `include='all'` is useful when you want one quick pass over the whole table.
- Custom percentiles are especially helpful for skewed or time-series-like data.

## Basic Statistical Functions

```python
iris.describe()                  # Summary statistics (count, mean, std, min, quartiles, max)
iris.mean(numeric_only=True)     # Mean
iris.median(numeric_only=True)   # Median
iris.std(numeric_only=True)      # Standard deviation
iris.var(numeric_only=True)      # Variance
iris.min(numeric_only=True)      # Minimum
iris.max(numeric_only=True)      # Maximum
iris.quantile([0.25, 0.5, 0.75]) # Quartiles
iris.sum(numeric_only=True)      # Sum

# Top-k values in a Series
iris['sepal_length'].nlargest(2)   # Get 2 largest values
iris['sepal_length'].nsmallest(2)  # Get 2 smallest values
```

## Difference & Percentage Change

```python
# Difference between consecutive values
iris['sepal_length_diff'] = iris['sepal_length'].diff()

# Percentage change between consecutive values
iris['sepal_length_pct'] = iris['sepal_length'].pct_change()

iris[['sepal_length', 'sepal_length_diff', 'sepal_length_pct']].head()
```

## Cumulative Statistics

```python
iris['petal_length_cumsum'] = iris['petal_length'].cumsum()
iris['petal_length_cummax'] = iris['petal_length'].cummax()
iris['petal_length_cummin'] = iris['petal_length'].cummin()
iris['petal_length_cumprod'] = iris['petal_length'].cumprod()
```

## Correlation & Covariance

```python
# Correlation matrix
iris.corr(numeric_only=True)

# Covariance matrix
iris.cov(numeric_only=True)
```

### Visualization

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Heatmap of correlation
sns.heatmap(iris.corr(numeric_only=True), annot=True, cmap="coolwarm")
plt.show()
```

## Rolling & Expanding Windows

```python
# Rolling mean with window size 3
iris['rolling_mean'] = iris['sepal_length'].rolling(window=3).mean()

# Expanding mean (cumulative average)
iris['expanding_mean'] = iris['sepal_length'].expanding().mean()
```

## Key Takeaways

- Use `.describe()` and dataset overview methods for quick inspection.
- Use `describe(include=...)` when the dataset mixes numeric and categorical columns.
- `.nlargest()` and `.nsmallest()` are useful for quickly finding extremes.
- `.diff()` and `.pct_change()` are useful for time-series or sequential comparisons.
- `.corr()` and `.cov()` reveal relationships between variables.
- Cumulative and rolling functions support sequential trend analysis.
