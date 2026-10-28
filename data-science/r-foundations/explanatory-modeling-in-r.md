[Data Science](../README.md) › [R Foundations](README.md) › 解釋型建模

# 解釋型建模 (Explanatory Modeling in R)

解釋型建模的目標是理解 outcome 與 predictors 的關係（方向、大小、不確定性），而不是追求最低預測誤差。本篇聚焦 **R 的操作**：formula 語法、`lm()` / `glm()`、類別變數編碼、broom 整理輸出、模型比較。迴歸理論、假設與診斷見 [迴歸分析](../statistics/regression-analysis/README.md)；以預測為目標的流程見 [tidymodels](../machine-learning/packages/tidymodels/README.md)。

## 流程

```
1. 畫圖：散點圖 + 平滑線，看方向、形狀、離群、變異是否隨 x 改變
2. 決定轉換：右偏的正值變數 → log
3. 擬合：lm()（連續）/ glm()（二元、計數）
4. 診斷：殘差圖、影響點
5. 整理：broom::tidy() / glance() / augment()
6. 比較候選模型：anova()、AIC；解讀效應量與信賴區間，不只看 p 值
```

```r
library(tidyverse)
library(broom)

ggplot(evals, aes(age, score)) +
  geom_point(alpha = 0.4) +
  geom_smooth(method = "lm", se = FALSE) +              # 線性趨勢
  geom_smooth(method = "loess", se = FALSE, color = "tomato")   # 對照：是否彎曲
```

## Formula 語法

| 寫法 | 意義 | 例子 |
| --- | --- | --- |
| `y ~ x` | 簡單迴歸 | `score ~ age` |
| `y ~ x1 + x2` | 多個主效應 | `expr ~ condition + batch` |
| `y ~ x1:x2` | 只有交互作用項 | |
| `y ~ x1 * x2` | 主效應 + 交互作用（= `x1 + x2 + x1:x2`） | `expr ~ genotype * treatment` |
| `y ~ . ` | 資料中其他所有欄位 | |
| `y ~ . - id` | 排除某欄 | |
| `y ~ x - 1` 或 `y ~ 0 + x` | 不要截距（類別變數時每組一個係數） | limma 的 `~ 0 + group` |
| `y ~ log(x)` | 公式內轉換 | |
| `y ~ I(x^2)` | 算術運算要用 `I()` 包住 | `^` 在 formula 中另有意義 |
| `y ~ poly(x, 2)`、`splines::ns(x, df = 3)` | 多項式、自然樣條 | 非線性關係 |
| `y ~ offset(log(libsize)) + x` | 係數固定為 1 的項 | 計數模型的定序深度 |

```r
model.matrix(~ condition + batch, data = coldata)   # 看 formula 實際產生的設計矩陣
```

`model.matrix()` 就是 DESeq2 / limma 的 `design` 背後的東西，見 [limma](../../biology/genomics/sequencing-and-analysis/workflows/limma-differential-expression.md)。

## 線性模型 `lm()`

```r
house <- house_prices |>
  mutate(log10_price = log10(price), log10_size = log10(sqft_living))

fit <- lm(log10_price ~ log10_size + yr_built + condition, data = house)

summary(fit)              # 係數、SE、t、p、R²、殘差標準誤
confint(fit)              # 係數的 95% CI
tidy(fit, conf.int = TRUE)  # 係數表 → tibble
glance(fit)               # 模型層級：r.squared、adj.r.squared、sigma、AIC、BIC
augment(fit)              # 每列：.fitted、.resid、.hat、.cooksd

predict(fit, newdata = new_houses, interval = "confidence")   # 平均值的 CI
predict(fit, newdata = new_houses, interval = "prediction")   # 單一新觀測的 PI（較寬）

par(mfrow = c(2, 2)); plot(fit)   # 4 張診斷圖：殘差 vs fitted、Q-Q、scale-location、leverage
```

| 輸出 | 怎麼讀 |
| --- | --- |
| 多元迴歸的係數 | **其他變數固定時**，該變數增加一單位，y 的平均變化；不能當成單變數相關來讀 |
| log10–log10 模型的係數 | 彈性：x 增加 1%，y 約增加 β% |
| 只對 y 取 log | x 增加一單位，y 乘以 10^β（自然 log 則為 e^β） |
| R² vs adjusted R² | 加變數 R² 必增；比較不同變數數的模型用 adjusted R² 或 AIC |
| `sigma` | 殘差標準差，與 y 同單位，代表典型的預測誤差 |

殘差圖的判讀見 [模型假設與診斷](../statistics/multivariate-analysis/assumptions-diagnostics.md)；解釋與預測目標的差異見 [多元線性迴歸](../statistics/regression-analysis/multiple-linear-regression.md)。

## 類別變數

R 會自動把 factor 轉成 dummy 變數，**第一個 level 是參考組**，其他係數都是「與參考組的差」。

```r
coldata$condition <- factor(coldata$condition, levels = c("control", "treated"))
coldata$condition <- relevel(coldata$condition, ref = "control")   # 同樣效果

fit <- lm(expr ~ condition + batch, data = coldata)
# conditiontreated 的係數 = treated − control（在 batch 固定下）
```

| 想要 | 做法 |
| --- | --- |
| 改參考組 | `relevel()` 或 `factor(levels = )`，見 [類別資料](categorical-data.md) |
| 所有組兩兩比較 | `emmeans::emmeans(fit, pairwise ~ group)`（含多重比較校正） |
| 各組的調整後平均（marginal means） | `emmeans::emmeans(fit, ~ group)` |
| 整個類別變數是否有效應 | `anova(fit)` 或 `car::Anova(fit, type = 2)` |

> 交互作用模型 `y ~ genotype * treatment` 中，`treatment` 的主效應係數是「在 genotype **參考組**下」的處理效應，不是整體平均效應。這是解讀 DESeq2 交互作用設計時最常見的誤解。

## 廣義線性模型 `glm()`

| outcome | family | 係數解讀 | 筆記 |
| --- | --- | --- | --- |
| 二元（有病 / 沒病） | `binomial` | exp(β) = odds ratio | [邏輯斯迴歸](../statistics/regression-analysis/logistic-regression.md) |
| 計數 | `poisson` | exp(β) = rate ratio | [計數資料 GLM](../statistics/regression-analysis/glm-count-models.md) |
| 過度離散計數（RNA-seq reads） | `MASS::glm.nb()` | exp(β) = rate ratio | 同上 |
| 正值、右偏（濃度） | `Gamma(link = "log")` | exp(β) = 平均值的倍數 | |

```r
fit_lr <- glm(disease ~ age + sex + smoking, family = binomial, data = cohort)
tidy(fit_lr, exponentiate = TRUE, conf.int = TRUE)   # 直接得到 OR 與 95% CI

fit_nb <- MASS::glm.nb(count ~ condition + offset(log(libsize)), data = df)
```

重複測量、同一病人多個樣本時要用混合模型（`lme4::lmer()`），見 [混合效應模型](../statistics/regression-analysis/mixed-effects-models.md)。

## 模型比較

```r
m1 <- lm(log10_price ~ log10_size, data = house)
m2 <- lm(log10_price ~ log10_size + yr_built + condition, data = house)

anova(m1, m2)                 # 巢狀模型的 F 檢定：多加的變數整體是否有幫助
AIC(m1, m2); BIC(m1, m2)      # 越小越好；不需巢狀，但資料必須相同（注意 NA 造成的列數差異）
map(list(m1 = m1, m2 = m2), glance) |> list_rbind(names_to = "model")
```

| 指標 | 用途 |
| --- | --- |
| `anova()` | 巢狀模型；glm 用 `anova(m1, m2, test = "LRT")` |
| AIC / BIC | 兼顧配適與複雜度；BIC 懲罰較重 |
| adjusted R² | 只限線性模型 |
| 殘差圖 | 新模型是否修正了系統性型態 |

> 解釋型建模中，變數的選擇應由研究問題與因果假設決定（要控制哪些混淆因子），而不是逐步迴歸挑出 p 值最小的組合。見 [混淆與偏誤](../statistics/experimental-design/confounding-bias.md)。

## 常見錯誤

| 錯誤 | 修正 |
| --- | --- |
| 沒畫圖就 `lm()` | 先看散點圖：彎曲、分群、變異不等 |
| 只看 p 值 | 報告效應量與 CI（`tidy(conf.int = TRUE)`） |
| 右偏的價格、濃度直接建模 | 取 log，或用 Gamma / log-link GLM |
| 數值編碼的類別（批次 1、2、3）沒轉 factor | 被當成連續變數，只估一個斜率；先 `factor()` |
| 參考組不是預期的組 | fold change 方向相反；明確設定 levels |
| 比較 AIC 時兩個模型用的列數不同 | 有 NA 的欄位會讓 `lm()` 自動刪列；先 `drop_na()` 統一資料 |
| `I()` 漏寫：`y ~ x^2` | formula 中 `^` 是交互作用展開，結果只有 `x`；寫 `I(x^2)` 或 `poly()` |
