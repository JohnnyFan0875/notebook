[Statistics](../README.md) › [推論統計](README.md) › 抽樣設計與調查資料

# 抽樣設計與調查資料分析 (Survey Sampling in R)

用 R 實作 [抽樣與估計](sampling-estimation.md) 的抽樣方法（random / systematic / stratified / weighted / bootstrap），以及有權重的複雜抽樣調查資料（NHANES、`survey` 套件）。

## Sampling in R

這份筆記整理的是 sampling 在 R 裡的實作思路，不是抽樣理論的完整推導。理論背景可搭配統計章節的 sampling、estimation 與 bootstrap 筆記一起看；這裡的重點是你拿到一個 data frame 後，怎麼實際抽樣、重複抽樣、比較估計誤差。

### `slice_sample()` 與 `sample()`

先分清楚兩個基本工具：

- `slice_sample()`：對 data frame / tibble 抽列。
- `sample()`：對向量抽值。

```r
library(dplyr)

coffee_ratings %>%
  slice_sample(n = 5)

cup_points_samp <- sample(coffee_ratings$total_cup_points, size = 10)
```

如果你的抽樣單位是一整列觀測，優先用 `slice_sample()`；只有在你真的只想抽單一向量值時，才直接用 `sample()`。

### 固定隨機種子

```r
set.seed(19000113)

coffee_ratings %>%
  slice_sample(n = 5)
```

抽樣分析如果沒有固定種子，很容易讓 notebook、報告與除錯結果每次都變。不是所有情況都要固定，但在教學、重現與比較方法時通常應該固定。

### 以數量或比例抽樣

```r
coffee_ratings %>%
  slice_sample(n = 300)

coffee_ratings %>%
  slice_sample(prop = 0.25)
```

- `n =`：指定抽幾列。
- `prop =`：指定抽母體的幾成。

這兩者最好不要混用在同一個需求敘述裡，因為 sample size 對估計精度有直接影響。

### 點估計與 sample size

最常見的 workflow 是：

1. 抽一個 sample
2. 算統計量
3. 看它和母體參數差多少

```r
population_mean <- coffee_ratings %>%
  summarize(mean_points = mean(total_cup_points)) %>%
  pull(mean_points)

sample_mean <- coffee_ratings %>%
  slice_sample(n = 100) %>%
  summarize(mean_points = mean(total_cup_points)) %>%
  pull(mean_points)
```

相對誤差可寫成：

```r
100 * abs(population_mean - sample_mean) / population_mean
```

實務感受通常很一致：

- sample 太小，點估計很容易飄。
- sample 變大，估計通常更穩。
- 但 sample 大不代表抽樣設計合理，偏樣本還是會偏。

### 重複抽樣看 sampling variability

同樣的 `n = 30` 抽樣，每次答案都可能不同。這不是 bug，而是 sampling variability。

```r
mean_cup_points_1000 <- replicate(
  n = 1000,
  expr = coffee_ratings %>%
    slice_sample(n = 30) %>%
    summarize(mean_cup_points = mean(total_cup_points)) %>%
    pull(mean_cup_points)
)
```

這樣得到的 1000 個樣本平均，就是 sampling distribution 的模擬近似。

如果想看分布：

```r
tibble(mean_cup_points = mean_cup_points_1000) %>%
  ggplot(aes(mean_cup_points)) +
  geom_histogram(bins = 30)
```

### Systematic Sampling

Systematic sampling 的想法是每隔固定間距取一列。

```r
library(tibble)

coffee_ratings <- coffee_ratings %>%
  rowid_to_column()

sample_size <- 5
pop_size <- nrow(coffee_ratings)
interval <- pop_size %/% sample_size
row_indexes <- seq_len(sample_size) * interval

coffee_ratings %>%
  slice(row_indexes)
```

這種方法很快，但有一個前提：資料列順序本身不能帶有你在意的結構模式。

#### 什麼時候 systematic sampling 很危險

如果資料已經依時間、地理、分數或任何週期性結構排序，systematic sampling 很可能把排序模式直接帶進樣本。

可以先檢查：

```r
coffee_ratings %>%
  ggplot(aes(x = rowid, y = aftertaste)) +
  geom_point() +
  geom_smooth()
```

如果 row order 有明顯 pattern，systematic sampling 不一定安全。

#### 讓它比較安全的做法

```r
shuffled <- coffee_ratings %>%
  slice_sample(prop = 1) %>%
  select(-rowid) %>%
  rowid_to_column()
```

先 shuffle 再 systematic sample，通常就更接近 simple random sampling。

### Stratified Sampling

當你知道某些群體一定要被代表時，stratified sampling 比單純 random sample 更穩。

#### 比例分層抽樣

```r
coffee_ratings %>%
  group_by(country_of_origin) %>%
  slice_sample(prop = 0.1) %>%
  ungroup()
```

每個 strata 都抽同樣比例，能大致保留群體結構。

#### 各層固定筆數

```r
coffee_ratings %>%
  group_by(country_of_origin) %>%
  slice_sample(n = 15) %>%
  ungroup()
```

這種寫法適合：

- 小群體很重要，不想在比例抽樣時被稀釋掉
- 想讓各群體比較更公平

但要記得，固定筆數會改變樣本裡各群體的原始占比。

### Weighted Sampling

有時你想讓某些觀測更容易被抽中。

```r
coffee_ratings_weight <- coffee_ratings %>%
  mutate(weight = if_else(country_of_origin == "Taiwan", 2, 1))

coffee_ratings_weight %>%
  slice_sample(prop = 0.1, weight_by = weight)
```

`weight_by` 不是保證一定抽到，而是改變被抽中的機率。這很適合：

- 模擬不均勻抽樣機制
- 提高某些稀有但重要群體進樣本的機率

### Stratified 與 Cluster 的差別

在 R 裡兩者都能寫，但目的不同：

- stratified sampling：每個群體都抽一些，重點是覆蓋不同 strata。
- cluster sampling：先抽群，再把群內個體一起納入或再抽，重點是降低收集成本。

如果你的分析目標是跨群體比較，通常優先考慮 stratified；如果你的收集成本是按群發生，cluster sampling 才比較有現實意義。

### With Replacement vs Without Replacement

一般樣本抽取常是 without replacement：

```r
sample(1:6, size = 4, replace = FALSE)
```

bootstrap resampling 則是 with replacement：

```r
sample(1:6, size = 4, replace = TRUE)
```

差別不是語法小細節，而是統計意義完全不同：

- without replacement：模擬從母體抽一批不重複觀測
- with replacement：允許重複抽到同一筆，常用來近似 sampling variability

### Bootstrap in R

概念、適用條件與 percentile vs BCa 見 [抽樣與估計](sampling-estimation.md) 與 [拔靴法](../probability-and-distributions/monte-carlo-simulation.md#拔靴法-bootstrap)。R 寫法：

```r
bootstrap_means <- replicate(1000, coffee_focus %>%
  slice_sample(prop = 1, replace = TRUE) %>%
  summarize(m = mean(flavor)) %>% pull(m))

sd(bootstrap_means)                        # bootstrap SE
quantile(bootstrap_means, c(0.025, 0.975)) # percentile 95% CI
```

### 實務提醒

- `slice_sample()` 是 tidyverse 裡最自然的抽樣入口。
- 抽樣流程若要可重現，記得 `set.seed()`。
- systematic sampling 只在 row order 沒有結構時才安全。
- stratified sampling 解決的是 representation，不是自動消除 bias。
- bootstrap 是從現有樣本近似 sampling variability，不會修復原始樣本本身的偏差。

如果你開始同時思考 sample design、point estimate、sampling variability 與 bootstrap uncertainty，代表你已經不只是在「抽幾筆資料」，而是在建立完整的 inferential workflow。

## Survey Data Analysis in R

survey data 和一般表格資料最大的差別，不是多了一欄 `weight` 而已，而是樣本本身來自特定抽樣設計。只把 survey data 當普通 data frame 做平均、比例與圖表，常會得到偏掉的 population story。

### Why Survey Weights Exist

survey weight 大致可以理解成：

- 一筆樣本在母體中代表多少個單位
- 抽樣設計與非等機率抽樣留下來的校正資訊

例如某筆 household 的 weight 若是 `25,985`，直覺上表示這筆樣本代表母體中的很多戶，不應和 weight 很小的樣本被等量對待。

Key point: survey weights 不是可有可無的修飾欄位，而是讓 sample estimate 更接近 population estimate 的核心資訊。

### Start With a Survey Design Object

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

### Unweighted and Weighted Can Tell Different Stories

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

### Weighted Categorical Summaries

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

### Weighted Quantitative Summaries

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

### Standard Errors Matter

survey data 的另一個核心觀念是：即使 estimate 看起來簡單，標準誤也不能直接沿用 iid sample 的公式。

當你看到：

- `mean`
- `total`
- `SE`

要把它理解成：

- 這不是單純把 weights 乘上去而已
- 抽樣設計會影響變異估計

如果只做 weighted average 卻忽略 `SE`、confidence interval 或設計效果，就只完成了一半分析。

### Visualizing Weighted Categorical Data

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

### Scatterplots Need Extra Care

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

### Weighted Smoothers in Plots

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

### A Practical Survey Workflow

如果拿到 NHANES、BLS 或其他大型 survey data，可以用這個順序工作：

1. 先確認權重欄位代表什麼母體與哪個子樣本。
2. 先建立 survey design object。
3. 做 unweighted EDA 只當資料熟悉用，不拿來當正式人口結論。
4. 正式的比例、平均數、總量、分位數改用 `svy*` 函式。
5. 類別關係用 weighted table 與 `svychisq()`。
6. 視覺化時優先畫 weighted summaries，而不是只畫 raw counts。
7. 解釋結果時一起看 estimate 和標準誤。

### Common Mistakes

- 看到 `weight` 欄位卻直接忽略。
- 用 sample proportion 當成 population proportion。
- 對 survey data 直接跑普通 `chisq.test()`。
- 只報 weighted mean，不報標準誤或不確定性。
- 把 raw scatterplot 的視覺密度誤認成母體密度。
- 不先確認哪個 weight 適用於哪個分析子樣本。
