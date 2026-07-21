# Mean of Sample Mean Derivation

Let $X_1, X_2, \ldots, X_n$ be independent and identically distributed random variables from the same population.

Assume each observation has population mean:

$$
E(X_i) = \mu
$$

The sample mean is:

$$
\bar{X} = \frac{X_1 + X_2 + \cdots + X_n}{n}
$$

Now take expectation on both sides:

$$
E(\bar{X})
= E\left(\frac{X_1 + X_2 + \cdots + X_n}{n}\right)
$$

Use the constant multiple rule:

$$
E(\bar{X})
= \frac{1}{n} E(X_1 + X_2 + \cdots + X_n)
$$

Use linearity of expectation:

$$
E(\bar{X})
= \frac{1}{n}\left[E(X_1) + E(X_2) + \cdots + E(X_n)\right]
$$

Since every $X_i$ comes from the same population:

$$
E(X_1) = E(X_2) = \cdots = E(X_n) = \mu
$$

Therefore:

$$
E(\bar{X})
= \frac{1}{n}(\mu + \mu + \cdots + \mu)
= \frac{1}{n}(n\mu)
= \mu
$$

So the sample mean is an unbiased estimator of the population mean:

$$
E(\bar{X}) = \mu
$$

[Back to Sampling Distributions](../sampling-distributions.md#central-limit-theorem-clt)
