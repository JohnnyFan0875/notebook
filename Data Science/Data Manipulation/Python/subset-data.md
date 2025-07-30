# Subsetting Data

Subsetting is the process of selecting specific **rows**, **columns**, or **cells** from a DataFrame or Series. It is one of the most fundamental tasks in data manipulation, often used for filtering data, extracting features, or preparing subsets for analysis.

## Why Subset?

- Focus on a region or category of interest
- Perform operations on a filtered dataset
- Clean or validate specific parts of the data

## Common Subsetting Techniques

| Type                                                 | Method                     | Example                                                 | Description                      |
| ---------------------------------------------------- | -------------------------- | ------------------------------------------------------- | -------------------------------- |
| [Column selection](#column-selection)                | `df["col"]`, `df[["col"]]` | `df["age"]`                                             | Select one or more columns       |
| [Row filtering](#row-filtering)                      | Boolean indexing           | `df[df["age"] > 30]`                                    | Filter rows based on a condition |
| [Label-based access](#label-based-access-loc)        | `df.loc[row, col]`         | `df.loc["dog1", "weight_kg"]`                           | Subset by row/column labels      |
| [Position-based access](#position-based-access-iloc) | `df.iloc[row, col]`        | `df.iloc[0, 1]`                                         | Subset by integer position       |
| [Multiple conditions](#multiple-conditions)          | `&`, `isin()`              | `df[(df["color"] == "Black") & (df["weight_kg"] > 20)]` | Filter with compound logic       |
| [Index filtering](#index-filtering)                  | `.loc[index_list]`         | `df.loc[["dog1", "dog3"]]`                              | Select multiple rows by index    |

## Example Dataset

```python
import pandas as pd

df = pd.DataFrame(
    {
        "name": ["Bella", "Charlie", "Lucy"],
        "height_cm": [56, 43, 46],
        "weight_kg": [24, 24, 24]
    },
    index=["dog1", "dog2", "dog3"]  # setting custom row labels
)
```

## Column Selection

```python
# Select a single column (returns a Series)
df["height_cm"]

# Select multiple columns (returns a DataFrame)
df[["name", "weight_kg"]]

# Selecting Columns by Data Type
df.select_dtypes(include='object')
df.select_dtypes(include='number')
```

## Row Filtering

```python
# Filter rows where weight > 23
df["weight_kg"] > 23      # boolean series
df[df["weight_kg"] > 23]  # dataframe
```

## Label-based access (`.loc[]`)

```python
# Access a specific cell by row and column labels
df.loc["dog1", "weight_kg"]

# Access an entire row
df.loc["dog1"]

# Access a subset of rows and columns
df.loc[["dog1", "dog3"], ["name", "height_cm"]]
```

## Position-based access (`.iloc[]`)

```python
# Access the cell at first row, second column
df.iloc[0, 1]

# Access the first two rows
df.iloc[0:2]
df.iloc[:2]
df.head(2)

# Access the last two rows
df.tail(2)

# Access a subset of rows and columns
df.iloc[[0, 2], [0, 2]]
```

## Multiple conditions

```python
# Height greater than 45 AND weight equal to 24
df[(df["height_cm"] > 45) & (df["weight_kg"] == 24)]

# # Height greater than 45 OR weight equal to 24
df[(df["height_cm"] > 45) | (df["weight_kg"] == 24)]

# Name is either Bella or Lucy
df[df["name"].isin(["Bella", "Lucy"])]

# Name is neithor Bella nor Lucy
df[~df["name"].isin(["Bella", "Lucy"])]
```

## Index filtering

```python
# Select rows by a list of index labels
df.loc[["dog1", "dog3"]]
```
