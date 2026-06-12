# Pandas: Indexing and Slicing

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

# Access subsets of rows based on multiindex
df = df.set_index(['name', 'height_cm'], drop=False)
df.loc[[('Bella', 56), ('Charlie', 43)]]
df.loc['Bella':'Charlie'] # Charlie is included

# Select rows 0,1,2 and columns 'name','height_cm' (row index labels 0,1,2)
df_select = df.loc[[0,1,2],['name','height_cm']]

# Select all rows and columns 'name','height_cm'
df_select = df.loc[:,['name','height_cm']]
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

# Select rows 0,1,2 and columns 0,1 by integer position
df_select = df.iloc[[0,1,2],[0,1]]

# Select all rows and columns 0,1
df_select = df.iloc[:,[0,1]]

# Select a single column as DataFrame
df_select = df.iloc[:,[2]]  # DataFrame

# Select a single column as Series
df_select = df.iloc[:,2]    # Series
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
