# Correlation

Correlation measures the strength and direction of the relationship between variables.  
The most common measure is the **Pearson correlation coefficient**, which quantifies the linear association.  
Another important concept is **autocorrelation**, which measures correlation in time series (a variable with its own past values).

---

## Pearson Correlation Coefficient

- **Definition:** Measures the strength and direction of the linear relationship between two continuous variables.
- **Range:**
  - -1 → Perfect negative linear relationship (x increases, y decreases)
  - 0 → No linear relationship
  - +1 → Perfect positive linear relationship (x increases, y increases)

### Formula

\[
r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}
\]

- \(x_i, y_i\): data points
- \(\bar{x}, \bar{y}\): sample means

### Interpretation Guide

| r (absolute value) | Strength of correlation |
| ------------------ | ----------------------- |
| 0.00 – 0.10        | Negligible              |
| 0.10 – 0.30        | Weak                    |
| 0.30 – 0.50        | Moderate                |
| 0.50 – 0.70        | Strong                  |
| 0.70 – 1.00        | Very strong             |

### Python Examples

```python
import pandas as pd
from scipy import stats

# Example data
df = pd.DataFrame({'X': [1, 2, 3, 4, 5],
                   'Y': [2, 4, 5, 4, 5]})

# Method 1: SciPy
corr, p_value = stats.pearsonr(df['X'], df['Y'])
print("Pearson r:", corr, "p-value:", p_value)

# Method 2: Pandas (pairwise correlation)
print(df['X'].corr(df['Y']))

# Method 3: Full correlation matrix
print(df.corr())
```

## Autocorrelation

### Definition

Correlation of a variable with its own lagged values (time series).

### Interpretation

- **Negative autocorrelation** → Mean reversion
- **Positive autocorrelation** → Momentum / trend-following

### Formula (lag k autocorrelation)

\[
\rho*k = \frac{\sum*{t=k+1}^n (x*t - \bar{x})(x*{t-k} - \bar{x})}{\sum\_{t=1}^n (x_t - \bar{x})^2}
\]

- \(x_t\): value at time \(t\)
- \(\bar{x}\): mean of the series
- \(k\): lag (number of steps back in time)

---

### Example (basic)

```python
# Autocorrelation of a single column
autocorr_val = df['X'].autocorr()
print("Autocorrelation:", autocorr_val)
```

### Time Series Example

```python
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

## Summary

- Pearson correlation → measures linear relationship between two continuous variables.
- Autocorrelation → measures correlation of a variable with itself over time (important in time series).
