# Probability and Distributions

**Probability** is the mathematical language for describing uncertainty.

Before making any statistical inference — testing a hypothesis, building a model, or interpreting a p-value — you need to understand how probability works and what distributions describe.

**Key point:**

- **Descriptive statistics** tells you what you observed.
- **Probability** tells you what could happen and how likely it is, which makes it the bridge from raw observations to inference.

## How This Connects to Other Topics

```
Descriptive Statistics          ← done
        ↓
Probability & Distributions     ← This section
        ↓
Inferential Statistics          ← Uses distributions to test hypotheses
        ↓
Regression / ANOVA / ...        ← Applied methods built on inference
```

Specifically, the **sampling distribution** module is the direct bridge into inferential statistics because it explains why the Central Limit Theorem makes so many statistical tests possible.

## Overview of Topics

| Section                                                         | Key Questions Answered                                                                 |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [**Probability Basics**](./probability-basics.md)               | What is probability? How do we combine events? What is conditional probability?        |
| [**Random Variables**](./random-variables.md)                   | What is a random variable? What are PMF, PDF, CDF? How do we summarize a distribution? |
| [**Discrete Distributions**](./discrete-distributions.md)       | Which distribution fits count data? What are Binomial, Poisson, Geometric?             |
| [**Continuous Distributions**](./continuous-distributions.md)   | What is the Normal distribution? When do we use t, Chi-square, F, Exponential?         |
| [**Sampling Distributions & CLT**](./sampling-distributions.md) | Why does the normal distribution appear everywhere? What is the Central Limit Theorem? |
| [**Monte Carlo Simulation**](./monte-carlo-simulation.md)       | How can repeated random sampling approximate probabilities, uncertainty, and risk?     |

## Notes by Section

### Probability Basics

| Topic | What to Focus On | Why It Matters |
| ----- | ---------------- | -------------- |
| Probability interpretations | Classical, frequentist, and subjective probability | Different contexts use probability in slightly different ways |
| Events | Complement, union, intersection, mutually exclusive events | These are the building blocks for probability rules |
| Addition and multiplication rules | Combining event probabilities with or without overlap/independence | Most probability calculations reduce to these rules |
| Conditional probability | $P(A \mid B)$ and how information changes probability | Foundation for dependence, diagnosis-style problems, and Bayes' Theorem |
| Law of total probability | Breaking one probability into weighted conditional pieces | Useful when outcomes come from multiple groups or pathways |
| Bayes' Theorem | Updating probability after observing evidence | Core idea behind diagnostic testing, classification, and Bayesian inference |
| Formula to simulation | Checking probability calculations with repeated random sampling | Builds intuition and catches mistakes in manual probability reasoning |

### Random Variables

| Topic | What to Focus On | Why It Matters |
| ----- | ---------------- | -------------- |
| Discrete vs continuous variables | Countable outcomes vs values on a continuum | Determines whether probabilities use PMF, PDF, or areas under curves |
| PMF | Probability of each possible value for a discrete variable | Directly answers questions like $P(X = k)$ |
| PDF | Density curve for a continuous variable | Probabilities are areas over intervals, not single-point heights |
| CDF | $P(X \leq x)$ for discrete or continuous variables | Converts distributions into cumulative probabilities |
| Expected value | Long-run average of a random variable | Gives the distribution's center or theoretical mean |
| Variance and SD | Expected squared deviation and its square root | Describes spread around the expected value |
| Percentiles and inverse CDF | Values that place a chosen probability below them | Used for cutoffs, quantiles, and confidence interval critical values |

### Discrete Distributions

| Distribution | What to Focus On | Typical Use Case |
| ------------ | ---------------- | ---------------- |
| **Binomial** | Fixed number of independent Bernoulli trials; mean and variance derivation | Number of successes in $n$ independent trials |
| **Poisson** | Counts in a fixed interval; mean equals variance; rare-event connection to Binomial | Number of events in a fixed time or space interval |
| **Geometric** | Waiting time until first success; memoryless property; mean and variance derivation | Number of trials until first success |
| **Hypergeometric** | Sampling without replacement from a finite population | Quality control, card drawing, finite-population sampling |
| **Simulation check** | Comparing theoretical probabilities to simulated frequencies | Sanity-checking discrete probability models in code |

### Continuous Distributions

| Distribution | What to Focus On | Typical Use Case |
| ------------ | ---------------- | ---------------- |
| **Normal** | Bell shape, z-scores, percentiles, empirical rule, visualization | Continuous measurements and the foundation of many tests |
| **t-distribution** | Heavier tails, degrees of freedom, critical values | Small-sample mean inference when population SD is unknown |
| **Chi-square (χ²)** | Sum of squared standard normals; right-skewed shape | Variance tests, goodness-of-fit, independence tests |
| **F-distribution** | Ratio of scaled Chi-square variables | Comparing variances, ANOVA, regression F-tests |
| **Exponential** | Waiting time between Poisson events; memoryless property | Time-to-event and interarrival-time modeling |
| **Uniform** | Equal density over a bounded interval | Random number generation and simple bounded uncertainty |
| **Family relationships** | How Normal, t, Chi-square, F, and Exponential connect | Helps explain why these distributions appear in inference |

### Sampling Distributions & CLT

| Topic | What to Focus On | Why It Matters |
| ----- | ---------------- | -------------- |
| Sample vs population | Sample statistic vs population parameter; sampling error | Frames why inference is necessary |
| Sampling distribution of the mean | Repeated samples produce a distribution of $\bar{X}$ values | Shows that estimates vary from sample to sample |
| Central Limit Theorem | Sample means approach Normal as $n$ increases | Explains why Normal-based inference often works even for non-normal raw data |
| Mean of $\bar{X}$ | $E(\bar{X}) = \mu$ and its derivation | Shows that the sample mean is unbiased for the population mean |
| Standard Error | $SE = \sigma / \sqrt{n}$ | Measures precision of the sample mean and explains why larger samples help |
| Unknown $\sigma$ | Use the t-distribution when population SD is estimated with sample SD | Connects sampling distributions to one-sample t-tests |
| Sample proportions | $\hat{p}$ is approximately Normal under common conditions | Extends CLT reasoning from means to proportions |
| Bridge to inference | t-tests, z-tests, ANOVA, and confidence intervals rely on sampling distributions | Connects probability theory to inferential statistics |

### Monte Carlo Simulation

| Topic | What to Focus On | Why It Matters |
| ----- | ---------------- | -------------- |
| Core workflow | Define a random process, simulate it many times, summarize the results | Turns probability models into numerical estimates |
| Monte Carlo estimate | Approximate probabilities by repeated random sampling | Useful when exact formulas are inconvenient |
| Simulation error | Error shrinks roughly like $1 / \sqrt{n_{sim}}$ | Explains why more simulations reduce noise slowly |
| Monte Carlo vs bootstrap | Model-generated data vs resampling the observed sample | Separates probability simulation from uncertainty estimation |
| Bootstrap distribution | Resampled statistics form a distribution of plausible values | Builds intuition for confidence intervals around an estimate |
| Tail risk | Simulating rare or bad outcomes directly | Useful for risk questions where averages are not enough |
| Limitations | Model assumptions, rare-event noise, dependence, and false precision | Prevents overtrusting simulated output |

## Key Concepts at a Glance

| Concept             | One-Line Summary                                            |
| ------------------- | ----------------------------------------------------------- |
| **Probability**     | A number between 0 and 1 expressing likelihood              |
| **Random Variable** | A variable whose value is determined by a random process    |
| **PMF**             | Probability of each outcome for a discrete variable         |
| **PDF**             | Probability density at each point for a continuous variable |
| **CDF**             | Cumulative probability up to a given value                  |
| **Expected Value**  | The long-run average of a random variable                   |
| **Variance**        | How spread out the distribution is around the mean          |
| **CLT**             | Sample means approach normal distribution as n grows        |

## Key Takeaway

- Probability gives you a model of **uncertainty**.
- Distributions are templates that describe how random variables behave.
- Together, they allow you to go from _what I observed_ → _what is likely true in general_.
