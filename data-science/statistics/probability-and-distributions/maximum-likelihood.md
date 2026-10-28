[Statistics](../README.md) › [機率與分配](README.md) › 最大概似估計

# 最大概似估計 (Maximum Likelihood Estimation, MLE)

給定資料，找出「最能解釋這些資料」的參數值。幾乎所有統計模型（線性 / 邏輯斯迴歸、GLM、存活模型）以及多數 ML 模型的訓練，背後都是 MLE。

## 機率 vs 概似

| | 機率 (probability) | 概似 (likelihood) |
| --- | --- | --- |
| 固定的 | 參數 θ | 資料 x |
| 變動的 | 資料 x | 參數 θ |
| 問題 | 「參數已知，看到這筆資料的機率？」 | 「資料已知，哪個參數最可能？」 |
| 寫法 | $P(x \mid \theta)$ | $L(\theta \mid x) = P(x \mid \theta)$ |

獨立觀測值的概似是各點機率（密度）的乘積；實務上取 log 變成相加，數值更穩定：

$$
\ell(\theta) = \log L(\theta) = \sum_{i=1}^n \log f(x_i \mid \theta), \qquad
\hat\theta_{MLE} = \arg\max_\theta \ \ell(\theta)
$$

## 常見的 MLE 結果

| 模型 | MLE |
| --- | --- |
| Bernoulli(p) | $\hat p$ = 樣本成功比例 |
| Poisson(λ) | $\hat\lambda = \bar{x}$ |
| Normal(μ, σ²) | $\hat\mu = \bar{x}$，$\hat\sigma^2 = \frac{1}{n}\sum(x_i-\bar{x})^2$（除以 n，**有偏**） |
| Exponential(λ) | $\hat\lambda = 1/\bar{x}$ |

```python
import numpy as np
from scipy import stats, optimize

rng = np.random.default_rng(0)
x = rng.poisson(lam=3.2, size=200)

# 方法 1：數值最佳化（最小化負 log-likelihood）
nll = lambda lam: -stats.poisson.logpmf(x, lam).sum()
optimize.minimize_scalar(nll, bounds=(0.01, 20), method="bounded").x   # ≈ x.mean()

# 方法 2：scipy 連續分配直接 fit
data = rng.normal(5, 2, 500)
stats.norm.fit(data)           # (μ̂, σ̂)
```

## MLE 與 ML 損失函數的對應

**最小化損失函數 = 最大化某個分配假設下的 log-likelihood**。

| 假設的資料分配 | 負 log-likelihood 化簡後 | ML 名稱 |
| --- | --- | --- |
| $y \sim N(\hat y, \sigma^2)$ | $\sum (y-\hat y)^2$ | **MSE**（線性迴歸 / OLS） |
| $y \sim \text{Bernoulli}(\hat p)$ | $-\sum [y\log\hat p + (1-y)\log(1-\hat p)]$ | **Binary cross-entropy / log loss**（邏輯斯迴歸） |
| $y \sim \text{Categorical}(\hat{\mathbf p})$ | $-\sum \log \hat p_{y}$ | **Categorical cross-entropy**（softmax） |
| $y \sim \text{Laplace}$ | $\sum \lvert y-\hat y\rvert$ | **MAE** |
| $y \sim \text{Poisson}(\hat\mu)$ | $\sum (\hat\mu - y\log\hat\mu)$ | **Poisson loss**（計數迴歸） |

再加上參數的先驗分配就變成 MAP 估計，對應 **正則化 (regularization)**：常態先驗 ↔ L2 (Ridge)、Laplace 先驗 ↔ L1 (Lasso)。見 [Loss Functions](../../machine-learning/foundations/loss-functions.md)、[Regularization](../../machine-learning/foundations/regularization.md)、[先驗分配](../bayesian-statistics/prior-distributions.md)。

## 用 likelihood 比較模型

| 工具 | 公式 | 用途 |
| --- | --- | --- |
| 概似比檢定 (likelihood ratio test, LRT) | $2(\ell_{full} - \ell_{reduced}) \sim \chi^2_{\Delta df}$ | **巢狀 (nested)** 模型：多加的變數有沒有用？ |
| AIC | $2k - 2\ell$ | 比較模型，偏好預測力 |
| BIC | $k\log n - 2\ell$ | 比較模型，懲罰較重，偏好精簡 |

k = 參數數、n = 樣本數。AIC / BIC **越小越好**，只能比較**同一份資料**上的模型。

```python
import statsmodels.formula.api as smf
from scipy.stats import chi2

m0 = smf.ols("y ~ x1", data=df).fit()
m1 = smf.ols("y ~ x1 + x2 + x3", data=df).fit()

lr = 2 * (m1.llf - m0.llf)
chi2.sf(lr, df=m1.df_model - m0.df_model)   # LRT p 值
m0.aic, m1.aic, m0.bic, m1.bic
```

## MLE 的性質

| 性質 | 意義 |
| --- | --- |
| 一致性 (consistency) | n → ∞ 時收斂到真值 |
| 漸近常態 (asymptotic normality) | 大樣本下 $\hat\theta$ 近似常態 → 可算 SE、CI、Wald 檢定 |
| 有效性 (efficiency) | 大樣本下變異數達到理論下限 |
| 小樣本可能有偏 | 例如 σ̂² 除以 n |
| 依賴模型假設 | 分配假設錯了，估計與 SE 都可能失準 |

> 貝氏方法把 likelihood 與先驗結合得到後驗，見 [概似與共軛](../bayesian-statistics/likelihood-conjugate.md)。
