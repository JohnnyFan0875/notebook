[視覺化](../README.md) › [Seaborn](README.md) › 迴歸圖

# 迴歸圖 (Regression Plots)

在散布圖上疊加擬合的迴歸線與信賴帶，並用殘差圖檢查模型假設。Seaborn 的迴歸圖只用於**視覺化**，不輸出係數或 p 值；要做推論用 statsmodels，見 [簡單線性迴歸](../../../statistics/regression-analysis/simple-linear-regression.md)。

## 迴歸線

```python
import seaborn as sns
import matplotlib.pyplot as plt

iris = sns.load_dataset("iris")
tips = sns.load_dataset("tips")
fig, axes = plt.subplots(1, 3, figsize=(14, 4), layout="constrained")

# 1. 線性 + 95% CI 帶（bootstrap）
sns.regplot(data=iris, x="sepal_length", y="petal_length", ax=axes[0])

# 2. 多項式 / 穩健迴歸 / LOWESS 平滑
sns.regplot(data=iris, x="sepal_length", y="petal_length", order=2, ci=None, ax=axes[1])

# 3. 邏輯斯迴歸：y 必須是 0/1 數值，字串類別會報錯；需要 statsmodels
tips["smoker_yes"] = (tips["smoker"] == "Yes").astype(int)
sns.regplot(data=tips, x="total_bill", y="smoker_yes", logistic=True, ci=None,
            y_jitter=0.03, scatter_kws={"alpha": 0.3}, ax=axes[2])

# figure-level：每個物種各自一條線
sns.lmplot(data=iris, x="sepal_length", y="petal_length", hue="species", ci=None, height=4)
```

| 參數 | 用途 |
| --- | --- |
| `ci` | 迴歸線信賴帶，預設 95；`None` 不畫（`regplot` 仍用 `ci=`，不是 `errorbar=`） |
| `order=n` | n 次多項式 |
| `logistic=True` | 邏輯斯迴歸（y 為 0/1） |
| `lowess=True` | 局部加權平滑，看非線性趨勢 |
| `robust=True` | 降低離群值影響 |
| `x_bins` / `x_estimator` | x 分箱後畫各箱平均 ± CI，點很多時清楚 |
| `x_jitter` / `y_jitter` | 只影響點的顯示位置，不影響擬合 |
| `truncate=False` | 迴歸線延伸到整個 x 軸範圍 |

> `lmplot(hue=...)` 的每條線是**分開擬合**；斜率與截距等同於 `petal_length ~ sepal_length * species` 交互作用模型的各組估計，不是控制物種後的共同斜率。Simpson's paradox（合併後斜率方向與各組相反）就靠這種分組迴歸線發現，見 [多變量探索](../../../statistics/multivariate-analysis/multivariate-eda.md#simpsons-paradox)。

## 殘差與診斷圖

```python
import numpy as np
import statsmodels.api as sm

# 1. residplot：先擬合 y ~ x，再畫 (x, 殘差)；x 軸是預測變數，不是 fitted values
sns.residplot(data=iris, x="sepal_length", y="petal_length", lowess=True,
              line_kws={"color": "tomato"})

# 2. 用 statsmodels 模型畫 Q-Q 與 Scale-Location
model = sm.OLS(iris["petal_length"], sm.add_constant(iris["sepal_length"])).fit()
std_resid = model.get_influence().resid_studentized_internal

fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
sm.qqplot(std_resid, line="45", ax=axes[0])           # 標準化殘差才能對 45° 線；原始殘差用 line="s"
sns.regplot(x=model.fittedvalues, y=np.sqrt(np.abs(std_resid)), lowess=True,
            line_kws={"color": "tomato"}, ax=axes[1])
axes[1].set(xlabel="Fitted values", ylabel="√|standardized residuals|", title="Scale-Location")
```

| 圖 | 理想樣子 | 有問題時 |
| --- | --- | --- |
| 殘差 vs x / fitted | 點隨機散在 0 附近，平滑線水平 | U 形 → 非線性；漏斗形 → 異質變異 |
| Q-Q plot | 點貼著對角線 | 尾巴翹起 → 重尾或偏態 |
| Scale-Location | 平滑線大致水平 | 線上升 → 變異隨 fitted 增加 |

四張診斷圖的完整判讀、槓桿與 Cook's distance 見 [模型假設與診斷](../../../statistics/multivariate-analysis/assumptions-diagnostics.md#四張診斷圖)。
