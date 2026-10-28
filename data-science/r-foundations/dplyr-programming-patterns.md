[Data Science](../README.md) › [R Foundations](README.md) › dplyr 程式化模式

# dplyr 程式化模式 (dplyr Programming Patterns)

一次性的 pipeline 變成要對不同欄位、不同資料表重複套用時，需要三種工具：**tidyselect** 規則化選欄、**`across()`** 批次轉換多欄、**tidy evaluation (`{{ }}`)** 讓函式接受欄名參數。基本 verbs 見 [Tidyverse 工作流](tidyverse-workflow.md)。

```
同一段 pipeline 重複貼？ → 包成函式（參數是值）
很多欄套同一轉換？      → across() + 選欄 helper
函式參數是「欄名」？    → {{ col }}；動態輸出欄名 → "mean_{{ col }}" :=
```

## 選欄 helper (tidyselect)

| helper | 選到 | 例子 |
| --- | --- | --- |
| `starts_with()` / `ends_with()` | 前綴 / 後綴 | `starts_with("perc")` |
| `contains()` | 包含字串 | `contains("rate")` |
| `matches()` | regex | `matches("^(CD|HLA)")` |
| `where()` | 依型別或條件 | `where(is.numeric)` |
| `all_of()` / `any_of()` | 字串向量（缺欄時報錯 / 忽略） | `all_of(c("id", "age"))` |
| `everything()` / `last_col()` | 全部 / 最後一欄 | |
| `a:b`、`!`、`&`、`\|` | 範圍、排除、組合 | `!where(is.numeric)` |

```r
world_bank |> select(country, year, starts_with("perc"))
world_bank |> relocate(matches("^perc"), .after = year)     # 只改順序
meta |> select(any_of(c("sample_id", "batch", "age")))      # 欄位可能不存在時

cols <- c("TP53", "MYC")
expr |> select(all_of(cols))      # 欄名在變數裡：用 all_of()，不要直接 select(cols)
```

## `across()`：多欄同一轉換

```r
world_bank |>
  mutate(across(starts_with("perc"), \(x) x / 100))           # 百分比 → 比例

world_bank |>
  summarize(across(ends_with("rate"), \(x) mean(x, na.rm = TRUE)), .by = region)

# 多個函式 + 命名規則
expr_tbl |>
  summarize(across(where(is.numeric), list(mean = mean, sd = sd), .names = "{.col}_{.fn}"))

# 依型別分組計數
df |> count(across(!where(is.numeric)))
```

> dplyr ≥ 1.1.0 已棄用把額外參數傳給 `across()`（`across(x, mean, na.rm = TRUE)`），改用匿名函式 `\(x) mean(x, na.rm = TRUE)`。

### 同一列多欄計算

```r
# 快：向量化的列運算
scores |> mutate(total = rowSums(pick(q1:q10), na.rm = TRUE),
                 mean_q = rowMeans(pick(starts_with("q")), na.rm = TRUE))

# 通用但慢：rowwise + c_across（逐列呼叫函式）
scores |> rowwise() |> mutate(max_q = max(c_across(q1:q10))) |> ungroup()
```

`rowwise()` 只在沒有向量化版本時使用（`rowSums`、`pmax`、`pmin` 都是向量化的）。

## 列層級的集合運算

比較兩張表**整列**是否相同，不靠 key 配對；和 join 是不同問題。

| 函式 | 回傳 |
| --- | --- |
| `intersect(a, b)` | 兩表都有的列 |
| `union(a, b)` / `union_all(a, b)` | 合併去重 / 不去重 |
| `setdiff(a, b)` | 只在 a 的列 |
| `setequal(a, b)` | 忽略順序是否相同 |
| `symdiff(a, b)` | 只在其中一邊的列（dplyr ≥ 1.1.0） |

```r
setdiff(results_v1, results_v2)     # 重跑 pipeline 後哪些列變了
```

## 函式接受欄名：tidy evaluation

dplyr verbs 讀的是**裸欄名**（data masking），直接把參數丟進去會被當成變數找不到。

```r
# 1. {{ }}（curly-curly）：最常用，涵蓋大多數 wrapper
summarize_mean_by <- function(df, group_col, value_col) {
  df |>
    summarize(mean_value = mean({{ value_col }}, na.rm = TRUE), .by = {{ group_col }})
}
summarize_mean_by(gapminder, continent, lifeExp)

# 2. 動態輸出欄名：glue 語法 + :=
summarize_named_mean <- function(df, group_col, value_col) {
  df |>
    summarize("mean_{{ value_col }}" := mean({{ value_col }}, na.rm = TRUE),
              .by = {{ group_col }})
}                                                    # 產生 mean_lifeExp

# 3. 欄名是字串（來自設定檔、迴圈）：.data 代名詞
summarize_by_name <- function(df, group_name, value_name) {
  df |> summarize(mean_value = mean(.data[[value_name]]), .by = all_of(group_name))
}
purrr::map(c("lifeExp", "gdpPercap"), \(v) summarize_by_name(gapminder, "continent", v))

# 4. 多個欄位參數：用 ... 轉交
count_by <- function(df, ...) df |> count(...) |> mutate(prop = n / sum(n))
count_by(gapminder, continent, year)
```

| 情境 | 寫法 |
| --- | --- |
| 參數是裸欄名 | `{{ col }}` |
| 參數是字串 | `.data[[name]]`（data masking）/ `all_of(name)`（tidyselect） |
| 輸出欄名要依輸入變 | `"prefix_{{ col }}" :=` 或 `"{name}" :=` |
| 需要保存、檢查表達式 | `enquo(col)` + `!!col`；取名稱 `rlang::as_name(enquo(col))` |

### 包 ggplot2

```r
plot_hist <- function(df, x_var) {
  ggplot2::ggplot(df, ggplot2::aes(x = {{ x_var }})) +
    ggplot2::geom_histogram(bins = 30) +
    ggplot2::labs(x = rlang::as_label(rlang::enquo(x_var)))
}
plot_hist(gapminder, lifeExp)
```

## 常見錯誤

| 錯誤 | 症狀 | 對策 |
| --- | --- | --- |
| 函式內 `group_by(group_col)` | `object 'continent' not found` 或 `Column not found` | `{{ group_col }}` |
| `select(cols)`，`cols` 是字串向量 | 有同名欄時選錯；或 deprecation warning | `select(all_of(cols))` |
| 外部變數與欄名同名 | `filter(df, n > n)` 意義不明 | 欄用 `.data$n`、外部變數用 `.env$n` |
| 一欄一欄重複寫 `mutate()` | 程式冗長、漏改 | `across()` |
| 用 `rowwise()` 解可向量化的問題 | 慢 | `rowSums(pick(...))`、`pmax()` |
