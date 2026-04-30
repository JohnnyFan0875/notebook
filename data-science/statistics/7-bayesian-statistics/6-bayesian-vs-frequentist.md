# 6. Bayesian vs Frequentist

These two frameworks are both valid approaches to statistical inference. Understanding their differences — not just philosophically, but practically — helps you choose the right tool for each problem.

> 📌 **兩者並非對立**：在大樣本下，貝氏方法和頻率方法通常給出相似的結論。它們的根本差異在於：對「機率」的定義、對「參數」的看法，以及如何處理不確定性。選擇哪個框架，往往取決於問題性質與溝通需求，而非哪個「更正確」。

---

## 6.1 Philosophical Differences

| Dimension                 | Frequentist                                    | Bayesian                                       |
| ------------------------- | ---------------------------------------------- | ---------------------------------------------- |
| **Probability means**     | Long-run frequency of events                   | Degree of belief / uncertainty                 |
| **Parameters are**        | Fixed, unknown constants                       | Random variables with probability distributions|
| **Prior information**     | Not used                                       | Formally incorporated as prior distribution    |
| **Data is**               | A random realization from repeated experiments | Fixed and observed; parameters are uncertain   |
| **Goal of inference**     | Properties of estimators over repeated samples | Update beliefs given the observed data         |

---

## 6.2 Practical Differences in Output

### Confidence Interval vs Credible Interval

This is the most common source of confusion in applied statistics.

| Feature                    | Frequentist Confidence Interval         | Bayesian Credible Interval                |
| -------------------------- | --------------------------------------- | ----------------------------------------- |
| **Correct interpretation** | "If repeated, 95% of such intervals contain true θ" | "Given the data, P(θ ∈ interval) = 95%" |
| **What is random?**        | The interval (constructed from random data) | The parameter θ                         |
| **Intuitive meaning?**     | ❌ Counterintuitive — θ is not random   | ✅ Direct probability statement about θ  |
| **Requires prior?**        | No                                      | Yes                                       |

> 💡 Most practitioners **misinterpret** confidence intervals as credible intervals. The frequentist interpretation is technically correct but requires careful mental gymnastics. The Bayesian credible interval says what most people *think* a confidence interval says.  
> 實務中，絕大多數人對信賴區間的直覺理解，其實是可信區間的定義。

### p-value vs Posterior Probability

| Feature                   | Frequentist p-value                            | Bayesian Posterior                          |
| ------------------------- | ---------------------------------------------- | ------------------------------------------- |
| **What it answers**       | P(data this extreme \| H₀ is true)             | P(H₀ \| data) or P(θ > 0 \| data)          |
| **What researchers want** | ❌ Often misused as P(H₀ \| data)             | ✅ Directly the probability of interest     |
| **Decision threshold**    | Arbitrary (α = 0.05)                           | Based on the full posterior + loss function |
| **Effect size info**      | Not directly — must compute separately         | Built into the posterior distribution       |

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import beta

np.random.seed(42)

# Scenario: A/B test — did variant B improve conversion rate?
# Control: 100 users, 20 conversions (rate = 0.20)
# Variant: 100 users, 28 conversions (rate = 0.28)

n_ctrl, k_ctrl = 100, 20
n_var,  k_var  = 100, 28

# --- Frequentist: proportion z-test ---
p_ctrl = k_ctrl / n_ctrl
p_var  = k_var  / n_var
p_pool = (k_ctrl + k_var) / (n_ctrl + n_var)
se     = np.sqrt(p_pool * (1 - p_pool) * (1/n_ctrl + 1/n_var))
z      = (p_var - p_ctrl) / se
p_val  = 2 * (1 - stats.norm.cdf(abs(z)))   # two-sided

print(f"--- Frequentist ---")
print(f"p-value: {p_val:.4f}  {'(significant at α=0.05)' if p_val < 0.05 else '(not significant)'}")

# --- Bayesian: Beta-Binomial ---
prior_a, prior_b = 1, 1  # flat prior

post_ctrl = beta(prior_a + k_ctrl, prior_b + n_ctrl - k_ctrl)
post_var  = beta(prior_a + k_var,  prior_b + n_var  - k_var)

# P(variant > control) via Monte Carlo
n_sim     = 100_000
theta_ctrl = post_ctrl.rvs(n_sim)
theta_var  = post_var.rvs(n_sim)
prob_better = (theta_var > theta_ctrl).mean()

print(f"\n--- Bayesian ---")
print(f"P(variant > control | data) = {prob_better:.4f}")
print(f"Control posterior:  mean = {post_ctrl.mean():.3f}, 95% HDI ≈ [{post_ctrl.ppf(0.025):.3f}, {post_ctrl.ppf(0.975):.3f}]")
print(f"Variant  posterior: mean = {post_var.mean():.3f},  95% HDI ≈ [{post_var.ppf(0.025):.3f}, {post_var.ppf(0.975):.3f}]")
```

**Output interpretation:**

The frequentist result gives: "Is p-value < 0.05?" — a binary yes/no decision.  
The Bayesian result gives: "There is an 82% probability that the variant outperforms control" — a **continuous, actionable probability**.

---

## 6.3 When to Use Which Framework

This is a practical guide, not a prescription. Use what fits the question and context.

| Scenario                              | Preferred Framework | Reason                                               |
| ------------------------------------- | ------------------- | ---------------------------------------------------- |
| Large sample, standard hypothesis test | Either              | Results converge; frequentist is computationally simpler |
| Small sample, sparse data              | **Bayesian**        | Prior regularizes estimates; avoids overfitting      |
| Need to incorporate prior knowledge    | **Bayesian**        | Prior is a first-class model component               |
| Need a probability statement about θ  | **Bayesian**        | Frequentist can't give P(θ \| data) directly         |
| Sequential data / online updating     | **Bayesian**        | Natural update cycle fits streaming data             |
| Regulatory/legal context (FDA, courts)| Often **Frequentist** | Established standards; non-informative priors required |
| Communicating to non-statisticians    | **Bayesian**        | Credible interval interpretation is intuitive        |
| Complex hierarchical models           | **Bayesian**        | Natural framework for partial pooling               |
| Exploratory analysis                  | Either              | Both work; choose based on familiarity              |

---

## 6.4 The Large-Sample Equivalence

As n → ∞, Bayesian and frequentist point estimates converge:

- The **posterior mean** approaches the **MLE**
- The **credible interval** approaches the **confidence interval**
- The **posterior** becomes dominated by the likelihood, regardless of prior

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta, norm

theta = np.linspace(0, 1, 400)
true_theta = 0.35  # true parameter

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
sample_sizes = [5, 30, 200]

for ax, n in zip(axes, sample_sizes):
    k = int(true_theta * n)  # heads observed
    
    # Bayesian posterior (weakly informative prior)
    prior_a, prior_b = 2, 2
    posterior = beta(prior_a + k, prior_b + n - k)
    post_pdf  = posterior.pdf(theta)
    
    # Frequentist: Normal approximation to sampling distribution of MLE
    mle    = k / n
    se     = np.sqrt(mle * (1 - mle) / n)
    freq_pdf = norm.pdf(theta, loc=mle, scale=se)
    
    ax.plot(theta, post_pdf / post_pdf.max(),  color='tomato',    linewidth=2,  label='Posterior')
    ax.plot(theta, freq_pdf / freq_pdf.max(),  color='steelblue', linewidth=2,  linestyle='--', label='Freq. Sampling Dist.')
    ax.axvline(true_theta, color='black', linestyle=':', alpha=0.5, label='True θ')
    ax.set_title(f'n = {n}')
    ax.set_xlabel('θ')
    ax.legend(fontsize=8)
    ax.set_yticks([])

plt.suptitle('Convergence of Bayesian and Frequentist Inference as n Grows', y=1.02, fontsize=12)
plt.tight_layout()
plt.show()
```

> 💡 With small n, the prior visibly pulls the posterior away from the MLE. With large n, the two methods agree — the data overwhelms the prior. This convergence is a formal result known as **Bernstein–von Mises theorem**.

---

## 6.5 Common Misconceptions

| Misconception                                 | Reality                                                              |
| --------------------------------------------- | -------------------------------------------------------------------- |
| "Bayesian is subjective, frequentist is objective" | Both require assumptions — priors in Bayesian, model/test choice in frequentist |
| "p < 0.05 means there is a 95% chance H₀ is false" | ❌ Incorrect. P(data\|H₀) ≠ P(H₀\|data). This is the Bayesian quantity. |
| "A wider prior always leads to worse estimates" | Not necessarily — with enough data, prior choice rarely matters      |
| "Bayesian is always better for small samples"  | Only if the prior is well-specified; a bad prior can hurt estimates  |
| "Confidence intervals contain the parameter 95% of the time" | The parameter is fixed — the interval either contains it or doesn't. The 95% applies to the procedure. |

---

## 6.6 Key Takeaways

| Concept                              | Key Point                                                                        |
| ------------------------------------ | -------------------------------------------------------------------------------- |
| **Probability interpretation differs** | Bayesian = belief; Frequentist = long-run frequency                           |
| **Credible ≠ Confidence interval**   | Same number, completely different meaning                                        |
| **Bayesian gives P(θ\|data)**        | Frequentist cannot directly answer "what is the probability this effect is real?"|
| **Both converge at large n**         | Philosophical differences shrink as data accumulates                            |
| **Use priors carefully**             | Good priors help; bad priors hurt — always report your choice                   |
| **Framework choice = problem choice** | Match the framework to the question, not the other way around                  |

---
