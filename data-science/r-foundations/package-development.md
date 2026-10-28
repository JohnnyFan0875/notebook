[Data Science](../README.md) › [R Foundations](README.md) › R 套件開發

# R 套件開發 (R Package Development)

當同一組函式在多個專案間複製貼上、需要多人共用，或需要文件與測試時，就該把它們包成套件。套件不只是「可以 `install`」：它把函式、依賴、文件、命名空間與測試收進一個標準結構，`R CMD check` 會幫你抓出大部分問題。實驗室內部的工具套件不必上 CRAN，放 GitHub 用 `pak` 安裝就很好用。

## 開發流程

```
create_package()  →  use_r("fn")  →  load_all() 互動試用  →  寫 roxygen 註解  →  document()
       ↑                                                                          ↓
  use_package() 加依賴  ←──  check() 修到 0 errors / 0 warnings  ←──  use_test() + test()
```

```r
library(usethis)                       # 建立檔案與設定
library(devtools)                      # load / document / test / check

create_package("~/projects/labtools")  # 建立骨架並開成 RStudio 專案
use_git(); use_mit_license()

use_r("normalize")                     # 建立 R/normalize.R
load_all()                             # Ctrl/Cmd+Shift+L：模擬安裝並載入，修改後重跑即可
use_package("dplyr")                   # 加進 DESCRIPTION 的 Imports
use_package("ggplot2", type = "Suggests")

document()                             # Ctrl/Cmd+Shift+D：roxygen → man/ 與 NAMESPACE
use_testthat(); use_test("normalize")  # 建立 tests/testthat/test-normalize.R
test()                                 # Ctrl/Cmd+Shift+T
check()                                # Ctrl/Cmd+Shift+E：完整 R CMD check
install()                              # 安裝到本機 library
```

## 套件結構

```
labtools/
├── DESCRIPTION        # metadata 與依賴
├── NAMESPACE          # 匯出 / 匯入；由 roxygen 產生，不要手改
├── R/                 # 函式（只放函式定義，不放頂層執行的程式）
├── man/               # 說明文件；由 roxygen 產生
├── tests/testthat/    # 單元測試
├── inst/extdata/      # 範例資料檔：system.file("extdata", "x.csv", package = "labtools")
├── data/              # 內建資料集（use_data()）
├── vignettes/         # 長篇教學（use_vignette()）
└── src/               # C++ 程式（use_rcpp()，見 Rcpp 筆記）
```

| 檔案 / 資料夾 | 注意 |
| --- | --- |
| `R/` | 依主題分檔；不要在裡面寫 `library()`，依賴寫在 DESCRIPTION |
| `DESCRIPTION` | `Package`、`Title`、`Version`、`Description`、`License`、`Imports`、`Suggests` |
| 套件名稱 | 只能用 ASCII 字母、數字與 `.`，字母開頭；用 `available::available("name")` 檢查是否撞名 |

## 依賴

| 欄位 | 意義 | 程式內呼叫方式 |
| --- | --- | --- |
| `Imports` | 核心功能需要，安裝套件時一併安裝 | `dplyr::filter()`（建議），或 roxygen `@importFrom dplyr filter` |
| `Suggests` | 只有測試、vignette、選用功能需要 | 先 `rlang::check_installed("ggplot2")` 再用 |
| `Depends` | 會附掛到使用者的搜尋路徑 | 除了 `R (>= 4.1)` 版本需求外，幾乎不該用 |
| `LinkingTo` | 編譯時需要的 C/C++ header（Rcpp） | |

> 在套件裡用 `pkg::fn()` 寫法，讀程式時一眼就知道函式來源，也避免同名函式衝突（`dplyr::filter` vs `stats::filter`）。

## roxygen2 文件

```r
#' Normalize counts to counts per million
#'
#' Divides each column by its library size and multiplies by 1e6.
#'
#' @param counts A numeric matrix, genes in rows and samples in columns.
#' @param log Logical; return log2(CPM + 1)?
#' @returns A numeric matrix with the same dimensions as `counts`.
#' @seealso [edgeR::cpm()] for the version with TMM normalization.
#' @export
#' @examples
#' m <- matrix(c(10, 0, 90, 5, 5, 90), nrow = 3)
#' cpm(m)
cpm <- function(counts, log = FALSE) {
  stopifnot(is.matrix(counts), is.numeric(counts))
  out <- sweep(counts, 2, colSums(counts), "/") * 1e6
  if (log) log2(out + 1) else out
}
```

| 標籤 | 用途 |
| --- | --- |
| 第一行 / 第二段 | title / description |
| `@param` | 每個參數的型別與意義（寫清楚維度、單位） |
| `@returns` | 回傳型別與結構 |
| `@export` | 列入 NAMESPACE 成為公開 API；內部輔助函式不要 export |
| `@examples` | 會在 `check()` 時實際執行，等同最基本的測試 |
| `@seealso`、`@family` | 連到相關函式 |

`document()` 會由這些註解產生 `man/*.Rd` 與 `NAMESPACE`；source of truth 是註解，不要手改產生的檔案。

## testthat 測試

```r
# tests/testthat/test-normalize.R
test_that("cpm columns sum to 1e6", {
  m <- matrix(c(10, 0, 90, 5, 5, 90), nrow = 3)
  expect_equal(colSums(cpm(m)), c(1e6, 1e6))
})

test_that("cpm rejects non-matrix input", {
  expect_error(cpm(data.frame(a = 1)), "is.matrix")
})

test_that("log output is non-negative", {
  expect_true(all(cpm(diag(3), log = TRUE) >= 0))
})
```

| 該測什麼 | 例子 |
| --- | --- |
| 正常輸入的正確輸出 | 已知答案的小例子 |
| 邊界情況 | 全 0 的欄、單一樣本、空矩陣、`NA` |
| 錯誤輸入的訊息 | `expect_error()`、`expect_warning()` |
| 回傳型別與維度 | `expect_type()`、`expect_s3_class()`、`expect_equal(dim(...))` |
| 複雜輸出不變 | `expect_snapshot()` 記錄輸出，之後比對 |

修 bug 時先寫一個會失敗的測試再修，之後就不會再回歸。測試覆蓋率用 `covr::package_coverage()`。

## 分享與發佈

| 對象 | 做法 |
| --- | --- |
| 自己 / 實驗室 | 推到 GitHub，`pak::pak("user/labtools")` 安裝 |
| 文件網站 | `use_pkgdown_github_pages()`：自動產生函式文件與 vignette 網站 |
| 持續整合 | `use_github_action("check-standard")`：每次 push 在三種作業系統上跑 `check()` |
| CRAN | `check()` 零 NOTE、`devtools::check_win_devel()`、`use_release_issue()` 檢查清單 |
| Bioconductor | 需使用 Bioconductor 的類別（如 `SummarizedExperiment`）、通過 `BiocCheck::BiocCheck()`、附 vignette，依 Bioconductor 的半年發佈週期 |

版本號用 `major.minor.patch`，開發中版本加 `.9000`（`0.1.0.9000`）；`use_version()` 更新並寫入 `NEWS.md`。

## 套件 vs 分析專案

| | 套件 | 分析專案 |
| --- | --- | --- |
| 目的 | 可重用的函式 | 產出某一份結果 |
| 依賴管理 | DESCRIPTION 宣告**最低**版本 | [renv](reproducible-environments-with-renv.md) 鎖定**確切**版本 |
| 結構 | 固定（`R/`、`man/`、`tests/`） | 自由（`data/`、`scripts/`、`reports/`），見 [防禦性程式設計](defensive-programming.md) |

常見組合：通用函式抽成套件，各分析專案用 renv 鎖定包含該套件在內的環境。

## 常見錯誤

| 錯誤 | 修正 |
| --- | --- |
| 在 `R/` 裡寫 `library(dplyr)` | 改用 DESCRIPTION `Imports` + `dplyr::` |
| 什麼都放 `Depends` | 改放 `Imports` |
| 手改 `NAMESPACE` | 下次 `document()` 被覆蓋；改 roxygen 註解 |
| 修改後忘了 `load_all()` / `document()` | 跑到舊版函式或舊文件 |
| 所有函式都 `@export` | 公開 API 一旦有人用就很難改；只 export 使用者需要的 |
| `@examples` 依賴網路或大檔 | `check()` 失敗；用 `inst/extdata/` 的小檔或 `\donttest{}` |
| 從不跑 `check()` | 依賴漏宣告、文件不符等問題累積到發佈前才爆發 |
