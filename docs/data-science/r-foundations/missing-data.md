# Missing Data in R

在 R 裡處理缺值，不只是把 `NA` 刪掉或補掉而已。更實際的工作流通常是：

1. 先確認哪些值其實是缺值
2. 再量化缺值分布
3. 視覺化缺值模式
4. 最後才決定刪除、標記、或 impute

這篇筆記偏重 R 裡的操作習慣與 `naniar` 風格 workflow，而不是單純的 missingness 理論分類。

## Missing Data Is Normal

真實資料裡幾乎一定會有缺值。

重要的不是假設資料乾淨，而是盡早回答幾個問題：

- 缺值是真的 `NA` 嗎？
- 還是其實被寫成 `"N/A"`、`"missing"`、`-99` 這種代碼？
- 缺值集中在哪些欄位？
- 缺值是否有明顯模式？

## First Principle: Missing Data Can Be Hidden

理想情況下，缺值會被明確編成 `NA`。

但常見現實是：

- `"missing"`
- `"Not Available"`
- `"N/A"`
- `"na"`
- `-99`
- `-98`

如果直接假設資料裡所有缺值都已經是 `NA`，很容易低估缺失比例。

## Start with Counts and Summaries

在 R 裡，最先做的通常不是補值，而是摘要。

`naniar` 常用函式包括：

```r
miss_var_summary(airquality)
miss_case_summary(airquality)
miss_var_table(airquality)
miss_case_table(airquality)
```

它們回答的問題分別像是：

- 哪些欄位缺最多？
- 哪些列缺最多？
- 缺值數量的分布長什麼樣？

## Looking Across Time or Runs

如果資料有順序或時間結構，單一總表不一定夠。

像這種函式能幫你看 span 或 run：

```r
miss_var_span(pedestrian, var = hourly_counts, span_every = 4000)
miss_var_run(pedestrian, hourly_counts)
```

這類工具適合回答：

- 缺值是否集中在某些時間段？
- 是零星缺值，還是一整段連續缺？

## Visualizing Missingness

純文字摘要很重要，但圖形往往更快看出模式。

常見視覺化：

```r
vis_miss(airquality)
vis_miss(airquality, cluster = TRUE)
gg_miss_var(airquality)
gg_miss_case(airquality)
gg_miss_upset(airquality)
gg_miss_fct(x = airquality, fct = Month)
gg_miss_span(pedestrian, hourly_counts, span_every = 3000)
```

這些圖通常在做三件事：

- 看缺值多寡
- 看缺值組合是否一起出現
- 看缺值是否跟某個 grouping variable 有關

## Replace Hidden Labels with Real `NA`

當資料把缺值藏在字串或 sentinel value 裡時，第一步通常是正規化。

```r
replace_with_na(data, replace = list(
  grade = c("N/A", "N/a")
))
```

更一般的做法是把常見假缺值一次轉掉：

```r
replace_with_na_all(condition = ~ .x %in% c("N/A", "missing", "na"))
replace_with_na_all(condition = ~ .x == -99)
```

## Scoped Replacement Helpers

`replace_with_na()` 很實用，但手動指定每一欄很快會變得冗長。

因此有幾個 scoped variants：

- `replace_with_na_all()`
- `replace_with_na_at()`
- `replace_with_na_if()`

這些特別適合：

- 某批欄位共享同一種錯誤編碼
- 只有 numeric 欄位才會用 `-99`
- 只有 character 欄位才會出現 `"missing"`

## Missingness Mechanisms Still Matter

雖然這篇偏 R 操作，但背後的 missingness 假設仍然重要：

- `MCAR`
- `MAR`
- `MNAR`

如果你要的是概念版整理，可以搭配：

- [Missing Data Mechanisms](/home/johnny_fan/project/notebook/docs/data-science/data-manipulation-and-eda/missing-data.md:1)

這裡的重點是：R 工具能幫你觀察模式，但不會自動替你判定 missingness 機制。

## Shadow Matrix

shadow matrix 的概念是：除了原始資料值之外，再建立一份與原資料同行同列的「缺值狀態表」。

它會記錄每個位置是：

- `!NA`
- `NA`

這讓你可以把「值」和「是否缺失」一起分析，而不是把缺值資訊藏在資料清理步驟裡。

## Nabular Data

`nabular` 可以理解成：

- original data
- 加上 shadow columns 的擴充版本

常見入口：

```r
bind_shadow(airquality)
nabular(airquality)
```

這很適合用來做：

- summary
- plotting
- model diagnostics

因為缺值狀態已經變成可以 join、group、facet 的資料欄位。

## Why Nabular Is Useful

一旦把缺值狀態顯式化，你就能問更好的問題：

- 缺值列的 `income` 是否特別高或特別低？
- 某個欄位缺值時，其他欄位分布有沒有改變？
- 某個 imputed 值在圖上能不能被單獨標出來？

這種做法比單純 `drop_na()` 更有資訊。

## Tracking Imputation

課程特別強調：imputation 不該只是把洞補平，還要讓你知道哪些值是補出來的。

這就是 `bind_shadow()` 和 `add_label_shadow()` 很有價值的地方。

```r
aq_imp <- airquality %>%
  bind_shadow() %>%
  add_label_shadow()
```

這樣後續畫圖或摘要時，可以把 imputed vs observed 區分開來。

## `impute_below()`

`impute_below()` 不是正式分析用的精確補值方法，而是很適合探索資料結構的視覺化技巧。

```r
impute_below(c(5, 6, 7, NA, 9, 10))
```

概念上，它會把缺值放到目前資料範圍的下方，讓圖形上能看到原本缺值落點。

這特別適合：

- scatter plot
- histogram
- density / distribution exploration

## Scoped `impute_below`

和 `replace_with_na` 類似，`impute_below` 也有 scoped variants：

- `impute_below_if(data, is.numeric)`
- `impute_below_at(data, vars(var1, var2))`
- `impute_below_all(data)`

這在只想針對 numeric 欄位做 exploratory imputation 時很好用。

## Long-Format Tracking

當你需要把 imputed 狀態帶進圖表，long format 常常更方便。

像 `shadow_long()` 這類工具可以把：

- 原值
- 對應欄位名稱
- 缺值標記

整理成比較適合 `ggplot2` 的長表格式。

## Practical Workflow

一個穩定的 R 缺值 workflow 通常長這樣：

1. 先找 hidden missing labels
2. 把它們統一轉成 `NA`
3. 用 summary 與 plots 看缺值規模和模式
4. 判斷缺值可能更接近 `MCAR`、`MAR` 或 `MNAR`
5. 視需求選擇 delete、indicator、exploratory imputation 或正式 imputation
6. 在需要補值時，盡量保留「哪些值被補過」的追蹤資訊

## Deletion vs Imputation

不是每次都該補值。

一些常見判斷：

- 缺值很少且近似隨機時，刪除可能就夠
- 缺值有結構時，直接刪除常會偏
- exploratory imputation 可以幫你看圖，但不等於正式建模方案

課程裡很重要的一個提醒是：

- bad imputation can lead to poor estimates and decisions

所以補值不是越早做越好，而是越晚越好，直到你真的知道為什麼要補。

## Common Traps

- 假設所有缺值都已經是 `NA`
- 把 `-99`、`"missing"`、`"na"` 當成正常值留下
- 一看到缺值就直接刪整列
- 用補值後的資料畫圖，卻忘了標出哪些點原本是缺的
- 把 exploratory imputation 當成正式分析結果
- 只看總缺值比例，不看缺值是否集中在特定變數、群組或時間段

## Related Notes

- [Functions in R](functions.md)
- [Defensive Programming in R](defensive-programming.md)
- [Missing Data Mechanisms](/home/johnny_fan/project/notebook/docs/data-science/data-manipulation-and-eda/missing-data.md:1)
