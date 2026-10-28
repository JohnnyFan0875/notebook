# Pandas: Updating, Adding and Removing

## Pandas: Updating Data

Updating data is a common operation when cleaning or transforming datasets. Pandas provides flexible methods for updating cells, replacing values, applying functions, and conditional updates.

### Example Dataset

```python
import seaborn as sns
import pandas as pd

# Load iris dataset
iris = sns.load_dataset("iris").copy()

iris.head()
```

### Update by Label/Position

```python
# Update a specific cell using condition
iris.loc[iris['species'] == "setosa", "sepal_length"] = 6.0

# Update cell by row/column index
iris.iloc[0, 1] = 3.5   # First row, second column (sepal_width)

# Fast scalar update by integer position
iris.iat[1, 2] = 1.5    # Row 2, third column (petal_length)

# Fast scalar update by label
iris.at[0, 'petal_width'] = 0.4
```

- `.loc[]` / `.iloc[]` for row/col selection.
- `.at[]` / `.iat[]` for fast scalar updates.

### Replace Values

```python
# Replace exact match
iris['species'] = iris['species'].replace("setosa", "SET")

# Replace substring in strings
iris['species'] = iris['species'].astype(str).str.replace("versicolor", "VERSI", regex=False)

# Replace using a dictionary
replace_dict = {"virginica": "VIR", "setosa": "SET"}
iris['species'] = iris['species'].replace(replace_dict)
```

- `.replace()` works with scalars, lists, and dict mappings.
- `.str.replace()` applies string replacements.

### Apply Functions

```python
# Column-wise transformation
iris['sepal_length_plus1'] = iris['sepal_length'].apply(lambda x: x + 1)

# Use a predefined function
def ratio(sl, sw):
    return sl / sw if sw != 0 else None

iris['sl_sw_ratio'] = iris.apply(lambda row: ratio(row['sepal_length'], row['sepal_width']), axis=1)

# Applymap for element-wise transformations across numeric data
numeric_df = iris.select_dtypes(include='number')
iris_doubled = numeric_df.applymap(lambda x: x * 2)

# Transform one Series using map
iris['length_label'] = iris['sepal_length'].map(lambda x: 'short' if x < 5.5 else 'long')
```

- `.apply()` works column- or row-wise.
- `.applymap()` applies element-wise to an entire DataFrame.
- `.map()` transforms a Series.

### Conditional Update

```python
# Increase petal_length by 0.5 if petal_width < 1.0
iris.loc[iris['petal_width'] < 1.0, 'petal_length'] += 0.5

# Fill NaN in sepal_length with 0 only for versicolor species
iris.loc[(iris['species'] == 'versicolor') & (iris['sepal_length'].isna()), 'sepal_length'] = 0
```

- Combine boolean conditions with `.loc[]` for conditional updates.
- Allows highly flexible data cleaning.

### Key Takeaways

- Use `.loc[]` / `.iloc[]` for updating by condition or position.
- `.replace()` and `.str.replace()` are versatile for substitution.
- `.apply()`, `.map()`, and `.applymap()` allow transformations.
- Conditional updates with `.loc[]` enable precise control over modifica

## Pandas: Adding and Removing Columns & Rows

This file covers how to add and remove columns or rows in a Pandas DataFrame using practical examples.

### Example Dataset

```python
import seaborn as sns
import pandas as pd

# Use the Iris dataset
iris = sns.load_dataset("iris")
iris.head()
```

### Adding Columns

#### 1. Add a New Column with Assignment

```python
iris["sepal_area"] = iris["sepal_length"] * iris["sepal_width"]
```

#### 2. Add Column with a Constant Value

```python
iris["dataset"] = "iris"
```

#### 3. Add Column with a Function of Existing Columns

```python
iris["petal_ratio"] = iris["petal_length"] / iris["petal_width"]
```

#### 4. Add Column Using `assign`

```python
iris = iris.assign(length_sum = iris["sepal_length"] + iris["petal_length"])
```

#### 5. Insert Column at Specific Position

```python
iris.insert(2, "sepal_length_cm", iris["sepal_length"] * 2.54)  # Convert inches to cm if needed
```

### Removing Columns

#### 1. Drop a Single Column

```python
iris.drop("dataset", axis=1)
```

#### 2. Drop Multiple Columns

```python
iris.drop(["sepal_area", "petal_ratio"], axis=1)
```

#### 3. Drop Columns In-Place

```python
iris.drop("length_sum", axis=1, inplace=True)
```

### Adding Rows

#### 1. Append a Single Row with `concat`

```python
new_row = pd.DataFrame({
    "sepal_length": [5.0],
    "sepal_width": [3.5],
    "petal_length": [1.3],
    "petal_width": [0.2],
    "species": ["setosa"]
})
iris = pd.concat([iris, new_row], ignore_index=True)
```

#### 2. Append Multiple Rows

```python
new_rows = pd.DataFrame({
    "sepal_length": [6.5, 7.1],
    "sepal_width": [3.0, 2.9],
    "petal_length": [5.2, 5.9],
    "petal_width": [2.0, 2.3],
    "species": ["virginica", "versicolor"]
})
iris = pd.concat([iris, new_rows], ignore_index=True)
```

> Note: `DataFrame.append()` is deprecated in Pandas ≥ 2.0; use `pd.concat()` instead.

### Removing Rows

#### 1. Drop Rows by Index

```python
iris.drop(0)   # drop row with index 0
```

#### 2. Drop Multiple Rows by Index

```python
iris.drop([1, 2])
```

#### 3. Drop Rows with Condition

```python
iris = iris[iris["sepal_length"] > 5.0]  # keep only rows where sepal_length > 5.0
```

#### 4. Drop Rows by Condition Using Index

```python
iris.drop(iris[iris["sepal_length"] > 7.5].index) # drop rows where sepal_length > 7.5
```

### Key Takeaways

- Use **assignment**, **assign()**, or **insert()** to add new columns.
- Use **drop(axis=1)** to remove columns.
- Use **concat()** to append rows (instead of `append()`).
- Use **drop()** or boolean filtering to remove rows.
- Always check whether to modify **in-place** or return a new DataFrame.
