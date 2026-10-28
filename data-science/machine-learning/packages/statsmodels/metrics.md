[Machine Learning](../../README.md) › [套件](../README.md) › [statsmodels](README.md) › 指標

# statsmodels：模型配適指標 (Fit Metrics)

statsmodels 結果物件內建的配適指標，以及它們和 sklearn 指標的差別。這些都是**樣本內**指標；預測能力要用測試集或交叉驗證，見 [迴歸指標](../../evaluation/mse-rmse.md)。

## 線性迴歸 (`ols(...).fit()`)

| 指標 | 屬性 | 公式 | 說明 |
| --- | --- | --- | --- |
| R² | `rsquared` | $1 - SS_{res}/SS_{tot}$ | 解釋變異比例；加變數只會上升 |
| 調整 R² | `rsquared_adj` | $1 - (1-R^2)\frac{n-1}{n-p-1}$ | 懲罰變數數量 |
| 殘差平方和 | `ssr` | $\sum (y_i - \hat{y}_i)^2$ | — |
| **殘差均方** | `mse_resid` | $SS_{res} / (n - p - 1)$ | **除以殘差自由度**，是誤差變異 σ² 的不偏估計；**不是** sklearn 的 MSE |
| 殘差標準誤 | `np.sqrt(mse_resid)` | — | R `summary()` 的 Residual standard error |
| AIC / BIC | `aic`、`bic` | 依 log-likelihood 與參數數 | 比較模型，越小越好 |
| 整體 F 檢定 | `fvalue`、`f_pvalue` | — | 所有斜率是否同時為 0 |

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.tools.eval_measures import rmse

df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [2, 4, 5, 4, 5]})
model = smf.ols("y ~ x", data=df).fit()

model.rsquared                  # 0.6
model.ssr                       # 2.4
model.mse_resid                 # 0.8  = 2.4 / (5 − 2)
np.mean(model.resid ** 2)       # 0.48 = 2.4 / 5   ← 這才是 sklearn 的 mean_squared_error
rmse(df["y"], model.predict(df))  # 0.693 = √0.48
np.mean(np.abs(model.resid))    # MAE
```

> 小樣本時兩種「MSE」差很多（0.8 vs 0.48）。比較 statsmodels 與 sklearn 的結果、或和他人報告的數字對照時，先確認除以 n 還是 n − p − 1。

## 邏輯斯迴歸 (`logit(...).fit()`)

| 指標 | 屬性 | 說明 |
| --- | --- | --- |
| McFadden pseudo R² | `prsquared` | $1 - \ell_{model}/\ell_{null}$；**數值通常遠低於線性迴歸的 R²**，0.2–0.4 已算配適良好 |
| 概似比檢定 | `llr`、`llr_pvalue` | 模型是否比只有截距好 |
| Log-likelihood | `llf`、`llnull` | — |
| AIC / BIC | `aic`、`bic` | 比較模型 |
| 分類表 | `pred_table(threshold=0.5)` | 樣本內的混淆矩陣 |

pseudo R² 不能解讀成「解釋了多少變異」。分類表現（AUC、precision、recall）應在測試資料上用 sklearn 計算，見 [混淆矩陣指標](../../evaluation/confusion-metrics.md)、[ROC 與 AUC](../../evaluation/roc-auc.md)。

## 指標怎麼選

| 目的 | 指標 |
| --- | --- |
| 描述配適程度 | R²、調整 R²（線性）；pseudo R²（邏輯斯） |
| 比較非巢狀模型 | AIC、BIC |
| 比較巢狀模型 | 概似比檢定（`compare_lr_test`）、F 檢定（`compare_f_test`） |
| 誤差大小 | 殘差標準誤 `sqrt(mse_resid)`；預測誤差用測試集 RMSE |
| 預測能力 | **交叉驗證或測試集**，不是樣本內指標 |
