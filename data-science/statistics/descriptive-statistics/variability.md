# Variability

**Variability** (also called _dispersion_ or _spread_) describes how much the data differ from the center (mean or median). While measures of central tendency show where the data are centered, measures of variability tell us **how consistent or diverse** the data are.

Common measures include **range**, **variance**, **standard deviation**, and **interquartile range (IQR)**.

## 1. Range

### Definition

The **range** is the simplest measure of spread — the difference between the maximum and minimum values.

$$
\text{Range} = \max(x_i) - \min(x_i)
$$

### Properties

- Very sensitive to outliers.
- Provides a quick estimate of total spread.
- Does not describe how data are distributed between extremes.

### Python Example

```python
import pandas as pd
from sklearn.datasets import load_iris

df = load_iris(as_frame=True).frame
rng = df['sepal length (cm)'].max() - df['sepal length (cm)'].min()
print(f"Range: {rng:.2f}")
```

## 2. Variance

### Definition

The **variance** measures the average squared deviation of data points from the mean.

$$
\sigma^2 = \frac{\sum_{i=1}^N (x_i - \mu)^2}{N}, \quad
s^2 = \frac{\sum_{i=1}^n (x_i - \bar{x})^2}{n - 1}
$$

| Symbol         | Meaning                  |
| -------------- | ------------------------ |
| $x_i$          | Each data point          |
| $\mu, \bar{x}$ | Population / sample mean |
| $N, n$         | Population / sample size |

- **Population variance (σ²):** Divide by (N)
- **Sample variance (s²):** Divide by (n−1) (_Bessel’s correction_) to reduce bias in small samples.

### Properties

- Expressed in **squared units** (e.g., cm² if data are in cm).
- Sensitive to extreme values.
- Serves as the foundation for standard deviation and ANOVA.
- Sample variance is usually larger than population variance due to estimation uncertainty.

### Python Example

```python
import numpy as np

values = df['sepal length (cm)']
var_population = np.var(values)
var_sample = np.var(values, ddof=1)
print(f"Population variance: {var_population:.3f}\nSample variance: {var_sample:.3f}")
```

## 3. Standard Deviation (SD)

### Definition

The **standard deviation (SD)** is the square root of the variance. It has the same unit as the data and indicates the **typical distance from the mean**.

- 資料的發散程度，可以用「各資料點與平均數的距離」來理解
- Same unit as the data points.

$$
\sigma = \sqrt{\frac{\sum_{i=1}^N (x_i - \mu)^2}{N}}, \quad
s = \sqrt{\frac{\sum_{i=1}^n (x_i - \bar{x})^2}{n - 1}}
$$

### Interpretation

- A **small SD** → data are tightly clustered around the mean.
- A **large SD** → data are widely spread.

### Python Example

```python
std_population = np.std(values)
std_sample = np.std(values, ddof=1)
print(f"Population SD: {std_population:.3f}\nSample SD: {std_sample:.3f}")
```

### Empirical Rule (68–95–99.7 Rule)

For **normally distributed data**:

- 68% of values lie within 1 SD of the mean.
- 95% within 2 SD.
- 99.7% within 3 SD.

```python
from scipy import stats

within_1sd = stats.norm.cdf(1) - stats.norm.cdf(-1)
within_2sd = stats.norm.cdf(2) - stats.norm.cdf(-2)
within_3sd = stats.norm.cdf(3) - stats.norm.cdf(-3)
print(within_1sd, within_2sd, within_3sd)
```

## 4. Interquartile Range (IQR)

### Definition

The **IQR** represents the range of the middle 50% of data — between the 25th (Q₁) and 75th (Q₃) percentiles.

$$
\text{IQR} = Q_3 - Q_1
$$

### Properties

- Resistant to outliers and skewed data.
- Useful for comparing spread across groups.
- Forms the basis of boxplot whiskers.

### Python Example

```python
Q1 = df['sepal length (cm)'].quantile(0.25)
Q3 = df['sepal length (cm)'].quantile(0.75)
IQR = Q3 - Q1
print(f"IQR: {IQR:.3f}")
```

## 5. Comparison Summary

| Measure                | Formula                    | Robust to Outliers? | Units        | Notes                                |
| ---------------------- | -------------------------- | ------------------- | ------------ | ------------------------------------ |
| **Range**              | max − min                  | ❌ No               | Same as data | Simplest, ignores internal structure |
| **Variance**           | Mean of squared deviations | ❌ No               | Squared      | Basis for SD, used in ANOVA          |
| **Standard Deviation** | √Variance                  | ❌ No               | Same as data | Most common measure of spread        |
| **IQR**                | Q₃ − Q₁                    | ✅ Yes              | Same as data | Robust summary of middle 50%         |

## 6. Visualization Example

```python
import matplotlib.pyplot as plt

plt.boxplot(df['sepal length (cm)'])
plt.title('Boxplot of Sepal Length (cm)')
plt.ylabel('Value')
plt.show()
```

## 7. Key Takeaways

- Variability quantifies **how much data deviate** from the central value.
- **Range** and **SD** show total spread; **IQR** focuses on central spread.
- Always pair measures of variability with measures of central tendency for complete description.

**Next:** Explore [Shape of Distribution](./shape-distribution.md) to examine how symmetry and tails affect variabilit
