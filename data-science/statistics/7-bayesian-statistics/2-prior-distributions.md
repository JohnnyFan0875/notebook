# 2. Prior Distributions

The prior distribution $P(\theta)$ encodes **everything you believe about the parameter before seeing any data**. Choosing a prior is one of the most distinctive — and most debated — aspects of Bayesian statistics.

> 📌 **先驗不是主觀任意的**：好的先驗反映真實的領域知識或合理的限制條件。選擇先驗本質上是在做模型假設，就像頻率統計假設常態性或等變異一樣。先驗的選擇應該透明且可辯護。

---

## 2.1 What a Prior Distribution Does

The prior constrains the parameter space to reflect what is realistically possible or likely before any data is collected. It:

- Encodes domain knowledge (e.g., "a conversion rate must be between 0 and 1")
- Regularizes estimates when data is sparse
- Becomes less influential as sample size grows
- Makes all modeling assumptions **explicit and transparent**

---

## 2.2 Types of Priors

### Informative Priors

A prior with a clear, concentrated shape — asserting strong belief about parameter values.

**When to use:** You have reliable prior data (historical experiments, expert consensus, published literature).

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta, norm

theta = np.linspace(0, 1, 300)

# Informative: strong belief that θ is near 0.3
# Based on historical data showing ~30% success rate
informative = beta.pdf(theta, a=15, b=35)  # mean = 15/50 = 0.3, concentrated

plt.plot(theta, informative, label='Informative: Beta(15, 35)', color='tomato', linewidth=2)
plt.xlabel('θ')
plt.ylabel('Density')
plt.title('Informative Prior')
plt.legend()
plt.show()
```

> 💡 An informative prior with Beta(15, 35) is equivalent to having already observed 15 successes and 35 failures. **Strong priors require strong justification.**

---

### Weakly Informative Priors

A prior that rules out extreme values but remains broad enough to let the data determine the result.

**When to use:** You know the rough scale or plausible range, but don't have precise historical estimates. This is the **recommended default** for most applied Bayesian work.

```python
theta_norm = np.linspace(-5, 5, 300)

# Weakly informative Normal prior on a regression coefficient
# "I don't expect it to be larger than ±3 in standardized units"
weakly_informative = norm.pdf(theta_norm, loc=0, scale=1)

plt.plot(theta_norm, weakly_informative, label='Weakly Informative: N(0, 1)', color='steelblue', linewidth=2)
plt.xlabel('θ')
plt.ylabel('Density')
plt.title('Weakly Informative Prior')
plt.legend()
plt.show()
```

> 💡 The Stan development team and PyMC community both recommend weakly informative priors as the practical default. They prevent sampling pathologies while remaining honest about uncertainty.  
> 實務上最推薦的選擇：提供合理約束，但讓資料主導。

---

### Non-Informative (Flat) Priors

A prior that is uniform or nearly so — imposing minimal assumptions.

**When to use:** Maximum objectivity; often in theoretical or regulatory contexts where using prior information would be controversial.

> ⚠️ **Flat ≠ Objective.** A flat prior on θ becomes informative once you transform the variable. For example, a flat prior on θ implies a non-flat prior on log(θ). True non-informativeness is mathematically subtle.

```python
# Flat prior: uniform over [0, 1]
flat = np.ones_like(theta)

# Jeffreys prior for a binomial proportion: Beta(0.5, 0.5)
# Invariant to reparameterization — the "most objective" choice
jeffreys = beta.pdf(theta, a=0.5, b=0.5)

plt.figure(figsize=(8, 4))
plt.plot(theta, flat,     label="Flat: Uniform(0, 1)",     linestyle='--', color='gray')
plt.plot(theta, jeffreys, label="Jeffreys: Beta(0.5, 0.5)", color='steelblue', linewidth=2)
plt.xlabel('θ')
plt.ylabel('Density')
plt.title('Non-Informative Priors')
plt.legend()
plt.show()
```

---

## 2.3 Comparison of Prior Types

| Type                     | Shape         | Influence on Posterior     | When to Use                             |
| ------------------------ | ------------- | -------------------------- | --------------------------------------- |
| **Informative**          | Concentrated  | High with small n          | Strong historical data or expert knowledge |
| **Weakly Informative**   | Broad but bounded | Low; keeps sampler stable | Default for most applied problems      |
| **Flat (Uniform)**       | Constant      | Minimal — data dominates   | Theoretical work; sensitive contexts   |
| **Jeffreys**             | U-shaped (Beta) or varies | Reparameterization-invariant | When objectivity is required     |

---

## 2.4 Common Prior Distributions by Parameter Type

Choosing a prior also requires matching the distribution family to the parameter's **support** (the range of values it can take).

| Parameter Type             | Typical Constraint     | Recommended Prior           | Why                                    |
| -------------------------- | ---------------------- | --------------------------- | -------------------------------------- |
| Probability / proportion   | [0, 1]                 | **Beta(α, β)**              | Natural support on [0, 1]              |
| Count / rate               | [0, ∞)                 | **Gamma(α, β)** or Half-Normal | Non-negative support                |
| Unbounded real number      | (−∞, ∞)                | **Normal(μ, σ)**            | Symmetric, flexible                    |
| Standard deviation / scale | (0, ∞)                 | **Half-Normal** or **Exponential** | Enforces positivity              |
| Correlation                | [−1, 1]                | **LKJ(η)**                  | Proper prior for correlation matrices  |

```python
from scipy.stats import gamma, expon, halfnorm

x = np.linspace(0, 5, 300)

fig, axes = plt.subplots(1, 3, figsize=(13, 4))

# Gamma prior for a rate parameter
axes[0].plot(x, gamma.pdf(x, a=2, scale=1), color='steelblue', linewidth=2)
axes[0].set_title('Gamma(2, 1) — for rates')
axes[0].set_xlabel('θ')

# Half-Normal for standard deviations
axes[1].plot(x, halfnorm.pdf(x, scale=1), color='tomato', linewidth=2)
axes[1].set_title('Half-Normal(0, 1) — for σ')
axes[1].set_xlabel('θ')

# Beta for proportions
axes[2].plot(theta, beta.pdf(theta, 2, 5), color='seagreen', linewidth=2)
axes[2].set_title('Beta(2, 5) — for proportions')
axes[2].set_xlabel('θ')

plt.tight_layout()
plt.show()
```

---

## 2.5 Visualizing Prior Sensitivity (Prior Predictive Check)

Before fitting a model, always simulate data from your prior to check whether it generates plausible outcomes. This is called a **prior predictive check**.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta, binom

np.random.seed(42)
n_samples = 1000
n_flips   = 20

# Draw θ from the prior
theta_samples = beta.rvs(a=2, b=2, size=n_samples)

# For each θ, simulate data
y_pred = binom.rvs(n=n_flips, p=theta_samples)

plt.figure(figsize=(8, 4))
plt.hist(y_pred, bins=np.arange(0, n_flips + 2) - 0.5,
         density=True, color='steelblue', edgecolor='white', alpha=0.8)
plt.xlabel('Number of Heads (out of 20 flips)')
plt.ylabel('Proportion')
plt.title('Prior Predictive Distribution\nBeta(2, 2) prior on θ')
plt.tight_layout()
plt.show()
```

> 💡 **Ask yourself**: Does this distribution of simulated outcomes make sense for my problem?  
> If the prior predictive generates absurd data (e.g., negative heights, 100% success rates every time), your prior needs revision.  
> 先驗預測性檢查：用先驗模擬資料，確認它能產生「合理」的結果。如果模擬出荒謬的數值，就需要重新考慮先驗設定。

---

## 2.6 Key Takeaways

| Concept                       | Key Point                                                                        |
| ----------------------------- | -------------------------------------------------------------------------------- |
| **Prior = modeling assumption** | All Bayesian priors are assumptions — make them explicit and justifiable        |
| **Default to weakly informative** | Prevents sampling issues; lets data speak while avoiding extreme values    |
| **Match prior to parameter support** | Never place probability mass in impossible regions (e.g., negative σ)    |
| **Flat ≠ Objective**          | Uniform priors can be highly informative under reparameterization                |
| **Always run a prior predictive check** | Simulate data from your prior to verify it generates plausible outcomes |

---

**← Previous:** [Core Concepts & Bayes' Theorem](./1-bayes-theorem.md)  
**Next:** [Likelihood & Conjugate Priors →](./3-likelihood-conjugate.md)
