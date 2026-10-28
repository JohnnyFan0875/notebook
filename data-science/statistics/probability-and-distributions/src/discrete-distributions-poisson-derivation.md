# Poisson 平均與變異數推導

[← 回到卜瓦松分配](../discrete-distributions.md#卜瓦松分配-poisson)

PMF：$P(X = k) = \dfrac{e^{-\lambda}\lambda^k}{k!}$，並利用 $\sum_{j=0}^{\infty} \dfrac{e^{-\lambda}\lambda^j}{j!} = 1$（機率總和為 1）。

**平均**（$k/k! = 1/(k-1)!$，令 $j = k-1$）

$$
E(X) = \sum_{k=1}^{\infty} \frac{e^{-\lambda}\lambda^k}{(k-1)!}
= \lambda \sum_{j=0}^{\infty} \frac{e^{-\lambda}\lambda^{j}}{j!} = \lambda
$$

**變異數**：先算 $E[X(X-1)]$（$k(k-1)/k! = 1/(k-2)!$，令 $j = k-2$）

$$
E[X(X-1)] = \sum_{k=2}^{\infty} \frac{e^{-\lambda}\lambda^k}{(k-2)!}
= \lambda^2 \sum_{j=0}^{\infty} \frac{e^{-\lambda}\lambda^{j}}{j!} = \lambda^2
$$

$$
E(X^2) = E[X(X-1)] + E(X) = \lambda^2 + \lambda
\quad\Rightarrow\quad
\text{Var}(X) = \lambda^2 + \lambda - \lambda^2 = \lambda
$$
