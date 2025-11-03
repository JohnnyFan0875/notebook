# Shape of Distribution

The **shape of a distribution** describes how data values are arranged across the range of observations. Understanding distribution shape helps interpret tendencies, variability, and potential deviations from normality.

Two primary numerical measures of shape are **skewness** and **kurtosis**, often complemented by visualizations such as histograms and Q–Q plots.

## 1. Skewness

### Definition

**Skewness** quantifies the degree of asymmetry in a data distribution.

$$
\text{Skewness} = \frac{\sum (x_i - \bar{x})^3}{(n-1)s^3}
$$

- $x_i$: each observation
- $\bar{x}$: sample mean
- $s$: sample standard deviation
- $n$: sample size

### Interpretation

| Skewness | Description                                    | Example                        |
| -------- | ---------------------------------------------- | ------------------------------ |
| 0        | Perfectly symmetric                            | Normal distribution            |
| > 0      | Right-skewed/Positive-skewed (long right tail) | Income, reaction time          |
| < 0      | Left-skewed/Negative-skewed (long left tail)   | Exam scores, age at retirement |

![Image](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*XU3Kdl521XnWHECHZ7XOaQ.jpeg)

### Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.datasets import load_iris

iris = load_iris(as_frame=True)
df = iris.frame

sns.histplot(df['sepal length (cm)'], kde=True, color='skyblue')
plt.title('Distribution Shape Example')
plt.xlabel('Sepal Length (cm)')
plt.show()

skew_val = df['sepal length (cm)'].skew()
print(f"Skewness: {skew_val:.3f}")
```

## 2. Kurtosis

### Definition

**Kurtosis** measures the “tailedness” or concentration of values near the mean compared to the tails.

$$
\text{Kurtosis} = \frac{\sum (x_i - \bar{x})^4}{(n-1)s^4}
$$

### Interpretation

| Type            | Description             | Shape                        |
| --------------- | ----------------------- | ---------------------------- |
| **Mesokurtic**  | Normal tail thickness   | (kurtosis ≈ 3 or excess ≈ 0) |
| **Leptokurtic** | Heavy tails, sharp peak | More outliers than normal    |
| **Platykurtic** | Flat top, light tails   | Fewer outliers               |

![Image](https://analystprep.com/cfa-level-1-exam/wp-content/uploads/2019/08/page-64.png)

### Python Example

```python
kurt_val = df['sepal length (cm)'].kurt()
print(f"Kurtosis: {kurt_val:.3f}")
```

## 3. Normality Assessment

| Method Type                      | Description                                                              | Reference                                                                                                                                                |
| -------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Histogram**                    | Visual overview of distribution symmetry and tails.                      | [Normality Tests – Visual Methods](../inferential-statistics/2-hypothesis-testing-framework/assumption-tests/normality-tests.md#visual-methods)          |
| **Q–Q Plot (Quantile–Quantile)** | Compares data quantiles with those of a theoretical normal distribution. | [Normality Tests – Q–Q Plot](../inferential-statistics/2-hypothesis-testing-framework/assumption-tests/normality-tests.md#qq-plot-quantilequantile-plot) |
| **Shapiro–Wilk Test**            | Formal statistical test for normality (small to moderate samples).       | [Normality Tests – Shapiro–Wilk](../inferential-statistics/2-hypothesis-testing-framework/assumption-tests/normality-tests.md#shapirowilk-test)          |
| **Anderson–Darling Test**        | Robust test comparing empirical and theoretical distributions.           | [Normality Tests – Anderson–Darling](../inferential-statistics/2-hypothesis-testing-framework/assumption-tests/normality-tests.md#andersondarling-test)  |

For detailed procedures, interpretation, and example code, see the full section in [**Inferential Statistics – Normality Tests**](../inferential-statistics/2-hypothesis-testing-framework/assumption-tests/normality-tests.md)

## 4. Practical Guidelines

| Condition                   | Recommended Measure                 | Reason                           |
| --------------------------- | ----------------------------------- | -------------------------------- |
| Moderate skew / light tails | Report skewness & kurtosis only     | Shape nearly normal              |
| Strong skew / heavy tails   | Apply transformation (log, Box–Cox) | Stabilizes variance & symmetry   |
| Very small sample           | Use visual + Shapiro test           | Statistical tests may lack power |

## 5. Key Takeaways

- **Skewness** describes direction and degree of asymmetry.
- **Kurtosis** describes concentration of tails relative to the normal distribution.
- Always **visualize** before applying formal tests.
- Normality assessment is crucial for choosing **parametric vs non-parametric** tests later in inferential statistics.
