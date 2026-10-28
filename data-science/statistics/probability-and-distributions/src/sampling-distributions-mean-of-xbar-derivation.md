# 樣本平均數的期望值推導

[← 回到中央極限定理](../sampling-distributions.md#中央極限定理-central-limit-theorem-clt)

設 $X_1, \ldots, X_n$ 為獨立同分配 (i.i.d.)，$E(X_i) = \mu$，$\bar{X} = \frac{1}{n}\sum X_i$。

$$
E(\bar{X})
= \frac{1}{n} E\left(\sum_{i=1}^n X_i\right)
= \frac{1}{n} \sum_{i=1}^n E(X_i)
= \frac{1}{n} \cdot n\mu
= \mu
$$

用到的只有「常數倍」與「期望值的線性」，因此 $\bar{X}$ 是 μ 的**不偏估計量**。

同理，若各 $X_i$ 獨立且 $\text{Var}(X_i) = \sigma^2$：

$$
\text{Var}(\bar{X}) = \frac{1}{n^2} \sum_{i=1}^n \text{Var}(X_i) = \frac{\sigma^2}{n}
\quad\Rightarrow\quad
SE = \frac{\sigma}{\sqrt{n}}
$$
