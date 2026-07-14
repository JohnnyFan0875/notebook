# Modeling with tidymodels

`tidymodels` 是一組把機器學習 workflow 拆成多個明確階段的套件集合。重點不是記住某一個模型函式，而是把資料切分、前處理、模型定義、預測與評估串成可重跑的分析流程。

## Core Packages

- `rsample`: 資料切分與 resampling。
- `parsnip`: 用統一語法定義模型。
- `recipes`: 前處理與特徵工程。
- `workflows`: 把模型與前處理綁成同一個 pipeline。
- `yardstick`: 評估指標。

## Basic Workflow

1. 先把資料切成 training / test。
2. 用 `parsnip` 宣告模型類型、engine 與 mode。
3. 用 `recipes` 定義前處理。
4. 用 `workflow()` 把模型與 recipe 合併。
5. fit 在 training data，再用 test data 做評估。

這種拆法的好處是模型規格、前處理規格與資料切分彼此分離，之後換演算法或新增步驟時不需要重寫整段分析。

## Splitting Data with rsample

最常見的起點是 `initial_split()`：

```r
library(tidymodels)

mpg_split <- initial_split(mpg, prop = 0.75, strata = hwy)
mpg_training <- training(mpg_split)
mpg_test <- testing(mpg_split)
```

- `prop = 0.75` 表示 75% 拿去 training。
- `training()` 與 `testing()` 會從 split 物件取出兩側資料。
- `strata =` 可在切分時維持某欄位的分布，比較適合類別不平衡或連續變數分布需要近似保留的情境。

切分必須先做，因為後面的前處理也應該只從 training data 學習參數，避免資料洩漏。

## Defining Models with parsnip

`parsnip` 把模型拆成三件事：

- 模型類型，例如 `linear_reg()`、`logistic_reg()`、`decision_tree()`。
- 計算引擎，例如 `"lm"`、`"glm"`、`"rpart"`。
- 問題模式，例如 `"regression"` 或 `"classification"`。

```r
log_model <- logistic_reg() %>%
  set_engine("glm") %>%
  set_mode("classification")

log_fit <- log_model %>%
  fit(purchased ~ total_visits + total_time, data = leads_training)
```

- `set_engine()` 決定底層用哪個套件計算。
- `set_mode()` 用來區分同一個模型族在 regression / classification 間的用途。
- `fit()` 才會真正把模型估計到資料上。

這種做法把「模型概念」和「實作 engine」分開，之後若要替換底層引擎，通常不需要改掉整體 workflow。

## Making Predictions

`predict()` 的回傳格式會依 `type =` 改變：

```r
class_pred <- predict(log_fit, new_data = leads_test, type = "class")
prob_pred <- predict(log_fit, new_data = leads_test, type = "prob")
```

- `type = "class"` 會產生 `.pred_class`。
- `type = "prob"` 會產生每個類別對應的機率欄位，例如 `.pred_yes`、`.pred_no`。

常見做法是把 prediction 與真實標籤合併後再評估：

```r
pred_results <- leads_test %>%
  bind_cols(class_pred, prob_pred)
```

`tidymodels` 的很多評估函式都假設資料已經整理成這種「truth 欄位 + `.pred_*` 欄位」的 tibble。

## Preprocessing with recipes

`recipes` 用來把前處理步驟顯式化，而不是零散地寫在資料清理腳本裡：

```r
leads_recipe <- recipe(purchased ~ ., data = leads_training) %>%
  step_log(total_time, base = 10)
```

- `recipe(outcome ~ ., data = ...)` 會建立欄位角色資訊。
- `summary(leads_recipe)` 可檢查每個變數的 `role`、`type` 與來源。
- 常見步驟包含缺值處理、轉換、標準化、dummy encoding 與欄位篩選。

例如：

```r
leads_recipe <- recipe(purchased ~ ., data = leads_training) %>%
  step_corr(all_numeric(), threshold = 0.9) %>%
  step_normalize(all_numeric()) %>%
  step_dummy(all_nominal(), -all_outcomes())
```

- `step_corr()` 移除高度相關的數值欄位。
- `step_normalize()` 做中心化與標準化。
- `step_dummy()` 把類別欄位轉成 dummy variables。

`prep()` 與 `bake()` 是 `recipes` 的核心：

```r
trained_recipe <- prep(leads_recipe, training = leads_training)
train_processed <- bake(trained_recipe, new_data = NULL)
test_processed <- bake(trained_recipe, new_data = leads_test)
```

- `prep()` 會在 training data 上估計前處理需要的參數。
- `bake(..., new_data = NULL)` 取出處理後的 training data。
- `bake(..., new_data = leads_test)` 把同一套規則套到 test data。

重點不是把資料變乾淨，而是確保 training、test 與未來新資料都用同一套轉換規則。

## Combining Steps with workflows

如果模型與前處理分開管理，很容易在預測時忘記先套 recipe。`workflow()` 就是用來避免這種錯誤：

```r
dt_model <- decision_tree() %>%
  set_engine("rpart") %>%
  set_mode("classification")

dt_workflow <- workflow() %>%
  add_model(dt_model) %>%
  add_recipe(leads_recipe)
```

- `add_model()` 加入 `parsnip` 模型。
- `add_recipe()` 加入前處理規則。
- 如果問題很簡單，也可以改用 `add_formula()`。

workflow 的價值在於把「先 recipe、再 fit、再 predict」的順序固定下來，降低手動串接時出錯的機會。

## Evaluation with yardstick

完成 workflow 後，可以直接用 split 做最後評估：

```r
dt_last_fit <- dt_workflow %>%
  last_fit(split = leads_split)

collect_metrics(dt_last_fit)
collect_predictions(dt_last_fit)
```

- `last_fit()` 會用 training side fit model，並在 test side 做最終評估。
- `collect_metrics()` 取回指標摘要。
- `collect_predictions()` 取回逐列 prediction 結果。

如果想一次算多個指標，可以先定義 metric set：

```r
cls_metrics <- metric_set(roc_auc, sens, spec)

pred_results %>%
  cls_metrics(truth = purchased, estimate = .pred_class, .pred_yes)
```

實務上要注意每個指標需要的欄位型別不同：

- 像 `accuracy()` 這類指標通常吃類別預測。
- 像 `roc_auc()` 則通常需要正類別機率欄位。

## Practical Notes

- 不要在 full data 上先做前處理再切 training / test，這會造成 leakage。
- `parsnip` 的重點是統一模型語法，不是取代統計理解；仍要知道模型假設與輸入需求。
- `recipes` 適合把前處理寫成可檢查、可重跑、可替換的步驟，而不是散落在多個 `mutate()` 裡。
- `workflow()` 適合當分析專案的主幹，因為它把模型與前處理綁成單一物件。
- 當 workflow 開始需要 cross-validation、tuning 或多模型比較時，tidymodels 的模組化設計會比手寫流程更容易維護。
