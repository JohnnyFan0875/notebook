[Machine Learning](../../README.md) › [監督式學習](../README.md) › [迴歸](README.md) › Ridge

# Ridge 迴歸 (Ridge Regression)

[線性迴歸](linear.md) 加上 **L2 懲罰** $\lambda \sum \beta_j^2$（也叫 Tikhonov 正則化）：係數被拉向 0 但不會剛好為 0。主要用途是**穩定共線特徵的係數**、降低變異。原理與 Lasso / Elastic Net 的比較見 [正則化](../../foundations/regularization.md)。

$$
\hat{\beta}_{ridge} = \arg\min_\beta \sum_i (y_i - x_i^\top \beta)^2 + \alpha \sum_j \beta_j^2
$$

| `alpha` | 效果 |
| --- | --- |
| → 0 | 等於 OLS |
| 增大 | 係數整體縮小，偏誤 ↑、變異 ↓ |
| → ∞ | 所有係數 → 0，只剩截距 |

## 用法

```python
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeCV
from sklearn.metrics import root_mean_squared_error

X, y = load_diabetes(return_X_y=True, as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 懲罰對量尺敏感 → 先標準化；RidgeCV 內建高效的留一交叉驗證選 alpha
ridge = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 3, 61))).fit(X_train, y_train)
ridge[-1].alpha_                                           # 1.26
root_mean_squared_error(y_test, ridge.predict(X_test))     # 53.8（OLS 53.9、預測平均 73.2）
```

diabetes 只有 10 個特徵、442 筆，Ridge 和 OLS 的預測幾乎一樣；它的價值在特徵多、共線嚴重或 p 接近 n 時才明顯。

## 共線性下的穩定性

兩個幾乎相同的特徵（相關 0.997）共同代表一個真實效果（合計 = 3）。對資料做 5 次 bootstrap 重新配適，前兩個係數：

| 方法 | 5 次 bootstrap 的 (β₁, β₂) | 觀察 |
| --- | --- | --- |
| OLS | (3.62, −0.65)、(1.26, 1.64)、(3.13, −0.09)、(1.95, 1.13)、(1.51, 1.59) | 劇烈擺盪、正負號會翻轉 |
| Ridge (`alpha=1`) | (2.07, 0.89)、(1.38, 1.51)、(2.06, 0.96)、(1.66, 1.41)、(1.53, 1.56) | 較穩定，傾向平分 |

兩者的總和都約為 3，預測幾乎一樣；差別在**係數能不能被解讀**。Lasso 與 Elastic Net 的對照見 [Elastic Net](elastic-net.md#相關特徵的行為)。

## 何時用

| 適合 | 不適合 |
| --- | --- |
| 很多特徵、彼此相關（基因表現、光譜、問卷題組） | 需要稀疏模型、自動挑特徵 → [Lasso](lasso.md) |
| p 接近或大於 n | 需要係數的 p 值 → 用未懲罰模型，見 [statsmodels](../../packages/statsmodels/README.md) |
| 多項式 / 樣條展開後的高維特徵 | — |

> 分類問題的 L2 正則化就是 `LogisticRegression` 的預設（`C` = 1/alpha），見 [邏輯斯迴歸](../classification/logistic-regression.md)。Ridge 等價於係數有常態先驗的 MAP 估計，見 [正則化 ↔ 貝氏先驗](../../foundations/regularization.md#正則化--貝氏先驗)。
