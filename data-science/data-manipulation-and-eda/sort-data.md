# Sorting Data

Sorting is a key operation in data manipulation. It helps organize data for readability, prioritization, and further analysis.

## Common Sorting Techniques

| Task                                              | Method / Example                             | Description                                                     |
| ------------------------------------------------- | -------------------------------------------- | --------------------------------------------------------------- |
| [Sort by column value](#sorting-by-column-values) | `df.sort_values("col")`                      | Sort rows by one/multiple column(s) (ascending by default)      |
| [Sort by index](#sorting-by-index)                | `df.sort_index()`                            | Sort rows by index labels                                       |
| [In-place sort](#in-place-sorting)                | `df.sort_values("col", inplace=True)`        | Modify original DataFrame directly                              |
| [Sort a Series](#sorting-a-series)                | `series.sort_values()`,`series.sort_index()` | Sort a Series from smallest to largest or based on index labels |

---

## Example Dataset

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Bella", "Charlie", "Lucy"],
    "age": [5, 3, 7],
    "weight_kg": [24, 22, 28]
})
```

## Sorting by Column Values

### 1. Single Column Sort

```python
df.sort_values("age")                    # Ascending
df.sort_values("age", ascending=False)   # Descending
```

### 2. Multi-Column Sort

```python
df.sort_values(["age", "weight_kg"])
df.sort_values(["age", "weight_kg"], ascending=[True,False])
```

## Sorting by Index

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

## Sorting a Series

```python
s = pd.Series([3, 1, 4], index=["c", "a", "b"])
s.sort_values()     # Sort by values
s.sort_index()      # Sort by index
```

## In-Place Sorting

- `inplace=True` means changing the object directly, don’t return a copy

```python
df_sort = df.sort_values("age", inplace=True) # sorted by age
df.sort_values("age", inplace=True) # df is modified in-place, and nothing is returned (Return None)
```

> Be careful: `inplace=True` changes the original object and cannot be undone unless you saved a copy beforehand.
