# 2. Decomposition

**Decomposition** separates a time series into its structural components — trend, seasonality, and residual — so that each can be analyzed, modeled, or visualized independently. It is one of the most powerful tools for understanding *why* a series behaves the way it does.

> 📌 **為什麼先做分解**：直接對含有趨勢和季節性的序列建模，等於讓模型同時學習多種不同性質的模式。先分解能讓你確認模型需要處理哪些成分，並且更容易發現資料中的異常或結構性變化。

---

## 2.1 Additive vs Multiplicative Decomposition

The choice between these two models depends on how the seasonal variation behaves as the overall level changes.

| Model              | Formula                              | When to Use                                          |
| ------------------ | ------------------------------------ | ---------------------------------------------------- |
| **Additive**       | Yₜ = Tₜ + Sₜ + Rₜ                   | Seasonal amplitude is **constant** regardless of level |
| **Multiplicative** | Yₜ = Tₜ × Sₜ × Rₜ                   | Seasonal amplitude **grows proportionally** with level |

> 💡 **Quick visual check**: Plot the raw series. If the peaks and troughs get larger as the overall level rises (like a megaphone shape), use multiplicative. If they stay roughly the same height throughout, use additive.  
> 觀察季節性波動的幅度：如果振幅隨著整體水準等比例增大，用乘法模型；如果振幅固定，用加法模型。

> 💡 **Log trick**: A multiplicative model can always be converted to an additive model by taking the log: log(Y) = log(T) + log(S) + log(R). This is why log-transforming before additive decomposition is so common.

---

## 2.2 Classical Decomposition

The classical method uses **centered moving averages** to estimate the trend, then separates out the seasonal component.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# Load airline passenger data
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv"
df = pd.read_csv(url, parse_dates=['Month'], index_col='Month')
df.columns = ['Passengers']
df = df.asfreq('MS')

# Additive decomposition
result_add = seasonal_decompose(df['Passengers'], model='additive', period=12)

# Multiplicative decomposition
result_mul = seasonal_decompose(df['Passengers'], model='multiplicative', period=12)

# Plot additive
fig, axes = plt.subplots(4, 1, figsize=(11, 9), sharex=True)
result_add.observed.plot( ax=axes[0], title='Observed',   color='steelblue')
result_add.trend.plot(    ax=axes[1], title='Trend',      color='tomato')
result_add.seasonal.plot( ax=axes[2], title='Seasonal',   color='seagreen')
result_add.resid.plot(    ax=axes[3], title='Residual',   color='gray', alpha=0.8)
plt.suptitle('Classical Additive Decomposition', fontsize=13, y=1.01)
plt.tight_layout()
plt.show()
```

**Limitations of classical decomposition:**

| Limitation                            | Impact                                          |
| ------------------------------------- | ----------------------------------------------- |
| Trend estimate missing at endpoints   | First and last ~m/2 periods have NaN trend      |
| Seasonal pattern assumed fixed        | Cannot change over time                         |
| Sensitive to outliers                 | One extreme value distorts nearby trend values  |
| Only handles one seasonal period      | Can't handle daily + weekly + yearly at once    |

---

## 2.3 STL Decomposition

**STL (Seasonal-Trend decomposition using Loess)** is the modern alternative. It uses locally-weighted regression (LOESS) to fit each component, making it far more flexible and robust.

```python
from statsmodels.tsa.seasonal import STL

# STL decomposition
stl = STL(df['Passengers'], period=12, robust=True)
result_stl = stl.fit()

fig, axes = plt.subplots(4, 1, figsize=(11, 9), sharex=True)
result_stl.observed.plot( ax=axes[0], title='Observed',  color='steelblue')
result_stl.trend.plot(    ax=axes[1], title='Trend',     color='tomato')
result_stl.seasonal.plot( ax=axes[2], title='Seasonal',  color='seagreen')
result_stl.resid.plot(    ax=axes[3], title='Residual',  color='gray', alpha=0.8)
plt.suptitle('STL Decomposition', fontsize=13, y=1.01)
plt.tight_layout()
plt.show()
```

**Key STL parameters:**

| Parameter   | Description                                              | Recommended Setting           |
| ----------- | -------------------------------------------------------- | ----------------------------- |
| `period`    | The seasonal period (m=12 for monthly, 7 for daily)      | Required — must specify        |
| `robust`    | Use robust LOESS to downweight outliers                  | `True` when outliers expected |
| `seasonal`  | Smoothness of seasonal component (must be odd)           | Larger = smoother season      |
| `trend`     | Smoothness of trend component (must be odd, > period)    | Larger = smoother trend       |

---

## 2.4 Comparing Classical vs STL

| Feature                          | Classical Decomposition | STL                         |
| -------------------------------- | ----------------------- | --------------------------- |
| **Trend at endpoints**           | ❌ Missing (NaN)        | ✅ Available                |
| **Seasonal pattern over time**   | ❌ Fixed                | ✅ Can evolve               |
| **Outlier robustness**           | ❌ Sensitive            | ✅ Robust option available  |
| **Multiple seasonalities**       | ❌ One period only      | ❌ One period (use MSTL)    |
| **Multiplicative support**       | ✅ Direct               | Via log transform           |
| **Ease of use**                  | ✅ Simple               | Slightly more parameters    |

> 💡 **Default choice**: Use STL with `robust=True` for most practical applications. Use classical decomposition only for quick exploratory checks or when teaching the concept.  
> 實務首選 STL，尤其是資料中可能含有離群值時。

---

## 2.5 Using Decomposition for Feature Engineering

Decomposition components can be extracted and used directly as features or for downstream analysis.

```python
# Extract components
trend_component    = result_stl.trend
seasonal_component = result_stl.seasonal
residual_component = result_stl.resid

# Strength of trend and seasonality (Wang, Smith & Hyndman, 2006)
var_resid    = np.var(residual_component.dropna())
var_trend_r  = np.var((trend_component + residual_component).dropna())
var_season_r = np.var((seasonal_component + residual_component).dropna())

strength_trend    = max(0, 1 - var_resid / var_trend_r)
strength_seasonal = max(0, 1 - var_resid / var_season_r)

print(f"Strength of Trend:      {strength_trend:.3f}  (0 = none, 1 = perfect)")
print(f"Strength of Seasonality:{strength_seasonal:.3f}  (0 = none, 1 = perfect)")
```

> 💡 These strength measures (0 to 1) give you an objective quantification of how dominant each component is. A trend strength > 0.6 means the trend is substantial; seasonality strength > 0.6 means seasonal modeling is likely necessary.

```python
# Seasonally adjusted series: remove seasonal component
seasonally_adjusted = df['Passengers'] - seasonal_component

plt.figure(figsize=(10, 4))
plt.plot(df['Passengers'],    label='Original',            color='steelblue', alpha=0.5)
plt.plot(seasonally_adjusted, label='Seasonally Adjusted', color='tomato',    linewidth=2)
plt.title('Original vs Seasonally Adjusted Series')
plt.legend()
plt.tight_layout()
plt.show()
```

> 💡 **Seasonally adjusted series** are what you see in official economic statistics (e.g., seasonally adjusted unemployment rate). Removing seasonality lets you see the true underlying trend without monthly noise.

---

## 2.6 Residual Diagnostics After Decomposition

After decomposition, the residuals should be **white noise** — no structure, no autocorrelation, approximately normal. If residuals still contain patterns, the decomposition hasn't captured everything.

```python
import matplotlib.pyplot as plt
import scipy.stats as stats

resid = result_stl.resid.dropna()

fig, axes = plt.subplots(1, 3, figsize=(13, 4))

# Residual time plot — should be random around zero
axes[0].plot(resid, color='gray', alpha=0.7)
axes[0].axhline(0, color='black', linestyle='--')
axes[0].set_title('Residuals over Time')

# Histogram — should be approximately normal
axes[1].hist(resid, bins=20, color='steelblue', edgecolor='white', density=True)
x = np.linspace(resid.min(), resid.max(), 200)
axes[1].plot(x, stats.norm.pdf(x, resid.mean(), resid.std()), 'r-', linewidth=2)
axes[1].set_title('Residual Distribution')

# Q-Q plot — should follow the diagonal
stats.probplot(resid, dist="norm", plot=axes[2])
axes[2].set_title('Q–Q Plot of Residuals')

plt.tight_layout()
plt.show()

print(f"Residual mean: {resid.mean():.4f}  (should be ≈ 0)")
print(f"Residual std:  {resid.std():.4f}")
```

---

## 2.7 Key Takeaways

| Concept                           | Key Point                                                                           |
| --------------------------------- | ----------------------------------------------------------------------------------- |
| **Additive vs multiplicative**    | Check if seasonal amplitude grows with level — if yes, use multiplicative (or log) |
| **STL > classical in practice**   | More robust, trend at endpoints, evolving seasonality                               |
| **Seasonally adjusted = deseasonalized** | Removing seasonal component reveals underlying trend                       |
| **Measure component strength**    | Quantify how dominant trend and seasonality are before choosing a model             |
| **Residuals should be white noise** | Patterns in residuals mean the decomposition missed structure                    |

---