# 5. ARIMA Models

**ARIMA (Autoregressive Integrated Moving Average)** is the workhorse of classical time series forecasting. It combines three mechanisms — autoregression, differencing, and moving average — into a single unified model that can handle a wide range of stationary and non-stationary time series.

> 📌 **ARIMA 是三個想法的組合**：AR（用過去的值預測現在）+ I（用差分消除趨勢）+ MA（用過去的誤差修正預測）。理解每個成分的直覺，比死背參數選擇規則更重要。

---

## 5.1 The Three Components

### AR(p) — Autoregressive

The current value is a linear combination of the past p values:

$$y_t = c + \phi_1 y_{t-1} + \phi_2 y_{t-2} + \cdots + \phi_p y_{t-p} + \varepsilon_t$$

- φᵢ = autoregressive coefficients
- p = order (how many past values to use)
- Like a regression where the **predictors are lagged versions of the same series**

### MA(q) — Moving Average

The current value depends on the current and past q forecast errors:

$$y_t = \mu + \varepsilon_t + \theta_1 \varepsilon_{t-1} + \theta_2 \varepsilon_{t-2} + \cdots + \theta_q \varepsilon_{t-q}$$

- θᵢ = moving average coefficients
- q = order (how many past errors to use)
- Not the same as a rolling average — it's a **regression on past forecast errors**

> ⚠️ The MA in ARIMA is different from the "moving average" used in smoothing. In ARIMA, MA terms model the dependence on past *errors* (shocks), not past *values*.  
> ARIMA 的 MA 項是對過去誤差的迴歸，不是平滑用的移動平均。兩者名稱相同但概念不同。

### I(d) — Integrated

The degree of differencing applied to make the series stationary:

- d=0: series is already stationary
- d=1: first difference Δyₜ = yₜ − yₜ₋₁
- d=2: second difference Δ²yₜ = Δyₜ − Δyₜ₋₁ (rare)

---

## 5.2 ARIMA(p, d, q) Notation

| Parameter | Meaning                       | Determined By            |
| --------- | ----------------------------- | ------------------------ |
| **p**     | AR order                      | PACF plot cut-off        |
| **d**     | Differencing order            | ADF/KPSS test result     |
| **q**     | MA order                      | ACF plot cut-off         |

---

## 5.3 Manual Order Selection Using ACF/PACF

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv"
df = pd.read_csv(url, parse_dates=['Month'], index_col='Month').asfreq('MS')
df.columns = ['Passengers']

# Step 1: Transform to stabilize variance
log_pass = np.log(df['Passengers'])

# Step 2: First difference to achieve stationarity (d=1)
diff_series = log_pass.diff(1).dropna()

# Step 3: Read ACF and PACF to choose p and q
fig, axes = plt.subplots(2, 1, figsize=(10, 7))
plot_acf( diff_series, lags=24, ax=axes[0], alpha=0.05)
plot_pacf(diff_series, lags=24, ax=axes[1], alpha=0.05, method='ywm')
axes[0].set_title('ACF of Log First-Differenced Series → q order hint')
axes[1].set_title('PACF of Log First-Differenced Series → p order hint')
plt.tight_layout()
plt.show()
```

**Decision guide from ACF/PACF:**

| ACF                     | PACF                    | Model Suggestion        |
| ----------------------- | ----------------------- | ----------------------- |
| Cuts off at lag 1       | Decays                  | MA(1): ARIMA(0,d,1)     |
| Cuts off at lag 2       | Decays                  | MA(2): ARIMA(0,d,2)     |
| Decays                  | Cuts off at lag 1       | AR(1): ARIMA(1,d,0)     |
| Decays                  | Cuts off at lag 2       | AR(2): ARIMA(2,d,0)     |
| Both decay              | Both decay              | ARMA: ARIMA(p,d,q) — use AIC to choose |

---

## 5.4 Fitting an ARIMA Model with statsmodels

```python
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')

# Fit ARIMA(1, 1, 1) on log-transformed series
model = ARIMA(log_pass, order=(1, 1, 1))
result = model.fit()

print(result.summary())
```

**Key sections in the summary to check:**

| Summary Section        | What to Look For                                         |
| ---------------------- | -------------------------------------------------------- |
| **Coefficients**       | Are AR/MA coefficients significantly different from 0?   |
| **AIC / BIC**          | Lower is better — use to compare competing models       |
| **Log Likelihood**     | Higher is better — but always penalize complexity with AIC |
| **Ljung-Box (Q)**      | p-value > 0.05 → residuals are white noise ✅            |
| **Jarque-Bera**        | p-value > 0.05 → residuals are approximately normal ✅   |

---

## 5.5 Automatic Order Selection with Auto-ARIMA

Manual ACF/PACF reading is valuable for understanding, but in practice, automated selection using information criteria is more reliable — especially for ARMA models where both ACF and PACF decay.

```python
from pmdarima import auto_arima

auto_model = auto_arima(
    log_pass,
    d=1,              # fix d=1 from our stationarity test
    start_p=0, max_p=5,
    start_q=0, max_q=5,
    seasonal=False,   # no seasonal component here (handled in Section 6)
    information_criterion='aic',
    stepwise=True,    # faster; use stepwise search
    trace=True        # print candidate models
)

print(auto_model.summary())
print(f"\nSelected order: ARIMA{auto_model.order}")
```

---

## 5.6 Forecasting

```python
import matplotlib.pyplot as plt

# Fit on full series
model   = ARIMA(log_pass, order=auto_model.order)
result  = model.fit()

# Forecast next 24 months
forecast_steps = 24
forecast = result.get_forecast(steps=forecast_steps)
forecast_mean  = forecast.predicted_mean
forecast_ci    = forecast.conf_int(alpha=0.05)   # 95% confidence interval

# Convert back from log scale
forecast_mean_exp = np.exp(forecast_mean)
forecast_ci_exp   = np.exp(forecast_ci)

# Combine history and forecast for plotting
fig, ax = plt.subplots(figsize=(11, 5))

df['Passengers'].plot(ax=ax, label='Observed', color='steelblue', linewidth=1.5)

forecast_mean_exp.plot(ax=ax, label='Forecast', color='tomato', linewidth=2)

ax.fill_between(
    forecast_ci_exp.index,
    forecast_ci_exp.iloc[:, 0],
    forecast_ci_exp.iloc[:, 1],
    color='tomato', alpha=0.2, label='95% CI'
)

ax.set_title('ARIMA Forecast — Airline Passengers')
ax.set_ylabel('Passengers (thousands)')
ax.legend()
plt.tight_layout()
plt.show()
```

> ⚠️ **Forecast uncertainty grows rapidly.** The confidence interval for ARIMA forecasts expands with the horizon — long-horizon forecasts from ARIMA often have extremely wide intervals, which may not be useful in practice.  
> 預測區間隨時間快速變寬，長期預測的不確定性往往很大。ARIMA 更適合短期預測。

---

## 5.7 Residual Diagnostics

After fitting, **always inspect the residuals**. A good model should have residuals that are white noise.

```python
result.plot_diagnostics(figsize=(12, 8))
plt.suptitle('ARIMA Residual Diagnostics', y=1.01, fontsize=13)
plt.tight_layout()
plt.show()
```

The four-panel diagnostic plot shows:

| Panel                      | What It Shows                   | What to Look For              |
| -------------------------- | ------------------------------- | ----------------------------- |
| **Standardized Residuals** | Residuals over time             | Random, no patterns           |
| **Histogram + KDE**        | Residual distribution           | Approximately normal          |
| **Q–Q Plot**               | Normality check                 | Points on the diagonal        |
| **Correlogram (ACF)**      | Residual autocorrelation        | All within confidence bands   |

```python
from statsmodels.stats.diagnostic import acorr_ljungbox

lb = acorr_ljungbox(result.resid, lags=[10, 20], return_df=True)
print(lb)
# p-value > 0.05 at all lags → white noise residuals ✅
```

---

## 5.8 Model Comparison with AIC/BIC

When choosing between competing models, always compare information criteria on the **same data** (same differencing, same transformation):

```python
candidates = [(0,1,1), (1,1,0), (1,1,1), (2,1,1), (1,1,2), (2,1,2)]
results_table = []

for order in candidates:
    try:
        m = ARIMA(log_pass, order=order).fit()
        results_table.append({
            'Order': f'ARIMA{order}',
            'AIC': round(m.aic, 2),
            'BIC': round(m.bic, 2),
            'LogLik': round(m.llf, 2)
        })
    except:
        pass

comparison = pd.DataFrame(results_table).sort_values('AIC')
print(comparison.to_string(index=False))
```

> 💡 **AIC vs BIC**: AIC tends to select slightly more complex models; BIC penalizes complexity more heavily and often selects simpler models. When in doubt, prefer the model selected by BIC for production forecasting — simpler models tend to generalize better.

---

## 5.9 Key Takeaways

| Concept                           | Key Point                                                                         |
| --------------------------------- | --------------------------------------------------------------------------------- |
| **AR: regression on past values** | φ coefficients tell you how much weight each past value gets                     |
| **MA: regression on past errors** | θ coefficients adjust for past forecast errors — not a smoothing average         |
| **I: differencing**               | Removes stochastic trends; d determined by ADF/KPSS tests                        |
| **PACF → p, ACF → q**             | The core rule for manual order identification                                    |
| **Auto-ARIMA for ambiguous cases**| When both ACF and PACF decay, use AIC-based automated search                    |
| **Always diagnose residuals**     | White noise residuals = good model. Patterns in residuals = model misspecification |
| **Forecast intervals widen fast** | ARIMA is most reliable for short horizons (≤ 12 periods ahead)                  |

---