# Explanatory Modeling in R

當你在 R 裡做 regression，真正重要的通常不是 `lm()` 這個函式本身，而是你怎麼把視覺化、模型公式、係數整理與模型比較串成一條清楚的分析流程。

這類 workflow 比較接近 explanatory modeling: 重點不是只求最低預測誤差，而是想理解 outcome 和 predictors 之間的關係。

## A Simple Mental Model

很多迴歸分析都可以先用這個框架理解：

\[
y = f(x) + \epsilon
\]

- `y`: outcome variable
- `x`: explanatory / predictor variables
- `f(x)`: 系統性的訊號
- `\epsilon`: 沒有被模型解釋掉的 noise

Key point: explanatory modeling 的重點是把資料中的結構講清楚，不是把所有殘差都消滅。

## Start with Visualization

在線性模型之前，先用圖看關係方向與形狀：

```r
library(ggplot2)

ggplot(evals, aes(x = age, y = score)) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE)
```

- `geom_point()` 先看資料雲的分布。
- `geom_smooth(method = "lm")` 幫你把線性趨勢畫出來。
- `se = FALSE` 讓圖先聚焦在 fitted line 本身。

如果散點圖看起來明顯彎曲、分群或變異隨 `x` 改變，再直接套簡單線性模型通常就不夠。

## Fitting a Simple Regression

```r
model_score <- lm(score ~ age, data = evals)
summary(model_score)
```

- 左邊是 outcome
- 右邊是 predictor
- `summary()` 先看係數、標準誤、`R^2` 與殘差尺度

這一步的核心不是把輸出全部背下來，而是先回答：

- 方向是正還是負
- 關係大不大
- 線性模型是否至少大致合理

## Multiple Regression Changes the Question

當你加進更多 predictors，係數的意思就變成：

- 在其他變數固定時，某個 predictor 和 outcome 的關係

```r
model_price <- lm(log10_price ~ log10_size + yr_built, data = house_prices)
summary(model_price)
```

這讓你從「單純相關」往「控制其他因素後的關係」前進。

如果你再把類別變數加進來：

```r
model_price_cat <- lm(log10_price ~ log10_size + condition, data = house_prices)
```

R 會透過 formula interface 自動做 dummy coding，所以你通常不需要手動建立 indicator columns。

## Log Transforms Often Help Interpretation

在價格、面積、人口這種右偏變數上，直接建模常會讓殘差很不穩定。常見做法是先轉成 log scale：

```r
house_prices <- house_prices %>%
  mutate(
    log10_price = log10(price),
    log10_size = log10(sqft_living)
  )
```

這麼做常見的目的有三個：

- 壓縮極端值影響
- 讓關係更接近線性
- 讓比例變化比絕對差更容易解讀

Key point: transform 不是為了讓圖更好看，而是讓模型關係與誤差結構更合理。

## Tidy Output with `broom`

如果你要把模型結果接到後續整理、比較或視覺化，`broom` 會比一直看 `summary()` 更順手：

```r
library(broom)

tidy(model_price)
glance(model_price)
augment(model_price)
```

- `tidy()`: 係數層級結果
- `glance()`: 模型層級摘要，例如 `r.squared`、`adj.r.squared`、`sigma`
- `augment()`: 每筆資料的 fitted value、residual 與診斷欄位

這種分層很有用，因為你不會再把「係數表」和「逐列 residuals」混在同一個輸出裡找。

## Teaching-Friendly Helpers from `moderndive`

如果你想更直接地把 regression 結果整理成易讀表格，`moderndive` 很方便：

```r
library(moderndive)

get_regression_table(model_price)
get_regression_points(model_price)
```

- `get_regression_table()` 適合快速看 estimate、standard error、statistic、p-value。
- `get_regression_points()` 適合把 observed、fitted 與 residual 接回 row-level workflow。

這對教學、筆記整理或想快速檢查 residual pattern 時特別實用。

## Sum of Squared Residuals

很多 regression fitting 的核心都圍繞在 residuals：

```r
get_regression_points(model_price) %>%
  mutate(sq_residuals = residual^2) %>%
  summarize(sum_sq_residuals = sum(sq_residuals))
```

這個量對應的是模型沒有解釋好的部分。平方後再加總，有兩個效果：

- 正負 residual 不會互相抵消
- 大誤差會被更重地懲罰

這也是最小平方法背後的重要直覺。

## Comparing Models

在 explanatory modeling 裡，常常不是只有一個模型，而是要比較多個合理版本：

```r
model_1 <- lm(log10_price ~ log10_size + yr_built, data = house_prices)
model_2 <- lm(log10_price ~ log10_size + condition, data = house_prices)

glance(model_1)
glance(model_2)
```

比較時可以先看：

- `adj.r.squared`
- `sigma`
- AIC / BIC
- residual pattern 是否更穩定

不要只因為某個模型 `R^2` 較高就直接選它。變數越多，表面 fit 通常越好，但解釋價值不一定更高。

## A Practical Workflow

一個很穩定的分析節奏通常長這樣：

1. 先用圖看 relationship 與可能的 transformation。
2. 用 `lm()` 建立簡單模型。
3. 必要時加入其他 numerical 或 categorical predictors。
4. 用 `broom` 或 `moderndive` 把輸出整理成 tibble。
5. 比較多個模型，不只看 fit，也看可解釋性與 residual behavior。

## Common Mistakes

- 一看到連續 outcome 就直接 `lm()`，沒有先畫散點圖。
- 只看 p-value，不看 effect size、residual pattern 與模型假設。
- 用 raw scale 建模明顯右偏的資料，卻忽略 log transform。
- 把多變數模型的係數當成單變數相關來讀。
- 比較模型時只看 `R^2`，忽略 adjusted `R^2`、`sigma` 與模型複雜度。

## Where to Go Next

- 如果你想把模型、前處理與評估包成更完整 pipeline，接著看 [Modeling with tidymodels](modeling-with-tidymodels.md)。
- 如果你想補 regression 理論與假設診斷，接著看 statistics 模組裡的 simple / multiple regression 筆記。
