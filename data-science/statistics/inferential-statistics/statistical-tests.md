# Common Statistical Tests

This section covers the most frequently used parametric hypothesis tests, organized by the **research question and data structure**. Each test has specific assumptions — always check them before running the test.

Key point: Test selection usually comes down to four things: outcome type, number of groups, whether samples are independent or paired, and whether the assumptions are reasonable.

## A Fast Decision Workflow

Before naming a test, walk through this sequence:

1. Is the outcome numerical or categorical?
2. How many groups or conditions are being compared?
3. Are observations independent, paired, or repeated?
4. Is the target parameter a mean, proportion, association, or distributional fit?
5. Are the main assumptions plausible enough for a parametric method?

Most test confusion comes from skipping step 3. The same two-group problem can lead to a completely different test depending on whether the samples are independent or paired.

## Test Selection Guide

**Three questions to ask before choosing a test:**

1. **What type is the outcome variable?** — Numerical / Categorical
2. **How many groups?** — 1 / 2 / 3+
3. **Are the groups independent or paired?** — Independent / Paired

### Numerical Outcome

| Research Question | Groups | Parametric Test | When Assumptions Fail |
| ------------------------------------------------ | ---------- | ---------------------------- | ------------------------------- |
| Sample mean vs. known value | 1 | One-sample t-test | One-sample Wilcoxon signed-rank |
| Two independent groups — means differ? | 2 | Independent t-test (Welch's) | Mann–Whitney U |
| Two related/paired measurements — means differ? | 2 (paired) | Paired t-test | Wilcoxon signed-rank |
| Three or more independent groups — means differ? | 3+ | One-way ANOVA | Kruskal–Wallis |
| Two factors + interaction effect? | 3+ | Two-way ANOVA | ART ANOVA / PERMANOVA |

Tip: Parametric tests usually rely on means, standard deviations, and approximate normality. Non-parametric tests work on ranks or signs and are better when data is ordinal, strongly non-normal, or very small. See the dedicated non-parametric module for those alternatives.

## Parametric vs. Non-parametric: A Better Rule

Do not treat non-parametric tests as "backup tests for when Shapiro fails". A better framing is:

| If your target is mostly about... | Prefer |
| --------------------------------- | ------ |
| Mean differences on roughly continuous data | Parametric tests |
| Median / rank differences, ordinal data, or highly skewed distributions | Non-parametric tests |
| Very small samples with binary outcomes | Exact tests |

Tip: With moderate-to-large samples, t-tests are often robust to mild non-normality. Severe skewness, extreme outliers, or ordinal scales matter more than blindly passing or failing one normality test.

### Categorical Outcome

| Research Question | Groups | Large Sample (n·p ≥ 5) | Small Sample / Low Counts |
| ---------------------------------------------------- | ------ | -------------------------- | ------------------------- |
| Sample proportion vs. known value | 1 | One-proportion z-test | Exact binomial test |
| Two groups — proportions differ? | 2 | Two-proportion z-test | Fisher's exact test |
| Association between two categorical variables (r×c)? | 2+ | Chi-square independence | Fisher's exact test |
| Observed frequencies match expected distribution? | 1 | Chi-square goodness-of-fit | Exact binomial test |

## One-Sample t-test

**Question**: Is the population mean equal to a specific hypothesized value μ₀?

**H₀**: μ = μ₀
**H₁**: μ ≠ μ₀ (two-tailed)

**When to use t vs. z:**

| Condition | Use |
| ------------------------ | ------ |
| σ known, n ≥ 30 | z-test |
| σ unknown (typical case) | t-test |

**Test statistic**:

\[
t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}
\]

**Assumptions:**

| Assumption | How to Check |
| ---------------------------------------------- | --------------------------------- |
| Data is continuous | Check data type |
| Observations are independent | Study design |
| Population is approximately normal (or n ≥ 30) | Histogram, Q-Q plot, Shapiro-Wilk |

```python
from scipy import stats
import numpy as np
from sklearn.datasets import load_iris

df = load_iris(as_frame=True).frame
x = df['sepal length (cm)']

mu_0 = 5.5  # hypothesized population mean

# Run one-sample t-test
t_stat, p_value = stats.ttest_1samp(x, popmean=mu_0)

n     = len(x)
x_bar = x.mean()
s     = x.std(ddof=1)
se    = s / np.sqrt(n)

print(f"n         = {n}")
print(f"x̄         = {x_bar:.4f}")
print(f"μ₀        = {mu_0}")
print(f"t-stat    = {t_stat:.4f}")
print(f"p-value   = {p_value:.4f}")
print(f"Decision  = {'Reject H₀' if p_value < 0.05 else 'Fail to Reject H₀'}")

# Cohen's d for one-sample
d = (x_bar - mu_0) / s
print(f"Cohen's d = {d:.4f}")
```

## Independent Samples t-test

**Question**: Do two independent groups have different population means?

**H₀**: μ₁ = μ₂
**H₁**: μ₁ ≠ μ₂

**Assumptions:**

| Assumption | How to Check |
| --------------------------------------------- | ------------------- |
| Both groups are continuous | Check data type |
| Groups are independent | Study design |
| Both approximately normal (or n ≥ 30 each) | Histogram, Q-Q plot |
| Equal variances (Welch's t-test relaxes this) | Levene's test |

Tip: Use Welch's t-test (`equal_var=False`) by default — it works even when variances are unequal, and performs nearly as well as the classic t-test when variances _are_ equal.

### Student's t-test vs. Welch's t-test

| Version | Assumes equal variances? | Good default? |
| ------- | ------------------------ | ------------- |
| Student's t-test | Yes | No |
| Welch's t-test | No | Yes |

Tip: In modern applied work, Welch's t-test is usually the safer default unless you have a strong reason to enforce equal variance.

**When to use which variant:**

| Situation | Test |
| ----------------------------------------------------- | ---------------------------------- |
| Normal data, variances unequal or sample sizes differ | Welch's t-test (`equal_var=False`) |
| Non-normal data, skewed, or outliers | Mann–Whitney U (see the non-parametric module) |

```python
from scipy import stats
import numpy as np
from sklearn.datasets import load_iris
import pandas as pd

iris = load_iris(as_frame=True)
df = iris.frame
df['species'] = iris.target_names[iris.target]

group1 = df[df['species'] == 'setosa']['sepal length (cm)']
group2 = df[df['species'] == 'versicolor']['sepal length (cm)']

# Check variance equality first (Levene's test)
levene_stat, levene_p = stats.levene(group1, group2)
print(f"Levene's test: stat={levene_stat:.4f}, p={levene_p:.4f}")
print(f"Variances {'are' if levene_p > 0.05 else 'are NOT'} equal")

# Welch's t-test (safer default — does not assume equal variances)
t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)
print(f"\nWelch's t-test: t={t_stat:.4f}, p={p_value:.4e}")
print(f"Decision: {'Reject H₀' if p_value < 0.05 else 'Fail to Reject H₀'}")

# Cohen's d
def cohens_d(g1, g2):
    n1, n2 = len(g1), len(g2)
    s_pooled = np.sqrt(((n1 - 1) * g1.std(ddof=1)**2 + (n2 - 1) * g2.std(ddof=1)**2) / (n1 + n2 - 2))
    return abs(g1.mean() - g2.mean()) / s_pooled

d = cohens_d(group1, group2)
print(f"Cohen's d = {d:.4f}  ({'large' if d >= 0.8 else 'medium' if d >= 0.5 else 'small'})")
```

## Paired t-test

**Question**: Do paired or matched measurements differ on average?

**Use when**: Each data point in group 1 is naturally matched with one in group 2 (e.g., before/after measurements on the same subjects, or matched pairs).

**H₀**: μ_diff = 0
**H₁**: μ_diff ≠ 0

Tip: The paired t-test is essentially a one-sample t-test on the differences (dᵢ = x₁ᵢ − x₂ᵢ).

### A Common Design Mistake

Do not use an independent t-test for before/after data on the same subjects. Doing so throws away the within-subject pairing and often reduces power substantially.

**Test statistic**:

\[
t = \frac{\bar{d} - \mu_d}{s_d / \sqrt{n}}
\]

where $\bar{d}$ is the mean of pair-wise differences, $\mu_d$ is the hypothesized difference (usually 0), and $s_d$ is the SD of differences.

```python
import numpy as np
from scipy import stats

# Example: blood pressure before and after medication
np.random.seed(42)
before = np.array([140, 138, 145, 150, 142, 137, 148, 153, 141, 139])
after  = np.array([130, 132, 138, 145, 136, 130, 140, 148, 135, 133])

differences = before - after
print(f"Mean difference: {differences.mean():.2f}")
print(f"SD of differences: {differences.std(ddof=1):.2f}")

t_stat, p_value = stats.ttest_rel(before, after)
print(f"t-stat  = {t_stat:.4f}")
print(f"p-value = {p_value:.4f}")
print(f"Decision: {'Reject H₀' if p_value < 0.05 else 'Fail to Reject H₀'}")

# Effect size (Cohen's d for paired)
d = differences.mean() / differences.std(ddof=1)
print(f"Cohen's d = {d:.4f}")
```

## Proportion Tests

**Valid when**: n·p̂ ≥ 5 (or 10) and n·(1−p̂) ≥ 5 (or 10) — otherwise use exact binomial test.

Tip: For proportions, always look at the actual counts, not just the percentages. A 10% conversion rate based on 20 users is a very different inferential situation from a 10% rate based on 20,000 users.

### One-Proportion z-test

**Question**: Is the true population proportion equal to a known value π₀?

**H₀**: π = π₀
**H₁**: π ≠ π₀

```python
from statsmodels.stats.proportion import proportions_ztest

# Example: Is the click-through rate 30%?
clicks = 82
n = 200
pi_0 = 0.30  # hypothesized proportion

z_stat, p_value = proportions_ztest(count=clicks, nobs=n, value=pi_0, alternative='two-sided')
p_hat = clicks / n

print(f"p̂ = {p_hat:.4f}")
print(f"z-stat  = {z_stat:.4f}")
print(f"p-value = {p_value:.4f}")
print(f"Decision: {'Reject H₀' if p_value < 0.05 else 'Fail to Reject H₀'}")
```

### Two-Proportion z-test

**Question**: Do two independent groups have different proportions?

Common use case: **A/B testing** (e.g., do Control and Treatment have different conversion rates?)

**Test statistic:**

\[
z = \frac{\hat{p}_1 - \hat{p}_2}{\sqrt{\hat{p}(1-\hat{p})\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}
\]

where $\hat{p} = (x_1 + x_2)/(n_1 + n_2)$ is the **pooled proportion** under H₀.

```python
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

# Control: 45/200 converted; Treatment: 62/200 converted
counts = np.array([62, 45])   # successes
nobs   = np.array([200, 200]) # totals

z_stat, p_value = proportions_ztest(counts, nobs, alternative='two-sided')

print(f"Control rate:   {45/200:.3f}")
print(f"Treatment rate: {62/200:.3f}")
print(f"z-stat  = {z_stat:.4f}")
print(f"p-value = {p_value:.4f}")
print(f"Decision: {'Reject H₀ — significant difference' if p_value < 0.05 else 'Fail to Reject H₀ — no significant difference'}")
```

## Chi-Square Tests

### Chi-Square Test of Independence

**Question**: Is there an association between two categorical variables?

**H₀**: The two variables are independent (no association)
**H₁**: The two variables are associated

**Assumptions:**

| Assumption | Check |
| ------------------------------- | ------------------------------------ |
| Data is categorical | Check data type |
| Observations are independent | Study design |
| Expected count ≥ 5 in each cell | Inspect the expected frequency table |

Warning: If any expected cell count < 5, use Fisher's Exact Test instead (especially for 2×2 tables).

```python
import pandas as pd
from scipy import stats
import numpy as np

# Example: Survival by passenger class (Titanic-style)
data = pd.DataFrame({
    'Class':    ['1st', '1st', '1st', '2nd', '2nd', '2nd', '3rd', '3rd', '3rd'] * 20,
    'Survived': (['Yes', 'Yes', 'No'] + ['Yes', 'No', 'No'] + ['No', 'No', 'No']) * 20
})

ct = pd.crosstab(data['Class'], data['Survived'])
chi2, p_value, dof, expected = stats.chi2_contingency(ct)

print("Observed counts:")
print(ct)

print("\nExpected counts:")
print(pd.DataFrame(expected, index=ct.index, columns=ct.columns).round(2))

print(f"Chi-square statistic = {chi2:.4f}")
print(f"Degrees of freedom   = {dof}")
print(f"p-value              = {p_value:.4f}")
print(f"Decision: {'Reject H₀ — variables are associated' if p_value < 0.05 else 'Fail to Reject H₀'}")

# Effect size: Cramér's V
n = ct.values.sum()
cramers_v = np.sqrt(chi2 / (n * (min(ct.shape) - 1)))
print(f"Cramér's V = {cramers_v:.4f}")
```

Tip: The chi-square approximation depends on expected frequencies, not only observed ones. Always inspect the expected table when counts are small or imbalanced.

**Cramér's V — effect size for chi-square:**

| Cramér's V | Strength of Association |
| ---------- | ----------------------- |
| < 0.10 | Negligible |
| 0.10–0.29 | Weak |
| 0.30–0.49 | Moderate |
| ≥ 0.50 | Strong |

### Chi-Square Goodness-of-Fit

**Question**: Do observed frequencies match a hypothesized distribution?

**H₀**: Observed frequencies fit the expected distribution
**H₁**: They do not fit

**Degrees of freedom**: number of categories − 1

```python
from scipy.stats import chisquare
import numpy as np

# Example: Is a die fair?
observed = np.array([11, 9, 10, 12, 8, 10])
expected = np.array([10, 10, 10, 10, 10, 10])  # equal probability

chi2_stat, p_value = chisquare(f_obs=observed, f_exp=expected)
print(f"Chi2 = {chi2_stat:.4f}, p = {p_value:.4f}")
```

Tip: Independence vs. Homogeneity vs. Goodness-of-Fit: - Independence: One population, two variables — are they related? - Homogeneity: Multiple populations, one variable — do they have the same distribution? - Goodness-of-Fit: One variable — does it match a known distribution? Independence and Homogeneity use the same χ² formula; the distinction is conceptual (study design).

## Exact Tests

Use exact tests when **sample sizes are small** or **expected cell counts < 5**, where Normal/chi-square approximations break down.

### Exact Binomial Test

**Question**: Does an observed proportion differ from a hypothesized value — with small n?
**Alternative to**: One-proportion z-test

**H₀**: p = p₀
**H₁**: p ≠ p₀

```python
from scipy.stats import binomtest

result = binomtest(k=3, n=12, p=0.5, alternative="two-sided")
print(f"Exact p-value = {result.pvalue:.4f}")
print(result.proportion_ci(confidence_level=0.95))
```

### Fisher's Exact Test

Best for small-sample 2×2 contingency tables.

```python
from scipy.stats import fisher_exact
import numpy as np

table = np.array([[1, 9],
                  [8, 2]])

odds_ratio, p_value = fisher_exact(table, alternative="two-sided")
print(f"Odds ratio = {odds_ratio:.4f}")
print(f"Exact p-value = {p_value:.4f}")
```

Tip: Fisher's exact test is not just "chi-square for small n". It uses the exact finite-sample distribution under the null, so its p-values remain valid when approximation-based methods become unreliable.

## Matching the Question to the Test Statistic

Different tests focus on different quantities:

| Question type | Test statistic usually compares |
| ------------- | ------------------------------- |
| Mean vs. reference | Signal relative to standard error |
| Mean vs. mean | Difference of means relative to pooled / Welch SE |
| Proportion vs. reference | Difference in proportions relative to binomial SE |
| Count table association | Observed vs expected frequencies |
| Distribution fit | Observed pattern vs theoretical pattern |

Knowing what the statistic is actually comparing makes it easier to interpret why a result became significant.

## Reporting Checklist

For almost any test, a good report should include:

1. The null and alternative hypotheses.
2. The chosen test and why it matches the design.
3. The test statistic and degrees of freedom if relevant.
4. The p-value.
5. An effect size.
6. A confidence interval when available.
7. Any important assumption checks or corrections.

\[
P(X = x) = \binom{n}{x} p_0^x (1 - p_0)^{n-x}
\]

```python
from scipy.stats import binomtest

# 12 successes in 20 trials; expected p = 0.5
result = binomtest(k=12, n=20, p=0.5, alternative='two-sided')
print(f"p-value = {result.pvalue:.4f}")
```

### Fisher's Exact Test

**Question**: Is there an association between two categorical variables in a 2×2 table — with small n?
**Alternative to**: Chi-square test of independence or two-proportion z-test

**H₀**: The two variables are independent (OR = 1)
**H₁**: An association exists

```python
from scipy.stats import fisher_exact

table = [[8, 2],
         [1, 9]]

oddsratio, p_value = fisher_exact(table, alternative='two-sided')
print(f"Odds Ratio = {oddsratio:.3f}, p-value = {p_value:.4f}")
```

**Exact vs. Approximation — when to switch:**

| Method | Distribution | Use When |
| ------------------------------- | --------------------------------- | ------------------------------- |
| Proportion z-test / Chi-square | Normal / χ² (approximation) | Large n, expected counts ≥ 5 |
| Exact Binomial / Fisher's Exact | Binomial / Hypergeometric (exact) | Small n, any expected count < 5 |

## ANOVA Guide

Use ANOVA when the outcome is numerical and you need to compare **three or more means**.

Key point: ANOVA only answers whether at least one group mean differs from the others. If the result is significant, you still need post-hoc comparisons to identify which groups differ.

| Situation | Use | Details |
| --------- | --- | ------- |
| 3+ independent groups, one factor | One-way ANOVA | [One-Way ANOVA](./one-way-anova.md) |
| Two categorical factors | Two-way ANOVA | [Two-Way ANOVA](./two-way-anova.md) |
| Same subject measured repeatedly | Repeated-measures ANOVA | [Repeated-Measures ANOVA](./repeated-measures-anova.md) |
| Need group-by-group differences | Post-hoc tests | [Post-hoc and Effect Size](./post-hoc-effect-size.md) |

**Must-know formula:**

\[
F = \frac{MS_{\text{between}}}{MS_{\text{within}}}
\]

| If Assumption Fails | Use Instead |
| ------------------- | ----------- |
| Equal variance fails | Welch's ANOVA |
| Normality fails badly | Kruskal-Wallis |
| Independence fails | Repeated-measures ANOVA or mixed model |

## Checking Assumptions

Before running any parametric test, verify the three core assumptions: **independence**, **normality**, and **equal variance**. A full guide with tests and remedies is in [Assumption Checks](./assumption-checks.md). Quick reference is below.

### Normality

```python
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
from sklearn.datasets import load_iris

df = load_iris(as_frame=True).frame
x = df['sepal length (cm)']

fig, axes = plt.subplots(1, 3, figsize=(14, 4))

axes[0].hist(x, bins=20, color='steelblue', edgecolor='white')
axes[0].set_title('Histogram')

stats.probplot(x, dist='norm', plot=axes[1])
axes[1].set_title('Q-Q Plot')

axes[2].boxplot(x)
axes[2].set_title('Boxplot')

plt.tight_layout()
plt.show()

# Shapiro-Wilk (n ≤ 2000; prefer visual checks for large n)
stat, p = stats.shapiro(x)
print(f"Shapiro-Wilk: W={stat:.4f}, p={p:.4f}")
print(f"Normality: {'likely met' if p > 0.05 else 'may be violated — consider non-parametric or transform'}")
```

Warning: For n > 200, Shapiro–Wilk almost always rejects normality even for trivial deviations. With large n, CLT compensates, so prioritize the Q–Q plot over the p-value. See also [Normality Tests](./assumption-checks.md#normality-tests).

### Equal Variance

Run a variance test before any two-group or multi-group comparison:

```python
from scipy import stats

# Levene's test (robust default — works even without normality)
stat, p = stats.levene(group1, group2)
print(f"Levene's: stat={stat:.4f}, p={p:.4f}")
# p ≤ 0.05 → variances unequal → use Welch's t-test / Welch's ANOVA

# Bartlett's test (more powerful when data are confirmed normal)
stat, p = stats.bartlett(group1, group2)
print(f"Bartlett's: stat={stat:.4f}, p={p:.4f}")
```

Tip: See [Variance Tests / Homoscedasticity](./assumption-checks.md#variance-tests-homoscedasticity) for a comparison of Levene's, Bartlett's, and Brown-Forsythe.

## Summary Comparison Table

| Test | H₀ | Data Type | Groups | Key Assumption | Effect Size |
| ------------------------------ | -------------------------- | ----------- | ---------- | ---------------------------------- | --------------- |
| **One-sample t-test** | μ = μ₀ | Numerical | 1 | Approx. normal or n ≥ 30 | Cohen's d |
| **Independent t-test** | μ₁ = μ₂ | Numerical | 2 | Approx. normal, independent groups | Cohen's d |
| **Paired t-test** | μ_diff = 0 | Numerical | 2 (paired) | Differences approx. normal | Cohen's d |
| **One-way ANOVA** | μ₁ = … = μₖ | Numerical | 3+ | Normal, equal variances | η² |
| **Two-way ANOVA** | No main/interaction effect | Numerical | 3+ | Normal, equal variances | η²ₚ |
| **One-proportion z-test** | π = π₀ | Categorical | 1 | n·p ≥ 5 and n·(1−p) ≥ 5 | — |
| **Two-proportion z-test** | π₁ = π₂ | Categorical | 2 | n·p ≥ 5 in both groups | Difference in p |
| **Chi-square independence** | No association | Categorical | 2+ | Expected counts ≥ 5 per cell | Cramér's V |
| **Chi-square goodness-of-fit** | Fits distribution | Categorical | 1 | Expected counts ≥ 5 | — |
| **Exact binomial test** | p = p₀ | Categorical | 1 | Small n; no approximation needed | — |
| **Fisher's exact test** | No association | Categorical | 2 | Small n or expected counts < 5 | Odds ratio |

## Key Takeaways

| Concept | Key Point |
| ----------------------------------- | -------------------------------------------------------------------------------------- |
| **Match test to research question** | Data type, number of groups, and independence drive the choice |
| **Check assumptions first** | Running a test without checking assumptions can give invalid results |
| **Welch's t-test as default** | Use `equal_var=False` — handles unequal variances safely with no real downside |
| **Paired vs. independent** | Paired tests are more powerful when matching is valid — always use when appropriate |
| **ANOVA needs post-hoc** | A significant F only tells you _that_ groups differ — post-hoc identifies _which_ |
| **Chi-square needs ≥ 5 expected** | Switch to Fisher's Exact Test for small expected counts |
| **Exact tests for small n** | Exact binomial and Fisher's are always valid; approximations fail at small samples |
| **Always report effect size** | p-value alone is insufficient — always pair with Cohen's d, η², Cramér's V, or similar |
