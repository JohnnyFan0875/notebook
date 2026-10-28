[Machine Learning](README.md) › ML 方法速查

# ML 方法速查 (Model Selection Guide)

依「任務」與「資料特性」快速找到模型、指標與驗證方式，點連結看細節。

## 1. 依任務選模型

| 任務 | 先做的 baseline | 常用模型 | 筆記 |
| --- | --- | --- | --- |
| 迴歸（連續 y） | 平均值 / 中位數、線性迴歸 | Ridge / Lasso、隨機森林、Gradient Boosting | [線性](supervised-learning/regression/linear.md)、[Ridge](supervised-learning/regression/ridge.md)、[Lasso](supervised-learning/regression/lasso.md)、[Elastic Net](supervised-learning/regression/elastic-net.md) |
| 分類（類別 y） | 多數類別、邏輯斯迴歸 | 隨機森林、Gradient Boosting、SVM | [邏輯斯迴歸](supervised-learning/classification/logistic-regression.md)、[SVM](supervised-learning/classification/svm.md)、[KNN](supervised-learning/classification/knn.md)、[決策樹](supervised-learning/classification/decision-tree.md)、[Naive Bayes](supervised-learning/classification/naive-bayes.md) |
| 表格資料要最高分 | 單一調好的樹模型 | XGBoost / LightGBM、stacking | [Gradient Boosting](supervised-learning/ensemble/gradient-boosting.md)、[XGBoost](supervised-learning/ensemble/xgboost.md)、[Stacking](supervised-learning/ensemble/stacking.md) |
| 要可解釋的係數 | — | 線性 / 邏輯斯迴歸、淺層決策樹 | [statsmodels](packages/statsmodels/README.md)、[可解釋性](interpretability-and-diagnostics/model-interpretability.md) |
| 找群組（無標籤） | K-Means | 階層式、DBSCAN、GMM | [分群](unsupervised-learning/clustering/README.md) |
| 降維、視覺化 | PCA | t-SNE、UMAP、NMF | [降維](unsupervised-learning/dimensionality-reduction/README.md) |
| 找異常 | z-score / IQR 規則 | Isolation Forest、LOF | [異常偵測](unsupervised-learning/anomaly-detection/README.md) |
| 購物籃 / 共現規則 | — | Apriori、FP-Growth | [關聯規則](unsupervised-learning/association-rules/README.md) |
| 推薦 | 熱門度排序 | 協同過濾、ALS | [推薦系統](recommender-systems/README.md) |

## 2. 依資料特性調整

| 資料特性 | 風險 | 對策 | 筆記 |
| --- | --- | --- | --- |
| 特徵遠多於樣本 (p ≫ n)，如基因表現 | 過擬合、特徵選擇洩漏 | 正則化、特徵選擇放在 CV 內、nested CV | [高維小樣本](foundations/high-dimensional-data.md) |
| 同一病人 / 使用者有多筆資料 | 同一實體跨 train/test → 分數虛高 | `GroupKFold` | [交叉驗證](workflow/cross-validation.md) |
| 有時間順序 | 用未來預測過去 | `TimeSeriesSplit`、依時間切 | [交叉驗證](workflow/cross-validation.md)、[Basetable](foundations/basetable-and-time-aware-feature-engineering.md) |
| 類別不平衡 | accuracy 失真 | PR-AUC、class weight、調閾值 | [類別不平衡](evaluation/class-imbalance.md) |
| 缺失值 | 偏誤、洩漏 | pipeline 內補值 + 缺失指標 | [補值](preprocessing/imputation.md) |
| 高基數類別 | one-hot 爆量、target encoding 洩漏 | 頻率 / target encoding（fold 內） | [類別編碼](preprocessing/categorical-encoding.md) |
| 量尺差異大 | 距離 / 正則化模型失準 | 標準化（樹模型不需要） | [特徵縮放](preprocessing/feature-scaling.md) |
| 離群值 | MSE 型模型被拉偏 | 穩健損失、轉換、確認是否為錯誤 | [離群值](preprocessing/outlier-handling.md) |
| 批次效應 (batch effect) | 模型學到批次而非生物訊號 | 依批次分組驗證、設計時平衡批次 | [干擾與批次效應](../statistics/experimental-design/confounding-bias.md#生資最常見的干擾批次效應-batch-effect) |

## 3. 選評估指標

| 情境 | 指標 | 筆記 |
| --- | --- | --- |
| 迴歸，誤差單位要好解釋 | RMSE、MAE | [MSE / RMSE](evaluation/mse-rmse.md) |
| 分類，類別平衡 | Accuracy、ROC-AUC | [ROC-AUC](evaluation/roc-auc.md) |
| 分類，正類稀少 | PR-AUC、F1、Recall@固定 Precision | [混淆矩陣指標](evaluation/confusion-metrics.md)、[類別不平衡](evaluation/class-imbalance.md) |
| 需要可信的機率 | Log loss、Brier score、校準曲線 | [閾值與校準](evaluation/classification-thresholds-and-calibration.md) |
| 只能處理前 k% 名單（行銷、篩檢） | Gains / Lift | [Gains 與 Lift](evaluation/gains-and-lift-curves.md) |
| 分群（無標籤） | Silhouette、與已知標籤比對（ARI） | [K-Means](unsupervised-learning/clustering/kmeans.md) |

## 4. 選驗證方式

| 情境 | 驗證方式 |
| --- | --- |
| 資料量大、獨立樣本 | train / validation / test 三分 |
| 一般表格資料 | `KFold` / `StratifiedKFold`（分類） |
| 有分組（病人、批次、使用者） | `GroupKFold` / `StratifiedGroupKFold` |
| 時間序列 | `TimeSeriesSplit` |
| 小樣本且要調參又要報告效能 | Nested CV |

細節見 [交叉驗證](workflow/cross-validation.md)、[資料切分與洩漏](workflow/data-splitting-and-leakage.md)。

## 選擇前的三個問題

1. **預測單位與預測時間點是什麼？** 決定哪些特徵合法、資料該怎麼切（見 [問題定義](workflow/problem-framing.md)）
2. **哪種錯誤代價高？** 決定指標與閾值（見 [評估思維](foundations/evaluation-mindset.md)）
3. **要預測還是要解釋？** 要解釋就優先簡單模型與 [statsmodels](packages/statsmodels/README.md)；要預測就以驗證分數為準
