[Machine Learning](../../README.md) › [套件](../README.md) › [statsmodels](README.md) › 線性迴歸

# statsmodels：線性迴歸 (OLS)

用公式 API 配適最小平方法迴歸，取得係數、推論與預測區間。概念見 [統計：多元線性迴歸](../../../statistics/regression-analysis/multiple-linear-regression.md)；以預測為目的的 sklearn 用法見 [線性迴歸](../../supervised-learning/regression/linear.md)。

## 用法

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

df = pd.DataFrame({"x": [1, 2, 3, 4, 5],
                   "y": [2, 4, 5, 4, 5]})

model = smf.ols("y ~ x", data=df).fit()

# 1. 係數與推論
model.params            # Intercept 2.2、x 0.6
model.conf_int()        # x 的 95% CI：(−0.30, 1.50) → 包含 0，n=5 時證據不足
model.pvalues
model.rsquared          # 0.6
print(model.summary())  # 完整摘要表

# 2. 樣本內
model.fittedvalues      # 配適值
model.resid             # 殘差

# 3. 新資料：點預測 + 兩種區間
new = pd.DataFrame({"x": [6, 7, 8]})
model.predict(new)                                       # 5.8, 6.4, 7.0
model.get_prediction(new).summary_frame(alpha=0.05)
# x=6：mean 5.8；平均值的 CI (2.81, 8.79)；單一觀測的預測區間 (1.68, 9.92)
```

| 區間 | 欄位 | 意義 |
| --- | --- | --- |
| 信賴區間 (CI) | `mean_ci_lower/upper` | 「x = 6 的**平均** y」落在哪裡 |
| 預測區間 (PI) | `obs_ci_lower/upper` | 「下一個 x = 6 的**單一觀測**」落在哪裡；永遠比 CI 寬 |

## 讀 `summary()`

| 區塊 | 欄位 | 看什麼 |
| --- | --- | --- |
| 上方 | R-squared、Adj. R-squared | 解釋變異比例，見 [指標](metrics.md) |
| 上方 | F-statistic、Prob (F-statistic) | 所有係數是否同時為 0 |
| 上方 | AIC、BIC | 比較模型（越小越好） |
| 係數表 | coef、std err | 估計值與標準誤 |
| 係數表 | t、P>\|t\| | 個別係數的檢定 |
| 係數表 | [0.025, 0.975] | 95% 信賴區間 |
| 下方 | Durbin-Watson | 殘差自相關（≈ 2 表示無） |
| 下方 | Omnibus、Jarque-Bera | 殘差常態性 |
| 下方 | Cond. No. | 很大（> 1000 量級）暗示共線性或尺度問題 |

## 係數解讀

| 模型 | 係數意義 |
| --- | --- |
| `y ~ x` | x 增加 1，y 平均改變 β |
| `np.log(y) ~ x` | x 增加 1，y 約變為 $e^{\beta}$ 倍（β 小時約 β × 100%） |
| `y ~ np.log(x)` | x 增加 1%，y 約改變 β / 100 |
| `y ~ C(group)` | 各組相對參考組的平均差 |
| `y ~ x1 * x2` | x1 的效果隨 x2 改變（看交互作用項） |

## 穩健標準誤

殘差變異不相等（異質變異）或資料分群時，係數不變但標準誤會錯：

```python
model.get_robustcov_results(cov_type="HC3")                     # 異質變異穩健
smf.ols("y ~ x", data=df).fit(cov_type="cluster",
                              cov_kwds={"groups": df["patient_id"]})   # 同一病人多筆資料
```

配適後一定要做 [診斷](diagnostics.md)：殘差圖、影響點、共線性。
