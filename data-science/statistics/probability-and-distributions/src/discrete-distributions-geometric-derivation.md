# Geometric Mean and Variance Derivation

Start from the Geometric PMF:

$$
P(X = k) = (1-p)^{k-1}p, \qquad k = 1, 2, 3, \ldots
$$

Let

$$
q = 1-p
$$

so the PMF becomes:

$$
P(X = k) = p q^{k-1}
$$

For $|q| < 1$, the geometric series is:

$$
\sum_{k=0}^{\infty} q^k = \frac{1}{1-q}
$$

Differentiate both sides with respect to $q$:

$$
\frac{d}{dq}\sum_{k=0}^{\infty} q^k
=
\frac{d}{dq}\frac{1}{1-q}
$$

This gives:

$$
\sum_{k=1}^{\infty} k q^{k-1}
=
\frac{1}{(1-q)^2}
$$

Now compute the mean:

$$
E(X) = \sum_{k=1}^{\infty} k P(X = k)
= \sum_{k=1}^{\infty} k p q^{k-1}
= p \sum_{k=1}^{\infty} k q^{k-1}
$$

Therefore:

$$
E(X) = p \cdot \frac{1}{(1-q)^2}
$$

Since $1-q = p$:

$$
E(X) = p \cdot \frac{1}{p^2}
= \frac{1}{p}
$$

For the variance, first compute $E[X(X-1)]$.

Differentiate again:

$$
\frac{d}{dq}\sum_{k=1}^{\infty} k q^{k-1}
=
\frac{d}{dq}\frac{1}{(1-q)^2}
$$

This gives:

$$
\sum_{k=2}^{\infty} k(k-1)q^{k-2}
=
\frac{2}{(1-q)^3}
$$

Multiply both sides by $q$:

$$
\sum_{k=2}^{\infty} k(k-1)q^{k-1}
=
\frac{2q}{(1-q)^3}
$$

So:

$$
E[X(X-1)]
= \sum_{k=1}^{\infty} k(k-1)P(X=k)
= p \sum_{k=2}^{\infty} k(k-1)q^{k-1}
$$

Therefore:

$$
E[X(X-1)] = p \cdot \frac{2q}{(1-q)^3}
$$

Since $1-q = p$:

$$
E[X(X-1)] = p \cdot \frac{2q}{p^3}
= \frac{2q}{p^2}
$$

Now use:

$$
E(X^2) = E[X(X-1)] + E(X)
$$

So:

$$
E(X^2) = \frac{2q}{p^2} + \frac{1}{p}
= \frac{2q + p}{p^2}
$$

Because $q = 1-p$:

$$
E(X^2) = \frac{2(1-p) + p}{p^2}
= \frac{2-p}{p^2}
$$

Finally:

$$
\text{Var}(X) = E(X^2) - [E(X)]^2
= \frac{2-p}{p^2} - \frac{1}{p^2}
= \frac{1-p}{p^2}
$$

[Back to Geometric Distribution](../discrete-distributions.md#geometric-distribution)
