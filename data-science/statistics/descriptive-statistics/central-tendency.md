# Central Tendency

Measures of **central tendency** describe where the center or typical value of a dataset lies. They provide a single representative number summarizing an entire distribution.

Common measures include the **mean**, **median**, and **mode**. Each offers a different perspective on what is considered the “center” of the data and is appropriate under different conditions.

## 1. Mean (Arithmetic Average)

### Definition

The **mean** is the sum of all observations divided by the number of observations.

$$
\bar{x} = \frac{\sum_{i=1}^n x_i}{n}
$$

- $x_i$: each data point
- $n$: number of observations
- $\bar{x}$: sample mean

### Properties

- Sensitive to **outliers** and **skewed distributions**.
- Provides a stable measure for **symmetric** distributions.

### Python Example

```python
import pandas as pd
from sklearn.datasets import load_iris

iris = load_iris(as_frame=True)
df = iris.frame

mean_value = df['sepal length (cm)'].mean()
print(mean_value)
```

### Variants

| Type                | Formula                         | When to Use                           |
| ------------------- | ------------------------------- | ------------------------------------- |
| **Arithmetic Mean** | $\bar{x} = \frac{1}{n}\sum x_i$ | Regular datasets                      |
| **Geometric Mean**  | $(\prod x_i)^{1/n}$             | Growth rates, ratios, log-normal data |
| **Harmonic Mean**   | $\frac{n}{\sum (1/x_i)}$        | Speeds, rates, averages of ratios     |

## 2. Median (Middle Value)

### Definition

The **median** is the value separating the higher half and the lower half of the data.

For ordered data $x_1 \le x_2 \le \dots \le x_n$:

- If $n$ is odd → median = middle value.
- If $n$ is even → median = average of the two middle values.

### Properties

- **Robust to outliers and skewed distributions**.
- Represents the 50th percentile (Q₂) of the data.
- Preferred when the data are not symmetrically distributed.

### Python Example

```python
median_value = df['sepal length (cm)'].median()
print(median_value)
```

## 3. Mode (Most Frequent Value)

### Definition

The **mode** is the most frequently occurring value in the dataset.

- For continuous data, the mode corresponds to the **peak** of the distribution.
- A dataset may be:

  - **Unimodal** (one peak)
  - **Bimodal** (two peaks)
  - **Multimodal** (multiple peaks)

### Properties

- Useful for **categorical** and **discrete** variables.
- Can coexist with mean and median to describe distribution shape.

### Python Example

```python
mode_value = df['sepal length (cm)'].mode()[0]
print(mode_value)
```

## 4. Comparison and Use Cases

| Scenario                                    | Best Measure | Reason                          |
| ------------------------------------------- | ------------ | ------------------------------- |
| **Symmetric distribution without outliers** | Mean         | Uses all data points            |
| **Skewed or heavy-tailed distribution**     | Median       | Resistant to outliers           |
| **Categorical data**                        | Mode         | Represents most common category |
| **Data with extreme values**                | Median       | Robust to distortion            |

## 5. Relationship Between Mean, Median, and Mode

- **Symmetric distribution:** mean ≈ median ≈ mode
- **Right-skewed:** mean > median > mode
- **Left-skewed:** mean < median < mode

![Image](https://www.statisticshowto.com/wp-content/uploads/2014/02/pearson-mode-skewness.jpg)

## 6. Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns

sns.histplot(df['sepal length (cm)'], kde=True)
plt.axvline(df['sepal length (cm)'].mean(), color='red', linestyle='--', label='Mean')
plt.axvline(df['sepal length (cm)'].median(), color='green', linestyle='--', label='Median')
plt.legend()
plt.title('Mean vs Median Visualization')
plt.show()
```

## 7. Key Takeaways

- **Mean** is sensitive to outliers; use when data are symmetric and continuous.
- **Median** is robust; ideal for skewed data or when outliers exist.
- **Mode** is appropriate for categorical or discrete variables.
- When describing real data, it’s often useful to report **all three** to show distribution characteristics.

**Next:** Explore [Variability](./variability.md) to understand how data spread complements the measures of center.
