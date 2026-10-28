[Statistics](../README.md) › [時間序列](README.md) › ARIMA

# ARIMA 模型

**ARIMA** (AutoRegressive Integrated Moving Average) = AR（用過去的值）+ I（差分去趨勢）+ MA（用過去的誤差修正）。理解每個成分的直覺，比背選階規則重要。

| 成分 | 公式 | 意義 | 階數由誰決定 |
| --- | --- | --- | --- |
| **AR(p)** 自迴歸 | $y_t = c + \phi_1 y_{t-1} + \cdots + \phi_p y_{t-p} + \varepsilon_t$ | 預測變數是**自己的落後值**的迴歸 | PACF 截斷處 |
| **I(d)** 整合 | d 次差分 | d = 0 已定態；d = 1 一階差分；d = 2 罕見 | ADF / KPSS |
| **MA(q)** 移動平均 | $y_t = \mu + \varepsilon_t + \theta_1 \varepsilon_{t-1} + \cdots + \theta_q \varepsilon_{t-q}$ | 對**過去的預測誤差（衝擊）**的迴歸 | ACF 截斷處 |

> ARIMA 的 MA ≠ 平滑用的「移動平均」。名字相同，概念不同：前者建模過去的**誤差**，後者平均過去的**值**。
>
> ARIMA 適合處理「前處理後剩下的結構」：先處理明顯的趨勢、變異改變與（非季節 ARIMA 時的）季節性，它不是處理原始資料的萬能黑盒子。

## 選階：ACF / PACF

| ACF | PACF | 建議 |
| --- | --- | --- |
| lag 1 後截斷 | 衰減 | ARIMA(0, d, 1) |
| lag 2 後截斷 | 衰減 | ARIMA(0, d, 2) |
| 衰減 | lag 1 後截斷 | ARIMA(1, d, 0) |
| 衰減 | lag 2 後截斷 | ARIMA(2, d, 0) |
| 都衰減 | 都衰減 | ARIMA(p, d, q)，用 AIC / auto-ARIMA 選 |

詳細判讀見 [自相關](autocorrelation.md)。

## 完整流程

```python
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
from pmdarima import auto_arima

url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv"
y = pd.read_csv(url, parse_dates=["Month"], index_col="Month").asfreq("MS")["Passengers"]
log_y = np.log(y)                                       # 1. 穩定變異

# 2. 自動選階（以 AIC 為準；d 由定態檢定決定）
auto = auto_arima(log_y, d=1, max_p=5, max_q=5, seasonal=False,
                  information_criterion="aic", stepwise=True)
auto.order

# 3. 配適
res = ARIMA(log_y, order=auto.order).fit()
res.summary()

# 4. 殘差診斷：應為白噪音
res.plot_diagnostics(figsize=(12, 8))
acorr_ljungbox(res.resid, lags=[10, 20], return_df=True)   # p > 0.05 ✅

# 5. 預測 24 期並轉回原尺度
fc = res.get_forecast(steps=24)
mean = np.exp(fc.predicted_mean)
ci = np.exp(fc.conf_int(alpha=0.05))

# 6. 手動比較候選模型（相同資料、相同轉換才能比 AIC）
for order in [(0, 1, 1), (1, 1, 0), (1, 1, 1), (2, 1, 1)]:
    m = ARIMA(log_y, order=order).fit()
    print(order, round(m.aic, 1), round(m.bic, 1))
```

| summary 欄位 | 看什麼 |
| --- | --- |
| 係數 | AR / MA 係數是否顯著不為 0 |
| AIC / BIC | 越小越好；BIC 懲罰較重、偏好較簡單的模型 |
| Ljung-Box (Q) | p > 0.05 → 殘差為白噪音 |
| Jarque-Bera | p > 0.05 → 殘差近似常態 |

| 殘差診斷圖 | 應該看到 |
| --- | --- |
| 標準化殘差 vs 時間 | 隨機、無型態 |
| 直方圖 + KDE | 近似常態 |
| Q–Q 圖 | 點在對角線上 |
| 殘差 ACF (correlogram) | 全在信賴帶內 |

> - **預測區間擴張很快**：ARIMA 最適合短期預測（約 ≤ 12 期）。
> - log 尺度的預測取 exp 得到的是**中位數**預測，不是平均數；需要平均數時要做偏誤校正。
> - 有季節性時改用 [SARIMA](seasonality-sarima.md)；評估方式見 [預測評估](forecast-evaluation.md)。
