# Seasonality & SARIMA

Many real-world time series exhibit **seasonal patterns** — regular, predictable fluctuations that repeat at a fixed period. Monthly retail sales peak in December, weekly website traffic dips on weekends, daily power demand spikes at noon. A standard ARIMA model ignores this structure. **SARIMA** extends ARIMA to handle it explicitly.

Key point: Seasonality is one of the most common patterns in time series: if your data has obvious cyclical repeats and you do not use a seasonal model, there will be a lot of exploitable structure in the residuals. SARIMA is the most important classical method for processing seasonal time series.

## Identifying Seasonality

Before choosing a model, confirm that seasonality is present and determine its period m.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv"
df = pd.read_csv(url, parse_dates=['Month'], index_col='Month').asfreq('MS')
df.columns = ['Passengers']

# Method 1: Seasonal subseries plot
df['Month_num'] = df.index.month
df['Year']      = df.index.year

fig, ax = plt.subplots(figsize=(10, 4))
for year, group in df.groupby('Year'):
    ax.plot(group['Month_num'], group['Passengers'],
            alpha=0.5, color='steelblue', linewidth=1)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun',
                    'Jul','Aug','Sep','Oct','Nov','Dec'])
ax.set_title('Seasonal Subseries Plot — Each Line = One Year')
ax.set_ylabel('Passengers (thousands)')
plt.tight_layout()
plt.show()

# Method 2: Boxplot by month
import seaborn as sns
fig, ax = plt.subplots(figsize=(10, 4))
sns.boxplot(x='Month_num', y='Passengers', data=df, ax=ax, palette='Set2')
ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun',
                    'Jul','Aug','Sep','Oct','Nov','Dec'])
ax.set_title('Monthly Distribution of Passenger Counts')
plt.tight_layout()
plt.show()
```

Tip: The subseries plot shows the within-year pattern (which months are high/low) as well as the year-over-year trend (is the pattern growing?). If each month's lines trend upward together, you likely need a multiplicative model.

## SARIMA: Adding Seasonal Terms

**SARIMA(p, d, q)(P, D, Q)[m]** extends ARIMA by adding a second set of AR, I, and MA terms that operate at the **seasonal lag** (multiples of m).

| Parameter | Level | Controls |
| --------- | --------- | -------------------------------------------- |
| p | Non-seasonal | AR order — lags 1 to p |
| d | Non-seasonal | Differencing order |
| q | Non-seasonal | MA order — lags 1 to q |
| P | Seasonal | Seasonal AR order — lags m, 2m, ..., Pm |
| D | Seasonal | Seasonal differencing order |
| Q | Seasonal | Seasonal MA order — lags m, 2m, ..., Qm |
| **m** | — | **Seasonal period** (12 for monthly, 7 for daily, 4 for quarterly) |

**The full SARIMA model equation:**

\[
\Phi_P(B^m) \phi_p(B) (1-B)^d (1-B^m)^D y_t = \Theta_Q(B^m) \theta_q(B) \varepsilon_t
\]

Tip: Don't be intimidated by the notation. In practice: fit SARIMA(p,d,q)(P,D,Q)[m] where m is your seasonal period, and let the ACF/PACF at seasonal lags guide P and Q.

## Seasonal ACF/PACF: Reading the Seasonal Structure

After seasonal differencing, look for spikes at **multiples of m** in the ACF and PACF:

```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Apply log + first difference + seasonal difference (m=12)
log_pass    = np.log(df['Passengers'])
diff_series = log_pass.diff(1).diff(12).dropna()

fig, axes = plt.subplots(2, 1, figsize=(11, 8))
plot_acf( diff_series, lags=48, ax=axes[0], alpha=0.05)
plot_pacf(diff_series, lags=48, ax=axes[1], alpha=0.05, method='ywm')
axes[0].set_title('ACF — Log + Diff(1) + Seasonal Diff(12)')
axes[1].set_title('PACF — Log + Diff(1) + Seasonal Diff(12)')
for ax in axes:
    for lag in [12, 24, 36, 48]:
        ax.axvline(lag, color='tomato', linestyle=':', alpha=0.5)
plt.tight_layout()
plt.show()
```

**Reading seasonal lags in ACF/PACF:**

| Location of Spike | Look At | Suggests |
| ---------------------------- | -------- | --------------------------------- |
| Spike at lag m (e.g., 12) | ACF | Seasonal MA term (Q=1) |
| Spike at lag m in PACF | PACF | Seasonal AR term (P=1) |
| Spikes at m, 2m in ACF | ACF | Possible Q=2 (or slow seasonal decay → P>0) |
| No significant seasonal lags | Both | Seasonal differencing was sufficient |

## Fitting SARIMA with statsmodels

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
warnings.filterwarnings('ignore')

log_pass = np.log(df['Passengers'])

# SARIMA(1,1,1)(1,1,1)[12] — a common starting point for monthly data
model = SARIMAX(
    log_pass,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12),
    enforce_stationarity=False,
    enforce_invertibility=False
)
result = model.fit(disp=False)

print(result.summary())
print(f"\nAIC: {result.aic:.2f}")
print(f"BIC: {result.bic:.2f}")
```

## Automatic Seasonal Order Selection

```python
from pmdarima import auto_arima

auto_model = auto_arima(
    log_pass,
    m=12,                 # monthly seasonality
    d=1, D=1,             # fix non-seasonal and seasonal differencing
    start_p=0, max_p=3,
    start_q=0, max_q=3,
    start_P=0, max_P=2,
    start_Q=0, max_Q=2,
    seasonal=True,
    information_criterion='aic',
    stepwise=True,
    trace=True
)

print(f"\nSelected: SARIMA{auto_model.order}{auto_model.seasonal_order}")
```

## Forecasting with SARIMA

```python
forecast_steps = 36   # 3 years ahead
forecast = result.get_forecast(steps=forecast_steps)
fc_mean  = np.exp(forecast.predicted_mean)
fc_ci    = np.exp(forecast.conf_int(alpha=0.05))

fig, ax = plt.subplots(figsize=(12, 5))
df['Passengers'].plot(ax=ax, label='Observed', color='steelblue', linewidth=1.5)
fc_mean.plot(ax=ax, label='SARIMA Forecast', color='tomato', linewidth=2)
ax.fill_between(fc_ci.index, fc_ci.iloc[:,0], fc_ci.iloc[:,1],
                color='tomato', alpha=0.2, label='95% CI')
ax.set_title('SARIMA(1,1,1)(1,1,1)[12] — Airline Passenger Forecast')
ax.set_ylabel('Passengers (thousands)')
ax.legend()
plt.tight_layout()
plt.show()
```

## Alternative: STL + ARIMA (STL Forecasting)

A powerful modern alternative: decompose with STL, then model the seasonally-adjusted series with ARIMA, and forecast the seasonal component separately.

```python
from statsmodels.tsa.forecasting.stl import STLForecast

stl_forecast = STLForecast(
    log_pass,
    ARIMA,
    model_kwargs=dict(order=(1, 1, 0)),
    period=12
)
stl_result = stl_forecast.fit(disp=False)

forecast_stl = stl_result.forecast(36)
fc_stl_exp   = np.exp(forecast_stl)

fig, ax = plt.subplots(figsize=(12, 5))
df['Passengers'].plot(ax=ax, label='Observed', color='steelblue', linewidth=1.5)
fc_stl_exp.plot(ax=ax, label='STL + ARIMA Forecast', color='seagreen', linewidth=2)
ax.set_title('STL + ARIMA Forecast — Airline Passengers')
ax.set_ylabel('Passengers (thousands)')
ax.legend()
plt.tight_layout()
plt.show()
```

Tip: STL + ARIMA vs SARIMA: STL handles non-linear and evolving seasonal patterns better than SARIMA's rigid multiplicative/additive structure. For complex seasonality, STL + ARIMA often outperforms SARIMA.

## Handling Multiple Seasonalities: Prophet

When data has **more than one seasonal period** (e.g., daily data with both weekly and yearly cycles), SARIMA becomes impractical. Meta's **Prophet** library is designed for this.

```python
from prophet import Prophet
import pandas as pd

# Prophet requires columns 'ds' (datetime) and 'y' (values)
prophet_df = df[['Passengers']].reset_index()
prophet_df.columns = ['ds', 'y']

model_prophet = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,  # monthly data — no weekly cycle
    daily_seasonality=False,
    seasonality_mode='multiplicative'  # because variance grows with level
)
model_prophet.fit(prophet_df)

future   = model_prophet.make_future_dataframe(periods=36, freq='MS')
forecast_p = model_prophet.predict(future)

model_prophet.plot(forecast_p)
plt.title('Prophet Forecast — Airline Passengers')
plt.tight_layout()
plt.show()

model_prophet.plot_components(forecast_p)
plt.tight_layout()
plt.show()
```

**Prophet strengths and limitations:**

| Strength | Limitation |
| ---------------------------------------- | --------------------------------------------- |
| Automatic multiple seasonality handling | Less interpretable than ARIMA |
| Handles holidays and special events | Requires sufficient history |
| Robust to missing data and outliers | May overfit short series |
| Easy to use without ACF/PACF expertise | Less suitable for high-frequency financial data |

## Choosing a Seasonal Model

| Scenario | Recommended Model |
| ------------------------------------------- | ----------------------------------------- |
| Monthly/quarterly data, one seasonal period | **SARIMA** |
| Complex or evolving seasonality | **STL + ARIMA** |
| Multiple seasonal periods (weekly + yearly) | **Prophet** or **MSTL + ARIMA** |
| Few data points, strong prior knowledge | **Prophet** with custom seasonality |
| Interpretability required | **SARIMA** or **STL + ARIMA** |

## Key Takeaways

| Concept | Key Point |
| --------------------------------- | ---------------------------------------------------------------------------------- |
| **Seasonal period m is critical** | Always identify m correctly before fitting (12 for monthly, 4 for quarterly, etc.) |
| **Seasonal differencing (D=1)** | Removes the seasonal unit root; usually needed alongside regular differencing |
| **Seasonal ACF/PACF at lag m** | Spikes at m in ACF → Q=1; spikes at m in PACF → P=1 |
| **SARIMA notation** | (p,d,q)(P,D,Q)[m] — two sets of parameters at two time scales |
| **STL + ARIMA is more flexible** | Better for non-linear or evolving seasonal patterns |
| **Prophet for multiple seasons** | When data has daily + weekly + yearly seasonality, SARIMA is impractical |

## Seasonal vs. Non-seasonal Orders

Keep these roles separate:

- `(p, d, q)` models short-range non-seasonal structure
- `(P, D, Q)[m]` models repeated seasonal structure

Tip: Confusing these roles is one of the fastest ways to overcomplicate a SARIMA model.
