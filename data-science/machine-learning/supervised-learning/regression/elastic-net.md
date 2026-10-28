[Machine Learning](../../README.md) › [監督式學習](../README.md) › [迴歸](README.md) › Elastic Net

# Elastic Net 迴歸 (Elastic Net Regression)

Elastic Net 同時加上 L1 與 L2 懲罰：既能把部分係數壓成 0（像 [Lasso](lasso.md)），又能讓相關特徵**一起**被保留、平分權重（像 [Ridge](ridge.md)）。特徵很多且彼此高度相關時（基因共表現、同一 pathway）常是最實用的折衷。

$$
\min_\beta \frac{1}{2n}\sum_i (y_i - x_i^\top\beta)^2 + \alpha \Big( \rho \sum_j \lvert\beta_j\rvert + \frac{1-\rho}{2} \sum_j \beta_j^2 \Big)
$$

| 參數 | 意義 |
| --- | --- |
| `alpha` | 整體懲罰強度 |
| `l1_ratio`（ρ） | L1 的比例：1 = Lasso、0 = Ridge |

## 相關特徵的行為

兩個幾乎相同的特徵（相關 0.997）共同代表一個效果（合計 = 3），5 次 bootstrap：

| 方法 | (β₁, β₂) | 行為 |
| --- | --- | --- |
| OLS | (3.62, −0.65)、(1.26, 1.64)、(3.13, −0.09)… | 不穩定，正負號會翻 |
| Lasso (`alpha=0.1`) | (2.86, **0**)、(1.25, 1.56)、(2.95, **0**)、(1.96, 1.01)、(1.40, 1.61) | 有時丟掉其中一個，丟哪個看運氣 |
| Elastic Net (`alpha=0.1, l1_ratio=0.5`) | (1.49, 1.33)、(1.38, 1.40)、(1.53, 1.38)、(1.49, 1.45)、(1.48, 1.50) | **穩定平分**（grouping effect） |

> 生資的意義：Lasso 從一群共表現基因中「選出」的那個基因，換一批樣本就可能換人；Elastic Net 會保留整群，生物學解讀較穩定。

## 用法

```python
from sklearn.model_selection import KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNetCV

# 同時用 CV 選 alpha 與 l1_ratio；l1_ratio 偏向 1 的值較有意義（官方建議多放接近 1 的值）
enet = make_pipeline(StandardScaler(),
                     ElasticNetCV(l1_ratio=[0.1, 0.5, 0.7, 0.9, 0.95, 1], cv=KFold(5, shuffle=True, random_state=0)))
enet.fit(X_train, y_train)          # 承 Ridge 筆記的 diabetes 切分
enet[-1].alpha_, enet[-1].l1_ratio_  # 0.085, 0.9
root_mean_squared_error(y_test, enet.predict(X_test))      # 53.7

# 分類版本：LogisticRegression(l1_ratio=0.5, solver="saga")
```

diabetes 上 OLS、Ridge、Lasso、Elastic Net 的測試 RMSE 都在 53.6–53.9 之間：低維資料上正則化的差異很小，差別出現在高維、共線的資料。

## 比較

| | Ridge | Lasso | Elastic Net |
| --- | --- | --- | --- |
| 係數歸零 | 否 | 是 | 是 |
| 相關特徵 | 平分 | 任選一個 | 一起保留 |
| p > n | 可用 | 最多選 n 個 | 可選超過 n 個 |
| 要調的參數 | `alpha` | `alpha` | `alpha`、`l1_ratio` |

## 常見錯誤

| 錯誤 | 改正 |
| --- | --- |
| 沒標準化就配適、比較係數 | 放進 pipeline 先 `StandardScaler` |
| 只調 `alpha`，`l1_ratio` 固定 0.5 | 兩者一起用 CV 選 |
| 把係數 = 0 解讀成「不重要」或「無因果」 | 可能只是被相關特徵取代 |
| 假設 Elastic Net 一定比較好 | 和 Ridge、Lasso 一起比較 CV 分數 |
