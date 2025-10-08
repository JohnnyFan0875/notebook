# t-score and z-score

Both the **t-score** and **z-score** are standardized test statistics that measure how many standard deviations a value is from the mean.  
They are used in hypothesis testing and confidence interval estimation.

## General Notes

- **In hypothesis tests (z-test, t-test):** how many standard deviations a sample mean (or observation) is from the hypothesized population mean.
- **In confidence intervals:** how far to extend around a sample statistic (like the sample mean) to capture a specified level of confidence (e.g., 95%).
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
- As \(n \to \infty\), the t-distribution approaches the normal distribution → t and z become nearly identical.

## Critical Value from Confidence Level

The critical z-value for a given confidence level is calculated as:

$$
z\_{\alpha/2} = \texttt{stats.norm.ppf}\left(1 - \frac{1 - \text{confidence level}}{2}\right)
$$

Example: For 95% confidence ($\alpha = 0.05$):

$$
z\_{0.025} = \texttt{stats.norm.ppf}(0.975) \approx 1.96
$$

```python
from scipy import stats

confidence = 0.95
alpha = 1 - confidence
z_alpha_over_2 = stats.norm.ppf(1 - alpha/2)
print(z_alpha_over_2)  # ~1.96
```

## Interpretation

- In a **hypothesis test**: measures how extreme your observed sample statistic is under $H_0$.
- In a **confidence interval**: determines how far to extend around the sample mean to capture a specified confidence level.

## Comparison: t-test vs z-test

- **z-test**: Used when the **population standard deviation ($\sigma$) is known**, usually with **large samples ($n ≥ 30$)**.
- **t-test**: Used when $\sigma$ is **unknown** (typical case), especially with **small samples ($n < 30$)**.
