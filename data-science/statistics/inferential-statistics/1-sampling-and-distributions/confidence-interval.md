# Confidence Intervals

A **confidence interval (CI)** provides a range of plausible values for a population parameter, based on sample data.  
It reflects the degree of uncertainty around an estimate.

- Relationship with sampling distribution:
  - The confidence interval for the mean is derived from the **sampling distribution of the sample mean**.
  - When we repeatedly take samples of size $n$ from a population with mean $\mu$ and standard deviation $\sigma$, the sample means $\bar{x}$ follow an approximately **normal distribution** (by the Central Limit Theorem)

## 1. Concept Overview

| Concept                                                                    | Meaning                                                               |
| -------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **Confidence Interval (CI)**                                               | Range of plausible values for a population parameter                  |
| [**Confidence Level (1 − α)**](#3-confidence-level)                        | The proportion of repeated CIs expected to contain the true parameter |
| [**Significance Level (α)**](../hypothesis-testing/significance-levels.md) | The complement of the confidence level (α = 1 − confidence level)     |

## 2. Formula for the Mean

| Case                                      | Formula for Confidence Interval of the Mean           | Distribution Used                    |
| ----------------------------------------- | ----------------------------------------------------- | ------------------------------------ |
| **Population standard deviation known**   | $\text{CI} = \bar{x} \pm z \times \frac{σ}{\sqrt{n}}$ | **Standard Normal (z-distribution)** |
| **Population standard deviation unknown** | $\text{CI} = \bar{x} \pm t \times \frac{s}{\sqrt{n}}$ | **Student’s t-distribution**         |

- $\bar{x}$: sample mean
- $σ$: population standard deviation
- $s$: sample standard deviation
- $n$: sample size
- [**z / t**](../hypothesis-testing/t-z-score.md): critical value corresponding to the desired confidence level

## 3. Confidence Level

The **confidence level** represents the degree of certainty that a particular estimate includes the true population parameter.  
對這個『估計方法』有多少信心，若重複做很多次實驗，有這個比例的信賴區間會包含真實答案。

- Confidence level = $1 − α$, where α is the significance level.
- Common choices:
  - 95% confidence level → α = 0.05
  - 99% confidence level → α = 0.01
- Interpretation:
  - If we repeat the same study many times, approximately 95% (or 99%) of the calculated confidence intervals would contain the true parameter.
  - It does **not** mean that there is a 95% probability the true parameter is in a specific interval (the parameter is fixed, the interval varies).
    - 想像射箭 100 次，每次都畫一個區間（信賴區間）去「包住靶心」。95 次成功包到靶心表示方法的「信心」是 95%。但單看其中一個箭圈（某一次的區間）時，靶心不是「有 95% 機率在圈裡」，而是要嘛在裡面、要嘛不在裡面。

## 4. Components of CI

$$
E =
\begin{cases}
z \times \frac{\sigma}{\sqrt{n}} & \text{if population SD (}\sigma\text{) is known} \\
t \times \frac{s}{\sqrt{n}} & \text{if population SD (}\sigma\text{) is unknown}
\end{cases}
$$

$$
\text{CI} = \bar{x} \pm E
$$

$$
CI =
\begin{cases}
\bar{x} \pm SE & \text{if population SD (}\sigma\text{) is known} \\
\bar{x} \pm SE & \text{if population SD (}\sigma\text{) is unknown}
\end{cases}
$$

- [Standard Error](./standard-error.md) ($SE$): variability between sample means
- Margion of Error ($E$): the maximum expected difference between the sample mean and the true population mean

## 5. Interpretation and Visualization

- How confident we are that the interval contains the true population parameter  
  有多少的信心 (機率) 此信賴區間包含真實的母體參數
- Wider intervals → lower precision (often due to smaller sample size or higher variability).
- For a **95%** confidence level, Z-score ≈ 1.96. The lower and upper bounds correspond to the **2.5th** and **97.5th** percentiles of the sampling distribution of the mean.

<p align="center">
  <img src="https://miro.medium.com/v2/resize:fit:1100/format:webp/1*zhq4V275F0YthnSLYRU0FA.jpeg" width="500" height="300">
</p>

## 6. Python Examples

從一個母體（population）中重複抽樣，每次抽取 50 個樣本，總共重複 1000 次。
每次抽樣後都計算該樣本的平均值，得到 1000 個樣本平均（`sample means`）。
這 1000 個樣本平均的平均值（`sample_mean`）會非常接近母體的真實平均數。
而 `quantile_2_5` 和 `quantile_97_5` 則代表這些樣本平均的第 2.5 與第 97.5 百分位數，也就是說，約有 95% 的樣本平均值會落在這兩個數值之間。
這個區間描述的是「樣本平均的抽樣分布（sampling distribution） 的 95% 範圍」。

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

```python
import numpy as np
from scipy import stats

data = [23, 21, 19, 22, 20, 23, 21, 20, 22, 21]
mean = np.mean(data)
sem = stats.sem(data)  # standard error of the mean (sem)
confidence = 0.95

ci = stats.t.interval(confidence, len(data)-1, loc=mean, scale=sem) # df = len(data)-1
print("95% confidence interval:", ci)
```

## 7. Summary

- Confidence intervals provide a range of plausible values for a parameter.
- Confidence level (1 − α) sets the degree of certainty.
- Narrower intervals indicate higher precision (larger n or lower variance).
- Always report CIs alongside [p-values](../hypothesis-testing/p-value.md) and [effect sizes](./effect-size.md) for robust interpretation.
