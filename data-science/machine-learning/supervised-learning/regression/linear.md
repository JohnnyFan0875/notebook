[Machine Learning](../../README.md) › [監督式學習](../README.md) › [迴歸](README.md) › 線性迴歸

# 線性迴歸 (Linear Regression)

用特徵的線性組合預測連續目標：$\hat{y} = \beta_0 + \beta_1 x_1 + \cdots + \beta_p x_p$，以最小平方法 (OLS, ordinary least squares) 估計係數，也就是最小化 [MSE](../../evaluation/mse-rmse.md)。它是迴歸問題的第一個 baseline。

這篇是 **ML 用法**（預測、驗證）。係數推論、假設檢查與統計觀點見 [簡單線性迴歸](../../../statistics/regression-analysis/simple-linear-regression.md)、[多元線性迴歸](../../../statistics/regression-analysis/multiple-linear-regression.md)、[statsmodels 線性迴歸](../../packages/statsmodels/linear-regression.md)。

## ML vs 統計的用法

| | ML（sklearn） | 統計（statsmodels） |
| --- | --- | --- |
| 目的 | 預測新資料 | 推論係數（效果大小、p 值、CI） |
| 評估 | 測試集 / CV 的 RMSE、R² | 係數 SE、殘差診斷、R² |
| 特徵數 | 可以很多（搭配正則化） | 通常少，且需有理論依據 |
| 輸出 | `coef_`、`predict()` | `summary()` 完整表格 |

## 用法

```python
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import root_mean_squared_error, r2_score

X, y = load_diabetes(return_X_y=True, as_frame=True)          # 10 個特徵，y = 一年後疾病進展
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 1. CV 估計泛化誤差
cv = KFold(5, shuffle=True, random_state=0)
-cross_val_score(LinearRegression(), X_train, y_train, cv=cv,
                 scoring="neg_root_mean_squared_error").mean()        # 54.9

# 2. 配適與測試
ols = LinearRegression().fit(X_train, y_train)
ols.score(X_train, y_train)                                           # 訓練 R² 0.528
r2_score(y_test, ols.predict(X_test))                                 # 測試 R² 0.453
root_mean_squared_error(y_test, ols.predict(X_test))                  # 53.9

# 3. 係數：標準化後才能比較大小
std_ols = make_pipeline(StandardScaler(), LinearRegression()).fit(X_train, y_train)
std_ols[-1].coef_      # bmi 25.6、s5 35.2、s1 −44.4、s2 24.6 …（每增加 1 SD 的效果）

# 4. 只有一個特徵時，X 也必須是 2D
x = np.array([1, 2, 3, 4, 5])
LinearRegression().fit(x.reshape(-1, 1), [2, 4, 5, 4, 5]).coef_      # [0.6]，截距 2.2
```

> `s1`（−44）與 `s2`（+25）係數方向相反且都很大，是因為兩者高度相關（總膽固醇與 LDL）：係數互相抵消，個別數值不穩定。這就是共線性，見 [Ridge](ridge.md)。

## 假設與問題

| 假設 / 問題 | 違反時 | 對策 |
| --- | --- | --- |
| 線性關係 | 系統性殘差型態 | 加多項式 / 交互作用項、轉換、改用樹模型 |
| 誤差變異相等 | 預測區間不準 | 轉換 y（log）、穩健 SE |
| 誤差獨立 | SE 低估 | [混合效應模型](../../../statistics/regression-analysis/mixed-effects-models.md)、分組驗證 |
| 共線性 | 係數不穩定、正負號怪異 | [Ridge](ridge.md)、[Elastic Net](elastic-net.md)、刪除冗餘特徵 |
| 離群值 | 係數被拉偏 | Huber 迴歸，見 [離群值處理](../../preprocessing/outlier-handling.md) |
| p 接近或超過 n | 過擬合、無唯一解 | 正則化，見 [高維小樣本](../../foundations/high-dimensional-data.md) |

> 只為預測時，常態性假設不重要；殘差圖仍然值得看，因為它會揭露漏掉的非線性與離群值。判讀方式見 [模型診斷](../../interpretability-and-diagnostics/model-diagnostics.md)。

## 非線性擴充

```python
from sklearn.preprocessing import PolynomialFeatures, SplineTransformer

make_pipeline(PolynomialFeatures(degree=2, include_bias=False), StandardScaler(), LinearRegression())
make_pipeline(SplineTransformer(n_knots=5, degree=3), LinearRegression())     # 平滑非線性
```

多項式次數越高越容易過擬合，見 [過擬合與欠擬合](../../foundations/overfitting-underfitting.md)；通常要搭配 [Ridge](ridge.md)。
