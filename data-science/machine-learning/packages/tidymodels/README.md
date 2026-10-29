[Machine Learning](../../README.md) › [套件](../README.md) › tidymodels

# tidymodels

R 的預測建模套件集合，定位等同 Python 的 [scikit-learn](../scikit-learn/README.md)：把資料切分、前處理、模型定義、調參與評估拆成可替換的元件，再串成一個 workflow。概念（交叉驗證、資料洩漏、指標選擇）見 ML 各主題筆記，這裡只整理 R 的寫法。以預測為目標時用這裡；要解讀係數與 p 值見 [R 解釋型建模](../../../r-foundations/explanatory-modeling-in-r.md)。

> 本筆記的程式碼以 tidymodels 1.5（tune 2.1）實跑驗證；數字來自 `modeldata::cells`、`set.seed(42)`。

## 核心套件

| 套件 | 負責 | 主要函式 | scikit-learn 對應 |
| --- | --- | --- | --- |
| `rsample` | 切分、重抽樣 | `initial_split()`、`vfold_cv()`、`group_vfold_cv()`、`bootstraps()` | `train_test_split`、`KFold`、`GroupKFold` |
| `recipes` | 前處理、特徵工程 | `recipe()`、`step_*()`、`prep()`、`bake()` | `ColumnTransformer` + transformers |
| `parsnip` | 統一的模型語法 | `logistic_reg()`、`rand_forest()`、`set_engine()`、`set_mode()` | 各 estimator 類別 |
| `workflows` | 綁定前處理與模型 | `workflow()`、`add_recipe()`、`add_model()` | `Pipeline` |
| `tune` | 調參、重抽樣評估 | `tune()`、`tune_grid()`、`fit_resamples()`、`select_best()`、`last_fit()` | `GridSearchCV`、`cross_validate` |
| `yardstick` | 評估指標 | `metric_set()`、`roc_auc()`、`accuracy()`、`rmse()` | `sklearn.metrics` |

## 完整流程

```
initial_split ──► training ──► vfold_cv ──► tune_grid（每折內 prep recipe + fit）
      │                                         │
      │                                   select_best
      │                                         │
      └──────── testing ◄── last_fit（training 全部重 fit，test 評估一次）
```

```r
library(tidymodels)
data(cells, package = "modeldata")         # 細胞影像特徵；class = PS / WS
cells <- cells |> select(-case)

# 1. 切分：先切 test，之後所有估計都只用 training
set.seed(42)
split <- initial_split(cells, prop = 0.8, strata = class)
train <- training(split)
folds <- vfold_cv(train, v = 5, strata = class)

# 2. 前處理：只是「規格」，實際參數在每折的 analysis set 上估計
rec <- recipe(class ~ ., data = train) |>
  step_zv(all_predictors()) |>                       # 移除零變異欄位
  step_corr(all_numeric_predictors(), threshold = 0.9) |>
  step_normalize(all_numeric_predictors())

# 3. 模型：tune() 標記要調的參數
lasso_spec <- logistic_reg(penalty = tune(), mixture = 1) |>  # mixture = 1：Lasso
  set_engine("glmnet") |>
  set_mode("classification")

wf <- workflow() |> add_recipe(rec) |> add_model(lasso_spec)

# 4. 調參：每組參數 × 每折都重新 prep recipe 再 fit
res <- tune_grid(
  wf, resamples = folds,
  grid = grid_regular(penalty(), levels = 20),
  metrics = metric_set(roc_auc, mn_log_loss)
)
collect_metrics(res)                     # 每組參數的平均與標準誤
show_best(res, metric = "roc_auc", n = 3)
best <- select_best(res, metric = "roc_auc")   # penalty ≈ 0.0023、CV AUC 0.870
# 較保守：1-SE 規則內挑最簡單（penalty 最大）的模型
# select_by_one_std_err(res, desc(penalty), metric = "roc_auc")

# 5. 最終模型：用整個 training 重 fit，test 只評估這一次
final <- finalize_workflow(wf, best) |> last_fit(split)
collect_metrics(final)                   # test 上的指標：roc_auc 0.908、accuracy 0.819（另附 brier_class）
collect_predictions(final)               # .pred_class、.pred_PS、.pred_WS
fitted_wf <- extract_workflow(final)     # 之後 predict(fitted_wf, new_data) 用
```

不調參、只想估計一個固定模型的 CV 表現時，把第 4 步換成 `fit_resamples(wf, resamples = folds)`。

## recipes 與資料洩漏

`step_normalize()` 的平均與標準差、`step_impute_*()` 的補值、`step_corr()` 要刪哪些欄位，都是**從資料估計出來的參數**。放在 workflow 裡交給 `tune_grid()` / `fit_resamples()` 時，每一折只用該折的 analysis set 估計，assessment set 不會洩漏進去；這和 sklearn 把 scaler 放進 `Pipeline` 是同一件事（見 [資料洩漏](../../foundations/data-leakage.md)）。

| 寫法 | 洩漏？ | 說明 |
| --- | --- | --- |
| recipe 放進 workflow → `tune_grid()` / `fit_resamples()` / `last_fit()` | 否 | 每折各自 `prep()` |
| 先對全部資料 `mutate(x = scale(x))`，再切分 | 是 | test 的分布資訊進了訓練 |
| `prep(rec, training = cells)`（整份資料）後 `bake()` 再做 CV | 是 | 前處理參數看過所有折 |
| 手動 `prep(rec, training = train)` → `bake(new_data = test)` | 對 test 不洩漏 | 但對 CV 內部仍洩漏；只用於檢查 recipe 產出 |

```r
# 檢查 recipe 的輸出長什麼樣子（除錯用，不用於建模）
prepped <- prep(rec, training = train)
bake(prepped, new_data = NULL)           # 處理後的 training
tidy(prepped, number = 2)                # 第 2 步（step_corr）刪了哪些欄位
```

### 常用 `step_*`

| 需求 | step | 選擇器 |
| --- | --- | --- |
| 補值 | `step_impute_median()`、`step_impute_knn()` | `all_numeric_predictors()` |
| 標準化 | `step_normalize()` | `all_numeric_predictors()` |
| log 轉換 | `step_log(base = 10, offset = 1)` | 指定欄位 |
| 類別 → dummy | `step_dummy()` | `all_nominal_predictors()` |
| 罕見類別合併 | `step_other(threshold = 0.05)` | `all_nominal_predictors()` |
| 移除零 / 近零變異 | `step_zv()`、`step_nzv()` | `all_predictors()` |
| 移除高相關 | `step_corr(threshold = 0.9)` | `all_numeric_predictors()` |
| PCA | `step_pca(num_comp = 10)` | `all_numeric_predictors()` |
| 類別不平衡 | `themis::step_downsample()`、`step_smote()` | 只在訓練折內作用（`skip = TRUE`） |

> 舊寫法 `step_dummy(all_nominal(), -all_outcomes())` 可改成 `all_nominal_predictors()`；舊版 `step_knnimpute()` 等已改名為 `step_impute_*()`。

## parsnip：模型 = 類型 + engine + mode

| 模型 | 函式 | 常用 engine | 可調參數 |
| --- | --- | --- | --- |
| 線性 / 邏輯斯迴歸 | `linear_reg()`、`logistic_reg()` | `"lm"` / `"glm"`、`"glmnet"` | `penalty`、`mixture`（0 = Ridge、1 = Lasso） |
| 決策樹 | `decision_tree()` | `"rpart"` | `cost_complexity`、`tree_depth`、`min_n` |
| 隨機森林 | `rand_forest()` | `"ranger"` | `mtry`、`trees`、`min_n` |
| Boosting | `boost_tree()` | `"xgboost"`、`"lightgbm"`（需 bonsai） | `trees`、`learn_rate`、`tree_depth` |
| SVM | `svm_rbf()` | `"kernlab"` | `cost`、`rbf_sigma` |
| KNN | `nearest_neighbor()` | `"kknn"` | `neighbors` |

同一個模型類型換 engine 不必改 workflow 其他部分；`translate(lasso_spec)` 可看實際呼叫的底層函式。

## 預測與評估

```r
predict(fitted_wf, new_data = test_df)                 # .pred_class
predict(fitted_wf, new_data = test_df, type = "prob")  # .pred_PS、.pred_WS

# yardstick 吃「truth 欄 + .pred_* 欄」的 tibble
preds <- collect_predictions(final)
cls_metrics <- metric_set(roc_auc, accuracy, sens, spec)
preds |> cls_metrics(truth = class, estimate = .pred_class, .pred_PS)
```

| 陷阱 | 說明 |
| --- | --- |
| 物件取名 `spec`、`sens`、`rmse` | 會蓋掉同名的 yardstick 指標函式，`metric_set(..., spec)` 直接報錯「must be functions」；模型規格取名 `lasso_spec`、`rf_spec` |
| 正類別是**第一個 factor level** | yardstick 預設 `event_level = "first"`；結果是 `no` / `yes` 時，要 `relevel` 或設 `event_level = "second"`，否則 sensitivity、AUC 都算成反類別 |
| 機率指標要給機率欄 | `roc_auc()`、`mn_log_loss()` 傳 `.pred_<正類別>`；`accuracy()`、`sens()` 傳 `.pred_class` |
| `metric_set` 混用類別與機率指標 | `estimate =` 給類別、機率欄放在後面的位置參數 |

指標怎麼選見 [模型評估](../../evaluation/README.md)、[類別不平衡](../../evaluation/class-imbalance.md)。

## 重抽樣策略

| 資料結構 | rsample | 對應筆記 |
| --- | --- | --- |
| 一般 i.i.d. | `vfold_cv(v = 5 or 10, strata = y)` | [交叉驗證](../../workflow/cross-validation.md) |
| 重複 CV（小樣本降低變異） | `vfold_cv(v = 10, repeats = 5)` | 同上 |
| 同病人多筆樣本 | `group_vfold_cv(group = patient_id)` | 同上 |
| 時間序列 | `sliding_period()`、`rolling_origin()` | 同上 |
| Nested CV | `nested_cv(outside = vfold_cv(5), inside = vfold_cv(5))` | 同上 |
| Bootstrap / OOB | `bootstraps(times = 100)` | [抽樣與估計](../../../statistics/inferential-statistics/sampling-estimation.md) |

> 高維小樣本（如 n = 80、p = 20 000 的表現量資料）：特徵篩選（`step_corr`、依變異挑基因）必須放在 recipe 裡讓每折各自做，在 CV 外先挑好特徵是生資最常見的洩漏來源（見 [高維資料](../../foundations/high-dimensional-data.md)）。

## scikit-learn ↔ tidymodels 對照

| 任務 | scikit-learn | tidymodels |
| --- | --- | --- |
| 切 train / test | `train_test_split(X, y, stratify=y)` | `initial_split(df, strata = y)` |
| K-fold | `StratifiedKFold(5)` | `vfold_cv(train, v = 5, strata = y)` |
| 前處理 | `ColumnTransformer([...])` | `recipe(y ~ .) \|> step_*()` |
| 學參數 / 套用 | `fit` / `transform` | `prep()` / `bake()` |
| 模型 | `LogisticRegression(penalty="l1", C=...)` | `logistic_reg(penalty = ..., mixture = 1) \|> set_engine("glmnet")` |
| Pipeline | `Pipeline([("prep", ct), ("clf", model)])` | `workflow() \|> add_recipe() \|> add_model()` |
| 標記要調的參數 | `param_grid={"clf__C": [...]}` | `penalty = tune()` |
| Grid search | `GridSearchCV(pipe, grid, cv=folds)` | `tune_grid(wf, resamples = folds, grid = ...)` |
| CV 分數 | `cross_validate(pipe, X, y, cv=folds)` | `fit_resamples(wf, folds)` + `collect_metrics()` |
| 最佳參數 | `search.best_params_` | `select_best(res, metric = "roc_auc")` |
| 最終 fit + test | `best_estimator_.fit` 後在 test 上評分 | `finalize_workflow()` \|> `last_fit(split)` |
| 指標 | `roc_auc_score(y, p)` | `roc_auc(df, truth, .pred_yes)` |

> 正則化參數方向相反：sklearn 的 `C` 越大懲罰越弱；glmnet 的 `penalty`（λ）越大懲罰越強。
