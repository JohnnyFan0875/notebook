# Pandas: Index & MultiIndex

Indexes are fundamental to Pandas for aligning data, fast lookups, and hierarchical (multi-level) indexing. Working effectively with indexes improves efficiency and expressiveness.

## Example Dataset

```python
import seaborn as sns
import pandas as pd

# Load iris dataset
iris = sns.load_dataset("iris").copy()

iris.head()
```

## Set / Reset Index

```python
# Set column as the new index
idx_df = iris.set_index('species')
idx_df = iris.set_index(['species', 'sepal_length'])

# Reset back to default integer index
reset_df = idx_df.reset_index()

# Inspect index properties
idx_df.index.name        # Name of index
idx_df.index.is_unique   # Check if index values are unique
```

- `.set_index()` promotes a column to become the index.
- `.reset_index()` restores default integer index.

## Create Multi-Level Index

```python
# Create multi-level index using species and sepal_length
multi_idx = iris.set_index(['species', 'sepal_length'])

# Inspect MultiIndex info
multi_idx.index.names        # Names of index levels
multi_idx.index.levels       # Unique values per level
```

- Multi-level indexes allow grouping and slicing on hierarchical keys.

## Select Rows by Tuple Index

```python
# Select rows using tuple-based indexing
multi_idx.loc[[('setosa', 5.1), ('virginica', 6.3)]]

# Slice using pd.IndexSlice for multi-level selection
idx = pd.IndexSlice
multi_idx.loc[idx[:, 5.0:5.5], :]
```

- `pd.IndexSlice` helps build readable multi-level selections.

## Inspect & Manipulate Index

```python
# Sort by MultiIndex levels
multi_idx.sort_index(level=['species', 'sepal_length'], ascending=[True, False])

# Swap index levels
multi_idx_swapped = multi_idx.swaplevel()

# Reset MultiIndex back to columns
multi_idx.reset_index()
```

- Sorting, swapping, and resetting help reorganize data.

## Advanced Usage

```python
# Group by MultiIndex and compute mean
multi_idx.groupby(level='species').mean()

# Stack/Unstack to reshape data
stacked = iris.set_index(['species', 'sepal_length']).stack()
unstacked = stacked.unstack()
```

- MultiIndex integrates well with grouping and reshaping operations.

## Key Takeaways

- Use `.set_index()` and `.reset_index()` to control the DataFrame index.
- MultiIndex enables powerful hierarchical grouping and selection.
- `pd.IndexSlice` is recommended for readable multi-level filtering.
- Index manipulation (sorting, swapping, stacking) is essential for advanced reshaping and alignment.
