# t-score and z-score

Both the **t-score** and **z-score** are standardized test statistics that measure how many standard deviations a value is from the mean.  
樣本平均數 $\bar{x}$ 離母體平均數 $𝜇$ 有幾個標準誤（SE）那麼遠  
They are used in hypothesis testing and confidence interval estimation.

## General Notes

- The numerical value of a z-score or t-score may be the same, but the **interpretation differs** between contexts.

## z-score

When the **population standard deviation ($\sigma$) is known**:

$$
z = \frac{\bar{x} - \mu}{\sigma / \sqrt{n}}
$$

- $\bar{x}$: sample mean
- $\mu$: population mean (hypothesized value)
- $\sigma$: population standard deviation
- $n$: sample size

**Use cases:**

- Large sample size ($n ≥ 30$)
- Population standard deviation is known

**Example critical values:**

- 95% confidence → critical z = ±1.96
- 99% confidence → critical z = ±2.576

## t-score

When the **population standard deviation is unknown**, use the sample standard deviation $s$:

$$
t = \frac{\bar{x} - \mu}{s / \sqrt{n}}
$$

- $\bar{x}$: sample mean
- $\mu$: population mean (hypothesized value)
- $s$: sample standard deviation
- $n$: sample size

**Note**

- Same structure as z-score, but variability estimated from sample data.
- Used for **small sample sizes ($n < 30$)**.
- The **t-distribution** has heavier tails to account for uncertainty.
- As $n \to \infty$, the t-distribution approaches the normal distribution → t and z become nearly identical.

## Critical Value from Confidence Level

### Two-Tailed Test (Default for Confidence Intervals)

$$
z_{\alpha/2} = \texttt{stats.norm.ppf}\left(1 - \frac{\alpha}{2}\right)
$$

**Example (95% confidence):**

$$
z_{\alpha/2} = \texttt{stats.norm.ppf}(0.975) = +1.96
$$

The corresponding **left-tail** critical value is:

$$
-z_{\alpha/2} = -1.96
$$

$$
z_{\alpha/2} = \texttt{stats.norm.ppf}(0.025) = -1.96
$$

### Right-Tailed Test

Used when testing if the sample mean is **significantly greater** than the population mean.

$$
z_{\alpha} = \texttt{stats.norm.ppf}(1 - \alpha)
$$

**Example (α = 0.05):**

$$
z_{\alpha} = \texttt{stats.norm.ppf}(0.95) = +1.645
$$

### Left-Tailed Test

Used when testing if the sample mean is **significantly less** than the population mean.

$$
z_{\alpha} = \texttt{stats.norm.ppf}(\alpha)
$$

**Example (α = 0.05):**

$$
z_{\alpha} = \texttt{stats.norm.ppf}(0.05) = -1.645
$$

```python
from scipy import stats

confidence = 0.95
alpha = 1 - confidence
z_alpha_over_2 = stats.norm.ppf(1 - alpha/2)
print(z_alpha_over_2)  # ~1.96
```

## Interpretation

- In a **hypothesis test (z-test, t-test)**: how many standard deviations a sample mean (or observation) is from the hypothesized population mean.
- In a **confidence interval**: determines how far to extend around the sample mean to capture a specified confidence level (e.g., 95%).

## Comparison: t-test vs z-test

Please refer to [t-test vs z-test](./t-tests.md)
