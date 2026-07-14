# Outlier Handling

Outliers are observations that sit far away from the bulk of a distribution. They can come from data entry mistakes, measurement problems, or genuinely extreme behavior.

處理離群值的重點不是「看起來很大就刪」，而是先分辨它到底是錯誤，還是真實但少見的現象。

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

這種作法本質上就是 winsorization 的一種簡化版本。

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

## Common Detection Rules

### IQR Rule

```python
q1 = df["col1"].quantile(0.25)
q3 = df["col1"].quantile(0.75)
iqr = q3 - q1

lower_threshold = q1 - 1.5 * iqr
upper_threshold = q3 + 1.5 * iqr

df_outlier = df[
    (df["col1"] < lower_threshold) | (df["col1"] > upper_threshold)
]
```

IQR rule 對偏態分布通常比單純 mean +/- k*sd 更穩一些。

### Z-Score Rule

```python
from scipy.stats import zscore

df["zscore"] = zscore(df["feature"])
outliers = df[df["zscore"].abs() > 3]
```

這種方法比較依賴分布近似對稱，否則容易被極端值本身拉歪。

## Winsorization

如果你不想直接刪資料，但也不想讓極端值主導模型，可以考慮 winsorization。

```python
from scipy.stats.mstats import winsorize

basetable["variable_winsorized"] = winsorize(
    basetable["variable"],
    limits=[0.05, 0.01],
)
```

這代表把最小的 5% 和最大的 1% 壓回較接近分位數的範圍。

## Standard Deviation Capping

另一種常見作法是把數值限制在 `mean +/- 3 * sd` 內：

```python
mean_age = basetable["age"].mean()
sd_age = basetable["age"].std()
lower_limit = mean_age - 3 * sd_age
upper_limit = mean_age + 3 * sd_age

basetable["age_no_outliers"] = [
    min(max(a, lower_limit), upper_limit)
    for a in basetable["age"]
]
```

這在近似常態的欄位比較合理；對 heavy-tailed feature 要更小心。

## Critical Notes

- **Understand context**: Outliers may carry important domain-specific information (e.g., rare diseases, fraud cases). Blindly removing them can erase valuable signals.
- **Detect carefully**: Use statistical rules (e.g., z-score, IQR method) but confirm with domain knowledge.
- **Consistency**: Apply the same strategy across train and test sets to avoid [data leakage](../foundations/data-leakage.md).
- **Model choice**: Some models (e.g., tree-based algorithms) are more robust to outliers than others (e.g., [linear regression](../supervised-learning/regression/linear.md)).
- **Missing-value interaction**: 有些極端值與缺值會一起出現，這時候要把 [imputation](imputation.md) 一起考慮。
- **Aggregate features can be skewed**: 像 `sum_spend`、`max_donation`、`days_since_last_event` 這類 basetable 特徵，常常會比原始欄位更偏。

> Outlier handling should balance **data integrity** and **model performance**. Always combine statistical methods with **domain expertise** before deciding how to treat outliers.

## Related Concepts

- [Feature Scaling](feature-scaling.md)
- [MSE, RMSE](../evaluation/mse-rmse.md)
- [Model Diagnostics](../interpretability-and-diagnostics/model-diagnostics.md)
- [Generalization](../foundations/generalization.md)
- [Imputation](imputation.md)
- [Basetable and Time-Aware Feature Engineering](../foundations/basetable-and-time-aware-feature-engineering.md)

[Back to Preprocessing](README.md)
