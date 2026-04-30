# 3. Likelihood & Conjugate Priors

This section covers the **likelihood function** — what the data tells us about the parameter — and **conjugate priors**, which allow the posterior to be computed in closed form without numerical methods.

> 📌 **為什麼共軛先驗重要**：在大多數現實問題中，後驗分佈沒有解析解，需要用 MCMC 等方法近似。但共軛先驗讓我們能直接計算出後驗，非常適合用來建立直覺和學習貝氏更新的機制。

---

## 3.1 The Likelihood Function

The **likelihood** $P(D | \theta)$ is the probability of observing the data we collected, **as a function of the parameter θ**.

> ⚠️ **Common confusion**: The likelihood is NOT a probability distribution over θ — it does not integrate to 1 over θ. It is a function of θ that tells you how probable the observed data is for each possible value of θ.  
> 概似函數是參數 θ 的函數，不是 θ 的機率分佈。

### Example: Binomial Likelihood

For n coin flips with k heads:

$$\mathcal{L}(\theta | k, n) = P(k | \theta, n) = \binom{n}{k} \theta^k (1-\theta)^{n-k}$$

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

theta = np.linspace(0, 1, 300)

fig, axes = plt.subplots(1, 3, figsize=(13, 4))

datasets = [(3, 10), (7, 10), (70, 100)]
for ax, (k, n) in zip(axes, datasets):
    # Likelihood (binom constant drops out; we compute proportionally)
    likelihood = theta**k * (1 - theta)**(n - k)
    ax.plot(theta, likelihood / likelihood.max(), color='steelblue', linewidth=2)
    ax.axvline(k/n, color='tomato', linestyle='--', label=f'MLE = {k/n:.2f}')
    ax.set_title(f'{k} heads / {n} flips')
    ax.set_xlabel('θ')
    ax.set_ylabel('Scaled Likelihood')
    ax.legend()

plt.suptitle('Binomial Likelihood — Effect of Sample Size', fontsize=13, y=1.02)
plt.tight_layout()
plt.show()
```

> 💡 As n grows, the likelihood becomes **narrower and more concentrated** around the true θ. This is why large samples overwhelm the prior.

---

## 3.2 Conjugate Priors

A prior is **conjugate** to a likelihood if the resulting posterior belongs to the **same distribution family** as the prior. This produces a closed-form posterior update.

$$\text{Prior (family F)} \times \text{Likelihood} \Rightarrow \text{Posterior (family F)}$$

The posterior hyperparameters are just the prior hyperparameters **plus** a simple function of the data.

---

## 3.3 The Big Three Conjugate Pairs

### Pair 1: Beta–Binomial (for proportions)

| Component   | Distribution      | Parameters                        |
| ----------- | ----------------- | --------------------------------- |
| Prior       | Beta(α, β)        | α = prior successes, β = prior failures |
| Likelihood  | Binomial(n, θ)    | k = observed successes            |
| **Posterior** | **Beta(α + k, β + n − k)** | Simply add counts        |

**Interpretation**: The Beta(α, β) prior is equivalent to having already seen α − 1 successes and β − 1 failures (pseudo-counts).

```python
from scipy.stats import beta
import numpy as np
import matplotlib.pyplot as plt

theta = np.linspace(0, 1, 300)

# Prior
alpha_0, beta_0 = 2, 2  # weakly informative

# Observe data sequentially: 3 heads, then 4 more heads
datasets = [(3, 5), (7, 10), (30, 50)]

fig, axes = plt.subplots(1, 3, figsize=(13, 4))

for ax, (k, n) in zip(axes, datasets):
    prior     = beta.pdf(theta, alpha_0, beta_0)
    posterior = beta.pdf(theta, alpha_0 + k, beta_0 + (n - k))
    
    ax.plot(theta, prior,     label=f'Prior: Beta({alpha_0},{beta_0})', linestyle='--', color='gray')
    ax.plot(theta, posterior, label=f'Posterior: Beta({alpha_0+k},{beta_0+n-k})', color='tomato', linewidth=2)
    ax.axvline(k/n, linestyle=':', color='steelblue', label=f'MLE = {k/n:.2f}')
    ax.set_title(f'{k} heads / {n} flips')
    ax.set_xlabel('θ')
    ax.legend(fontsize=8)

plt.suptitle('Beta–Binomial Conjugate Update', fontsize=13, y=1.02)
plt.tight_layout()
plt.show()
```

---

### Pair 2: Gamma–Poisson (for counts / rates)

| Component   | Distribution        | Parameters                               |
| ----------- | ------------------- | ---------------------------------------- |
| Prior       | Gamma(α, β)         | α = shape, β = rate                      |
| Likelihood  | Poisson(λ)          | x₁, …, xₙ = observed counts             |
| **Posterior** | **Gamma(α + Σxᵢ, β + n)** | Add total count and observation count |

**Use case:** Modeling arrival rates (website visits per hour, defects per unit, etc.)

```python
from scipy.stats import gamma
import numpy as np
import matplotlib.pyplot as plt

lam = np.linspace(0, 15, 300)

# Prior: Gamma(2, 1) — weakly informative, mean = 2
alpha_0, beta_0 = 2, 1

# Observe 10 events with total count = 47 (mean ≈ 4.7)
n_obs   = 10
total   = 47

alpha_post = alpha_0 + total
beta_post  = beta_0  + n_obs

prior     = gamma.pdf(lam, a=alpha_0, scale=1/beta_0)
posterior = gamma.pdf(lam, a=alpha_post, scale=1/beta_post)

plt.figure(figsize=(8, 4))
plt.plot(lam, prior,     label=f'Prior: Gamma({alpha_0}, {beta_0})',           linestyle='--', color='gray')
plt.plot(lam, posterior, label=f'Posterior: Gamma({alpha_post}, {beta_post})',  color='tomato', linewidth=2)
plt.axvline(total/n_obs, linestyle=':', color='steelblue', label=f'MLE = {total/n_obs:.1f}')
plt.xlabel('λ (rate)')
plt.ylabel('Density')
plt.title('Gamma–Poisson Conjugate Update')
plt.legend()
plt.tight_layout()
plt.show()
```

---

### Pair 3: Normal–Normal (for means, known variance)

| Component     | Distribution             | Parameters                                |
| ------------- | ------------------------ | ----------------------------------------- |
| Prior         | Normal(μ₀, σ₀²)          | μ₀ = prior mean, σ₀² = prior variance     |
| Likelihood    | Normal(μ, σ²), σ known   | x̄ = sample mean, n = sample size         |
| **Posterior** | **Normal(μₙ, σₙ²)**     | Precision-weighted average of prior and data |

**Posterior mean formula** (precision-weighted):

$$\mu_n = \frac{\frac{\mu_0}{\sigma_0^2} + \frac{n\bar{x}}{\sigma^2}}{\frac{1}{\sigma_0^2} + \frac{n}{\sigma^2}}$$

$$\frac{1}{\sigma_n^2} = \frac{1}{\sigma_0^2} + \frac{n}{\sigma^2}$$

> 💡 **Interpretation**: The posterior mean is a **precision-weighted average** between the prior mean and the sample mean. Higher precision (lower variance) gets more weight.  
> 後驗均值是先驗均值與樣本均值的精確度加權平均。精確度越高（變異越小），影響力越大。

```python
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(50, 90, 400)

# Prior belief: μ ~ Normal(70, 5²)
mu_0   = 70
sigma_0 = 5

# Likelihood: observe n=10 people, sample mean = 75, known sigma = 8
x_bar   = 75
n       = 10
sigma_known = 8

# Compute posterior parameters
precision_prior = 1 / sigma_0**2
precision_data  = n / sigma_known**2
precision_post  = precision_prior + precision_data

mu_post    = (precision_prior * mu_0 + precision_data * x_bar) / precision_post
sigma_post = np.sqrt(1 / precision_post)

prior     = norm.pdf(x, mu_0, sigma_0)
posterior = norm.pdf(x, mu_post, sigma_post)

plt.figure(figsize=(9, 5))
plt.plot(x, prior,     label=f'Prior: N({mu_0}, {sigma_0}²)',                         linestyle='--', color='gray')
plt.plot(x, posterior, label=f'Posterior: N({mu_post:.2f}, {sigma_post:.2f}²)',         color='tomato', linewidth=2.5)
plt.axvline(x_bar, linestyle=':', color='steelblue', label=f'Sample mean = {x_bar}')
plt.xlabel('μ')
plt.ylabel('Density')
plt.title('Normal–Normal Conjugate Update')
plt.legend()
plt.tight_layout()
plt.show()
```

---

## 3.4 Summary Table: Conjugate Families

| Likelihood   | Prior Family | Posterior Family | Common Use Case                        |
| ------------ | ------------ | ---------------- | -------------------------------------- |
| Binomial     | Beta         | Beta             | A/B testing, conversion rates          |
| Poisson      | Gamma        | Gamma            | Event rates, count data                |
| Normal (σ known) | Normal   | Normal           | Estimating population mean             |
| Normal (μ known) | Gamma (on precision) | Gamma | Estimating variance                |
| Multinomial  | Dirichlet    | Dirichlet        | Multi-class proportions                |
| Exponential  | Gamma        | Gamma            | Time-to-event, reliability             |

> ⚠️ Conjugacy only works when the model is simple enough. For most real-world models (e.g., logistic regression, hierarchical models), there is no conjugate prior — this is where MCMC (Section 5) becomes necessary.

---

## 3.5 Key Takeaways

| Concept                          | Key Point                                                                           |
| -------------------------------- | ----------------------------------------------------------------------------------- |
| **Likelihood ≠ probability of θ** | It's the probability of the *data* as a function of θ                             |
| **Conjugacy = closed-form posterior** | Prior and posterior belong to the same family — update is just arithmetic     |
| **Beta–Binomial**                | The workhorse for proportion estimation (A/B tests, surveys)                        |
| **Gamma–Poisson**                | Standard for rate / count models                                                    |
| **Normal–Normal**                | Posterior mean = precision-weighted average of prior and data                       |
| **Conjugacy is a special case**  | Most real models aren't conjugate — conjugacy builds intuition, MCMC does the rest  |

---