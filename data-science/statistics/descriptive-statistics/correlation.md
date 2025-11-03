# Correlation

**Correlation** measures the strength and direction of the relationship between two or more variables. It helps describe whether changes in one variable are associated with changes in another.

The most common measure is the **Pearson correlation coefficient**, which quantifies linear relationships between continuous variables. Other variants (Spearman, Kendall) are used for ranked or non-linear relationships.

## 1. Pearson Correlation Coefficient

### Definition

Measures the **strength and direction** of the linear relationship between two continuous variables.

$$
r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}
$$

- (x_i, y_i): data points
- (\bar{x}, \bar{y}): sample means

### Interpretation

| r   | Relationship Type      | Description                                        |
| --- | ---------------------- | -------------------------------------------------- |
| +1  | Perfect positive       | As X increases, Y increases exactly proportionally |
| 0   | No linear relationship | X and Y change independently                       |
| −1  | Perfect negative       | As X increases, Y decreases exactly proportionally |

|           |             |                          |                             |             |
| --------- | ----------- | ------------------------ | --------------------------- | ----------- |
| \*\*      | r           | range\*\*                | **Strength of correlation** | **Example** |
| 0.00–0.10 | Negligible  | Random noise             |                             |             |
| 0.10–0.30 | Weak        | Slight trend             |                             |             |
| 0.30–0.50 | Moderate    | Clear tendency           |                             |             |
| 0.50–0.70 | Strong      | Consistent trend         |                             |             |
| 0.70–1.00 | Very strong | Nearly perfect alignment |                             |             |

### Python Example

```python
import pandas as pd
from scipy import stats

# Example data
X = [1, 2, 3, 4, 5]
Y = [2, 4, 5, 4, 5]

# Method 1: SciPy
corr, p_value = stats.pearsonr(X, Y)
print(f"Pearson r = {corr:.3f}, p = {p_value:.3f}")

# Method 2: Pandas
import pandas as pd
df = pd.DataFrame({'X': X, 'Y': Y})
print(df.corr())
```

## 2. Coefficient of Determination (R²)

### Definition

**R² (R-squared)** measures the proportion of variance in one variable that is explained by another variable in a linear model.

$$
R^2 = r^2, \text{ where } r = \text{ Pearson correlation coefficient }
$$

### Interpretation

| R²  | Explanation    | Meaning                                     |
| --- | -------------- | ------------------------------------------- |
| 0   | No explanation | The predictor explains none of the variance |
| 0.5 | Moderate fit   | 50% of variance explained                   |
| 1   | Perfect fit    | All variance explained                      |

**Example:** If (r = 0.8), then (R^2 = 0.64). 64% of the variation in Y is explained by X.

```python
r = df['X'].corr(df['Y'])
R2 = r ** 2
print(f"R² = {R2:.2f}")
```

**Key notes:**

- R² measures **goodness of fit**, not causation.
- Non-linear relationships can have low R² even if strongly associated.

## 3. Spearman and Kendall Rank Correlations

### Spearman’s ρ (rho)

- Based on **ranked data** (ordinal or non-normal).
- Detects **monotonic** (not necessarily linear) relationships.

```python
rho, p = stats.spearmanr(X, Y)
print(f"Spearman rho = {rho:.3f}, p = {p:.3f}")
```

### Kendall’s τ (tau)

- Measures rank correlation using concordant and discordant pairs.
- More robust for small samples or many ties.

```python
tau, p = stats.kendalltau(X, Y)
print(f"Kendall tau = {tau:.3f}, p = {p:.3f}")
```

| Method         | Data Type          | Detects                 | Robustness              |
| -------------- | ------------------ | ----------------------- | ----------------------- |
| **Pearson r**  | Continuous, normal | Linear relationships    | Sensitive to outliers   |
| **Spearman ρ** | Ordinal, skewed    | Monotonic relationships | Robust to non-normality |
| **Kendall τ**  | Ordinal, small n   | Monotonic relationships | Robust to ties          |

## 4. Autocorrelation (Serial Correlation)

### Definition

**Autocorrelation** measures correlation of a variable with its own lagged values — important in **time series** analysis.

$$
\rho_k = \frac{\sum_{t=k+1}^n (x_t - \bar{x})(x_{t-k} - \bar{x})}{\sum_{t=1}^n (x_t - \bar{x})^2}
$$

- $x_t$: value at time t
- $k$: lag (steps back in time)

### Interpretation

- Positive autocorrelation → momentum/trend-following.
- Negative autocorrelation → mean reversion.

### Python Example

```python
import pandas as pd

# Example time series
df = pd.DataFrame({'Price': [100, 102, 101, 105, 107]})

df['Return'] = df['Price'].pct_change()
autocorr = df['Return'].autocorr()
print(f"Autocorrelation = {autocorr:.3f}")
```

```python
# Time Series Example

import pandas as pd

# Example time series DataFrame
df = pd.DataFrame({'Price': [100, 102, 101, 105, 107]},
                  index=pd.date_range("2023-01-01", periods=5, freq="D"))

# Convert index to datetime
df.index = pd.to_datetime(df.index)

# Downsample from daily to monthly data
df = df.resample(rule='M').last()

# Compute returns from prices
df['Return'] = df['Price'].pct_change()

# Compute autocorrelation of returns
autocorrelation = df['Return'].autocorr()
print("The autocorrelation is:", autocorrelation)
```

## 5. Visualization

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.lmplot(x='X', y='Y', data=df)
plt.title('Scatter Plot with Regression Line')
plt.show()
```

- Points near the line → strong correlation.
- Scattered points → weak correlation.

## 6. Key Takeaways

- **Correlation ≠ causation** — a strong correlation does not imply one variable causes the other.
- **Pearson r** is ideal for linear, continuous, and normally distributed data.
- **Spearman ρ** and **Kendall τ** handle non-normal or ordinal data.
- **R²** expresses the proportion of variance explained by the relationship.
- **Autocorrelation** detects patterns within time-dependent data.
- If the relationship is not linear, consider [**transformation**](../../python-foundations/numpy/statistics.md#transformations).
