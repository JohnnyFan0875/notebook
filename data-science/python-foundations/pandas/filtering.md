# Pandas: Row Selection & Filtering

Filtering allows you to select subsets of your DataFrame based on conditions, string patterns, or logical rules. Pandas provides flexible methods to filter rows efficiently.

## Example Dataset

```python
import seaborn as sns
import pandas as pd

# Load the iris dataset
iris = sns.load_dataset("iris").copy()

iris.head()
```

## Conditional Filtering

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

## String Filtering

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

## Advanced Conditions

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

## Key Takeaways

- Conditional filtering is the core of data subsetting.
- Use `.query()` for readability when combining multiple conditions.
- String filtering is essential for text-based columns.
- `np.select()` and `np.where()` help classify or create indicator variables.
