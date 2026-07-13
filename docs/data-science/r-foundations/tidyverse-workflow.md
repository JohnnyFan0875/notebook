# Tidyverse Workflow in R

`tidyverse` 的價值不只是「一包很多函式」，而是它把資料整理、摘要與視覺化串成一條一致的工作流。當資料已經接近 tidy format 時，你可以先用 `dplyr` 篩選與彙整，再把結果直接送進 `ggplot2`。

## The Core Mental Model

先把資料想成：

- rows: observations
- columns: variables
- each verb: 對資料表做一個明確轉換

最常見的 tidyverse 分析節奏是：

1. 讀入或準備資料
2. 用 `filter()` / `select()` / `mutate()` 整理欄位
3. 用 `group_by()` / `summarize()` 做摘要
4. 用 `ggplot2` 把結果視覺化

Key point: tidyverse 的強項不是單一函式，而是每一步都維持相容的表格結構。

## Tibbles and Pipes

tidyverse 裡最常見的表格物件是 tibble。它和 base R 的 data frame 很像，但輸出更適合互動分析，也較少自動把字串偷偷轉型。

`%>%` 代表把前一步的結果接到下一個函式：

```r
library(dplyr)

gapminder_2007 <- gapminder %>%
  filter(year == 2007)
```

這樣寫的好處是流程是由上到下展開的，你比較容易看出每一步對資料形狀做了什麼。

如果某個中間結果後面還會重用，先指派給一個清楚命名的物件通常比把整條 pipeline 拉得很長更好。

## Extracting Rows with `filter()`

`filter()` 用來保留符合條件的列。

```r
gapminder %>%
  filter(country == "United States", year == 2007)
```

常見用法包括：

- 篩某一年或某個區間
- 篩單一國家、群組或類別
- 把後續視覺化限制在一個子集合

這一步很重要，因為很多圖表不是畫不出來，而是畫了不該混在一起的資料。

## Common Transformation Verbs

除了 `filter()`，最常一起出現的還有幾個基本 verb：

```r
gapminder %>%
  select(country, continent, year, lifeExp)

gapminder %>%
  arrange(desc(lifeExp))

gapminder %>%
  mutate(gdp_billions = gdpPercap * pop / 1e9)
```

- `select()`: 挑欄位，讓後續工作聚焦
- `arrange()`: 排序，方便檢查極端值或排名
- `mutate()`: 新增或改寫欄位

Key point: `mutate()` 通常是在建立下游分析需要的新變數，而不是為了把所有可能的欄位都先算一遍。

## Grouping and `summarize()`

當你不再關心每一列，而是想看群組層級的整體特徵時，就該用 `summarize()`。

```r
gapminder %>%
  summarize(meanLifeExp = mean(lifeExp))
```

這會把很多列壓縮成一個摘要結果。更常見的情況是先分組再摘要：

```r
gapminder %>%
  group_by(continent, year) %>%
  summarize(
    mean_lifeExp = mean(lifeExp),
    mean_gdpPercap = mean(gdpPercap),
    .groups = "drop"
  )
```

如果你需要的是各群出現次數，`count()` 通常比手寫 `group_by(...) %>% summarize(n = n())` 更直接：

```r
gapminder %>%
  count(continent, sort = TRUE)
```

## Data Transformation and Visualization

很多 tidyverse workflow 真正有效的地方，在於你可以先整理資料，再直接把整理後的表送進 `ggplot2`。

```r
gapminder %>%
  filter(year == 2007) %>%
  ggplot(aes(x = gdpPercap, y = lifeExp)) +
  geom_point()
```

這個模式的意思是：

- `dplyr` 負責把資料變成你真正想看的子集合
- `ggplot2` 負責把那個子集合映成視覺元素

如果圖很亂，先回頭檢查資料轉換是否正確，通常比一開始就在圖層上硬調更有效。

## Aesthetics in `ggplot2`

`aes()` 會把資料欄位對應到視覺通道：

```r
gapminder_2007 %>%
  ggplot(
    aes(
      x = gdpPercap,
      y = lifeExp,
      color = continent,
      size = pop
    )
  ) +
  geom_point()
```

常見對應包括：

- `x`, `y`: 座標位置
- `color`: 群組或數值差異
- `size`: 規模大小

Key point: 美學映射應該幫助比較，而不是把每個欄位都塞進圖裡。

## Choosing Plot Types

同一份 tidy data 可以用不同圖表回答不同問題。

### Scatter Plots

```r
ggplot(gapminder_2007, aes(gdpPercap, lifeExp)) +
  geom_point()
```

適合看：

- 兩個連續變數之間的關係
- 群組分布與離群值

### Line Plots

```r
gapminder %>%
  filter(country %in% c("Taiwan", "Japan")) %>%
  ggplot(aes(year, lifeExp, color = country)) +
  geom_line()
```

適合看：

- 隨時間變化的趨勢
- 同一個個體或群組 across ordered x-axis 的變化

Scatter plot 與 line plot 的差別不只是幾何形狀，而是資料是否帶有自然順序。當 x 軸是時間、階段或其他有順序的索引時，`geom_line()` 才比較有意義。

### Other Common Choices

- histogram: 單一連續變數的分布
- bar plot: 類別計數或已彙總數值
- box plot: 群組間分布比較

不要把 plot type 當模板背下來。先問自己：

- 我想比較 relationship、distribution，還是 trend？
- 我的 x 軸是 category、continuous，還是 time？
- 資料是原始列，還是已經 summary 過？

## A Small End-to-End Example

```r
library(dplyr)
library(ggplot2)

summary_2007 <- gapminder %>%
  filter(year == 2007) %>%
  group_by(continent) %>%
  summarize(
    mean_lifeExp = mean(lifeExp),
    mean_gdpPercap = mean(gdpPercap),
    .groups = "drop"
  )

ggplot(summary_2007, aes(mean_gdpPercap, mean_lifeExp, color = continent)) +
  geom_point(size = 3)
```

這個流程展示的不是特定函式技巧，而是 tidyverse 最重要的習慣：

1. 先決定分析單位
2. 再把資料整理成對應形狀
3. 最後才選圖

## Practical Habits

- 圖畫不清楚時，先檢查資料是否該先 `filter()` 或 `summarize()`。
- 會重用的中間結果先命名，例如 `gapminder_2007`。
- 一張圖盡量只承載一個主要問題，不要把所有欄位都映射進 `aes()`。
- `group_by()` 之後要留意輸出是否仍保持分組狀態；必要時明確加上 `.groups = "drop"`。
- 如果你已經在做大量 joins、reshape 或 grouped summaries，代表你真正需要的是 workflow clarity，不只是多記幾個函式名。
