# Descriptive Statistics

Descriptive statistics summarize and describe the main features of a dataset. They provide simple summaries about the **center**, **spread**, and **shape** of data distributions.

## 1. Central Tendency

### Mean

$$
\bar{x} = \frac{\sum\_{i=1}^n x_i}{n}
$$

- \(x_i\): each individual data point
- \(n\): number of data points (sample size)
- \(\bar{x}\): sample mean (average)

### Median

- The middle value when all data points are ordered.
- For even \(n\), it is the average of the two middle values.

### Mode

- The most frequently occurring value(s).

📌 **Notes**

- Mean is sensitive to outliers.
- Median and mode are more robust in skewed distributions.

```python
from sklearn.datasets import load_iris
import pandas as pd

iris = load_iris(as_frame=True)
df = iris.frame

df['sepal length (cm)'].mean()
df['sepal length (cm)'].median()
df['sepal length (cm)'].mode()[0]
```

## 2. Measures of Dispersion

### Range

\[
\text{Range} = \max(x_i) - \min(x_i)
\]

- \(\max(x_i)\): largest value
- \(\min(x_i)\): smallest value

### Variance

- Variance is the **square of standard deviation**.
- Units are squared compared to the data points (e.g., cm² if data is in cm).

\[
\sigma^2 = \frac{\sum*{i=1}^N (x_i - \mu)^2}{N}, \quad
s^2 = \frac{\sum*{i=1}^n (x_i - \bar{x})^2}{n-1}
\]

- \(x_i\): each data point
- \(\mu\): population mean
- \(\bar{x}\): sample mean
- \(N\): population size
- \(n\): sample size

📌 **Notes:**

- Sample variance is usually larger than population variance due to estimation uncertainty.

```python
import numpy as np
pop_var = np.var(data)            # population variance
samp_var = np.var(data, ddof=1)   # sample variance
```

### Standard Deviation (SD)

- Describes how spread out or dispersed the values in a dataset are around the mean (average).
- 資料的發散程度，可以用「各資料點與平均數的距離」來理解。
- Same unit as the data points.
- Square root of variance.

\[
\sigma = \sqrt{\frac{\sum*{i=1}^N (x_i - \mu)^2}{N}}, \quad
s = \sqrt{\frac{\sum*{i=1}^n (x_i - \bar{x})^2}{n-1}}
\]

- \(x_i\): each data point
- \(\mu\): population mean
- \(\bar{x}\): sample mean
- \(N\): population size
- \(n\): sample size
- \(n-1\): Bessel’s correction (sample variance tends to underestimate population variance, so we divide by \(n-1\))

📌 **Notes:**

- Sample SD ≥ Population SD (due to estimation uncertainty).

```python
import numpy as np
pop_std = np.std(data)          # population SD
samp_std = np.std(data, ddof=1) # sample SD
```

### Empirical Rule (68–95–99.7 rule)

- In a normal distribution:
  - 68% of values fall within 1 SD of mean
  - 95% within 2 SD
  - 99.7% within 3 SD

```python
from scipy import stats

cum_prob_mean_plus_one_std = stats.norm.cdf(11, 10, 1)  # mean=10, std=1
cum_prob_mean_minus_one_std = stats.norm.cdf(9, 10, 1)
cum_prob_mean_plus_one_std - cum_prob_mean_minus_one_std  # ≈ 68%
```

### Interquartile Range (IQR)

\[
\text{IQR} = Q_3 - Q_1
\]

- \(Q_1\): 25th percentile (lower quartile)
- \(Q_3\): 75th percentile (upper quartile)
- Represents the spread of the middle 50% of data.

## 3. Standard Error (SE)

- SE = standard deviation of the **sampling distribution of the mean**.
- 樣本平均數距離母體平均數多遠的誤差程度資訊。
- If you draw many samples of size \(n\) and compute their means, the SD of those means is the SE.

\[
SE = \frac{s}{\sqrt{n}}
\]

- \(s\): sample standard deviation
- \(n\): sample size

```python
import scipy.stats as stats
stats.sem(df['sepal length (cm)']) # standard error of the mean (sem)
```

```python
np.std(df['sepal length (cm)'], ddof=1) / np.sqrt(len(df['sepal length (cm)']))
```

📌 **Notes:**

- SE decreases as sample size increases.
- Can be estimated with **bootstrap** (resampling the sample) or **Monte Carlo simulation** (if population parameters are known).
- Reference: [haosquare](https://haosquare.com/standard-error/)

### Example

#### Example 1: Single Sample

- Quick formula in practice. Most common in real applications.

```python
sample_size = 100
sample_data = df.sample(n=sample_size)  # one sample drawn from population
```

#### Example 2: Bootstrap SE

- When only one dataset is available and the population distribution is unknown.
- Resample with replacement many times → compute means → estimate SE.
- More robust, data-driven method.

```python
import random
n_bootstrap = 5000

arr = []
for _ in range(n_bootstrap):
    new_data = random.choices(sample_data, k=sample_size) # resample with replacement
    arr.append(np.mean(new_data))

std_error = np.std(arr, ddof=1)
```

#### Example 3: Monte Carlo Simulation (known mean & std)

- Simulation-based approach when true parameters are known
- When population parameters (\(\mu, \sigma\)) are known.
- Generate repeated random samples from the true distribution.
- Used in teaching, simulations, and validation of formulas. .

```python
n_sample = 5000
arr = []

for _ in range(n_sample):
    new_data = np.random.normal(pop_mean, pop_std, size=sample_size)
    arr.append(new_data.mean())

std_error = np.std(arr)  # ddof=0 since population known
```

## 4. Confidence Interval (CI)

\[
CI = \bar{x} \pm z\_{\alpha/2} \times SE
\]

- \(\bar{x}\): sample mean
- \(z\_{\alpha/2}\): critical z-value (e.g., 1.96 for 95% CI)
- \(SE\): standard error

📌 **Notes:**

- Lower bound and upper bound correspond to the **2.5th and 97.5th percentiles** of the sampling distribution (for 95% CI).

```python
import numpy as np

mean = df['sepal length (cm)'].mean()
se = stats.sem(df['sepal length (cm)'])
ci = stats.t.interval(0.95, len(df)-1, loc=mean, scale=se)
ci
```

## 5. Correlation & R²

### Pearson Correlation

\[
r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}
\]

- \(x_i, y_i\): paired values
- \(\bar{x}, \bar{y}\): sample means of X and Y

Range: –1 (perfect negative) → +1 (perfect positive).

### Coefficient of Determination

- **Definition:** Measures how well the independent variable(s) explain the variance in the dependent variable.
- **Formula:**  
  \[
  R^2 = r^2
  \]  
  where \(r\) is the Pearson correlation coefficient.
- **Interpretation:**
  - Range: \(0 \leq R^2 \leq 1\)
  - \(R^2 = 0\): the model does not explain any variance in the target.
  - \(R^2 = 1\): the model perfectly explains the variance in the target.
- **Key points:**
  - \(R^2\) is the square of Pearson’s \(r\).
  - It describes the **degree of fit**, not causation.
  - Explains **goodness of fit**: how well the features explain the variance in the target variable.
  - In practice:
    - If \(r = 0.8\), then \(R^2 = 0.64\).
    - This means 64% of the variation in the target is explained by the predictor.

📌 **Notes:**

- Correlation shows whether two variables are linearly related; it does **not** indicate causation.
- If the relationship is not linear, consider **transformation** [link](../python-foundations/numpy/statistics.md#transformations).
- Related concept: [R-squared vs. Adjusted R-squared](r-squared-adjusted-r-squared.md).
- Reference: [Kaggle discussion](https://www.kaggle.com/discussions/getting-started/27261).

```python
# Pearson correlation
r = df['sepal length (cm)'].corr(df['petal length (cm)'])
r_squared = r**2
r, r_squared
```

## 6. Shape of Distribution

### Skewness

\[
\text{Skewness} = \frac{\sum (x_i - \bar{x})^3}{(n-1)s^3}
\]

- Positive skew → long right tail
- Negative skew → long left tail

![Image](https://cdn.analyticsvidhya.com/wp-content/uploads/2024/09/sk1.webp)

### Kurtosis

\[
\text{Kurtosis} = \frac{\sum (x_i - \bar{x})^4}{(n-1)s^4}
\]

- High kurtosis → heavy tails, more outliers
- Low kurtosis → flatter distribution

```python
df['sepal length (cm)'].skew(), df['sepal length (cm)'].kurt()
```

## 7. Normality Checks

Normality tests help assess whether data follows a **normal distribution**.

### 1. Visual Methods

- **Histogram**
  - Plot the frequency distribution of the data.
  - Skewness (asymmetry) can indicate deviation from normality.

```python
import matplotlib.pyplot as plt

df['sepal length (cm)'].hist()
plt.show()
```

- **Q-Q Plot (Quantile-Quantile Plot)**
  - Compares the quantiles of your data to the quantiles of a normal distribution.
  - If the data is normally distributed, points lie close to a straight line.
  - [seaborn Q-Q Plot](../visualization/seaborn/regression.md#quantile-quantile-qq-plot)

```python
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np

data = np.random.normal(0, 1, 100)
stats.probplot(data, dist="norm", plot=plt)
plt.show()
```

### 2. Statistical Tests

#### Shapiro-Wilk Test (most common)

- **Null hypothesis (H₀):** Data is normally distributed.
- **Test statistic formula:**  
  \[
  W = \frac{\left(\sum a*i x*{(i)}\right)^2}{\sum (x_i - \bar{x})^2}
  \]  
  where \(a_i\) are constants derived from expected values of order statistics of a standard normal distribution.

```python
from scipy import stats

data = [12.3, 15.4, 14.6, 13.7, 12.8, 15.2, 14.1, 13.5, 12.9, 14.0]
statistic, p_value = stats.shapiro(data)
print("Shapiro-Wilk Test:", statistic, p_value)
```

Interpretation:

- If **p > 0.05** → Fail to reject H₀ (data is consistent with normality).
- If **p ≤ 0.05** → Reject H₀ (data is not normally distributed).

#### Anderson-Darling Test

- More powerful for **small sample sizes**.
- Compares empirical distribution to the normal distribution.

```python
from scipy import stats

data = [12.3, 15.4, 14.6, 13.7, 12.8, 15.2, 14.1, 13.5, 12.9, 14.0]
result = stats.anderson(data, dist='norm')

print(f"Test Statistic: {result.statistic}")
print(f"Critical Values: {result.critical_values}")
print(f"Significance Levels: {result.significance_level}")
```

Interpretation:

- If the test statistic is greater than the critical value at a given significance level → Reject H₀ (data is not normal).

📌 **Summary:**

- **Histogram & Q-Q plot** → quick visual inspection.
- **Shapiro-Wilk** → widely used, reliable.
- **Anderson-Darling** → strong for small samples.

## 8. Visualization Tools

- **Histogram** → distribution shape
- **Boxplot** → quartiles, median, outliers
- **Density Plot** → smooth probability curve

```python
df['sepal length (cm)'].plot(kind='box')
```

## 9. Standardization

\[
Z = \frac{x - \bar{x}}{s}
\]

- \(x\): data point
- \(\bar{x}\): sample mean
- \(s\): sample standard deviation

📌 **Notes:**

- After standardization → mean = 0, SD = 1
- Skewness remains the same

## 🔑 Key Takeaways

- Variance has **squared units**, while SD keeps the same unit as data.
- **Sample SD ≥ population SD** due to estimation uncertainty.
- SE = SD of the sampling distribution of the mean.
- CI quantifies uncertainty, not probability of the parameter itself.
- Median & IQR are robust against skewness and outliers.
- Standardization (z-scores) is useful for comparing across scales.
