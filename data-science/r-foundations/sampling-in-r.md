# Sampling in R

這份筆記整理的是 sampling 在 R 裡的實作思路，不是抽樣理論的完整推導。理論背景可搭配統計章節的 sampling、estimation 與 bootstrap 筆記一起看；這裡的重點是你拿到一個 data frame 後，怎麼實際抽樣、重複抽樣、比較估計誤差。

## `slice_sample()` 與 `sample()`

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

## 固定隨機種子

```r
set.seed(19000113)

coffee_ratings %>%
  slice_sample(n = 5)
```

抽樣分析如果沒有固定種子，很容易讓 notebook、報告與除錯結果每次都變。不是所有情況都要固定，但在教學、重現與比較方法時通常應該固定。

## 以數量或比例抽樣

```r
coffee_ratings %>%
  slice_sample(n = 300)

coffee_ratings %>%
  slice_sample(prop = 0.25)
```

- `n =`：指定抽幾列。
- `prop =`：指定抽母體的幾成。

這兩者最好不要混用在同一個需求敘述裡，因為 sample size 對估計精度有直接影響。

## 點估計與 sample size

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

## 重複抽樣看 sampling variability

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

## Systematic Sampling

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

### 什麼時候 systematic sampling 很危險

如果資料已經依時間、地理、分數或任何週期性結構排序，systematic sampling 很可能把排序模式直接帶進樣本。

可以先檢查：

```r
coffee_ratings %>%
  ggplot(aes(x = rowid, y = aftertaste)) +
  geom_point() +
  geom_smooth()
```

如果 row order 有明顯 pattern，systematic sampling 不一定安全。

### 讓它比較安全的做法

```r
shuffled <- coffee_ratings %>%
  slice_sample(prop = 1) %>%
  select(-rowid) %>%
  rowid_to_column()
```

先 shuffle 再 systematic sample，通常就更接近 simple random sampling。

## Stratified Sampling

當你知道某些群體一定要被代表時，stratified sampling 比單純 random sample 更穩。

### 比例分層抽樣

```r
coffee_ratings %>%
  group_by(country_of_origin) %>%
  slice_sample(prop = 0.1) %>%
  ungroup()
```

每個 strata 都抽同樣比例，能大致保留群體結構。

### 各層固定筆數

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

## Weighted Sampling

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

## Stratified 與 Cluster 的差別

在 R 裡兩者都能寫，但目的不同：

- stratified sampling：每個群體都抽一些，重點是覆蓋不同 strata。
- cluster sampling：先抽群，再把群內個體一起納入或再抽，重點是降低收集成本。

如果你的分析目標是跨群體比較，通常優先考慮 stratified；如果你的收集成本是按群發生，cluster sampling 才比較有現實意義。

## With Replacement vs Without Replacement

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

## Bootstrap 的基本流程

Bootstrap 可以先記三步：

1. 從目前樣本中「有放回」重抽一個同樣大小的 resample
2. 計算想要的統計量
3. 重複很多次，形成 bootstrap distribution

```r
coffee_resamp <- coffee_focus %>%
  slice_sample(prop = 1, replace = TRUE)
```

這個 resample 會有兩個特徵：

- 有些 row 會重複出現
- 有些原始 row 不會出現在這次 resample 中

這正是 bootstrap 的正常現象，不是抽壞了。

## Bootstrap 統計量

```r
bootstrap_means <- replicate(
  n = 1000,
  expr = coffee_focus %>%
    slice_sample(prop = 1, replace = TRUE) %>%
    summarize(mean_flavor = mean(flavor)) %>%
    pull(mean_flavor)
)

bootstrap_distn <- tibble(resample_mean = bootstrap_means)
```

這組 `resample_mean` 的分布，就是 mean flavor 的 bootstrap distribution。

## 用 bootstrap 估標準誤

bootstrap standard error 最直接的做法，就是取 bootstrap distribution 的標準差。

```r
standard_error <- bootstrap_distn %>%
  summarize(se = sd(resample_mean)) %>%
  pull(se)
```

如果你沒有方便的解析公式，這是很實用的替代方案。

## 用 bootstrap 做信賴區間

### Quantile 法

```r
bootstrap_distn %>%
  summarize(
    lower = quantile(resample_mean, 0.025),
    upper = quantile(resample_mean, 0.975)
  )
```

這是 percentile / quantile 型 CI，簡單直接。

### Standard error 法

若 bootstrap distribution 近似對稱，也可用 estimate ± 1.96 * SE 的近似寫法：

```r
sample_mean <- coffee_focus %>%
  summarize(mean_flavor = mean(flavor)) %>%
  pull(mean_flavor)

lower <- sample_mean - 1.96 * standard_error
upper <- sample_mean + 1.96 * standard_error
```

但若分布偏斜，quantile 法通常比較穩。

## 實務提醒

- `slice_sample()` 是 tidyverse 裡最自然的抽樣入口。
- 抽樣流程若要可重現，記得 `set.seed()`。
- systematic sampling 只在 row order 沒有結構時才安全。
- stratified sampling 解決的是 representation，不是自動消除 bias。
- bootstrap 是從現有樣本近似 sampling variability，不會修復原始樣本本身的偏差。

如果你開始同時思考 sample design、point estimate、sampling variability 與 bootstrap uncertainty，代表你已經不只是在「抽幾筆資料」，而是在建立完整的 inferential workflow。
