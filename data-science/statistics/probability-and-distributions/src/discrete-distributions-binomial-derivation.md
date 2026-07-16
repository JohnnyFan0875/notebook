# Binomial Mean and Variance Derivation

Let

$$
X = X_1 + X_2 + \cdots + X_n
$$

where each $X_i$ is a Bernoulli random variable:

$$
X_i =
\begin{cases}
1, & \text{if trial } i \text{ is a success} \\
0, & \text{if trial } i \text{ is a failure}
\end{cases}
$$

with

$$
P(X_i = 1) = p \qquad P(X_i = 0) = 1-p
$$

So for each trial:

$$
E(X_i) = 1 \cdot p + 0 \cdot (1-p) = p
$$

By linearity of expectation:

$$
E(X) = E(X_1 + \cdots + X_n) = E(X_1) + \cdots + E(X_n) = np
$$

For variance, first note that for a Bernoulli variable:

$$
\text{Var}(X_i) = E(X_i^2) - [E(X_i)]^2
$$

Since $X_i$ is only 0 or 1, we have $X_i^2 = X_i$, so:

$$
E(X_i^2) = E(X_i) = p
$$

Therefore:

$$
\text{Var}(X_i) = p - p^2 = p(1-p)
$$

Because Binomial trials are independent:

$$
\text{Var}(X) = \text{Var}(X_1 + \cdots + X_n) = \text{Var}(X_1) + \cdots + \text{Var}(X_n) = np(1-p)
$$

[Back to Binomial Distribution](../discrete-distributions.md#binomial-distribution)
