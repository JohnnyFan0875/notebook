# Pandas: Creating Data

Creating DataFrames and Series is often the first step of any analysis. Pandas provides multiple methods to create data from scratch or load it from files and databases.

## Example Dataset

```python
import seaborn as sns
import pandas as pd

# Load iris dataset as example
iris = sns.load_dataset("iris").copy()

iris.head()
```

## Creating and Combining Series

- Creating a Series with a custom index

```python
s = pd.Series(['a', 'b', 'c', 'd'], index=['1', '2', '3', '4'])
```

- Creating from NumPy

```python
import numpy as np

s = pd.Series(np.array([10, 20, 30]), index=['A', 'B', 'C'])
```

## Creating DataFrames

### From Dictionary

```python
df_dict = pd.DataFrame({
    "species": ["setosa", "versicolor", "virginica"],
    "avg_length": [5.0, 5.9, 6.5]
})
```

### From List

```python
df_list = pd.DataFrame([
    ["setosa", 5.0],
    ["versicolor", 5.9]
], columns=["species", "avg_length"])
```

## Setting Index and Column Names

```python
df = pd.DataFrame([[5.1, 3.5], [4.9, 3.0], [4.7, 3.2]])
df.index = ["row1", "row2", "row3"]
df.columns = ["sepal_length", "sepal_width"]
```

## Key Takeaways

- DataFrames can be created from dictionaries, lists, or arrays.
- Use `read_csv`, `read_excel`, `read_html`, `read_pickle`, `read_hdf`, and `read_sql` for file/database input.
- For large CSVs, chunked reading is efficient.
- Index and column names ca
