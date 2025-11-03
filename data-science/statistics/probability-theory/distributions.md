# Probability Distributions

## 1. Introduction

Probability distributions are foundational in statistics and data science. The `scipy.stats` module provides a comprehensive set of tools to work with continuous and discrete distributions, including PDF/PMF, CDF, random sampling, and parameter estimation.

### 1.1 Key Concepts

- **PDF (Probability Density Function)**: Describes the relative likelihood of a continuous random variable taking on a given value. The area under the curve over an interval represents the probability of falling within that interval.
- **PMF (Probability Mass Function)**: Used for discrete variables, giving the probability of each possible outcome.
- **CDF (Cumulative Distribution Function)**: Gives the cumulative probability that a random variable is less than or equal to a particular value.
- **PPF (Percent-Point Function)**: The inverse of the CDF, used to find threshold values for a given percentile.
- **rvs (Random Variates)**: Function to generate random samples following a specified distribution.

### 1.2 Standardization

- Standardization transforms raw values of a variable into **z-scores (or t-scores)**.
- After standardization:
  - Mean = 0
  - Standard deviation = 1
- Skewness of the original distribution remains unchanged.
- The x-axis becomes standardized units (z or t).
- Interpretation:
  - \(Z = \pm 1\) → The value is 1 standard deviation away from the mean.

\[
Z = \frac{X - \mu}{\sigma}
\]

### 1.3 Continuous Probability Distribution

- **x-axis:** values of the random variable \(X\)
- **y-axis:** probability density associated with each value (Probability Density Function, PDF)
- The probability of \(X\) lying within a range \([a,b]\) is given by the **area under the curve** of the PDF between those points:

\[
P(a \leq X \leq b) = \int_a^b f(x) \, dx
\]

- The value of the PDF at a single point \(f(x)\) is **not** the probability; probability comes from the **area under the curve**.

#### Examples of Continuous Distributions

- **Normal distribution (Gaussian, z-distribution)**

  - Bell-shaped, symmetric
  - [Empirical Rule (68–95–99.7 rule)](https://www.notion.so/Empirical-Rule-68-95-99-7-rule-15f06ef7ce8a80589f26d5296667e845?pvs=21)

- **Exponential distribution**

  - Models waiting times between independent events

- **Chi distribution**

  - With low degrees of freedom (df): positively skewed
  - As df increases (>30): approaches normal
  - Mean = df, Variance = \(2 \times df\)

- **t-distribution**
  - Similar to normal but with heavier tails
  - Mean = 0, Variance = \(\frac{df}{df-2}\) (for df > 2)
  - As \(n > 30\), t-distribution ≈ normal distribution
  - Used when population variance is unknown, regardless of sample size

## 2. Common Distribution Functions

Each distribution in `scipy.stats` provides a consistent interface:

```python
from scipy.stats import norm  # Example with normal distribution

# PDF: Probability Density Function - gives the likelihood of a value
norm.pdf(x, loc=mu, scale=sigma)

# CDF: Cumulative Distribution Function - cumulative probability up to x
norm.cdf(x, loc=mu, scale=sigma)

# PPF: Percent-Point Function - the value at a given percentile
norm.ppf(q, loc=mu, scale=sigma)

# rvs: Random Variates - generate random samples
norm.rvs(loc=mu, scale=sigma, size=n)
```

## 3. Common Distributions

### 3.1 Normal Distribution (`norm`)

- Bell-shaped, symmetric curve
- Area under curve = 1; tails extend to ±∞
- 68% within 1σ, 95% within 2σ, 99.7% within 3σ (empirical rule)

```python
from scipy.stats import norm
import numpy as np

x = np.linspace(-4, 4, 1000)  # Generate x-values for plot
pdf = norm.pdf(x, loc=0, scale=1)  # Standard normal PDF
cdf = norm.cdf(x, loc=0, scale=1)  # CDF
samples = norm.rvs(loc=0, scale=1, size=1000)  # Random samples
```

### 3.2 Binomial Distribution (`binom`)

- Models number of successes in n independent Bernoulli trials
- Parameters: `n` (trials), `p` (probability of success)

```python
from scipy.stats import binom
import numpy as np

x = np.arange(0, 21)
pmf = binom.pmf(x, n=20, p=0.5)  # Probability of each outcome
cdf = binom.cdf(x, n=20, p=0.5)
samples = binom.rvs(n=20, p=0.5, size=1000)
```

### 3.3 Poisson Distribution (`poisson`)

- Models count of events in a fixed interval given a constant average rate (λ)

```python
from scipy.stats import poisson

x = np.arange(0, 20)
pmf = poisson.pmf(x, mu=5)
cdf = poisson.cdf(x, mu=5)
samples = poisson.rvs(mu=5, size=1000)
```

### 3.4 Exponential Distribution (`expon`)

- Models time between Poisson events
- Mean time = `scale = 1 / λ`

```python
from scipy.stats import expon

x = np.linspace(0, 10, 1000)
pdf = expon.pdf(x, scale=1)
cdf = expon.cdf(x, scale=1)
samples = expon.rvs(scale=1, size=1000)
```

### 3.5 t Distribution (`t`)

- Similar to normal, but with heavier tails
- Used for small-sample inference; controlled by degrees of freedom (df)

```python
from scipy.stats import t

x = np.linspace(-4, 4, 1000)
pdf = t.pdf(x, df=10)
cdf = t.cdf(x, df=10)
samples = t.rvs(df=10, size=1000)
```

### 3.6 Uniform Distribution (`uniform`)

- All values in interval \[a, b] are equally likely

```python
from scipy.stats import uniform

x = np.linspace(0, 1, 1000)
pdf = uniform.pdf(x, loc=0, scale=1)
cdf = uniform.cdf(x, loc=0, scale=1)
samples = uniform.rvs(loc=0, scale=1, size=1000)
```

## 4. Practical Use Cases

```python
from scipy.stats import binom, poisson, expon, norm
import matplotlib.pyplot as plt
import numpy as np

# Plot PDF of standard normal
x = np.linspace(-4, 4, 1000)
y = norm.pdf(x)
plt.plot(x, y)
plt.title("Standard Normal PDF")
plt.xlabel("x")
plt.ylabel("Density")
plt.grid(True)
plt.show()

# Simulate and plot Poisson distribution
samples = poisson.rvs(mu=5, size=1000)
plt.hist(samples, bins=15, density=True, alpha=0.7)
plt.title("Poisson Distribution")
plt.xlabel("Number of Events")
plt.ylabel("Probability")
plt.grid(True)
plt.show()
```

## 5. Distribution Comparison

| Distribution | Type       | Key Use                | Skewed?       | Support        |
| ------------ | ---------- | ---------------------- | ------------- | -------------- |
| Normal       | Continuous | General modeling       | No            | (-∞, ∞)        |
| Binomial     | Discrete   | Yes/no trials          | No (if p=0.5) | {0, ..., n}    |
| Poisson      | Discrete   | Rare event counts      | Yes           | {0, 1, 2, ...} |
| Exponential  | Continuous | Waiting time           | Yes           | \[0, ∞)        |
| t            | Continuous | Inference with small n | No            | (-∞, ∞)        |
| Uniform      | Continuous | Baseline model         | No            | \[a, b]        |

## 6. Extra Tips

- Use `help(scipy.stats.norm)` or `norm.__doc__` to see detailed docs
- Estimate distribution parameters using `.fit()`:

```python
from scipy.stats import norm

# Generate synthetic data
data = norm.rvs(loc=10, scale=2, size=1000)
mu, sigma = norm.fit(data)
```

- Use `seaborn` for quick visualizations:

```python
import seaborn as sns
sns.histplot(norm.rvs(size=1000), kde=True)
```

## 7. Summary

The `scipy.stats` module provides a powerful and unified interface for working with probability distributions in Python. Mastery of these functions enables effective simulation, hypothesis testing, and probabilistic modeling.
