[Data Science](../README.md) › [Python Foundations](README.md) › scipy.stats 速查

# scipy.stats 速查 (scipy.stats Cheat Sheet)

Python 做統計時的三層工具：`numpy` 產生亂數與基本摘要、`scipy.stats` 提供機率分配與單一檢定、`statsmodels` 做模型（迴歸、GLM、混合效應）與多重檢定。這篇是 API 對照表；方法本身怎麼選、怎麼解讀見 [統計方法速查](../statistics/method-selection.md)。

| 需要 | 用 | R 對應 |
| --- | --- | --- |
| 亂數 | `np.random.default_rng(seed)` | `set.seed()` + `rnorm()` 等 |
| 機率分配（密度、累積、分位數） | `scipy.stats.<dist>` | `dnorm` / `pnorm` / `qnorm` / `rnorm` |
| 單一檢定（t、Wilcoxon、卡方…） | `scipy.stats` | `t.test`、`wilcox.test`、`chisq.test` |
| 迴歸、GLM、ANOVA 表、混合模型 | `statsmodels`（formula：`smf.ols("y ~ x", df)`） | `lm`、`glm`、`lme4` |
| 多重檢定校正 | `scipy.stats.false_discovery_control`、`statsmodels.stats.multitest` | `p.adjust` |
| 預測模型 | `scikit-learn` | `tidymodels` |

statsmodels 的用法見 [statsmodels](../machine-learning/packages/statsmodels/README.md)；scikit-learn 見 [scikit-learn](../machine-learning/packages/scikit-learn/README.md)。

## 亂數：`default_rng`

```python
import numpy as np

rng = np.random.default_rng(42)          # 新 API：獨立的 Generator 物件
rng.normal(loc=0, scale=1, size=5)
rng.integers(0, 10, size=3)              # 不含上界
rng.choice(["A", "B"], size=10, p=[0.7, 0.3])
rng.permutation(10)
rng.binomial(n=10, p=0.5, size=5)
rng.poisson(lam=3, size=5)
```

| 舊寫法（legacy） | 新寫法 |
| --- | --- |
| `np.random.seed(0)` + `np.random.rand(3)` | `rng = np.random.default_rng(0)`；`rng.random(3)` |
| `np.random.randn(3)` | `rng.standard_normal(3)` |
| `np.random.randint(0, 10)` | `rng.integers(0, 10)` |
| `np.random.normal(...)` | `rng.normal(...)` |

> 新 API 不共用全域狀態：把 `rng` 當參數傳進函式，結果可重現、平行時也不會互相干擾（見 [平行運算](performance-and-scaling/parallel.md#常見陷阱)）。NumPy 隨機抽樣的完整用法見 [NumPy 隨機與統計](numpy/random-and-statistics.md)。

## 機率分配

每個分配都是同一組方法，參數名稱依分配而不同（`loc`、`scale` 為位置與尺度）。

| 方法 | 意義 | R | 例子（標準常態） |
| --- | --- | --- | --- |
| `pdf(x)` / `pmf(k)` | 密度 / 機率質量 | `d*` | `norm.pdf(0)` → 0.399 |
| `cdf(x)` | P(X ≤ x) | `p*` | `norm.cdf(1.96)` → 0.975 |
| `sf(x)` | P(X > x) = 1 − cdf，尾端更精確 | `p*(lower.tail=FALSE)` | `norm.sf(1.96) * 2` → 0.05（雙尾 p） |
| `ppf(q)` | 分位數（cdf 的反函數） | `q*` | `norm.ppf(0.975)` → 1.96 |
| `isf(q)` | 上尾分位數 | | |
| `rvs(size, random_state=rng)` | 抽樣 | `r*` | |
| `mean()`、`var()`、`interval(0.95)` | 動差、中央區間 | | |
| `fit(data)` | 以 MLE 估計參數 | `MASS::fitdistr` | |

```python
from scipy import stats

stats.norm.cdf(1.96)                     # 0.975
stats.norm.ppf(0.975)                    # 1.96
stats.t.ppf(0.975, df=9)                 # 2.262：小樣本的 95% CI 臨界值
stats.binom.pmf(3, n=10, p=0.5)          # 0.117：恰好 3 次
stats.binom.cdf(3, n=10, p=0.5)          # 0.172：最多 3 次
stats.poisson.sf(4, mu=2)                # 0.053：P(X ≥ 5)；離散分配 sf(k) 是 P(X > k)
stats.norm.rvs(size=3, random_state=rng) # 用自己的 Generator 抽樣

dist = stats.norm(loc=10, scale=2)       # 「凍結」參數，之後不用重複傳
dist.cdf(12), dist.interval(0.95)
```

| 分配 | scipy | 參數 | 生資常見用途 |
| --- | --- | --- | --- |
| 常態 | `norm` | `loc`=μ、`scale`=σ | log 表現量、z 分數 |
| t | `t` | `df` | 小樣本平均數 |
| 卡方 | `chi2` | `df` | 適合度、列聯表 |
| F | `f` | `dfn`、`dfd` | ANOVA |
| 二項 | `binom` | `n`、`p` | 等位基因比例、成功次數 |
| Poisson | `poisson` | `mu` | 計數（無過度離散時） |
| 負二項 | `nbinom` | `n`、`p`（注意與 DESeq2 的 μ、α 參數化不同） | RNA-seq 計數 |
| 超幾何 | `hypergeom` | `M`、`n`、`N` | 基因集富集（Fisher 單尾） |
| Beta | `beta` | `a`、`b` | 比例的先驗、甲基化 β 值 |
| Gamma / 指數 | `gamma` / `expon` | `a`、`scale` | 等待時間、存活 |

各分配的性質見 [離散分配](../statistics/probability-and-distributions/discrete-distributions.md)、[連續分配](../statistics/probability-and-distributions/continuous-distributions.md)。

```python
# 富集分析：20000 個基因中 200 個屬於某 pathway；50 個差異表現基因裡有 5 個落在 pathway
stats.hypergeom.sf(4, M=20000, n=200, N=50)   # P(重疊 ≥ 5) ≈ 1.4e-4（期望只有 0.5 個）
```

## 檢定對照

所有檢定回傳結果物件，取 `.statistic`、`.pvalue`；多數還有 `.confidence_interval()` 或 `.df`。

| 問題 | scipy.stats | R | 筆記 |
| --- | --- | --- | --- |
| 兩組平均（獨立） | `ttest_ind(a, b, equal_var=False)`（Welch） | `t.test(a, b)` | [統計檢定](../statistics/inferential-statistics/statistical-tests.md) |
| 配對 / 前後測 | `ttest_rel(a, b)` | `t.test(a, b, paired=TRUE)` | 同上 |
| 單一樣本 vs 已知值 | `ttest_1samp(a, popmean=0)` | `t.test(a, mu=0)` | 同上 |
| 兩組（無母數） | `mannwhitneyu(a, b)` | `wilcox.test(a, b)` | [兩獨立樣本](../statistics/nonparametric-methods/two-independent-samples.md) |
| 配對（無母數） | `wilcoxon(a, b)` | `wilcox.test(a, b, paired=TRUE)` | [單樣本與配對](../statistics/nonparametric-methods/one-sample-and-paired.md) |
| 3+ 組 | `f_oneway(a, b, c)` | `aov()` / `oneway.test()` | [單因子 ANOVA](../statistics/inferential-statistics/one-way-anova.md) |
| 3+ 組（無母數） | `kruskal(a, b, c)` | `kruskal.test()` | [Kruskal-Wallis](../statistics/nonparametric-methods/kruskal-wallis.md) |
| 事後比較 | `tukey_hsd(a, b, c)` | `TukeyHSD()` | [事後檢定](../statistics/inferential-statistics/post-hoc-effect-size.md) |
| 列聯表 | `chi2_contingency(table)` | `chisq.test()` | [卡方檢定](../statistics/nonparametric-methods/chi-square.md) |
| 2×2 小樣本 | `fisher_exact(table)` | `fisher.test()` | 同上 |
| 相關 | `pearsonr`、`spearmanr`、`kendalltau` | `cor.test(method=)` | [等級相關](../statistics/nonparametric-methods/rank-correlation.md) |
| 常態性 | `shapiro(x)`；圖：`probplot` | `shapiro.test()` | [假設檢查](../statistics/inferential-statistics/assumption-checks.md) |
| 變異數同質 | `levene(a, b)` | `car::leveneTest()` | 同上 |
| 兩分配是否相同 | `ks_2samp(a, b)` | `ks.test()` | |
| 多重檢定 (BH-FDR) | `false_discovery_control(p)` | `p.adjust(p, "BH")` | [多重檢定](../statistics/inferential-statistics/multiple-testing.md) |
| Bootstrap CI | `bootstrap((x,), np.mean, rng=rng)` | `boot::boot()` | [蒙地卡羅模擬](../statistics/probability-and-distributions/monte-carlo-simulation.md) |
| 置換檢定 | `permutation_test((a, b), stat, rng=rng)` | `coin` 套件 | 同上 |

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(1)
a = rng.normal(5.0, 1, 20)
b = rng.normal(5.8, 1, 20)

res = stats.ttest_ind(a, b, equal_var=False)   # Welch t：預設應該用這個
res.statistic, res.pvalue, res.df
res.confidence_interval(0.95)                  # 平均差的 CI

stats.mannwhitneyu(a, b, alternative="two-sided").pvalue

table = [[8, 2], [1, 5]]
stats.fisher_exact(table)                      # 勝算比與 p 值
chi = stats.chi2_contingency([[10, 20], [30, 25]])   # 2×2 預設套用 Yates 連續性校正
chi.statistic, chi.pvalue, chi.dof, chi.expected_freq

pvals = np.array([0.01, 0.02, 0.03, 0.04, 0.2])
stats.false_discovery_control(pvals)           # BH 校正後：[0.05, 0.05, 0.05, 0.05, 0.2]

stats.bootstrap((a,), np.mean, confidence_level=0.95, rng=np.random.default_rng(0)).confidence_interval
stats.permutation_test((a, b), lambda x, y: x.mean() - y.mean(), rng=np.random.default_rng(0)).pvalue
```

| 注意 | 說明 |
| --- | --- |
| `ttest_ind` 預設 `equal_var=True`（Student t） | 和 R 的 `t.test` 預設（Welch）不同，**要自己設 `equal_var=False`** |
| `alternative=` | `"two-sided"`（預設）、`"less"`、`"greater"` |
| 缺值 | 多數檢定遇到 `NaN` 會回傳 `nan`；設 `nan_policy="omit"` 或先 `dropna()` |
| 很多基因同時檢定 | 檢定函式多數支援 `axis=`，可對整個矩陣向量化（例如 `ttest_ind(X_ctrl, X_trt, axis=1)`），再做 FDR |
| `chi2_contingency` | 2×2 表預設 `correction=True`（Yates），與手算結果不同時檢查這個 |
| 隨機方法的參數 | 新版 scipy 用 `rng=`；舊版用 `random_state=` |

> RNA-seq 的差異表現不要對每個基因做 t 檢定：計數資料、小樣本、過度離散，應用 DESeq2 / edgeR（負二項 GLM）或 Python 的 PyDESeq2，見 [GLM 與計數模型](../statistics/regression-analysis/glm-count-models.md)。

## 描述統計

```python
stats.describe(a)                        # n、min/max、mean、variance（ddof=1）、skewness、kurtosis
stats.sem(a)                             # 標準誤
stats.zscore(a)                          # 標準化（預設 ddof=0）
stats.iqr(a)
stats.median_abs_deviation(a, scale="normal")
stats.trim_mean(a, 0.1)                  # 截尾平均
stats.gmean(a), stats.hmean(a)           # 幾何 / 調和平均
stats.rankdata(a)                        # 排名（同分取平均）
```

這些量的意義與選擇見 [單變數：數值型](../statistics/descriptive-statistics/univariate-numerical.md)。
