# 3. Stationarity

**Stationarity** is the most important concept in classical time series analysis. Most models — ARIMA, VAR, cointegration — are built on the assumption that the series is stationary. Applying them to non-stationary data produces unreliable estimates and spurious results.

> 📌 **為什麼平穩性這麼重要**：非平穩序列的統計性質（均值、變異數）會隨時間改變，這意味著過去的模式不能用來預測未來。更危險的是：對兩個非平穩序列做迴歸，即使兩者毫無關係，也可能得到很高的 R² 和顯著的 p-value — 這就是「偽迴歸」（spurious regression）問題。

---

## 3.1 What Is Stationarity?

A time series is **strictly stationary** if its joint probability distribution does not change over time. In practice, we use the weaker and more testable condition of **weak (covariance) stationarity**:

| Condition                     | Meaning                                              |
| ----------------------------- | ---------------------------------------------------- |
| **Constant mean**             | E[Yₜ] = μ for all t                                 |
| **Constant variance**         | Var(Yₜ) = σ² for all t                              |
| **Constant autocovariance**   | Cov(Yₜ, Yₜ₋ₖ) depends only on lag k, not on t      |

> 💡 The key intuition: a stationary series **looks the same regardless of when you observe it**. It has no trend, no systematic change in variance, and no seasonality (in the strict sense).

---

## 3.2 Visual Identification

Always plot the series before running any formal test. A visual check reveals most non-stationarity instantly.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
n = 200
t = np.arange(n)

# Stationary: white noise
stationary    = np.random.normal(0, 1, n)

# Non-stationary: random walk (no drift)
random_walk   = np.cumsum(np.random.normal(0, 1, n))

# Non-stationary: trend + noise
trend_series  = 0.5 * t + np.random.normal(0, 5, n)

# Non-stationary: growing variance
hetero        = np.random.normal(0, 1 + 0.05 * t, n)

fig, axes = plt.subplots(2, 2, figsize=(12, 7))

axes[0, 0].plot(stationary,   color='seagreen',  linewidth=1)
axes[0, 0].set_title('✅ Stationary — White Noise')

axes[0, 1].plot(random_walk,  color='steelblue', linewidth=1)
axes[0, 1].set_title('❌ Non-Stationary — Random Walk')

axes[1, 0].plot(trend_series, color='tomato',    linewidth=1)
axes[1, 0].set_title('❌ Non-Stationary — Deterministic Trend')

axes[1, 1].plot(hetero,       color='orange',    linewidth=1)
axes[1, 1].set_title('❌ Non-Stationary — Growing Variance')

for ax in axes.flat:
    ax.axhline(0, color='black', linestyle='--', alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## 3.3 Formal Tests for Stationarity

Visual inspection is necessary but not sufficient. Use statistical tests to confirm.

### ADF Test (Augmented Dickey-Fuller)

**H₀: The series has a unit root (non-stationary)**  
**H₁: The series is stationary**

```python
from statsmodels.tsa.stattools import adfuller
import pandas as pd

url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv"
df = pd.read_csv(url, parse_dates=['Month'], index_col='Month').asfreq('MS')
df.columns = ['Passengers']

def adf_report(series, label='Series'):
    result = adfuller(series.dropna(), autolag='AIC')
    print(f"\n{'='*40}")
    print(f"ADF Test — {label}")
    print(f"{'='*40}")
    print(f"Test Statistic : {result[0]:.4f}")
    print(f"p-value        : {result[1]:.4f}")
    print(f"Lags Used      : {result[2]}")
    print(f"Critical Values:")
    for key, val in result[4].items():
        print(f"   {key}: {val:.4f}")
    conclusion = "✅ Stationary (reject H₀)" if result[1] < 0.05 else "❌ Non-Stationary (fail to reject H₀)"
    print(f"Conclusion: {conclusion}")

adf_report(df['Passengers'], 'Original Series')
adf_report(np.log(df['Passengers']).diff(1), 'Log First Difference')
```

> ⚠️ ADF is **biased toward rejecting stationarity** (i.e., biased toward finding a unit root). Always pair it with KPSS for a more complete picture.

---

### KPSS Test (Kwiatkowski-Phillips-Schmidt-Shin)

**H₀: The series is stationary (trend-stationary)**  
**H₁: The series has a unit root (non-stationary)**

> 💡 KPSS has the **opposite null hypothesis** from ADF. This is intentional — using both together gives a more reliable conclusion.

```python
from statsmodels.tsa.stattools import kpss

def kpss_report(series, label='Series', regression='c'):
    result = kpss(series.dropna(), regression=regression, nlags='auto')
    print(f"\n{'='*40}")
    print(f"KPSS Test — {label}")
    print(f"{'='*40}")
    print(f"Test Statistic : {result[0]:.4f}")
    print(f"p-value        : {result[1]:.4f}")
    print(f"Critical Values:")
    for key, val in result[3].items():
        print(f"   {key}: {val:.4f}")
    conclusion = "❌ Non-Stationary (reject H₀)" if result[1] < 0.05 else "✅ Stationary (fail to reject H₀)"
    print(f"Conclusion: {conclusion}")

kpss_report(df['Passengers'], 'Original Series')
kpss_report(np.log(df['Passengers']).diff(1).dropna(), 'Log First Difference')
```

### Interpreting ADF + KPSS Together

| ADF Result       | KPSS Result      | Conclusion                                       |
| ---------------- | ---------------- | ------------------------------------------------ |
| Reject H₀ (p<0.05) | Fail to reject H₀ (p>0.05) | ✅ **Stationary**                 |
| Fail to reject H₀  | Reject H₀        | ❌ **Non-Stationary** (unit root) |
| Reject H₀        | Reject H₀        | ⚠️ **Trend-stationary** — detrend and retest     |
| Fail to reject H₀  | Fail to reject H₀ | ⚠️ **Inconclusive** — check visually            |

---

## 3.4 Making a Series Stationary

### Strategy 1: Differencing (for stochastic trends / random walks)

$$\Delta y_t = y_t - y_{t-1}$$

```python
import numpy as np

log_passengers = np.log(df['Passengers'])

# First difference removes linear trend
diff_1 = log_passengers.diff(1)

# Second difference — rarely needed; only if first diff still non-stationary
diff_2 = log_passengers.diff(1).diff(1)

adf_report(diff_1.dropna(), 'Log + First Difference')
```

> ⚠️ **Don't over-difference.** If d=1 achieves stationarity, don't use d=2. Over-differencing introduces unnecessary MA structure and makes models harder to interpret. A sign of over-differencing: the ACF of the differenced series starts at a large *negative* lag-1 value.

---

### Strategy 2: Log Transformation (for growing variance)

Applies when the variance of the series increases proportionally with its level (multiplicative structure).

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

df['Passengers'].plot(             ax=axes[0], title='Original — Growing Variance',  color='steelblue')
np.log(df['Passengers']).plot(     ax=axes[1], title='Log Transform — Stabilized Variance', color='tomato')

plt.tight_layout()
plt.show()
```

---

### Strategy 3: Box-Cox Transformation (generalized power transform)

The Box-Cox transform finds the optimal power λ to stabilize variance:

$$y_t^{(\lambda)} = \begin{cases} \frac{y_t^\lambda - 1}{\lambda} & \lambda \neq 0 \\ \log(y_t) & \lambda = 0 \end{cases}$$

| λ value | Transformation     |
| ------- | ------------------ |
| 1       | No transformation  |
| 0.5     | Square root        |
| 0       | Log (natural)      |
| −1      | Reciprocal         |

```python
from scipy.stats import boxcox

transformed, lam = boxcox(df['Passengers'])
print(f"Optimal λ = {lam:.4f}")
# λ ≈ 0 → log is optimal; λ ≈ 0.5 → square root is optimal
```

---

## 3.5 Choosing the Right Number of Differences (d)

| Method                          | How It Works                                                           |
| ------------------------------- | ---------------------------------------------------------------------- |
| **ADF + KPSS sequence**         | Difference once, retest; repeat until stationary                       |
| **ACF inspection**              | Slow-decaying ACF → non-stationary; after differencing should drop off quickly |
| **`pmdarima.arima.ndiffs()`**   | Automated test-based selection of d                                    |

```python
from pmdarima.arima import ndiffs

d = ndiffs(np.log(df['Passengers']), test='adf')
print(f"Recommended d = {d}")
```

---

## 3.6 Complete Stationarity Workflow

```
Plot raw series
      ↓
Growing variance? → Log transform (or Box-Cox)
      ↓
Run ADF + KPSS
      ↓
Both say stationary? → ✅ Done
      ↓
Non-stationary → Apply first difference
      ↓
Retest ADF + KPSS
      ↓
Still non-stationary → Second difference (rare)
      ↓
Visually inspect ACF — should decay quickly
```

---

## 3.7 Key Takeaways

| Concept                           | Key Point                                                                        |
| --------------------------------- | -------------------------------------------------------------------------------- |
| **Stationarity = stable statistics** | Constant mean, variance, and autocovariance structure over time              |
| **ADF and KPSS have opposite H₀** | Use both together for reliable conclusions                                      |
| **Differencing removes trend**    | d=1 handles most stochastic trends; d=2 is rare                                 |
| **Log stabilizes variance**       | Use when seasonal amplitude grows proportionally with level                      |
| **Don't over-difference**         | d should be the minimum needed to achieve stationarity                           |
| **Spurious regression is real**   | Regressing two non-stationary series produces meaningless R² — always test first |

---

**← Previous:** [Decomposition](./2-decomposition.md)  
**Next:** [Autocorrelation: ACF & PACF →](./4-autocorrelation.md)
