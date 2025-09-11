# Outlier Handling

Outliers are data points that deviate significantly from the majority of a dataset. They can arise from measurement errors, data entry mistakes, or genuine variability. Handling outliers appropriately is important, as they can distort statistical summaries, bias model training, and affect prediction accuracy.

## Common Techniques

### 1. Remove Outliers

- **Description**: Drop observations that are erroneous or irrelevant.
- **When to use**: When outliers are clearly due to mistakes (e.g., negative age).
- **Example in Python**:

```python
import pandas as pd

# Example dataset
 df = pd.DataFrame({"age": [25, 28, 30, 150, 27]})

# Remove outliers using a threshold
 df = df[df["age"] < 120]
```

### 2. Cap or Clip Outliers

- **Description**: Limit the influence of extreme values by capping them at a threshold.
- **When to use**: When extreme values are real but should not dominate.
- **Example in Python**:

```python
import numpy as np

# Winsorization: cap values outside 1st and 99th percentile
lower, upper = df["age"].quantile([0.01, 0.99])
df["age"] = np.clip(df["age"], lower, upper)
```

### 3. Transformations

- **Description**: Apply transformations to compress the range of data.
- **Common transforms**: log, square root, cube root.
- **Example in Python**:

```python
import numpy as np

# Apply log transformation (adding 1 to avoid log(0))
df["log_income"] = np.log1p(df["income"])
```

### 4. Impute Outliers

- **Description**: Replace outliers with more representative values.
- **When to use**: If data is limited and removal is not ideal.
- **Example in Python**:

```python
median_age = df["age"].median()
df.loc[df["age"] > 120, "age"] = median_age
```

## Critical Notes

- **Understand context**: Outliers may carry important domain-specific information (e.g., rare diseases, fraud cases). Blindly removing them can erase valuable signals.
- **Detect carefully**: Use statistical rules (e.g., z-score, IQR method) but confirm with domain knowledge.
- **Consistency**: Apply the same strategy across train and test sets to avoid data leakage.
- **Model choice**: Some models (e.g., tree-based algorithms) are more robust to outliers than others (e.g., linear regression).

> Outlier handling should balance **data integrity** and **model performance**. Always combine statistical methods with **domain expertise** before deciding how to treat outliers.
