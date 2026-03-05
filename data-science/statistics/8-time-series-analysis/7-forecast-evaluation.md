# 7. Forecast Evaluation

Fitting a model is only half the job. **Evaluation** tells you whether the model actually works on new, unseen data — and how much you can trust its predictions. A model that fits the training data perfectly but fails on the test period is useless for forecasting.

> 📌 **模型評估的核心原則**：永遠不能用訓練資料評估預測效果。時間序列必須按時間順序切分，用過去預測未來，而非隨機抽樣。這與一般機器學習的交叉驗證不同。

---

## 7.1 Train-Test Split for Time Series

Unlike cross-sectional data, **time series must be split chronologically** — you cannot randomly shuffle observations into train/test sets. The training set must always precede the test set.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv"
df = pd.read_csv(url, parse_dates=['Month'], index_col='Month').asfreq('MS')
df.columns = ['Passengers']

# Hold out the last 24 months as test set
train = df.iloc[:-24]
test  = df.iloc[-24:]

print(f"Train: {train.index[0].date()} to {train.index[-1].date()} ({len(train)} obs)")
print(f"Test:  {test.index[0].date()}  to {test.index[-1].date()}  ({len(test)} obs)")

fig, ax = plt.subplots(figsize=(11, 4))
train['Passengers'].plot(ax=ax, label='Train', color='steelblue', linewidth=1.5)
test['Passengers'].plot( ax=ax, label='Test',  color='tomato',    linewidth=1.5)
ax.set_title('Train / Test Split (last 24 months held out)')
ax.legend()
plt.tight_layout()
plt.show()
```

> 💡 **How much data to hold out?** A common rule: hold out at least one or two full seasonal cycles. For monthly data, 12–24 months is typical. The goal is to test whether the model generalizes to a realistic forecast horizon.

---

## 7.2 Error Metrics

Once we have forecasts on the test set, we measure accuracy with these metrics:

### MAE — Mean Absolute Error

$$\text{MAE} = \frac{1}{h} \sum_{t=1}^{h} |y_t - \hat{y}_t|$$

- Easy to interpret: average absolute deviation in the original units
- Treats all errors equally — not sensitive to large individual errors
- **Best for**: general reporting, when large errors aren't especially costly

### RMSE — Root Mean Squared Error

$$\text{RMSE} = \sqrt{\frac{1}{h} \sum_{t=1}^{h} (y_t - \hat{y}_t)^2}$$

- Penalizes large errors more heavily than MAE (due to squaring)
- Same units as the original series
- **Best for**: when large forecast errors are especially costly

### MAPE — Mean Absolute Percentage Error

$$\text{MAPE} = \frac{100\%}{h} \sum_{t=1}^{h} \left| \frac{y_t - \hat{y}_t}{y_t} \right|$$

- Scale-free: expressed as a percentage, easy to communicate to non-statisticians
- **Limitation**: undefined when yₜ = 0; biased when values are small
- **Best for**: comparing accuracy across different series or scales

### MASE — Mean Absolute Scaled Error

$$\text{MASE} = \frac{\text{MAE}}{\frac{1}{n-m} \sum_{t=m+1}^{n} |y_t - y_{t-m}|}$$

The denominator is the in-sample MAE of a seasonal naive forecast (predicting yₜ = yₜ₋ₘ).

- **MASE < 1**: model beats the seasonal naive baseline
- **MASE > 1**: seasonal naive would have done better — model needs improvement
- **Best for**: proper scale-free comparison across multiple series

```python
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
warnings.filterwarnings('ignore')

# Fit model on train, forecast on test
log_train = np.log(train['Passengers'])
log_test  = np.log(test['Passengers'])

model = SARIMAX(log_train, order=(1,1,1), seasonal_order=(1,1,1,12),
                enforce_stationarity=False, enforce_invertibility=False)
result = model.fit(disp=False)

forecast = result.forecast(steps=len(test))
fc_exp   = np.exp(forecast)

y_true = test['Passengers'].values
y_pred = fc_exp.values

# Metrics
mae  = mean_absolute_error(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))
mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# MASE — seasonal naive baseline (m=12)
m = 12
naive_errors = np.abs(np.diff(train['Passengers'].values, n=m))
naive_mae    = naive_errors[m:].mean()  # in-sample seasonal naive MAE
mase = mae / naive_mae

print(f"MAE:  {mae:.2f} thousand passengers")
print(f"RMSE: {rmse:.2f} thousand passengers")
print(f"MAPE: {mape:.2f}%")
print(f"MASE: {mase:.3f}  {'✅ beats naive' if mase < 1 else '❌ worse than naive'}")
```

---

## 7.3 Visualizing Forecast vs Actual

```python
fig, ax = plt.subplots(figsize=(12, 5))

train['Passengers'].plot(ax=ax, label='Training Data', color='steelblue', linewidth=1.5)
test['Passengers'].plot(ax=ax,  label='Actual (Test)', color='seagreen',  linewidth=2)
fc_exp.plot(ax=ax,              label='Forecast',      color='tomato',    linewidth=2, linestyle='--')

# Confidence interval
forecast_full = result.get_forecast(steps=len(test))
ci = np.exp(forecast_full.conf_int(alpha=0.05))
ax.fill_between(ci.index, ci.iloc[:,0], ci.iloc[:,1],
                color='tomato', alpha=0.2, label='95% CI')

ax.set_title(f'SARIMA Forecast vs Actual  (MAPE = {mape:.1f}%)')
ax.set_ylabel('Passengers (thousands)')
ax.legend()
plt.tight_layout()
plt.show()
```

---

## 7.4 Walk-Forward Validation (Time Series Cross-Validation)

A single train/test split can be sensitive to which particular period you hold out. **Walk-forward validation** (also called expanding window or rolling origin) provides a more robust evaluation.

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np, warnings
warnings.filterwarnings('ignore')

log_pass   = np.log(df['Passengers'])
n          = len(log_pass)
min_train  = 84    # start after 7 years of training data
horizon    = 12    # evaluate 12-step-ahead forecasts

actuals    = []
forecasts  = []
origins    = []

for origin in range(min_train, n - horizon + 1, 6):   # step by 6 months
    train_wf = log_pass.iloc[:origin]
    test_wf  = log_pass.iloc[origin:origin + horizon]

    m = SARIMAX(train_wf, order=(1,1,1), seasonal_order=(1,1,1,12),
                enforce_stationarity=False, enforce_invertibility=False)
    r = m.fit(disp=False)
    fc = r.forecast(horizon)

    actuals.append(np.exp(test_wf.values))
    forecasts.append(np.exp(fc.values))
    origins.append(log_pass.index[origin])

# Average MAPE across all origins
all_mape = [np.mean(np.abs((a - f) / a)) * 100
            for a, f in zip(actuals, forecasts)]

print(f"Walk-forward MAPE: {np.mean(all_mape):.2f}% ± {np.std(all_mape):.2f}%")
print(f"Evaluation origins: {len(all_mape)}")
```

> 💡 **Expanding vs rolling window**: Expanding window (grows the training set) is more common — it uses all available historical data. Rolling window (fixed training size) is used when you suspect the underlying process changes over time.

---

## 7.5 Residual Diagnostics

Good forecasts require well-behaved residuals. These diagnostics should always be run after model fitting.

```python
import scipy.stats as stats

# Fit on full training data for residual diagnostics
model_full  = SARIMAX(log_train, order=(1,1,1), seasonal_order=(1,1,1,12),
                      enforce_stationarity=False, enforce_invertibility=False)
result_full = model_full.fit(disp=False)
resid       = result_full.resid.dropna()

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# 1. Residuals over time
axes[0,0].plot(resid, color='gray', linewidth=1, alpha=0.8)
axes[0,0].axhline(0, color='black', linestyle='--', alpha=0.5)
axes[0,0].set_title('Residuals Over Time')

# 2. Histogram
axes[0,1].hist(resid, bins=20, color='steelblue', edgecolor='white', density=True)
x_range = np.linspace(resid.min(), resid.max(), 200)
axes[0,1].plot(x_range, stats.norm.pdf(x_range, resid.mean(), resid.std()),
               'r-', linewidth=2, label='Normal fit')
axes[0,1].set_title('Residual Distribution')
axes[0,1].legend()

# 3. Q–Q plot
stats.probplot(resid, dist='norm', plot=axes[1,0])
axes[1,0].set_title('Q–Q Plot')

# 4. ACF of residuals
from statsmodels.graphics.tsaplots import plot_acf
plot_acf(resid, lags=24, ax=axes[1,1], alpha=0.05)
axes[1,1].set_title('ACF of Residuals (should be white noise)')

plt.suptitle('Residual Diagnostics', fontsize=13, y=1.01)
plt.tight_layout()
plt.show()
```

**Residual checklist:**

| Check                           | Method                | Acceptable Result                      |
| ------------------------------- | --------------------- | -------------------------------------- |
| **No trend / pattern**          | Time plot             | Residuals scatter randomly around zero |
| **Constant variance**           | Time plot             | No fanning or clustering               |
| **Approximately normal**        | Histogram + Q–Q plot  | Roughly bell-shaped; near diagonal     |
| **No autocorrelation**          | ACF plot              | All lags within confidence bands       |
| **Ljung-Box test**              | Statistical test      | p-value > 0.05 at all lags             |

```python
from statsmodels.stats.diagnostic import acorr_ljungbox

lb = acorr_ljungbox(resid, lags=[12, 24], return_df=True)
print(lb)
```

---

## 7.6 Benchmark Comparisons

Always compare your model against simple baselines. If your model can't beat a naive forecast, something is wrong.

| Baseline                         | Definition                                    | When It's Competitive         |
| -------------------------------- | --------------------------------------------- | ----------------------------- |
| **Naive (random walk)**          | ŷₜ₊₁ = yₜ                                    | Many financial series         |
| **Seasonal Naive**               | ŷₜ = yₜ₋ₘ (same period last cycle)           | Highly seasonal series        |
| **Mean forecast**                | ŷₜ = ȳ (training mean)                       | Series with no trend or seasonality |
| **Drift**                        | Extrapolate the average trend from training   | Strong, steady trends         |

```python
# Seasonal Naive baseline
seasonal_naive = train['Passengers'].values[-12:]  # last 12 months repeated

sn_mape = np.mean(np.abs((y_true - seasonal_naive) / y_true)) * 100
print(f"Seasonal Naive MAPE: {sn_mape:.2f}%")
print(f"SARIMA MAPE:         {mape:.2f}%")
print(f"Improvement:         {sn_mape - mape:.2f} percentage points")
```

---

## 7.7 Metric Selection Guide

| Situation                                    | Recommended Metric     | Reason                                  |
| -------------------------------------------- | ---------------------- | --------------------------------------- |
| Reporting to non-technical stakeholders      | **MAPE**               | Easy to communicate as a percentage     |
| Comparing models on the same scale           | **MAE** or **RMSE**    | Direct, unit-matched comparison         |
| Large errors are especially costly           | **RMSE**               | Penalizes outliers more heavily         |
| Comparing across multiple series / scales    | **MASE**               | Scale-free; relative to naive baseline  |
| Selecting model order (in-sample)            | **AIC / BIC**          | Penalizes complexity; avoids overfitting|

> ⚠️ Never use R² for time series forecast evaluation. R² measures in-sample fit and is extremely misleading for out-of-sample forecast quality. Two spuriously correlated non-stationary series can have R² near 1.  
> 時間序列預測不要用 R²。R² 衡量的是樣本內配適，對樣本外預測效果毫無意義，甚至誤導。

---

## 7.8 Key Takeaways

| Concept                           | Key Point                                                                          |
| --------------------------------- | ---------------------------------------------------------------------------------- |
| **Split chronologically**         | Never randomly split time series — training must precede test in time              |
| **MAE for general use**           | Intuitive, robust; reports error in original units                                 |
| **RMSE for outlier sensitivity**  | Penalizes large errors more — use when big misses are costly                       |
| **MAPE for communication**        | Easy percentage interpretation; but undefined when y = 0                          |
| **MASE for cross-series comparison** | Relative to seasonal naive — always run this to confirm model adds value       |
| **Walk-forward for robust eval**  | Multiple evaluation origins give a more stable estimate of true forecast accuracy  |
| **Always beat a naive baseline**  | If MASE > 1, the model is worse than predicting "same as last year"               |
| **Residuals must be white noise** | Patterns in residuals = unused structure = room to improve the model              |

---

**← Previous:** [Seasonality & SARIMA](./6-seasonality-sarima.md)  
**↑ Back to:** [Time Series Analysis — README](./README.md)
