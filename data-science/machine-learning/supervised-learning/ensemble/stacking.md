[Machine Learning](../../README.md) › [監督式學習](../README.md) › [集成方法](README.md) › Stacking

# 堆疊集成 (Stacking)

用多個不同的基本模型產生預測，再訓練一個**第二層模型 (meta-model)** 學習怎麼組合它們。第二層的訓練資料必須是基本模型的 **out-of-fold (OOF) 預測**，否則就是洩漏。

```
                    ┌─ 模型 A ─┐
訓練資料 ─ K-fold ─┼─ 模型 B ─┼─► OOF 預測（每筆都由沒看過它的模型預測）─► meta-model
                    └─ 模型 C ─┘
預測時：A、B、C（用全部訓練資料重新 fit）的預測 → meta-model → 最終預測
```

## 為什麼要 OOF

若基本模型在訓練資料上預測自己看過的樣本，預測會過度樂觀（例如隨機森林的訓練 accuracy ≈ 1），meta-model 就會學到「永遠相信那個最會背答案的模型」。OOF 預測讓第二層看到的是基本模型在**沒看過的資料**上的表現。sklearn 的 `StackingClassifier` 透過 `cv` 參數自動做這件事。

## 用法

```python
from sklearn.ensemble import StackingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

stack = StackingClassifier(
    estimators=[("rf",  RandomForestClassifier(n_estimators=300, random_state=0)),
                ("svm", make_pipeline(StandardScaler(), SVC())),           # 自動用 decision_function
                ("knn", make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=15)))],
    final_estimator=LogisticRegression(max_iter=1000),   # 第二層用簡單模型，避免過擬合
    cv=5,                    # 產生 OOF 預測的 fold 數
    stack_method="auto",     # 依序嘗試 predict_proba → decision_function → predict
    passthrough=False,       # True：第二層也看原始特徵
)
stack.fit(X_train, y_train)  # 承乳癌範例；CV AUC 0.993（RF 0.986、SVM 0.993、KNN 0.986）
```

乳癌資料上 stacking 和最好的單一模型（SVM 0.993）持平，卻多了 3 個模型的訓練與部署成本。

## Blending vs Stacking

| | Blending | Stacking |
| --- | --- | --- |
| 做法 | 直接對各模型的預測取（加權）平均；或在一塊保留的驗證集上學權重 | 用 OOF 預測訓練第二層模型 |
| 實作 | 簡單 | 較複雜 |
| 洩漏風險 | 低 | OOF 流程錯就洩漏 |
| 建議 | 單模型與驗證流程還不穩時先用 | 單模型都穩定、仍想再擠分數時 |

Kaggle 情境的用法見 [Kaggle 競賽流程](../../workflow/kaggle-competition-workflow.md#6-ensemble)。

## 注意事項

| 注意 | 原因 |
| --- | --- |
| 基本模型要**多樣** | 相似的模型提供不了新資訊 |
| 第二層用簡單模型 | 輸入只有幾欄，複雜模型容易過擬合 |
| 評估 stacking 本身要再包一層 CV | `cross_val_score(stack, ...)`；stacking 內部的 `cv` 只用來產生 OOF |
| 和強的單一模型比較 | 增加的複雜度常不值得 |
| 手動實作時 | 用 `cross_val_predict(model, X, y, cv=5, method="predict_proba")` 產生 OOF |
