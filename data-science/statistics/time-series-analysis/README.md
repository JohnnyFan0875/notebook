# Time Series Analysis

**Time series analysis** is the study of data collected sequentially over time. Unlike cross-sectional data, time series observations are **not independent** — what happened yesterday influences what happens today. This temporal dependence is both the defining challenge and the greatest source of insight.

Key point: In time series, order matters. You cannot shuffle observations or ignore temporal dependence, because the whole point is to learn what the past says about the future.

## Why This Order?

The sections follow a natural time series workflow:

```
Understand the structure of time series data
        ↓
Decompose: Trend + Seasonality + Residual
        ↓
Check stationarity — transform if needed
        ↓
Model the dependence structure (AR, MA, ARIMA)
        ↓
Handle seasonality (SARIMA, STL)
        ↓
Evaluate forecasts and diagnose residuals
```

This order matters because **most time series models assume stationarity**. Skipping decomposition and stationarity testing before modeling is one of the most common mistakes in practice.

## Overview of Topics

| Section | Level | Key Questions Answered |
| ------------------------------------------------------------------------ | ----------- | -------------------------------------------------------------------- |
| [**Time Series Fundamentals**](./fundamentals.md) | Foundation | What is a time series? What are its components? How do I load and plot it? |
| [**Decomposition**](./decomposition.md) | Foundation | How do I separate trend, seasonality, and noise? |
| [**Stationarity**](./stationarity.md) | Core | Is my series stationary? How do I test and transform it? |
| [**Autocorrelation: ACF & PACF**](./autocorrelation.md) | Core | How does the past correlate with the present? How do I read ACF/PACF plots? |
| [**ARIMA Models**](./arima.md) | Modeling | How do I fit AR, MA, and ARIMA models? How do I choose orders? |
| [**Seasonality & SARIMA**](./seasonality-sarima.md) | Modeling | How do I handle regular seasonal patterns? |
| [**Forecast Evaluation**](./forecast-evaluation.md) | Evaluation | How do I measure forecast accuracy? How do I diagnose residuals? |

## What's Inside Each Section

### Time Series Fundamentals

- What distinguishes time series from cross-sectional data
- The four components: Trend, Seasonality, Cyclicality, Irregular
- Loading, indexing, and resampling with pandas DatetimeIndex
- Plotting conventions and visual inspection

### Decomposition

Two decomposition models:

| Model | Formula | When to Use |
| --------------- | --------------------------------- | ----------------------------------- |
| **Additive** | Y = Trend + Seasonal + Residual | Seasonal variation is roughly constant |
| **Multiplicative** | Y = Trend × Seasonal × Residual | Seasonal variation grows with level |

Methods: Classical decomposition, STL (Seasonal-Trend using Loess)

### Stationarity

- What stationarity means (constant mean, variance, autocorrelation)
- Why it matters for ARIMA and most classical models
- Tests: ADF, KPSS
- Transformations: differencing, log transform, Box-Cox

### Autocorrelation: ACF & PACF

The two key diagnostic plots for time series:

| Plot | What It Shows | Use For |
| -------- | -------------------------------------------------- | --------------------------- |
| **ACF** | Correlation of series with its own lags | Identifying MA order (q) |
| **PACF** | Partial correlation after removing intermediate lags | Identifying AR order (p) |

### ARIMA Models

The core classical time series framework:

| Component | Name | Controls |
| --------- | --------------------- | ---------------------------- |
| **AR(p)** | Autoregressive | How many past values to use |
| **I(d)** | Integrated (differencing) | How many times to difference |
| **MA(q)** | Moving Average | How many past errors to use |

### Seasonality & SARIMA

- SARIMA(p,d,q)(P,D,Q)[m]: adding seasonal AR, I, and MA terms
- STL decomposition for flexible seasonality handling
- Prophet for automatic trend + seasonality modeling

### Forecast Evaluation

Error metrics and diagnostic tools:

| Metric | Full Name | Interpretation |
| -------- | ------------------------------ | ------------------------------ |
| **MAE** | Mean Absolute Error | Average absolute deviation |
| **RMSE** | Root Mean Squared Error | Penalizes large errors heavily |
| **MAPE** | Mean Absolute Percentage Error | Scale-free; easy to communicate |
| **AIC / BIC** | Information Criteria | Model selection (lower = better) |

## Visualization Quick Reference

| Chart | Best For |
| ------------------------- | ----------------------------------------------------- |
| Line plot | Raw series — trend and seasonality inspection |
| Decomposition plot | Separating trend, seasonal, and residual components |
| ACF plot | Identifying moving average order; checking stationarity |
| PACF plot | Identifying autoregressive order |
| Forecast plot with CI | Communicating predictions with uncertainty |
| Residual diagnostic plot | Checking model assumptions after fitting |

## Tools Used in This Module

| Library | Purpose |
| ---------------- | ---------------------------------------------------- |
| `pandas` | Time series indexing, resampling, rolling statistics |
| `numpy` | Numerical computation |
| `matplotlib` / `seaborn` | Visualization |
| `statsmodels` | ARIMA, SARIMA, decomposition, ADF/KPSS tests |
| `pmdarima` | Auto ARIMA order selection |
| `prophet` | Additive trend + seasonality modeling (Meta) |
| `sklearn` | Error metrics for forecast evaluation |

## Key Takeaway

Time series analysis answers: "What patterns exist in this sequence, and what will likely come next?" Always visualize before modeling, always test stationarity before fitting ARIMA, and always evaluate on held-out data — never on the training period.

## Deep-Study Priorities

The most useful path through this module is:

1. visualize the raw series
2. understand components and stationarity
3. read ACF / PACF and differencing
4. fit ARIMA / SARIMA only after preprocessing
5. evaluate on a chronological split

Tip: In time series, preprocessing choices are part of the model, not a separate cleanup stage.
