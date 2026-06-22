# XGBoost

`Extreme Gradient Boosting with XGBoost` 是 `notebook_temp/output` 裡目前 machine learning 區塊最明顯的缺口之一。XGBoost 是梯度提升樹家族中非常常見的實務工具，特別擅長結構化表格資料。

## 為什麼它常有效

- 以 boosting 方式逐步修正前一輪模型的殘差
- 內建 regularization，比基本 gradient boosting 更強調泛化
- 對缺失值、非線性與特徵交互作用通常有不錯表現
- 訓練效率與工程成熟度高

## 什麼時候值得優先嘗試

- tabular data 為主
- 特徵之間有非線性與交互作用
- 線性模型表現不足，但又不想立刻進入深度學習

## 常用參數

- `n_estimators`: 樹的數量
- `max_depth`: 每棵樹的深度
- `learning_rate`: 每一步更新幅度
- `subsample`: 每棵樹使用的樣本比例
- `colsample_bytree`: 每棵樹使用的特徵比例
- `reg_alpha`, `reg_lambda`: L1 / L2 regularization

## Minimal Example

```python
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.datasets import load_breast_cancer

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = XGBClassifier(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss",
    random_state=42,
)

model.fit(X_train, y_train)
pred_prob = model.predict_proba(X_test)[:, 1]
print(roc_auc_score(y_test, pred_prob))
```

## 實務提醒

- XGBoost 很強，但不是免調參魔法。
- `learning_rate` 降低時，通常要搭配更多 `n_estimators`。
- 分數高時，也要回頭檢查資料洩漏與類別不平衡問題。

## 常見錯誤

- 只調 `max_depth`，卻忽略 subsampling 與 regularization。
- 把 feature importance 當成因果解釋。
- 只看 leaderboard 分數，沒有做 error analysis。

## Related Concepts

- [Gradient Boosting](gradient-boosting.md)
- [Random Forest](random-forest.md)
- [Hyperparameter Tuning](../../workflow/hyperparameter-tuning.md)
- [Model Interpretability](../../interpretability-and-diagnostics/model-interpretability.md)
