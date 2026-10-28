[Data Science](../README.md) › R Foundations

# R 基礎 (R Foundations)

資料分析中反覆用到的 R：資料結構與函式、tidyverse / data.table 資料整理、匯入與缺值處理，以及效能、套件化與文字處理。生資分析大量依賴 R 與 Bioconductor，這裡是讀懂那些套件的前置知識。Python 的對應內容見 [Python Foundations](../python-foundations/README.md)。

## 建議順序

```
資料結構 → 類別資料 → 控制流程 → 函式 → 日期時間 → 匯入 → 缺值
                                                        ↓
     Bioconductor ← 統計函式 ← data.table ← join / reshape ← tidyverse
```

只需要整理表格的人：讀完第一排後直接進 tidyverse；處理千萬列以上資料再補 data.table。

## 語言基礎

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [資料結構](data-structures.md) | vector、matrix、data frame / tibble、list、強制轉型 | `[` 和 `[[` 差在哪？為什麼整欄變成字串？ |
| [類別資料](categorical-data.md) | factor、levels、參考組、`cut()`、forcats | 為什麼 fold change 方向反了？ |
| [控制流程](control-flow.md) | `if`、`case_when()`、迴圈、何時向量化 | 這裡該寫迴圈還是向量化？ |
| [函式](functions.md) | 參數、預設值、`...`、輸入檢查、`tryCatch()` | 如何寫出可重用、會早失敗的函式？ |
| [防禦性程式設計](defensive-programming.md) | 斷言、join 後驗證、風格、專案結構、`here` / `renv` | 如何讓腳本不悄悄算錯？ |
| [物件導向：S3 與 R6](object-oriented-programming-s3-r6.md) | method dispatch、R6 class | `print()` / `summary()` 怎麼知道要做什麼？ |
| [函數式程式設計](functional-programming.md) | apply 家族、purrr、`safely()` | 如何對很多檔案 / 模型重複做同一件事？ |

## 資料整理

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [日期與時間](datetime.md) | `Date` / `POSIXct`、lubridate、period vs duration、時區 | 日期欄位怎麼解析、怎麼算追蹤時間？ |
| [匯入資料](importing-data.md) | readr、Excel、JSON / httr2、DBI、haven、arrow、生資格式 | 這個檔案該用什麼讀？讀完要檢查什麼？ |
| [缺失值](missing-data.md) | `NA` 行為、藏起來的缺值、naniar、shadow matrix | 缺值在哪裡、有沒有模式？ |
| [Tidyverse 工作流](tidyverse-workflow.md) | tidy data、`\|>`、核心 verbs、`.by`、接 ggplot2 | dplyr 的基本節奏是什麼？ |
| [dplyr 合併資料](joining-data-with-dplyr.md) | join 類型、`join_by()`、區間 join、cardinality 檢查 | join 後列數為什麼變多 / 變少？ |
| [tidyr 資料重塑](data-reshaping-with-tidyr.md) | pivot、拆欄、`complete()`、巢狀資料展開 | 寬表、長表怎麼互轉？ |
| [dplyr 程式化模式](dplyr-programming-patterns.md) | tidyselect、`across()`、`{{ }}`、`.data` | 如何寫接受欄名參數的函式？ |
| [data.table](data-table-joins-and-reshaping.md) | `DT[i, j, by]`、`:=`、join、rolling / overlap join | 大資料怎麼又快又省記憶體？ |

## 統計與建模

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [統計函式速查](statistical-functions.md) | `d/p/q/r` 分配函式、描述統計、檢定、`p.adjust()` | 這個檢定在 R 裡怎麼寫？ |
| [解釋型建模](explanatory-modeling-in-r.md) | `lm()` / `glm()`、broom、模型比較 | 如何建模並解讀係數？ |
| [tidymodels](../machine-learning/packages/tidymodels/README.md) | recipes、parsnip、workflows、tune | 如何在 R 做 ML pipeline？ |
| [抽樣與調查資料](../statistics/inferential-statistics/survey-sampling.md) | 分層抽樣、bootstrap、survey 套件 | 如何處理有抽樣設計的資料？ |

## 效能、工程化與報告

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [寫出有效率的 R](writing-efficient-r-code.md) | 量測、向量化、記憶體 | 程式哪裡慢？ |
| [Rcpp](rcpp-for-r-performance.md) | 用 C++ 寫熱點函式 | 向量化不夠快時怎麼辦？ |
| [平行運算](parallel-programming-in-r.md) | parallel、future、foreach | 如何用滿多核心？ |
| [R 套件開發](package-development.md) | usethis、roxygen2、testthat | 如何把函式打包、測試、分享？ |
| [R Markdown 報告](reporting-with-r-markdown.md) | R Markdown / Quarto、參數化報告 | 如何產出可重跑的分析報告？ |

## 文字資料

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [正規表示式](regular-expressions.md) | stringr、regex pattern | 如何從字串擷取、驗證、替換？ |
| [字串距離與模糊比對](string-distance-and-fuzzy-matching.md) | stringdist、fuzzy join | 拼錯、別名怎麼對起來？ |
| [文字分析](text-analysis.md) | tidytext、sentiment、LDA | 如何把文件轉成可分析的 tokens？ |
| [rvest 網頁擷取](../web-scraping/rvest.md) | rvest、httr2 | 如何在 R 抓網頁表格？ |

## 相關章節

| 需求 | 去哪裡 |
| --- | --- |
| Bioconductor 物件、`SummarizedExperiment` | [Bioconductor 入門](../../biology/genomics/sequencing-and-analysis/workflows/bioconductor-introduction.md) |
| RNA-seq 差異表現（DESeq2 / limma） | [DESeq2](../../biology/genomics/sequencing-and-analysis/workflows/rnaseq-differential-expression-with-deseq2.md)、[limma](../../biology/genomics/sequencing-and-analysis/workflows/limma-differential-expression.md) |
| 統計方法的選擇與解讀 | [Statistics](../statistics/README.md) |
| EDA 流程與圖表原則 | [Data Manipulation and EDA](../data-manipulation-and-eda/README.md) |
| SQL | [Databases](../databases/README.md) |
| 大資料：sparklyr | [Data Engineering](../data-engineering/README.md) |
