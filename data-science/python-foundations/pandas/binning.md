# Pandas: Binning & Categorization

Binning is the process of converting continuous variables into categorical ones by grouping values into bins. This is useful for summarizing data, building histograms, or preparing features for machine learning models.

## Example Dataset

```python
import seaborn as sns
import pandas as pd

# Use the Iris dataset
iris = sns.load_dataset("iris")
iris.head()
```

## Fixed-Width Bins with `pd.cut`

```python
# Bin sepal length into categories
iris['sepal_length_cat'] = pd.cut(
    iris['sepal_length'],
    bins=[4, 5, 6, 7, 8],
    labels=['4–5', '5–6', '6–7', '7–8']
)

iris[['sepal_length', 'sepal_length_cat']].head()
```

- `bins`: define the edges of intervals.
- `labels`: assign human-readable category names.
- Result is a categorical Series.

## Quantile-Based Bins with `pd.qcut`

```python
# Divide petal length into 3 quantile-based bins
iris['petal_length_group'] = pd.qcut(
    iris['petal_length'],
    q=3,
    labels=['Short', 'Medium', 'Long']
)

iris['petal_length_group'].value_counts()
```

- `q`: number of quantiles (e.g., 3 → tertiles).
- Ensures roughly equal number of samples per bin.
- Useful for splitting skewed distributions.

## Inspect Categories

```python
# List categories and counts
iris['sepal_length_cat'].cat.categories
iris['sepal_length_cat'].value_counts()
```

## Key Takeaways

- **`pd.cut()`**: fixed-width binning for continuous variables.
- **`pd.qcut()`**: quantile-based binning (equal-sized groups).
- Binning converts continuous values into categories, making patterns easier to interpret.
- Useful in **EDA** and **feature engineering**.
