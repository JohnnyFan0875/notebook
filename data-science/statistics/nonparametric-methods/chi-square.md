[Statistics](../README.md) › [無母數方法](README.md) › 卡方檢定

# 類別關聯：卡方檢定與 Fisher's Exact Test

卡方檢定直接處理**次數 (counts)**，檢驗類別變數之間的關係。它不建模連續變數的平均與變異，但仍有結構上的假設：觀測獨立、期望次數足夠。

| 檢定 | 問題 | 資料 |
| --- | --- | --- |
| 獨立性檢定 (test of independence) | 兩個類別變數有關聯嗎？ | 交叉表 |
| 同質性檢定 (test of homogeneity) | 多個母體的類別分配相同嗎？ | 交叉表（公式同上，差在研究設計） |
| 適合度檢定 (goodness of fit) | 觀察次數符合期望分配嗎？ | 一個類別變數 + 期望比例 |
| Fisher's exact test | 小樣本 2×2 的關聯 | 2×2 表 |
| McNemar's test | **配對**的二元結果（同一人前後測） | 配對 2×2 表 |

## 獨立性檢定

1. 建交叉表，得觀察次數 O
2. 假設獨立，計算期望次數：$E_{ij} = \dfrac{\text{列總和}_i \times \text{欄總和}_j}{N}$
3. $\chi^2 = \sum \dfrac{(O_{ij}-E_{ij})^2}{E_{ij}}$，df = (列數 − 1)(欄數 − 1)

觀察與期望差越多 → χ² 越大 → 越有關聯的證據。

```python
import numpy as np
import pandas as pd
from scipy import stats

ct = pd.crosstab(df["genotype"], df["phenotype"])
chi2, p, dof, expected = stats.chi2_contingency(ct)   # 2×2 預設有 Yates 連續性校正

# 檢查期望次數
(expected < 5).sum(), expected.min()

# 效果量 Cramér's V
n = ct.values.sum()
cramers_v = np.sqrt(chi2 / (n * (min(ct.shape) - 1)))

# 哪幾格造成關聯？標準化殘差 |r| > 2 值得注意
std_resid = (ct - expected) / np.sqrt(expected)
```

| Cramér's V | 關聯強度（依表格大小調整） |
| --- | --- |
| 0.1–0.3 | 弱 |
| 0.3–0.5 | 中 |
| > 0.5 | 強 |

## 假設與替代方案

| 假設 | 準則 |
| --- | --- |
| 觀測獨立 | 每個個體只出現在一格 |
| 期望次數 | ≥ 80% 的格子 E ≥ 5，且沒有任何格子 E < 1 |

| 情況 | 建議 |
| --- | --- |
| 2×2，期望次數都 ≥ 5 | 卡方 |
| 2×2，有格子期望次數 < 5 | **Fisher's exact test** |
| 較大表格，很多格子 < 5 | 合併類別，或用模擬 p 值（R：`fisher.test(tab, simulate.p.value = TRUE)`） |
| 配對資料 | McNemar |
| 分層的 2×2 表（例如各醫院分別一張） | Cochran-Mantel-Haenszel 檢定 |

```python
from scipy.stats import fisher_exact
from statsmodels.stats.contingency_tables import mcnemar

fisher_exact([[8, 2], [1, 9]])                          # (odds ratio, p)
# 富集分析（單尾）：列 = 在 / 不在基因清單，欄 = 在 / 不在 pathway
fisher_exact([[k, n - k], [K - k, N - K - n + k]], alternative="greater")
mcnemar([[30, 5], [15, 50]], exact=True).pvalue         # 配對二元資料
```

> Fisher's exact test 使用超幾何分配精確計算 p 值，不只是「小樣本版卡方」。單尾 Fisher 就是 GO / pathway [富集分析](../probability-and-distributions/discrete-distributions.md#超幾何分配-hypergeometric) 的標準做法。

## 適合度檢定

```python
observed = np.array([8, 10, 12, 9, 11, 10])                 # 骰子 60 次
stats.chisquare(observed)                                   # 預設期望為均等

observed = np.array([45, 30, 25])
stats.chisquare(observed, f_exp=np.array([0.5, 0.3, 0.2]) * observed.sum())   # 自訂期望比例
```

df = 類別數 − 1（若期望比例中有參數由資料估計，每估一個再減 1）。

> **遺傳學應用**：檢查 Hardy-Weinberg 平衡、孟德爾分離比（3:1、9:3:3:1）都是適合度檢定。

## 視覺化

```python
import seaborn as sns
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
sns.heatmap(ct, annot=True, fmt="d", cmap="Blues", ax=ax[0])                  # 觀察次數
sns.heatmap(std_resid, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax[1])  # 標準化殘差
plt.show()

pd.crosstab(df["genotype"], df["phenotype"], normalize="index").plot(kind="bar")   # 列比例長條圖
```
