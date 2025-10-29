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

## Other Non-parametric or Exact Tests

These tests are also **non-parametric**, but they focus on **categorical or count data** rather than continuous or ordinal ranks.

| Test                                                                    | Purpose                                                                                                                   | Data Type / Use Case                    | Corresponding File                               |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | ------------------------------------------------ |
| [**Binomial Test**](./binomial-test.md)                                 | Tests whether an observed proportion differs from a hypothesized value (exact probability from binomial distribution).    | Binary (success/failure, single sample) | [`binomial-test.md`](./binomial-test.md)         |
| [**Fisher’s Exact Test**](./fisher-exact-test.md)                       | Tests for association between two categorical variables in a 2×2 contingency table (exact test, valid for small samples). | Categorical (2×2 table)                 | [`fisher-exact-test.md`](./fisher-exact-test.md) |
| [**Chi-square Test**](./chi-square.md)                                  | Tests for association or goodness-of-fit between categorical variables (approximation for large samples).                 | Categorical (r×c table, frequencies)    | [`chi-square.md`](./chi-square.md)               |
| [**Proportion Tests (z-test)**](./proportion-tests.md)                  | Compares one or two sample proportions to hypothesized values (normal approximation of binomial).                         | Binary or categorical (large samples)   | [`proportion-tests.md`](./proportion-tests.md)   |
| [**Levene’s / Bartlett’s / Brown–Forsythe Tests**](./variance-tests.md) | Non-parametric or robust tests for equality of variances across groups (no strict normality assumption).                  | Continuous data (variance homogeneity)  | [`variance-tests.md`](./variance-tests.md)       |
