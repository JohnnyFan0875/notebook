# Pandas: Adding and Removing Columns & Rows

This file covers how to add and remove columns or rows in a Pandas DataFrame using practical examples.

## Example Dataset

```python
import seaborn as sns
import pandas as pd

# Use the Iris dataset
iris = sns.load_dataset("iris")
iris.head()
```

## Adding Columns

### 1. Add a New Column with Assignment

```python
iris["sepal_area"] = iris["sepal_length"] * iris["sepal_width"]
```

### 2. Add Column with a Constant Value

```python
iris["dataset"] = "iris"
```

### 3. Add Column with a Function of Existing Columns

```python
iris["petal_ratio"] = iris["petal_length"] / iris["petal_width"]
```

### 4. Add Column Using `assign`

```python
iris = iris.assign(length_sum = iris["sepal_length"] + iris["petal_length"])
```

### 5. Insert Column at Specific Position

```python
iris.insert(2, "sepal_length_cm", iris["sepal_length"] * 2.54)  # Convert inches to cm if needed
```

## Removing Columns

### 1. Drop a Single Column

```python
iris.drop("dataset", axis=1)
```

### 2. Drop Multiple Columns

```python
iris.drop(["sepal_area", "petal_ratio"], axis=1)
```

### 3. Drop Columns In-Place

```python
iris.drop("length_sum", axis=1, inplace=True)
```

## Adding Rows

### 1. Append a Single Row with `concat`

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

### 2. Append Multiple Rows

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

## Removing Rows

### 1. Drop Rows by Index

```python
iris.drop(0)   # drop row with index 0
```

### 2. Drop Multiple Rows by Index

```python
iris.drop([1, 2])
```

### 3. Drop Rows with Condition

```python
iris = iris[iris["sepal_length"] > 5.0]  # keep only rows where sepal_length > 5.0
```

### 4. Drop Rows by Condition Using Index

```python
iris.drop(iris[iris["sepal_length"] > 7.5].index) # drop rows where sepal_length > 7.5
```

## Key Takeaways

- Use **assignment**, **assign()**, or **insert()** to add new columns.
- Use **drop(axis=1)** to remove columns.
- Use **concat()** to append rows (instead of `append()`).
- Use **drop()** or boolean filtering to remove rows.
- Always check whether to modify **in-place** or return a new DataFrame.
