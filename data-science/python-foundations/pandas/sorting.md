# Pandas: Sorting

Sorting 看起來簡單，但在資料清理與輸出報表時非常重要。特別是多欄位排序與 MultiIndex 排序，常直接影響你後續閱讀、比對與 join 的正確性。

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

多欄位排序時，第二個欄位只會在第一個欄位相同的情況下作為 tie-breaker。

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

## Practical Advice

- 在分析流程中，通常優先用回傳新物件的寫法，比 `inplace=True` 更清楚也更安全。
- 若你只是想看排序結果，可以直接 `df.sort_values(...).head()`，不用先改原資料。
