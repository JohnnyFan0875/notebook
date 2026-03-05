# 1. Time Series Fundamentals

A **time series** is a sequence of observations indexed in time order. The defining property is that **the order of observations matters** — you cannot shuffle them without destroying information.

> 📌 **為什麼時間序列特殊**：一般統計假設觀測值彼此獨立（i.i.d.）。時間序列違反這個假設：昨天的股價影響今天的股價，上個月的銷售量影響這個月的庫存。這個「時間依賴性」既是挑戰，也是我們能夠預測的原因。

---

## 1.1 The Four Components of a Time Series

Every time series can be thought of as a combination of four underlying components:

| Component         | 中文   | Description                                          | Example                                        |
| ----------------- | ------ | ---------------------------------------------------- | ---------------------------------------------- |
| **Trend (T)**     | 趨勢   | Long-run upward or downward direction                | Rising global temperatures, growing user base  |
| **Seasonality (S)** | 季節性 | Regular, periodic patterns at fixed frequency      | Holiday sales spikes every December            |
| **Cyclicality (C)** | 循環性 | Irregular long-run fluctuations — no fixed period  | Business cycles (expansion/recession)          |
| **Irregular (I)** | 不規則 | Random noise; unexplained variation                  | A one-off event, measurement error             |

> 💡 **Seasonality vs Cyclicality**: Seasonality repeats at a known, fixed period (weekly, monthly, yearly). Cyclicality has no fixed period — business cycles might last 3 years or 10 years. In practice, most classical models handle seasonality explicitly but treat cyclicality as part of the trend.  
> 季節性有固定週期，循環性沒有。兩者常被混淆，但對建模策略影響很大。

---

## 1.2 Loading and Indexing Time Series in pandas

A proper **DatetimeIndex** is essential. It enables resampling, slicing, rolling windows, and frequency inference.

```python
import pandas as pd
import matplotlib.pyplot as plt

# Example: load monthly airline passenger data
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv"
df = pd.read_csv(url, parse_dates=['Month'], index_col='Month')
df.columns = ['Passengers']

print(df.head())
print(f"\nFrequency: {df.index.freq}")
print(f"Date range: {df.index.min()} to {df.index.max()}")
print(f"Shape: {df.shape}")
```

**Setting or inferring frequency:**

```python
# If frequency isn't set automatically, set it manually
df = df.asfreq('MS')  # MS = month start frequency

# Common frequency strings
# 'D'   — calendar day
# 'B'   — business day
# 'W'   — weekly
# 'MS'  — month start
# 'ME'  — month end
# 'QS'  — quarter start
# 'YS'  — year start
# 'h'   — hourly
# 'min' — minute
```

> ⚠️ Always set or verify the frequency. If pandas can't infer it, most statsmodels functions will raise an error or produce incorrect results.  
> 沒有正確設定時間頻率，statsmodels 的模型幾乎一定會出錯。這是最常見的環境問題。

---

## 1.3 Simulating a Time Series from Scratch

Understanding components is easier when we build them up manually:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
n = 120  # 10 years of monthly data

t = np.arange(n)
dates = pd.date_range(start='2014-01', periods=n, freq='MS')

# Components
trend      = 100 + 0.8 * t
seasonality = 20 * np.sin(2 * np.pi * t / 12)
noise      = np.random.normal(0, 5, n)

series = trend + seasonality + noise

df = pd.Series(series, index=dates, name='Value')

# Plot each component
fig, axes = plt.subplots(4, 1, figsize=(11, 9), sharex=True)

axes[0].plot(dates, series,      color='steelblue',  linewidth=1.5)
axes[0].set_title('Observed Series (Trend + Seasonality + Noise)')

axes[1].plot(dates, trend,       color='tomato',     linewidth=1.5)
axes[1].set_title('Trend Component')

axes[2].plot(dates, seasonality, color='seagreen',   linewidth=1.5)
axes[2].set_title('Seasonal Component')

axes[3].plot(dates, noise,       color='gray',       linewidth=1, alpha=0.8)
axes[3].set_title('Irregular (Noise) Component')

plt.tight_layout()
plt.show()
```

---

## 1.4 Essential Time Series Operations in pandas

### Resampling

Change the frequency of the data by aggregating (downsampling) or interpolating (upsampling).

```python
# Load daily data, resample to monthly
# (using airline data already at monthly; demonstrated conceptually)
df_monthly = df.resample('QS').mean()   # quarterly average
df_annual  = df.resample('YS').sum()    # annual total
```

### Rolling Statistics

Compute statistics over a sliding window — useful for smoothing and detecting local trends.

```python
# 12-month rolling mean and standard deviation
rolling_mean = df['Passengers'].rolling(window=12, center=True).mean()
rolling_std  = df['Passengers'].rolling(window=12, center=True).std()

plt.figure(figsize=(10, 4))
plt.plot(df['Passengers'],  label='Original',      color='steelblue', alpha=0.6)
plt.plot(rolling_mean,       label='Rolling Mean (12)', color='tomato',    linewidth=2)
plt.fill_between(df.index,
                 rolling_mean - rolling_std,
                 rolling_mean + rolling_std,
                 alpha=0.15, color='tomato', label='±1 Rolling SD')
plt.title('Rolling Statistics — Airline Passengers')
plt.legend()
plt.tight_layout()
plt.show()
```

### Lag and Shift

Create lagged versions of the series — fundamental for building AR models and computing autocorrelation.

```python
df['lag_1']  = df['Passengers'].shift(1)   # previous month
df['lag_12'] = df['Passengers'].shift(12)  # same month last year

print(df[['Passengers', 'lag_1', 'lag_12']].head(15))
```

### Differencing

Subtract consecutive observations to remove trend. First difference: Δyₜ = yₜ − yₜ₋₁.

```python
df['diff_1']  = df['Passengers'].diff(1)   # first difference
df['diff_12'] = df['Passengers'].diff(12)  # seasonal difference (lag 12)

fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
df['Passengers'].plot(ax=axes[0], title='Original Series',         color='steelblue')
df['diff_1'].plot(    ax=axes[1], title='First Difference (d=1)',  color='tomato')
df['diff_12'].plot(   ax=axes[2], title='Seasonal Difference (D=1, m=12)', color='seagreen')
plt.tight_layout()
plt.show()
```

---

## 1.5 First Look: Visual Inspection Checklist

Before any modeling, always plot the raw series and ask:

| Question                                    | What to Look For                              | Why It Matters                            |
| ------------------------------------------- | --------------------------------------------- | ----------------------------------------- |
| Is there a trend?                           | Upward or downward drift over time            | May need differencing or detrending       |
| Is there seasonality?                       | Regular repeating patterns                    | Need seasonal model (SARIMA) or decomposition |
| Is the variance growing over time?          | Wider oscillations as level increases         | Suggests multiplicative model or log transform |
| Are there structural breaks or outliers?    | Sudden level shifts, spikes                   | May need intervention variables or robust methods |
| Is the series relatively smooth or noisy?  | High-frequency noise vs clear patterns        | Informs smoothing and model complexity   |

```python
# Quick visual inspection
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Raw series
df['Passengers'].plot(ax=axes[0,0], title='Raw Series', color='steelblue')

# Log transform — stabilizes variance
np.log(df['Passengers']).plot(ax=axes[0,1], title='Log Transform', color='tomato')

# First difference of log
np.log(df['Passengers']).diff(1).plot(ax=axes[1,0], title='Log + First Diff', color='seagreen')

# Seasonal diff of log first diff
np.log(df['Passengers']).diff(1).diff(12).plot(
    ax=axes[1,1], title='Log + First Diff + Seasonal Diff', color='orange')

plt.tight_layout()
plt.show()
```

> 💡 **Log + differencing** is one of the most common preprocessing pipelines for economic and business time series with growing variance. It often converts a non-stationary multiplicative series into something approximately stationary.

---

## 1.6 Key Takeaways

| Concept                        | Key Point                                                                         |
| ------------------------------ | --------------------------------------------------------------------------------- |
| **Observations are ordered**   | Time series data cannot be shuffled — temporal dependence is the core property    |
| **Four components**            | Trend, Seasonality, Cyclicality, Irregular — understand which are present         |
| **DatetimeIndex is essential** | Set `parse_dates` and `asfreq()` before doing anything else                       |
| **Rolling stats smooth noise** | Use rolling mean/SD for trend visualization and anomaly detection                 |
| **Differencing removes trend** | First difference removes linear trend; seasonal difference removes annual pattern |
| **Visual inspection first**    | Always plot raw series before choosing transformations or models                  |

---

**Next:** [Decomposition →](./2-decomposition.md)
