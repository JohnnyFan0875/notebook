[Machine Learning](../../README.md) › [監督式學習](../README.md) › [集成方法](README.md) › Gradient Boosting

# 梯度提升 (Gradient Boosting)

依序加入淺樹，每棵新樹擬合**目前模型損失函數的負梯度**（平方損失時就是殘差），再乘上學習率加進模型。等於在「函數空間」做梯度下降。是表格資料上最常勝出的模型家族（XGBoost、LightGBM、CatBoost 都屬於這一類）。

$$
F_m(x) = F_{m-1}(x) + \eta \cdot h_m(x), \qquad h_m \approx -\frac{\partial L(y, F_{m-1}(x))}{\partial F_{m-1}(x)}
$$

## 關鍵參數

| 參數 | 作用 | 常用範圍 |
| --- | --- | --- |
| `learning_rate` (η) | 每棵樹的貢獻縮放；越小越穩但需要越多樹 | 0.01–0.1 |
| `n_estimators` / `max_iter` | 樹的數量；**會過擬合**，用 early stopping 決定 | 數百到數千 |
| `max_depth` / `max_leaf_nodes` | 每棵樹的複雜度（交互作用的階數） | 深度 3–8 |
| `subsample` | 每棵樹用的樣本比例（< 1 = stochastic GB） | 0.5–0.9 |
| `min_samples_leaf` | 葉節點最少樣本 | 依資料量 |

![Ensemble n_estimators](src/ensemble-n-estimators.png)

右圖：學習率 1.0 很快收斂；0.1 需要約 800 輪；0.02 在 800 輪時還沒收斂。學習率與樹數必須一起調，實務做法是**固定較小的學習率，用 early stopping 決定樹數**。

## 兩種 sklearn 實作

| | `GradientBoostingClassifier/Regressor` | `HistGradientBoostingClassifier/Regressor` |
| --- | --- | --- |
| 速度 | 慢（精確分裂） | **快很多**（特徵先分箱成 ≤ 255 個 bin），適合數萬筆以上 |
| 缺失值 | 需補值 | **原生支援 NaN** |
| 類別特徵 | 需編碼 | `categorical_features="from_dtype"` 原生支援 |
| Early stopping | `n_iter_no_change` + `validation_fraction` | `early_stopping="auto"`（n > 10,000 時自動開啟） |
| 對應 | 經典版本 | 類似 LightGBM |

```python
from sklearn.ensemble import GradientBoostingClassifier, HistGradientBoostingClassifier

# 承乳癌範例
# 1. 經典版 + early stopping：設很大的 n_estimators，讓驗證分數決定何時停
gb = GradientBoostingClassifier(n_estimators=1000, learning_rate=0.05, max_depth=3, subsample=0.8,
                                validation_fraction=0.2, n_iter_no_change=20, random_state=0)
gb.fit(X_train, y_train)
gb.n_estimators_          # 113：實際只用了 113 棵就停止

# 2. HistGradientBoosting：預設值就很強，大資料首選
hgb = HistGradientBoostingClassifier(learning_rate=0.05, max_iter=1000, early_stopping=True,
                                     random_state=0)
hgb.fit(X_train, y_train)
hgb.n_iter_               # 80

# 其他損失：迴歸可用 loss="absolute_error"、"quantile"（預測區間）、"poisson"（計數）
```

乳癌資料（398 筆）CV AUC：Gradient Boosting 0.985、HistGB 0.983，都略低於邏輯斯迴歸 0.992。樣本小、關係近線性時，boosting 沒有優勢。

## 調參順序

```
1. 固定 learning_rate = 0.05–0.1，開 early stopping
2. 調樹的複雜度：max_depth / max_leaf_nodes、min_samples_leaf
3. 調隨機性：subsample、max_features（或 XGBoost 的 colsample_bytree）
4. 調正則化：l2_regularization（HistGB）、reg_lambda / reg_alpha（XGBoost）
5. 最後把 learning_rate 降低、樹數加多做最後提升
```

調參方法見 [超參數調整](../../workflow/hyperparameter-tuning.md)。

## 特性

| 優點 | 缺點 |
| --- | --- |
| 表格資料上準確度通常最高 | 參數多、需要調 |
| 支援各種損失（分位數、Poisson…） | 依序訓練（樹內可平行，樹間不行） |
| HistGB / XGBoost / LightGBM 原生處理缺失 | 樹數過多會過擬合（不像隨機森林） |
| — | 對標籤雜訊比隨機森林敏感 |

| 函式庫 | 特色 |
| --- | --- |
| sklearn `HistGradientBoosting*` | 不用額外安裝、與 pipeline 整合最好 |
| [XGBoost](xgboost.md) | 最成熟、GPU、競賽常用 |
| LightGBM | leaf-wise 生長，大資料最快 |
| CatBoost | 類別特徵處理最好（ordered target encoding） |

> Boosting 和 [隨機森林](random-forest.md) 的差別：隨機森林平均許多「各自很強、但變異高」的深樹；boosting 依序累加許多「各自很弱」的淺樹。
