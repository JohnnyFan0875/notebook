#### Standard Error

The **Standard Error (SE, 標準誤)** quantifies how much a **sample statistic** (such as the sample mean) would vary if we repeatedly drew samples from the same population.

- It represents the **standard deviation of a sampling distribution** — that is, the variability of an estimator, not of individual data points.
- 標準誤代表「樣本平均」在不同抽樣下會變動多少。若不斷重複抽樣，每次都算平均數，這些平均值會圍繞在母體平均數附近，形成分佈。這個分佈的標準差，就是標準誤。

> - **Standard deviation (SD)** → describes variability _within_ a sample.
> - **Standard error (SE)** → describes variability _between_ sample means.

## 1. Concept

When we repeatedly take samples of size $ n $ from a population with mean $\mu$ and standard deviation $\sigma$, the sample means $\bar{x}$ form a [**sampling distribution**](./sampling-and-clt.md#31-sampling-distribution-of-the-mean). The standard deviation of this distribution — the spread of the sample means — is called the **standard error**.

$$
SE =
\begin{cases}
\dfrac{\sigma}{\sqrt{n}} & \text{if population SD (}\sigma\text{) is known} \\
\dfrac{s}{\sqrt{n}} & \text{if population SD (}\sigma\text{) is unknown}
\end{cases}
$$

As sample size increases, $SE$ decreases. Larger samples yield more stable and precise estimates of the population mean.

## 2. Relationship Between SD and SE

| Concept                     | Symbol               | Represents                             | Depends on                | Typical Use            |
| --------------------------- | -------------------- | -------------------------------------- | ------------------------- | ---------------------- |
| **Standard Deviation (SD)** | $s$                  | Variability of individual observations | Population or sample data | Descriptive statistics |
| **Standard Error (SE)**     | $\frac{s}{\sqrt{n}}$ | Variability of sample means            | Sample size $n$         | Inferential statistics |

## 3. Connection to Sampling Distribution

- The **Law of Large Numbers** ensures that as $n$ increases, sample means converge toward the true mean $\mu$.
- The **Central Limit Theorem (CLT)** tells us that the distribution of sample means becomes approximately normal for large $n$.
- The **Standard Error** gives the spread of that normal distribution.

## 5. Relation to Confidence Interval and Hypothesis Testing

- [Confidence Interval](./confidence-interval.md):

$$
CI = \bar{x} \pm z_{\alpha/2} \times SE
$$

SE determines the **width** of the interval (precision of estimate).

- Hypothesis Test (e.g., t-test):

$$
t = \frac{\bar{x} - \mu_0}{SE}
$$

SE determines the **test statistic’s scale**, affecting the p-value.  
Smaller SE → narrower CI and larger t → easier to detect significant differences.

## 6. Python Example

```python
import numpy as np
from scipy import stats

data = np.array([21, 23, 22, 20, 24, 21, 23, 22, 25, 21])
n = len(data)
sample_std = np.std(data, ddof=1)
se = sample_std / np.sqrt(n)

print("Sample SD:", sample_std)
print("Standard Error:", se)
```

```python
import numpy as np
import matplotlib.pyplot as plt

pop = np.random.normal(100, 15, 100000)
sample_sizes = [5, 10, 30, 100]
ses = []

for n in sample_sizes:
    means = [np.mean(np.random.choice(pop, n)) for _ in range(1000)]
    ses.append(np.std(means, ddof=1))

plt.plot(sample_sizes, ses, marker='o')
plt.xlabel("Sample Size (n)")
plt.ylabel("Standard Error")
plt.title("Effect of Sample Size on Standard Error")
plt.show()
```
