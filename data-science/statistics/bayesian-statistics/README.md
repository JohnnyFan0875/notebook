# Bayesian Statistics

**Bayesian statistics** is a framework for reasoning under uncertainty. It treats probability as a **degree of belief** that gets updated as new evidence arrives — rather than as a long-run frequency of events.

Key point: Bayesian statistics treats learning as belief-updating. Instead of only describing how unusual the data is under a null model, it lets you express uncertainty directly about the parameters themselves.

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

## Overview of Topics

| Section | Level | Key Questions Answered |
| -------------------------------------------------------------------------- | ----------- | -------------------------------------------------------------------- |
| [**Core Concepts & Bayes' Theorem**](./bayes-theorem.md) | Foundation | What is Bayesian thinking? How does Bayes' theorem work? |
| [**Prior Distributions**](./prior-distributions.md) | Foundation | How do I encode prior beliefs? What types of priors exist? |
| [**Likelihood & Conjugate Priors**](./likelihood-conjugate.md) | Core | What is the likelihood function? What are conjugate pairs? |
| [**Posterior Inference**](./posterior-inference.md) | Core | How do I summarize and interpret the posterior? |
| [**Markov Chain Monte Carlo (MCMC)**](./mcmc.md) | Computation | How do I sample from distributions I can't solve analytically? |
| [**Bayesian vs Frequentist**](./bayesian-vs-frequentist.md) | Perspective | When should I use which framework? What are the key differences? |

## What's Inside Each Section

### Core Concepts & Bayes' Theorem

- What probability means in the Bayesian framework
- Bayes' theorem derivation and intuition
- The update cycle: Prior → Likelihood → Posterior
- Worked example: coin flipping from scratch

### Prior Distributions

Three categories of priors with practical guidance:

| Prior Type | When to Use |
| ---------------- | -------------------------------------------------- |
| **Informative** | Strong domain knowledge or historical data exists |
| **Weakly informative** | Some constraints known, letting data drive result |
| **Non-informative (flat)** | Maximum objectivity; let data speak |

### Likelihood & Conjugate Priors

- What the likelihood function represents
- Conjugate prior pairs: Beta-Binomial, Gamma-Poisson, Normal-Normal
- Why conjugacy makes computation tractable

### Posterior Inference

Key outputs from the posterior distribution:

| Output | Description |
| ------------------------------ | -------------------------------------------------------- |
| **Posterior Mean / Median** | Point estimate of the parameter |
| **Credible Interval (HDI/ETI)** | Bayesian analog of a confidence interval |
| **MAP (Maximum A Posteriori)** | Mode of the posterior — most likely parameter value |
| **Posterior Predictive** | Distribution over future observations |

### MCMC

- Why exact posteriors are often intractable
- Metropolis-Hastings: the foundational algorithm
- Hamiltonian Monte Carlo (HMC) and NUTS: modern samplers
- Diagnosing convergence: trace plots, R̂, ESS

### Bayesian vs Frequentist

Organized by key conceptual differences:

| Dimension | Bayesian | Frequentist |
| -------------------- | -------------------------------- | ------------------------------------ |
| Probability means | Degree of belief | Long-run frequency |
| Parameters are | Random variables with distributions | Fixed but unknown constants |
| Prior knowledge | Formally incorporated | Not used |
| Key output | Posterior distribution | p-value, confidence interval |

## Visualization Quick Reference

| Chart | Best For |
| ------------------------------ | ----------------------------------------------------- |
| Prior/Posterior overlay | Showing how data updates belief |
| Trace plot | Diagnosing MCMC convergence |
| Posterior density plot | Summarizing parameter uncertainty |
| Credible interval plot | Communicating uncertainty around an estimate |
| Posterior predictive check | Assessing model fit |

## Tools Used in This Module

| Library | Purpose |
| ------------ | -------------------------------------------- |
| `scipy.stats` | Prior/posterior distributions, Beta, Gamma |
| `numpy` | Numerical computation, sampling |
| `matplotlib` / `seaborn` | Visualization |
| `pymc` | Probabilistic programming, MCMC |
| `arviz` | MCMC diagnostics and posterior visualization |

## Key Takeaway

Bayesian statistics answers: "Given what I knew before and what I've just observed, what should I believe now — and how confident am I?" Always pair parameter estimates with their full posterior distribution. A single number without uncertainty is an incomplete Bayesian answer.

## Deep-Study Priorities

The most effective order is:

1. prior / likelihood / posterior roles
2. conjugate intuition
3. posterior summaries and predictive checks
4. MCMC after the modeling logic is clear

Tip: Bayesian computation is much easier once Bayesian interpretation already feels natural.
