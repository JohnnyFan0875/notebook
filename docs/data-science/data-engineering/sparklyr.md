# Spark with `sparklyr`

`sparklyr` 是 R 連接 Apache Spark 的主要介面之一。它的價值不是把 Spark 變成另一套完全不同的系統，而是讓 R 使用者能沿用熟悉的 `dplyr`、formula 與 pipe workflow，把資料留在 Spark 叢集內處理。

Key point: `sparklyr` 的核心優勢不是「R 也能跑 Spark」這句話本身，而是它把 Spark DataFrame、SQL、feature engineering 與 MLlib 接到 R 的資料分析語言裡。

## The Core Lifecycle

最基本的節奏很簡單：

1. connect
2. work in Spark
3. disconnect

```r
library(sparklyr)

sc <- spark_connect(master = "local")

# do work

spark_disconnect(sc)
```

這個生命週期很值得刻意記住，因為 Spark connection 不是一般本地 data frame。它代表你正在對一個分散式運算環境發送操作。

## Why `sparklyr` Feels Familiar

`sparklyr` 最容易上手的地方，是很多資料操作長得像 `dplyr`：

- `select()`
- `filter()`
- `arrange()`
- `mutate()`
- `group_by()`
- `summarise()`

這種熟悉感很重要，但不要因此忘記一件事：

- 語法像 `dplyr`
- 執行位置卻常常在 Spark

也就是說，這些操作通常不是先把大表拉回 R 再算，而是先翻譯成 Spark 端可執行的工作。

## Local Tibble vs Spark Table

很多 `sparklyr` workflow 會從本地 tibble 開始，再把資料複製進 Spark。

```r
local_tbl <- tibble::tibble(
  agnetha = 1:3,
  benny = pi ^ c(1, 4, 9),
  bjorn = month.name[1:3],
  anni_frid = c(TRUE, FALSE, TRUE)
)
```

接著再讓它進入 Spark 世界，例如透過 `copy_to()` 或讀取外部來源。

心智模型可以這樣分：

- local tibble: 在 R session 記憶體裡
- Spark table / Spark DataFrame: 在 Spark 執行環境裡

## `compute()` vs `collect()`

這是 `sparklyr` 最常見、也最容易混淆的兩個動作之一。

```r
intermediate_data <- initial_data %>%
  # some calculations
  compute("an_intermediate_result")

results <- intermediate_data %>%
  # some more calculations
  collect()
```

可以先這樣理解：

- `compute()`: 把目前的轉換結果 materialize 在 Spark 端，通常形成可重用的中介結果
- `collect()`: 把結果拉回 R 端記憶體

Key point: `compute()` 是留在 Spark，`collect()` 是離開 Spark。

Warning: `collect()` 很方便，但只適合結果已經夠小、真的需要回到 R 時再用。太早 `collect()`，等於把分散式處理的好處提早丟掉。

## SQL via `DBI`

`sparklyr` 不只支援 `dplyr` 風格，也能透過 `DBI` 直接下 SQL。

```r
sql_query <- "SELECT agnetha, bjorn FROM abba WHERE anni_frid"
results <- DBI::dbGetQuery(sc, sql_query)
```

這很適合：

- 臨時查詢
- 團隊比較習慣 SQL
- 某些 join / aggregation 用 SQL 比較好表達

實務上不需要把 `dplyr` 和 SQL 當成二選一。很多 Spark workflow 本來就會混用兩種表達方式。

## Three Function Families Worth Remembering

這門課最有價值的整理之一，是把 `sparklyr` 常見功能分成三個命名家族：

- `sdf_`: Spark DataFrame helpers
- `ft_`: feature transformation helpers
- `ml_`: machine learning helpers

這個命名規則很好用，因為它比背單一 API 更能幫你建立方向感。

## `sdf_`: Spark DataFrame Helpers

`sdf_` 系列偏向 Spark 內部資料表操作與 Spark-native dataset 工作。

你可以把它理解成：

- 比純 `dplyr` 更貼近 Spark 物件本身
- 不是所有事情都要經過一般 tabular verbs

Key point: 如果 `dplyr` 比較像「表格轉換語言」，`sdf_` 比較像「Spark DataFrame 工具箱」。

## `ft_`: Feature Transformations

`ft_` 系列對應 Spark MLlib 之前的特徵處理階段。

常見用途包括：

- 類別轉索引
- 數值分箱
- 特徵向量組裝
- 其他模型前的欄位轉換

這在 Spark workflow 裡很重要，因為大規模資料的 feature engineering 最好也維持在 Spark 端完成，而不是先拉回本機再加工。

## `ml_`: Machine Learning on Spark

`ml_` 系列對應 Spark MLlib 的建模介面。

課程示意像這樣：

```r
model_formula <- reformulate(features, response = "response")

model <- training_data %>%
  ml_gradient_boosted_trees(model_formula)

predicted <- ml_predict(model, testing_data) %>%
  dplyr::pull(prediction)

results <- testing_data %>%
  dplyr::select(response) %>%
  collect() %>%
  dplyr::mutate(predicted_response = predicted)
```

這段流程反映了 Spark 上機器學習的一個常見節奏：

1. 在 Spark 中準備 training / testing data
2. 用 `ml_` 系列訓練模型
3. 用 `ml_predict()` 在 Spark 端做推論
4. 只把最終需要比較或視覺化的小結果拉回 R

## Formula Interface Still Matters

對 R 使用者來說，`reformulate()` 或 formula-style 模型指定是很自然的工作方式。

這也是 `sparklyr` 的一個實務優勢：

- 你不一定要完全改成另一套陌生建模語言
- 可以沿用 R 裡常見的 formula 思維

但也要記得，底層仍然是 Spark MLlib，不是本地 R 的所有 modeling package 都能直接等價替換。

## When `sparklyr` Is a Good Fit

`sparklyr` 特別適合這些情境：

- 你本來就在 R 生態工作
- 資料已經大到不適合全放本地記憶體
- 想保留 `dplyr` 風格而不是整個轉去 PySpark
- 想把 SQL、feature engineering、MLlib 與 R 分析 workflow 接在一起

## Practical Reminders

- `spark_connect()` / `spark_disconnect()` 是最基本的 session lifecycle。
- `dplyr` 語法在 `sparklyr` 裡常常代表 Spark 端運算，而不是本地 R 運算。
- `compute()` 是把中介結果留在 Spark，`collect()` 是把結果帶回 R。
- `DBI::dbGetQuery()` 讓 SQL 仍然是第一級入口，不必和 `dplyr` 對立。
- `sdf_`、`ft_`、`ml_` 這三個命名家族比單背函式更重要。
- 在 Spark 上建模時，盡量把 feature engineering 和 prediction 也留在 Spark 端，最後再只拉回小結果。

[Back to Data Engineering](README.md)
