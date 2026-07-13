# Importing Data in R

R 不只拿來分析本地 `csv`。在實際工作裡，常見來源還包括：

- relational databases
- HTTP 資源
- Web APIs
- JSON
- 其他統計軟體格式，例如 Stata / SPSS

這篇整理的是 R 裡比較進階、但又常見的讀取入口。

## Mental Model

匯入資料時，先不要只想「用哪個函式打開檔案」，而要先分辨來源型態：

- table in a database
- file on the web
- API response
- serialized file from another stats tool

來源型態不同，後續的風險也不同：

- database 會有 connection lifecycle
- web data 會有 HTTP 與格式問題
- JSON 會有 nested structure
- foreign statistical files 會有 labels 與 type conversion 問題

## Databases with `DBI`

R 連關聯式資料庫時，常見入口是 `DBI` 搭配具體驅動套件。

```r
con <- DBI::dbConnect(
  RMySQL::MySQL(),
  dbname = "company",
  host = "localhost",
  username = "user",
  password = "password"
)
```

建立連線後，最常用的幾個動作是：

- 看有哪些 tables
- 直接讀一張表
- 執行 SQL query

## Listing and Reading Tables

```r
DBI::dbListTables(con)
employees <- DBI::dbReadTable(con, "employees")
```

`dbReadTable()` 適合直接把整張表讀進 R。

但如果資料量大，通常不要把整張表無條件拉下來。

## Querying with SQL

如果只需要部分欄位或部分列，通常改用 SQL 更合理。

```r
DBI::dbGetQuery(con, "SELECT name FROM employees")
DBI::dbGetQuery(con, "SELECT * FROM products WHERE price > 100")
```

這樣的好處是：

- 把篩選推到資料庫端
- 降低資料搬運量
- 讓 R 端只接收分析需要的子集

## `dbGetQuery()` vs `dbSendQuery()`

`dbGetQuery()` 是高階、一步到位的讀法。

如果你需要更手動的流程，可以用：

```r
res <- DBI::dbSendQuery(con, "SELECT * FROM products")
data <- DBI::fetch(res)
DBI::dbClearResult(res)
```

這個模式在你要控制 result lifecycle 或逐步 fetch 時比較有用。

## Always Disconnect

資料庫連線是需要明確收尾的資源。

```r
DBI::dbDisconnect(con)
```

如果 notebook 或 script 反覆開連線卻不關，後面常會遇到資源占用與 session 殘留問題。

## Delimited Text with Base R

最基本的文字檔匯入通常還是從 base R 開始：

```r
read.csv("states.csv")
read.delim("states.txt")
```

可以把它們理解成 `read.table()` 的方便 wrapper：

- `read.csv()`: comma-separated
- `read.delim()`: tab-delimited
- `read.csv2()`: 常見於 decimal comma 的 locale
- `read.delim2()`: tab-delimited 且常配合 decimal comma

這個 mental model 很重要，因為很多匯入問題最後都會回到 `read.table()` 那組參數，例如：

- `sep`
- `header`
- `dec`
- `comment.char`
- `fill`

如果你已經知道資料是規則分隔的 text file，先分清楚是 delimiter 問題、header 問題，還是 decimal mark 問題，通常會比盲調參數快很多。

## `readr` for More Predictable Parsing

如果想要更一致的型別推論與更 tidyverse 風格的介面，常見選擇是 `readr`。

```r
readr::read_csv("states.csv")
readr::read_delim("states2.txt", delim = "/")
```

幾個常用控制點：

- `col_names = FALSE`: 沒有 header 時讓 R 自動命名
- `col_names = c(...)`: 手動指定欄名
- `col_types = "ccdd"`: 明確指定每欄型別

```r
readr::read_delim("states3.txt", delim = "/", col_names = FALSE)
readr::read_delim("states2.txt", delim = "/", col_types = "ccdd")
```

關鍵點不是背字串格式，而是知道匯入資料時可以把「欄名是否可信」與「型別是否可信」分開控制。

## Reading Files Directly from URLs

不少函式其實可以直接讀遠端檔案，而不一定要先手動下載。

```r
read.csv("http://assets.datacamp.com/course/importing_data_into_r/states.csv")
readxl::read_excel("http://assets.datacamp.com/course/importing_data_into_r/cities.xlsx")
```

這在探索型工作很方便，但正式流程通常仍要考慮：

- 網址是否穩定
- 是否需要驗證下載版本
- 網路失敗時怎麼處理

## HTTP Basics

HTTP 是 web 上資料交換的基礎協定。

重點不是背全名，而是知道：

- client 送 request
- server 回 response
- response 內容可能是 table、HTML、JSON 或其他格式

在 R 端，這常透過像 `httr` 這類套件處理。

## Why `httr` Matters

課程把 `httr` 當成進入 web data 的工具箱。

它特別重要的原因是：很多資料不再是公開檔案，而是要經過 API request 才能取得。

這和單純 `read.csv(url)` 不同，因為你可能還要處理：

- request method
- headers
- query parameters
- authentication

## JSON

JSON 是 web API 最常見的資料格式之一。

它的特性是：

- 結構清楚
- human-readable
- 很適合機器生成與解析
- 容易表達 nested objects

對 R 來說，最常見的入口是 `jsonlite`。

## Parsing JSON with `jsonlite`

```r
library(jsonlite)

fromJSON("http://www.omdbapi.com/?i=tt0095953&r=json")
```

`fromJSON()` 可以讀：

- URL
- JSON 字串
- 本地 JSON 檔案內容

## JSON Can Map to Different R Structures

例如：

```r
fromJSON('[4, 7, 4, 6, 4, 5, 10]')
fromJSON('[4, "a", 4, 6, false, null]')
fromJSON('{"id":1,"name":"Frank","age":23}')
```

解析後可能變成：

- vector
- list
- data frame-like structure

所以讀 JSON 時，重點不是只會 `fromJSON()`，而是知道結果物件接下來應該怎麼檢查。

## Serializing Back to JSON

`jsonlite` 也能把 R 物件轉回 JSON：

```r
toJSON(list(id = 1, name = "Frank"))
```

這在你要和 API 溝通、送出 payload 時很有用。

## APIs

API 可以理解成一套讓程式彼此交換資料的介面。

對資料分析工作來說，Web API 最常見的角色是：

- 提供查詢入口
- 回傳 JSON
- 透過 HTTP verbs 互動，例如 `GET`

很多時候，你並不是在「讀檔」，而是在「向服務要資料」。

## Practical API Workflow in R

典型流程通常像這樣：

1. 找到 API endpoint
2. 組 request URL 或參數
3. 取得 response
4. 把 response parse 成 R 物件
5. 整理成分析用的 tibble / data frame

一個常見簡化版是直接用 `fromJSON(url)` 讀 API response。

## Excel with `readxl`

Excel 常常不是單一表格，而是一個 workbook 裡面有多個 sheets。用 `readxl` 時，實務上常分兩步：

1. 先列出有哪些 sheets
2. 再精準讀入需要的那一張

```r
library(readxl)

excel_sheets("cities.xlsx")
read_excel("cities.xlsx")
read_excel("cities.xlsx", sheet = 2)
read_excel("cities.xlsx", sheet = "year_2000")
```

常用參數包括：

- `col_names`
- `col_types`
- `skip`

```r
read_excel(
  "cities.xlsx",
  col_names = c("Capital", "Population"),
  skip = 2
)

read_excel("cities.xlsx", col_types = c("text", "text"))
read_excel("cities.xlsx", col_types = c("text", "blank"))
```

這些控制項背後的意思很直白：

- `col_names`: header 要不要信、要不要自己指定
- `col_types`: 型別推論要不要手動接管
- `skip`: 前面是不是有說明列、空白列、報表裝飾列

Excel 匯入的核心不是「把檔案打開」，而是先判斷 sheet 結構是不是已經足夠表格化。

## When `XLConnect` Still Matters

如果需求不只是讀取，而是要操作 workbook 本身，`XLConnect` 提供更完整的 Excel 介面：

```r
library(XLConnect)

book <- loadWorkbook("cities.xlsx")
getSheets(book)
readWorksheet(book, sheet = "year_2000")
writeWorksheet(book, pop_2010, sheet = "year_2010")
removeSheet(book, sheet = "Y2010")
```

它的強項是 workbook-level 操作，例如：

- 讀指定工作表的一部分
- 寫回新的工作表
- 刪除工作表

```r
readWorksheet(
  book,
  sheet = "year_2000",
  startRow = 3,
  endRow = 4,
  header = FALSE
)
```

但它也比較重，因為常伴隨 `rJava` / Java 依賴。實務上通常可以這樣分：

- 純讀取 Excel: 優先考慮 `readxl`
- 要修改 workbook 結構: 再考慮 `XLConnect`

## `haven` for Statistical Software Files

當資料來自其他統計軟體時，`haven` 是很常見的橋接工具。

```r
library(haven)
```

常見讀取函式包括：

- `read_dta()` for Stata
- `read_sav()` for SPSS
- `read_por()` for SPSS portable files

## Reading Stata Files

```r
ontime <- read_dta("ontime.dta")
```

Stata 匯入時常要特別注意 labelled values 的表現方式。

## Reading SPSS Files

```r
ontime <- read_sav(file.path("~", "datasets", "ontime.sav"))
```

SPSS 匯入時，常見的關心點包括：

- value labels 是否保留
- 是否轉成 factor
- 缺失值標記如何表現

## Labels and Type Conversion

這類跨軟體匯入最常踩雷的地方，不是函式本身，而是語意轉換。

像課程特別提到：

- `convert.factors`
- `use.value.labels`
- `"labelled"`

心智模型可以記成：

- 原檔不只是「資料值」
- 還帶有 metadata、labels、甚至缺值語意

所以匯入後應該立刻檢查欄位型別，而不是假設它們已經是理想的 tidy format。

## Practical Checks After Import

不管來源是 DB、API、JSON 還是 foreign stats file，讀進 R 後都建議立刻檢查：

- `str(obj)`
- `class(obj)`
- `names(obj)`
- `head(obj)`

如果是 tabular data，再補看：

- 是否有怪異欄位型別
- labels 是否被保留成你能接受的形式
- 缺值是否正常變成 `NA`

## Common Traps

- 用 `dbReadTable()` 直接拉整張大表，而不是先在 SQL 端過濾
- 建立 DB connection 後忘了 `dbDisconnect()`
- 把 API 當成穩定檔案來源，卻沒處理 response 結構變化
- 讀 JSON 後直接假設它一定是 data frame
- 從 Stata / SPSS 匯入後忽略 labelled values 與型別轉換
- 看到能直接讀 URL 就跳過下載與版本管理的考量

## Related Notes

- [Functions in R](functions.md)
- [Missing Data in R](missing-data.md)
- [Ingestion](/home/johnny_fan/project/notebook/docs/data-science/data-engineering/ingestion.md:1)
