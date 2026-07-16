# Poisson Mean and Variance Derivation

Start from the Poisson PMF:

$$
P(X = k) = \frac{e^{-\lambda}\lambda^k}{k!}, \qquad k = 0, 1, 2, \ldots
$$

For the mean:

$$
E(X) = \sum_{k=0}^{\infty} k \, P(X = k)
= \sum_{k=1}^{\infty} k \frac{e^{-\lambda}\lambda^k}{k!}
$$

Since $k / k! = 1 / (k-1)!$, this becomes:

$$
E(X) = \sum_{k=1}^{\infty} \frac{e^{-\lambda}\lambda^k}{(k-1)!}
= \lambda \sum_{k=1}^{\infty} \frac{e^{-\lambda}\lambda^{k-1}}{(k-1)!}
$$

Let $j = k-1$. Then:

$$
E(X) = \lambda \sum_{j=0}^{\infty} \frac{e^{-\lambda}\lambda^j}{j!}
= \lambda \cdot 1
= \lambda
$$

For the variance, first compute $E[X(X-1)]$:

$$
E[X(X-1)] = \sum_{k=0}^{\infty} k(k-1) P(X = k)
= \sum_{k=2}^{\infty} k(k-1)\frac{e^{-\lambda}\lambda^k}{k!}
$$

Since $k(k-1) / k! = 1 / (k-2)!$, we get:

$$
E[X(X-1)] = \sum_{k=2}^{\infty} \frac{e^{-\lambda}\lambda^k}{(k-2)!}
= \lambda^2 \sum_{k=2}^{\infty} \frac{e^{-\lambda}\lambda^{k-2}}{(k-2)!}
$$

Let $j = k-2$. Then:

$$
E[X(X-1)] = \lambda^2 \sum_{j=0}^{\infty} \frac{e^{-\lambda}\lambda^j}{j!}
= \lambda^2
$$

Now use:

$$
E(X^2) = E[X(X-1)] + E(X) = \lambda^2 + \lambda
$$

So:

$$
\text{Var}(X) = E(X^2) - [E(X)]^2
= (\lambda^2 + \lambda) - \lambda^2
= \lambda
$$

[Back to Poisson Distribution](../discrete-distributions.md#poisson-distribution)
