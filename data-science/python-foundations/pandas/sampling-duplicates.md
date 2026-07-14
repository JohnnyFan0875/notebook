# Pandas: Sampling, Duplicates, and Unique Values

Sampling, duplicate handling, and unique value extraction are essential for data cleaning, exploration, and validation. Pandas provides built-in methods for all three tasks.

## Example Dataset

```python
import seaborn as sns
import pandas as pd

# Load iris dataset
iris = sns.load_dataset("iris").copy()

iris.head()
```

## Get Unique Values

```python
# List unique species
iris['species'].unique()

# Count unique species
iris['species'].nunique()
```

- `.unique()` returns distinct values.
- `.nunique()` counts the number of unique values.

## Handle Duplicates

```python
# Drop duplicate rows (keep first occurrence)
iris.drop_duplicates()

# Drop duplicates based on specific column
iris.drop_duplicates(subset='species')

# Show all duplicates (keep=False keeps all duplicates)
iris[iris.duplicated(subset='species', keep=False)]
```

- Use `.drop_duplicates()` to remove duplicates.
- `.duplicated()` flags duplicates as True/False.

## Random Sampling

```python
# Sample 5 random rows (reproducible with random_state)
iris.sample(n=5, random_state=42)

# Sample 30% of the rows
iris.sample(frac=0.3, random_state=42)
```

- `.sample()` selects random rows by count (`n`) or fraction (`frac`).
- `random_state=` makes the sample reproducible.
- choose `n=` when you want a fixed count, and `frac=` when you want a proportion of the dataset.

### Sampling With Replacement

```python
iris.sample(n=5, replace=True, random_state=42)
```

- `replace=False` is the default and means each row can appear at most once.
- `replace=True` allows the same row to be sampled multiple times.

This is especially useful for bootstrap-style resampling.

## Group-wise Sampling

```python
# Sample 1 row per group based on species
iris.groupby('species').sample(n=1, random_state=42)

# Sample 40% of rows per group
iris.groupby('species').sample(frac=0.4, random_state=42)
```

- Grouped sampling is useful for stratified analysis.

There are two common patterns:

- proportional stratified sampling: `groupby(...).sample(frac=...)`
- equal-count stratified sampling: `groupby(...).sample(n=...)`

The first preserves group proportions more closely. The second forces balanced subgroup sizes, which can be useful for comparisons but changes the observed sample composition.

## Weighted Sampling

Pandas can also sample rows with unequal probabilities.

```python
weights = iris["species"].map({
    "setosa": 2,
    "versicolor": 1,
    "virginica": 1,
})

iris.sample(frac=0.3, weights=weights, random_state=42)
```

- `weights=` changes the relative chance each row is drawn.
- weights can be a Series or a column name.
- this is useful when you intentionally want to oversample some rows or categories.

Be careful: weighted sampling is a data collection choice, not automatically a population-correct inference method.

## Systematic Sampling Pattern

Pandas does not have a dedicated systematic sampling method, but the pattern is simple.

```python
k = 10
systematic = iris.iloc[::k]
```

This is only safe when row order does not encode a hidden pattern. If rows are sorted by time, geography, or category, shuffle first:

```python
shuffled = iris.sample(frac=1, random_state=42)
systematic = shuffled.iloc[::10]
```

## Additional Tips

```python
# Get value counts (frequency of each category)
iris['species'].value_counts()

# Normalize to get proportions
iris['species'].value_counts(normalize=True)
```

- `.value_counts()` is a quick way to see distribution of categorical values.

## Key Takeaways

- `.unique()` and `.nunique()` explore distinct values.
- `.drop_duplicates()` and `.duplicated()` clean duplicate records.
- `.sample()` helps with random subsampling.
- Grouped sampling ensures balanced sampling across categories.
- `.value_counts()` provides quick frequency distributions.
