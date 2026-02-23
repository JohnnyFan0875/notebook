# Probability & Distributions

**Probability** is the mathematical language for describing uncertainty. Before making any statistical inference — testing a hypothesis, building a model, or interpreting a p-value — you need to understand how probability works and what distributions describe.

> 📌 **為什麼要學機率？**  
> Descriptive statistics describes what you *observed*. Probability describes what you *expect to happen* — it's the bridge between your sample data and conclusions about the wider world.

---

## How This Connects to Other Topics

```
Descriptive Statistics          ← You are here (done)
        ↓
Probability & Distributions     ← This section
        ↓
Inferential Statistics          ← Uses distributions to test hypotheses
        ↓
Regression / ANOVA / ...        ← Applied methods built on inference
```

Specifically, the **sampling distribution** (Section 5) is the direct bridge into inferential statistics — it explains why the Central Limit Theorem makes so many statistical tests possible.

---

## Overview of Topics

| # | Section | Key Questions Answered |
|---|---------|----------------------|
| 1 | [**Probability Basics**](./1-probability-basics.md) | What is probability? How do we combine events? What is conditional probability? |
| 2 | [**Random Variables**](./2-random-variables.md) | What is a random variable? What are PMF, PDF, CDF? How do we summarize a distribution? |
| 3 | [**Discrete Distributions**](./3-discrete-distributions.md) | Which distribution fits count data? What are Binomial, Poisson, Geometric? |
| 4 | [**Continuous Distributions**](./4-continuous-distributions.md) | What is the Normal distribution? When do we use t, Chi-square, F, Exponential? |
| 5 | [**Sampling Distributions & CLT**](./5-sampling-distributions.md) | Why does the normal distribution appear everywhere? What is the Central Limit Theorem? |

---

## What's Inside Each Section

### 1. Probability Basics
- Classical, frequentist, and subjective probability
- Complement, union, intersection of events
- Addition and multiplication rules
- Conditional probability and independence
- Bayes' Theorem (intuition + formula)

### 2. Random Variables
- Discrete vs continuous random variables
- PMF (Probability Mass Function) — for discrete
- PDF (Probability Density Function) — for continuous
- CDF (Cumulative Distribution Function)
- Expected value (mean) and variance of a distribution

### 3. Discrete Distributions

| Distribution | Typical Use Case |
|-------------|-----------------|
| **Binomial** | Number of successes in n independent trials |
| **Poisson** | Number of events in a fixed time/space interval |
| **Geometric** | Number of trials until first success |
| **Hypergeometric** | Sampling without replacement (e.g., quality control) |

### 4. Continuous Distributions

| Distribution | Typical Use Case |
|-------------|-----------------|
| **Normal (Gaussian)** | Heights, measurement errors; foundation of many tests |
| **t-distribution** | Small sample mean estimation; t-tests |
| **Chi-square (χ²)** | Variance tests; goodness-of-fit; categorical tests |
| **F-distribution** | Comparing variances; ANOVA |
| **Exponential** | Time between events; survival analysis |
| **Uniform** | Equal probability across a range; random number generation |

### 5. Sampling Distributions & CLT
- What is a sampling distribution?
- Central Limit Theorem (CLT) — the most important theorem in statistics
- Standard Error revisited
- Why CLT justifies using normal-based tests even on non-normal data

---

## Key Concepts at a Glance

| Concept | One-Line Summary |
|---------|-----------------|
| **Probability** | A number between 0 and 1 expressing likelihood |
| **Random Variable** | A variable whose value is determined by a random process |
| **PMF** | Probability of each outcome for a discrete variable |
| **PDF** | Probability density at each point for a continuous variable |
| **CDF** | Cumulative probability up to a given value |
| **Expected Value** | The long-run average of a random variable |
| **Variance** | How spread out the distribution is around the mean |
| **CLT** | Sample means approach normal distribution as n grows |

---

## What's Intentionally Excluded

| Topic | Why Excluded | Where It Belongs |
|-------|-------------|-----------------|
| Hypothesis testing (p-values, α) | Requires probability as a foundation first | Inferential Statistics |
| Bayesian inference | Builds on Bayes' Theorem but is a separate paradigm | Bayesian Statistics |
| Markov Chains | Advanced probability topic | Advanced / separate section |
| Multivariate distributions | Beyond introductory scope | Multivariate Analysis |

---

## Key Takeaway

> Probability gives you a **model of uncertainty**.  
> Distributions are **templates** that describe how random variables behave.  
> Together, they allow you to go from "what I observed" → "what is likely true in general."
