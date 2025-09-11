# Row-wise Operations

Row-wise operations allow you to process or transform each row in a dataframe. Common approaches include:

- Using `apply()` with a custom function
- Iterating with `iterrows()`

## Example: `Apply` Function for Row-wise Operation

- Mark samples where the **mean radius** is above the dataset’s average as `High`, otherwise `Low`.
- Create a row-wise function to classify them.

```python
import pandas as pd
from sklearn.datasets import load_breast_cancer

# Load dataset
data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)

# Custom function to classify mean radius
def classify_radius(mean_radius):
    threshold = df['mean radius'].mean()
    return "High" if mean_radius > threshold else "Low"

# Apply the function row-wise
df['radius_class'] = df['mean radius'].apply(classify_radius)

print(df[['mean radius', 'radius_class']].head())
```

**Output (first 5 rows):**

| mean radius | radius_class |
| ----------- | ------------ |
| 17.99       | High         |
| 20.57       | High         |
| 19.69       | High         |
| 11.42       | Low          |
| 20.29       | High         |

## Example: `iterrows()` Function for Row-wise Operation

`iterrows()` allows looping through each row in the dataframe. While slower than `apply()`, it is sometimes easier for custom logic.

```python
for idx, row in df.head(3).iterrows():
    print(f"Row {idx} - Mean radius: {row['mean radius']}, Class: {row['radius_class']}")
```

**Output:**

```
Row 0 - Mean radius: 17.99, Class: High
Row 1 - Mean radius: 20.57, Class: High
Row 2 - Mean radius: 19.69, Class: High
```

## Notes

- Prefer **`apply()`** for efficiency when applying the same function to each row or column.
- Use **`iterrows()`** for more flexible row-by-row operations, but be mindful of performance on large datasets.
- Always validate curated results before exporting.
