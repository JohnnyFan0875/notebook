[Statistics](../README.md) › [時間序列](README.md) › 季節性與 SARIMA

# 季節性與 SARIMA (Seasonality & SARIMA)

固定週期重複的規律（12 月銷售高峰、週末流量下降、晝夜節律）。有明顯季節性卻不用季節模型，殘差裡會留下大量可利用的結構。

## 確認季節性與週期 m

| 方法 | 看什麼 |
| --- | --- |
| 季節子序列圖 (seasonal subseries plot) | 每年一條線：哪幾個月高 / 低、型態是否逐年放大（→ 乘法） |
| 依月份的 boxplot | 各月分布 |
| [STL 分解](decomposition.md) | 季節成分強度 |
| ACF | lag m、2m 有尖峰 |

```python
import numpy as np
import pandas as pd
import seaborn as sns

url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv"
y = pd.read_csv(url, parse_dates=["Month"], index_col="Month").asfreq("MS")["Passengers"]

d = y.to_frame("y").assign(month=y.index.month, year=y.index.year)
sns.lineplot(data=d, x="month", y="y", hue="year", legend=False)    # 子序列圖
sns.boxplot(data=d, x="month", y="y")                               # 依月 boxplot
```

## SARIMA(p, d, q)(P, D, Q)[m]

在 ARIMA 之外，再加一組作用在**季節落後 (m, 2m, …)** 的 AR、差分、MA。

| 參數 | 層級 | 控制 |
| --- | --- | --- |
| p, d, q | 非季節 | 短期結構（lag 1, 2, …） |
| P | 季節 | 季節 AR：lag m, 2m, …, Pm |
| D | 季節 | 季節差分次數（通常 1） |
| Q | 季節 | 季節 MA：lag m, 2m, …, Qm |
| **m** | — | **季節週期**：月資料 12、季資料 4、日資料（週週期）7 |

**讀季節 ACF / PACF**（先做 log + 一階差分 + 季節差分）：

| 尖峰位置 | 建議 |
| --- | --- |
| ACF 在 lag m 有尖峰 | 季節 MA，Q = 1 |
| PACF 在 lag m 有尖峰 | 季節 AR，P = 1 |
| ACF 在 m、2m 都有 | Q = 2，或季節衰減緩慢 → P > 0 |
| 季節 lag 都不顯著 | 季節差分已足夠 |

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.forecasting.stl import STLForecast
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima import auto_arima

log_y = np.log(y)
plot_acf(log_y.diff().diff(12).dropna(), lags=48)          # 看 lag 12, 24, 36 …

# SARIMA(1,1,1)(1,1,1)[12]：月資料常見的起點（「airline model」是 (0,1,1)(0,1,1)[12]）
res = SARIMAX(log_y, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)).fit(disp=False)
res.aic, res.bic
fc = np.exp(res.get_forecast(36).predicted_mean)

# 自動選階
auto = auto_arima(log_y, m=12, d=1, D=1, max_p=3, max_q=3, max_P=2, max_Q=2,
                  seasonal=True, information_criterion="aic", stepwise=True)
auto.order, auto.seasonal_order

# 替代：STL 去季節 → ARIMA 建模去季節化序列 → 季節成分另外外推
stl_res = STLForecast(log_y, ARIMA, model_kwargs={"order": (1, 1, 0)}, period=12).fit()
np.exp(stl_res.forecast(36))
```

## 多重季節性：Prophet

日資料同時有週與年週期時，SARIMA 不實用。

```python
from prophet import Prophet

dfp = y.reset_index().rename(columns={"Month": "ds", "Passengers": "y"})   # Prophet 需要 ds / y 欄位
m = Prophet(yearly_seasonality=True, seasonality_mode="multiplicative").fit(dfp)
fc = m.predict(m.make_future_dataframe(periods=36, freq="MS"))
m.plot(fc); m.plot_components(fc)
```

| Prophet 優點 | 限制 |
| --- | --- |
| 自動處理多重季節性、假日 | 解釋性不如 ARIMA |
| 對缺失與離群值穩健 | 需要足夠歷史；短序列易過擬合 |
| 不需要讀 ACF / PACF | 不適合高頻金融資料 |

## 選哪個模型

| 情境 | 建議 |
| --- | --- |
| 月 / 季資料、單一季節週期 | **SARIMA** |
| 季節型態複雜或會演變 | **STL + ARIMA** |
| 多重季節週期 | **Prophet** 或 **MSTL + ARIMA** |
| 需要解釋性 | SARIMA 或 STL + ARIMA |

> 把兩組角色分清楚：(p, d, q) 是短期非季節結構；(P, D, Q)[m] 是重複的季節結構。混淆兩者是把 SARIMA 搞得過度複雜的最快方式。
