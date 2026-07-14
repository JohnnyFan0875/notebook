# Statistical Functions in R

這頁整理的是「已經懂統計概念，但在 R 裡常忘記函式名字或輸入格式」時最常用的那一層。重點不是重講統計理論，而是把常見分析問題快速映射到 R 的函式介面。

## 先記住 `d / p / q / r`

R 的機率分布函式有一套非常穩定的命名規則：

| Prefix | Meaning | Typical question |
| ------ | ------- | ---------------- |
| `d*` | density / mass | 某個值的 density 或 probability 是多少 |
| `p*` | cumulative probability | 小於等於某個值的機率是多少 |
| `q*` | quantile | 給定機率，要找哪個分位點 |
| `r*` | random generation | 依照某分布抽樣 |

例如 normal distribution：

```r
dnorm(0)                # density at x = 0
pnorm(1.96)             # P(X <= 1.96)
qnorm(0.975)            # 97.5th percentile
rnorm(5, mean = 0, sd = 1)
```

同樣規則也會出現在其他分布：

```r
dbinom(3, size = 10, prob = 0.4)
pbinom(3, size = 10, prob = 0.4)
qbinom(0.8, size = 10, prob = 0.4)
rbinom(5, size = 10, prob = 0.4)
```

Key point: 看到新的分布名字時，先不要急著背四個函式；先確認它也遵守 `d/p/q/r + distribution_name` 這個規律。

## Descriptive Statistics

最常用的摘要函式：

```r
x <- c(2, 5, 11, 11, 13, NA)

mean(x, na.rm = TRUE)
median(x, na.rm = TRUE)
sd(x, na.rm = TRUE)
var(x, na.rm = TRUE)
range(x, na.rm = TRUE)
quantile(x, probs = c(0.25, 0.5, 0.75), na.rm = TRUE)
summary(x)
```

## Interview Fast Mapping

如果面試或實作時要快速回答「這個統計量在 R 裡怎麼算」，一個很常用的對照是：

- mean: `mean()`
- median: `median()`
- variance: `var()`
- standard deviation: `sd()`
- correlation: `cor()`
- covariance: `cov()`

高訊號補充通常是：

- 很多 base R 統計函式都需要自己加 `na.rm = TRUE`
- `summary()` 適合先做第一輪 data sanity check，但不等於完整 EDA

## Normality Checks

normality 不該只靠單一 p-value。比較穩的順序通常是：先看圖，再看 formal test。

### Q-Q Plot

```r
x <- rnorm(100)

qqnorm(x)
qqline(x, col = "red")
```

如果點大致落在直線附近，表示常態假設還算合理。

### Shapiro-Wilk Test

```r
shapiro.test(x)
```

這通常是小到中等樣本的預設選擇。

### Kolmogorov-Smirnov Test

```r
ks.test(x, "pnorm", mean(x), sd(x))
```

Warning: 大樣本下，normality test 很容易因為很小的偏離就拒絕虛無假設，所以還是要搭配 Q-Q plot 一起看。

## Covariance and Correlation

如果你想量化兩個數值變數一起變動的方向與強度：

```r
x <- c(3, 5, 7)
y <- c(6, 11, 13)

cov(x, y)
cor(x, y)
```

常見變體：

```r
cor(x, y, method = "pearson")
cor(x, y, method = "spearman")
cor(x, y, method = "kendall")
```

Key point: `cov()` 的量綱會跟原始資料有關，不適合直接比較不同尺度；`cor()` 被標準化到 `[-1, 1]`，通常更容易解讀。

## Linear and Logistic Regression in R

### Linear Regression

```r
model_lm <- lm(y ~ x1 + x2, data = df)
summary(model_lm)
```

通常先看：

- coefficients
- `R-squared`
- residual standard error
- p-values

### Logistic Regression

```r
model_glm <- glm(y ~ x1 + x2, data = df, family = "binomial")
summary(model_glm)
predict(model_glm, newdata = df, type = "response")
```

這裡的 `type = "response"` 很重要，因為它會把 log-odds 轉成 probability。

## Common Mistakes

- 忘記 `na.rm = TRUE`，導致摘要統計直接回 `NA`
- 把 `dnorm()` 當成 cumulative probability；累積機率應該用 `pnorm()`
- 看到 `glm()` 就直接當線性回歸；是否為 logistic 要看 `family = "binomial"`
- 用單一 normality test 的 p-value 代替整個 assumption check
- 把 `correlation` 當成 causation

## Related Notes

- [Functions in R](functions.md)
- [Vectors in R](vectors.md)
- [Probability Basics](../statistics/probability-and-distributions/probability-basics.md)
- [Discrete Distributions](../statistics/probability-and-distributions/discrete-distributions.md)
- [Assumption Checks](../statistics/inferential-statistics/assumption-checks.md)
- [Bivariate Analysis](../statistics/descriptive-statistics/bivariate.md)
- [Simple Linear Regression](../statistics/regression-analysis/simple-linear-regression.md)
- [Logistic Regression](../statistics/regression-analysis/logistic-regression.md)
