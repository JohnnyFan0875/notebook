[Machine Learning](../../README.md) › [套件](../README.md) › statsmodels

# statsmodels

Python 的統計建模與推論套件：給出係數、標準誤、p 值、信賴區間與完整摘要表，語法接近 R。本筆記以 statsmodels 0.15 驗證。統計觀念本身見 [統計：迴歸分析](../../../statistics/regression-analysis/README.md)。

## 建議順序

```
線性迴歸（公式 API、summary）→ 診斷（殘差、影響點）→ 指標 → 邏輯斯迴歸 → ANOVA
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [線性迴歸](linear-regression.md) | `ols`、`summary()`、預測區間 | 係數多大？顯著嗎？ |
| [診斷](diagnostics.md) | 殘差、leverage、Cook's D、DFFITS、VIF | 結果是不是被少數點或違反假設驅動？ |
| [指標](metrics.md) | R²、調整 R²、`mse_resid`、AIC / BIC、pseudo R² | 模型配適得多好？ |
| [邏輯斯迴歸](logistic-regression.md) | `logit`、odds ratio、完全分離 | 二元結果的效果大小？ |
| [ANOVA](anova.md) | 單因子、雙因子、ANCOVA、Type II / III、Tukey | 組別平均有差嗎？ |

## 兩種 API

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf

# 1. 公式 API（推薦）：自動加截距、處理類別變數
model = smf.ols("y ~ x1 + x2 + C(group)", data=df).fit()

# 2. 陣列 API：要自己加截距
X = sm.add_constant(df[["x1", "x2"]])
model = sm.OLS(df["y"], X).fit()
```

| 公式語法 | 意義 |
| --- | --- |
| `y ~ x1 + x2` | 兩個主效果 |
| `y ~ x1 * x2` | 主效果 + 交互作用（= `x1 + x2 + x1:x2`） |
| `C(group)` | 當作類別變數（dummy 編碼） |
| `C(group, Treatment(reference="B"))` | 指定參考組 |
| `np.log(y) ~ x`、`I(x**2)` | 在公式內轉換 |
| `y ~ x - 1` | 不要截距 |

## statsmodels vs scikit-learn

| 面向 | statsmodels | [scikit-learn](../scikit-learn/README.md) |
| --- | --- | --- |
| 目的 | 統計推論、假設檢定 | 預測、ML 流程 |
| API | 公式（類似 R） | 物件導向 `fit(X, y)` |
| 輸出 | p 值、CI、檢定統計量 | 預測值、少量統計資訊 |
| 預設正則化 | 無 | 部分模型有（`LogisticRegression` 預設 L2） |
| 驗證 | 樣本內診斷 | 交叉驗證、pipeline |
| 適合 | 研究、需要解釋係數 | 上線、模型比較 |

> 兩者互補：用 statsmodels 理解效果與檢查假設，用 scikit-learn 做交叉驗證與預測流程。
