[Machine Learning](../README.md) › [模型評估](README.md) › Baseline 與錯誤分析

# Baseline 與錯誤分析 (Baselines and Error Analysis)

比較複雜模型之前，先建一個簡單的 baseline；選出有潛力的模型之後，回頭研究它錯在哪裡。

## Baseline

| 任務 | Baseline | sklearn |
| --- | --- | --- |
| 迴歸 | 預測平均數 / 中位數 | `DummyRegressor(strategy="mean")` |
| 迴歸 | 簡單 [線性迴歸](../supervised-learning/regression/linear.md) | `LinearRegression`、`Ridge` |
| 分類 | 永遠猜多數類別 | `DummyClassifier(strategy="most_frequent")` |
| 分類 | 依類別比例隨機猜 | `DummyClassifier(strategy="stratified")` |
| 分類 | 簡單 [邏輯斯迴歸](../supervised-learning/classification/logistic-regression.md) | `LogisticRegression` |
| 時間序列 | 最後一個值（naive）、去年同期（seasonal naive） | 見 [預測評估](../../statistics/time-series-analysis/forecast-evaluation.md#一定要比較基準模型-baselines) |
| 生醫 | 現行臨床評分、單一已知 biomarker | — |

```python
from sklearn.dummy import DummyRegressor, DummyClassifier
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

dummy = DummyRegressor(strategy="mean").fit(X_train, y_train)
root_mean_squared_error(y_test, dummy.predict(X_test))       # 71.4
ridge = make_pipeline(StandardScaler(), Ridge()).fit(X_train, y_train)
root_mean_squared_error(y_test, ridge.predict(X_test))       # 55.7  → 比 baseline 降 22%
```

| Baseline 的用途 | 說明 |
| --- | --- |
| 判斷問題難度 | 複雜模型只比 baseline 好一點 → 特徵可能不足 |
| 抓洩漏 | 複雜模型好得不合理 → 先懷疑 [資料洩漏](../foundations/data-leakage.md) |
| 設定最低門檻 | 之後每個模型都必須贏過它 |
| 解讀指標 | 「accuracy 0.95」在正類 5% 的資料上 = 什麼都沒學到 |

## 錯誤分析 (Error Analysis)

整體指標看起來可接受，但在重要切片上表現很差，模型就還沒準備好。

| 問題 | 切片 |
| --- | --- |
| 哪些類別或數值區間最難？ | 依類別、依真值 / 預測值分箱 |
| 錯誤集中在特定族群嗎？ | 性別、年齡層、地區、醫院、批次、定序平台 |
| 錯誤集中在特定時期嗎？ | 依月份 / 季度 |
| 有系統性的偽陽性或偽陰性嗎？ | 看混淆矩陣與錯誤案例本身 |
| 錯誤和缺失、離群值、特定特徵範圍有關嗎？ | 依特徵分箱、依缺失與否 |

```python
import pandas as pd
from sklearn.metrics import recall_score

res = X_test.assign(y=y_test, pred=model.predict(X_test), err=lambda d: d["y"] != d["pred"])

res.groupby("hospital")["err"].agg(["mean", "size"])                    # 各醫院錯誤率與樣本數
res.groupby(pd.qcut(res["age"], 4), observed=True)["err"].mean()        # 依年齡四分位
res.groupby("batch")[["y", "pred"]].apply(lambda d: recall_score(d["y"], d["pred"]))   # 各批次 recall
res[res["err"]].sample(20, random_state=0)                              # 直接看錯誤案例
```

> 切片時一定要同時看**樣本數**：小群體的錯誤率本來就波動大，見 [指標的不確定性](metric-uncertainty.md)。

更多診斷方法（殘差、漂移、校準）見 [模型診斷](../interpretability-and-diagnostics/model-diagnostics.md)。
