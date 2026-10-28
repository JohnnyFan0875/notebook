[Machine Learning](../../README.md) › [監督式學習](../README.md) › [集成方法](README.md) › Voting

# 投票集成 (Voting Ensemble)

把幾個**不同類型**的模型各自訓練，再合併預測：分類用投票或平均機率，迴歸用平均。最簡單的異質集成；模型之間的錯誤越不相關，合併後越有幫助。

| 方式 | 做法 | 何時用 |
| --- | --- | --- |
| Hard voting | 多數決 | 模型沒有可靠的機率輸出 |
| **Soft voting** | 平均各模型的預測機率（可加權） | 模型都有 `predict_proba`；通常優於 hard |
| `VotingRegressor` | 平均預測值 | 迴歸 |

## 用法

```python
from sklearn.ensemble import VotingClassifier, VotingRegressor, RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# 每個基本模型自帶需要的前處理（樹不用縮放，KNN / 邏輯斯要）
vote = VotingClassifier(
    estimators=[("lr",  make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))),
                ("rf",  RandomForestClassifier(n_estimators=300, random_state=0)),
                ("knn", make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=15)))],
    voting="soft",
    weights=None,              # 例如 [2, 1, 1] 讓邏輯斯迴歸權重較大
)
vote.fit(X_train, y_train)     # 承乳癌範例；CV AUC 0.992（各模型：0.992 / 0.986 / 0.986）

# 調基本模型的參數：用 名稱__參數
param_grid = {"rf__min_samples_leaf": [1, 3], "knn__kneighborsclassifier__n_neighbors": [7, 15, 31]}

# 迴歸
VotingRegressor([("ridge", make_pipeline(StandardScaler(), Ridge())),
                 ("rf", RandomForestRegressor(random_state=0))])
```

> SVM 要放進 soft voting 需要機率：用 `CalibratedClassifierCV(SVC(), ensemble=False)`（sklearn 1.9 起 `SVC(probability=True)` 已 deprecated），見 [SVM](../classification/svm.md)。

## 什麼時候有幫助

| 有幫助 | 沒幫助 |
| --- | --- |
| 各模型表現相近、**錯誤型態不同**（線性 + 樹 + 距離型） | 一個模型明顯強很多：平均會被弱模型拖累 |
| 想要比單一模型更穩定的預測 | 模型高度相似（三個不同設定的隨機森林） |

乳癌資料上 soft voting（0.992）與最好的單一模型持平：基本模型都已接近上限時，投票只換來更穩定，不會更準。

## 與 Stacking 的差別

| | Voting | [Stacking](stacking.md) |
| --- | --- | --- |
| 合併方式 | 固定規則（平均 / 多數決），權重手動給 | 第二層模型**學習**怎麼合併 |
| 洩漏風險 | 低 | 需要 out-of-fold 預測，做錯就洩漏 |
| 複雜度 | 低 | 較高 |
| 建議 | 先試 | Voting 有效後再試 |
