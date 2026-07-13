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

### `groupby()` as a Spreadsheet Pivot-Table Mental Model

如果你有試算表背景，可以先把這個模式想成「先決定列分組，再決定要彙總哪個值欄」。

```python
totals = sales.groupby("store")["revenue"].sum()
print(totals)
```

這很像最基本的 pivot table：

- rows: `store`
- values: `revenue`
- summary: `sum`

當你只是想做「按類別加總、平均、計數」，`groupby(...).sum()` / `.mean()` / `.size()` 往往就是最直接的起手式。

如果之後還想把結果拿去畫圖，通常會先 `reset_index()` 變回普通 DataFrame：

```python
totals = (
    sales.groupby("store")["revenue"]
    .sum()
    .reset_index()
)
```

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

## Custom quantile aggregation and cumulative statistics

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

## Group Transformation

```python
# Compute standard deviation of petal_length per species, aligned to original rows
iris['petal_std'] = iris.groupby('species')['petal_length'].transform('std')

# Compute normalized petal_length per group (subtract group mean)
iris['petal_norm'] = iris['petal_length'] - iris.groupby('species')['petal_length'].transform('mean')
```

- `.transform()` returns group-calculated values aligned with the original DataFrame.

## Boolean Means as Rates

One very practical pandas pattern is to store an event as `True` / `False` and then take the mean.

```python
df["is_arrested"].mean()
df.groupby("district")["is_arrested"].mean()
df.groupby(["district", "driver_gender"])["is_arrested"].mean()
```

This works because pandas treats booleans numerically in many contexts:

- `True` behaves like `1`
- `False` behaves like `0`

So the mean of a boolean Series is the event rate.

That makes boolean columns especially convenient for questions like:

- arrest rate
- conversion rate
- search rate
- defect rate
- retention flag by cohort

Key point: if the business question is really "what proportion of rows satisfy this condition?", a boolean column plus `.mean()` is often the cleanest expression.

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
