[Data Science](../README.md) › [R Foundations](README.md) › 防禦性程式設計

# 防禦性程式設計 (Defensive Programming)

讓錯誤**早一點暴露、訊息看得懂、不悄悄變成錯誤結論**。分析腳本最危險的不是報錯，而是沒報錯卻算錯（欄位對錯、join 爆量、NA 被當成 0）。函式層級的輸入檢查與 `tryCatch()` 見 [函式](functions.md#輸入檢查與錯誤處理)；Python 對應見 [錯誤處理與斷言](../python-foundations/errors-and-assertions.md)、[軟體工程實務](../python-foundations/software-engineering.md)。

## 語言層級的小陷阱

| 寫法 | 風險 | 改成 |
| --- | --- | --- |
| `T` / `F` | 只是普通變數，可被 `T <- 0` 覆蓋 | `TRUE` / `FALSE` |
| `if (x)` | `x` 可能是長度 > 1、`NA` 或數字 | `if (isTRUE(x))` |
| `1:length(x)` | 空 vector 會得到 `1 0` | `seq_along(x)`、`seq_len(n)` |
| `df$col` | 部分比對到別的欄 | `df[["col"]]` |
| `sapply()` | 回傳型別隨輸入變（vector / matrix / list） | `vapply(x, f, numeric(1))` 或 `purrr::map_dbl()` |
| `x == NA` | 永遠是 `NA` | `is.na(x)` |
| `ifelse()` 處理日期 | 丟失 `Date` 屬性 | `dplyr::if_else()` |

```r
isTRUE(TRUE); isTRUE(c(TRUE, TRUE)); isTRUE(NA)   # TRUE FALSE FALSE
```

## 在資料流程中加斷言

在關鍵步驟後檢查假設，比事後追查結果異常快得多。

```r
library(dplyr)

stopifnot(
  !anyDuplicated(samples$sample_id),               # ID 唯一
  all(c("sample_id", "condition") %in% names(samples)),
  !anyNA(samples$condition)
)

n_before <- nrow(counts)
merged <- left_join(counts, samples, by = "sample_id",
                    relationship = "many-to-one")   # dplyr ≥ 1.1.0：違反就報錯（防 join 爆量）
stopifnot(nrow(merged) == n_before)

# 計數矩陣的欄順序要和 metadata 列順序一致（DESeq2 不會幫你對齊）
stopifnot(identical(colnames(count_mat), samples$sample_id))
```

| 工具 | 用途 |
| --- | --- |
| `stopifnot()` | base R，簡單斷言 |
| `checkmate` | `assert_numeric(x, lower = 0, any.missing = FALSE)`，訊息清楚、速度快 |
| `rlang::abort()` / `cli::cli_abort()` | 結構化、格式化的錯誤訊息（tidyverse 套件慣用） |
| `validate` / `pointblank` | 資料層級的規則檢查與報告，見 [資料品質檢查](../data-engineering/data-quality-checks.md) |
| `testthat` | 函式的單元測試，見 [R 套件開發](package-development.md) |

## DRY：不要複製貼上

複製一次可以接受，第二次要警覺，第三次就該抽成函式、共用常數或參數化流程。重複越多，修 bug 時漏改其中一份的機率越高。

```r
# 重複三次的清理邏輯 → 一個函式 + map
clean_batch <- function(path) readr::read_csv(path) |> janitor::clean_names() |> filter(qc_pass)
batches <- purrr::map(list.files("data", full.names = TRUE), clean_batch)
```

## 風格與靜態檢查

一致的格式讓錯誤更容易被看到：`res <- t.test(x, paired = FALSE)` 比 `res<-t.test(x,paired=FALSE)` 好掃描。

| 工具 | 做什麼 |
| --- | --- |
| `styler::style_file("analysis.R")` | 依 tidyverse style guide 自動排版 |
| `lintr::lint("analysis.R")` | 靜態檢查：未使用變數、`T`/`F`、過長行 |
| RStudio / Positron 診斷 | 編輯時即時提示 |

## 檔名與專案結構

| 原則 | 好 | 避免 |
| --- | --- | --- |
| 不用空白 | `load-survival-data.R` | `my final script.R`（shell 要加引號、URL 變 `%20`） |
| 可排序 | `01-import.R`、`02-clean.R` | `import.R`、`clean_new2.R` |
| 副檔名一致 | 一律 `.R` | `.r` / `.R` 混用 |
| 日期用 ISO | `2024-03-15-qc-report.html` | `3-15-24-report.html` |

```
project/
├── project.Rproj        # 或 .here 檔；搭配 here::here() 取路徑，不要 setwd()
├── renv.lock            # 套件版本鎖定（renv::init() / renv::snapshot()）
├── R/                   # 函式
├── analysis/            # 依序執行的腳本或 .qmd
├── data/raw/            # 原始資料，唯讀
├── data/processed/
└── output/
```

> `setwd("C:/Users/me/...")` 寫死絕對路徑，換台電腦就壞。用 RStudio Project 或 `here::here("data", "raw", "counts.csv")`。

## 最小習慣清單

| 習慣 | 成本 | 效果 |
| --- | --- | --- |
| 不用 `T` / `F`，迴圈用 `seq_along()` | 零 | 避免隱性錯誤 |
| join / filter 後檢查列數 | 一行 | 抓到 join 爆量、誤刪資料 |
| 關鍵輸入加 `stopifnot()` | 一行 | 早失敗 |
| warning 要讀，不要一律 `suppressWarnings()` | 零 | 解析失敗、NA 產生常藏在 warning 裡 |
| 固定 seed：`set.seed(42)` | 一行 | 隨機結果可重現 |
| `sessionInfo()` 或 `renv` 記錄版本 | 一行 | 結果可重現 |
