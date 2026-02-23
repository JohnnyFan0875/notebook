# 3. Univariate Analysis — Numerical Data

This section covers how to fully describe a **single numerical variable** (Interval or Ratio scale). A complete description requires three dimensions working together:

| Dimension            | Question It Answers                   |       Key Measures |
| -------------------- | ------------------------------------- | -----------------: |
| **Central Tendency** | Where is the center of the data?      | Mean, Median, Mode |
| **Variability**      | How spread out are the values?        | Range, SD, IQR, CV |
| **Shape**            | What does the distribution look like? | Skewness, Kurtosis |

> 📌 **Always describe all three.** Reporting only the mean without variability or shape is incomplete and can be misleading. For example, two datasets can have the same mean but completely different distributions.

---

## Part A: Central Tendency (集中趨勢)

### A.1 Mean (平均數)

The sum of all values divided by the number of observations.

$$\bar{x} = \frac{\sum_{i=1}^n x_i}{n}$$

- Uses every data point → **sensitive to outliers**
- Best for symmetric distributions without extreme values

```python
import pandas as pd
from sklearn.datasets import load_iris

df = load_iris(as_frame=True).frame
mean_val = df['sepal length (cm)'].mean()
print(f"Mean: {mean_val:.3f}")
```

**Mean variants — when to use which:**

| Type                | Formula       | When to Use                            | Example                             |
| ------------------- | ------------- | -------------------------------------- | ----------------------------------- |
| **Arithmetic Mean** | Σxᵢ / n       | Default for most situations            | Average exam score                  |
| **Geometric Mean**  | (∏xᵢ)^(1/n)   | Growth rates, ratios, log-normal data  | Average annual return on investment |
| **Harmonic Mean**   | n / Σ(1/xᵢ)   | Averages of rates                      | Average speed over equal distances  |
| **Weighted Mean**   | Σ(wᵢxᵢ) / Σwᵢ | Observations have different importance | GPA, weighted survey results        |

```python
import numpy as np
from scipy.stats import gmean, hmean

values = [2, 4, 8]
weights = [0.2, 0.3, 0.5]

print(f"Arithmetic: {np.mean(values):.3f}")           # 4.667
print(f"Geometric:  {gmean(values):.3f}")              # 4.000
print(f"Harmonic:   {hmean(values):.3f}")              # 3.429
print(f"Weighted:   {np.average(values, weights=weights):.3f}")  # 5.600
```

---

### A.2 Median (中位數)

The middle value when data is sorted. If n is even, it's the average of the two middle values.

- **Robust to outliers** — extreme values don't affect it
- Represents the 50th percentile (Q₂)
- Preferred when data is skewed

```python
median_val = df['sepal length (cm)'].median()
print(f"Median: {median_val:.3f}")
```

---

### A.3 Mode (眾數)

The most frequently occurring value.

- Useful for **discrete** or **categorical** data
- A distribution can be unimodal (1 peak), bimodal (2 peaks), or multimodal (3+ peaks)

> 💡 **Bimodal distribution** often suggests two distinct sub-populations mixed together (e.g., height data from both men and women combined). 如果資料呈現雙峰分佈，通常代表資料中混合了兩個不同的群體。

```python
mode_val = df['sepal length (cm)'].mode()[0]
print(f"Mode: {mode_val:.3f}")
```

---

### A.4 When to Use Which Measure

| Situation                               | Recommended        | Reason                               |
| --------------------------------------- | ------------------ | ------------------------------------ |
| Symmetric distribution, no outliers     | **Mean**           | Uses all data, mathematically stable |
| Skewed distribution                     | **Median**         | Not distorted by extreme values      |
| Data with outliers                      | **Median**         | Resistant to distortion              |
| Categorical or discrete data            | **Mode**           | Mean/Median are not meaningful       |
| Growth rates, investment returns        | **Geometric Mean** | Correct for multiplicative processes |
| Averaging rates (speed, price-per-unit) | **Harmonic Mean**  | Correct for ratio-type averages      |
| Survey with unequal group sizes         | **Weighted Mean**  | Accounts for different group weights |

**The relationship between Mean, Median, and Mode tells you about skew:**

| Distribution Shape                | Relationship             | What It Implies                  |
| --------------------------------- | ------------------------ | -------------------------------- |
| Symmetric                         | Mean ≈ Median ≈ Mode     | Any measure is representative    |
| Right-skewed (right tail is long) | Mode < Median < **Mean** | Mean pulled up by high outliers  |
| Left-skewed (left tail is long)   | **Mean** < Median < Mode | Mean pulled down by low outliers |

> 💡 **Quick check**: If Mean > Median, suspect right skew (common in income, house price data). Report both.

---

## Part B: Variability / Spread (變異性)

### B.1 Range (全距)

$$\text{Range} = \max(x_i) - \min(x_i)$$

- Simplest measure of spread — only uses two data points
- Very sensitive to outliers
- Use as a quick sanity check, not a primary measure

```python
rng = df['sepal length (cm)'].max() - df['sepal length (cm)'].min()
print(f"Range: {rng:.2f}")
```

---

### B.2 Variance (變異數)

The average of squared deviations from the mean.

$$s^2 = \frac{\sum_{i=1}^n (x_i - \bar{x})^2}{n - 1}$$

> 💡 **Why divide by (n−1)?** This is **Bessel's correction** (貝索修正). When estimating population variance from a sample, dividing by (n−1) instead of n corrects for the systematic underestimation that occurs with small samples.

```python
values = df['sepal length (cm)']

var_sample = np.var(values, ddof=1)   # sample: divide by n-1
var_pop    = np.var(values, ddof=0)   # population: divide by n

print(f"Sample Variance:     {var_sample:.4f}")
print(f"Population Variance: {var_pop:.4f}")
```

> ⚠️ Variance is in **squared units** (e.g., cm²), making it hard to interpret directly. Use Standard Deviation for interpretation.

---

### B.3 Standard Deviation (標準差)

$$s = \sqrt{\frac{\sum_{i=1}^n (x_i - \bar{x})^2}{n - 1}}$$

- Same unit as the data → directly interpretable
- Represents the **typical distance** from the mean
- Small SD → data tightly clustered; Large SD → data widely spread

```python
std_sample = np.std(values, ddof=1)
print(f"Standard Deviation: {std_sample:.4f}")
```

**Empirical Rule (68–95–99.7 Rule)** — for normally distributed data:

| Range from Mean | % of Data Covered |
| --------------- | ----------------- |
| ± 1 SD          | ~68%              |
| ± 2 SD          | ~95%              |
| ± 3 SD          | ~99.7%            |

> 💡 Data points beyond ±3 SD are often flagged as outliers in a normal distribution.

```python
mean = values.mean()
std  = np.std(values, ddof=1)

within_1sd = ((values >= mean - std) & (values <= mean + std)).mean()
within_2sd = ((values >= mean - 2*std) & (values <= mean + 2*std)).mean()
print(f"Within ±1 SD: {within_1sd:.1%}")
print(f"Within ±2 SD: {within_2sd:.1%}")
```

---

### B.4 Standard Error (SE) vs Standard Deviation (SD)

> ⚠️ These two are frequently confused. 這兩個非常容易搞混，務必區分清楚。

| Metric                      | Formula           | What It Describes                               | Use When                                     |
| --------------------------- | ----------------- | ----------------------------------------------- | -------------------------------------------- |
| **Standard Deviation (SD)** | √(Σ(xᵢ-x̄)²/(n-1)) | Spread of **individual data points**            | Describing how variable the data is          |
| **Standard Error (SE)**     | SD / √n           | Precision of the **sample mean** as an estimate | Reporting how reliable your mean estimate is |

```python
se = std_sample / np.sqrt(len(values))
print(f"SD: {std_sample:.4f}  ← spread of the data")
print(f"SE: {se:.4f}  ← precision of the mean estimate")
```

> 💡 SE decreases as sample size grows — a larger sample gives a more precise estimate of the population mean. SE 隨樣本數增加而縮小，代表估計越來越可靠。

---

### B.5 Interquartile Range (IQR, 四分位距)

$$\text{IQR} = Q_3 - Q_1$$

- Represents the spread of the **middle 50%** of the data
- **Robust to outliers** — unaffected by extreme values
- The basis of boxplot whiskers

```python
Q1  = values.quantile(0.25)
Q3  = values.quantile(0.75)
IQR = Q3 - Q1
print(f"Q1: {Q1:.3f},  Q3: {Q3:.3f},  IQR: {IQR:.3f}")
```

**Outlier Detection — the 1.5 × IQR Rule:**

$$\text{Lower fence} = Q_1 - 1.5 \times IQR$$
$$\text{Upper fence} = Q_3 + 1.5 \times IQR$$

Data points outside these fences are flagged as potential outliers (this is what boxplot whiskers represent).

```python
lower_fence = Q1 - 1.5 * IQR
upper_fence = Q3 + 1.5 * IQR

outliers = values[(values < lower_fence) | (values > upper_fence)]
print(f"Potential outliers: {outliers.tolist()}")
```

---

### B.6 Coefficient of Variation (CV, 變異係數)

$$CV = \frac{s}{\bar{x}} \times 100\%$$

- **Unit-free** (expressed as a percentage) — allows comparing variability across different variables
- Useful when variables have different units or very different magnitudes
- E.g., comparing variability of salary (NT$) vs. age (years)

```python
cv = (std_sample / values.mean()) * 100
print(f"CV: {cv:.2f}%")
```

| CV     | Interpretation       |
| ------ | -------------------- |
| < 15%  | Low variability      |
| 15–35% | Moderate variability |
| > 35%  | High variability     |

> ⚠️ CV is only meaningful when the mean is **positive** and the variable has a **true zero** (Ratio scale). Don't use CV for temperature in °C or year.

---

### B.7 Variability Measures — Summary

| Measure                | Robust to Outliers? | Units        | Best Used When                              |
| ---------------------- | ------------------- | ------------ | ------------------------------------------- |
| **Range**              | ❌ No               | Same as data | Quick overview, sanity check                |
| **Variance**           | ❌ No               | Squared      | Internal calculations, basis for SD         |
| **Standard Deviation** | ❌ No               | Same as data | Normal-ish data; paired with mean           |
| **Standard Error**     | ❌ No               | Same as data | Reporting precision of the mean             |
| **IQR**                | ✅ Yes              | Same as data | Skewed data or when outliers exist          |
| **CV**                 | ❌ No               | % (unitless) | Comparing spread across different variables |

---

## Part C: Shape of Distribution (分佈形狀)

### C.1 Why Shape Matters

Two datasets can have the **same mean and SD** but completely different shapes. Shape tells you:

- Whether the data is symmetric or skewed
- Whether there are heavy tails with extreme values
- Whether parametric methods (which assume normality) are appropriate

---

### C.2 Skewness (偏態)

Measures the **asymmetry** of the distribution.

$$\text{Skewness} = \frac{\sum (x_i - \bar{x})^3}{(n-1)s^3}$$

| Value          | Shape        | Description                        | Common Example                      |
| -------------- | ------------ | ---------------------------------- | ----------------------------------- |
| ≈ 0            | Symmetric    | Balanced distribution              | Normal distribution                 |
| > 0 (positive) | Right-skewed | Long tail extends to the **right** | Income, house prices, reaction time |
| < 0 (negative) | Left-skewed  | Long tail extends to the **left**  | Exam scores near the maximum        |

> 💡 Right-skewed = 右偏 = 右尾較長 = Mean > Median  
> **Practical threshold**: |Skewness| > 1 is generally considered substantially skewed; consider transformation.

```python
skew_val = df['sepal length (cm)'].skew()
print(f"Skewness: {skew_val:.3f}")
```

---

### C.3 Kurtosis (峰態)

Measures the **tailedness** — how heavy the tails are compared to a normal distribution.

| Type            | Excess Kurtosis | Shape                   | Practical Implication               |
| --------------- | --------------- | ----------------------- | ----------------------------------- |
| **Mesokurtic**  | ≈ 0             | Normal tails            | Behaves like a normal distribution  |
| **Leptokurtic** | > 0             | Heavy tails, sharp peak | More extreme outliers than expected |
| **Platykurtic** | < 0             | Light tails, flat peak  | Fewer extreme values                |

> ⚠️ **Important distinction**: pandas `.kurt()` returns **excess kurtosis** (normal distribution = 0).  
> The raw formula gives kurtosis = 3 for a normal distribution; excess kurtosis subtracts 3 to center it at 0.  
> pandas 的 `.kurt()` 回傳的是 excess kurtosis（正態分佈 = 0），公式中的 raw kurtosis 正態分佈 = 3，兩者不同，注意不要混淆。

```python
kurt_val = df['sepal length (cm)'].kurt()  # excess kurtosis
print(f"Excess Kurtosis: {kurt_val:.3f}")
```

---

### C.4 Visual Normality Check

> ⚠️ Formal normality tests (Shapiro-Wilk, Anderson-Darling) are hypothesis tests — they belong in Inferential Statistics. At the descriptive stage, use **visual methods only**.

**Histogram with KDE:**

```python
import matplotlib.pyplot as plt
import seaborn as sns

sns.histplot(df['sepal length (cm)'], kde=True, color='steelblue')
plt.title('Distribution of Sepal Length')
plt.xlabel('Sepal Length (cm)')
plt.show()
```

**Q–Q Plot (Quantile–Quantile Plot):**

Compares the data's quantiles against a theoretical normal distribution. Points should fall along the diagonal line if the data is normally distributed.

```python
import scipy.stats as stats

fig, ax = plt.subplots()
stats.probplot(df['sepal length (cm)'], dist="norm", plot=ax)
ax.set_title('Q–Q Plot of Sepal Length')
plt.show()
```

| Pattern in Q–Q Plot              | Interpretation               |
| -------------------------------- | ---------------------------- |
| Points along the diagonal        | Data is approximately normal |
| Points curve upward at both ends | Heavy tails (leptokurtic)    |
| S-shaped curve                   | Skewed distribution          |
| Points deviate at one end only   | One-sided tail issue         |

---

### C.5 Full Distribution Summary

Putting it all together — describe a numerical variable with all three dimensions:

```python
col = df['sepal length (cm)']

print("=== Central Tendency ===")
print(f"  Mean:     {col.mean():.3f}")
print(f"  Median:   {col.median():.3f}")
print(f"  Mode:     {col.mode()[0]:.3f}")

print("\n=== Variability ===")
print(f"  Range:    {col.max() - col.min():.3f}")
print(f"  SD:       {col.std():.3f}")
print(f"  IQR:      {col.quantile(0.75) - col.quantile(0.25):.3f}")
print(f"  CV:       {col.std()/col.mean()*100:.2f}%")

print("\n=== Shape ===")
print(f"  Skewness: {col.skew():.3f}")
print(f"  Kurtosis: {col.kurt():.3f}  (excess)")
```

---

### C.6 Practical Guidelines

| Condition           | Recommended Action                    |
| ------------------- | ------------------------------------- | ----- | ----------------------------------------------------------------------- |
|                     | Skewness                              | < 0.5 | Approximately symmetric — use mean + SD                                 |
| 0.5 ≤               | Skewness                              | < 1   | Moderately skewed — report both mean and median                         |
|                     | Skewness                              | ≥ 1   | Substantially skewed — prefer median + IQR; consider log transformation |
| Excess Kurtosis > 2 | Heavy tails — be cautious of outliers |

---

## Part D: Visualization

```python
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# Histogram
axes[0].hist(df['sepal length (cm)'], bins=20, color='steelblue', edgecolor='white')
axes[0].set_title('Histogram')
axes[0].set_xlabel('Sepal Length (cm)')

# Boxplot
axes[1].boxplot(df['sepal length (cm)'])
axes[1].set_title('Boxplot')
axes[1].set_ylabel('Sepal Length (cm)')

# KDE plot
df['sepal length (cm)'].plot(kind='kde', ax=axes[2], color='steelblue')
axes[2].set_title('Density Plot')
axes[2].set_xlabel('Sepal Length (cm)')

plt.tight_layout()
plt.show()
```

| Chart                  | Best For                                                 |
| ---------------------- | -------------------------------------------------------- |
| **Histogram**          | Seeing the overall shape and spread                      |
| **Boxplot**            | Quickly spotting outliers; comparing groups              |
| **KDE (Density Plot)** | Smooth version of histogram; cleaner shape visualization |
| **Q–Q Plot**           | Assessing normality visually                             |

---

## Key Takeaways

| Concept                     | Key Point                                                         |
| --------------------------- | ----------------------------------------------------------------- |
| **Always report all three** | Central tendency alone is insufficient                            |
| **Mean vs Median**          | If Mean ≠ Median, there's skew — report both                      |
| **SD vs SE**                | SD describes data spread; SE describes estimate precision         |
| **IQR over SD**             | When data is skewed or has outliers, IQR is more informative      |
| **CV for comparison**       | Use CV when comparing variability across different-unit variables |
| **Visual first**            | Always plot before interpreting numbers                           |

---

**Next:** [Bivariate Analysis →](./4-bivariate.md)
