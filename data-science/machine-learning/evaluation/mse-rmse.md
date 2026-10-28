[Machine Learning](../README.md) › [模型評估](README.md) › 迴歸指標

# 迴歸指標：MSE、RMSE 與其他 (Regression Metrics)

連續目標的預測誤差指標。MSE / RMSE 最常用，但它們對大誤差特別敏感；選指標要看「哪種錯誤代價高」。它們同時也是訓練損失，兩者的區別見 [損失函數](../foundations/loss-functions.md)。

## 指標比較

| 指標 | 公式 | 單位 | 特性 | 何時用 |
| --- | --- | --- | --- | --- |
| MSE | $\frac{1}{n}\sum (y_i - \hat{y}_i)^2$ | 平方單位 | 大誤差懲罰最重；對離群值敏感 | 最佳化、數學推導 |
| RMSE | $\sqrt{\text{MSE}}$ | **同 y** | 同 MSE，但可直接解讀 | 報告的預設選擇 |
| MAE | $\frac{1}{n}\sum \lvert y_i - \hat{y}_i \rvert$ | 同 y | 穩健；每單位誤差同等重要 | 有離群值、誤差成本線性 |
| R² | $1 - \frac{\text{SSE}}{\text{SST}}$ | 無單位 | 相對於「預測平均數」的改善比例 | 跨資料集比較；可為負 |
| MAPE | $\frac{1}{n}\sum \left\lvert \frac{y_i - \hat{y}_i}{y_i} \right\rvert$ | % | 相對誤差 | y 遠離 0 的情況（銷售）；y 接近 0 時爆炸 |
| RMSLE | RMSE of $\log(1+y)$ | — | 懲罰比例誤差、低估比高估重 | 右偏目標（價格、計數） |

> RMSE ≥ MAE 永遠成立；兩者差距越大，代表誤差中有越多大誤差。

```python
import numpy as np
from sklearn.metrics import (mean_squared_error, root_mean_squared_error, mean_absolute_error,
                             r2_score, mean_absolute_percentage_error)

y_true = np.array([3, -0.5, 2, 7])
y_pred = np.array([2.5, 0.0, 2, 8])

mean_squared_error(y_true, y_pred)        # 0.375
root_mean_squared_error(y_true, y_pred)   # 0.612   sklearn ≥ 1.4
mean_absolute_error(y_true, y_pred)       # 0.5
r2_score(y_true, y_pred)                  # 0.949

# CV / GridSearchCV 的 scoring 字串（誤差類取負號，越大越好）
scoring = "neg_root_mean_squared_error"   # 也有 neg_mean_absolute_error、r2
```

> 舊寫法 `mean_squared_error(..., squared=False)` 在 sklearn 1.4 deprecated、1.6 移除，改用 `root_mean_squared_error`。

## 解讀

| 情境 | 判讀方式 |
| --- | --- |
| RMSE 本身 | 和 y 的 SD、和 [baseline](baselines-and-error-analysis.md)（預測平均數）的 RMSE 比；單看數字沒有意義 |
| R² = 0 | 等於預測平均數；**測試集 R² 可以為負**（比預測平均還差） |
| 訓練 R² 很高、測試 R² 低 | [過擬合](../foundations/overfitting-underfitting.md) |
| 只看單一數字 | 會漏掉「高值區系統性低估」這類問題 → 畫預測 vs 實際、殘差圖，見 [模型診斷](../interpretability-and-diagnostics/model-diagnostics.md) |

diabetes 資料的例子：預測平均數的 RMSE 71.4，Ridge 55.7、MAE 44.7、R² 0.39，見 [Baseline 與錯誤分析](baselines-and-error-analysis.md)。

> 統計迴歸的 R²、調整後 R² 與係數推論見 [迴歸分析](../../statistics/regression-analysis/README.md)；這裡的重點是**樣本外**預測誤差。
