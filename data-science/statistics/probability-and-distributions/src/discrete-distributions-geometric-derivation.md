# Geometric 平均與變異數推導

[← 回到幾何分配](../discrete-distributions.md#幾何分配-geometric)

PMF：$P(X = k) = p\,q^{k-1}$，其中 $q = 1-p$，$k = 1, 2, \ldots$

**工具：幾何級數微分**（$|q| < 1$）

$$
\sum_{k=0}^{\infty} q^k = \frac{1}{1-q}
\ \xrightarrow{\ d/dq\ }\
\sum_{k=1}^{\infty} k q^{k-1} = \frac{1}{(1-q)^2}
\ \xrightarrow{\ d/dq\ }\
\sum_{k=2}^{\infty} k(k-1) q^{k-2} = \frac{2}{(1-q)^3}
$$

**平均**

$$
E(X) = p \sum_{k=1}^{\infty} k q^{k-1} = p \cdot \frac{1}{p^2} = \frac{1}{p}
$$

**變異數**：先算 $E[X(X-1)]$

$$
E[X(X-1)] = p \sum_{k=2}^{\infty} k(k-1) q^{k-1} = p \cdot \frac{2q}{p^3} = \frac{2q}{p^2}
$$

$$
E(X^2) = \frac{2q}{p^2} + \frac{1}{p} = \frac{2-p}{p^2}
\quad\Rightarrow\quad
\text{Var}(X) = \frac{2-p}{p^2} - \frac{1}{p^2} = \frac{1-p}{p^2}
$$
