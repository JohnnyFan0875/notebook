[Machine Learning](../README.md) › 套件

# 套件 (Packages)

把套件語法和概念筆記分開：先在概念頁弄懂「為什麼」，再來這裡查「怎麼寫」。

| 套件 | 定位 | 筆記 |
| --- | --- | --- |
| scikit-learn | 預測建模：pipeline、交叉驗證、前處理、模型比較 | [scikit-learn 速查](scikit-learn/README.md) |
| statsmodels | 統計推論：係數、p 值、信賴區間、診斷、ANOVA | [statsmodels](statsmodels/README.md) |

## 該用哪一個

| 需求 | 用 |
| --- | --- |
| 預測新資料、比較模型、上線 | scikit-learn |
| 係數的 p 值、信賴區間、完整摘要表 | statsmodels |
| R 風格的公式（`y ~ x1 + C(group)`） | statsmodels |
| 交叉驗證、調參、pipeline | scikit-learn |
| ANOVA、事後檢定、迴歸診斷 | statsmodels |
| 兩者都要 | 用 statsmodels 解讀係數，用 scikit-learn 做驗證與預測流程 |

> 同一個模型，兩個套件的預設可能不同：sklearn 的 `LogisticRegression` **預設有 L2 正則化**（`C=1.0`），係數會被縮小；statsmodels 的 `logit` 是未懲罰的最大概似估計。要比較係數時記得設 `C=np.inf` 或使用 statsmodels。
