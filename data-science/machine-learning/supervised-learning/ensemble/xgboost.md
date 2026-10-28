[Machine Learning](../../README.md) › [監督式學習](../README.md) › [集成方法](README.md) › XGBoost

# XGBoost (Extreme Gradient Boosting)

[Gradient Boosting](gradient-boosting.md) 的高效能實作，在表格資料與競賽中最常見。相較 sklearn 的經典版：

| 特色 | 說明 |
| --- | --- |
| 正則化目標函數 | 損失之外加上葉節點數與葉權重的 L1 / L2 懲罰（`gamma`、`reg_alpha`、`reg_lambda`） |
| 二階近似 | 用梯度與 Hessian 決定分裂與葉值 |
| 缺失值 | 每個分裂學習缺失值該往哪邊走 |
| 效能 | 直方圖分裂（`tree_method="hist"`，預設）、多執行緒、GPU（`device="cuda"`） |
| sklearn 相容 | `XGBClassifier` / `XGBRegressor` 可放進 pipeline、`GridSearchCV` |

## 用法

```python
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

# 承乳癌範例（1 = 惡性）
# 1. 基本
model = XGBClassifier(n_estimators=300, max_depth=3, learning_rate=0.05,
                      subsample=0.8, colsample_bytree=0.8,
                      eval_metric="logloss", random_state=42)
# CV AUC 0.992

# 2. Early stopping：從訓練資料再切出驗證集（不要用測試集！）
X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.2,
                                            stratify=y_train, random_state=0)
model = XGBClassifier(n_estimators=2000, learning_rate=0.05, max_depth=3,
                      subsample=0.8, colsample_bytree=0.8, eval_metric="logloss",
                      early_stopping_rounds=50, random_state=42)
model.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], verbose=False)
model.best_iteration          # 326
roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])      # 0.996

# 3. 不平衡：scale_pos_weight ≈ 陰性數 / 陽性數
(y_train == 0).sum() / (y_train == 1).sum()                   # 1.69
```

> 新版 XGBoost：`early_stopping_rounds` 與 `eval_metric` 放在**建構子**；3.x 的 `fit()` 已不接受這兩個參數（舊教學的寫法會報 `TypeError`）。GPU 改用 `device="cuda"`（舊寫法 `tree_method="gpu_hist"`）。本筆記以 XGBoost 3.4 驗證。

## 參數

| 參數 | 作用 | 常用起點 |
| --- | --- | --- |
| `learning_rate` (`eta`) | 每棵樹的貢獻 | 0.05–0.1 |
| `n_estimators` | 樹數上限，搭配 early stopping | 1000+ |
| `max_depth` | 樹深 | 3–8 |
| `min_child_weight` | 葉節點的最小 Hessian 總和（≈ 最少樣本數） | 1–10 |
| `subsample` / `colsample_bytree` | 樣本 / 特徵抽樣比例 | 0.7–0.9 |
| `reg_lambda` / `reg_alpha` | 葉權重的 L2 / L1 正則化 | 1 / 0 |
| `gamma` | 分裂需要的最小損失下降 | 0 |
| `scale_pos_weight` | 不平衡時加重陽性 | 陰性 / 陽性比 |

調參順序與 [Gradient Boosting](gradient-boosting.md#調參順序) 相同。

## 提醒

| 提醒 | 說明 |
| --- | --- |
| 不是免調參魔法 | 降低 `learning_rate` 要搭配更多樹；只調 `max_depth` 而忽略 subsampling 與正則化常不夠 |
| Early stopping 的驗證集不能是測試集 | 否則測試分數偏樂觀 |
| 分數很高時先查洩漏與不平衡 | 見 [資料洩漏](../../foundations/data-leakage.md)、[類別不平衡](../../evaluation/class-imbalance.md) |
| 重要性不是因果 | 內建 `feature_importances_`（gain）有偏誤；用 SHAP 或 permutation importance，見 [可解釋性](../../interpretability-and-diagnostics/model-interpretability.md) |
| 先和 sklearn `HistGradientBoosting` 比 | 小到中型資料常差不多，後者不需額外安裝 |
| 小資料不一定贏 | 乳癌資料上 XGBoost（0.992）和邏輯斯迴歸（0.992）打平 |
