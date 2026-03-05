# 4. Posterior Inference

Once we have the posterior distribution $P(\theta | D)$, we need to **summarize and communicate it**. Unlike frequentist inference, which produces a single point estimate plus a p-value, Bayesian inference delivers a full distribution — and we have multiple tools to describe it.

> 📌 **後驗分佈是貝氏推論的完整答案**：不要只報告後驗均值就停下來。後驗分佈的形狀、寬度和尾端都包含重要資訊。一個數字無法代表全貌。

---

## 4.1 Point Estimates from the Posterior

Three common ways to summarize the posterior with a single number:

| Estimate                   | 中文        | Formula / Definition               | Best Used When                         |
| -------------------------- | ----------- | ---------------------------------- | -------------------------------------- |
| **Posterior Mean**         | 後驗期望值  | E[θ \| D] = ∫ θ · P(θ\|D) dθ      | Symmetric, well-behaved posteriors     |
| **Posterior Median**       | 後驗中位數  | 50th percentile of posterior       | Skewed posteriors; robust choice       |
| **MAP (Maximum A Posteriori)** | 最大後驗估計 | argmax_θ P(θ \| D)             | When a single "most likely" value needed |

> 💡 **Posterior Mean vs MAP**: The posterior mean minimizes expected squared error; MAP minimizes expected 0-1 loss. For symmetric distributions, they're equal. For skewed distributions, the mean is typically preferred as a summary.  
> 後驗均值 = 最小化期望平方誤差；MAP = 後驗眾數。對稱分佈時相同，偏態時要注意區別。

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

theta = np.linspace(0, 1, 500)

# Posterior from Beta-Binomial: Beta(8, 4)
a, b = 8, 4
posterior = beta(a, b)

# Point estimates
post_mean   = posterior.mean()
post_median = posterior.median()
post_map    = (a - 1) / (a + b - 2)  # mode of Beta distribution

pdf_vals = posterior.pdf(theta)

plt.figure(figsize=(8, 4))
plt.plot(theta, pdf_vals, color='tomato', linewidth=2, label='Posterior: Beta(8, 4)')
plt.axvline(post_mean,   color='steelblue', linestyle='-',  linewidth=1.5, label=f'Mean   = {post_mean:.3f}')
plt.axvline(post_median, color='seagreen',  linestyle='--', linewidth=1.5, label=f'Median = {post_median:.3f}')
plt.axvline(post_map,    color='orange',    linestyle=':',  linewidth=1.5, label=f'MAP    = {post_map:.3f}')
plt.xlabel('θ')
plt.ylabel('Density')
plt.title('Point Estimates from the Posterior')
plt.legend()
plt.tight_layout()
plt.show()
```

---

## 4.2 Credible Intervals

A **credible interval** is the Bayesian analog of a confidence interval — but with a more intuitive interpretation.

> 💡 **Key difference from a frequentist confidence interval**:  
> - **Confidence interval**: "If I repeated this experiment many times, 95% of such intervals would contain the true θ." (θ is fixed; the interval is random.)  
> - **Credible interval**: "Given the data I observed, there is a 95% probability that θ lies in this interval." (θ is random; the interval is computed once.)  
> 信賴區間的正確解讀非常違反直覺。可信區間的解讀才是一般人直覺上認為信賴區間應該代表的意思。

### Equal-Tailed Interval (ETI / Quantile-Based)

Takes the 2.5th and 97.5th percentiles of the posterior. Simple and symmetric by construction.

```python
from scipy.stats import beta

a, b   = 8, 4
post   = beta(a, b)

eti_lower = post.ppf(0.025)
eti_upper = post.ppf(0.975)
print(f"95% ETI: [{eti_lower:.3f}, {eti_upper:.3f}]")
```

### Highest Density Interval (HDI)

The shortest interval that contains 95% of the posterior mass. For skewed distributions, this is **narrower and more informative** than the ETI.

```python
import numpy as np
from scipy.stats import beta

def compute_hdi(dist, credible_mass=0.95, n_points=10000):
    """Compute the HDI for a scipy distribution."""
    x = np.linspace(dist.ppf(0.001), dist.ppf(0.999), n_points)
    pdf_vals = dist.pdf(x)
    
    # Sort x by descending pdf value
    sorted_idx = np.argsort(pdf_vals)[::-1]
    sorted_x   = x[sorted_idx]
    
    # Cumulate until we reach credible_mass
    cum_pdf = np.cumsum(pdf_vals[sorted_idx]) / pdf_vals.sum()
    included = cum_pdf <= credible_mass
    
    hdi_points = sorted_x[included]
    return hdi_points.min(), hdi_points.max()

post = beta(8, 4)
hdi_lower, hdi_upper = compute_hdi(post)
print(f"95% HDI: [{hdi_lower:.3f}, {hdi_upper:.3f}]")
```

### Visualizing Both Intervals

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

theta     = np.linspace(0, 1, 500)
a, b      = 3, 12        # skewed posterior
post      = beta(a, b)
pdf_vals  = post.pdf(theta)

eti_lo, eti_hi = post.ppf(0.025), post.ppf(0.975)
hdi_lo, hdi_hi = compute_hdi(post)

plt.figure(figsize=(9, 4))
plt.plot(theta, pdf_vals, color='tomato', linewidth=2, label='Posterior: Beta(3, 12)')

# ETI shading
mask_eti = (theta >= eti_lo) & (theta <= eti_hi)
plt.fill_between(theta, pdf_vals, where=mask_eti, alpha=0.25, color='steelblue', label=f'ETI [{eti_lo:.3f}, {eti_hi:.3f}]')

# HDI shading
mask_hdi = (theta >= hdi_lo) & (theta <= hdi_hi)
plt.fill_between(theta, pdf_vals, where=mask_hdi, alpha=0.25, color='seagreen', label=f'HDI [{hdi_lo:.3f}, {hdi_hi:.3f}]')

plt.xlabel('θ')
plt.ylabel('Density')
plt.title('95% ETI vs 95% HDI (Skewed Posterior)')
plt.legend()
plt.tight_layout()
plt.show()
```

> 💡 For skewed posteriors, the HDI will be **narrower** and shifted toward the high-density region. For symmetric posteriors, ETI ≈ HDI.

---

## 4.3 Posterior Predictive Distribution

The **posterior predictive** distribution answers: *"Given the data I've seen, what should I expect for a future observation?"*

It integrates over all possible parameter values, weighted by the posterior:

$$P(\tilde{y} | D) = \int P(\tilde{y} | \theta) \cdot P(\theta | D) \, d\theta$$

> 💡 The posterior predictive accounts for **two sources of uncertainty**: (1) uncertainty about the parameter θ, and (2) inherent randomness even if θ were known. This is why predictions are always more uncertain than the posterior alone suggests.  
> 後驗預測分佈同時考量了「對參數不確定」和「資料本身的隨機性」，因此比後驗本身更寬。

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta, binom

np.random.seed(42)

a, b        = 8, 4      # posterior: Beta(8, 4)
n_future    = 10        # predict next 10 flips
n_samples   = 10000

# Sample θ from posterior, then sample data from Binomial
theta_samples = beta.rvs(a=a, b=b, size=n_samples)
y_pred        = binom.rvs(n=n_future, p=theta_samples)

plt.figure(figsize=(8, 4))
bins = np.arange(0, n_future + 2) - 0.5
plt.hist(y_pred, bins=bins, density=True,
         color='steelblue', edgecolor='white', alpha=0.8)
plt.xlabel('Number of Heads (out of 10 future flips)')
plt.ylabel('Probability')
plt.title('Posterior Predictive Distribution')
plt.xticks(range(n_future + 1))
plt.tight_layout()
plt.show()

print(f"Predicted mean: {y_pred.mean():.2f}  (expected: {a/(a+b) * n_future:.2f})")
print(f"Predicted 90% range: [{np.percentile(y_pred, 5):.0f}, {np.percentile(y_pred, 95):.0f}]")
```

---

## 4.4 Posterior Predictive Checks (PPC)

A **posterior predictive check** compares the **observed data** to data **simulated from the posterior predictive**. It's the primary tool for detecting model misspecification.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta, binom

np.random.seed(0)

# Observed data
observed = np.array([7, 6, 8, 5, 7, 6, 9, 7, 8, 6])  # heads out of 10 flips each
n_trials = 10

# Fit model: conjugate Beta-Binomial
prior_a, prior_b = 1, 1  # flat prior
post_a = prior_a + observed.sum()
post_b = prior_b + len(observed) * n_trials - observed.sum()

# Simulate from posterior predictive
n_rep     = 500
theta_rep = beta.rvs(a=post_a, b=post_b, size=n_rep)
y_rep     = binom.rvs(n=n_trials, p=theta_rep, size=n_rep)

# Compare statistic: mean
obs_stat  = observed.mean()
rep_stats = y_rep  # each replicated dataset is one draw

plt.figure(figsize=(8, 4))
plt.hist(rep_stats, bins=range(0, 12), density=True,
         color='lightgray', edgecolor='white', label='Simulated from Posterior Predictive')
plt.axvline(obs_stat, color='tomato', linewidth=2.5, label=f'Observed mean = {obs_stat:.1f}')
plt.xlabel('Number of Heads per Session')
plt.ylabel('Proportion')
plt.title('Posterior Predictive Check')
plt.legend()
plt.tight_layout()
plt.show()
```

> ✅ If the observed statistic falls comfortably within the simulated distribution — model is plausible.  
> ⚠️ If the observed statistic is in the extreme tails — model may be misspecified.

---

## 4.5 Summary: Posterior Inference Toolkit

| Tool                           | What It Answers                                        | When to Use                          |
| ------------------------------ | ------------------------------------------------------ | ------------------------------------ |
| **Posterior Mean**             | Best single estimate (minimizes MSE)                   | Symmetric posteriors                 |
| **Posterior Median**           | Robust central value                                   | Skewed posteriors                    |
| **MAP**                        | Most likely value                                      | When mode is the natural summary     |
| **ETI (Equal-Tailed Interval)**| Symmetric credible interval                            | Quick reporting, symmetric posteriors|
| **HDI (Highest Density Interval)** | Narrowest credible interval                        | Skewed posteriors; preferred default |
| **Posterior Predictive**       | Expected distribution of new data                      | Forecasting; propagating uncertainty |
| **Posterior Predictive Check** | Model fit assessment                                   | Always — validate your model         |

---

## 4.6 Key Takeaways

| Concept                        | Key Point                                                                         |
| ------------------------------ | --------------------------------------------------------------------------------- |
| **Credible interval ≠ CI**     | A 95% credible interval directly means "95% probability θ is in here"            |
| **HDI > ETI for skewed posteriors** | HDI is shorter and located where the data is most informative              |
| **Posterior predictive is broader** | It reflects both parameter uncertainty and data randomness               |
| **Always do a PPC**            | If simulated data looks nothing like observed data — reconsider your model        |
| **Report the full posterior**  | A single point estimate discards all uncertainty information                      |

---

**← Previous:** [Likelihood & Conjugate Priors](./3-likelihood-conjugate.md)  
**Next:** [MCMC →](./5-mcmc.md)
