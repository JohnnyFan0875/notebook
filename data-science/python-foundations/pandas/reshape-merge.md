# Pandas: Reshaping & Merging

Reshaping and merging are essential for reorganizing data, joining datasets, and preparing for analysis. Pandas provides flexible tools like pivot, melt, stack/unstack, concat, and merge.

## Example Dataset

```python
import seaborn as sns
import pandas as pd

# Load iris dataset
iris = sns.load_dataset("iris").copy()

iris.head()
```

## Pivot Table

```python
# Create a pivot table: mean petal_length by species and sepal_width
iris.pivot_table(
    index='species',
    values='petal_length',
    columns='sepal_width',
    aggfunc='mean',
    fill_value=0
)

# Pivot table with multiple aggregation functions
iris.pivot_table(
    index='species',
    values=['sepal_length', 'petal_width'],
    aggfunc={'sepal_length': 'mean', 'petal_width': 'sum'},
    fill_value=0
)
```

- `.pivot_table()` is flexible for summarization and reshaping.

## Melt (Unpivot)

```python
# Convert wide to long format
iris.melt(
    id_vars=['species'],
    var_name='measurement',
    value_name='value'
)

# Melt only numeric columns
iris.melt(
    id_vars='species',
    value_vars=['sepal_length','sepal_width','petal_length','petal_width'],
    var_name='measurement',
    value_name='value'
)
```

- `.melt()` is useful for converting wide to long format.

## Concatenation

```python
# Vertical concatenation (stack rows)
pd.concat([iris, iris], ignore_index=True)

# Horizontal concatenation (align by index)
pd.concat([iris, iris[['petal_width']]], axis=1)

# Concatenate Series objects
series1 = pd.Series(['a','b','c','d'], index=['1','2','3','4'])
series2 = pd.Series(['e','f','g','h'], index=['5','6','7','8'])
pd.concat([series1, series2], ignore_index=True)
```

- `pd.concat()` stacks or aligns DataFrames/Series vertically or horizontally.

## Merging DataFrames

```python
# Basic merge on species
iris.merge(iris, on='species', suffixes=['_L','_R'])

# Ordered merge (useful for time series)
pd.merge_ordered(iris, iris, on='species')

# As-of merge (nearest key join, useful for time series)
iris_sorted = iris.sort_values('sepal_length')
pd.merge_asof(
    iris_sorted, iris_sorted,
    on='sepal_length',
    suffixes=['_L','_R']
)
```

- `merge`, `merge_ordered`, and `merge_asof` provide SQL-like joins.

## Key Takeaways

- `.pivot_table()` is powerful for summarization and reshaping.
- `.melt()` transforms wide to long format.
- `.stack()` and `.unstack()` convert between hierarchical and flat tables.
- `pd.concat()` appends or aligns DataFrames.
- `merge` operations join datasets on keys, similar to SQL joins.
