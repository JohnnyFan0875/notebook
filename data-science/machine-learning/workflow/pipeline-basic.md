[Machine Learning](../README.md) › [工作流程](README.md) › Pipeline

# Pipeline 基礎 (Pipeline Basics)

[scikit-learn](../packages/scikit-learn/README.md) 的 `Pipeline` 把前處理與模型串成一個物件：`fit` 時每一步只從訓練資料學習，`predict` 時用同樣的轉換套用到新資料。這是防止 [資料洩漏](../foundations/data-leakage.md) 最簡單可靠的方法。

| 好處 | 說明 |
| --- | --- |
| 防止洩漏 | 在 [交叉驗證](cross-validation.md) 中，每個 fold 都重新 fit 前處理 |
| 前處理與模型綁在一起 | 不會忘記某一步，或訓練與預測用了不同設定 |
| 調參更安全 | 前處理的參數也能一起調 |
| 上線可重現 | 存一個檔案就包含完整流程 |

## 建立與使用

```python
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score

# 1. 單一型態資料：make_pipeline 自動以小寫類別名稱命名步驟
pipe = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                     LogisticRegression(max_iter=1000))

# 2. 混合型態：ColumnTransformer 對不同欄位做不同處理
numeric_features = ["age", "income"]
categorical_features = ["city", "segment"]

preprocess = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric_features),
    ("cat", make_pipeline(SimpleImputer(strategy="most_frequent"),
                          OneHotEncoder(handle_unknown="ignore")), categorical_features),
])
pipeline = Pipeline([
    ("preprocess", preprocess),
    ("model", RandomForestClassifier(random_state=42)),
])

# 3. 當成一般模型使用
cross_val_score(pipeline, X_train, y_train, cv=5, scoring="roc_auc")
pipeline.fit(X_train, y_train)
pipeline.predict(X_test)

# 4. 調參：用「步驟名__參數名」，前處理的參數也能調
param_grid = {
    "model__n_estimators": [100, 300],
    "model__max_depth": [None, 5, 10],
    "preprocess__num__simpleimputer__strategy": ["mean", "median"],
}
search = GridSearchCV(pipeline, param_grid, cv=5, scoring="roc_auc").fit(X_train, y_train)

# 5. 檢查與存檔
search.best_estimator_[:-1].get_feature_names_out()   # 前處理後的欄位名：num__age, cat__city_A, ...
import joblib
joblib.dump(search.best_estimator_, "model.joblib")   # 存整個 pipeline，不只模型
```

依型態自動選欄位，可用 `make_column_selector(dtype_include="number")` 與 `make_column_selector(dtype_exclude="number")`。

> pandas 3 的字串欄位預設是 `str` dtype 而不是 `object`；`make_column_selector(dtype_include=object)` 會出現 deprecation 警告，用 `dtype_exclude="number"` 選類別欄位可同時相容 pandas 2 與 3。

## 規則

| 規則 | 原因 |
| --- | --- |
| 前處理放在 pipeline 裡，不要在切分前做 | 否則就是洩漏 |
| 不同欄位不同處理 → `ColumnTransformer` | 數值補中位數 + 縮放；類別補眾數 + one-hot |
| `OneHotEncoder(handle_unknown="ignore")` | 上線時遇到新類別不會報錯 |
| 調參用 `步驟名__參數名` | `make_pipeline` 的步驟名是小寫類別名（`logisticregression__C`） |
| 存整個 pipeline | 只存模型，上線時前處理就會不一致 |
| 記錄套件版本 | `joblib` 存的物件在不同 sklearn 版本間不保證相容 |

相關：[補值](../preprocessing/imputation.md)、[類別編碼](../preprocessing/categorical-encoding.md)、[特徵縮放](../preprocessing/feature-scaling.md)、[超參數調整](hyperparameter-tuning.md)、[MLflow](../production/mlflow.md)；R 的對應做法（recipes + workflows）見 [tidymodels](../packages/tidymodels/README.md)。
