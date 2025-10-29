# t-score and z-score

Both the **t-score** and **z-score** are standardized test statistics that measure how many standard deviations a value is from the mean.  
樣本平均數 $\bar{x}$ 離母體平均數 $𝜇$ 有幾個標準誤（SE）那麼遠  
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
- As $n \to \infty$, the t-distribution approaches the normal distribution → t and z become nearly identical.

## Critical Value from Confidence Level

| Test Type                                              | Formula                                                                                           | Example                                                                                                                                                          | Interpretation                                                                              |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **Two-Tailed Test** (Default for Confidence Intervals) | $ z\_{\alpha/2} = \texttt{stats.norm.ppf}\left(1 - \frac{1 - \text{confidence level}}{2}\right) $ | **For 95% confidence:** $ z*{\alpha/2} = \texttt{stats.norm.ppf}(0.975) = +1.96 $ <br> **Left-tail:** $ -z*{\alpha/2} = -1.96 = \texttt{stats.norm.ppf}(0.025) $ | Used when testing for **any significant difference** (either higher or lower).              |
| **Right-Tailed Test**                                  | $ z\_{\alpha} = \texttt{stats.norm.ppf}(1 - \alpha) $                                             | **For α = 0.05:** $ z\_{\alpha} = \texttt{stats.norm.ppf}(0.95) = +1.645 $                                                                                       | Used when testing if the sample mean is **significantly greater** than the population mean. |
| **Left-Tailed Test**                                   | $ z\_{\alpha} = \texttt{stats.norm.ppf}(\alpha) $                                                 | **For α = 0.05:** <br> $ z\_{\alpha} = \texttt{stats.norm.ppf}(0.05) = -1.645 $                                                                                  | Used when testing if the sample mean is **significantly less** than the population mean.    |

### Summary of Common Critical Values

| Confidence Level | α    | Tail(s)      | Cumulative Probability | Critical z-value |
| ---------------- | ---- | ------------ | ---------------------- | ---------------- |
| 90%              | 0.10 | Two-tailed   | 0.95                   | ±1.645           |
| 95%              | 0.05 | Two-tailed   | 0.975                  | ±1.960           |
| 99%              | 0.01 | Two-tailed   | 0.995                  | ±2.576           |
| 95%              | 0.05 | Right-tailed | 0.95                   | +1.645           |
| 95%              | 0.05 | Left-tailed  | 0.05                   | −1.645           |


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
