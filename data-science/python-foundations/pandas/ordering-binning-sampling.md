# Pandas: Sorting, Binning, Sampling and Duplicates

## Pandas: Sorting

Sorting 看起來簡單，但在資料清理與輸出報表時非常重要。特別是多欄位排序與 MultiIndex 排序，常直接影響你後續閱讀、比對與 join 的正確性。

### Example Dataset

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Bella", "Charlie", "Lucy"],
    "age": [5, 3, 7],
    "weight_kg": [24, 22, 28]
})
```

### Sorting by Column Values

#### 1. Single Column Sort

```python
df.sort_values("age")                    # Ascending
df.sort_values("age", ascending=False)   # Descending
```

#### 2. Multi-Column Sort

```python
df.sort_values(["age", "weight_kg"])
df.sort_values(["age", "weight_kg"], ascending=[True,False])
```

多欄位排序時，第二個欄位只會在第一個欄位相同的情況下作為 tie-breaker。

### Sorting by Index

```python
df.sort_index()                 # Ascending
df.sort_index(ascending=False)  # Descending
```

- MultiIndex Sorting

```python
import pandas as pd

df = pd.DataFrame({
    "col1": ["B", "A", "A", "B"],
    "col2": [1, 2, 1, 2],
    "value": [10, 20, 30, 40]
})

df = df.set_index(["col1", "col2"])
df_sorted = df.sort_index(level=["col1", "col2"], ascending=[True, False])
print(df_sorted)
```

```text
              value
col1   col2
A      2      20
       1      30
B      2      40
       1      10
```

### Sorting a Series

```python
s = pd.Series([3, 1, 4], index=["c", "a", "b"])
s.sort_values()     # Sort by values
s.sort_index()      # Sort by index
```

### In-Place Sorting

- `inplace=True` means changing the object directly, don’t return a copy

```python
df_sort = df.sort_values("age", inplace=True) # sorted by age
df.sort_values("age", inplace=True) # df is modified in-place, and nothing is returned (Return None)
```

> Be careful: `inplace=True` changes the original object and cannot be undone unless you saved a copy beforehand.

### Practical Advice

- 在分析流程中，通常優先用回傳新物件的寫法，比 `inplace=True` 更清楚也更安全。
- 若你只是想看排序結果，可以直接 `df.sort_values(...).head()`，不用先改原資料。

## Pandas: Binning & Categorization

Binning is the process of converting continuous variables into categorical ones by grouping values into bins. This is useful for summarizing data, building histograms, or preparing features for machine learning models.

### Example Dataset

```python
import seaborn as sns
import pandas as pd

# Use the Iris dataset
iris = sns.load_dataset("iris")
iris.head()
```

### Fixed-Width Bins with `pd.cut`

```python
# Bin sepal length into categories
iris['sepal_length_cat'] = pd.cut(
    iris['sepal_length'],
    bins=[4, 5, 6, 7, 8],
    labels=['4–5', '5–6', '6–7', '7–8']
)

iris[['sepal_length', 'sepal_length_cat']].head()
```

- `bins`: define the edges of intervals.
- `labels`: assign human-readable category names.
- Result is a categorical Series.

### Quantile-Based Bins with `pd.qcut`

```python
# Divide petal length into 3 quantile-based bins
iris['petal_length_group'] = pd.qcut(
    iris['petal_length'],
    q=3,
    labels=['Short', 'Medium', 'Long']
)

iris['petal_length_group'].value_counts()
```

- `q`: number of quantiles (e.g., 3 → tertiles).
- Ensures roughly equal number of samples per bin.
- Useful for splitting skewed distributions.

### When to Use `cut` vs `qcut`

| Method | Best for | Main tradeoff |
| --- | --- | --- |
| `pd.cut()` | bins with business meaning, such as age groups or lab thresholds | groups may have very uneven counts |
| `pd.qcut()` | equal-frequency grouping for exploration or modeling | cut points may be less intuitive |

### Inspect Categories

```python
# List categories and counts
iris['sepal_length_cat'].cat.categories
iris['sepal_length_cat'].value_counts()
```

### Key Takeaways

- **`pd.cut()`**: fixed-width binning for continuous variables.
- **`pd.qcut()`**: quantile-based binning (equal-sized groups).
- Binning converts continuous values into categories, making patterns easier to interpret.
- Useful in **EDA** and **feature engineering**.

### Common Pitfalls

- 用太多 bins，結果每箱樣本太少。
- 把分箱後的類別誤當成有真實線性距離的數值。
- 在建模前先做分箱，卻沒有確認是否真的比保留原始連續資訊更好。

## Pandas: Sampling, Duplicates, and Unique Values

Sampling, duplicate handling, and unique value extraction are essential for data cleaning, exploration, and validation. Pandas provides built-in methods for all three tasks.

### Example Dataset

```python
import seaborn as sns
import pandas as pd

# Load iris dataset
iris = sns.load_dataset("iris").copy()

iris.head()
```

### Get Unique Values

```python
# List unique species
iris['species'].unique()

# Count unique species
iris['species'].nunique()
```

- `.unique()` returns distinct values.
- `.nunique()` counts the number of unique values.

### Handle Duplicates

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

### Random Sampling

```python
# Sample 5 random rows (reproducible with random_state)
iris.sample(n=5, random_state=42)

# Sample 30% of the rows
iris.sample(frac=0.3, random_state=42)
```

- `.sample()` selects random rows by count (`n`) or fraction (`frac`).
- `random_state=` makes the sample reproducible.
- choose `n=` when you want a fixed count, and `frac=` when you want a proportion of the dataset.

#### Sampling With Replacement

```python
iris.sample(n=5, replace=True, random_state=42)
```

- `replace=False` is the default and means each row can appear at most once.
- `replace=True` allows the same row to be sampled multiple times.

This is especially useful for bootstrap-style resampling.

### Group-wise Sampling

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

### Weighted Sampling

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

### Systematic Sampling Pattern

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

### Additional Tips

```python
# Get value counts (frequency of each category)
iris['species'].value_counts()

# Normalize to get proportions
iris['species'].value_counts(normalize=True)
```

- `.value_counts()` is a quick way to see distribution of categorical values.

### Key Takeaways

- `.unique()` and `.nunique()` explore distinct values.
- `.drop_duplicates()` and `.duplicated()` clean duplicate records.
- `.sample()` helps with random subsampling.
- Grouped sampling ensures balanced sampling across categories.
- `.value_counts()` provides quick frequency distributions.
