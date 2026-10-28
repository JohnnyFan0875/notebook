[Statistics](../README.md) › [推論統計](README.md) › 常用檢定

# 常用統計檢定 (Common Statistical Tests)

選檢定通常取決於四件事：**結果變數型態、組數、獨立或配對、假設是否合理**。最常出錯的是「獨立 vs 配對」。

## 選擇流程

```
結果變數是？
├─ 數值
│   ├─ 1 組 vs 已知值 ────────── 單一樣本 t        （不符假設 → Wilcoxon signed-rank）
│   ├─ 2 組獨立 ─────────────── Welch t          （→ Mann-Whitney U）
│   ├─ 2 組配對 / 前後測 ──────── 配對 t           （→ Wilcoxon signed-rank）
│   ├─ 3+ 組獨立 ────────────── 單因子 ANOVA      （→ Kruskal-Wallis）
│   ├─ 3+ 次重複量測 ─────────── 重複量數 ANOVA / 混合模型（→ Friedman）
│   └─ 兩個數值變數的關係 ─────── Pearson 相關檢定  （→ Spearman）
└─ 類別
    ├─ 1 個比例 vs 已知值 ─────── 單一比例 z        （小樣本 → exact binomial）
    ├─ 2 個比例 ─────────────── 兩比例 z          （小樣本 → Fisher's exact）
    ├─ r × c 交叉表 ─────────── 卡方獨立性         （期望次數 < 5 → Fisher's exact）
    └─ 配對的二元結果 ─────────── McNemar
```

無母數替代方法見 [無母數方法](../nonparametric-methods/README.md)；卡方與 Fisher 的細節見 [卡方檢定](../nonparametric-methods/chi-square.md)。

> **母數 vs 無母數不是「Shapiro 沒過就換」**。目標是平均數差異且資料大致連續 → 母數方法；目標是中位數 / 排名、資料為 Ordinal 或嚴重偏態 → 無母數；小樣本二元結果 → exact test。中大樣本下 t 檢定對輕微非常態相當穩健。

## t 檢定

| 檢定 | 問題 | H₀ | 統計量 | Python |
| --- | --- | --- | --- | --- |
| 單一樣本 (one-sample) | 平均數 = 某值？ | μ = μ₀ | $\frac{\bar{x}-\mu_0}{s/\sqrt{n}}$ | `ttest_1samp(x, mu0)` |
| 獨立樣本 (independent, **Welch**) | 兩組平均數不同？ | μ₁ = μ₂ | $\frac{\bar{x}_1-\bar{x}_2}{\sqrt{s_1^2/n_1+s_2^2/n_2}}$ | `ttest_ind(a, b, equal_var=False)` |
| 配對 (paired) | 配對差異的平均 ≠ 0？ | μ_d = 0 | $\frac{\bar{d}}{s_d/\sqrt{n}}$ | `ttest_rel(before, after)` |

**假設**：連續資料、觀測獨立（配對時是「配對之間」獨立）、近似常態或 n 夠大。

> - **預設用 Welch**（`equal_var=False`）：變異數不等時仍正確，變異數相等時幾乎不損失檢定力。Student's t（假設等變異）不建議當預設。
> - **配對 t = 對差值做單一樣本 t**。前後測資料若用獨立 t，會丟掉個體內配對資訊，大幅降低檢定力。

```python
import numpy as np
from scipy import stats

# 單一樣本
stats.ttest_1samp(x, popmean=5.5)

# 獨立兩組（Welch）+ 平均差的 95% CI
res = stats.ttest_ind(setosa, versicolor, equal_var=False)
res.statistic, res.pvalue, res.confidence_interval(0.95)   # scipy ≥ 1.11

# 配對：例如同一批病人服藥前後血壓
before = np.array([140, 138, 145, 150, 142, 137, 148, 153, 141, 139])
after  = np.array([130, 132, 138, 145, 136, 130, 140, 148, 135, 133])
stats.ttest_rel(before, after)
d_paired = (before - after).mean() / (before - after).std(ddof=1)   # 配對 Cohen's d
```

## 比例檢定

條件：$n\hat p \ge 5$（或 10）且 $n(1-\hat p) \ge 5$，否則用 exact test。看比例時也要看**實際次數**：20 人的 10% 與 20,000 人的 10% 完全不同。

| 檢定 | 問題 | Python |
| --- | --- | --- |
| 單一比例 z | π = π₀？ | `proportions_ztest(count, nobs, value=pi0)` |
| 兩比例 z（[A/B 測試](../experimental-design/ab-testing.md)） | π₁ = π₂？ | `proportions_ztest([x1, x2], [n1, n2])` |
| Exact binomial | 小樣本的 π = π₀？ | `binomtest(k, n, p)` |
| Fisher's exact | 小樣本 2×2 | `fisher_exact(table)` |

```python
from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import binomtest, fisher_exact

proportions_ztest(count=82, nobs=200, value=0.30)                 # 單一比例
proportions_ztest(count=[62, 45], nobs=[200, 200])                # 兩比例
binomtest(k=3, n=12, p=0.5).pvalue                                # exact binomial
fisher_exact([[8, 2], [1, 9]])                                    # (odds ratio, p)
```

## 相關檢定

H₀：ρ = 0。`stats.pearsonr(a, b)` 與 `stats.spearmanr(a, b)` 直接回傳係數與 p 值，見 [雙變數分析](../descriptive-statistics/bivariate.md#數值--數值相關係數-correlation)。

## 卡方檢定（快速版）

```python
import pandas as pd
from scipy import stats

ct = pd.crosstab(df["group"], df["outcome"])
chi2, p, dof, expected = stats.chi2_contingency(ct)          # 獨立性檢定；務必檢查 expected ≥ 5
cramers_v = np.sqrt(chi2 / (ct.values.sum() * (min(ct.shape) - 1)))   # 效果量

stats.chisquare(f_obs=[11, 9, 10, 12, 8, 10])                 # 適合度：骰子公平嗎？
```

## 比較三組以上：ANOVA

ANOVA 只告訴你「**至少有一組**不同」，顯著後還要做 [事後檢定](post-hoc-effect-size.md) 才知道是哪幾組。

| 情境 | 方法 |
| --- | --- |
| 一個因子、3+ 獨立組 | [單因子 ANOVA](one-way-anova.md) |
| 兩個因子 | [二因子 ANOVA](two-way-anova.md) |
| 同一受試者重複量測 | [重複量數 ANOVA](repeated-measures-anova.md) / [混合效應模型](../regression-analysis/mixed-effects-models.md) |
| 變異數不等 | Welch's ANOVA |
| 嚴重非常態 | Kruskal-Wallis |

## 檢定其實都是線性模型

很多檢定都是 [線性迴歸](../regression-analysis/README.md) 的特例，理解這點有助於延伸到更複雜的設計（加共變數、批次效應）：

| 檢定 | 等價的模型 |
| --- | --- |
| 單一樣本 t | `y ~ 1`（檢定截距） |
| 兩樣本 t（Student） | `y ~ group`（檢定 group 係數） |
| 單因子 ANOVA | `y ~ C(group)`（F 檢定） |
| 二因子 ANOVA | `y ~ A * B` |
| ANCOVA | `y ~ group + covariate` |
| Pearson 相關 | `y ~ x`（標準化後斜率 = r） |
| 卡方 / 比例檢定 | Logistic / Poisson 迴歸 |

```python
import statsmodels.formula.api as smf
smf.ols("value ~ group", data=df).fit().summary()   # group 係數的 t 與 p 值 = Student's t 檢定
```

## 總表

| 檢定 | H₀ | 組數 | 主要假設 | 效果量 |
| --- | --- | --- | --- | --- |
| 單一樣本 t | μ = μ₀ | 1 | 近似常態或 n 大 | Cohen's d |
| Welch t | μ₁ = μ₂ | 2 | 獨立、近似常態 | Cohen's d |
| 配對 t | μ_d = 0 | 2（配對） | 差值近似常態 | Cohen's d（配對） |
| 單因子 ANOVA | μ₁ = … = μₖ | 3+ | 常態、等變異 | η² |
| 兩比例 z | π₁ = π₂ | 2 | 期望次數夠 | 比例差、RR、OR |
| 卡方獨立性 | 無關聯 | r × c | 期望次數 ≥ 5 | Cramér's V |
| Fisher's exact | 無關聯 | 2 × 2 | 小樣本皆可 | Odds ratio |

## 報告清單

1. H₀ 與 H₁
2. 選用的檢定與理由（為什麼符合研究設計）
3. 檢定統計量與自由度
4. p 值（多重檢定時報告校正後的值，見 [多重檢定校正](multiple-testing.md)）
5. 效果量與信賴區間
6. 假設檢查結果與任何校正
