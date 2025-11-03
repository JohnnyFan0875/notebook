# Probability Distributions

Probability distributions describe how the values of a random variable are distributed — in other words, how likely different outcomes are.  
They are essential in statistics, machine learning, and data analysis for hypothesis testing, modeling uncertainty, and simulating data.

## 1. Overview

A **probability distribution** defines the likelihood of each possible value that a random variable can take.  
Distributions are broadly classified into:

| Type           | Description                                               | Examples                                              |
| -------------- | --------------------------------------------------------- | ----------------------------------------------------- |
| **Discrete**   | Random variable takes countable values (e.g., 0, 1, 2, …) | Bernoulli, Binomial, Poisson, Geometric               |
| **Continuous** | Random variable can take any real value within a range    | Normal, Uniform, Exponential, Chi-square, t, F, Gamma |

## 2. Discrete Distributions

### 2.1 Bernoulli Distribution

- **Definition**: Models a single binary trial (success/failure).
- **PMF**: $P(X=x) = p^x (1-p)^{1-x}, \quad x \in \{0,1\}$
- **Mean**: $E[X] = p$
- **Variance**: $Var[X] = p(1-p)$
- **Use Case**: Binary outcomes, coin toss, success/failure events.

```python
from scipy.stats import bernoulli
bernoulli.pmf(1, p=0.6)
```

## 2.2 Binomial Distribution

**Definition:** Number of successes in $ n $ independent Bernoulli trials.

**PMF:**
$ P(X=k) = \binom{n}{k} p^k (1-p)^{n-k} $

**Mean / Variance:**
$ np $, $ np(1-p) $

**Use Case:** Repeated binary experiments (e.g., 10 coin flips).

```python
from scipy.stats import binom
binom.pmf(3, n=10, p=0.5)
```

## 2.3 Poisson Distribution

**Definition:** Counts the number of events occurring in a fixed interval.

**PMF:**
$ P(X=k) = \frac{e^{-\lambda} \lambda^k}{k!} $

**Mean / Variance:**
$ \lambda $

**Use Case:** Event counts (accidents per day, mutations per gene).

```python
from scipy.stats import poisson
poisson.pmf(4, mu=3)
```

## 2.4 Geometric Distribution

**Definition:** Number of trials until the first success.

**PMF:**
$ P(X=k) = (1-p)^{k-1}p, \quad k = 1,2,3,... $

**Mean / Variance:**
$ 1/p $, $ (1-p)/p^2 $

**Property:** Memoryless.

**Use Case:** Waiting times until first success or failure.

```python
from scipy.stats import geom
geom.pmf(3, p=0.25)
```

## 2.5 Negative Binomial Distribution

**Definition:** Number of trials required to achieve ( r ) successes.

**Generalization** of the geometric distribution.

**Use Case:** Overdispersed count data, epidemiology.

```python
from scipy.stats import nbinom
nbinom.pmf(5, n=3, p=0.4)
```

## 3. Continuous Distributions

### 3.1 Uniform Distribution

**Definition:** All outcomes equally likely in range [a, b].

**PDF:**
$ f(x) = \frac{1}{b-a}, \quad a \le x \le b $

**Use Case:** Random sampling, simulation baseline.

```python
from scipy.stats import uniform
uniform.pdf(0.5, loc=0, scale=1)
```

### 3.2 Normal (Gaussian) Distribution

**Definition:** The bell-shaped distribution commonly seen in nature.

**PDF:**
$ f(x) = \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x-\mu)^2}{2\sigma^2}} $

**Use Case:** Measurement errors, biological traits, regression residuals.

```python
from scipy.stats import norm
norm.pdf(0, loc=0, scale=1)
```

### 3.3 Exponential Distribution

**Definition:** Models waiting times between independent events.

**PDF:**
$ f(x) = \lambda e^{-\lambda x}, \quad x \ge 0 $

**Property:** Memoryless.

**Use Case:** Reliability, survival analysis, interarrival times.

```python
from scipy.stats import expon
expon.cdf(2, scale=1)
```

### 3.4 Chi-square Distribution

**Definition:** Sum of squares of $ k $ standard normal variables.
$ X = Z_1^2 + Z_2^2 + ... + Z_k^2 $

**Parameters:** $ k $ = degrees of freedom.

**Use Case:** Variance tests, goodness-of-fit, independence tests.

```python
from scipy.stats import chi2
chi2.pdf(4, df=3)
```

### 3.5 Student’s t Distribution

**Definition:** Arises when estimating a mean with unknown variance.

**Note:** Heavier tails than Normal; approaches Normal as df $ \to \infty $.

**Use Case:** t-tests, confidence intervals.

```python
from scipy.stats import t
t.ppf(0.975, df=10)  # 97.5% critical value
```

### 3.6 F Distribution

**Definition:** Ratio of two scaled Chi-square variables.
$ F = \frac{(X_1/v_1)}{(X_2/v_2)} $

**Use Case:** ANOVA, model comparison.

**Properties:** Right-skewed, depends on two degrees of freedom.

```python
from scipy.stats import f
f.ppf(0.95, dfn=3, dfd=20)
```

### 3.7 Gamma Distribution

**Definition:** General family that includes the Exponential distribution.

**PDF:**
$ f(x) = \frac{\lambda^k x^{k-1} e^{-\lambda x}}{\Gamma(k)} $

**Use Case:** Waiting times, rainfall models, reliability.

```python
from scipy.stats import gamma
gamma.pdf(2, a=3, scale=2)
```

### 3.8 Beta Distribution

**Definition:** Continuous distribution on [0, 1]; flexible shape.

**PDF:**
$ f(x) = \frac{x^{\alpha-1} (1-x)^{\beta-1}}{B(\alpha, \beta)} $

**Use Case:** Probabilities, proportions, Bayesian priors.

```python
from scipy.stats import beta
beta.pdf(0.5, a=2, b=5)
```

## 4. Comparison Summary

| Distribution | Type       | Support | Mean    | Variance           | Typical Use Case             |
| ------------ | ---------- | ------- | ------- | ------------------ | ---------------------------- |
| Bernoulli    | Discrete   | {0,1}   | p       | p(1-p)             | Binary outcomes              |
| Binomial     | Discrete   | 0–n     | np      | np(1-p)            | Repeated trials              |
| Poisson      | Discrete   | 0–∞     | λ       | λ                  | Event counts                 |
| Geometric    | Discrete   | 1–∞     | 1/p     | (1-p)/p²           | First success                |
| Normal       | Continuous | (-∞, ∞) | μ       | σ²                 | Measurement noise            |
| Exponential  | Continuous | [0, ∞)  | 1/λ     | 1/λ²               | Waiting times                |
| Chi-square   | Continuous | [0, ∞)  | k       | 2k                 | Variance / independence test |
| t            | Continuous | (-∞, ∞) | 0       | v/(v−2)            | Mean estimation              |
| F            | Continuous | (0, ∞)  | –       | –                  | ANOVA                        |
| Beta         | Continuous | [0,1]   | α/(α+β) | αβ/((α+β)²(α+β+1)) | Proportions                  |

## 5. See Also

- [Hypothesis Testing](./hypothesis-testing/README.md)
- [ANOVA and F-statistics](./hypothesis-testing/anova.md#test-statistic)
- [Sampling and Estimation](./sampling.md)
