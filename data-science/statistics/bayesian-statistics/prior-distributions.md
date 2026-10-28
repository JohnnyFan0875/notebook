[Statistics](../README.md) › [貝氏統計](README.md) › 先驗分配

# 先驗分配 (Prior Distributions)

先驗 P(θ) 編碼「看資料之前」對參數的所有信念。選先驗本質上是**模型假設**，就像頻率學派假設常態或等變異一樣，應該透明且有理由。

先驗的作用：編碼領域知識（比例必在 0–1）、資料稀少時**正則化**估計、樣本增加後影響變小、讓假設**明確可見**。

## 三種類型

| 類型 | 形狀 | 對後驗的影響 | 何時用 | 例子 |
| --- | --- | --- | --- | --- |
| 資訊性 (informative) | 集中 | n 小時很大 | 有可靠的歷史資料或文獻 | Beta(15, 35)：平均 0.3，等於「已看過 15 成功 35 失敗」 |
| **弱資訊性** (weakly informative) | 寬但有界 | 小，主要排除不合理值 | **多數應用的預設**（Stan / PyMC 社群推薦） | 標準化迴歸係數 ~ N(0, 1) |
| 無資訊 / 平坦 (non-informative / flat) | 常數 | 最小 | 理論工作、需要「客觀」的情境 | Uniform(0, 1) |
| Jeffreys | 依參數化而定 | 對重新參數化不變 | 需要客觀性時 | 比例：Beta(0.5, 0.5) |

> **平坦 ≠ 客觀**：θ 上的平坦先驗，換成 log(θ) 後就不再平坦。

## 依參數範圍選分配族

| 參數 | 範圍 (support) | 常用先驗 |
| --- | --- | --- |
| 機率 / 比例 | [0, 1] | Beta(α, β) |
| 計數率 | [0, ∞) | Gamma(α, β)、Half-Normal |
| 無界實數（迴歸係數、平均） | (−∞, ∞) | Normal(μ, σ)、Student-t |
| 標準差 / 尺度 | (0, ∞) | Half-Normal、Exponential、Half-Cauchy |
| 相關矩陣 | [−1, 1] | LKJ(η) |

不要把機率質量放在不可能的區域（例如負的 σ）。

> **先驗 ↔ 正則化**：迴歸係數放 Normal(0, τ) 先驗的 MAP 估計 = **Ridge**；放 Laplace 先驗 = **Lasso**。τ 越小正則化越強。見 [最大概似估計](../probability-and-distributions/maximum-likelihood.md#mle-與-ml-損失函數的對應)、[ML: Regularization](../../machine-learning/foundations/regularization.md)。
>
> **階層先驗 (hierarchical prior)**：各群組參數共享一個先驗，先驗的參數也從資料估計 → 群組間「借用資訊」。DESeq2 對 dispersion 與 log fold change 的收縮 (shrinkage) 就是這個概念（empirical Bayes）。

## 先驗預測檢查 (Prior Predictive Check)

配適前，先**從先驗模擬資料**，確認產生的結果合理。若模擬出荒謬值（負身高、每次都 100% 成功），就要修改先驗。

```python
import numpy as np
from scipy.stats import beta, binom
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
theta = beta.rvs(2, 2, size=1000, random_state=rng)       # 從先驗抽 θ
y_sim = binom.rvs(n=20, p=theta, random_state=rng)         # 每個 θ 模擬一次 20 次擲硬幣

plt.hist(y_sim, bins=np.arange(22) - 0.5, density=True, edgecolor="white")
plt.xlabel("Heads out of 20"); plt.show()
```

## 先驗敏感度分析 (Prior Sensitivity)

在幾個合理的先驗下配適同一模型，比較後驗變化多少。

```python
heads, tails = 8, 4
for name, (a, b) in {"flat": (1, 1), "weak": (2, 2), "skeptical": (10, 10)}.items():
    post = beta(a + heads, b + tails)
    print(f"{name:10s} mean={post.mean():.3f}  95% CI=({post.ppf(.025):.3f}, {post.ppf(.975):.3f})")
```

後驗隨先驗大幅變動代表：資料還不夠多讓概似主導，或模型對先驗高度敏感，報告時要特別說明。這不是失敗，而是告訴你結論有多少來自資料、多少來自假設。
