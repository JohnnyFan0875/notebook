[Statistics](../README.md) › 時間序列

# 時間序列分析 (Time Series Analysis)

依時間順序蒐集的資料。觀測值**不獨立**：昨天影響今天。這種時間相依性既是挑戰，也是能夠預測的原因。順序不能打亂。

## 建議順序

```
認識資料 → 分解（趨勢 + 季節 + 殘差）→ 定態檢查與轉換 → ACF / PACF → ARIMA → SARIMA → 預測評估
```

多數古典模型假設**定態 (stationarity)**，跳過分解與定態檢查是最常見的錯誤。

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [基礎](fundamentals.md) | 四種成分、DatetimeIndex、resample、rolling、lag | 時間序列資料怎麼整理？ |
| [分解](decomposition.md) | 加法 / 乘法、Classical、STL | 趨勢與季節性各佔多少？ |
| [定態](stationarity.md) | ADF、KPSS、差分、log、Box-Cox | 序列穩定嗎？怎麼轉換？ |
| [自相關](autocorrelation.md) | ACF、PACF、Ljung-Box | 過去與現在有多相關？ |
| [ARIMA](arima.md) | AR、MA、ARIMA、階數選擇 | 怎麼建模相依結構？ |
| [季節性與 SARIMA](seasonality-sarima.md) | SARIMA、STL + ARIMA、Prophet | 怎麼處理季節性？ |
| [預測評估](forecast-evaluation.md) | MAE、RMSE、MASE、時間序列交叉驗證 | 預測準不準？ |

## 常用工具

| 套件 | 用途 |
| --- | --- |
| `pandas` | 時間索引、resample、rolling |
| `statsmodels` | ARIMA、SARIMAX、分解、ADF / KPSS |
| `pmdarima` | 自動選擇 ARIMA 階數 |
| `prophet` | 趨勢 + 季節性自動建模 |

> 相關應用：[Finance: Autocorrelation](autocorrelation.md#金融情境動能與均值回歸)、[時間序列異常偵測](../../machine-learning/unsupervised-learning/anomaly-detection/time-series-anomalies.md)。
