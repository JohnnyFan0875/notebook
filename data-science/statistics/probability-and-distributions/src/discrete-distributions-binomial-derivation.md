# Binomial 平均與變異數推導

[← 回到二項分配](../discrete-distributions.md#二項分配-binomial)

把 Binomial 拆成 n 個獨立的 Bernoulli：$X = X_1 + \cdots + X_n$，其中 $X_i \in \{0, 1\}$、$P(X_i = 1) = p$。

**單次試驗**

$$
E(X_i) = 1 \cdot p + 0 \cdot (1-p) = p
$$

因為 $X_i$ 只能是 0 或 1，所以 $X_i^2 = X_i$，$E(X_i^2) = p$：

$$
\text{Var}(X_i) = E(X_i^2) - [E(X_i)]^2 = p - p^2 = p(1-p)
$$

**加總**

- 期望值的線性（不需獨立）：$E(X) = \sum E(X_i) = np$
- 各次獨立，變異數可相加：$\text{Var}(X) = \sum \text{Var}(X_i) = np(1-p)$
