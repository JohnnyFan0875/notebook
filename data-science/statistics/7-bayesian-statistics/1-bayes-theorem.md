# 1. Core Concepts & Bayes' Theorem

Bayesian statistics is built on a single, powerful idea: **probability is a measure of belief, and beliefs should be updated when new evidence arrives**. This section introduces the philosophical foundation and the mathematical engine behind it all.

> 📌 **為什麼貝氏統計重要**：頻率統計只能回答「假設虛無假設為真，這份資料有多極端？」而貝氏統計能直接回答「看完資料後，我對參數的信念是什麼？」這是認識論上根本的差異。

---

## 1.1 Two Views of Probability

Before deriving Bayes' theorem, it's essential to understand what "probability" even means. There are two fundamentally different interpretations:

| View              | 中文         | Probability Represents         | Example Statement                                         |
| ----------------- | ------------ | ------------------------------ | --------------------------------------------------------- |
| **Frequentist**   | 頻率主義     | Long-run frequency of an event | "A fair coin lands heads 50% of the time in many flips"  |
| **Bayesian**      | 貝氏主義     | Degree of belief or uncertainty| "I am 70% confident this coin is fair"                   |

> 💡 The Bayesian view allows us to assign probabilities to **one-time events** and to **model parameters** — things a frequentist treats as fixed unknown constants, not as random variables.  
> 貝氏統計最大的優勢：可以對「這個參數是多少」建立機率分佈，而不是把它當作一個固定的未知常數。

---

## 1.2 Bayes' Theorem

Bayes' theorem follows directly from the definition of conditional probability.

### Derivation

$$P(A \cap B) = P(A|B) \cdot P(B) = P(B|A) \cdot P(A)$$

Rearranging:

$$\boxed{P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}}$$

### In Statistical Inference Context

Replace generic events with **parameter θ** and **data D**:

$$\boxed{P(\theta | D) = \frac{P(D | \theta) \cdot P(\theta)}{P(D)}}$$

| Term                     | Name           | 中文     | Meaning                                          |
| ------------------------ | -------------- | -------- | ------------------------------------------------ |
| $P(\theta \| D)$          | **Posterior**  | 後驗分佈 | Belief about θ **after** seeing data             |
| $P(D \| \theta)$          | **Likelihood** | 概似函數 | How probable is this data given parameter θ?     |
| $P(\theta)$              | **Prior**      | 先驗分佈 | Belief about θ **before** seeing data            |
| $P(D)$                   | **Evidence**   | 邊際概似 | Normalizing constant — ensures posterior sums to 1 |

> 💡 **The practical shorthand**: Posterior ∝ Likelihood × Prior  
> Because P(D) is just a constant (doesn't depend on θ), we often work with the unnormalized form:  
> $P(\theta | D) \propto P(D | \theta) \cdot P(\theta)$

---

## 1.3 Intuition: The Update Cycle

Bayesian inference is fundamentally **iterative**. You start with a prior belief, observe data, and produce a posterior — which then becomes the prior for the next observation.

```
Prior Belief → [Observe Data] → Posterior Belief → [Observe More Data] → Updated Posterior → ...
```

This is how beliefs rationally evolve with accumulating evidence. Crucially:

- **Strong priors** require more data to overcome
- **Weak (vague) priors** let the data dominate quickly
- **More data** → Posterior concentrates around the true value regardless of prior choice

---

## 1.4 Worked Example: Coin Flipping

Suppose we want to estimate θ = probability of heads for a coin we suspect might be biased.

**Setup:**
- Prior: We believe θ is probably near 0.5 (fair coin), but we're uncertain → Beta(2, 2)
- We flip 10 times and observe 7 heads

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

# Parameter space
theta = np.linspace(0, 1, 300)

# Prior: Beta(2, 2) — weak belief in fairness
prior_a, prior_b = 2, 2
prior = beta.pdf(theta, prior_a, prior_b)

# Data: 7 heads out of 10 flips
heads = 7
tails = 3

# Posterior: Beta(prior_a + heads, prior_b + tails)
# This is the Beta-Binomial conjugate result (see Section 3)
post_a = prior_a + heads
post_b = prior_b + tails
posterior = beta.pdf(theta, post_a, post_b)

# Likelihood: proportional to theta^heads * (1-theta)^tails
likelihood = theta**heads * (1 - theta)**tails
likelihood /= likelihood.max()  # normalize for visualization only

# Plot
plt.figure(figsize=(9, 5))
plt.plot(theta, prior,      label=f'Prior: Beta({prior_a}, {prior_b})',  linestyle='--', color='gray')
plt.plot(theta, likelihood, label='Likelihood (scaled)',                  linestyle=':',  color='steelblue')
plt.plot(theta, posterior,  label=f'Posterior: Beta({post_a}, {post_b})', linewidth=2.5,  color='tomato')
plt.axvline(heads / (heads + tails), color='black', linestyle='--', alpha=0.4, label='MLE (7/10 = 0.7)')
plt.xlabel('θ (probability of heads)')
plt.ylabel('Density')
plt.title("Bayesian Update: Coin Flip Example")
plt.legend()
plt.tight_layout()
plt.show()
```

**Reading the plot:**
- The **prior** (gray dashed) reflects our initial belief — symmetric, centered at 0.5
- The **likelihood** (blue dotted) peaks at 0.7, driven purely by data
- The **posterior** (red solid) is a compromise — pulled toward 0.7 by data, but moderated by the prior

> 💡 With only 10 flips, the prior still has visible influence. With 1000 flips at the same rate, the posterior would nearly coincide with the likelihood. **Data dominates as n grows.**  
> 資料量越大，先驗的影響越小，後驗越接近最大概似估計（MLE）。這也解釋了為什麼頻率統計和貝氏統計在大樣本時往往得出相似結論。

---

## 1.5 The Evidence Term P(D)

The denominator $P(D)$ is the **marginal likelihood** — the probability of observing the data averaged over all possible parameter values:

$$P(D) = \int P(D | \theta) \cdot P(\theta) \, d\theta$$

> ⚠️ This integral is often **analytically intractable** for complex models — which is why MCMC methods (Section 5) exist. For now, note that we usually work with:  
> Posterior ∝ Likelihood × Prior  
> and let sampling methods handle normalization implicitly.

---

## 1.6 Key Takeaways

| Concept                            | Key Point                                                                        |
| ---------------------------------- | -------------------------------------------------------------------------------- |
| **Probability = degree of belief** | In Bayesian stats, parameters have distributions — they are not fixed constants  |
| **Bayes' theorem**                 | Posterior ∝ Likelihood × Prior — the complete update formula                    |
| **The update cycle**               | Each posterior can become the prior for the next round of data                   |
| **Prior influence shrinks**        | As n → ∞, the posterior is dominated by the likelihood regardless of prior      |
| **P(D) is just a normalizer**      | Often skipped; sampling methods handle it without computing it directly          |

---

**Next:** [Prior Distributions →](./2-prior-distributions.md)
