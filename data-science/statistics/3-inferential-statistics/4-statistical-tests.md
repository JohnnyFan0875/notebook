# 4. Common Statistical Tests

This section covers the most frequently used parametric hypothesis tests, organized by the **research question and data structure**. Each test has specific assumptions — always check them before running the test.

> 📌 **選對檢定的關鍵**：看你有幾組、是否獨立、資料型態是數值還是類別，以及是否符合常態假設。這幾個問題就能決定應該用哪個檢定。

---

## 4.1 Test Selection Guide

**Three questions to ask before choosing a test:**

1. **What type is the outcome variable?** — Numerical / Categorical
2. **How many groups?** — 1 / 2 / 3+
3. **Are the groups independent or paired?** — Independent / Paired

### Numerical Outcome

| Research Question                                | Groups     | Parametric Test              | When Assumptions Fail           |
| ------------------------------------------------ | ---------- | ---------------------------- | ------------------------------- |
| Sample mean vs. known value                      | 1          | One-sample t-test            | One-sample Wilcoxon signed-rank |
| Two independent groups — means differ?           | 2          | Independent t-test (Welch's) | Mann–Whitney U                  |
| Two related/paired measurements — means differ?  | 2 (paired) | Paired t-test                | Wilcoxon signed-rank            |
| Three or more independent groups — means differ? | 3+         | One-way ANOVA                | Kruskal–Wallis                  |
| Two factors + interaction effect?                | 3+         | Two-way ANOVA                | ART ANOVA / PERMANOVA           |

> 💡 **Parametric vs. Non-parametric**: Parametric tests assume approximately normal data and use means/SDs. Non-parametric tests make no distributional assumptions and work on ranks — use them when normality is violated, samples are small, or data is ordinal. Non-parametric tests are covered in Section 6.

### Categorical Outcome

| Research Question                                    | Groups | Large Sample (n·p ≥ 5)     | Small Sample / Low Counts |
| ---------------------------------------------------- | ------ | -------------------------- | ------------------------- |
| Sample proportion vs. known value                    | 1      | One-proportion z-test      | Exact binomial test       |
| Two groups — proportions differ?                     | 2      | Two-proportion z-test      | Fisher's exact test       |
| Association between two categorical variables (r×c)? | 2+     | Chi-square independence    | Fisher's exact test       |
| Observed frequencies match expected distribution?    | 1      | Chi-square goodness-of-fit | Exact binomial test       |

---

## 4.2 One-Sample t-test

**Question**: Is the population mean equal to a specific hypothesized value μ₀?

**H₀**: μ = μ₀  
**H₁**: μ ≠ μ₀ (two-tailed)

**When to use t vs. z:**

| Condition                | Use    |
| ------------------------ | ------ |
| σ known, n ≥ 30          | z-test |
| σ unknown (typical case) | t-test |

**Test statistic**:

$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}$$

**Assumptions:**

| Assumption                                     | How to Check                      |
| ---------------------------------------------- | --------------------------------- |
| Data is continuous                             | Check data type                   |
| Observations are independent                   | Study design                      |
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

---

## 4.3 Independent Samples t-test

**Question**: Do two independent groups have different population means?

**H₀**: μ₁ = μ₂  
**H₁**: μ₁ ≠ μ₂

**Assumptions:**

| Assumption                                    | How to Check        |
| --------------------------------------------- | ------------------- |
| Both groups are continuous                    | Check data type     |
| Groups are independent                        | Study design        |
| Both approximately normal (or n ≥ 30 each)    | Histogram, Q-Q plot |
| Equal variances (Welch's t-test relaxes this) | Levene's test       |

> 💡 Use **Welch's t-test** (`equal_var=False`) by default — it works even when variances are unequal, and performs nearly as well as the classic t-test when variances _are_ equal.

**When to use which variant:**

| Situation                                             | Test                               |
| ----------------------------------------------------- | ---------------------------------- |
| Normal data, variances unequal or sample sizes differ | Welch's t-test (`equal_var=False`) |
| Non-normal data, skewed, or outliers                  | Mann–Whitney U (Section 6)         |

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

---

## 4.4 Paired t-test

**Question**: Do paired or matched measurements differ on average?

**Use when**: Each data point in group 1 is naturally matched with one in group 2 (e.g., before/after measurements on the same subjects, or matched pairs).

**H₀**: μ_diff = 0  
**H₁**: μ_diff ≠ 0

> 💡 The paired t-test is essentially a **one-sample t-test on the differences** (dᵢ = x₁ᵢ − x₂ᵢ).

**Test statistic**:

$$t = \frac{\bar{d} - \mu_d}{s_d / \sqrt{n}}$$

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

---

## 4.5 Proportion Tests

**Valid when**: n·p̂ ≥ 5 (or 10) and n·(1−p̂) ≥ 5 (or 10) — otherwise use exact binomial test.

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

$$z = \frac{\hat{p}_1 - \hat{p}_2}{\sqrt{\hat{p}(1-\hat{p})\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}$$

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

---

## 4.6 Chi-Square Tests

### Chi-Square Test of Independence

**Question**: Is there an association between two categorical variables?

**H₀**: The two variables are independent (no association)  
**H₁**: The two variables are associated

**Assumptions:**

| Assumption                      | Check                                |
| ------------------------------- | ------------------------------------ |
| Data is categorical             | Check data type                      |
| Observations are independent    | Study design                         |
| Expected count ≥ 5 in each cell | Inspect the expected frequency table |

> ⚠️ If any expected cell count < 5, use **Fisher's Exact Test** instead (especially for 2×2 tables).

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

print(f"Chi-square statistic = {chi2:.4f}")
print(f"Degrees of freedom   = {dof}")
print(f"p-value              = {p_value:.4f}")
print(f"Decision: {'Reject H₀ — variables are associated' if p_value < 0.05 else 'Fail to Reject H₀'}")

# Effect size: Cramér's V
n = ct.values.sum()
cramers_v = np.sqrt(chi2 / (n * (min(ct.shape) - 1)))
print(f"Cramér's V = {cramers_v:.4f}")
```

**Cramér's V — effect size for chi-square:**

| Cramér's V | Strength of Association |
| ---------- | ----------------------- |
| < 0.10     | Negligible              |
| 0.10–0.29  | Weak                    |
| 0.30–0.49  | Moderate                |
| ≥ 0.50     | Strong                  |

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

> 💡 **Independence vs. Homogeneity vs. Goodness-of-Fit:**
>
> - **Independence**: One population, two variables — are they related?
> - **Homogeneity**: Multiple populations, one variable — do they have the same distribution?
> - **Goodness-of-Fit**: One variable — does it match a known distribution?
>   Independence and Homogeneity use the same χ² formula; the distinction is conceptual (study design).

---

## 4.7 Exact Tests

Use exact tests when **sample sizes are small** or **expected cell counts < 5**, where Normal/chi-square approximations break down.

### Exact Binomial Test

**Question**: Does an observed proportion differ from a hypothesized value — with small n?  
**Alternative to**: One-proportion z-test

**H₀**: p = p₀  
**H₁**: p ≠ p₀

$$P(X = x) = \binom{n}{x} p_0^x (1 - p_0)^{n-x}$$

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

| Method                          | Distribution                      | Use When                        |
| ------------------------------- | --------------------------------- | ------------------------------- |
| Proportion z-test / Chi-square  | Normal / χ² (approximation)       | Large n, expected counts ≥ 5    |
| Exact Binomial / Fisher's Exact | Binomial / Hypergeometric (exact) | Small n, any expected count < 5 |

---

## 4.8 ANOVA — Three or More Groups

**Question**: Do three or more independent groups have different population means?

**H₀**: μ₁ = μ₂ = … = μₖ  
**H₁**: At least one group mean differs

> ⚠️ ANOVA tells you _that_ a difference exists — not _which_ groups differ. Always follow up with post-hoc tests.

**Test statistic (F-test):**

$$F = \frac{MS_{\text{between}}}{MS_{\text{within}}}$$

| F value | Meaning                                                           |
| ------- | ----------------------------------------------------------------- |
| F ≈ 1   | Group means are similar — variance between groups ≈ within groups |
| F >> 1  | Between-group variance much larger — evidence against H₀          |

**Assumptions:**

| Assumption                    | If Violated                    |
| ----------------------------- | ------------------------------ |
| Independence of observations  | Redesign study                 |
| Normality within each group   | Use Kruskal–Wallis (Section 6) |
| Equal variances across groups | Use Welch's ANOVA              |

```python
from scipy import stats
import pandas as pd
import pingouin as pg

group_1 = [23, 21, 19, 22, 20, 23, 21, 20, 22, 21]
group_2 = [30, 28, 29, 32, 31, 30, 33, 29, 30, 32]
group_3 = [25, 24, 23, 26, 25, 27, 24, 23, 22, 25]

# One-way ANOVA
f_stat, p_value = stats.f_oneway(group_1, group_2, group_3)
print(f"F = {f_stat:.4f}, p = {p_value:.4f}")

# With pingouin (includes effect size η²)
data = group_1 + group_2 + group_3
groups = ['G1']*10 + ['G2']*10 + ['G3']*10
df = pd.DataFrame({'value': data, 'group': groups})
print(pg.anova(data=df, dv='value', between='group'))
```

### Post-hoc Tests

When ANOVA is significant, run pairwise comparisons with correction for multiple testing:

```python
from statsmodels.stats.multicomp import pairwise_tukeyhsd

tukey = pairwise_tukeyhsd(df['value'], df['group'], alpha=0.05)
print(tukey)
```

| Method          | When to Use                                       |
| --------------- | ------------------------------------------------- |
| **Tukey's HSD** | Equal group sizes; controls familywise error rate |
| **Bonferroni**  | More conservative; flexible for unequal groups    |

### Effect Size in ANOVA

| Measure                | Formula                            | Use In                                     | Small / Medium / Large |
| ---------------------- | ---------------------------------- | ------------------------------------------ | ---------------------- |
| **η² (eta²)**          | SS_between / SS_total              | One-way ANOVA                              | 0.01 / 0.06 / 0.14     |
| **η²ₚ (partial eta²)** | SS_effect / (SS_effect + SS_error) | Two-way ANOVA (controls for other factors) | 0.01 / 0.06 / 0.14     |

### Two-Way ANOVA

Tests two independent variables simultaneously, and whether they **interact**.

```python
import statsmodels.api as sm
from statsmodels.formula.api import ols

model = ols('score ~ C(treatment) * C(gender)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)
```

> 💡 The interaction term tests whether the effect of one factor **depends on the level of the other**. Always inspect the interaction before interpreting main effects.

---

## 4.9 Checking Normality Assumptions

Most parametric tests assume approximate normality. Always check before running.

```python
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
from sklearn.datasets import load_iris

df = load_iris(as_frame=True).frame
x = df['sepal length (cm)']

fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# Histogram
axes[0].hist(x, bins=20, color='steelblue', edgecolor='white')
axes[0].set_title('Histogram')

# Q-Q plot
stats.probplot(x, dist='norm', plot=axes[1])
axes[1].set_title('Q-Q Plot')

# Boxplot
axes[2].boxplot(x)
axes[2].set_title('Boxplot')

plt.tight_layout()
plt.show()

# Shapiro-Wilk test (best for n < 50; use with caution for large n)
stat, p = stats.shapiro(x)
print(f"Shapiro-Wilk: W={stat:.4f}, p={p:.4f}")
print(f"Normality assumption: {'likely met' if p > 0.05 else 'may be violated — consider non-parametric test'}")
```

> ⚠️ **Large sample caution**: For large n (> 200), Shapiro-Wilk will almost always reject normality even for trivially small deviations. With large n, the CLT usually applies anyway — prioritize visual checks (histogram, Q-Q plot) over the formal test.

---

## 4.10 Summary Comparison Table

| Test                           | H₀                         | Data Type   | Groups     | Key Assumption                     | Effect Size     |
| ------------------------------ | -------------------------- | ----------- | ---------- | ---------------------------------- | --------------- |
| **One-sample t-test**          | μ = μ₀                     | Numerical   | 1          | Approx. normal or n ≥ 30           | Cohen's d       |
| **Independent t-test**         | μ₁ = μ₂                    | Numerical   | 2          | Approx. normal, independent groups | Cohen's d       |
| **Paired t-test**              | μ_diff = 0                 | Numerical   | 2 (paired) | Differences approx. normal         | Cohen's d       |
| **One-way ANOVA**              | μ₁ = … = μₖ                | Numerical   | 3+         | Normal, equal variances            | η²              |
| **Two-way ANOVA**              | No main/interaction effect | Numerical   | 3+         | Normal, equal variances            | η²ₚ             |
| **One-proportion z-test**      | π = π₀                     | Categorical | 1          | n·p ≥ 5 and n·(1−p) ≥ 5            | —               |
| **Two-proportion z-test**      | π₁ = π₂                    | Categorical | 2          | n·p ≥ 5 in both groups             | Difference in p |
| **Chi-square independence**    | No association             | Categorical | 2+         | Expected counts ≥ 5 per cell       | Cramér's V      |
| **Chi-square goodness-of-fit** | Fits distribution          | Categorical | 1          | Expected counts ≥ 5                | —               |
| **Exact binomial test**        | p = p₀                     | Categorical | 1          | Small n; no approximation needed   | —               |
| **Fisher's exact test**        | No association             | Categorical | 2          | Small n or expected counts < 5     | Odds ratio      |

---

## 4.11 Key Takeaways

| Concept                             | Key Point                                                                              |
| ----------------------------------- | -------------------------------------------------------------------------------------- |
| **Match test to research question** | Data type, number of groups, and independence drive the choice                         |
| **Check assumptions first**         | Running a test without checking assumptions can give invalid results                   |
| **Welch's t-test as default**       | Use `equal_var=False` — handles unequal variances safely with no real downside         |
| **Paired vs. independent**          | Paired tests are more powerful when matching is valid — always use when appropriate    |
| **ANOVA needs post-hoc**            | A significant F only tells you _that_ groups differ — post-hoc identifies _which_      |
| **Chi-square needs ≥ 5 expected**   | Switch to Fisher's Exact Test for small expected counts                                |
| **Exact tests for small n**         | Exact binomial and Fisher's are always valid; approximations fail at small samples     |
| **Always report effect size**       | p-value alone is insufficient — always pair with Cohen's d, η², Cramér's V, or similar |

---

**← Previous:** [Hypothesis Testing Framework](./3-hypothesis-testing.md)  
**↑ Back to:** [Inferential Statistics – README](./README.md)  
**Next module →:** Regression Analysis _(coming soon)_
