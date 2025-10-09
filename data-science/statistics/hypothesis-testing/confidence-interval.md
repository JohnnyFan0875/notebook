# Confidence Intervals

A **confidence interval (CI)** provides a range of plausible values for a population parameter, based on sample data.  
It reflects the degree of uncertainty around an estimate.

👉 See also: [Significance and Confidence Levels](significance-and-confidence-levels.md#confidence-level-1--α)

## Formula for the Mean

$$
\text{CI} = \bar{x} \pm z \times \frac{s}{\sqrt{n}}
$$

- $\bar{x}$: sample mean
- $s$: sample standard deviation
- $n$: sample size
- $z$: critical value from the normal distribution (e.g., 1.96 for 95% confidence)

## Interpretation

- **How confident we are that the interval contains the true population parameter**  
  有多少的信心 (機率) 此信賴區間包含真實的母體參數

- Uses of confidence intervals:

  - Estimate a **true population parameter**
  - Compare the **difference between two groups** in a sample population

- **Margin of Error**:

$$
\text{Margin of Error} = \text{Critical Value (t or z)} \times \text{Standard Error}
$$

- For a 95% confidence level:

  - Z-score ≈ 1.96
  - The lower and upper bounds correspond to the **2.5th and 97.5th percentiles** of the sampling distribution of the mean.

- Wider intervals → lower precision (often due to smaller sample size or higher variability).

## Python Example (Simulation)

```python
import numpy as np

# Step 1: Generate a population
population = np.random.normal(loc=100, scale=15, size=10000)  # Mean=100, SD=15

# Step 2: Simulate the sampling distribution
sample_size = 50
n_samples = 1000

sample_means = []
for _ in range(n_samples):
    sample = np.random.choice(population, size=sample_size, replace=False)
    sample_means.append(np.mean(sample))

sample_means = np.array(sample_means)

# Step 3: Compute CI from percentiles
quantile_2_5 = np.percentile(sample_means, 2.5)   # Lower bound
quantile_97_5 = np.percentile(sample_means, 97.5) # Upper bound
sample_mean = np.mean(sample_means)

print(f"Sample Mean of Sampling Distribution: {sample_mean:.2f}")
print(f"95% Confidence Interval: ({quantile_2_5:.2f}, {quantile_97_5:.2f})")
```

## Python Example (Analytical)

```python
import numpy as np
from scipy import stats

data = [23, 21, 19, 22, 20, 23, 21, 20, 22, 21]
mean = np.mean(data)
sem = stats.sem(data)  # standard error
confidence = 0.95

ci = stats.t.interval(confidence, len(data)-1, loc=mean, scale=sem)
print("95% confidence interval:", ci)
```

## Summary

- Confidence intervals provide a range of plausible values for a parameter.
- Confidence level (1 − α) sets the degree of certainty.
- Narrower intervals indicate higher precision (larger n or lower variance).
- Always report CIs alongside p-values and effect sizes for robust interpretation.
