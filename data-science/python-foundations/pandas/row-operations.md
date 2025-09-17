# Pandas: Row-wise Operations

Row-wise operations allow you to process or transform each row in a DataFrame. Common approaches include:

- Using `apply()` with a custom function
- Iterating with `iterrows()` (less efficient)

## Example Dataset

```python
import seaborn as sns
import pandas as pd

# Load iris dataset
iris = sns.load_dataset("iris").copy()

iris.head()
```

## Example: `apply()` for Row-wise Operation

- Mark samples where **sepal_length** is above the dataset’s average as `High`, otherwise `Low`.
- Create a row-wise function to classify them.

```python
# Custom function to classify sepal_length
def classify_length(sepal_length):
    threshold = iris['sepal_length'].mean()
    return "High" if sepal_length > threshold else "Low"

# Apply the function row-wise
iris['length_class'] = iris['sepal_length'].apply(classify_length)

iris[['sepal_length', 'length_class']].head()
```

**Output (first 5 rows):**

| sepal_length | length_class |
| ------------ | ------------ |
| 5.1          | Low          |
| 4.9          | Low          |
| 4.7          | Low          |
| 4.6          | Low          |
| 5.0          | Low          |

## Example: `iterrows()` Function for Row-wise Operation

`iterrows()` allows looping through each row in the DataFrame. While slower than `apply()`, it is sometimes easier for custom logic.

```python
for idx, row in iris.head(3).iterrows():
    print(f"Row {idx} - Sepal length: {row['sepal_length']}, Class: {row['length_class']}")
```

**Output:**

```
Row 0 - Sepal length: 5.1, Class: Low
Row 1 - Sepal length: 4.9, Class: Low
Row 2 - Sepal length: 4.7, Class: Low
```

## Additional Tips

```python
# Apply a function across multiple columns (row-wise sum)
iris['sepal_sum'] = iris[['sepal_length', 'sepal_width']].apply(lambda row: row.sum(), axis=1)

# Row-wise conditional labeling
iris['wide_flower'] = iris.apply(lambda row: 'Yes' if row['sepal_width'] > 3.2 else 'No', axis=1)
```

- Use `axis=1` with `.apply()` to process rows as Series.
- Use `.iterrows()` for custom logic when vectorization is difficult.
- Avoid `.iterrows()` on large datasets due to performance.

## Key Takeaways

- Prefer `.apply()` for efficiency when applying functions row-wise.
- Use `.iterrows()` for readability or when logic cannot be vectorized.
- Row-wise operations are useful for classification, conditional labeling, and row-based feature
