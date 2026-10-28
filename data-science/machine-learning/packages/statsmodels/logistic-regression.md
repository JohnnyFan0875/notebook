[Machine Learning](../../README.md) › [套件](../README.md) › [statsmodels](README.md) › 邏輯斯迴歸

# statsmodels：邏輯斯迴歸 (Logit)

用公式 API 配適邏輯斯迴歸，取得 odds ratio、信賴區間與檢定。模型解讀見 [統計：邏輯斯迴歸](../../../statistics/regression-analysis/logistic-regression.md)；以預測為目的的流程見 [ML：邏輯斯迴歸](../../supervised-learning/classification/logistic-regression.md)。

## 用法

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

df = pd.DataFrame({"x": [2, 3, 5, 6, 7, 9, 10, 11, 13, 15],
                   "y": [0, 0, 1, 0, 0, 1, 0, 1, 1, 1]})

model = smf.logit("y ~ x", data=df).fit(disp=0)      # disp=0：不印迭代過程
print(model.summary())

# 1. 係數（log-odds）→ odds ratio
model.params                        # Intercept −3.49、x 0.435
np.exp(model.params["x"])           # OR 1.54：x 每增加 1，勝算乘以 1.54
np.exp(model.conf_int().loc["x"])   # OR 的 95% CI：(0.92, 2.60) → 包含 1
model.pvalues["x"]                  # 0.10（Wald 檢定）
model.llr_pvalue                    # 0.034（概似比檢定：模型整體比只有截距好）
model.prsquared                     # 0.32（McFadden pseudo R²）

# 2. 預測機率與分類
model.predict(pd.DataFrame({"x": [4, 8, 12]}))   # 0.15, 0.50, 0.85
model.pred_table(threshold=0.5)                  # [[4, 1], [1, 4]]：列 = 實際、欄 = 預測

# 3. 邊際效果：x 增加 1 時機率平均改變多少（比 OR 直觀）
model.get_margeff().summary()
```

> Wald p 值 (0.10) 與概似比 p 值 (0.034) 結論不同：小樣本時 Wald 檢定較不可靠，概似比檢定通常較好。

## 完全分離 (Perfect Separation)

如果某個 x 的值能把 0 與 1 完全分開，MLE 不存在，係數會趨向無限大：

```python
sep = pd.DataFrame({"x": [2, 3, 5, 7, 9, 11, 13, 15],
                    "y": [0, 0, 0, 1, 1, 1, 1, 1]})     # x ≤ 5 全是 0、x ≥ 7 全是 1
smf.logit("y ~ x", data=sep).fit(disp=0).params
# PerfectSeparationWarning；Intercept −123.6、x 20.6 → 不能解讀
```

| 對策 | 做法 |
| --- | --- |
| 正則化 | `smf.logit(...).fit_regularized(alpha=...)`，或 sklearn `LogisticRegression`（預設 L2） |
| Firth 校正 | R `logistf`；小樣本、罕見事件的標準做法 |
| 合併類別 / 收集更多資料 | 造成分離的稀有類別 |

> 小樣本生醫資料（某個突變的病人全部有反應）很常遇到完全分離，看到極大的係數與 SE 時要先檢查。

## 其他相關模型

| 結果變數 | statsmodels |
| --- | --- |
| 二元 | `smf.logit`、`smf.probit` |
| 多類別（無序） | `smf.mnlogit` |
| 有序類別 | `statsmodels.miscmodels.ordinal_model.OrderedModel` |
| 計數 | `smf.poisson`、`smf.negativebinomial`，或 `smf.glm(..., family=sm.families.Poisson())`，見 [GLM 與計數模型](../../../statistics/regression-analysis/glm-count-models.md) |
| 群集 / 重複量測 | `smf.gee`、`smf.mixedlm` |

分類表現（AUC、閾值、校準）請在測試資料上用 sklearn 評估，見 [模型評估](../../evaluation/README.md)；配適指標見 [指標](metrics.md)。
