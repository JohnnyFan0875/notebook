[Machine Learning](../../README.md) › [套件](../README.md) › scikit-learn

# scikit-learn 速查

scikit-learn 在這個筆記本中是「實作層」：概念放在各主題筆記，這裡只整理 API 慣例與「想做 X → 用哪個」。本筆記本的程式碼以 sklearn 1.9 驗證。

## 核心 API

所有物件都遵循同一套介面：

| 方法 | 誰有 | 作用 |
| --- | --- | --- |
| `fit(X, y)` | 所有估計器 | 從訓練資料學習參數 |
| `transform(X)` | 轉換器（scaler、encoder、PCA） | 套用學到的轉換 |
| `fit_transform(X)` | 轉換器 | 等於 fit + transform（**只能用在訓練資料**） |
| `predict(X)` | 預測器 | 類別或數值 |
| `predict_proba(X)` | 多數分類器 | 各類別機率 |
| `decision_function(X)` | SVM、線性模型 | 連續分數（可算 AUC） |
| `score(X, y)` | 預測器 | 分類：accuracy；迴歸：R² |
| `get_params()` / `set_params()` | 全部 | 讀寫超參數 |

| 慣例 | 說明 |
| --- | --- |
| `X` 是 2D、`y` 是 1D | 單一特徵要 `x.reshape(-1, 1)` 或 `df[["col"]]` |
| 結尾底線 `coef_`、`classes_` | fit 之後才存在的屬性 |
| `random_state` | 控制隨機性，讓結果可重現 |
| `n_jobs=-1` | 用所有 CPU 核心平行 |
| scorer 越大越好 | 誤差類指標要用 `neg_` 版本：`"neg_root_mean_squared_error"` |
| `set_output(transform="pandas")` | 讓轉換器輸出 DataFrame（保留欄位名） |

## 想做 X → 用哪個

| 任務 | 工具 | 筆記 |
| --- | --- | --- |
| 切 train / test | `train_test_split(stratify=y)` | [Train-Test Split](../../preprocessing/train-test-split.md) |
| 交叉驗證 | `cross_val_score`、`cross_validate`、`StratifiedKFold`、`GroupKFold`、`TimeSeriesSplit` | [交叉驗證](../../workflow/cross-validation.md) |
| 串起前處理與模型 | `Pipeline`、`make_pipeline`、`ColumnTransformer` | [Pipeline](../../workflow/pipeline-basic.md) |
| 調參 | `GridSearchCV`、`RandomizedSearchCV`、`HalvingRandomSearchCV` | [超參數調整](../../workflow/hyperparameter-tuning.md) |
| 補值 | `SimpleImputer`、`KNNImputer`、`IterativeImputer` | [補值](../../preprocessing/imputation.md) |
| 類別編碼 | `OneHotEncoder`、`OrdinalEncoder`、`TargetEncoder` | [類別編碼](../../preprocessing/categorical-encoding.md) |
| 縮放 | `StandardScaler`、`RobustScaler`、`MinMaxScaler` | [特徵縮放](../../preprocessing/feature-scaling.md) |
| 特徵選擇 | `SelectKBest`、`SelectFromModel`、`RFECV`、`SequentialFeatureSelector` | [特徵選擇](../../preprocessing/feature-selection.md) |
| Baseline | `DummyClassifier`、`DummyRegressor` | [Baseline](../../evaluation/baselines-and-error-analysis.md) |
| 調閾值 | `TunedThresholdClassifierCV`、`FixedThresholdClassifier` | [閾值與校準](../../evaluation/classification-thresholds-and-calibration.md) |
| 機率校準 | `CalibratedClassifierCV`、`CalibrationDisplay` | 同上 |
| 評估圖 | `RocCurveDisplay`、`PrecisionRecallDisplay`、`ConfusionMatrixDisplay`、`PredictionErrorDisplay` | [模型評估](../../evaluation/README.md) |
| 學習 / 驗證曲線 | `LearningCurveDisplay`、`ValidationCurveDisplay` | [過擬合與欠擬合](../../foundations/overfitting-underfitting.md) |
| 解釋模型 | `permutation_importance`、`PartialDependenceDisplay` | [可解釋性](../../interpretability-and-diagnostics/model-interpretability.md) |
| 分群 | `KMeans`、`AgglomerativeClustering`、`HDBSCAN`、`GaussianMixture` | [分群](../../unsupervised-learning/clustering/README.md) |
| 降維 | `PCA`、`TSNE`、`NMF` | [降維](../../unsupervised-learning/dimensionality-reduction/README.md) |
| 異常偵測 | `IsolationForest`、`LocalOutlierFactor` | [異常偵測](../../unsupervised-learning/anomaly-detection/README.md) |
| 存模型 | `joblib.dump(pipeline, "model.joblib")` | [Pipeline](../../workflow/pipeline-basic.md) |

## 近幾版的重要變動

讀舊教學時常遇到的 API 差異：

| 舊寫法 | 新寫法 | 版本 |
| --- | --- | --- |
| `mean_squared_error(..., squared=False)` | `root_mean_squared_error` | 1.4 deprecated，之後移除 |
| `base_estimator=`（Bagging、AdaBoost） | `estimator=` | 1.2 改名，1.4 移除舊名 |
| `AdaBoostClassifier(algorithm="SAMME.R")` | 刪掉 `algorithm` | SAMME.R 1.6 移除 |
| `OneHotEncoder(sparse=False)` | `sparse_output=False` | 1.2 改名 |
| `LogisticRegression(penalty="l1")` | `l1_ratio=1` | 1.8 deprecated |
| `LogisticRegression(multi_class=...)` | 刪掉（預設 multinomial） | 已移除 |
| `SVC(probability=True)` | `CalibratedClassifierCV(SVC(), ensemble=False)` | 1.9 deprecated |
| `TSNE(n_iter=...)` | `max_iter=` | 1.5 改名 |
| `KMeans` 的 `n_init=10` | 預設 `"auto"` | 1.4 |
| `TargetEncoder(shuffle=, random_state=)` | 傳入 `cv=KFold(...)` | 1.9 deprecated |

> 原則：**任何會從訓練資料學東西的步驟都放進 `Pipeline` / `ColumnTransformer`**，交叉驗證與上線時才不會洩漏或不一致。
