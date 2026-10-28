[Data Science](../README.md) › [R Foundations](README.md) › tidyr 資料重塑

# tidyr 資料重塑 (Data Reshaping with tidyr)

很多問題不是算不出來，而是資料形狀不對：變數名藏在欄名裡、一格塞多個值、API 回應是巢狀 list。`tidyr` 把這些整理成 tidy 表（每列一觀測、每欄一變數、每格一值，見 [Tidyverse 工作流](tidyverse-workflow.md#tidy-data)）。pandas 對照見 [reshape 與 merge](../python-foundations/pandas/reshape-merge.md)。

| 問題 | 函式 | pandas |
| --- | --- | --- |
| 寬 → 長（欄名裡是變數值） | `pivot_longer()` | `melt()` |
| 長 → 寬 | `pivot_wider()` | `pivot()` / `pivot_table()` |
| 一格多個變數 → 多欄 | `separate_wider_delim()` / `_regex()` | `str.split(expand=True)` |
| 一格多個同類值 → 多列 | `separate_longer_delim()` | `str.split().explode()` |
| 多欄 → 一欄 | `unite()` | 字串相加 |
| 補出缺少的組合 | `complete()`、`expand_grid()` | `reindex(MultiIndex.from_product())` |
| 補值 | `fill()`、`replace_na()`、`drop_na()` | `ffill()`、`fillna()`、`dropna()` |
| 巢狀 list 展開 | `unnest_wider()`、`unnest_longer()`、`hoist()` | `pd.json_normalize()`、`explode()` |

## 寬 ↔ 長

```r
library(tidyverse)

# 表現量矩陣（基因 × 樣本）→ long，才能接 ggplot / group_by
expr_long <- expr_wide |>
  pivot_longer(cols = -gene_id, names_to = "sample_id", values_to = "count")

# 欄名同時帶兩個變數：time_rep → time、rep
df |>
  pivot_longer(cols = starts_with("t"),
               names_to = c("time", "rep"), names_sep = "_",
               names_transform = list(time = parse_number),   # "t24" → 24
               values_to = "signal")

# 年份在欄名：轉成數值
nuke_df |>
  pivot_longer(-country, names_to = "year", values_to = "n_bombs",
               names_transform = as.integer, values_drop_na = TRUE)

# long → wide：每個 metric 一欄
metrics |> pivot_wider(names_from = metric, values_from = value)
expr_long |> pivot_wider(names_from = sample_id, values_from = count, values_fill = 0)
```

> `pivot_wider()` 前確認 `id + names_from` 組合唯一。否則會得到 list-column 與 warning（`Values are not uniquely identified`），代表有重複列，或需要 `values_fn = mean` 明確聚合。

| 什麼時候用 long | 什麼時候用 wide |
| --- | --- |
| `group_by()` / `summarize()`、ggplot facet、mixed model | 矩陣運算、PCA、相關矩陣、報表、DESeq2 輸入 |

## 拆欄與合欄

tidyr ≥ 1.3.0 用 `separate_wider_*()` / `separate_longer_*()` 取代 `separate()` / `separate_rows()`（舊函式仍可用，但已 superseded）。

```r
# 一格多個變數 → 多欄："TCGA-A1-0001" → project、site、patient
samples |>
  separate_wider_delim(barcode, delim = "-", names = c("project", "site", "patient"),
                       too_many = "drop")             # 多出的片段丟掉；too_few = "align_start"

# 用 regex 擷取
samples |>
  separate_wider_regex(sample, patterns = c(tissue = "[A-Za-z]+", "_", rep = "\\d+"))

# 一格多個同類值 → 多列："GO:0001;GO:0002" → 兩列
gene_go |> separate_longer_delim(go_terms, delim = ";")

# 多欄 → 一欄
df |> unite("sample_id", donor, tissue, sep = "_", remove = FALSE)
```

## 補齊組合與缺值

```r
# 每個樣本 × 每個基因都應該有一列；沒出現的補 0
counts_long |> complete(sample_id, gene_id, fill = list(count = 0))

# 建立完整格子（panel、時間序列）
grid <- expand_grid(year = 1945:1954, country = c("Russia", "UK", "US"))
grid |> anti_join(nuke_long, by = join_by(year, country))   # 哪些組合缺資料？

# 試算表常見的「合併儲存格」：往下補
sheet |> fill(patient_id, .direction = "down")

df |> replace_na(list(count = 0, note = "")); df |> drop_na(age)
```

> 「沒有資料」和「值為 0」意義不同：未偵測到的基因補 0 合理；未測量的樣本補 0 會扭曲結果。補值前先確認缺失的原因，見 [缺失值](missing-data.md)。

## 巢狀資料展開 (rectangling)

JSON / API 回應讀進來常是 list-column。先決定「一列代表什麼」，再展開。

```r
# list 元素是一組屬性 → 多欄；是重複項目 → 多列
characters |>
  unnest_wider(character) |>              # name、height、films 各成一欄
  unnest_longer(films)                    # 每部電影一列

# 只從深層抓幾個欄位
repos |> hoist(repo, owner = c("owner", "login"), stars = "stargazers_count")

# 分組後 nest，每組一個 data frame，配 purrr::map 跑模型
gapminder |>
  nest(.by = country) |>
  mutate(fit = map(data, \(d) lm(lifeExp ~ year, data = d)),
         slope = map_dbl(fit, \(m) coef(m)[["year"]]))
```

讀 JSON 本身見 [匯入資料](importing-data.md#json)；`map()` 見 [函數式程式設計](functional-programming.md)。

## 重塑後的檢查

| 檢查 | 寫法 |
| --- | --- |
| 列數符合預期 | long：`nrow(wide) * n_value_cols`；`stopifnot(nrow(long) == ...)` |
| key 唯一 | `count(long, sample_id, gene_id) \|> filter(n > 1)` |
| 新增的 NA | `sum(is.na(long$value))` 比較重塑前後 |
| 型別 | `glimpse()`：從欄名轉出來的值預設是 character |
