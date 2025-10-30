# Hypothesis Testing

Hypothesis testing is a framework to decide whether observed data provides enough evidence to reject a null hypothesis H₀.

## General Notes

- **Null hypothesis (H₀):** No effect or no difference.
- **Alternative hypothesis (Hₐ):** There is an effect or difference.
- **Test statistic:** A standardized value (z, t, or F) used to compute the p-value.
- **Central Limit Theorem (CLT)**: When the sample size is sufficiently large (typically n ≥ 30), the sampling distribution of the sample mean approximates a normal distribution, regardless of the population’s original shape.

## Type I and Type II Errors

| 概念               | 真實狀況    | 檢定結果               | 結果解釋           | 類型                  |
| ------------------ | ----------- | ---------------------- | ------------------ | --------------------- |
| **True Positive**  | Hₐ (有差異) | 拒絕 H₀ (認為有差異)   | 正確偵測到效果存在 | 正確                  |
| **False Positive** | H₀ (無差異) | 拒絕 H₀ (認為有差異)   | 錯誤地以為有差異   | **Type I error (α)**  |
| **True Negative**  | H₀ (無差異) | 不拒絕 H₀ (認為無差異) | 正確判定無差異     | 正確                  |
| **False Negative** | Hₐ (有差異) | 不拒絕 H₀ (認為無差異) | 錯誤地忽略真實差異 | **Type II error (β)** |

## Assumptions

- **Randomness:** Samples are random subsets of larger populations
- **Independence:** Each observation is independent (except paired tests)
- **Sample size:** Large enough for the Central Limit Theorem (CLT) to apply

## Basic Concepts

| Term                                                                                      | Meaning                                                                           | Note                      |
| ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ------------------------- |
| [**Significance (α) & Confidence Levels (1 − α)**](significance-and-confidence-levels.md) | 決定願意接受多大的錯誤機率（Type I error），並對應到信賴水準。                    | 影響信賴區間與臨界值設定  |
| [**Confidence Intervals (CI)**](confidence-interval.md)                                   | 根據樣本估計母體參數的範圍，反映 α 所設定的信心水準。                             | 與 z / t 分布有直接關聯   |
| [**t-score vs z-score**](t-z-score.md)                                                    | 決定使用哪種分布來計算臨界值與信賴區間：<br>z 用於已知 σ；t 用於未知 σ。          | 用於 p-value 與 CI 的計算 |
| [**p-value**](p-value.md)                                                                 | 衡量在 H₀ 為真時，觀察到這樣極端結果的機率。與 α 比較以判斷是否拒絕 H₀。          | 與檢定力 (Power) 相對應   |
| [**Power & Effect Size**](power-effect-size.md)                                           | Power = 1 − β，表示在 H₀ 為假時能正確拒絕的機率；<br>效應量則說明「差異有多大」。 | 綜合評估結果的實質意義    |

## Parametric vs Non-parametric Tests

Statistical tests are broadly classified based on the assumptions they make about data distribution:

| Type                     | Description                                                                                                                                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Parametric Tests**     | Assume data follow a specific distribution (usually normal) and rely on parameters like mean and standard deviation. Use when normality and equal variance assumptions are met; generally more powerful when valid. |
| **Non-parametric Tests** | Make minimal distributional assumptions and are suitable for ordinal, skewed, or small-sample data. Use when data violate parametric assumptions; analyze medians or ranks rather than means.                       |

## Choosing the Right Test

### Continuous or Ordinal Data

Used when the dependent variable is **numeric (interval/ratio)** or **ordinal (ordered category)**.

| Scenario                                 | Parametric Test                                                                     | Non-parametric / Exact Alternative                                                                     | Notes                                             |
| ---------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| One group mean vs population mean        | [One-sample t-test / z-test](./t-tests.md#one-sample-t-test)                        | [One-Sample Wilcoxon Signed-Rank Test](./non-parametric-tests.md#one-sample-wilcoxon-signed-rank-test) | z-test if σ known and n ≥ 30; otherwise t-test    |
| Two independent groups (equal variances) | [Independent two-sample t-test](./t-tests.md#two-sample-t-test-independent-samples) | [Mann–Whitney U](./non-parametric-tests.md#mannwhitney-u-test-wilcoxonmannwhitney)                     | Use Welch’s t-test if variances unequal           |
| Two related groups (paired data)         | [Paired t-test](./t-tests.md#paired-sample-t-test-dependent-samples)                | [Wilcoxon signed-rank](./non-parametric-tests.md#wilcoxon-signed-rank-test)                            | Example: before–after measurements                |
| ≥ 3 independent groups                   | [One-way ANOVA](./anova.md)                                                         | [Kruskal–Wallis](./non-parametric-tests.md#kruskalwallis-test)                                         | Post-hoc tests (Tukey, Bonferroni) if significant |
| Two factors (with interaction)           | [Two-way ANOVA](./anova.md#two-way-anova-factorial-anova)                           | Aligned Rank Transform ANOVA (ART ANOVA) / PERMANOVA                                                   | Report effect sizes (η², η²ₚ)                     |

### Categorical or Count Data

Used when the dependent variable is **categorical (nominal)** or represents **counts or proportions**.  
Tests are based on binomial or multinomial distributions — no assumption of normality.

| Scenario                                                  | Common Test                                                                                                                                   | Type                  |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| One group proportion                                      | [Exact Binomial Test](./exact-test.md#exact-binomial-test) / [One-sample proportion z-test](./proportion-tests.md#one-sample-proportion-test) | Exact / Approximation |
| Two group proportions                                     | [Fisher’s Exact Test](./exact-test.md#fishers-exact-test) / [Two-sample proportion z-test](./proportion-tests.md#two-sample-proportion-test)              | Exact / Approximation |
| Association between two categorical variables (r×c table) | [Chi-square Test of Independence](./chi-square.md#chi-square-test-of-independence) / [Fisher’s Exact Test](./exact-test.md#association-between-two-categorical-variables-rc-table)            | Approximation / Exact |
| Goodness-of-fit (observed vs expected)                    | [Chi-square Goodness-of-Fit](./chi-square.md#chi-square-goodness-of-fit)                                                                      | Approximation         |

Exact vs Approximation

| Type              | Typical Distribution      | Meaning                                                                                | Example Tests                  | Recommended When                  |
| ----------------- | ------------------------- | -------------------------------------------------------------------------------------- | ------------------------------ | --------------------------------- |
| **Exact**         | Binomial / Hypergeometric | Compute the _true probability (p-value)_ using the exact discrete distribution         | Exact Binomial, Fisher’s Exact | Small sample, low expected counts |
| **Approximation** | Normal / Chi-square       | Use a _continuous approximation_ (e.g., normal or chi-square) to estimate the p-value. | Proportion z-test, Chi-square  | Large sample, expected counts ≥ 5 |

## Assumption Tests (diagnostic tests)

Before choosing a statistical test, it’s essential to check whether your data meet **key assumptions** such as `normality` and `equal variances`. These diagnostic tests are not parametric or non-parametric by themselves.

| Assumption                        | Test                                                                   | Purpose                                                               | Recommended Use                             |
| --------------------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------- |
| **Normality**                     | [Shapiro–Wilk test](./normality-tests.md#shapirowilk-test)             | Tests if data come from a normal distribution.                        | General test for small to moderate samples. |
|                                   | [Kolmogorov–Smirnov test](./normality-tests.md#kolmogorovsmirnov-test) | Tests goodness-of-fit to normal distribution.                         | Alternative for larger samples.             |
| **Equal variances (homogeneity)** | [Levene’s test](./variance-tests.md#levenes-test)                      | Tests equality of variances across groups; robust to non-normal data. | General-purpose test.                       |
|                                   | [Bartlett’s test](./variance-tests.md#bartletts-test)                  | Tests equality of variances (assumes normality).                      | Use only for normal data.                   |
|                                   | [Brown–Forsythe test](./variance-tests.md#brownforsythe-test)          | Modified Levene’s using medians; robust to outliers.                  | Best for skewed or heteroscedastic data.    |

**Tip:**

- If normality or equal variance assumptions are violated → use **non-parametric alternatives** (e.g., Mann–Whitney, Kruskal–Wallis, or ART ANOVA).
- For unequal variances in ANOVA → use **Welch’s ANOVA**.

## Critical Notes

- Always check assumptions: normality, independence, equal variance.
- Use non-parametric or exact alternatives for small samples or non-normal data.
- For multiple comparisons, apply corrections (Bonferroni, Tukey).
- For small-sample categorical data, prefer **Exact Binomial** or **Fisher’s Exact Test** over asymptotic z or χ² methods.
