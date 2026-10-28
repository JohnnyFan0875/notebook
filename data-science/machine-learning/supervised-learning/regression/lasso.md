[Machine Learning](../../README.md) › [監督式學習](../README.md) › [迴歸](README.md) › Lasso

# Lasso 迴歸 (Lasso Regression)

Lasso (Least Absolute Shrinkage and Selection Operator) 是 [線性迴歸](linear.md) 加上 **L1 懲罰** $\lambda \sum \lvert\beta_j\rvert$：部分係數會**剛好變成 0**，等於同時做 [特徵選擇](../../preprocessing/feature-selection.md)。係數路徑圖見 [正則化](../../foundations/regularization.md)。

$$
\hat{\beta}_{lasso} = \arg\min_\beta \frac{1}{2n}\sum_i (y_i - x_i^\top \beta)^2 + \alpha \sum_j \lvert\beta_j\rvert
$$

| `alpha` | 效果 |
| --- | --- |
| 小 | 接近 OLS，多數係數非 0 |
| 增大 | 越來越多係數歸零 |
| 大到某值以上 | 全部係數 = 0 |

## 用法

```python
import numpy as np
from sklearn.model_selection import KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LassoCV

# 承 Ridge 筆記的 diabetes 切分
lasso = make_pipeline(StandardScaler(), LassoCV(cv=KFold(5, shuffle=True, random_state=0)))
lasso.fit(X_train, y_train)
lasso[-1].alpha_                         # 0.219  CV 選出的 alpha
(lasso[-1].coef_ != 0).sum()             # 10     這個 alpha 下沒有特徵被丟掉
root_mean_squared_error(y_test, lasso.predict(X_test))     # 53.6

# 想要更稀疏：用較大的 alpha（例如 CV 誤差在最小值 1 個標準誤內的最大 alpha，「1-SE rule」）
mse = lasso[-1].mse_path_.mean(axis=1); se = lasso[-1].mse_path_.std(axis=1) / np.sqrt(5)
alpha_1se = lasso[-1].alphas_[mse <= mse.min() + se[mse.argmin()]].max()
# alpha_1se ≈ 4.1 → 只剩 5 個特徵：sex、bmi、bp、s3、s5
```

> 只有 10 個特徵且都有些用處時，CV 最佳的 Lasso 不一定會丟特徵（如上）。Lasso 的稀疏性在 p 很大、真正相關的特徵很少時才顯著；`alpha=10` 時 diabetes 只剩 4 個特徵（見 [正則化](../../foundations/regularization.md) 的係數路徑）。R `glmnet` 預設報告的 `lambda.1se` 就是 1-SE rule。

## 特性與限制

| 特性 | 說明 |
| --- | --- |
| 自動特徵選擇 | 係數為 0 的特徵等於被移除 |
| 相關特徵中**任選一個** | 一群高度相關的特徵，Lasso 常只留一個，且留哪個不穩定 → [Elastic Net](elastic-net.md#相關特徵的行為) |
| p > n 時最多選 n 個特徵 | 高維資料（基因數 ≫ 樣本數）下的限制 |
| 係數有偏 | 被縮向 0；要不偏的效果估計可在選出的特徵上重新配適 OLS（relaxed lasso），但推論仍有選擇後偏誤 |
| 選出的特徵不等於「重要」或「因果」 | 換個子樣本可能選出不同的特徵；用 bootstrap 看被選中頻率 |

> 分類版本：`LogisticRegression(l1_ratio=1, solver="saga")`（sklearn ≥ 1.8；舊版寫 `penalty="l1"`），見 [邏輯斯迴歸](../classification/logistic-regression.md)。高維生資資料的完整建模流程見 [高維小樣本](../../foundations/high-dimensional-data.md)。
