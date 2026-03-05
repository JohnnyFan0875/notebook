# 5. Markov Chain Monte Carlo (MCMC)

For most real-world Bayesian models, the posterior distribution has **no closed-form solution** — the normalizing constant P(D) is an intractable integral. MCMC methods solve this by **sampling** from the posterior without needing to compute it directly.

> 📌 **MCMC 的本質**：我們不需要知道後驗分佈的公式，只需要能夠評估「unnormalized posterior」（即 likelihood × prior）。MCMC 利用這一點，建立一條馬可夫鏈，使其穩態分佈等於目標後驗分佈，然後從中抽樣。

---

## 5.1 Why MCMC?

### The Problem

For a model with parameters θ = {θ₁, θ₂, ..., θₖ}, the posterior is:

$$P(\theta | D) = \frac{P(D | \theta) \cdot P(\theta)}{\int P(D | \theta) \cdot P(\theta) \, d\theta}$$

The denominator requires integrating over **all possible combinations of k parameters**. In high dimensions, this is computationally impossible with grid or quadrature methods.

### The MCMC Solution

1. Start at some initial parameter value θ⁰
2. Propose a new value θ* using a transition rule
3. Accept or reject θ* based on how much it improves the posterior
4. Repeat for thousands of iterations
5. The sequence of accepted values forms a **Markov chain** whose stationary distribution is the posterior

> 💡 After a **burn-in** period (warm-up), the chain "forgets" its starting point and the samples are approximately from the true posterior. We discard the burn-in and use only the post-warm-up samples.  
> 燒入期（warm-up）是讓鏈收斂到後驗分佈的初期過程，這段的樣本不使用。

---

## 5.2 Metropolis-Hastings: The Foundational Algorithm

The simplest MCMC algorithm. At each step:

1. Propose θ* from a proposal distribution q(θ* | θᵗ) (e.g., Normal centered at current θ)
2. Compute the **acceptance ratio**: $r = \frac{P(\theta^* | D)}{P(\theta^t | D)}$
3. Accept θ* with probability min(1, r); otherwise stay at θᵗ

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, beta

np.random.seed(42)

# Target: Beta(6, 3) posterior (known, for demonstration)
def log_posterior(theta):
    if theta <= 0 or theta >= 1:
        return -np.inf
    return (6 - 1) * np.log(theta) + (3 - 1) * np.log(1 - theta)

# Metropolis-Hastings
n_iter    = 5000
proposal_sd = 0.1
samples   = np.zeros(n_iter)
samples[0] = 0.5  # starting value

n_accepted = 0
for i in range(1, n_iter):
    current  = samples[i - 1]
    proposed = current + np.random.normal(0, proposal_sd)
    
    log_ratio = log_posterior(proposed) - log_posterior(current)
    
    if np.log(np.random.uniform()) < log_ratio:
        samples[i] = proposed
        n_accepted += 1
    else:
        samples[i] = current

print(f"Acceptance rate: {n_accepted / n_iter:.1%}")

# Discard burn-in
burn_in      = 500
post_samples = samples[burn_in:]

# Compare to true posterior
theta_vals = np.linspace(0, 1, 300)
true_post  = beta(6, 3).pdf(theta_vals)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(samples[:1000], alpha=0.6, color='steelblue')
axes[0].axvline(burn_in, color='tomato', linestyle='--', label='End of burn-in')
axes[0].set_title('Trace Plot (first 1000 iterations)')
axes[0].set_xlabel('Iteration')
axes[0].set_ylabel('θ')
axes[0].legend()

axes[1].hist(post_samples, bins=40, density=True, alpha=0.6,
             color='steelblue', label='MCMC Samples')
axes[1].plot(theta_vals, true_post, 'r-', linewidth=2, label='True Posterior Beta(6,3)')
axes[1].set_xlabel('θ')
axes[1].set_ylabel('Density')
axes[1].set_title('MCMC vs True Posterior')
axes[1].legend()

plt.tight_layout()
plt.show()
```

> ⚠️ **Proposal width matters**: Too narrow → slow exploration (high autocorrelation). Too wide → most proposals rejected (low acceptance rate). Target acceptance rate for MH is roughly 23–50%.

---

## 5.3 Modern Samplers: HMC and NUTS

Metropolis-Hastings is inefficient in high dimensions. Modern probabilistic programming libraries use **Hamiltonian Monte Carlo (HMC)** and its self-tuning variant **NUTS (No-U-Turn Sampler)**.

| Sampler | Mechanism                                    | Acceptance Rate | Scales to High Dimensions? |
| ------- | -------------------------------------------- | --------------- | -------------------------- |
| **Metropolis-Hastings** | Random walk proposals              | 20–50%         | ❌ Poor                   |
| **HMC** | Uses gradient info to make directed proposals | ~65–90%        | ✅ Good                   |
| **NUTS** | HMC with automatic tuning of path length    | ~65–90%        | ✅ Excellent              |

> 💡 NUTS is the default sampler in PyMC and Stan. You rarely need to tune it manually — it adapts step size and path length during warm-up.

---

## 5.4 Bayesian Inference with PyMC

PyMC is the standard Python library for Bayesian modeling with MCMC.

```python
import numpy as np
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt

np.random.seed(42)

# Observed data: 15 heads out of 25 flips
observed_heads = 15
n_flips        = 25

with pm.Model() as coin_model:
    # Prior
    theta = pm.Beta('theta', alpha=2, beta=2)
    
    # Likelihood
    y = pm.Binomial('y', n=n_flips, p=theta, observed=observed_heads)
    
    # MCMC sampling (NUTS by default)
    trace = pm.sample(2000, tune=1000, chains=4, random_seed=42, progressbar=False)

# Summarize posterior
print(az.summary(trace, var_names=['theta'], round_to=3))
```

**Expected output:**

| Parameter | Mean  | SD    | HDI 3% | HDI 97% | r_hat |
| --------- | ----- | ----- | ------- | ------- | ----- |
| theta     | 0.587 | 0.090 | 0.416   | 0.759   | 1.0   |

```python
# Plot posterior
az.plot_posterior(trace, var_names=['theta'], hdi_prob=0.95)
plt.title('Posterior Distribution of θ')
plt.show()
```

---

## 5.5 MCMC Diagnostics

MCMC is not guaranteed to converge. Always inspect these diagnostics before trusting your results.

### Trace Plot

The trace plot shows the sampled values at each iteration. A healthy chain should look like **"fuzzy caterpillar"** — well-mixed, without trends or sticky regions.

```python
az.plot_trace(trace, var_names=['theta'])
plt.tight_layout()
plt.show()
```

| Pattern                        | Diagnosis                                 | Action                             |
| ------------------------------ | ----------------------------------------- | ---------------------------------- |
| Random, well-mixed (fuzzy)     | ✅ Converged                             | Proceed                            |
| Trend or drift                 | ❌ Not converged                         | More warm-up or reparameterize     |
| Flat stretches (sticky)        | ❌ Sampling problems (funnels)           | Reparameterize or use more chains  |
| Chains agree with each other   | ✅ Good mixing                           | Proceed                            |

---

### R̂ (Gelman–Rubin Statistic)

Compares **within-chain** variance to **between-chain** variance across multiple chains. If all chains converge to the same posterior, these should be equal.

$$\hat{R} \approx 1.00 \Rightarrow \text{Converged} \quad \quad \hat{R} > 1.01 \Rightarrow \text{Warning}$$

```python
# R-hat is automatically reported in az.summary()
summary = az.summary(trace, var_names=['theta'])
print(summary[['mean', 'sd', 'hdi_3%', 'hdi_97%', 'r_hat']])
```

> ⚠️ Always run **at least 4 chains** for R̂ to be meaningful. One chain will almost always look fine even when the sampler hasn't explored the full posterior.

---

### Effective Sample Size (ESS)

MCMC samples are **autocorrelated** — consecutive samples are similar. ESS adjusts the nominal sample count for autocorrelation:

$$\text{ESS} = \frac{N}{1 + 2 \sum_{k=1}^{\infty} \rho_k}$$

| ESS          | Interpretation                          |
| ------------ | --------------------------------------- |
| ESS ≥ 400    | ✅ Sufficient for most summaries        |
| ESS < 100    | ⚠️ Estimates may be unreliable          |
| ESS very low | ❌ High autocorrelation; increase n or reparameterize |

```python
# ESS is reported by az.summary() as ess_bulk and ess_tail
print(az.summary(trace)[['ess_bulk', 'ess_tail', 'r_hat']])
```

---

## 5.6 MCMC Diagnostics Checklist

Before reporting results, verify all of the following:

| Check             | Tool                   | Threshold / Expectation            |
| ----------------- | ---------------------- | ---------------------------------- |
| **Trace plots**   | `az.plot_trace()`      | Well-mixed, no trends              |
| **R̂**            | `az.summary()`         | All parameters ≤ 1.01              |
| **ESS_bulk**      | `az.summary()`         | ≥ 400 per parameter                |
| **ESS_tail**      | `az.summary()`         | ≥ 400 per parameter                |
| **Divergences**   | `trace.sample_stats`   | 0 divergences (or very few)        |
| **PPC**           | Section 4              | Simulated data matches observed    |

---

## 5.7 Key Takeaways

| Concept                        | Key Point                                                                          |
| ------------------------------ | ---------------------------------------------------------------------------------- |
| **MCMC samples, not solves**   | We get draws from the posterior — not the formula                                  |
| **Burn-in must be discarded**  | Early samples are influenced by the starting point, not the posterior               |
| **NUTS > Metropolis-Hastings** | Use PyMC/Stan in practice — don't implement your own MH for real models            |
| **Always run 4 chains**        | Single-chain convergence is unreliable                                             |
| **R̂ ≤ 1.01, ESS ≥ 400**       | These are the minimum acceptance criteria for MCMC results                         |
| **Divergences = red flag**     | Any divergences indicate a problematic geometry — don't ignore them                |

---

**← Previous:** [Posterior Inference](./4-posterior-inference.md)  
**Next:** [Bayesian vs Frequentist →](./6-bayesian-vs-frequentist.md)
