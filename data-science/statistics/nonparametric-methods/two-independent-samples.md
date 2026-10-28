[Statistics](../README.md) › [無母數方法](README.md) › 兩獨立樣本

# 兩獨立樣本：Mann-Whitney U 檢定

**Mann-Whitney U**（又稱 Wilcoxon rank-sum test）是獨立樣本 t 檢定的無母數替代。檢定一組的值是否**傾向**大於另一組。

## 原理

1. 把兩組資料**合併後排名**（最小 = 1）
2. 分別加總兩組的排名 R₁、R₂
3. $U_1 = R_1 - \frac{n_1(n_1+1)}{2}$，$U_1 + U_2 = n_1 n_2$
4. 兩組無差異時，排名應平均分布；U 極端代表某組集中在高（或低）排名

> **直覺**：$U_1 / (n_1 n_2)$ = 從 A、B 各隨機抽一個，A > B 的機率 P(A > B)。這個量與 [ROC 曲線的 AUC](../../machine-learning/evaluation/roc-auc.md) 完全相同。

| 假設 | H₀ | H₁ |
| --- | --- | --- |
| 雙尾 | 兩組分配相同 | 分配不同（一組傾向較大） |
| 單尾 | A 不傾向較大 | A 傾向大於 B |

## Python 範例

```python
import numpy as np
import pandas as pd
from scipy import stats
import pingouin as pg

group_a = np.array([72, 68, 75, 80, 65, 71, 78, 69, 74, 70])
group_b = np.array([85, 90, 82, 88, 79, 91, 84, 87, 83, 86])

res = stats.mannwhitneyu(group_a, group_b, alternative="two-sided")
res.statistic, res.pvalue                          # statistic = U₁（第一組）

# 效果量：rank-biserial correlation = 2·U₁/(n₁n₂) − 1，範圍 −1 ~ 1（> 0 表示 A 傾向較大）
rbc = 2 * res.statistic / (len(group_a) * len(group_b)) - 1

pg.mwu(group_a, group_b)                           # 一次給 U、p、RBC、CLES
```

| 效果量 \|r\| | 解讀 |
| --- | --- |
| 0.1–0.3 | 小 |
| 0.3–0.5 | 中 |
| > 0.5 | 大 |

## 假設

| 假設 | 檢查 |
| --- | --- |
| 組內與組間皆獨立 | 研究設計 |
| 至少為 Ordinal | 資料型態 |
| （解讀為中位數差異時）兩組形狀相同 | 畫圖比較 |

> 兩組形狀差很多時（例如一組變異大很多），Mann-Whitney 顯著不代表中位數不同。先畫 boxplot + 原始點或 violin plot。

```python
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({"Score": np.r_[group_a, group_b], "Group": ["A"] * 10 + ["B"] * 10})
sns.boxplot(x="Group", y="Score", data=df)
sns.stripplot(x="Group", y="Score", data=df, color="black", alpha=0.5)
plt.show()
```

## Mann-Whitney U vs t 檢定

| | Welch t 檢定 | Mann-Whitney U |
| --- | --- | --- |
| 假設常態 | 是（或 n 大） | 否 |
| 使用 | 原始值（平均數） | 排名 |
| 對離群值 | 敏感 | 穩健 |
| Ordinal 資料 | 不適合 | 適合 |
| 資料常態時的效率 | 100% | 約 95% |
| 效果量 | Cohen's d | Rank-biserial r |

> 單細胞 RNA-seq 的 marker gene 偵測（如 Seurat `FindMarkers` 預設）就是逐基因做 Wilcoxon rank-sum，再做 [多重檢定校正](../inferential-statistics/multiple-testing.md)。注意此時是把**細胞**當樣本，會有 [假重複](../inferential-statistics/assumption-checks.md#獨立性-independence) 的問題。
