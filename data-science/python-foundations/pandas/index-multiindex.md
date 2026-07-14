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

## Stack / Unstack Mental Model

- `stack()`：把 column level 壓回 row index。
- `unstack()`：把 row index 的某一層翻成 columns。

```python
stacked = iris.set_index(['species', 'sepal_length']).stack()
unstacked = stacked.unstack()
```

如果資料有多層 index / columns，可以指定 level：

```python
cars.unstack(level=[0, 1])
cars.unstack(level=['brand', 'model'])
cars_unstacked.stack(level=['year', 'brand'])
```

### Missing Values After Unstack

`unstack()` 很常產生缺值，因為不是每個 index 組合都一定存在。

```python
animals.unstack(level='class')
animals.unstack(level='class', fill_value='No')
```

- 先接受 reshape 後會出現 `NaN` 是正常現象。
- 如果業務語意允許，再用 `fill_value=` 或後續 `fillna()` 補值。

### `stack(dropna=...)`

```python
flowers.stack(dropna=True)
flowers.stack(dropna=False)
flowers.stack(dropna=False).fillna(0)
```

- `dropna=True` 會省略空值組合。
- `dropna=False` 會把空值組合也保留。

這會直接影響後續 groupby、計數與對齊結果，所以在 reshape 後最好確認一下資料列數是否符合預期。

### Rearranging Levels

```python
cars.swaplevel(0, 2)
cars.swaplevel(0, 2).unstack()
cars.unstack().swaplevel(0, 1, axis=1)
```

當 MultiIndex 的層級順序不利於分析或展示時，`swaplevel()` 常常比重建 index 更簡潔。

## Key Takeaways

- Use `.set_index()` and `.reset_index()` to control the DataFrame index.
- MultiIndex enables powerful hierarchical grouping and selection.
- `pd.IndexSlice` is recommended for readable multi-level filtering.
- Index manipulation (sorting, swapping, stacking) is essential for advanced reshaping and alignment.
