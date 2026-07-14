# Pandas: Categorical Data & Encoding

This note focuses on categorical data as a data-type and encoding problem inside pandas. If you want chart patterns for categorical variables, see [Seaborn: Categorical Plots](../../data-manipulation-and-eda/visualization/seaborn/categorical.md).

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

Sometimes a useful workflow is:

1. map raw labels to cleaner business labels
2. then convert the result to a categorical column

```python
mapping = {
    "0-15 Min": "short",
    "16-30 Min": "medium",
    "30+ Min": "long",
}

df["stop_length"] = df["stop_duration"].map(mapping)
```

This is helpful when the raw labels are verbose, inconsistent, or not in the order you actually want to analyze.

This pattern is especially helpful for survey data, where raw response labels are often long, messy, or semantically ordered rather than alphabetic.

```python
likert_map = {
    "Never": "never",
    "Rarely": "rarely",
    "Sometimes": "sometimes",
    "Often": "often",
    "Always": "always",
}

df["exercise_freq"] = df["exercise_freq_raw"].map(likert_map)
```

### When Category Saves Memory

`category` 最適合「重複值很多、唯一值相對少」的欄位，例如：

- country
- product type
- status
- manufacturer

```python
used_cars["manufacturer_name"].astype("category")
```

這類欄位通常會比 `object` 省很多記憶體，因為底層是：

- 一份 category 清單
- 一份對應到 category 的整數 codes

但如果欄位幾乎每列都不同，例如 ID、自由文字、URL，高 cardinality 時 category 的省記憶體效果就可能很有限，甚至不值得轉。

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

`ordered=True` 不只是標記而已，它會影響排序、比較與某些 groupby 呈現順序。

```python
dogs["coat"] = dogs["coat"].cat.set_categories(
    ["short", "medium", "long"],
    ordered=True,
)

dogs.sort_values("coat")
```

如果 `ordered=False`，這個欄位仍然是 categorical，但不應該被解讀成有自然大小關係。

一旦 category 被標成有序，就可以做有意義的比較與區間篩選：

```python
dogs["coat"] = dogs["coat"].cat.reorder_categories(
    ["short", "medium", "long"],
    ordered=True,
)

dogs[dogs["coat"] > "short"]
```

這種寫法只有在 category 順序本身有業務語意時才成立。

Survey 裡的 Likert 題是最常見的例子：

```python
likert_order = ["never", "rarely", "sometimes", "often", "always"]

df["exercise_freq"] = pd.Categorical(
    df["exercise_freq"],
    categories=likert_order,
    ordered=True,
)

df["exercise_freq"].value_counts().sort_index()
df[df["exercise_freq"] >= "often"]
```

Warning: 如果問卷把 Likert 題編成 `1` 到 `5`，它在 pandas 可能看起來像普通整數，但分析上仍然是 ordinal，不應直接當成等距連續數值。

### Rename Categories

```python
iris['species_cat'] = iris['species_cat'].cat.rename_categories(
    {'setosa': 'SETOSA', 'versicolor': 'VERSICOLOR', 'virginica': 'VIRGINICA'}
)
```

## Remove Unused Categories

When filtering or modifying a DataFrame, some categories may no longer be used in the data but still appear in the category list. Use `.remove_unused_categories()` to clean them up.

```python
import pandas as pd

df = pd.DataFrame({'col': ['apple', 'banana', 'apple']})
df['col'] = df['col'].astype('category')
print(df['col'].cat.categories)
# Index(['apple', 'banana'], dtype='object')

# Drop all banana rows
df = df[df['col'] != 'banana']
print(df['col'].cat.categories)
# Index(['apple', 'banana'], dtype='object')  <- banana still listed

# Remove unused categories
df['col'] = df['col'].cat.remove_unused_categories()
print(df['col'].cat.categories)
# Index(['apple'], dtype='object')
```

- `.remove_unused_categories()` updates the category list to include only categories actually present in the data.
- Rows are **not dropped** and values are **not turned into NaN** — it only prunes the category list.

### Difference from `set_categories`

```python
# Force categories to only 'apple'
df['col'] = df['col'].cat.set_categories(['apple'])
print(df)
```

Output:

```
     col
0   apple
1     NaN   # banana is no longer a valid category → becomes NaN
2   apple
```

- `.set_categories()` explicitly resets allowed categories, and any values not in the new set become `NaN`.
- `.remove_unused_categories()` only cleans up unused categories without altering valid values.

## Ordered Categories and GroupBy Output

有序 category 不只影響 `sort_values()`，也常影響 groupby 結果的呈現順序，這在報表和視覺化前整理很有用。

```python
dogs["coat"] = dogs["coat"].cat.reorder_categories(
    ["short", "medium", "long"],
    ordered=True,
)

dogs.groupby("coat")["age"].mean()
```

這樣的輸出順序通常會跟 category 順序一致，而不是單純字母排序。

如果你的目標是業務邏輯順序，例如：

- `low`, `medium`, `high`
- `bronze`, `silver`, `gold`
- `S`, `M`, `L`, `XL`

那先把 category 順序定好，通常比事後手動重排更穩定。

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
- Use `.remove_unused_categories()` to prune unused categories.
- Use `.set_categories()` carefully, since it can turn values not in the new list into `NaN`.
- Use `set_categories` + `pd.get_dummies(..., dummy_na=True)` for **consistent encoding across datasets**.
