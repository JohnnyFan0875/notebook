[Statistics](../README.md) › [推論統計](README.md) › [ANOVA](anova-overview.md) › 重複量數

# 重複量數變異數分析 (Repeated-Measures ANOVA)

**同一受試者**在多個條件或時間點被量測時，比較各條件的平均數。

| 情境 | 例子 |
| --- | --- |
| 同一受試者、多個時間點 | 治療前、第 1 週、第 1 個月 |
| 同一受試者、多個條件 | 安慰劑、低劑量、高劑量 |

只有兩個時間點 → [配對 t 檢定](statistical-tests.md)。

> 重複量測**不獨立**，不能用一般單因子 ANOVA。但這也是優點：每個人都是自己的對照，**個體間差異被移除**，殘差變小、檢定力提高。

變異拆解：

| 來源 | 意義 |
| --- | --- |
| 受試者間 (between-subject) | 人與人之間穩定的差異（被移除） |
| 條件 / 時間 (within-subject) | 想檢定的效果 |
| 殘差 | 剩下的雜訊 |

## 球形假設 (Sphericity)

各條件**兩兩差值的變異數**大致相等（例如 T1−T2、T1−T3、T2−T3 的變異數相近）。違反時 F 檢定過於寬鬆（偽陽性增加）。

- 檢查：Mauchly's test
- 違反時：使用 **Greenhouse-Geisser**（保守）或 Huynh-Feldt 校正後的 p 值
- 只有兩個條件時球形假設必然成立

## Python 範例

```python
import numpy as np
import pandas as pd
import pingouin as pg
import seaborn as sns
import matplotlib.pyplot as plt

# 長格式 (long format)：每列 = 一位受試者在一個條件下的量測
rng = np.random.default_rng(42)
rows = []
for s in range(20):
    base = rng.normal(100, 8)
    for cond, shift in [("baseline", 0), ("week_1", -4), ("month_1", -8)]:
        rows.append({"subject": s, "condition": cond, "score": base + shift + rng.normal(0, 3)})
df = pd.DataFrame(rows)

pg.rm_anova(data=df, dv="score", within="condition", subject="subject",
            detailed=True, correction=True)          # 含 GG 校正 p 值、ng2
pg.sphericity(data=df, dv="score", within="condition", subject="subject")
pg.pairwise_tests(data=df, dv="score", within="condition", subject="subject",
                  padjust="holm")                    # 事後兩兩比較

# 視覺化：每位受試者的軌跡（灰）+ 平均 ± 95% CI（藍）
sns.lineplot(data=df, x="condition", y="score", units="subject", estimator=None, alpha=0.25, color="gray")
sns.pointplot(data=df, x="condition", y="score", errorbar=("ci", 95), color="steelblue")
plt.show()
```

個體軌跡圖能看出平均趨勢是否一致，還是只被少數人帶動。

**效果量**：pingouin 輸出 `np2`（partial η²）或 `ng2`（generalized η²）；generalized η² 較適合跨研究設計比較。

## 何時改用混合效應模型

重複量數 ANOVA 在以下情況很受限，應改用 [線性混合效應模型](../regression-analysis/mixed-effects-models.md)：

| 情況 | 原因 |
| --- | --- |
| 有缺失的量測 | RM-ANOVA 會整個刪除該受試者 |
| 量測時間不規則、各人次數不同 | RM-ANOVA 需要完整的平衡設計 |
| 同時有受試者內與受試者間的預測變數 | 混合模型更有彈性 |
| 想估計每個人的斜率（成長曲線） | 隨機斜率 |

| 其他替代方法 | 情境 |
| --- | --- |
| [Friedman test](../nonparametric-methods/kruskal-wallis.md) | Ordinal 或嚴重非常態的重複資料 |
| GEE | 關心族群平均效果、結果為二元或計數 |

## 報告範本

```text
重複量數 ANOVA 顯示分數在三次回診間有顯著變化，
F(2, 38) = 15.21，p < .001，generalized η² = .24。
分數從 baseline 到第 1 週下降，到第 1 個月進一步下降。Mauchly 檢定未顯示違反球形假設。
```
