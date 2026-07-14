# dplyr Programming Patterns

當你開始不只寫一次性的 pipeline，而是想把同樣的資料整理邏輯重用在不同欄位、不同資料表或不同圖表上，問題就從「會不會用 dplyr」變成「能不能把 dplyr workflow 包成穩定的程式」。這篇整理幾個最常見的 `dplyr` programming pattern。

## From One-Off Pipelines to Reusable Code

一開始的 `dplyr` 通常像這樣：

```r
imf_data %>%
  select(iso, country, year, consumer_price_index) %>%
  filter(country == "Uruguay", year > 2010)
```

如果你接著還要對 Belize、Samoa、Taiwan 重複同一件事，就代表該把這段邏輯包成函數，而不是一直複製貼上。

```r
cpi_by_country <- function(country_name) {
  imf_data %>%
    select(iso, country, year, consumer_price_index) %>%
    filter(country == country_name, year > 2010)
}
```

Key point: dplyr programming 的核心不是炫技，而是把資料操作變成可重用、可檢查、可組合的單位。

## Column Selection Helpers

當欄位很多時，直接手打一長串欄名通常不穩。`tidyselect` helper 能讓選欄位更有彈性。

常見 helper：

- `starts_with()`
- `ends_with()`
- `contains()`
- `matches()`
- `everything()`
- `last_col()`

例如：

```r
world_bank_data %>%
  select(country, year, starts_with("perc"))

world_bank_data %>%
  select(country, year, ends_with("rate"))

world_bank_data %>%
  select(matches("^co"))
```

其中 `matches()` 最值得特別記，因為它吃 regular expression，能處理比較複雜的 pattern-based selection。

## Reordering Columns with `relocate()`

有時你不是要刪欄，而是把欄位移到更合理的位置。這時比起重寫整個 `select()`，`relocate()` 通常更清楚。

```r
world_bank_data %>%
  relocate(matches("^perc"), .after = year)

world_bank_data %>%
  relocate(matches("^perc"), .before = infant_mortality_rate)
```

這很適合：

- 把同一類指標排在一起
- 把 ID / metadata 欄位移到前面
- 調整輸出表格的閱讀順序

Key point: `relocate()` 改的是欄位順序，不改資料內容，適合拿來整理輸出可讀性。

## Transforming Many Columns with `across()`

當多個欄位要套用同樣轉換時，不要一欄一欄手寫 `mutate()`。`across()` 就是為這種情況設計的。

```r
world_bank_data %>%
  mutate(
    across(
      .cols = starts_with("perc"),
      .fns = ~ .x / 100
    )
  )
```

`across()` 常見用法：

- 在 `mutate()` 中做批次轉換
- 在 `summarize()` 中做批次摘要
- 配合 selection helper 指定欄位集合

例如批次摘要：

```r
world_bank_data %>%
  summarize(
    across(
      .cols = ends_with("rate"),
      .fns = mean,
      na.rm = TRUE
    )
  )
```

如果你發現自己在連續欄位上重複寫很多近似函式，通常就該先想 `across()`。

## Using `where()` to Select by Type

有時你想選的不是命名 pattern，而是欄位型別。

```r
df %>%
  count(across(.cols = !where(is.numeric)))
```

`where()` 很適合：

- 只對 numeric 欄位做標準化
- 只對 character 欄位做字串清理
- 將型別條件和 `across()` 搭配

這比硬寫欄名更穩，因為當 schema 變動時，型別條件往往比欄名清單更能持續成立。

## Row-Wise Work with `rowwise()` and `c_across()`

`dplyr` 預設偏向 column-wise thinking，但有些需求是「同一列的多欄一起算」。

```r
df %>%
  rowwise() %>%
  mutate(
    mean_rate = mean(c_across(infant_mortality_rate:last_col()), na.rm = TRUE)
  ) %>%
  ungroup()
```

這適合：

- 同一列多欄加總或平均
- 問卷多題組合同列分數
- 少量欄位的 row-wise aggregation

Warning: `rowwise()` 很方便，但通常比向量化 / column-wise 操作慢。只有在問題本質真的是 row-wise 時才用。

## Set Operations on Data Frames

有時你不是要按 key 合併，而是想直接比較「兩份資料有哪些整列相同或不同」。這時比 join 更自然的是 set operations。

常見函式：

- `intersect()`
- `union()`
- `setdiff()`
- `setequal()`

例如：

```r
intersect(uruguay_imf, uruguay_wb)
union(uruguay_imf_filtered, uruguay_wb_filtered)
setdiff(uruguay_imf_filtered, uruguay_wb_filtered)
setequal(union_one_way, union_other)
```

直覺上：

- `intersect()`: 共有的 rows
- `union()`: 合併後去重
- `setdiff()`: 只在第一份資料出現的 rows
- `setequal()`: 忽略順序後是否本質相同

Key point: set operations 比較的是整列內容，不是 join key 對應關係。這和 join 是不同問題。

## Basic Tidy Evaluation with `{{ }}`

當函數參數本身是欄位名稱時，普通字串參數不夠用，因為 `dplyr` verbs 常期待的是欄位表達式。

最簡單也最實用的寫法是 curly-curly：

```r
summarize_mean_by <- function(df, group_col, col_to_mean) {
  df %>%
    group_by({{ group_col }}) %>%
    summarize(mean_value = mean({{ col_to_mean }}, na.rm = TRUE))
}
```

這通常是現在最值得優先學會的 tidy-eval 入口，因為：

- 寫法短
- 可讀性高
- 大多數 wrapper function 都夠用

## `enquo()` and `!!`

如果你需要更明確地拿到欄位參數、轉存、重複使用或進一步組合，就會碰到 `enquo()` 和 `!!`。

```r
summarize_mean_by <- function(df, group_col, col_to_mean) {
  group_col <- enquo(group_col)
  col_to_mean <- enquo(col_to_mean)

  df %>%
    group_by(!!group_col) %>%
    summarize(mean_value = mean(!!col_to_mean, na.rm = TRUE))
}
```

可以把它們理解成：

- `enquo()`: 先把欄位表達式收起來
- `!!`: 再把它展開塞回 dplyr verb

很多時候 `{{ }}` 就夠了；只有在你真的要保存或操作 quosure 時，再往 `enquo()` / `!!` 走。

## Dynamic Output Names with `:=`

如果函數除了接收欄位，還要根據輸入欄位動態產生輸出欄名，就會用到 walrus operator `:=`。

```r
summarize_named_mean <- function(df, group_col, col_to_mean) {
  name_of_col_to_mean <- rlang::as_name(enquo(col_to_mean))
  new_col_name <- paste0("mean_", name_of_col_to_mean)

  df %>%
    group_by({{ group_col }}) %>%
    summarize(!!new_col_name := mean({{ col_to_mean }}, na.rm = TRUE))
}
```

這讓你可以在函數裡面安全地建立：

- `mean_sales`
- `mean_profit`
- `mean_consumer_price_index`

而不是每次都硬編一個固定欄名。

## Using `rlang` with ggplot2 Wrappers

tidy evaluation 不只出現在 `dplyr`。如果你想包 `ggplot2` 函數，也常會用到：

```r
plot_hist <- function(df, x_var) {
  ggplot2::ggplot(df, ggplot2::aes(x = {{ x_var }})) +
    ggplot2::geom_histogram() +
    ggplot2::labs(x = rlang::as_label(enquo(x_var)))
}
```

這個 pattern 很實用，因為它讓函數同時做到：

- 接受裸欄位名稱
- 正確映射到 `aes()`
- 自動把欄位名稱轉成圖上標籤

## Practical Workflow

1. 先判斷自己要解的是重複 pipeline、批次欄位操作，還是欄位參數化問題。
2. 若只是選欄規則化，先用 selection helpers。
3. 若同樣轉換套很多欄，先想 `across()`。
4. 若要包函數且參數是欄位，先從 `{{ }}` 開始。
5. 只有在需要保存 / 操作欄位表達式時，再升級到 `enquo()`、`!!` 與 `:=`。

## Common Mistakes

- 還在重複貼相同 pipeline，卻沒有抽成函數。
- 對很多欄做同樣轉換時仍一欄一欄手寫。
- 把 set operations 和 joins 混成同一種問題。
- 一開始就跳進複雜 tidy evaluation，而不是先用 `{{ }}`。
- 用 `rowwise()` 解本來可以向量化的問題，讓程式變慢又更難維護。
