[Statistics](../README.md) › [時間序列](README.md) › 基礎

# 時間序列基礎 (Time Series Fundamentals)

一般統計假設觀測獨立同分配 (i.i.d.)；時間序列違反這個假設：昨天的股價影響今天、上個月的銷售影響本月庫存。

## 四種成分

| 成分 | 說明 | 例子 |
| --- | --- | --- |
| 趨勢 (trend, T) | 長期上升或下降 | 全球氣溫上升 |
| 季節性 (seasonality, S) | **固定週期**的規律 | 每年 12 月銷售高峰、晝夜節律 |
| 循環 (cyclicality, C) | 長期波動，**沒有固定週期** | 景氣循環（3–10 年不等） |
| 不規則 (irregular, I) | 隨機雜訊 | 單一事件、量測誤差 |

季節性週期固定，循環不固定。多數古典模型明確處理季節性，循環則併入趨勢。

## pandas 時間序列操作

正確的 **DatetimeIndex** 與**頻率 (freq)** 是一切的前提；沒設好，statsmodels 幾乎一定出錯。

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

df = sm.datasets.co2.load_pandas().data.rename(columns={"co2": "CO2"})
df = df.asfreq("W-SAT").interpolate()      # 設定頻率並補值
df.index.freq, df.index.min(), df.index.max()

# 頻率字串：'D' 日、'B' 營業日、'W' 週、'MS' 月初、'ME' 月底、'QS' 季初、'YS' 年初、'h' 小時、'min' 分鐘

df.resample("MS").mean()                    # 降頻：週 → 月平均
df["CO2"].rolling(12, center=True).mean()   # 移動平均（平滑、看局部趨勢）
df["CO2"].rolling(12, center=True).std()    # 移動標準差（看變異是否改變）
df["CO2"].shift(1)                          # 落後一期 (lag)，AR 模型與自相關的基礎
df["CO2"].diff(1)                           # 一階差分：去除趨勢
df["CO2"].diff(52)                          # 季節差分：去除年週期（週資料 m = 52）
np.log(df["CO2"]).diff()                    # log + 差分 ≈ 成長率
```

### 事件紀錄轉時間序列

感測器 / IoT / 日誌資料常是長格式 `timestamp, device, value`：

```python
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")             # Unix 毫秒
wide = df.pivot_table(index="timestamp", columns="device", values="value")

# 不同頻率的來源對齊
env = pd.concat([temp, sun], axis=1)
env.resample("1h").agg({"temperature": "max", "sunshine": "sum"})          # 定義共同頻率與彙總方式
env.ffill()                                                               # 假設上次讀值持續有效
```

> `ffill()` 適合狀態型量測（溫度），不適合累積計數或突發事件計數。先想清楚分析單位：單一裝置隨時間、同時間多裝置、還是跨裝置的彙總。

## 建模前的視覺檢查

| 問題 | 看什麼 | 意義 |
| --- | --- | --- |
| 有趨勢嗎？ | 長期漂移 | 需要差分或去趨勢 |
| 有季節性嗎？ | 規律重複 | SARIMA 或分解 |
| 變異隨時間變大嗎？ | 振幅隨水準增加 | 乘法模型或 log 轉換 |
| 結構斷點或離群？ | 突然的水準移動、尖峰 | 介入變數或穩健方法 |

> **log + 差分**是經濟 / 商業資料最常見的前處理：常把非定態、乘法結構的序列轉成近似定態。下一步見 [分解](decomposition.md) 與 [定態](stationarity.md)。
