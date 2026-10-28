[Data Science](../README.md) › [R Foundations](README.md) › 正規表示式

# 正規表示式 (Regular Expressions in R)

樣本名稱、檔名、基因 ID、註解欄位常有固定但不整齊的格式。正規表示式 (regex) 用來**偵測、擷取、取代**這些模式。R 中主要透過 `stringr`（tidyverse，底層是 ICU 的 `stringi`）使用；語法與 Python `re` 幾乎相同，Python 版見 [文字清理與正規表示式](../python-foundations/text-cleaning-and-regex.md)，shell 的 `grep` / wildcard 見 [Regex 與 Wildcard](../../computing/operating-system/regex-wildcard.md)。

## stringr 函式速查

| 想做 | stringr | base R | 回傳 |
| --- | --- | --- | --- |
| 有沒有符合 | `str_detect(x, p)` | `grepl(p, x)` | logical |
| 哪幾個符合 | `str_which(x, p)` | `grep(p, x)` | 索引 |
| 只留符合的 | `str_subset(x, p)` | `grep(p, x, value = TRUE)` | character |
| 擷取第一個符合 | `str_extract(x, p)` | `regmatches(x, regexpr(p, x))` | character（無則 `NA`） |
| 擷取全部符合 | `str_extract_all(x, p)` | `regmatches(x, gregexpr(p, x))` | list |
| 擷取 capture groups | `str_match(x, p)` | `regexec()` | matrix：第 1 欄完整符合，之後每個 group 一欄 |
| 取代第一個 / 全部 | `str_replace()` / `str_replace_all()` | `sub()` / `gsub()` | character |
| 移除 | `str_remove()` / `str_remove_all()` | `gsub(p, "", x)` | character |
| 計數 | `str_count(x, p)` | | integer |
| 切分 | `str_split(x, p)` | `strsplit(x, p)` | list |
| 拆成多欄（data frame） | `tidyr::separate_wider_regex()` | | tibble |

> 參數順序：stringr 一律**資料在前、pattern 在後**，可以接 pipe；base R 的 `grepl` / `sub` 是 pattern 在前。

## 語法速查

R 字串中的 `\` 本身要跳脫，所以 regex 的 `\d` 要寫成 `"\\d"`。R ≥ 4.0 可用 raw string `r"(\d+)"` 避免雙反斜線。

| 類別 | 語法 | 意義 |
| --- | --- | --- |
| 錨點 | `^` / `$` | 字串開頭 / 結尾 |
| | `\\b` | 字詞邊界 |
| 字元類別 | `.` | 任意字元（字面的點要寫 `\\.`） |
| | `\\d` / `\\D` | 數字 / 非數字 |
| | `\\w` / `\\W` | 字母數字底線 / 相反 |
| | `\\s` / `\\S` | 空白 / 非空白 |
| | `[ACGT]` / `[^ACGT]` | 集合內 / 集合外任一字元 |
| | `[A-Za-z]`、`[[:alpha:]]`、`[[:punct:]]` | 範圍、POSIX 類別 |
| 數量 | `*` / `+` / `?` | 0 次以上 / 1 次以上 / 0 或 1 次 |
| | `{n}` / `{n,}` / `{n,m}` | 恰好 n 次 / 至少 n / n 到 m 次 |
| | `+?`、`*?` | 非貪婪（盡量少） |
| 群組 | `(...)` | 擷取群組；取代時用 `\\1`、`\\2` 引用 |
| | `(?:...)` | 只分組不擷取 |
| | `a\|b` | 或 |
| 環視 | `(?=...)` / `(?!...)` | 後面是 / 不是（不消耗字元） |
| | `(?<=...)` / `(?<!...)` | 前面是 / 不是 |

```r
library(stringr)

str_match("Book", "^.")        # "B"
str_match("Book", ".$")        # "k"
str_match("Book", "\\.")       # NA：沒有字面上的點
str_match_all("Toy Story 3", "[\\d\\s]")   # " ", " ", "3"
```

## 修飾：大小寫、字面比對

```r
str_detect("TP53", regex("tp53", ignore_case = TRUE))   # TRUE
str_detect("a.b", fixed("."))                           # 字面比對，不解讀為 regex，也最快
str_detect(x, coll("é", locale = "fr"))                  # 依語系比較（重音、大小寫規則）
str_view(c("chr1", "chrX"), "chr\\d")                   # 在 console 標示符合位置，除錯用
```

## 擷取與重組

```r
log <- "payload: 'Adam, 5, 3', headers: 'Auth...'"
p   <- "([A-Za-z]+), (\\d+), (\\d+)"

str_match(log, p)
#      [,1]          [,2]   [,3] [,4]
# [1,] "Adam, 5, 3"  "Adam" "5"  "3"

str_replace(log, p, "\\1 tried to log in \\2 times.")
# "payload: 'Adam tried to log in 5 times.', headers: 'Auth...'"
```

長 pattern 拆成具名片段再組合，比一行難讀的 regex 好維護：

```r
pieces <- c(name = "[A-Za-z]+", sep = ", ", attempts = "\\d+", sep = ", ", logins = "\\d+")
pattern <- paste0(pieces, collapse = "")

# 直接拆成 data frame 欄位：具名的片段變成欄，未命名的被丟棄
tibble::tibble(x = c("Adam, 5, 3", "Bea, 2, 1")) |>
  tidyr::separate_wider_regex(x, c(name = "[A-Za-z]+", ", ", attempts = "\\d+", ", ", logins = "\\d+"))
```

## 生資常見範例

```r
# 1. 去掉 Ensembl ID 的版本號，才能和其他註解表 join
str_remove("ENSG00000141510.18", "\\.\\d+$")            # "ENSG00000141510"

# 2. 驗證 ID 格式
str_detect(ids, "^ENSG\\d{11}(\\.\\d+)?$")

# 3. 從 FASTQ 檔名解析樣本、lane、read（Illumina 命名慣例）
f <- "Tumor-01_S3_L002_R1_001.fastq.gz"
str_match(f, "^(.+)_S(\\d+)_L(\\d{3})_R([12])_\\d{3}\\.fastq\\.gz$")[, -1]
# "Tumor-01" "3" "002" "1"

# 4. 統一樣本名稱：大小寫、空白、分隔符
str_to_lower(x) |> str_squish() |> str_replace_all("[\\s.-]+", "_")

# 5. 染色體命名統一（UCSC "chr1" vs Ensembl "1"）
str_remove(chrom, "^chr")

# 6. 找 motif 的所有位置（含重疊）：用 lookahead 才不會消耗字元
str_locate_all("ATATAT", "(?=ATA)")[[1]][, "start"]     # 1 3
str_count("ATATAT", "ATA")                              # 1：一般比對不重疊
```

序列層級的比對（容許錯配、反向互補）用 Bioconductor `Biostrings::matchPattern()` / `vmatchPattern()`，不要用 regex 硬寫。

## 字串模板：glue

組訊息、檔名、標籤時，`glue` 比 `paste0()` 好讀：

```r
library(glue)
sample <- "S01"; n <- 23e6
glue("{sample}: {format(n, big.mark = ',')} reads")      # "S01: 23,000,000 reads"
glue("results/{sample}_{Sys.Date()}.csv")
glue("Hi {a} and {b}", a = "Ann", b = NA, .na = "")     # NA 顯示為空字串
```

`stringr::str_glue()` 是同樣的功能。

## 常見錯誤

| 錯誤 | 修正 |
| --- | --- |
| 用 `.` 想比對句點 | `\\.` 或 `fixed(".")` |
| 少一個反斜線：`"\d"` | R 字串需 `"\\d"`；或 raw string `r"(\d)"` |
| 沒加錨點：`"chr1"` 也符合 `chr10`、`chr11` | `"^chr1$"` 或 `\\b` |
| 用 `str_detect()` 想取值 | 它只回 `TRUE` / `FALSE`；取值用 `str_extract()` / `str_match()` |
| 貪婪比對吃太多：`"<.*>"` 在 `"<a><b>"` 符合整串 | 非貪婪 `"<.*?>"` 或否定類別 `"<[^>]*>"` |
| 取代時忘記 backreference | `"\\1"`，不是 `"$1"` |
| `ifelse(str_detect(x, p), ...)` 遇到 `NA` | `str_detect(NA, p)` 回傳 `NA`；必要時先處理缺值 |
