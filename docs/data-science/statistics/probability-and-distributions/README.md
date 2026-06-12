# Introduction

**Probability** is the mathematical language for describing uncertainty. Before making any statistical inference — testing a hypothesis, building a model, or interpreting a p-value — you need to understand how probability works and what distributions describe.

Key point: Descriptive statistics tells you what you observed. Probability tells you what could happen and how likely it is, which makes it the bridge from raw observations to inference.

## Start Here If...

You should spend time in this module if any of these questions still feel fuzzy:

- "Why do p-values and confidence intervals use distributions at all?"
- "What exactly is a random variable?"
- "When do I use Binomial, Poisson, Normal, or t?"
- "Why does the normal distribution keep appearing everywhere?"

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

Specifically, the **sampling distribution** module is the direct bridge into inferential statistics because it explains why the Central Limit Theorem makes so many statistical tests possible.

## Overview of Topics

| Section | Key Questions Answered |
| --------- | ---------------------- |
| [**Probability Basics**](./probability-basics.md) | What is probability? How do we combine events? What is conditional probability? |
| [**Random Variables**](./random-variables.md) | What is a random variable? What are PMF, PDF, CDF? How do we summarize a distribution? |
| [**Discrete Distributions**](./discrete-distributions.md) | Which distribution fits count data? What are Binomial, Poisson, Geometric? |
| [**Continuous Distributions**](./continuous-distributions.md) | What is the Normal distribution? When do we use t, Chi-square, F, Exponential? |
| [**Sampling Distributions & CLT**](./sampling-distributions.md) | Why does the normal distribution appear everywhere? What is the Central Limit Theorem? |
| [**Monte Carlo Simulation**](./monte-carlo-simulation.md) | How can repeated random sampling approximate probabilities, uncertainty, and risk? |

## What's Inside Each Section

### Probability Basics
- Classical, frequentist, and subjective probability
- Complement, union, intersection of events
- Addition and multiplication rules
- Conditional probability and independence
- Bayes' Theorem (intuition + formula)

### Random Variables
- Discrete vs continuous random variables
- PMF (Probability Mass Function) — for discrete
- PDF (Probability Density Function) — for continuous
- CDF (Cumulative Distribution Function)
- Expected value (mean) and variance of a distribution

### Discrete Distributions

| Distribution | Typical Use Case |
| ------------- | ----------------- |
| **Binomial** | Number of successes in n independent trials |
| **Poisson** | Number of events in a fixed time/space interval |
| **Geometric** | Number of trials until first success |
| **Hypergeometric** | Sampling without replacement (e.g., quality control) |

### Continuous Distributions

| Distribution | Typical Use Case |
| ------------- | ----------------- |
| **Normal (Gaussian)** | Heights, measurement errors; foundation of many tests |
| **t-distribution** | Small sample mean estimation; t-tests |
| **Chi-square (χ²)** | Variance tests; goodness-of-fit; categorical tests |
| **F-distribution** | Comparing variances; ANOVA |
| **Exponential** | Time between events; survival analysis |
| **Uniform** | Equal probability across a range; random number generation |

### Sampling Distributions & CLT
- What is a sampling distribution?
- Central Limit Theorem (CLT) — the most important theorem in statistics
- Standard Error revisited
- Why CLT justifies using normal-based tests even on non-normal data

### Monte Carlo Simulation
- Estimating probabilities by repeated random sampling
- Distinguishing simulation from bootstrap resampling
- Building intuition for rare events and tail risk
- Connecting probability formulas to code and empirical approximation

## Key Concepts at a Glance

| Concept | One-Line Summary |
| --------- | ----------------- |
| **Probability** | A number between 0 and 1 expressing likelihood |
| **Random Variable** | A variable whose value is determined by a random process |
| **PMF** | Probability of each outcome for a discrete variable |
| **PDF** | Probability density at each point for a continuous variable |
| **CDF** | Cumulative probability up to a given value |
| **Expected Value** | The long-run average of a random variable |
| **Variance** | How spread out the distribution is around the mean |
| **CLT** | Sample means approach normal distribution as n grows |

## What's Intentionally Excluded

| Topic | Why Excluded | Where It Belongs |
| ------- | ------------- | ----------------- |
| Hypothesis testing (p-values, α) | Requires probability as a foundation first | Inferential Statistics |
| Bayesian inference | Builds on Bayes' Theorem but is a separate paradigm | Bayesian Statistics |
| Markov Chains | Advanced probability topic | Advanced / separate section |
| Multivariate distributions | Beyond introductory scope | Multivariate Analysis |

## Key Takeaway

Probability gives you a model of uncertainty. Distributions are templates that describe how random variables behave. Together, they allow you to go from "what I observed" → "what is likely true in general."

## Recommended Route

For most learners, the most effective route is:

1. probability rules and conditional probability
2. random variables and expected value
3. common discrete and continuous distributions
4. sampling distributions and the CLT
5. Monte Carlo only after the theory has a clear meaning

Tip: If inferential statistics feels mechanical, the missing piece is often probability intuition rather than more formulas.
