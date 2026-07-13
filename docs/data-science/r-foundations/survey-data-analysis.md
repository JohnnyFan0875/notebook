# Survey Data Analysis in R

survey data 和一般表格資料最大的差別，不是多了一欄 `weight` 而已，而是樣本本身來自特定抽樣設計。只把 survey data 當普通 data frame 做平均、比例與圖表，常會得到偏掉的 population story。

## Why Survey Weights Exist

survey weight 大致可以理解成：

- 一筆樣本在母體中代表多少個單位
- 抽樣設計與非等機率抽樣留下來的校正資訊

例如某筆 household 的 weight 若是 `25,985`，直覺上表示這筆樣本代表母體中的很多戶，不應和 weight 很小的樣本被等量對待。

Key point: survey weights 不是可有可無的修飾欄位，而是讓 sample estimate 更接近 population estimate 的核心資訊。

## Start With a Survey Design Object

在 R 裡，分析 survey data 最常見的入口是 `survey` 套件。重點不是直接對原始表做 `summarize()`，而是先建立 design object。

課程裡後續所有 weighted 統計都以 `NHANES_design` 為中心，代表：

- 權重資訊已掛進去
- 抽樣設計的變異估計方式也一起被保留

實務上思路要先固定成：

1. 原始資料表
2. survey design object
3. `svy*` 系列函式

而不是：

1. 原始資料表
2. 普通 `mean()` / `table()`
3. 最後才想起來 weights

## Unweighted and Weighted Can Tell Different Stories

以 NHANES race 分布為例，未加權時可以這樣做：

```r
tab_unw <- NHANESraw %>%
  group_by(Race1) %>%
  summarize(Freq = n()) %>%
  mutate(Prop = Freq / sum(Freq)) %>%
  arrange(desc(Prop))
```

但 survey 資料更重要的是 weighted version：

```r
tab_w <- svytable(~Race1, design = NHANES_design)
```

然後再轉成比例與資料框來畫圖。

Key point: unweighted distribution 描述的是 sample composition；weighted distribution 才更接近你想講的 population composition。

## Weighted Categorical Summaries

類別變數常見的 survey 工作包括：

- weighted one-way table
- weighted two-way table
- 比例長條圖
- survey-adjusted 卡方檢定

例如 race 和 diabetes 的關係：

```r
svytable(~Race1 + Diabetes, design = NHANES_design)
svychisq(~Race1 + Diabetes, design = NHANES_design)
```

這裡值得記住兩件事：

- `svytable()` 幫你做的是 survey-aware 的加權列聯表
- `svychisq()` 不是把普通 `chisq.test()` 套上 weights，而是使用 survey design 下適合的檢定

如果只是想比較組成比例，常會再配合：

```r
ggplot(tab_w, aes(x = Race1, fill = Diabetes, y = Freq)) +
  geom_col(position = "fill")
```

`position = "fill"` 讓你看條件比例，比較適合比較各族群內的疾病比例結構。

## Weighted Quantitative Summaries

對連續或計數型變數，survey 套件最常用的是：

```r
svymean(~DaysPhysHlthBad, design = NHANES_design, na.rm = TRUE)
svytotal(~DaysPhysHlthBad, design = NHANES_design, na.rm = TRUE)
svyquantile(~DaysPhysHlthBad, design = NHANES_design, na.rm = TRUE, quantiles = 0.5)
```

這幾個函式很有代表性：

- `svymean()`：population mean 的估計
- `svytotal()`：population total 的估計
- `svyquantile()`：weighted median 或其他分位數

輸出裡常會同時看到 estimate 與 `SE`。這提醒我們 survey analysis 不只在估計平均值，也在估計設計下的不確定性。

## Standard Errors Matter

survey data 的另一個核心觀念是：即使 estimate 看起來簡單，標準誤也不能直接沿用 iid sample 的公式。

當你看到：

- `mean`
- `total`
- `SE`

要把它理解成：

- 這不是單純把 weights 乘上去而已
- 抽樣設計會影響變異估計

如果只做 weighted average 卻忽略 `SE`、confidence interval 或設計效果，就只完成了一半分析。

## Visualizing Weighted Categorical Data

課程用 NHANES race 示範了一個實用流程：

1. 先把 weighted table 整成資料框
2. 算出比例
3. 依比例排序
4. 再用 `ggplot2` 畫圖

例如：

```r
ggplot(tab_w, aes(x = Race1, y = Prop)) +
  geom_col() +
  coord_flip()
```

這裡的重點不是 `geom_col()` 本身，而是圖上的 bar height 應該反映 weighted proportion，而不是 raw count。

## Scatterplots Need Extra Care

連續變數的散點圖也是一樣。課程先用嬰兒月齡與頭圍示範普通散點圖：

```r
babies <- filter(NHANESraw, AgeMonths <= 6) %>%
  select(AgeMonths, HeadCirc)

ggplot(babies, aes(x = AgeMonths, y = HeadCirc)) +
  geom_point()
```

但因為 `AgeMonths` 是離散整數，點會重疊，所以後續改用：

```r
ggplot(babies, aes(x = AgeMonths, y = HeadCirc)) +
  geom_jitter(width = 0.3, height = 0, alpha = 0.3)
```

這是 survey data 裡很實用的視覺化細節：在離散 x 軸上，`jitter` 比單純散點圖更能看出密度。

## Weighted Smoothers in Plots

課程後面進一步把權重帶進平滑線：

```r
ggplot(babies, aes(x = AgeMonths, y = HeadCirc, alpha = WTMEC4YR)) +
  geom_jitter(width = 0.3, height = 0) +
  guides(alpha = "none") +
  geom_smooth(method = "lm", se = FALSE, mapping = aes(weight = WTMEC4YR))
```

這個例子很值得記住，因為它說明兩件事：

- 點可以保留原始觀測值視角
- 趨勢線可以用 weight 反映母體代表性

不過也要小心：把 weight 映到 `alpha` 或其他美學屬性時，視覺效果不一定直觀，容易誤導。通常比較安全的是讓模型或摘要層吃 weights，而不是每個 aesthetic 都直接映射。

## A Practical Survey Workflow

如果拿到 NHANES、BLS 或其他大型 survey data，可以用這個順序工作：

1. 先確認權重欄位代表什麼母體與哪個子樣本。
2. 先建立 survey design object。
3. 做 unweighted EDA 只當資料熟悉用，不拿來當正式人口結論。
4. 正式的比例、平均數、總量、分位數改用 `svy*` 函式。
5. 類別關係用 weighted table 與 `svychisq()`。
6. 視覺化時優先畫 weighted summaries，而不是只畫 raw counts。
7. 解釋結果時一起看 estimate 和標準誤。

## Common Mistakes

- 看到 `weight` 欄位卻直接忽略。
- 用 sample proportion 當成 population proportion。
- 對 survey data 直接跑普通 `chisq.test()`。
- 只報 weighted mean，不報標準誤或不確定性。
- 把 raw scatterplot 的視覺密度誤認成母體密度。
- 不先確認哪個 weight 適用於哪個分析子樣本。
