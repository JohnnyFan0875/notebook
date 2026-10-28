[Data Science](../README.md) › [R Foundations](README.md) › 統計函式速查

# 統計函式速查 (Statistical Functions in R)

已經懂統計概念、只是忘了 R 函式名稱或參數時查這頁。方法選擇與解讀見 [Statistics](../statistics/README.md) 與 [方法選擇速查](../statistics/method-selection.md)；Python 對照見 [scipy.stats 速查](../python-foundations/scipy-stats.md)；迴歸模型見 [R 解釋型建模](explanatory-modeling-in-r.md)。

## 機率分配：`d / p / q / r`

所有分配都遵守「前綴 + 分配名」的規則。

| 前綴 | 意義 | 問題 | 常態例 |
| --- | --- | --- | --- |
| `d` | 密度 / 機率質量 | P(X = x)（離散）或密度 | `dnorm(0)` → 0.399 |
| `p` | 累積機率 (CDF) | P(X ≤ q) | `pnorm(1.96)` → 0.975 |
| `q` | 分位數（CDF 反函數） | 哪個值使 P(X ≤ q) = p | `qnorm(0.975)` → 1.96 |
| `r` | 隨機抽樣 | 產生模擬資料 | `rnorm(5)` |

| 分配 | 名稱 | 參數 | 生資常見用途 |
| --- | --- | --- | --- |
| 常態 | `norm` | `mean`, `sd` | log 表現量、z 分數 |
| t | `t` | `df` | 小樣本平均數 CI |
| χ² / F | `chisq` / `f` | `df` / `df1, df2` | 列聯表、ANOVA |
| 二項 | `binom` | `size`, `prob` | 等位基因計數、成功次數 |
| Poisson | `pois` | `lambda` | 讀數計數（無過度離散） |
| 負二項 | `nbinom` | `size`（離散參數）, `mu` | RNA-seq counts，見 [計數模型](../statistics/regression-analysis/glm-count-models.md) |
| 超幾何 | `hyper` | `m`, `n`, `k` | 富集分析 |
| 均勻 / 指數 / Beta / Gamma | `unif` / `exp` / `beta` / `gamma` | | 模擬、先驗、等待時間 |

```r
set.seed(42)                                   # 抽樣前固定 seed
pnorm(1.96, lower.tail = FALSE) * 2            # 雙尾 p ≈ 0.05
qt(0.975, df = 9)                              # 2.262   n=10 的 95% CI 臨界值
dbinom(3, size = 10, prob = 0.4)               # 0.215   恰好 3 次
pbinom(3, size = 10, prob = 0.4)               # 0.382   ≤ 3 次
rnbinom(5, size = 2, mu = 100)                 # 過度離散的計數

# 富集：20000 基因中 200 個在 pathway；50 個 DEG 中 5 個落在 pathway
phyper(5 - 1, m = 200, n = 20000 - 200, k = 50, lower.tail = FALSE)   # P(X ≥ 5)
```

> `lower.tail = FALSE` 回傳 P(X > q)。離散分配要算 P(X ≥ k) 時傳入 `k - 1`。

## 描述統計

```r
x <- c(2, 5, 11, 11, 13, NA)

mean(x, na.rm = TRUE); median(x, na.rm = TRUE)   # base R 預設不移除 NA
sd(x, na.rm = TRUE); var(x, na.rm = TRUE)        # 分母 n − 1
IQR(x, na.rm = TRUE); mad(x, na.rm = TRUE)       # mad() 預設乘 1.4826（常態下 ≈ SD）
quantile(x, c(0.25, 0.5, 0.75), na.rm = TRUE)    # type = 7，與 numpy 預設相同
range(x, na.rm = TRUE); summary(x)               # summary 會列出 NA 個數
scale(x)                                         # z 分數（回傳 matrix）
table(g); prop.table(table(g))                   # 次數與比例
cor(df$x, df$y, method = "spearman", use = "complete.obs")   # pearson / spearman / kendall
cov(x, y)                                        # 單位相依，跨變數比較用 cor
```

## 檢定

| 問題 | 函式 | 備註 |
| --- | --- | --- |
| 一樣本 / 兩獨立樣本平均 | `t.test(x, y)` | 預設 Welch（`var.equal = FALSE`） |
| 配對平均 | `t.test(x, y, paired = TRUE)` | 或 `t.test(d)`，d = 差值 |
| 兩組中位數（非參數） | `wilcox.test(x, y)` | 配對加 `paired = TRUE` |
| 多組平均 | `aov(y ~ g, data)` → `summary()` | 事後檢定 `TukeyHSD()` |
| 多組非參數 | `kruskal.test(y ~ g, data)` | |
| 列聯表獨立性 | `chisq.test(table(a, b))` | 期望值 < 5 改 `fisher.test()` |
| 比例 | `prop.test(x, n)`、`binom.test(x, n)` | |
| 相關顯著性 | `cor.test(x, y, method = "spearman")` | |
| 常態性 | `shapiro.test(x)`、`qqnorm(x); qqline(x)` | n 大時幾乎必拒絕，以圖為主 |
| 變異數同質 | `bartlett.test()`、`car::leveneTest()` | |
| 多重檢定校正 | `p.adjust(p, method = "BH")` | `"bonferroni"`、`"holm"`、`"BY"` |

```r
res <- t.test(expr ~ group, data = df)          # formula 介面：數值 ~ 分組
res$p.value; res$conf.int; res$estimate         # 檢定結果是 list
broom::tidy(res)                                # 轉成一列 tibble，方便批次整理

# 對每個基因做檢定 → 校正
pvals <- apply(mat, 1, \(g) t.test(g[grp == "trt"], g[grp == "ctrl"])$p.value)
padj  <- p.adjust(pvals, method = "BH")
```

> 數千個基因逐一 `t.test()` 在小樣本下變異數估計不穩，實務上改用 limma / DESeq2 的 shrinkage 方法；見 [多重檢定](../statistics/inferential-statistics/multiple-testing.md) 與 [統計檢定總覽](../statistics/inferential-statistics/statistical-tests.md)。

## 常見錯誤

| 錯誤 | 對策 |
| --- | --- |
| 忘記 `na.rm = TRUE`，結果是 `NA` | 先 `sum(is.na(x))` 確認缺值量 |
| 用 `dnorm()` 算累積機率 | 累積機率用 `pnorm()` |
| `glm()` 忘記 `family`，變成普通線性迴歸 | logistic：`family = binomial`；計數：`poisson` / `MASS::glm.nb()` |
| 用常態性檢定 p 值決定一切 | 搭配 Q-Q plot，見 [假設檢查](../statistics/inferential-statistics/assumption-checks.md) |
| `cor()` 遇到 NA 回傳 `NA` | `use = "complete.obs"` 或 `"pairwise.complete.obs"` |
| 相關當因果 | 見 [雙變數分析](../statistics/descriptive-statistics/bivariate.md) |
