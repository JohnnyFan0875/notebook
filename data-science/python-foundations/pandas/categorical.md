# Pandas: Categorical Data & Encoding

Categorical data is data that can take on a limited, fixed number of possible values (categories). Pandas provides the `category` dtype to efficiently work with categorical variables.

## Example Dataset

```python
import seaborn as sns
import pandas as pd

# Use the Iris dataset
iris = sns.load_dataset("iris")
iris.head()
```

## Convert to Categorical Type

```python
# Convert species column to categorical dtype
iris['species_cat'] = iris['species'].astype('category')

# Inspect categories
iris['species_cat'].cat.categories
```

- Reduces memory usage.
- Provides category-specific operations.

## Label Encoding

```python
# Numeric codes for each category (0-based)
iris['species_code'] = iris['species_cat'].cat.codes

iris[['species', 'species_code']].head()
```

- Useful when categories need to be represented as integers.
- Example: feeding into models that require numeric input.

## One-Hot Encoding

```python
# One-hot encode the species column
encoded = pd.get_dummies(iris, columns=['species'])
encoded.head()
```

- Creates binary indicator variables for each category.
- Useful for machine learning models.

## Crosstab (Contingency Tables)

`pd.crosstab()` is useful for analyzing the relationship between two or more categorical variables.

```python
# Frequency of species vs. sepal_width > 3.0
pd.crosstab(iris['species'], iris['sepal_width'] > 3.0)

# Crosstab with aggregation (median sepal length per species × width group)
pd.crosstab(
    iris['species'],
    iris['sepal_width'] > 3.0,
    values=iris['sepal_length'],
    aggfunc='median'
)

# Normalize to get proportions
pd.crosstab(iris['species'], iris['sepal_width'] > 3.0, normalize='index')
```

- `crosstab` creates frequency or summary tables of categorical variables.
- Supports aggregation and normalization.
- Useful for quick exploratory comparisons.

## Inspect Category Info

### Reorder Categories

```python
iris['species_cat'] = iris['species_cat'].cat.reorder_categories(
    ['setosa', 'versicolor', 'virginica'],
    ordered=True
)
```

### Rename Categories

```python
iris['species_cat'] = iris['species_cat'].cat.rename_categories(
    {'setosa': 'SETOSA', 'versicolor': 'VERSICOLOR', 'virginica': 'VIRGINICA'}
)
```

## Consistent Encoding Across Datasets

When preparing train/test splits, you may want to ensure both have the **same set of categories**, even if some are missing in one split.

```python
df = pd.DataFrame({"name_cat": ["Bella", "Lucy", "Bella"]})
df["name_cat"] = df["name_cat"].astype("category")

# Redefine categories (even if some are not present)
df["name_cat"] = df["name_cat"].cat.set_categories(["Bella", "Lucy", "Max"])

# One-hot encode with extra column for NaN
pd.get_dummies(df["name_cat"], dummy_na=True)
```

Output:

```
   Bella  Lucy  Max  NaN
0      1     0    0    0
1      0     1    0    0
2      1     0    0    0
```

- `set_categories([...])`: standardizes category list (Bella, Lucy, Max).
- `pd.get_dummies(..., dummy_na=True)`: produces consistent dummy columns with an extra `NaN` column.
- This ensures **train and test sets** have the same dummy columns, avoiding model training/serving mismatches.

## Find Inconsistent Categories

```python
# Simulate a known set of categories
known_species = ["setosa", "versicolor", "virginica"]

# Introduce a typo for demonstration
iris_with_typo = iris.copy()
iris_with_typo.loc[0, 'species'] = "setossa"

# Identify inconsistent categories
observed_species = set(iris_with_typo['species'])
inconsistent_species = observed_species.difference(known_species)

# Filter inconsistent and consistent rows
inconsistent_rows = iris_with_typo['species'].isin(inconsistent_species)
inconsistent_data = iris_with_typo[inconsistent_rows]
consistent_data = iris_with_typo[~inconsistent_rows]
```

## Key Takeaways

- Use `.astype('category')` to convert columns to categorical type.
- Use `.cat.codes` for label encoding.
- Use `pd.get_dummies()` for one-hot encoding.
- Use `pd.crosstab()` for contingency tables and categorical comparisons.
- `.cat` accessor allows reordering, renaming, and inspecting categories.
- Use `set_categories` + `pd.get_dummies(..., dummy_na=True)` for **consistent encoding across datasets**.
