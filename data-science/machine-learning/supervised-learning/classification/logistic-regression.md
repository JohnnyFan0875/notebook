[Machine Learning](../../README.md) › [監督式學習](../README.md) › [分類](README.md) › 邏輯斯迴歸

# 邏輯斯迴歸 (Logistic Regression)

雖然名字有「迴歸」，它是**分類**方法：用特徵的線性組合預測**對數勝算 (log-odds)**，再經 sigmoid 轉成機率。可解釋、訓練快、機率通常校準良好，是二元分類的標準 baseline。

這篇是 **ML 用法**（縮放、正則化、調參、評估）。odds ratio 解讀與 GLM 觀點見 [統計：邏輯斯迴歸](../../../statistics/regression-analysis/logistic-regression.md)；推論導向的用法見 [statsmodels 邏輯斯迴歸](../../packages/statsmodels/logistic-regression.md)。

## 模型

$$
\log \frac{p}{1-p} = \beta_0 + \beta_1 x_1 + \cdots + \beta_p x_p
\qquad\Longleftrightarrow\qquad
p = \frac{1}{1 + e^{-(\beta_0 + \beta^\top x)}}
$$

| 概念 | 說明 |
| --- | --- |
| 決策邊界 | $\beta^\top x = 0$（閾值 0.5 時），是一條**直線 / 超平面** |
| 係數 $\beta_j$ | $x_j$ 增加 1 單位，log-odds 增加 $\beta_j$；$e^{\beta_j}$ = odds ratio |
| 損失函數 | Log loss（= Bernoulli 負 log-likelihood），見 [損失函數](../../foundations/loss-functions.md) |
| 多類別 | sklearn 預設 multinomial（softmax）；舊參數 `multi_class` 已移除 |

## 用法

```python
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

X, y = load_breast_cancer(return_X_y=True, as_frame=True)
y = 1 - y                                      # 1 = 惡性
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

# C = 1/λ：越小正則化越強；l1_ratio：0 = L2、1 = L1（sklearn ≥ 1.8 寫法）
pipe = make_pipeline(StandardScaler(), LogisticRegression(solver="saga", max_iter=5000))
grid = {"logisticregression__C": [0.01, 0.1, 1, 10],
        "logisticregression__l1_ratio": [0, 0.5, 1]}
search = GridSearchCV(pipe, grid, cv=StratifiedKFold(5, shuffle=True, random_state=0), scoring="roc_auc")
search.fit(X_train, y_train)
search.best_params_            # C=1, l1_ratio=1（L1）
search.best_score_             # CV AUC 0.993
roc_auc_score(y_test, search.predict_proba(X_test)[:, 1])   # 0.998

# 係數 → 每增加 1 個標準差的 odds ratio
coef = pd.Series(search.best_estimator_[-1].coef_[0], index=X.columns)
(coef != 0).sum()                                        # L1 保留 15 / 30 個特徵
np.exp(coef).sort_values(ascending=False).head(3)        # radius error 12.9、worst texture 7.2、worst area 5.2
```

> 30 個特徵中半徑、周長、面積高度相關，個別 odds ratio 會隨正則化與特徵組合大幅變動，**不能當成獨立效果解讀**。要做係數推論請用少量、有理論依據的特徵配合 statsmodels。

## 常用參數

| 參數 | 說明 |
| --- | --- |
| `C` | 正則化強度的倒數；預設 1.0 |
| `l1_ratio` | 0（L2，預設）→ 1（L1），中間為 Elastic Net；L1 需 `saga` 或 `liblinear`，Elastic Net 只能 `saga` |
| `solver` | `lbfgs`（預設，L2）、`saga`（大資料、L1 / Elastic Net）、`liblinear`（小資料、二元） |
| `class_weight="balanced"` | 不平衡資料；會放大陽性機率，見 [類別不平衡](../../evaluation/class-imbalance.md) |
| `max_iter` | 不收斂（`ConvergenceWarning`）時加大；先確認有標準化 |

> sklearn 1.8 起 `penalty=` 已 deprecated（預計 1.10 移除），改用 `l1_ratio`；`C=np.inf` 等於不正則化。

## 何時用、限制

| 適合 | 限制 / 對策 |
| --- | --- |
| 任何二元分類的第一個 baseline | 只能畫線性邊界 → 加多項式 / 交互作用特徵，或改用樹模型 |
| 高維小樣本（基因表現）：搭配 L1 / Elastic Net | 共線時係數不穩 → L2 / Elastic Net |
| 需要可信的機率（風險分數） | 對離群值敏感 → 檢查 [離群值處理](../../preprocessing/outlier-handling.md) |
| 需要解釋方向與大小 | 完全可分 (perfect separation) 時無正則化的係數會發散 → 正則化 |

> 臨床預測模型（風險評分）常用邏輯斯迴歸，不只因為簡單：它的機率校準好、係數可審查，而且在中小型表格資料上常和複雜模型差不多準。乳癌資料上它的 CV AUC (0.992) 和 SVM、XGBoost、stacking 都在 0.99 左右。
