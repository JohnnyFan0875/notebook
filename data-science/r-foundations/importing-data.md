[Data Science](../README.md) › [R Foundations](README.md) › 匯入資料

# 匯入資料 (Importing Data)

先分辨來源型態，再挑工具：文字檔要處理分隔符與型別，Excel 要處理工作表結構，API 回傳巢狀 JSON，資料庫要管理連線，其他統計軟體的檔案帶有 label 與缺值語意。Python 對應見 [匯入資料（Python）](../python-foundations/importing-data.md)；正式的資料擷取管線見 [Ingestion](../data-engineering/ingestion.md)。

| 來源 | 首選 | 備選 / 說明 |
| --- | --- | --- |
| CSV / TSV | `readr::read_csv()` / `read_tsv()` | `data.table::fread()`（大檔最快）、base `read.csv()` |
| Excel | `readxl::read_excel()` | 寫檔：`writexl`、`openxlsx` |
| JSON / API | `jsonlite::fromJSON()`、`httr2` | |
| 關聯式資料庫 | `DBI` + 驅動（`RPostgres`、`RMariaDB`、`RSQLite`、`duckdb`） | `dbplyr` 把 dplyr 翻成 SQL |
| Stata / SPSS / SAS | `haven` | |
| Parquet / Arrow / Feather | `arrow` | 大於記憶體的資料：`open_dataset()` |
| R 物件 | `readRDS()` / `saveRDS()` | `qs` 套件更快 |
| 生資格式 | Bioconductor 專用讀取器 | 見 [生資檔案格式](#生資檔案格式) |

## 分隔文字檔

```r
library(readr)

df <- read_csv("samples.csv")                         # 印出推論的欄型別，務必看一眼
df <- read_tsv("counts.tsv.gz")                       # 自動解壓 .gz / .bz2 / .zip
read_delim("states2.txt", delim = "/")

# 明確指定型別：ID 保持字串（避免 "001" → 1）、日期指定格式
df <- read_csv("samples.csv",
  col_types = cols(
    sample_id = col_character(),
    age       = col_integer(),
    date      = col_date("%Y-%m-%d"),
    .default  = col_guess()
  ),
  na = c("", "NA", "N/A", "-"),                       # 哪些字串視為缺值
  skip = 2, comment = "#"                             # 跳過說明列、註解
)
problems(df)                                          # 解析失敗的列與原因

read_csv(c("a.csv", "b.csv"), id = "file")            # 多檔一次讀，記錄來源

# 大檔：data.table::fread 多執行緒，自動偵測分隔符
dt <- data.table::fread("variants.tsv.gz", select = c("chrom", "pos", "qual"))
```

| | base `read.csv()` | `readr::read_csv()` | `data.table::fread()` |
| --- | --- | --- | --- |
| 速度 | 慢 | 快 | 最快 |
| 回傳 | data.frame | tibble | data.table |
| 欄名 | `make.names()` 改寫（`my col` → `my.col`） | 保留原樣 | 保留原樣 |
| 型別推論 | 前幾列 | 前 1000 列，並回報 | 抽樣整檔 |
| 逗號作小數點 | `read.csv2()` | `read_csv2()` / `locale(decimal_mark = ",")` | `dec = ","` |

> base R 的 `read.table()` 家族（`read.csv`、`read.delim`、`read.csv2`、`read.delim2`）共用 `sep`、`header`、`dec`、`comment.char`、`fill` 等參數；匯入出錯時先判斷是分隔符、表頭還是小數點的問題。

讀遠端檔案：`read_csv("https://...")` 可直接讀，但正式流程應先下載、記錄版本與 checksum，避免網址失效或內容悄悄改變。

## Excel

```r
library(readxl)

excel_sheets("cities.xlsx")                           # 先列出工作表
read_excel("cities.xlsx", sheet = "year_2000")        # 依名稱或位置
read_excel("cities.xlsx", sheet = 2,
           range = "B3:D50",                          # 只讀一個區塊
           skip = 2, col_names = c("capital", "pop"),
           col_types = c("text", "numeric"),          # "skip" 可略過欄
           na = c("", "NA"))

# 所有工作表讀成 list
path <- "cities.xlsx"
sheets <- purrr::map(setNames(excel_sheets(path), excel_sheets(path)),
                     \(s) read_excel(path, sheet = s))

writexl::write_xlsx(list(summary = res, raw = df), "report.xlsx")   # 寫多個工作表
```

> 需要格式、公式、修改既有活頁簿時用 `openxlsx`；舊筆記常見的 `XLConnect` 依賴 Java（`rJava`），安裝麻煩，已少用。Excel 會把基因名轉成日期，見 [日期與時間](datetime.md#excel-帶來的日期問題)。

## JSON

```r
library(jsonlite)

fromJSON('[4, 7, 4, 6]')                       # integer vector
fromJSON('[4, "a", false, null]')              # 混合型別 → 強制轉成 character vector
fromJSON('{"id":1,"name":"Frank"}')            # named list
fromJSON('[{"id":1,"x":2},{"id":2,"x":5}]')    # data.frame（物件陣列自動簡化）
fromJSON("data.json", simplifyVector = FALSE)  # 保留原始巢狀 list

toJSON(list(id = 1, name = "Frank"), auto_unbox = TRUE)   # {"id":1,"name":"Frank"}
```

巢狀結構讀進來常變成 list-column，用 `tidyr::unnest_wider()` / `unnest_longer()` 展開，見 [tidyr 資料重塑](data-reshaping-with-tidyr.md#巢狀資料展開-rectangling)。

## HTTP 與 API

`httr2` 是 `httr` 的後繼版本，以 pipe 組裝 request。

```r
library(httr2)

resp <- request("https://rest.ensembl.org") |>
  req_url_path_append("lookup/symbol/homo_sapiens/BRCA2") |>
  req_url_query(expand = 1) |>
  req_headers(Accept = "application/json") |>
  req_retry(max_tries = 3) |>                  # 失敗自動重試（含 429 / 503）
  req_throttle(rate = 10 / 1) |>               # 每秒最多 10 次，遵守 API 限制
  req_perform()

resp_status(resp)                              # 200
gene <- resp_body_json(resp)                   # 解析成 list
gene$id                                        # "ENSG00000139618"

# 認證：token 放環境變數，不要寫進程式
request(url) |> req_auth_bearer_token(Sys.getenv("API_TOKEN"))
```

| 步驟 | 注意 |
| --- | --- |
| 找 endpoint 與參數 | 讀 API 文件；先用瀏覽器或 `curl` 試 |
| 限速與重試 | NCBI E-utilities 無 API key 時每秒 3 次 |
| 分頁 | 迴圈抓到沒有下一頁為止；`req_perform_iterative()` |
| 解析 | JSON → list → tibble；檢查欄位缺失 |
| 快取 | 結果存檔，避免重複請求 |

常用生資 API 多半已有 R 包裝（`biomaRt`、`rentrez`、`KEGGREST`），先找套件再自己寫 request。HTTP 觀念見 [API 與 HTTP（Python）](../python-foundations/api-http.md)。

## 資料庫：DBI

```r
library(DBI)

con <- dbConnect(RPostgres::Postgres(),
                 dbname = "lab", host = "localhost",
                 user = Sys.getenv("DB_USER"),
                 password = Sys.getenv("DB_PASS"))     # 帳密不寫死；或用 keyring 套件
on.exit(dbDisconnect(con), add = TRUE)                 # 在函式內：離開時一定關連線

dbListTables(con)
dbReadTable(con, "samples")                            # 整張表（小表才用）
dbGetQuery(con, "SELECT sample_id, tissue FROM samples WHERE age > 60")   # 篩選推到資料庫端

# 參數化查詢：避免 SQL injection 與引號問題
dbGetQuery(con, "SELECT * FROM samples WHERE tissue = $1", params = list("liver"))

# 大結果分批讀
res <- dbSendQuery(con, "SELECT * FROM variants")
while (!dbHasCompleted(res)) chunk <- dbFetch(res, n = 1e5)   # 每次 10 萬列
dbClearResult(res)

dbWriteTable(con, "results", results_df, overwrite = TRUE)

# dbplyr：寫 dplyr，在資料庫執行
tbl(con, "samples") |> filter(age > 60) |> count(tissue) |> show_query()
tbl(con, "samples") |> filter(age > 60) |> collect()   # collect() 才把資料拉回 R
```

本地分析大檔不需要資料庫伺服器：`duckdb` 可以直接用 SQL 查 CSV / Parquet（完整用法見 [DuckDB 與 Parquet](../databases/duckdb-and-parquet.md)）。

```r
con <- dbConnect(duckdb::duckdb())
dbGetQuery(con, "SELECT chrom, count(*) FROM 'variants.parquet' GROUP BY chrom")
```

SQL 本身見 [Databases](../databases/README.md)。

## Stata / SPSS / SAS：haven

```r
library(haven)

d <- read_dta("ontime.dta")            # Stata
d <- read_sav("survey.sav")            # SPSS；read_por() 讀 portable 檔
d <- read_sas("trial.sas7bdat")        # SAS

# 帶 value label 的欄位是 haven_labelled 型別
d$sex                                  # 1 [Male], 2 [Female]
d <- as_factor(d)                      # 依 label 轉成 factor（整個 data frame）
zap_labels(d$sex)                      # 只留數值
d <- zap_missing(d)                    # SPSS 使用者定義缺值（-9、999）轉 NA
```

> SPSS / Stata 常用 `-9`、`999` 表示缺值。沒處理就計算平均會嚴重失真；匯入後先 `summary()` 看極端值。

## Parquet 與大於記憶體的資料

```r
library(arrow)

write_parquet(df, "samples.parquet")           # 欄式、壓縮、保留型別
df <- read_parquet("samples.parquet", col_select = c(sample_id, tissue))

# 多檔資料集：延遲計算，只讀需要的欄與列
ds <- open_dataset("variants/", format = "parquet")   # 可依 chrom= 分割資料夾
ds |> filter(chrom == "chr17", qual > 30) |> select(pos, ref, alt) |> collect()
```

| 格式 | 跨語言 | 保留型別 | 適用 |
| --- | --- | --- | --- |
| CSV | 是 | 否 | 交換、人工檢查 |
| `.rds` | 否（只有 R） | 是，含任何 R 物件 | 存中間結果、模型 |
| Parquet | 是（Python / Spark / DuckDB） | 是 | 大型表格、跨語言共用 |

## 生資檔案格式

| 格式 | R 讀取 | 回傳 |
| --- | --- | --- |
| BED / GTF / GFF | `rtracklayer::import()` | `GRanges` |
| VCF | `VariantAnnotation::readVcf()`；表格化用 `vcfR` | `VCF` 物件 |
| BAM | `Rsamtools`、`GenomicAlignments::readGAlignments()` | 比對結果 |
| FASTA / FASTQ | `Biostrings::readDNAStringSet()`、`ShortRead` | 序列集合 |
| salmon / kallisto 定量 | `tximport`、`tximeta` | 基因層級 counts |
| 10x（`matrix.mtx`、`.h5`） | `Seurat::Read10X()`、`DropletUtils::read10xCounts()` | 稀疏矩陣 / `SingleCellExperiment` |
| AnnData `.h5ad` | `zellkonverter::readH5AD()` | `SingleCellExperiment` |
| HDF5 | `rhdf5`、`HDF5Array` | 陣列（可不載入記憶體） |

這些套件多數來自 Bioconductor，安裝用 `BiocManager::install()`；見 [Bioconductor 入門](../../biology/genomics/sequencing-and-analysis/workflows/bioconductor-introduction.md)。

## 匯入後的檢查

```r
dim(df); glimpse(df)                           # 列數、欄數、型別
problems(df)                                   # readr 解析問題
colSums(is.na(df))                             # 每欄缺值
summary(df)                                    # 極端值、編碼成數字的缺值
anyDuplicated(df$sample_id)                    # ID 唯一？
```

| 症狀 | 可能原因 |
| --- | --- |
| 數值欄變 character | 混入 `"<0.01"`、`"N/A"`、千分位逗號 |
| ID 前導 0 消失 | 被推論成數值；指定 `col_character()` |
| 列數比預期少 | 引號未閉合、`comment` 字元出現在資料中 |
| 中文亂碼 | 編碼不是 UTF-8：`locale(encoding = "Big5")` |
| 欄名有空白、特殊字元 | `janitor::clean_names()` |
