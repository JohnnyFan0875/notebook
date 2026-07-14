# Autocorrelation: ACF & PACF

This note focuses on autocorrelation as a time-series modeling diagnostic. If you want the finance-specific interpretation around momentum, mean reversion, and trading usefulness, see [Autocorrelation in Finance](../../finance/autocorrelation.md).

**Autocorrelation** measures how a time series is correlated with its own past values. ACF and PACF plots are the primary diagnostic tools for identifying the structure of a stationary time series — and for determining the orders p and q in an ARIMA model.

Key point: ACF and PACF are fingerprints of a time series: just like a scatter plot reveals the relationship between two variables, the ACF/PACF plot reveals the relationship between a series and its own history. Understanding these two graphs is the core skill for selecting ARIMA parameters.

## Autocorrelation Function (ACF)

The ACF measures the **linear correlation between yₜ and yₜ₋ₖ** for each lag k, without controlling for the effect of intermediate lags.

\[
\rho_k = \frac{\text{Cov}(Y_t, Y_{t-k})}{\text{Var}(Y_t)}
\]

**Range**: −1 ≤ ρₖ ≤ 1, just like a regular Pearson correlation.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv"
df = pd.read_csv(url, parse_dates=['Month'], index_col='Month').asfreq('MS')
df.columns = ['Passengers']

# Work with log-differenced series (stationary)
series = np.log(df['Passengers']).diff(1).dropna()

fig, ax = plt.subplots(figsize=(10, 4))
plot_acf(series, lags=36, ax=ax, alpha=0.05)
ax.set_title('ACF — Log First-Differenced Airline Passengers')
ax.set_xlabel('Lag (months)')
plt.tight_layout()
plt.show()
```

**How to read the ACF plot:**

| Pattern | Interpretation | Suggests |
| ---------------------------------------- | --------------------------------------- | ---------------- |
| Spikes cut off sharply after lag q | Only short-term dependence | MA(q) process |
| Spikes decay slowly / exponentially | Long-range dependence | AR process present |
| Alternating positive/negative spikes | Oscillatory dependence | Check for AR(2) |
| Spike at lag m (e.g., 12) still large | Seasonal pattern not yet removed | Need seasonal differencing |
| All spikes within confidence bands | White noise ✅ | No more structure to model |

Tip: The blue shaded region (or dashed lines) in the ACF plot represents the 95% confidence band. Spikes outside this band are statistically significant at α = 0.05. Spikes outside the blue region are statistically significant. It doesn't need to be that all spikes are perfectly within the band, one or two just outside the boundary is statistically normal.

## Partial Autocorrelation Function (PACF)

The PACF measures the correlation between yₜ and yₜ₋ₖ **after removing the linear effects of all intermediate lags** (yₜ₋₁, yₜ₋₂, ..., yₜ₋ₖ₊₁).

This is analogous to partial correlation in regression: the PACF at lag k tells you **only the direct relationship** between the observation and its k-th lag, not the indirect path through shorter lags.

```python
fig, ax = plt.subplots(figsize=(10, 4))
plot_pacf(series, lags=36, ax=ax, alpha=0.05, method='ywm')
ax.set_title('PACF — Log First-Differenced Airline Passengers')
ax.set_xlabel('Lag (months)')
plt.tight_layout()
plt.show()
```

**How to read the PACF plot:**

| Pattern | Interpretation | Suggests |
| --------------------------------------- | ---------------------------- | ---------------- |
| Spikes cut off sharply after lag p | Direct AR dependence at p | AR(p) process |
| Spikes decay slowly | MA structure dominant | MA process present |
| Single spike at lag 1 | Strong one-step dependence | AR(1) |
| Spikes cut off after lag p, with oscillation | Negative AR coefficients | AR(p) with negative φ |

## The ACF/PACF Pattern Recognition Table

This is the core of using ACF/PACF for model identification:

| Process | ACF Pattern | PACF Pattern |
| ---------- | ------------------------------ | ------------------------------ |
| **AR(p)** | Decays exponentially (or oscillating) | Cuts off sharply after lag p |
| **MA(q)** | Cuts off sharply after lag q | Decays exponentially |
| **ARMA(p,q)** | Decays (exponentially or oscillating) | Decays (exponentially or oscillating) |
| **White Noise** | All within confidence band | All within confidence band |
| **Non-stationary** | Decays very slowly (near 1) | Large spike at lag 1 |

Tip: Memory aid: - AR → look at PACF for the cut-off (p = where PACF cuts off) - MA → look at ACF for the cut-off (q = where ACF cuts off) AR looks at PACF, MA looks at ACF - each looks at "the picture they control".

## Side-by-Side Diagnostic Plot

Always plot ACF and PACF together for model identification:

```python
fig, axes = plt.subplots(2, 1, figsize=(10, 7))
plot_acf( series, lags=36, ax=axes[0], alpha=0.05)
plot_pacf(series, lags=36, ax=axes[1], alpha=0.05, method='ywm')
axes[0].set_title('ACF')
axes[1].set_title('PACF')
axes[0].set_xlabel('Lag')
axes[1].set_xlabel('Lag')
plt.tight_layout()
plt.show()
```

## Worked Example: Identifying AR vs MA Processes

```python
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_process import ArmaProcess

np.random.seed(42)
n = 300

# --- AR(2) process ---
ar_params = np.array([1, -0.6, -0.3])   # AR: 1 - 0.6L - 0.3L²
ma_params = np.array([1])               # MA: no terms
ar2_process = ArmaProcess(ar_params, ma_params)
ar2_series  = ar2_process.generate_sample(nsample=n)

# --- MA(2) process ---
ar_params2 = np.array([1])
ma_params2 = np.array([1, 0.7, 0.4])   # MA(2) terms
ma2_process = ArmaProcess(ar_params2, ma_params2)
ma2_series  = ma2_process.generate_sample(nsample=n)

fig, axes = plt.subplots(2, 3, figsize=(14, 7))

# AR(2)
axes[0,0].plot(ar2_series[:100], color='steelblue', linewidth=1)
axes[0,0].set_title('AR(2) Series (first 100 obs)')
plot_acf( ar2_series, lags=20, ax=axes[0,1], alpha=0.05)
axes[0,1].set_title('AR(2) — ACF  (expect: decays slowly)')
plot_pacf(ar2_series, lags=20, ax=axes[0,2], alpha=0.05, method='ywm')
axes[0,2].set_title('AR(2) — PACF (expect: cuts off at lag 2)')

# MA(2)
axes[1,0].plot(ma2_series[:100], color='tomato', linewidth=1)
axes[1,0].set_title('MA(2) Series (first 100 obs)')
plot_acf( ma2_series, lags=20, ax=axes[1,1], alpha=0.05)
axes[1,1].set_title('MA(2) — ACF  (expect: cuts off at lag 2)')
plot_pacf(ma2_series, lags=20, ax=axes[1,2], alpha=0.05, method='ywm')
axes[1,2].set_title('MA(2) — PACF (expect: decays slowly)')

plt.tight_layout()
plt.show()
```

## Autocorrelation as a Stationarity Check

ACF is also used to confirm whether a series is stationary **before modeling**:

```python
fig, axes = plt.subplots(2, 2, figsize=(13, 7))

# Non-stationary: original log series
plot_acf(np.log(df['Passengers']),       lags=36, ax=axes[0,0])
axes[0,0].set_title('ACF — Log Series (Non-Stationary)\nExpect: slow decay')

# After first difference
plot_acf(np.log(df['Passengers']).diff(1).dropna(), lags=36, ax=axes[0,1])
axes[0,1].set_title('ACF — Log + First Diff\nExpect: faster decay')

# PACF of stationary
plot_pacf(np.log(df['Passengers']),       lags=36, ax=axes[1,0], method='ywm')
axes[1,0].set_title('PACF — Log Series (Non-Stationary)')

plot_pacf(np.log(df['Passengers']).diff(1).dropna(), lags=36, ax=axes[1,1], method='ywm')
axes[1,1].set_title('PACF — Log + First Diff')

plt.tight_layout()
plt.show()
```

Warning: Non-stationary series sign in ACF: The ACF decays very slowly, staying near 1 for many lags. After differencing, the ACF should drop much more quickly. If it still decays slowly, difference again.

## Ljung-Box Test: Is There Remaining Autocorrelation?

After fitting a model, use the Ljung-Box test to check whether the **residuals** still have autocorrelation. If they do, the model hasn't captured all the structure.

**H₀: The residuals are white noise (no autocorrelation)**
**H₁: Some autocorrelation remains**

```python
from statsmodels.stats.diagnostic import acorr_ljungbox

residuals = series  # placeholder — use actual model residuals in practice

lb_result = acorr_ljungbox(residuals, lags=[10, 20], return_df=True)
print(lb_result)
# p-value > 0.05 → residuals are white noise ✅
# p-value < 0.05 → remaining autocorrelation ❌ — model needs adjustment
```

## Key Takeaways

| Concept | Key Point |
| ---------------------------- | --------------------------------------------------------------------------------- |
| **ACF = total correlation** | Includes direct and indirect effects of all intermediate lags |
| **PACF = direct correlation** | Removes the influence of shorter lags — isolates the k-lag direct effect |
| **AR → read PACF** | AR(p): PACF cuts off sharply after lag p; ACF decays |
| **MA → read ACF** | MA(q): ACF cuts off sharply after lag q; PACF decays |
| **Slow-decaying ACF = non-stationary** | Difference the series and check again |
| **Ljung-Box after fitting** | Check residual ACF is white noise — if not, the model is misspecified |

## ACF Is Structure, Not Causation

Autocorrelation tells you how the series relates to its own past. It does not tell you why that structure exists. Trend leakage, seasonality, under-differencing, and true serial persistence can all produce similar ACF patterns.
