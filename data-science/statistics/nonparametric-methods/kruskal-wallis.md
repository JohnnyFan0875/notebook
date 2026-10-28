[Statistics](../README.md) › [無母數方法](README.md) › Kruskal-Wallis

# 多組比較：Kruskal-Wallis 與 Friedman

| 設計 | 母數方法 | 無母數替代 | 事後檢定 |
| --- | --- | --- | --- |
| 3+ 組**獨立** | 單因子 ANOVA | **Kruskal-Wallis** | Dunn's test |
| 3+ 次**重複量測** | 重複量數 ANOVA | **Friedman** | Nemenyi / Conover |

## Kruskal-Wallis 檢定

Mann-Whitney U 推廣到三組以上：合併排名後，比較各組的排名和。

$$
H = \frac{12}{N(N+1)} \sum_{i=1}^{k} \frac{R_i^2}{n_i} - 3(N+1) \ \sim\ \chi^2_{k-1}\ \ (\text{每組 } n \ge 5)
$$

N = 總樣本數、k = 組數、Rᵢ = 第 i 組的排名和。

- H₀：各組來自相同分配；H₁：至少一組的分配不同
- 解讀為「中位數不同」需假設各組形狀相似，見 [何時使用](when-and-why.md#無母數檢定其實在檢定什麼)
- 顯著只代表「某處不同」，要再做 **Dunn's test**（不要直接做一堆未校正的 Mann-Whitney）

**效果量**：$\eta^2_H = \dfrac{H - k + 1}{N - k}$（小 0.01、中 0.06、大 0.14）

```python
import numpy as np
import pandas as pd
from scipy import stats
import scikit_posthocs as sp          # pip install scikit-posthocs

a = np.array([72, 68, 75, 80, 65, 71, 78])
b = np.array([85, 90, 82, 88, 79, 91, 84])
c = np.array([76, 74, 79, 83, 77, 80, 75])

# 1. 整體檢定
H, p = stats.kruskal(a, b, c)

# 2. 效果量
N, k = len(a) + len(b) + len(c), 3
eta2_h = (H - k + 1) / (N - k)

# 3. 事後檢定（顯著時）：Dunn's test + Holm 校正
df_long = pd.DataFrame({"score": np.r_[a, b, c], "group": ["A"]*7 + ["B"]*7 + ["C"]*7})
sp.posthoc_dunn(df_long, val_col="score", group_col="group", p_adjust="holm")
```

`p_adjust` 可選 `"bonferroni"`、`"holm"`（建議預設）、`"fdr_bh"`，原理見 [多重檢定校正](../inferential-statistics/multiple-testing.md)。

## Friedman 檢定（重複量測）

同一受試者在 3+ 個條件下量測，資料為 Ordinal 或嚴重非常態時使用。在**每位受試者內部**排名，再比較各條件的排名和。

```python
# 寬格式：每列 = 一位受試者，每欄 = 一個條件
stats.friedmanchisquare(df_wide["t1"], df_wide["t2"], df_wide["t3"])

# 事後檢定
sp.posthoc_nemenyi_friedman(df_wide[["t1", "t2", "t3"]].to_numpy())

# pingouin 版（長格式，含效果量 Kendall's W）
import pingouin as pg
pg.friedman(data=df_long_rm, dv="score", within="time", subject="subject")
```

## Kruskal-Wallis vs 單因子 ANOVA

| | 單因子 ANOVA | Kruskal-Wallis |
| --- | --- | --- |
| 假設常態 | 是 | 否 |
| 假設等變異 | 是（Welch 版不需要） | 建議形狀相似 |
| Ordinal 資料 | 不適合 | 適合 |
| 對離群值 | 敏感 | 穩健 |
| 常態時效率 | 100% | 約 95% |
| 事後檢定 | Tukey HSD、Games-Howell | Dunn's test |
| 效果量 | η²、ω² | η²_H |

視覺化同 [兩獨立樣本](two-independent-samples.md)：分組 boxplot + 原始點，或 violin plot。
