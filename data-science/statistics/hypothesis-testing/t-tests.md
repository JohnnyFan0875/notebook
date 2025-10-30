# t-tests

- The **t-test** family of statistical tests compares means to determine whether differences are statistically significant.
- They are widely used for small sample sizes and when the **population standard deviation ($\sigma$) is unknown**.
- Please refer to [t-score](t-z-score.md#t-score) for basic definition.

## Comparison: t-test vs z-test

- **z-test**: Used when the population standard deviation ($\sigma$) is **known**, usually with large samples ($n ≥ 30$).
- **t-test**: Used when $\sigma$ is **unknown** (typical case), especially with small samples ($n < 30$).

## One-Sample t-test

- **Purpose:** Compare the sample mean to a known population mean.
- **Example:** Whether the average test score of a class differs from the expected mean of 75.

**Assumptions:**

- Independence of observations
- Normality of data (important for small samples; CLT helps when $n ≥ 30$)(if not, use [one-sample Wilcoxon Signed-Rank Test](./non-parametric-tests.md#one-sample-wilcoxon-signed-rank-test))

**Formula:**

$$
t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}
$$

- $\bar{x}$: sample mean  
- $\mu_0$: hypothesized (population) mean  
- $s$: sample standard deviation  
- $n$: sample size  

**Python Example:**

```python
from scipy import stats

data = [23, 21, 19, 22, 20, 23, 21, 20, 22, 21]
population_mean = 20

t_statistic, p_value = stats.ttest_1samp(data, population_mean)
print(t_statistic, p_value)
```

## Two-Sample t-test (Independent Samples)

- **Purpose:** Compare means of two independent groups.
- **Assumptions:**
  - Independence of groups
  - Normality of both groups (CLT helps if n is large)
  - Equal variance (if not, use Welch’s t-test)

**Formula:**

$$
t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}
$$

- $\bar{x}_1, \bar{x}_2$: sample means
- $s_1, s_2$: standard deviations
- $n_1, n_2$: sample sizes

**Alternatives:**

| Situation                                                                                    | Test                                                                                                     |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| data roughly follow a **normal distribution** but have **unequal variances or sample sizes** | **Welch’s t-test**                                                                                       |
| data are **non-normal** (e.g., skewed, ordinal, or contain outliers)                         | [Mann–Whitney U test](./non-parametric-tests.md#mannwhitney-u-test-wilcoxonmannwhitney) (non-parametric) |

**Python Example:**

```python
sample_1 = [23, 21, 19, 22, 20, 23, 21, 20, 22, 21]
sample_2 = [30, 28, 29, 32, 31, 30, 33, 29, 30, 32]

t_statistic, p_value = stats.ttest_ind(sample_1, sample_2, equal_var=True)
print(t_statistic, p_value)
```

- `equal_var=False` for Welch's t-test

## Paired Sample t-test (Dependent Samples)

- **Purpose:** Compare means of two related groups (before–after, matched pairs).
- **Assumptions:**
  - Independence between pairs
  - Differences approximately normally distributed (important for small n, CLT helps for larger n)

**Formula:**

$$
t = \frac{\bar{d} - \mu_d}{s_d / \sqrt{n}}
$$

- $\bar{d}$: mean of differences
- $\mu_d$: hypothesized difference (often 0)
- $s_d$: standard deviation of differences
- $n$: number of pairs

**Python Example:**

```python
group_1 = [23, 21, 19, 22, 20, 23, 21, 20, 22, 21]  # Before
group_2 = [30, 28, 29, 32, 31, 30, 33, 29, 30, 32]  # After

t_statistic, p_value = stats.ttest_rel(group_1, group_2)
print(t_statistic, p_value)
```
