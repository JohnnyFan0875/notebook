# Sampling and Central Limit Theorem (CLT)

Sampling is the foundation of **statistical inference** — it allows us to make conclusions about an entire population based on a manageable subset of data.

## 1. Introduction to Sampling

### 1.1 What Is Sampling?

Sampling is the process of selecting a subset (**sample**) from a larger set (**population**) to estimate characteristics of the population.

| Term               | Definition                           | Example                              |
| ------------------ | ------------------------------------ | ------------------------------------ |
| **Population**     | The entire group of interest         | All patients with diabetes in Taiwan |
| **Sample**         | A smaller subset of the population   | 500 randomly selected patients       |
| **Sampling Frame** | The actual list used for sampling    | National patient registry            |
| **Parameter**      | True but unknown population value    | μ (population mean)                  |
| **Statistic**      | Sample-based estimate of a parameter | x̄ (sample mean)                      |

### 1.2 Why Sampling Matters

- Reduces cost and time
- Enables feasible data collection
- Necessary for inferential statistics
- Allows quantification of uncertainty (via **standard error**, **confidence intervals**, and **hypothesis testing**)

**Key Idea:**  
Good sampling ensures representativeness — poor sampling introduces **bias**, which invalidates inference.

## 2. Types of Sampling

Sampling methods are generally divided into two major categories:

### 2.1 Probability Sampling

Every unit in the population has a known, non-zero probability of selection.

| Method                           | Description                                                  | Notes                                               |
| -------------------------------- | ------------------------------------------------------------ | --------------------------------------------------- |
| **Simple Random Sampling (SRS)** | Each unit has equal chance of selection                      | Most basic and unbiased                             |
| **Systematic Sampling**          | Select every k-th unit from a list                           | Simpler to implement, but beware of hidden patterns |
| **Stratified Sampling**          | Divide population into strata and sample from each           | Ensures representation across key subgroups         |
| **Cluster Sampling**             | Divide population into clusters and randomly sample clusters | Useful for geographically scattered populations     |

### 2.2 Non-Probability Sampling

Not all units have a known or equal chance of selection.

| Method                            | Description                         | Risk                                               |
| --------------------------------- | ----------------------------------- | -------------------------------------------------- |
| **Convenience Sampling**          | Based on ease of access             | High risk of bias                                  |
| **Judgmental/Purposive Sampling** | Based on researcher’s judgment      | Subjective selection                               |
| **Snowball Sampling**             | Recruited via participant referrals | Common in hidden populations (e.g., rare diseases) |

**Note:**  
Inferential statistics assume random sampling — non-probability methods limit generalizability.

## 3. Sampling Distribution

A **sampling distribution** is the probability distribution of a statistic (e.g., mean, proportion, correlation) calculated from all possible samples of a given size $ n $ from a population.

### 3.1 Sampling Distribution of the Mean

If we repeatedly sample from a population with mean $ \mu $ and standard deviation $ \sigma $:

$$
\bar{X} \sim N\!\left(\mu, \frac{\sigma}{\sqrt{n}}\right)
$$

- $ \mu $: population mean
- $ \sigma / \sqrt{n} $: **standard error** — variability of sample means
- As $ n $ increases → sampling distribution becomes narrower → estimates become more precise

## 4. Central Limit Theorem (CLT)

### 4.1 Definition

The **Central Limit Theorem** states that the sampling distribution of the sample mean approaches a **normal distribution** as the sample size $ n $ increases (typically n ≥ 30) — regardless of the shape of the original population.

$$
\bar{X} \xrightarrow{d} N(\mu, \frac{\sigma^2}{n}) \text{ as } n \to \infty
$$

### 4.2 Key Implications

| Concept                 | Implication                                                                  |
| ----------------------- | ---------------------------------------------------------------------------- |
| **Inference**           | Enables use of normal (z) or t distributions even for non-normal populations |
| **Standard Error**      | Justifies why $ SE = \frac{s}{\sqrt{n}} $ quantifies uncertainty             |
| **Confidence Interval** | Validates construction of CIs using sample statistics                        |
| **Hypothesis Testing**  | Allows test statistics to follow known distributions under H₀                |

### 4.3 Relationship with the Law of Large Numbers (LLN)

- **LLN:** Sample mean → converges to population mean as n increases (consistency).
- **CLT:** Distribution of sample mean → approaches normal (shape).

Together, they explain _why and how_ inference works.

## 5. Bootstrapping (Resampling Approach)

When the population distribution is unknown or the sample size is limited, we can approximate the sampling distribution by **resampling with replacement** from the sample — called **bootstrapping**.

| Application                    | Purpose                                            |
| ------------------------------ | -------------------------------------------------- |
| Estimate standard errors       | Variability of estimates without analytic formulas |
| Construct confidence intervals | Percentile-based or bias-corrected methods         |
| Evaluate model stability       | Check robustness across resampled datasets         |

### Example Workflow

1. Draw a bootstrap sample (same size as original, with replacement)
2. Compute statistic (e.g., mean, median)
3. Repeat many times (e.g., 1000–10,000)
4. Use distribution of bootstrap statistics to estimate SE or CI

## 6. Python Examples

### 6.1 Demonstrate Sampling Distribution and CLT

```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Simulate a non-normal population (exponential)
population = np.random.exponential(scale=2.0, size=100000)

# Draw multiple random samples and compute means
sample_size = 50
n_samples = 1000
sample_means = [np.mean(np.random.choice(population, size=sample_size)) for _ in range(n_samples)]

# Plot sampling distribution of the means
sns.histplot(sample_means, kde=True, color="steelblue")
plt.title(f"Sampling Distribution of the Mean (n={sample_size})")
plt.xlabel("Sample Mean")
plt.show()
```

### 6.2 Bootstrap Example

```python
# One bootstrap example using replacement
sample = np.random.choice(population, size=100, replace=False)
boot_means = [np.mean(np.random.choice(sample, size=100, replace=True)) for _ in range(1000)]

sns.histplot(boot_means, kde=True, color="orange")
plt.title("Bootstrap Distribution of the Mean")
plt.xlabel("Bootstrap Sample Mean")
plt.show()
```

## 7. Common Pitfalls

| Issue                                   | Description                                           | Consequence                      |
| --------------------------------------- | ----------------------------------------------------- | -------------------------------- |
| **Non-representative sample**           | Sampling bias or poor design                          | Invalid inference                |
| **Small sample size**                   | CLT may not hold                                      | Non-normal sampling distribution |
| **Ignoring sampling design**            | Treating cluster or stratified sampling as SRS        | Underestimated standard errors   |
| **Confusing statistics vs. parameters** | Using sample metrics as if they were population truth | Misleading conclusions           |

## 8. Summary

- Sampling connects data collection to inference — it allows us to estimate population parameters efficiently.
- The Central Limit Theorem (CLT) justifies why normal approximations work and why the standard error is a valid measure of uncertainty.
- Bootstrapping provides a flexible alternative when analytic assumptions are difficult to meet.
- Proper sampling design and sufficient sample size are essential for valid and robust statistical inference.
