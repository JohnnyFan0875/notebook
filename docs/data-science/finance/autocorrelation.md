# Autocorrelation in Finance

自相關描述的是「現在的值與過去值之間有多像」。在金融資料中，它常用來判斷價格或報酬率是否存在延續性、反轉性，或某種尚未被模型解釋掉的時間依賴。

## 先分清楚：價格 vs 報酬率

- 價格序列通常帶有趨勢與非平穩性，因此很容易看起來有高自相關。
- 報酬率序列更常拿來做有效率市場、動能或均值回歸的判讀。
- 波動度或平方報酬率的自相關，也常用來觀察 volatility clustering。

## 如何解讀

- 正自相關：高值後面傾向還是高值，可能對應短期動能或趨勢延續。
- 負自相關：高值後面傾向轉低，可能對應均值回歸或短期反轉。
- 接近零：代表線性上的時間依賴很弱，但不表示完全沒有可預測性。

## 金融情境中的常見用途

1. 檢查報酬率是否存在短期動能或均值回歸。
2. 檢查模型殘差是否仍殘留時間結構。
3. 檢查平方報酬率是否有波動聚集現象。

## 常見陷阱

- 沒有先去趨勢或轉成報酬率，就直接判讀價格自相關。
- 把統計顯著當成可交易訊號，忽略交易成本與滑價。
- 用太高頻的資料卻忽略 bid-ask bounce 等微結構雜訊。

## Python Example

```python
import numpy as np
import pandas as pd
import seaborn as sns
from statsmodels.tsa.stattools import acf

df = sns.load_dataset("flights")
monthly_passengers = df["passengers"]
returns_like = monthly_passengers.pct_change().dropna()

acf_values = acf(returns_like, nlags=10)
pd.Series(acf_values, index=range(len(acf_values)))
```

## 實務判讀提醒

若你發現某個 lag 的自相關顯著，不要立刻下結論說「市場可預測」。下一步應該至少檢查：

- 這個結果是否只出現在特定期間？
- 換不同頻率或不同資產是否還存在？
- 加入交易成本後是否仍有經濟意義？

## Related Concepts

- [Time Series Autocorrelation](../statistics/time-series-analysis/autocorrelation.md)
- [Stationarity](../statistics/time-series-analysis/stationarity.md)
