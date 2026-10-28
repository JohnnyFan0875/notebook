[Statistics](../README.md) › [推論統計](README.md) › [ANOVA](anova-overview.md) › 事後檢定與效果量

# 事後檢定與效果量 (Post-hoc Tests & Effect Size)

ANOVA 顯著只說明「某處有差異」。接下來要回答兩個獨立的問題：**哪幾組不同？差異大到有意義嗎？**

## 事後檢定 (Post-hoc Tests)

| 方法 | 何時用 |
| --- | --- |
| **Tukey HSD** | 單因子 ANOVA 後的預設，變異數相近 |
| **Games-Howell** | 變異數或樣本數不等 |
| Dunnett | 每組只跟**一個對照組**比較 |
| Holm / Bonferroni | 少數事先計畫的比較 |
| BH (FDR) | 大量探索性比較 |

各校正方法的原理見 [多重檢定校正](multiple-testing.md)。

> 「事後」不代表「可有可無」。若研究問題就是特定組間差異，兩兩比較本身就是答案的一部分。

```python
import seaborn as sns
import pingouin as pg
from statsmodels.stats.multicomp import pairwise_tukeyhsd

tips = sns.load_dataset("tips")

pairwise_tukeyhsd(endog=tips["total_bill"], groups=tips["day"], alpha=0.05)   # Tukey HSD
pg.pairwise_gameshowell(data=tips, dv="total_bill", between="day")            # Games-Howell
```

| Tukey 表欄位 | 意義 |
| --- | --- |
| `meandiff` | 兩組平均差 |
| `p-adj` | 校正後 p 值 |
| `lower`, `upper` | 差值的**同時信賴區間 (simultaneous CI)**，通常是最有資訊量的欄位 |
| `reject` | 是否顯著 |

## 效果量 (Effect Size)

| 指標 | 公式 | 用於 | 特性 |
| --- | --- | --- | --- |
| η² (eta squared) | SS_between / SS_total | 單因子 ANOVA | 好解釋：組別解釋的變異比例；小樣本會高估 |
| partial η² | SS_effect / (SS_effect + SS_error) | 二因子、重複量數 | 每個效果相對於自己的誤差項 |
| ω² (omega squared) | 偏誤校正版 η² | 單因子，小樣本 | 較不高估 |
| Cohen's d | 兩組平均差 / pooled SD | **兩兩比較** | 描述特定對比的大小 |

| 大小 | η² / partial η² | Cohen's d |
| --- | --- | --- |
| 小 | 0.01 | 0.2 |
| 中 | 0.06 | 0.5 |
| 大 | 0.14 | 0.8 |

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf

anova = sm.stats.anova_lm(smf.ols("total_bill ~ C(day)", data=tips).fit(), typ=2)

ss_b, df_b = anova.loc["C(day)", ["sum_sq", "df"]]
ss_w, df_w = anova.loc["Residual", ["sum_sq", "df"]]
ms_w = ss_w / df_w

eta2   = ss_b / (ss_b + ss_w)
omega2 = (ss_b - df_b * ms_w) / (ss_b + ss_w + ms_w)

# 兩兩比較的 Cohen's d
sat = tips.loc[tips["day"] == "Sat", "total_bill"]
thu = tips.loc[tips["day"] == "Thur", "total_bill"]
pg.compute_effsize(sat, thu, eftype="cohen")
```

> 整體效果量（η²）描述整個組別結構；Cohen's d 描述特定一對的差異。兩者回答不同問題，重要的對比兩者都報。

## 報告範本

```text
單因子 ANOVA 顯示平均帳單金額依星期而異，F(3, 240) = 3.45，p = .018，η² = .041，ω² = .028。
Tukey HSD 顯示星期六高於星期四（平均差 = 3.21，95% CI [0.44, 5.98]，p-adj = .016，d = 0.42），
其餘兩兩比較未達顯著。
```

## 常見錯誤

| 錯誤 | 修正 |
| --- | --- |
| ANOVA 顯著就停止 | 做事後檢定 |
| 只報 p 值 | 加上效果量與差值的 CI |
| 很多 t 檢定不校正 | Tukey、Holm、Bonferroni |
| 忽略變異數不等 | Welch's ANOVA + Games-Howell |
| 只報整體 η² | 重要對比加報 Cohen's d |
