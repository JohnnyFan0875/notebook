# Pandas: Handling Missing Data

Missing values are common in real-world datasets. Pandas provides flexible tools to detect, fill, or drop missing data, ensuring clean and reliable analysis.

## Example Dataset

```python
import seaborn as sns
import pandas as pd
import numpy as np

# Load iris dataset and add artificial missing values
iris = sns.load_dataset("iris").copy()
iris.loc[0, 'sepal_length'] = np.nan
iris.loc[5, 'sepal_width'] = np.nan
iris.loc[10, 'petal_length'] = np.nan

iris.head(12)
```

## Detect Missing Data

```python
# Detect NaN values
iris.isna().head()

# Count missing values per column
iris.isna().sum()

# Check if any value is missing
iris.isna().any()

# Rows with any missing values
iris[iris.isnull().any(axis=1)]
```

- `.isna()` (or `.isnull()`) marks missing values as True.
- `.sum()` helps count missing values per column.

## Fill Missing Values

```python
# Fill all NaN with 0
iris.fillna(0)

# Fill NaN in a single column with the column mean
iris['sepal_length'].fillna(iris['sepal_length'].mean(), inplace=True)

# Fill using dictionary for multiple columns
iris.fillna({
    'sepal_length': iris['sepal_length'].mean(),
    'sepal_width': iris['sepal_width'].median()
})

# Forward fill (propagate last valid value)
iris.fillna(method='ffill')

# Backward fill (use next valid value)
iris.fillna(method='bfill')
```

- Choose mean/median/mode based on data type and distribution.
- Forward/backward fill works well for time-series.

## Drop Missing Data

```python
# Drop rows with any NaN
iris.dropna()

# Drop columns with any NaN
iris.dropna(axis=1)

# Drop rows with NaN only in specific columns
iris.dropna(subset=['petal_length'])
```

- Dropping rows/columns is simplest but may reduce dataset size.

## Interpolation

```python
# Linear interpolation
iris.interpolate(method='linear', inplace=True)

# Time interpolation (for time-indexed data)
iris['sepal_length'] = iris['sepal_length'].interpolate(method='time')
```

- Interpolation estimates missing values from surrounding data.

## Key Takeaways

- Use `.isna()` to detect missing data.
- Fill with statistics (mean/median/mode), forward/backward fill, or interpolation.
- Drop rows/columns only when missingness is not informative.
- Interpolation is powerful for continuous or time-based data.
