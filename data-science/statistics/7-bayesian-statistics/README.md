# Bayesian Statistics

**Bayesian statistics** is a framework for reasoning under uncertainty. It treats probability as a **degree of belief** that gets updated as new evidence arrives — rather than as a long-run frequency of events.

> 📌 **核心原則**：貝氏統計的本質是「用新資料更新舊有信念」。與頻率統計（Frequentist Statistics）的根本差異在於：貝氏統計允許我們對參數本身建立機率分佈，而非只對資料做推論。

---

## Why This Order?

The sections follow a natural Bayesian reasoning workflow:

```
What do I believe before seeing data? (Prior)
        ↓
What does the data tell me? (Likelihood)
        ↓
What should I believe now? (Posterior)
        ↓
How do I use and communicate this? (Inference & Decisions)
```

This order matters because Bayesian reasoning is fundamentally **sequential** — each posterior can become the next prior as more data arrives.

---

## Overview of Topics

| #   | Section                                                                    | Level       | Key Questions Answered                                               |
| --- | -------------------------------------------------------------------------- | ----------- | -------------------------------------------------------------------- |
| 1   | [**Core Concepts & Bayes' Theorem**](./1-bayes-theorem.md)                 | Foundation  | What is Bayesian thinking? How does Bayes' theorem work?             |
| 2   | [**Prior Distributions**](./2-prior-distributions.md)                     | Foundation  | How do I encode prior beliefs? What types of priors exist?           |
| 3   | [**Likelihood & Conjugate Priors**](./3-likelihood-conjugate.md)           | Core        | What is the likelihood function? What are conjugate pairs?           |
| 4   | [**Posterior Inference**](./4-posterior-inference.md)                      | Core        | How do I summarize and interpret the posterior?                      |
| 5   | [**Markov Chain Monte Carlo (MCMC)**](./5-mcmc.md)                         | Computation | How do I sample from distributions I can't solve analytically?       |
| 6   | [**Bayesian vs Frequentist**](./6-bayesian-vs-frequentist.md)              | Perspective | When should I use which framework? What are the key differences?     |

---

## What's Inside Each Section

### 1. Core Concepts & Bayes' Theorem

- What probability means in the Bayesian framework
- Bayes' theorem derivation and intuition
- The update cycle: Prior → Likelihood → Posterior
- Worked example: coin flipping from scratch

### 2. Prior Distributions

Three categories of priors with practical guidance:

| Prior Type       | When to Use                                        |
| ---------------- | -------------------------------------------------- |
| **Informative**  | Strong domain knowledge or historical data exists  |
| **Weakly informative** | Some constraints known, letting data drive result |
| **Non-informative (flat)** | Maximum objectivity; let data speak         |

### 3. Likelihood & Conjugate Priors

- What the likelihood function represents
- Conjugate prior pairs: Beta-Binomial, Gamma-Poisson, Normal-Normal
- Why conjugacy makes computation tractable

### 4. Posterior Inference

Key outputs from the posterior distribution:

| Output                         | Description                                              |
| ------------------------------ | -------------------------------------------------------- |
| **Posterior Mean / Median**    | Point estimate of the parameter                          |
| **Credible Interval (HDI/ETI)**| Bayesian analog of a confidence interval                 |
| **MAP (Maximum A Posteriori)** | Mode of the posterior — most likely parameter value      |
| **Posterior Predictive**       | Distribution over future observations                    |

### 5. MCMC

- Why exact posteriors are often intractable
- Metropolis-Hastings: the foundational algorithm
- Hamiltonian Monte Carlo (HMC) and NUTS: modern samplers
- Diagnosing convergence: trace plots, R̂, ESS

### 6. Bayesian vs Frequentist

Organized by key conceptual differences:

| Dimension            | Bayesian                         | Frequentist                          |
| -------------------- | -------------------------------- | ------------------------------------ |
| Probability means    | Degree of belief                 | Long-run frequency                   |
| Parameters are       | Random variables with distributions | Fixed but unknown constants       |
| Prior knowledge      | Formally incorporated            | Not used                             |
| Key output           | Posterior distribution           | p-value, confidence interval         |

---

## Visualization Quick Reference

| Chart                          | Best For                                              |
| ------------------------------ | ----------------------------------------------------- |
| Prior/Posterior overlay        | Showing how data updates belief                       |
| Trace plot                     | Diagnosing MCMC convergence                           |
| Posterior density plot         | Summarizing parameter uncertainty                     |
| Credible interval plot         | Communicating uncertainty around an estimate          |
| Posterior predictive check     | Assessing model fit                                   |

---

## Tools Used in This Module

| Library      | Purpose                                      |
| ------------ | -------------------------------------------- |
| `scipy.stats`| Prior/posterior distributions, Beta, Gamma   |
| `numpy`      | Numerical computation, sampling              |
| `matplotlib` / `seaborn` | Visualization                  |
| `pymc`       | Probabilistic programming, MCMC              |
| `arviz`      | MCMC diagnostics and posterior visualization |

---

## Key Takeaway

> Bayesian statistics answers: **"Given what I knew before and what I've just observed, what should I believe now — and how confident am I?"**  
> Always pair parameter estimates with their full posterior distribution. A single number without uncertainty is an incomplete Bayesian answer.
