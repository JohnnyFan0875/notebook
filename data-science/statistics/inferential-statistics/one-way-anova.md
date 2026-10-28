[Statistics](../README.md) › [推論統計](README.md) › [ANOVA](anova-overview.md) › 單因子

# 單因子變異數分析 (One-Way ANOVA)

**一個類別因子、三組以上獨立組別、一個數值結果**時，檢定各組平均數是否相等。

| 條件 | 例子 |
| --- | --- |
| 數值結果 | 血壓、表現量、帳單金額 |
| 一個類別因子，≥ 3 個水準 | 藥物 A / B / C、星期幾 |
| 組別獨立 | 每位受試者只出現在一組 |

只有兩組 → t 檢定即可（F = t²）；同一受試者重複量測 → [重複量數 ANOVA](repeated-measures-anova.md)。

**為什麼不直接做很多 t 檢定？** 3 組要做 3 次比較，偽陽性機率累積上升。ANOVA 先控制整體問題的型一錯誤。

## 假設與邏輯

| 假設 | 意義 |
| --- | --- |
| H₀ | μ₁ = μ₂ = … = μₖ |
| H₁ | 至少一個平均數不同 |

把總變異拆成兩部分：

$$
\underbrace{SS_{total}}_{\text{總變異}} = \underbrace{SS_{between}}_{\text{組平均離總平均多遠}} + \underbrace{SS_{within}}_{\text{組內資料多分散}}
$$

| ANOVA 表欄位 | 意義 |
| --- | --- |
| Source: Between / Factor | 組別能解釋的變異 |
| Source: Within / Residual | 組內未解釋的變異 |
| df | 自由度（組間 k−1；組內 N−k） |
| SS | 平方和 (sum of squares) |
| MS | 均方 = SS / df |
| F | MS_between / MS_within |

## Python 範例

```python
import numpy as np
import scipy.stats as stats
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf

tips = sns.load_dataset("tips")

# scipy：只回傳 F 與 p
groups = [g["total_bill"].to_numpy() for _, g in tips.groupby("day", observed=True)]
stats.f_oneway(*groups)

# statsmodels：完整 ANOVA 表
model = smf.ols("total_bill ~ C(day)", data=tips).fit()
anova = sm.stats.anova_lm(model, typ=2)

# 效果量 η² = SS_between / SS_total
eta2 = anova.loc["C(day)", "sum_sq"] / anova["sum_sq"].sum()

# 變異數不等時：Welch's ANOVA
import pingouin as pg
pg.welch_anova(data=tips, dv="total_bill", between="day")
```

| η² | 解讀 |
| --- | --- |
| 0.01 | 小 |
| 0.06 | 中 |
| 0.14 | 大 |

η² 回答「總變異有多少比例由組別解釋」，與顯著性是不同問題。小樣本時 η² 會高估，可改報 ω²，見 [事後檢定與效果量](post-hoc-effect-size.md)。

## 解讀與下一步

| 結果 | 意義 | 下一步 |
| --- | --- | --- |
| p < 0.05，變異數相近 | 至少一組不同 | Tukey HSD |
| p < 0.05，變異數不等 | 同上 | Welch's ANOVA + Games-Howell |
| p ≥ 0.05 | 證據不足（**不是**證明相等） | 討論檢定力與不確定性 |
| 嚴重非常態 / Ordinal | — | [Kruskal-Wallis](../nonparametric-methods/kruskal-wallis.md) |

## 報告範本

```text
單因子 ANOVA 顯示平均帳單金額在不同星期有差異，
F(3, 240) = 3.45，p = .018，η² = .041。
Tukey 事後檢定顯示星期六高於星期四，其餘兩兩比較未達顯著。
```
