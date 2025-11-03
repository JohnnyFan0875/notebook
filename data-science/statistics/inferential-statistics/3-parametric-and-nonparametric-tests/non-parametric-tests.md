# Non-parametric Tests

Non-parametric tests are used when data do **not meet the assumptions** of parametric tests (e.g., normality, homogeneity of variance).  
They are based on **ranks** instead of raw values, making them more robust for skewed distributions, ordinal data, or small samples.

## Wilcoxon Signed-Rank Test

- **Purpose:** Non-parametric alternative to the paired t-test.
- **Use case:** Compare two related samples (e.g., before–after design).
- **Null hypothesis (H₀):** Median difference between pairs = 0.

**Python Example:**

```python
from scipy import stats

before_treatment = [5, 7, 6, 9, 8]
after_treatment = [6, 8, 7, 10, 9]

statistic, p_value = stats.wilcoxon(before_treatment, after_treatment)
print("Wilcoxon statistic:", statistic, "p-value:", p_value)
```

## One-Sample Wilcoxon Signed-Rank Test

- **Purpose:** Non-parametric alternative to the one-sample t-test.
- **Use case:** Compare a single sample median against a hypothesized value (default is 0).
- **Null hypothesis (H₀):** Median of the differences between sample values and the hypothesized value = 0.

**Python Example:**

```python
from scipy import stats

sample_data = [6, 8, 7, 10, 9]
hypothesized_median = 7

# Calculate difference from hypothesized median
differences = [x - hypothesized_median for x in sample_data]

statistic, p_value = stats.wilcoxon(differences)
print("Wilcoxon statistic:", statistic, "p-value:", p_value)
```

### Mann–Whitney U Test (Wilcoxon–Mann–Whitney)

- **Purpose:** Non-parametric alternative to the two-sample t-test.
- **Use case:** Compares two independent groups.
- **Null hypothesis (H₀):** The two groups come from the same distribution.

```python
from scipy import stats

group_1 = [23, 21, 19, 22, 20]
group_2 = [30, 28, 29, 32, 31]

statistic, p_value = stats.mannwhitneyu(group_1, group_2, alternative="two-sided")
print("Mann–Whitney U statistic:", statistic, "p-value:", p_value)
```

### Kruskal–Wallis Test

- **Purpose:** Non-parametric alternative to one-way ANOVA.
- **Use case:** Compares >2 independent groups.
- **Null hypothesis (H₀):** All groups come from the same distribution.

```python
from scipy import stats

group1 = [20, 22, 23, 21, 24]
group2 = [30, 31, 32, 29, 33]
group3 = [15, 16, 14, 17, 15]

statistic, p_value = stats.kruskal(group1, group2, group3)
print("Kruskal–Wallis statistic:", statistic, "p-value:", p_value)
```
