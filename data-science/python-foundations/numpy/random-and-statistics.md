# NumPy Random Sampling and Statistics

## NumPy Random Sampling

### Example Setup

```python
import numpy as np

np.random.seed(42)  # Set seed for reproducibility
```

- Setting a seed ensures the same random numbers are generated each time.

### Random Numbers from Distributions

```python
np.random.normal(0, 1, 10)
# Example Output: [ 0.4967 -0.1383  0.6477  1.5230 -0.2341 -0.2341  1.5792  0.7674 -0.4695  0.5426]
```

- Normal distribution with mean `0` and standard deviation `1`, 10 samples.

```python
np.random.normal(loc=10, scale=2, size=(3, 5))
# 3x5 matrix, mean=10, std=2
# Example Output:
# [[10.99  8.72 11.30 13.05  9.53]
#  [ 8.53  9.54  8.54 11.54  9.54]
#  [ 9.35 11.91  8.75 10.75  9.75]]
```

### Uniform Random Numbers

```python
np.random.rand(3, 2)
# Example Output:
# [[0.42 0.72]
#  [0.  0.3 ]
#  [0.15 0.9 ]]
```

- Generates samples from uniform distribution over \[0,1).

### Random Integers

```python
np.random.randint(0, 10, size=5)
# Example Output: [6 3 7 4 6]
```

- Random integers between 0 (inclusive) and 10 (exclusive).

```python
np.random.randint(0, 10, (2, 3))
# Example Output:
# [[2 9 4]
#  [1 7 6]]
```

- 2x3 matrix of random integers.

### Random Choice

```python
np.random.choice(10, 5, replace=False)
# Example Output: [2 8 4 9 1]
```

- Randomly choose 5 unique numbers from range(0,10).

```python
weather = ['windy','cloudy','sunny','rainy']
weather_pick = np.random.choice(weather, size=(4,7), replace=True, p=[0.2,0.5,0.2,0.1])
print(weather_pick)
# Example Output (4x7 matrix of weather):
# [['cloudy' 'cloudy' 'rainy' 'cloudy' 'sunny' 'windy' 'cloudy']
#  ['cloudy' 'windy' 'sunny' 'rainy' 'cloudy' 'cloudy' 'cloudy']
#  ['windy'  'cloudy' 'sunny' 'cloudy' 'cloudy' 'cloudy' 'rainy']
#  ['cloudy' 'cloudy' 'windy' 'rainy' 'sunny'  'cloudy' 'cloudy']]
```

- Sampling with replacement, with specified probabilities `p` for each outcome.

```python
dice_random_choice = np.random.choice(list(range(1,7)), size=10, replace=True)
```

#### Random Steps and Simple Simulation

`np.random.choice()` 很常被拿來建立簡單 simulation，例如 random walk：

```python
np.random.seed(123)
steps = np.random.choice([-1, 1], size=100, replace=True)
walk = steps.cumsum()
```

這裡的直覺是：

- 每一步不是 `-1` 就是 `+1`
- `cumsum()` 把局部隨機步伐累積成整條路徑

這種 pattern 常是 Monte Carlo、toy simulation 與 stochastic process 入門的第一步。

### Shuffle

```python
sample = np.arange(10)
np.random.shuffle(sample)
print(sample)
# Example Output: [8 1 5 0 7 2 9 4 3 6]
```

- `np.random.shuffle` randomly permutes the elements of an array in place along the first axis.

### Repeated Seeds for Same Output

```python
np.random.seed(1)
print(np.random.rand()) # 0.417022004702574
print(np.random.rand()) # 0.7203244934421581

np.random.seed(1)
print(np.random.rand()) # 0.417022004702574
print(np.random.rand()) # 0.7203244934421581
```

- Resetting the seed produces identical results — useful for reproducibility.

### Summary

- **`rand`**: uniform distribution over \[0,1).
- **`randn` / `normal`**: samples from normal distribution.
- **`randint`**: random integers in specified range.
- **`choice`**: sample elements with or without replacement.
- **`shuffle`**: randomly permute elements along the first axis.
- **Seed (`np.random.seed`)**: ensures reproducibility of results.

## NumPy Statistics

This note focuses on **array-level numerical summaries**: mean, quantiles, z-scores, dispersion, and transformations on NumPy arrays. For DataFrame-oriented summaries, correlations, and rolling calculations, see [Pandas: Statistics & Correlation](../pandas/statistics.md).

### Example Array

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5, 100])
print(arr)
# [  1   2   3   4   5 100]
```

### Basic Statistics

```python
np.mean(arr)    # 19.166666666666668  → average value of elements
np.median(arr)  # 3.5                 → middle value when the array is sorted
```

### Aggregations

```python
arr.sum()   # 115 → total sum of all elements
arr.min()   # 1   → smallest value
arr.max()   # 100 → largest value
arr.std()   # 36.1 (approx) → standard deviation, measure of spread
arr.var()
```

- These are **descriptive statistics** that summarize the dataset.

### Quantiles and Percentiles

```python
np.quantile(arr, 0.25)                     # 2.25
np.quantile(arr, 0.75)                     # 4.75
np.percentile(arr, 90)                     # 55.0
np.quantile(arr, [0, 0.25, 0.5, 0.75, 1])  # [  1.    2.25  3.5   4.75 100.  ]
```

- **Quantiles** divide data into intervals. For example, 0.25 is the first quartile (25%).
- **Percentiles** are specific points in the data (e.g., 90th percentile).

### Interquartile Range (IQR)

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

### Z-score Outlier Detection

```python
z_scores = (arr - arr.mean()) / arr.std()
print(z_scores)
# [-0.58 -0.54 -0.51 -0.47 -0.44  2.54]

arr[np.abs(z_scores) > 2]
# [100]
```

- **Z-scores** standardize data. Values with |z| > 2 are often considered outliers.

### Rounding & Dispersion

```python
num1 = np.array([-1.67, -1.01, 0.97, 1.63])

np.round(num1, decimals=1)  # [-1.7 -1.0  1.0  1.6]
np.floor(num1)              # [-2. -2.  0.  1.]
np.ceil(num1)               # [-1. -1.  1.  2.]
```

- Rounding functions help with numerical presentation and approximations.

### Mean Absolute Deviation (MAD)

```python
dists = arr - np.mean(arr)
abs_dists = np.abs(dists)
mean_abs_dists = np.mean(abs_dists)
print(mean_abs_dists)
# 15.833333333333334
```

- **MAD** is another measure of spread, less sensitive to extreme outliers than standard deviation.

### Transformations

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

### Summary

- **Mean** and **Median** summarize central tendency.
- **Aggregations** (`sum`, `min`, `max`, `std`) provide descriptive summaries.
- **Quantiles/Percentiles** divide data into meaningful cut points.
- **IQR** measures spread and variability.
- **Z-scores** help detect outliers.
- **Rounding** is useful for presentation and approximations.
- **MAD** gives a robust alternative spread measure.
- **Transformations** (log, sqrt, Box-Cox) help normalize or stabilize data.
- These tools are essential for exploratory data analysis and preprocessing.
