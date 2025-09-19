# Hypothesis Testing

Hypothesis testing is a framework to decide whether observed data provides enough evidence to reject a null hypothesis \(H_0\).

## General Notes

- **Null hypothesis (H₀):** No effect or no difference.
- **Alternative hypothesis (Hₐ):** There is an effect or difference.
- **p-value:** Probability of observing the data (or something more extreme) if H₀ is true.
- **α (significance level):** Threshold (commonly 0.05) to decide whether to reject H₀.
- **Test statistic:** A standardized value (z, t, or F) used to compute the p-value.

## t-test vs z-test

- **z-test**: Used when population standard deviation (\(\sigma\)) is known, usually with **large samples (n ≥ 30)**.
- **t-test**: Used when \(\sigma\) is unknown (which is typical), especially with **small samples (n < 30)**.

## One-Sample t-test

- **Purpose:** Compare the sample mean to a known population mean.
- **Example:** Whether the average test score of a class differs from the expected mean of 75.
- **Assumptions:**
  - Independence of observations
  - Normality of data (important for small samples, less so for n ≥ 30 due to CLT)

**Formula:**
\[
t = \frac{\bar{x} - \mu}{s / \sqrt{n}}
\]

- \(\bar{x}\): sample mean
- \(\mu\): population mean (hypothesized value)
- \(s\): sample standard deviation
- \(n\): sample size

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
\[
t = \frac{\bar{x}\_1 - \bar{x}\_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}
\]

- \(\bar{x}\_1, \bar{x}\_2\): sample means
- \(s_1, s_2\): standard deviations
- \(n_1, n_2\): sample sizes

**Alternatives:**

- Welch’s t-test (unequal variances)
- Mann–Whitney U test (non-parametric)

**Python Example:**

```python
sample_1 = [23, 21, 19, 22, 20, 23, 21, 20, 22, 21]
sample_2 = [30, 28, 29, 32, 31, 30, 33, 29, 30, 32]

t_statistic, p_value = stats.ttest_ind(sample_1, sample_2, equal_var=True)
print(t_statistic, p_value)
```

## Paired Sample t-test (Dependent Samples)

- **Purpose:** Compare means of two related groups (before–after, matched pairs).
- **Assumptions:**
  - Independence between pairs
  - Differences approximately normally distributed (important for small n, CLT helps for larger n)

**Formula:**
\[
t = \frac{\bar{d} - \mu_d}{s_d / \sqrt{n}}
\]

- \(\bar{d}\): mean of differences
- \(\mu_d\): hypothesized difference (often 0)
- \(s_d\): standard deviation of differences
- \(n\): number of pairs

**Python Example:**

```python
group_1 = [23, 21, 19, 22, 20, 23, 21, 20, 22, 21]  # Before
group_2 = [30, 28, 29, 32, 31, 30, 33, 29, 30, 32]  # After

t_statistic, p_value = stats.ttest_rel(group_1, group_2)
print(t_statistic, p_value)
```

## Proportion Test (z-test for proportions)

- **Purpose:** Test whether a sample proportion differs from a hypothesized value (one-sample), or whether two sample proportions differ.
- **Data type:** Binomial (success/failure, categorical).
- As n grows, binomial → normal distrubution (CLT). Use exact tests (binomial test, Fisher’s exact) for small n.

### One-Sample Proportion Test

- H₀: \(p = p_0\) (The population proportion is equal to the hypothesized proportion)
- Hₐ: \(p ≠ p0\) (two-tailed), \(p > p0\) (right tailed), \(p < p0\) (left tailed)
- Assumption: \(n\hat{p} ≥ 10\) and \(n(1-\hat{p}) ≥ 10\)

```python
from statsmodels.stats import proportion
p_0 = 0.5
count = np.array([60])
nobs = np.array([100])

z_stat, p_value = proportion.proportions_ztest(count, nobs, value=p_0)
print(z_stat, p_value)
```

### Two-Sample Proportion Test

- H₀: \(p_1 = p_2\) (The two proportions are equal)
- Hₐ: \(p1 ≠ p2\) (two-tailed) (The two proportions are not equal)
- Assumption: Each group must satisfy \(n_i \hat{p}\_i ≥ 10\) and \(n_i(1-\hat{p}\_i) ≥ 10\)

```python
from statsmodels.stats import proportion
count = np.array([60, 50])  # successes
nobs = np.array([100, 120]) # sample sizes

z_stat, p_value = proportion.proportions_ztest(count, nobs)
print(z_stat, p_value)
```

## ANOVA (Analysis of Variance)

- **Purpose:** Compare means across **three or more groups**.
- **Null hypothesis (H₀):** All group means are equal.
- **Alternative (Hₐ):** At least one group mean differs.
- **Assumptions:**
  - Independence of observations
  - Normality within each group
  - Equal variances across groups (if not → Welch’s ANOVA; if non-normal → Kruskal-Wallis test)

**Test statistic (F):**
\[
F = \frac{MS*{between}}{MS*{within}}
\]

- \(MS\_{between}\): variance between group means
- \(MS\_{within}\): variance within groups

### Interpretation of Results

- If **p-value ≤ α** → At least two groups differ significantly.
  - However, ANOVA alone cannot tell which groups are different → need **post-hoc tests**.
- If **p-value > α** → Fail to reject H₀ (all groups have equal means).
- With more groups → more pairwise comparisons → higher chance of Type I error (false positives). Adjustments are required.

### Python Example

```python
import pandas as pd
from scipy import stats
import pingouin as pg

group_1 = [23, 21, 19, 22, 20, 23, 21, 20, 22, 21]
group_2 = [30, 28, 29, 32, 31, 30, 33, 29, 30, 32]
group_3 = [25, 24, 23, 26, 25, 27, 24, 23, 22, 25]

# One-way ANOVA
f_statistic, p_value = stats.f_oneway(group_1, group_2, group_3)
print(f_statistic, p_value)

# With Pingouin
data = group_1 + group_2 + group_3
groups = ['Group 1'] * len(group_1) + ['Group 2'] * len(group_2) + ['Group 3'] * len(group_3)
df = pd.DataFrame({'data': data, 'group': groups})

pg.anova(data=df, dv="data", between="group")
```

### Post-hoc Analysis

When ANOVA is significant, **post-hoc tests** identify which groups differ.

- **Purpose:** Perform pairwise comparisons while controlling for inflated Type I error (false positives) from multiple testing.
- **Common methods:**

#### Tukey’s Honest Significant Difference (HSD) Test

```python
from statsmodels.stats.multicomp import pairwise_tukeyhsd

tukey_results = pairwise_tukeyhsd(df['data'], df['group'], alpha=0.05)
print(tukey_results)

# Example output:
# Tukey's HSD Test Results:
#    pairwise_comparisons  |   p-adj
#    --------------------------------
#     Group 1 vs Group 2   |  0.0024
#     Group 1 vs Group 3   |  0.10
#     Group 2 vs Group 3   |  0.03
```

#### Bonferroni Correction

- Adjusts significance level when performing multiple t-tests.
- More conservative but reduces false positives.

```python
from statsmodels.stats.multitest import multipletests

comparisons = [('Group 1', 'Group 2'), ('Group 1', 'Group 3'), ('Group 2', 'Group 3')]
p_values = []

for group1, group2 in comparisons:
    group1_data = eval(group1.lower().replace(' ', '_'))
    group2_data = eval(group2.lower().replace(' ', '_'))
    t_stat, p_val = stats.ttest_ind(group1_data, group2_data)
    p_values.append(p_val)

corrected_p_values = multipletests(p_values, alpha=0.05, method='bonferroni')[1]

for (group1, group2), corrected_p_val in zip(comparisons, corrected_p_values):
    print(f"{group1} vs {group2}: corrected p-value = {corrected_p_val:.4f}")
```

📌 **Summary:**

- ANOVA tests whether there is a difference among groups, but not which groups differ.
- Post-hoc analysis (Tukey’s HSD, Bonferroni, etc.) is essential when ANOVA is significant.
- Always adjust for multiple comparisons to avoid Type I error.

## Test Homogeneity of Variance

- **Definition:** Homogeneity of variance (**homoscedasticity**) means the variance within each group is constant across levels of a categorical variable.
- **Why important?**
  - ANOVA and t-tests assume equal variances across groups.
  - Violating this assumption can inflate Type I error rates or reduce test power.
- **Null hypothesis (H₀):** Variances across groups are equal.
- **Alternative hypothesis (Hₐ):** At least one group has a different variance.

### Levene’s Test

- Robust to non-normality.
- Preferred when data may not be normally distributed.

```python
from scipy import stats

group1 = [20, 22, 23, 21, 24]
group2 = [30, 31, 32, 29, 33]
group3 = [15, 16, 14, 17, 15]

statistic, p_value = stats.levene(group1, group2, group3)
print(statistic, p_value)
```

### Bartlett’s Test

- More powerful if data are normally distributed.
- Sensitive to deviations from normality.

```python
statistic, p_value = stats.bartlett(group1, group2, group3)
print(statistic, p_value)
```

📌 **Summary:**

- Use **Levene’s test** when unsure about normality.
- Use **Bartlett’s test** when data are approximately normal.
- If variances are unequal →
  - Use **Welch’s ANOVA** instead of regular ANOVA.
  - Use **Welch’s t-test** instead of Student’s t-test.

## Chi-square Tests

- **Purpose:** Determine whether there's a significant association between **categorical** variables.
- **Statistic:** Chi-square (\(\chi^2\)) values are always non-negative (≥ 0) and tests are always **right-tailed**.
- **Assumptions:**
  - Expected frequency assumption: \(n \cdot \hat{p} ≥ 5\) and \(n \cdot (1-\hat{p}) ≥ 5\) for each category.
  - Data are counts/frequencies (not percentages or continuous values).
  - Observations should be independent.

### Chi-square Test of Independence

- Tests association between two categorical variables.
- H₀: The two variables are independent.
- Hₐ: The two variables are not independent (association exists).
- Degrees of freedom = \((\text{rows} - 1) \times (\text{columns} - 1)\).

```python
from scipy.stats import chi2_contingency
import numpy as np
import pandas as pd

data = np.array([[30, 10, 15],
                 [20, 25, 10]])
df = pd.DataFrame(data,
                  columns=["Democrat", "Republican", "Independent"],
                  index=["Male", "Female"])

chi2_stat, p_value, dof, expected = chi2_contingency(data)
print(chi2_stat, p_value, dof, expected)
```

### Chi-square Goodness-of-Fit

- Tests whether the observed frequency distribution of a categorical variable matches a hypothesized distribution.
- H₀: The observed frequencies fit the expected distribution.
- Hₐ: The observed frequencies do not fit the expected distribution.
- Degrees of freedom = \(k - 1\) (k = number of categories).

```python
from scipy.stats import chisquare
import numpy as np

observed = np.array([11, 9, 10, 12, 8, 10])
expected = np.array([10, 10, 10, 10, 10, 10])

chi2_stat, p_value = chisquare(f_obs=observed, f_exp=expected)
print(chi2_stat, p_value)
```

## Non-parametric Tests

### Wilcoxon Signed-Rank Test

- Non-parametric alternative to paired t-test.
- Compares two related samples.

```python
statistic, p_value = stats.wilcoxon(before_treatment, after_treatment)
```

### Mann–Whitney U Test (Wilcoxon-Mann-Whitney)

- Non-parametric alternative to two-sample t-test.
- Compares two independent groups.

```python
statistic, p_value = stats.mannwhitneyu(group_1, group_2)
```

### Kruskal–Wallis Test

- Non-parametric alternative to one-way ANOVA.
- Compares >2 independent groups.

```python
stat, p_value = stats.kruskal(group1, group2, group3)
```

## Choosing the Right Test

- One group vs population mean → One-sample t-test / z-test
- Two independent groups → Two-sample t-test (Welch if variances unequal) / Mann–Whitney U
- Two related groups → Paired t-test / Wilcoxon signed-rank
- ≥ 3 groups → ANOVA / Kruskal–Wallis
- Categorical proportions → Proportion z-test / Chi-square tests

## Critical Notes

- Always check assumptions: normality, independence, equal variance.
- Use non-parametric alternatives for small samples or non-normal data.
- Report test name, statistic, degrees of freedom, p-value, and effect size (Cohen’s d, η², etc.).
- For multiple comparisons, apply corrections (Bonferroni, Tukey).
