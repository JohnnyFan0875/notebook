# Confidence Intervals

A **confidence interval (CI)** provides a range of plausible values for a population parameter, based on sample data.  
It reflects the degree of uncertainty around an estimate.

👉 See also: [Significance and Confidence Levels](significance-and-confidence-levels.md#confidence-level-1--α)

## Formula for the Mean

| Case                                                            | Formula for Confidence Interval of the Mean           | Distribution Used            |
| --------------------------------------------------------------- | ----------------------------------------------------- | ---------------------------- |
| **Population standard deviation known**                         | $\text{CI} = \bar{x} \pm z \times \frac{s}{\sqrt{n}}$ | **Standard Normal (z)**      |
| **Population standard deviation unknown** (use sample SD ( s )) | $\text{CI} = \bar{x} \pm t \times \frac{s}{\sqrt{n}}$ | **Student’s t-distribution** |

- $\bar{x}$: sample mean
- $s$: sample standard deviation
- $n$: sample size
- $z$: critical value from the normal distribution (e.g., 1.96 for 95% confidence)

### Relationship Between Sampling Distribution, Standard Error, and Margin of Error

The confidence interval for the mean is derived from the **sampling distribution of the sample mean**.  
When we repeatedly take samples of size $n$ from a population with mean $\mu$ and standard deviation $\sigma$, the sample means $\bar{x}$ follow an approximately **normal distribution** (by the Central Limit Theorem):

$$
\bar{x} \sim N\!\left(\mu, \frac{\sigma}{\sqrt{n}}\right)
$$

The standard deviation of this sampling distribution, $\frac{\sigma}{\sqrt{n}}$, is called the [Standard Error of the Mean (SE)](../descriptive-statistics.md#3-standard-error-se) — it quantifies how much sample means vary across repeated samples.

$$
SE = \frac{s}{\sqrt{n}}
$$

Because 95% of values in a normal distribution fall within ±1.96 standard deviations of the mean, we can write:

$$
P\!\left(\bar{x} - 1.96 \frac{\sigma}{\sqrt{n}} < \mu < \bar{x} + 1.96 \frac{\sigma}{\sqrt{n}}\right) = 0.95
$$

Rearranging gives the **95% confidence interval for the mean**:

$$
\text{CI} = \bar{x} \pm (z \text{ or } t) \times SE
$$

The term $(z \text{ or } t) \times SE$ is known as the **Margin of Error (E)** —  
the maximum expected difference between the sample mean and the true population mean:

$$
E = (z \text{ or } t) \times \frac{s}{\sqrt{n}}
$$

Thus, the general expression for a confidence interval is:

$$
\text{CI} = \bar{x} \pm E
$$

- Use **z** when the population standard deviation (\(\sigma\)) is known or \(n\) is large.
- Use **t** when \(\sigma\) is unknown and estimated by the sample standard deviation (\(s\)).

## Interpretation

- **How confident we are that the interval contains the true population parameter**  
  有多少的信心 (機率) 此信賴區間包含真實的母體參數

- Uses of confidence intervals:

  - Estimate a **true population parameter**
  - Compare the **difference between two groups** in a sample population

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
