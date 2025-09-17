# Pandas: Grouping & Aggregation

Grouping and aggregation are essential for summarizing datasets. Pandas provides `.groupby()`, `.agg()`, `.transform()`, and `.describe()` to generate grouped summaries.

## Example Dataset

```python
import seaborn as sns
import pandas as pd

# Load iris dataset
iris = sns.load_dataset("iris").copy()

iris.head()
```

## Basic Group Aggregation

```python
# Mean sepal length per species
iris.groupby('species')['sepal_length'].mean()

# Sum of petal width per species
iris.groupby('species')['petal_width'].sum()

# Many groups, many summaries
iris.groupby(['species', 'sepal_width'])['petal_length'].mean()
iris.groupby(['species', 'sepal_width'])[['petal_length', 'petal_width']].mean()
```

- Grouping by one or more columns.
- Aggregation applies statistical functions to groups.

## Multiple Aggregations

```python
# Compute mean & max of sepal_length, and sum of petal_length per species
iris.groupby('species').agg({
    'sepal_length': ['mean', 'max'],
    'petal_length': 'sum'
})

# Aggregate and rename columns using tuple syntax
iris.groupby('species').agg(
    sepal_mean=('sepal_length', 'mean'),
    petal_sum=('petal_length', 'sum')
)
```

- `.agg()` allows different functions on different columns.
- Tuple syntax provides meaningful column names.

## Group Transformation

```python
# Compute standard deviation of petal_length per species, aligned to original rows
iris['petal_std'] = iris.groupby('species')['petal_length'].transform('std')

# Compute normalized petal_length per group (subtract group mean)
iris['petal_norm'] = iris['petal_length'] - iris.groupby('species')['petal_length'].transform('mean')
```

- `.transform()` returns group-calculated values aligned with the original DataFrame.

## Descriptive Stats Per Group

```python
# Quick descriptive stats per group
iris.groupby('species')['sepal_width'].describe()

# Count rows per group
iris.groupby('species').size()
```

- `.describe()` generates multiple statistics at once.
- `.size()` counts rows per group.

## Advanced Usage

```python
# Group by species and resample on a fake date column
iris['date'] = pd.date_range('2024-01-01', periods=len(iris), freq='D')
iris.groupby('species').resample('M', on='date')['sepal_length'].mean()
```

- Grouping can be combined with resampling for time-series style data.

## Key Takeaways

- `.groupby()` is the core tool for grouping and summarizing data.
- `.agg()` supports multiple functions per group.
- `.transform()` creates group-derived columns aligned with the DataFrame.
- `.describe()` and `.size()` quickly summarize group stats.
- Grouping can be combined with resampling or multi-level grouping for advanced analysis.
