[Statistics](../README.md) › [無母數方法](README.md) › 單一樣本與配對

# 單一樣本與配對檢定 (One-Sample & Paired Tests)

| 母數方法 | 無母數替代 |
| --- | --- |
| 單一樣本 t 檢定 | Sign test、Wilcoxon signed-rank |
| 配對 t 檢定 | Wilcoxon signed-rank |

## 兩種檢定比較

| | 符號檢定 (Sign Test) | Wilcoxon 符號等級檢定 (Signed-Rank Test) |
| --- | --- | --- |
| 使用的資訊 | 只有差值的**方向**（+ / −） | 方向 + **大小**（差值絕對值的排名） |
| 假設 | 幾乎沒有 | 差值大致**對稱** |
| 檢定力 | 低 | 高 |
| 何時用 | 只有方向可信（量測很粗糙、大量同分） | **預設選擇** |
| H₀ | 中位數 = M₀ | 差值分配對稱於 0（對稱時 = 中位數為 M₀） |

**符號檢定**：去掉 0 差值後，正號個數在 H₀ 下服從 Binomial(n, 0.5)。

**Wilcoxon signed-rank**：

1. 算差值 dᵢ = xᵢ − M₀（配對時 dᵢ = xᵢ − yᵢ），去掉 0
2. 對 |dᵢ| 排名，再加回原本的正負號
3. W⁺ = 正號排名和、W⁻ = 負號排名和；W = min(W⁺, W⁻)
4. W 很小 → 差值系統性地偏向某一方向

## Python 範例

```python
import numpy as np
from scipy import stats
import pingouin as pg

# 單一樣本：中位數是否為 80？
data = np.array([85, 92, 78, 95, 88, 70, 91, 84, 76, 89])
M0 = 80

d = data - M0
stats.binomtest((d > 0).sum(), n=(d != 0).sum(), p=0.5).pvalue   # 符號檢定
stats.wilcoxon(d)                                                 # Wilcoxon signed-rank

# 配對：治療前後
before = np.array([72, 68, 75, 80, 65, 71, 78, 69, 74, 70])
after  = np.array([78, 72, 80, 85, 70, 74, 82, 75, 79, 76])
stats.wilcoxon(before, after)

# 含效果量（matched-pairs rank-biserial correlation, RBC）
pg.wilcoxon(before, after)
```

| 效果量 \|r\| | 解讀 |
| --- | --- |
| 0.1–0.3 | 小 |
| 0.3–0.5 | 中 |
| > 0.5 | 大 |

## 視覺化配對資料

重點是呈現**每一對**的變化方向與大小。

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 2, figsize=(12, 4))
for b, a in zip(before, after):                       # 左：配對連線圖（spaghetti plot）
    ax[0].plot([0, 1], [b, a], color="steelblue" if a > b else "tomato", alpha=0.6)
ax[0].set_xticks([0, 1], ["Before", "After"])

ax[1].hist(after - before, bins=8, edgecolor="white")  # 右：差值分布，看是否對稱
ax[1].axvline(0, color="red", ls="--")
plt.show()
```

> 配對檢定處理的是「同一對之內」的相依性，**不同對之間仍需獨立**。
