# Pandas: Updating Data

Updating data is a common operation when cleaning or transforming datasets. Pandas provides flexible methods for updating cells, replacing values, applying functions, and conditional updates.

## Example Dataset

```python
import seaborn as sns
import pandas as pd

# Load iris dataset
iris = sns.load_dataset("iris").copy()

iris.head()
```

## Update by Label/Position

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

## Replace Values

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

## Apply Functions

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

## Conditional Update

```python
# Increase petal_length by 0.5 if petal_width < 1.0
iris.loc[iris['petal_width'] < 1.0, 'petal_length'] += 0.5

# Fill NaN in sepal_length with 0 only for versicolor species
iris.loc[(iris['species'] == 'versicolor') & (iris['sepal_length'].isna()), 'sepal_length'] = 0
```

- Combine boolean conditions with `.loc[]` for conditional updates.
- Allows highly flexible data cleaning.

## Key Takeaways

- Use `.loc[]` / `.iloc[]` for updating by condition or position.
- `.replace()` and `.str.replace()` are versatile for substitution.
- `.apply()`, `.map()`, and `.applymap()` allow transformations.
- Conditional updates with `.loc[]` enable precise control over modifica
