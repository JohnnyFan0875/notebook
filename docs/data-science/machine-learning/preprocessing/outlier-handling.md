# Outlier Handling

## -- to be added
```
- Using IQR (Interquartile Range)
    - (data < Q1 - 1.5 * IQR) or (data > Q3 + 1.5 * IQR)

```python
#method 1
data_0.75 = np.quantile(data, 0.75) = data.quantile(0.75)
data_0.25 = np.quantile(data, 0.25) = data.quantile(0.25)
iqr = data_0.75 - data_0.25

#method2
from scipy.stats import iqr
col1_iqr = iqr(data)
```

```python
lower_[threshold](../evaluation/classification-thresholds-and-calibration.md) = np.quantile(df['col1'], 0.25) - 1.5 * iqr
upper_[threshold](../evaluation/classification-thresholds-and-calibration.md) = np.quantile(df['col1'], 0.75) + 1.5 * iqr
df_outlier = df[(df['col1'] < lower_[threshold](../evaluation/classification-thresholds-and-calibration.md)) | (df['col1'] > upper_threshold)]
```

- Using z-score

```python
df = pd.DataFrame({'feature': [10, 12, 14, 15, 100, 18, 20, 21, 25, 28]})
df['zscore'] = scipy.stats.zscore(df['feature'])

[threshold](../evaluation/classification-thresholds-and-calibration.md) = 3

# Detect outliers (Z-score > 3 or < -3)
outliers = df[abs(df['zscore']) > [threshold](../evaluation/classification-thresholds-and-calibration.md)]
```
```

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

- **Description**: Limit the influence of extreme values by capping them at a [threshold](../evaluation/classification-thresholds-and-calibration.md).
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
- **Consistency**: Apply the same strategy across train and test sets to avoid [data leakage](../foundations/data-leakage.md).
- **Model choice**: Some models (e.g., tree-based algorithms) are more robust to outliers than others (e.g., [linear regression](../supervised-learning/regression/linear.md)).

> Outlier handling should balance **data integrity** and **model performance**. Always combine statistical methods with **domain expertise** before deciding how to treat outliers.

## Related Concepts

- [Feature Scaling](feature-scaling.md)
- [MSE, RMSE](../evaluation/mse-rmse.md)
- [Model Diagnostics](../interpretability-and-diagnostics/model-diagnostics.md)
- [Generalization](../foundations/generalization.md)

[Back to Preprocessing](README.md)
