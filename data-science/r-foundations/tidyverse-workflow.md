[Data Science](../README.md) › [R Foundations](README.md) › Tidyverse 工作流

# Tidyverse 工作流 (Tidyverse Workflow)

tidyverse 的價值不在於單一函式，而在於**每個 verb 都吃 data frame、吐 data frame**，所以讀檔 → 清理 → 摘要 → 畫圖能用 pipe 一路串起來。Python 的對應是 pandas method chaining，見 [pandas](../python-foundations/pandas/README.md)。

## Tidy data

| 原則 | 意思 | 反例 |
| --- | --- | --- |
| 每欄一個變數 | `sample`、`gene`、`count` 各一欄 | 每個樣本一欄（寬表） |
| 每列一個觀測 | 一列 = 一個樣本 × 一個基因 | 一列塞多個時間點 |
| 每格一個值 | `"TP53"` | `"TP53;BRCA1"` |

> 表現量矩陣（基因 × 樣本）是寬表，適合矩陣運算與 Bioconductor；要用 dplyr / ggplot2 分組畫圖時先 `pivot_longer()`。見 [tidyr 資料重塑](data-reshaping-with-tidyr.md)。

| 套件 | 負責 |
| --- | --- |
| `readr` / `readxl` | 讀檔，見 [匯入資料](importing-data.md) |
| `dplyr` | 列 / 欄操作、分組摘要、join |
| `tidyr` | 寬長轉換、拆欄、補缺值 |
| `stringr` / `forcats` / `lubridate` | 字串 / 類別 / 日期 |
| `purrr` | 對 list 迭代 |
| `ggplot2` | 圖 |

## Pipe：`|>` vs `%>%`

```r
library(tidyverse)

gapminder |> filter(year == 2007) |> arrange(desc(lifeExp))
```

| | `\|>`（base R ≥ 4.1.0） | `%>%`（magrittr） |
| --- | --- | --- |
| 需要套件 | 否 | 是（tidyverse 會載入） |
| 佔位符 | `_`，需具名參數：`lm(y ~ x, data = _)`（R ≥ 4.2.0） | `.`，可放任何位置 |
| 速度 | 語法轉換，零成本 | 函式呼叫，有些微開銷 |

新程式建議用 `|>`。中間結果會被重用就先存成有名字的物件，不要把 pipeline 拉到 20 行。

## 核心 verbs

| 想做 | dplyr | pandas 對應 |
| --- | --- | --- |
| 篩列 | `filter(year == 2007, pop > 1e7)` | `df.query(...)` / boolean mask |
| 選欄 | `select(country, starts_with("gdp"))` | `df[[...]]`、`df.filter(like=)` |
| 新增 / 改欄 | `mutate(gdp = gdpPercap * pop)` | `df.assign(...)` |
| 排序 | `arrange(desc(lifeExp))` | `sort_values(ascending=False)` |
| 改欄名 | `rename(life = lifeExp)` | `rename(columns=)` |
| 取不重複 | `distinct(country, continent)` | `drop_duplicates()` |
| 取前 n | `slice_max(lifeExp, n = 5)` | `nlargest(5, ...)` |
| 分組摘要 | `group_by(continent) \|> summarize(...)` | `groupby().agg()` |
| 計數 | `count(continent, sort = TRUE)` | `value_counts()` |
| 多欄套同函式 | `across(where(is.numeric), mean)` | `df.select_dtypes().mean()` |

```r
gapminder |>
  filter(year == 2007) |>
  mutate(gdp_billion = gdpPercap * pop / 1e9) |>
  summarize(
    n          = n(),
    mean_life  = mean(lifeExp),
    total_gdp  = sum(gdp_billion),
    .by = continent                                    # dplyr ≥ 1.1.0：單次分組，不留 group 狀態
  )

# 舊寫法：group_by() 後記得解除分組
gapminder |>
  group_by(continent, year) |>
  summarize(mean_life = mean(lifeExp), .groups = "drop")

# 多欄套同一組函式
gapminder |>
  summarize(across(c(lifeExp, gdpPercap), list(mean = mean, sd = sd)), .by = continent)

# 分組後 mutate：組內標準化
gapminder |> mutate(life_z = (lifeExp - mean(lifeExp)) / sd(lifeExp), .by = year)
```

> `group_by()` 的分組狀態會跟著物件走，後面的 `mutate()` / `slice()` 仍會分組執行。用 `.by` 或 `.groups = "drop"` / `ungroup()` 避免意外。

## 接到 ggplot2

先把資料整理成「圖要的形狀」，再畫圖；圖很亂時通常是資料沒先 filter / summarize。

```r
gapminder |>
  filter(year == 2007) |>
  ggplot(aes(x = gdpPercap, y = lifeExp, color = continent, size = pop)) +
  geom_point(alpha = 0.7) +
  scale_x_log10() +
  labs(x = "GDP per capita (log)", y = "Life expectancy")

gapminder |>
  filter(country %in% c("Taiwan", "Japan")) |>
  ggplot(aes(year, lifeExp, color = country)) +
  geom_line()
```

| 問題 | geom | 資料形狀 |
| --- | --- | --- |
| 兩連續變數關係 | `geom_point()` | 原始列 |
| 隨時間 / 有序 x 的趨勢 | `geom_line()` | 每組每時間一列 |
| 單變數分布 | `geom_histogram()` / `geom_density()` | 原始列 |
| 組間分布比較 | `geom_boxplot()` / `geom_violin()` | 原始列（long） |
| 類別計數 | `geom_bar()`（自己數）/ `geom_col()`（已摘要） | 原始 / 摘要後 |

圖表選擇原則見 [圖表設計原則](../data-manipulation-and-eda/visualization/chart-design-principles.md)。

## 一切皆物件（給 SAS / SPSS 使用者）

SAS 用 `DATA step` + `PROC` 產生報表；R 是在有狀態的 session 裡建立、轉換、重用物件。`summary()` 輸出、模型結果都是物件，「輸出」就是下一步的輸入。

```r
fit <- lm(lifeExp ~ log(gdpPercap) + continent, data = gapminder)
coef(fit); residuals(fit)            # 模型是物件，不是報表
broom::tidy(fit)                     # 係數表變 tibble，可再接 dplyr / ggplot2
broom::glance(fit)                   # 一列模型層級統計（R²、AIC）
```

| SAS 習慣 | R 對應 |
| --- | --- |
| `BY` 分組 | `summarize(.by = )` / `group_by()` |
| `PROC MEANS` / `PROC FREQ` | `summarize()`、`count()` |
| `PROC REG` 報表 | `lm()` 物件 + `summary()` / `broom::tidy()` |
| `PROC SORT` + `MERGE` | `left_join()`，見 [dplyr 合併資料](joining-data-with-dplyr.md) |
| 看 log | `str()`、`glimpse()`、`class()` |

> session 有狀態：物件是否存在取決於執行順序。交付前要「Restart R → 從頭跑一次」，或用 [R Markdown / Quarto](reporting-with-r-markdown.md) 強制從乾淨環境執行。
