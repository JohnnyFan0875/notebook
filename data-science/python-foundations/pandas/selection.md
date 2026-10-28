# Pandas: Selection and Filtering

## Pandas: Indexing and Slicing

This page focuses on dataframe-style selection with labels, boolean filters, and `.loc[]` / `.iloc[]`. For raw array indexing where axes and broadcasting are the main concerns, see [NumPy Indexing and Slicing](../numpy/array-basics.md).

### Example Dataset

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

### Column Selection

```python
# Select a single column (returns a Series)
df["height_cm"]

# Select multiple columns (returns a DataFrame)
df[["name", "weight_kg"]]

# Selecting Columns by Data Type
df.select_dtypes(include='object')
df.select_dtypes(include='number')
```

### Row Filtering

```python
# Filter rows where weight > 23
df["weight_kg"] > 23      # boolean series
df[df["weight_kg"] > 23]  # dataframe
```

### Label-based access (`.loc[]`)

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

### Position-based access (`.iloc[]`)

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

### Multiple conditions

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

### Index filtering

```python
# Select rows by a list of index labels
df.loc[["dog1", "dog3"]]
```

## Pandas: Filtering

Filtering allows you to select subsets of your DataFrame based on conditions, string patterns, or logical rules. Pandas provides flexible methods to filter rows efficiently.

### Example Dataset

```python
import seaborn as sns
import pandas as pd

# Load the iris dataset
iris = sns.load_dataset("iris").copy()

iris.head()
```

### Conditional Filtering

```python
# Select rows where sepal_length > 5.0
iris[iris['sepal_length'] > 5.0]

# Select rows where petal_length is between 1.5 and 2.0
iris[(iris['petal_length'] >= 1.5) & (iris['petal_length'] <= 2.0)]

# SQL-like query using .query()
iris.query('sepal_width > 3.5 or petal_width < 0.2')
```

- Use boolean conditions inside brackets for flexible filtering.
- `.query()` provides a clean SQL-like syntax.

### String Filtering

```python
# Convert species to string
temp = iris.copy()
temp['species_str'] = temp['species'].astype(str)

# Species containing 'osa'
temp[temp['species_str'].str.contains('osa')]

# Species starting with 'v'
temp[temp['species_str'].str.startswith('v')]

# Species ending with 'ca'
temp[temp['species_str'].str.endswith('ca')]

# Species matching regex (contains 'se' or 'gi')
temp[temp['species_str'].str.contains('se|gi')]

# Species beginning with 'v'
temp[temp['species_str'].str.contains('^v')]
```

- `.str.contains()`, `.str.startswith()`, `.str.endswith()` are useful for string-based filtering.
- Regex patterns can be passed to `.str.contains()` for complex matching.

If the source column may contain missing values, prefer being explicit about how to handle them:

```python
temp[temp['species_str'].str.contains('osa', na=False)]
```

`na=False` turns missing entries into `False` for the match result, which is often the safest choice when you are building a boolean mask.

### Advanced Conditions

```python
import numpy as np

# Assign flower size group based on petal_length
choices = ['Small', 'Medium', 'Large']
conds = [
    iris['petal_length'] < 2,
    iris['petal_length'].between(2, 5),
    iris['petal_length'] > 5
]
iris['size_group'] = np.select(conds, choices, default='Unknown')

# Quick binary classification with np.where
iris['is_setosa'] = np.where(iris['species'] == 'setosa', True, False)
```

- `np.select()` allows multi-condition classification.
- `np.where()` is great for quick binary flags.

### Key Takeaways

- Conditional filtering is the core of data subsetting.
- Use `.query()` for readability when combining multiple conditions.
- String filtering is essential for text-based columns.
- `np.select()` and `np.where()` help classify or create indicator variables.

### Boolean Indexing with DataFrames

```python
import pandas as pd
cars = pd.DataFrame({
    'cars_per_cap': [809, 731],
    'country': ['United States', 'Australia'],
    'drives_right': [True, False]
})

sel = cars[cars['drives_right']]
print(sel)
#    cars_per_cap      country  drives_right
# US          809  United States          True
```

- Boolean arrays can directly filter rows in pandas DataFrames.
