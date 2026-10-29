[Data Science](../README.md) › [Data Engineering](README.md) › sparklyr

# sparklyr

`sparklyr` 是 R 連接 Apache Spark 的介面：沿用 `dplyr`、formula 與 pipe 的寫法，但資料留在 Spark 裡處理。價值不在「R 也能跑 Spark」，而在把 Spark DataFrame、SQL、特徵工程與 MLlib 接進 R 的分析流程。Spark 的核心觀念（lazy evaluation、partition、shuffle）見 [Spark 與 PySpark](spark.md)。

## 生命週期

```r
library(sparklyr)
library(dplyr)

# spark_install(version = "3.5")          # 本機第一次使用時安裝 Spark
sc <- spark_connect(master = "local")     # 叢集：master = "yarn"；Databricks：method = "databricks_connect"

# ... 工作 ...

spark_disconnect(sc)
```

`sc` 不是本地資料，而是一個連到分散式運算環境的連線；操作是送到 Spark 執行。

## 本地 tibble vs Spark table

| 物件 | 在哪裡 | 怎麼得到 |
| --- | --- | --- |
| local tibble / data.frame | R session 記憶體 | `collect()` 的結果、一般 R 讀檔 |
| Spark table（`tbl_spark`） | Spark 執行環境 | `copy_to()`、`spark_read_*()`、`tbl(sc, "name")` |

```r
# 1. 把資料放進 Spark
expr_tbl <- spark_read_parquet(sc, name = "expr", path = "expr_parquet/")   # 大檔：直接由 Spark 讀
meta_tbl <- copy_to(sc, meta_df, "meta", overwrite = TRUE)                  # 小表：從 R 複製過去

# 2. dplyr 語法 → 翻譯成 Spark SQL，在 Spark 端執行
summary_tbl <- expr_tbl |>
  inner_join(meta_tbl, by = "sample_id") |>
  filter(tpm > 1) |>
  group_by(tissue, gene) |>
  summarise(mean_log_tpm = mean(log2(tpm + 1), na.rm = TRUE), n = n(), .groups = "drop")

show_query(summary_tbl)                 # 看翻譯出的 SQL
```

能翻譯的只有 Spark SQL 支援的函式；R 專屬函式（如自訂函式、`stringr` 的部分功能）會報錯或需要 `spark_apply()`（逐分區跑 R，慢）。

## `compute()` vs `collect()`

| 函式 | 結果在哪 | 用途 |
| --- | --- | --- |
| `compute("name")` | 留在 Spark，materialize 成可重用的中間表 | 同一中間結果要用很多次 |
| `collect()` | 拉回 R 記憶體 | 結果已經夠小，要畫圖或用 R 套件分析 |
| `sdf_register()` | 在 Spark 註冊名稱，不 materialize | 讓 SQL 可以查到它 |

```r
summary_tbl <- summary_tbl |> compute("tissue_gene_summary")   # 留在 Spark
top <- summary_tbl |> slice_max(mean_log_tpm, n = 20) |> collect()   # 只拉回小結果
```

> 太早 `collect()` 等於丟掉分散式處理的好處，還可能讓 R session 記憶體爆掉。

## 用 DBI 寫 SQL

```r
DBI::dbGetQuery(sc, "SELECT tissue, count(*) AS n FROM meta GROUP BY tissue")
```

`dplyr` 與 SQL 可以混用：臨時查詢或某些 join / window 用 SQL 較好寫時就用 SQL。

## 三個函式家族

| 前綴 | 用途 | 例子 |
| --- | --- | --- |
| `sdf_` | Spark DataFrame 工具 | `sdf_nrow()`、`sdf_sample()`、`sdf_random_split()`、`sdf_pivot()`、`sdf_register()` |
| `ft_` | 特徵轉換（Spark MLlib feature） | `ft_string_indexer()`、`ft_one_hot_encoder()`、`ft_bucketizer()`、`ft_vector_assembler()`、`ft_standard_scaler()` |
| `ml_` | 機器學習 | `ml_logistic_regression()`、`ml_random_forest()`、`ml_gradient_boosted_trees()`、`ml_predict()`、`ml_pipeline()` |

記住命名規則比背單一 API 更有方向感。

## 在 Spark 上建模

```r
splits <- sdf_random_split(model_tbl, training = 0.8, testing = 0.2, seed = 42)

model <- splits$training |>
  ml_gradient_boosted_trees(response ~ age + tissue + mean_log_tpm, type = "classification")

pred <- ml_predict(model, splits$testing)          # 仍在 Spark，含原欄位 + prediction / probability_*
ml_binary_classification_evaluator(pred, label_col = "response", raw_prediction_col = "rawPrediction")

result <- pred |> select(response, prediction) |> collect()   # 只拉回需要比較的欄
```

> 不要把 `ml_predict()` 的 `prediction` 單獨 `pull()` 出來，再和另外 `collect()` 的測試資料按順序綁在一起：Spark 不保證列順序，結果可能錯位。直接從 `pred` 一起取出。

formula 介面讓 R 使用者不必改用陌生的建模語言，但底層是 Spark MLlib，不是所有 R 建模套件都有對應。隨機切分只適合獨立樣本；有病人、批次或時間結構時要依群組或時間切，見 [交叉驗證](../machine-learning/workflow/cross-validation.md)。

## 什麼時候用 sparklyr

| 適合 | 不適合 |
| --- | --- |
| 已在 R 生態、資料大到不適合放本地記憶體 | 資料放得進記憶體：直接用 `dplyr` / `data.table` / `arrow` / `duckdb` |
| 想保留 `dplyr` 風格，而不是整個改寫成 PySpark | 需要大量 R 專屬套件的分析（只能 `collect()` 後做） |
| 要在 Databricks / 叢集上和 PySpark 使用者共用同一份資料 | |

R 的單機大資料選項見 [超出記憶體的處理](scalable-processing-and-out-of-core.md)。
