# Data Reshaping with tidyr

很多資料問題不是算不出統計量，而是資料形狀不適合下游工作。`tidyr` 的核心價值，就是把「欄位裡塞了變數名稱」、「多個值擠在一格」、「list-column 還沒展開」這些問題整理成可供 `dplyr`、`ggplot2`、建模函式直接使用的表格。

## Tidy Data as a Goal

整理資料前，先確認你要逼近的目標形狀：

- each row: one observation
- each column: one variable
- each cell: one value

Key point: tidy data 不是美觀偏好，而是讓 filter、group、join、plot 與 model 可以用一致方式工作的前提。

## Wide vs Long

最常見的 reshape 問題，是資料原本是 wide format，但分析其實比較適合 long format。

例如把年份放在欄名裡：

```r
nuke_df
# country | 1945 | 1946 | 1948 | ...
```

通常會先轉成：

```r
nuke_long <- nuke_df %>%
  pivot_longer(
    -country,
    names_to = "year",
    values_to = "n_bombs"
  )
```

轉完之後，每列才真正代表一個 `country-year` observation。

## `pivot_longer()`

`pivot_longer()` 適合處理：

- 變數名稱被塞進欄名
- 問卷或時間序列被攤成很多平行欄位
- 同型欄位需要先疊成一欄才能 group / summarize / visualize

最常見的參數是：

```r
df %>%
  pivot_longer(
    cols = -id,
    names_to = "feature",
    values_to = "value"
  )
```

心法是：

- `cols`: 哪些欄要被收起來
- `names_to`: 原本欄名要去哪一欄
- `values_to`: 原本欄值要去哪一欄

如果你後面要做 `group_by(feature)`、畫 faceted plot，long format 幾乎都比較自然。

## `pivot_wider()`

有些情況則相反。當資料已經是 key-value 形式，但你需要把類別展開成欄位給報表、比較表或某些模型輸入時，就用 `pivot_wider()`。

```r
metrics %>%
  pivot_wider(
    names_from = metric,
    values_from = value
  )
```

常見場景：

- 把 long summary 轉回 spreadsheet-style 報表
- 把 metric 名稱展開成多欄
- 為後續寬表輸出做準備

Warning: `pivot_wider()` 前先確認 key 組合是否唯一。否則你以為是在 reshape，實際上是在面對重複值聚合問題。

## When Long Format Is Better

多數分析工作其實偏好 long format，因為它比較容易：

- `group_by()` / `summarize()`
- `ggplot(aes(...))`
- 做 facet 或顏色映射
- 套用同一套清理邏輯到多個題目或時間點

如果你發現自己在寬表上反覆寫很多近似欄名，例如 `score_q1`, `score_q2`, `score_q3` 分開處理，通常代表該先 `pivot_longer()`。

## Splitting Values Across Columns

有些問題不是 wide vs long，而是一格裡面混了多個值。這時可以用 `separate()`：

```r
df %>%
  separate(code, into = c("region", "id"), sep = "-")
```

適合用在：

- `"US-001"` 這種複合 ID
- 日期或代碼欄裡混有多個結構化片段
- 一個欄位其實藏了兩個變數

Key point: `separate()` 的目標是把一格裡的多個變數拆開，而不是做一般字串清理。

## Splitting Values Across Rows

如果單一儲存格裡面是多個同類值，而不是多個不同變數，通常該用 `separate_rows()`。

```r
df %>%
  separate_rows(tags, sep = ",")
```

這適合：

- tag lists
- 多選題答案
- 一列中用分隔符串起來的多個成員

`separate()` 是拆成多欄；`separate_rows()` 是拆成多列。兩者解決的不是同一種問題。

## Creating Missing Combinations

有時你不是想 reshape 現有資料，而是想把「理論上應該存在的組合」先建出來，再去補資料或找缺漏。這時 `expand_grid()` 很有用：

```r
full_df <- expand_grid(
  year = 1945:1954,
  country = c("Russian Federation", "United Kingdom", "United States")
)
```

這個做法常用於：

- 建立完整 panel / time grid
- 檢查哪些組合缺資料
- 在 join 前先明確定義 universe

如果你想保留某些欄位之間原本成對出現的關係，再和其他欄位做展開，可以搭配 `nesting()`。

## Rectangling Nested Data

當資料來自 JSON、API 或 list-column 時，問題已經不只是 reshape，而是 rectangling: 把 nested structure 展開成可分析的長方形表格。

常見函式包括：

- `unnest_wider()`: 把 list 元素展成多欄
- `unnest_longer()`: 把 list 元素展成多列
- `hoist()`: 從深層 list 中抽指定欄位

例如：

```r
characters %>%
  unnest_wider(character) %>%
  unnest_longer(films)
```

直覺上：

- 如果 list 裡是一組屬性，常用 `unnest_wider()`
- 如果 list 裡是一串 repeated items，常用 `unnest_longer()`

## Rectangular vs Non-Rectangular Data

CSV、spreadsheet 這類 tabular data 一開始就比較接近 tidy workflow。JSON、XML 或 API 回傳則常把資訊包成巢狀結構：

- one field contains a list
- one row contains a nested object
- important values buried several levels deep

這種資料的第一步通常不是畫圖或建模，而是先決定：

- 什麼才是一列 observation
- 哪些巢狀欄位要展寬
- 哪些重複項目要展長

## Practical Workflow

1. 先定義 observation unit，不要一上來就選函式。
2. 看看問題屬於哪一種：wide/long、cell 裡混多值、或 nested/list-column。
3. 先 reshape 成 tidy structure，再做摘要與視覺化。
4. reshape 後立即檢查 row count、key uniqueness 與缺值變化。
5. 如果資料來自 API 或 JSON，先做 rectangling，再考慮 joins 與 modeling。

## Common Mistakes

- 還沒想清楚 observation unit 就急著 `pivot_longer()`。
- `pivot_wider()` 前沒檢查 key 是否唯一。
- 把 `separate()` 和 `separate_rows()` 混用。
- reshape 後沒有檢查列數與缺值，導致下游摘要靜悄悄失真。
- 面對 nested data 仍硬把 list-column 當普通文字欄位處理。
