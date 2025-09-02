# Sampling and Statistical Inference

## 1. Introduction to Sampling

Sampling is the process of selecting a subset (a sample) from a larger population to estimate characteristics of the whole population. It is a cornerstone of statistical inference and allows for analysis when a full population census is impractical.

### 1.1 Why Sampling Matters

- Reduces cost and time
- Enables feasible data collection
- Necessary for inferential statistics

### 1.2 Key Concepts

- **Population**: The entire group you're interested in studying
- **Sample**: A subset of the population
- **Sampling Frame**: A list from which the sample is actually drawn
- **Sampling Bias**: Systematic error due to non-representative sampling

## 2. Types of Sampling

### 2.1 Probability Sampling

Every member of the population has a known, non-zero probability of being selected.

- **Simple Random Sampling (SRS)**: Every unit has equal probability
- **Systematic Sampling**: Select every k-th unit from a list
- **Stratified Sampling**: Divide population into strata and sample from each
- **Cluster Sampling**: Divide population into clusters and sample entire clusters

### 2.2 Non-Probability Sampling

Not every unit has a known or equal chance of being selected.

- **Convenience Sampling**
- **Judgmental or Purposive Sampling**
- **Snowball Sampling**

## 3. Central Limit Theorem (CLT)

The CLT states that the sampling distribution of the sample mean approaches a normal distribution as the sample size increases, regardless of the population's distribution.

### Key Implications:

- Enables use of normal distribution in hypothesis testing
- Justifies use of standard errors and confidence intervals

## 4. Sampling Distribution

A sampling distribution is the probability distribution of a given statistic based on a random sample.

- Most commonly: Sampling distribution of the mean
- Important in estimating standard errors and confidence intervals

## 5. Bootstrapping

A resampling technique used to estimate statistics on a population by sampling a dataset with replacement.

### Applications:

- Estimate standard errors
- Construct confidence intervals
- Evaluate model stability

## 6. Python Code Examples (Conceptual)

```python
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Simulate population
population = np.random.exponential(scale=2.0, size=10000)

# Sample
sample = np.random.choice(population, size=100, replace=False)
sample_boot = np.random.choice(sample, size=100, replace=True)

# Bootstrap resampling
boot_means = [np.mean(sample_boot) for _ in range(1000)]

# Plotting
sns.histplot(boot_means, kde=True)
plt.title("Bootstrap Distribution of the Mean")
plt.xlabel("Sample Mean")
plt.show()
```

## 7. Common Pitfalls

- Using non-representative samples
- Ignoring sampling bias
- Small sample sizes undermining CLT
- Confusing sample statistics with population parameters

## 8. Summary

Sampling enables generalization from a subset to a population. Mastering sampling strategies and the central limit theorem is crucial for valid inference and accurate predictive modeling.
