[Machine Learning](../../README.md) › [套件](../README.md) › [statsmodels](README.md) › ANOVA

# statsmodels：ANOVA

檢定兩組以上的平均是否不同。statsmodels 的做法是先用 `ols` 配適線性模型，再用 `anova_lm` 產生 ANOVA 表。觀念、假設與事後檢定見 [單因子 ANOVA](../../../statistics/inferential-statistics/one-way-anova.md)、[雙因子 ANOVA](../../../statistics/inferential-statistics/two-way-anova.md)、[事後檢定與效果量](../../../statistics/inferential-statistics/post-hoc-effect-size.md)。

## 用法

```python
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# 1. 單因子
df = pd.DataFrame({"score": [5, 6, 7, 8, 5, 6, 7, 6, 7],
                   "group": list("AAABBBCCC")})
anova_lm(smf.ols("score ~ C(group)", data=df).fit(), typ=2)
#           sum_sq  df     F  PR(>F)
# C(group)   0.667   2  0.27    0.77     ← 三組平均沒有顯著差異
# Residual   7.333   6

# 2. 事後兩兩比較（ANOVA 顯著時才看）
print(pairwise_tukeyhsd(df["score"], df["group"], alpha=0.05))

# 3. 雙因子 + 交互作用
df2 = pd.DataFrame({"score": [5, 6, 7, 8, 6, 7, 9, 5, 6, 8, 7, 9],
                    "treatment": list("AAAABBBBCCCC"),
                    "gender": list("MFMFMFMFMFMF")})
anova_lm(smf.ols("score ~ C(treatment) * C(gender)", data=df2).fit(), typ=2)

# 4. ANCOVA：控制連續共變量
df3 = pd.DataFrame({"score": [10, 12, 13, 15, 14, 16, 17, 18],
                    "treatment": list("AABBCCCC"),
                    "age": [23, 25, 22, 30, 28, 26, 29, 31]})
anova_lm(smf.ols("score ~ C(treatment) + age", data=df3).fit(), typ=2)
```

## 平方和類型

| `typ` | 計算方式 | 何時用 |
| --- | --- | --- |
| 1（序列） | 依公式順序逐一加入 | 有明確的加入順序；**不平衡設計時結果依順序而變** |
| 2 | 每個主效果在調整其他主效果後的貢獻 | **無交互作用時的好預設**；不平衡設計 |
| 3 | 每項在調整所有其他項（含交互作用）後的貢獻 | 有交互作用且想檢定主效果；SPSS / SAS 預設 |

> Type III 必須搭配**總和為零的對比編碼**，否則主效果的檢定沒有意義：
>
> ```python
> anova_lm(smf.ols("score ~ C(treatment, Sum) * C(gender, Sum)", data=df2).fit(), typ=3)
> ```
>
> 平衡設計（每格樣本數相同）時三種類型的結果相同；上面的 `df2` 就是平衡設計。

## 假設與替代

| 假設 | 檢查 | 不成立時 |
| --- | --- | --- |
| 殘差近似常態 | Q–Q 圖、Shapiro-Wilk | 樣本夠大時穩健；否則 [Kruskal-Wallis](../../../statistics/nonparametric-methods/kruskal-wallis.md) |
| 各組變異相等 | Levene 檢定 | Welch ANOVA（`pingouin.welch_anova`）、Games-Howell 事後檢定 |
| 觀測獨立 | 研究設計 | 重複量測 → [混合效應模型](../../../statistics/regression-analysis/mixed-effects-models.md) |

> 範例資料只有 6–12 筆，用來示範語法；結果都不顯著（p > 0.1）。實際分析前先做 [樣本數與檢定力](../../../statistics/experimental-design/sample-size-power.md) 規劃。
