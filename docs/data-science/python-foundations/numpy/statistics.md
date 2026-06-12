# NumPy Statistics

## Example Array

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5, 100])
print(arr)
# [  1   2   3   4   5 100]
```

## Basic Statistics

```python
np.mean(arr)    # 19.166666666666668  → average value of elements
np.median(arr)  # 3.5                 → middle value when the array is sorted
```

## Aggregations

```python
arr.sum()   # 115 → total sum of all elements
arr.min()   # 1   → smallest value
arr.max()   # 100 → largest value
arr.std()   # 36.1 (approx) → standard deviation, measure of spread
arr.var()
```

- These are **descriptive statistics** that summarize the dataset.

## Quantiles and Percentiles

```python
np.quantile(arr, 0.25)                     # 2.25
np.quantile(arr, 0.75)                     # 4.75
np.percentile(arr, 90)                     # 55.0
np.quantile(arr, [0, 0.25, 0.5, 0.75, 1])  # [  1.    2.25  3.5   4.75 100.  ]
```

- **Quantiles** divide data into intervals. For example, 0.25 is the first quartile (25%).
- **Percentiles** are specific points in the data (e.g., 90th percentile).

## Interquartile Range (IQR)

```python
q1, q3 = np.percentile(arr, [25, 75])
iqr = q3 - q1                         # 2.5
```

- **IQR** = Q3 − Q1, measures spread of the middle 50% of data.

```python
from scipy.stats import iqr
iqr(arr)  # 2.5
```

- SciPy also provides an IQR function.

## Z-score Outlier Detection

```python
z_scores = (arr - arr.mean()) / arr.std()
print(z_scores)
# [-0.58 -0.54 -0.51 -0.47 -0.44  2.54]

arr[np.abs(z_scores) > 2]
# [100]
```

- **Z-scores** standardize data. Values with |z| > 2 are often considered outliers.

## Rounding & Dispersion

```python
num1 = np.array([-1.67, -1.01, 0.97, 1.63])

np.round(num1, decimals=1)  # [-1.7 -1.0  1.0  1.6]
np.floor(num1)              # [-2. -2.  0.  1.]
np.ceil(num1)               # [-1. -1.  1.  2.]
```

- Rounding functions help with numerical presentation and approximations.

## Mean Absolute Deviation (MAD)

```python
dists = arr - np.mean(arr)
abs_dists = np.abs(dists)
mean_abs_dists = np.mean(abs_dists)
print(mean_abs_dists)
# 15.833333333333334
```

- **MAD** is another measure of spread, less sensitive to extreme outliers than standard deviation.

## Transformations

```python
np.log(arr)
np.sqrt(arr)
```

- Log and square root transformations stabilize variance and reduce skewness.

```python
from scipy.stats import boxcox
transformed, lambda_val = boxcox(arr[arr > 0])
```

- **Box-Cox Transformation** makes data closer to normal distribution; requires positive values.

- **Log Transformation**: stabilizes variance, useful for positively skewed data.
- **Square Root / Cube Root Transformation**: useful for count or skewed data.
- **Box-Cox Transformation**: general method to normalize variance, requires strictly positive data.

## Summary

- **Mean** and **Median** summarize central tendency.
- **Aggregations** (`sum`, `min`, `max`, `std`) provide descriptive summaries.
- **Quantiles/Percentiles** divide data into meaningful cut points.
- **IQR** measures spread and variability.
- **Z-scores** help detect outliers.
- **Rounding** is useful for presentation and approximations.
- **MAD** gives a robust alternative spread measure.
- **Transformations** (log, sqrt, Box-Cox) help normalize or stabilize data.
- These tools are essential for exploratory data analysis and preprocessing.
