[Machine Learning](../../README.md) › [監督式學習](../README.md) › [集成方法](README.md) › AdaBoost

# AdaBoost (Adaptive Boosting)

最早的實用 boosting 演算法：依序訓練多個弱學習器（通常是只切一刀的決策樹 stump），每一輪**提高上一輪分錯樣本的權重**，讓下一個學習器專注在難的樣本；最後依各學習器的準確度加權投票。

```
所有樣本權重相同 → 訓練 stump 1 → 分錯的樣本權重 ↑
                → 訓練 stump 2 → 分錯的樣本權重 ↑
                → …
最終預測 = Σ（學習器權重 × 學習器預測）    準的學習器權重大
```

| | AdaBoost | [Gradient Boosting](gradient-boosting.md) |
| --- | --- | --- |
| 如何專注在錯誤 | 調整**樣本權重** | 擬合前一輪的**殘差 / 梯度** |
| 損失函數 | 指數損失（分類） | 任意可微損失 |
| 現況 | 概念重要，實務上多被 Gradient Boosting 取代 | 表格資料主流 |

## 用法

```python
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV, StratifiedKFold

# 承乳癌範例
ada = AdaBoostClassifier(estimator=DecisionTreeClassifier(max_depth=1),   # stump；舊名 base_estimator 已移除
                         n_estimators=300, learning_rate=0.5, random_state=0)
# CV AUC 0.992

search = GridSearchCV(ada, {"n_estimators": [100, 300, 500], "learning_rate": [0.1, 0.5, 1.0]},
                      cv=StratifiedKFold(5, shuffle=True, random_state=0), scoring="roc_auc")

# 迴歸（AdaBoost.R2）：loss 決定樣本權重如何依誤差更新
AdaBoostRegressor(estimator=DecisionTreeRegressor(max_depth=3), n_estimators=100,
                  learning_rate=0.1, loss="linear")      # "linear"、"square"、"exponential"
```

> 新版 sklearn 的 `AdaBoostClassifier` 只剩 SAMME 演算法：`"SAMME.R"` 在 1.4 deprecated、1.6 移除；`algorithm` 參數本身在 1.6 deprecated、1.8 移除。舊程式碼的 `algorithm="SAMME.R"` 在新版會報錯，直接刪掉這個參數即可。

| 參數 | 說明 |
| --- | --- |
| `estimator` | 弱學習器；分類常用 `max_depth=1`，迴歸常用 2–4 |
| `n_estimators` | 輪數；太多可能過擬合（尤其有雜訊時） |
| `learning_rate` | 縮小每個學習器的貢獻；和 `n_estimators` 互相取捨，一起調 |

## 特性

| 優點 | 缺點 |
| --- | --- |
| 簡單、參數少 | **對標籤雜訊與離群值敏感**：錯標的樣本權重會被不斷放大 |
| 弱學習器就能組出強模型 | 依序訓練，無法平行 |
| 理論與直覺清楚，是理解 boosting 的起點 | 通常不如 Gradient Boosting / XGBoost |
