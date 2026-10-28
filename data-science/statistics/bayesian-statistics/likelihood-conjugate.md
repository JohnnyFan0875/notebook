[Statistics](../README.md) › [貝氏統計](README.md) › 概似與共軛

# 概似與共軛先驗 (Likelihood & Conjugate Priors)

## 概似函數 (Likelihood Function)

概似 $L(\theta) = P(D \mid \theta)$：**資料固定**，看哪些 θ 讓觀察到的資料最合理。

> 概似**不是** θ 的機率分配，對 θ 積分不等於 1。它是 θ 的函數，其最大值就是 [MLE](../probability-and-distributions/maximum-likelihood.md)。

例：n 次擲硬幣得 k 次正面，$L(\theta) \propto \theta^k (1-\theta)^{n-k}$，峰值在 k/n。n 越大，概似越窄、越集中，所以大樣本會壓過先驗。

## 共軛先驗 (Conjugate Prior)

若先驗與後驗屬於**同一個分配族**，就稱此先驗與概似共軛。後驗可以直接用公式更新：先驗的超參數 (hyperparameter) **加上**資料的簡單摘要。

| 概似（資料） | 共軛先驗 | 後驗 | 先驗的直覺 | 用途 |
| --- | --- | --- | --- | --- |
| Binomial（k 成功 / n 次） | Beta(α, β) | **Beta(α + k, β + n − k)** | 已看過 α 次成功、β 次失敗（pseudo-counts） | 比例、A/B 測試、轉換率 |
| Poisson（x₁…xₙ） | Gamma(α, β) | **Gamma(α + Σxᵢ, β + n)** | 已在 β 個區間內看過 α 個事件 | 事件率、計數 |
| Normal（σ 已知） | Normal(μ₀, σ₀²) | Normal(μₙ, σₙ²)，見下 | 先驗平均與其精確度 | 估計平均數 |
| Normal（μ 已知） | Gamma（作用於精確度 1/σ²） | Gamma | — | 估計變異數 |
| Multinomial | Dirichlet | Dirichlet | 各類別的 pseudo-counts | 多類別比例、topic model |
| Exponential | Gamma | Gamma | — | 存活時間、可靠度 |

> Gamma-Poisson 混合的**邊際分配**正是 [負二項分配](../probability-and-distributions/discrete-distributions.md#負二項分配-negative-binomial)，這是 RNA-seq 計數使用 NB 的理論來源。

### Normal-Normal：精確度加權平均

$$
\frac{1}{\sigma_n^2} = \frac{1}{\sigma_0^2} + \frac{n}{\sigma^2}, \qquad
\mu_n = \sigma_n^2 \left( \frac{\mu_0}{\sigma_0^2} + \frac{n\bar{x}}{\sigma^2} \right)
$$

後驗平均是先驗平均與樣本平均的**精確度 (precision = 1/變異數) 加權平均**：哪邊越精確，權重越大。n 越大，資料權重越大。

## Python 範例

```python
import numpy as np
from scipy.stats import beta, gamma, norm

# Beta-Binomial：先驗 Beta(2,2)，觀察 30/50
post_p = beta(2 + 30, 2 + 20)
post_p.mean(), post_p.interval(0.95)

# Gamma-Poisson：先驗 Gamma(2, rate=1)，10 個區間共 47 個事件
post_lam = gamma(a=2 + 47, scale=1 / (1 + 10))      # scipy 用 scale = 1/rate
post_lam.mean()                                      # ≈ 4.45，介於先驗平均 2 與 MLE 4.7 之間

# Normal-Normal：先驗 N(70, 5²)，n=10、x̄=75、σ=8
prec = 1 / 5**2 + 10 / 8**2
mu_n = (70 / 5**2 + 10 * 75 / 8**2) / prec
sd_n = np.sqrt(1 / prec)                             # μ_n ≈ 74.0，sd_n ≈ 2.26
```

> **共軛只適用簡單模型**。邏輯斯迴歸、階層模型等多數真實模型沒有共軛先驗，需要 [MCMC](mcmc.md)。但共軛模型仍很有價值：它讓「先驗樣本量如何影響後驗」、「概似強度如何改變平衡」變得透明。
