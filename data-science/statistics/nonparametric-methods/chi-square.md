# Categorical Association: Chi-Square Tests

The **Chi-Square (χ²) test** is used to examine relationships between **categorical variables**. Unlike the previous tests which work on ranks, Chi-Square works directly on **counts (frequencies)**.

Key point: No parametric equivalent in the strict sense — Chi-square is its own family. It answers: "Are these two categorical variables associated, or are they independent?"

## Two Types of Chi-Square Tests

| Test | Question Answered | Data Required |
| --------------------------------- | --------------------------------------------------------------------- | --------------------------------- |
| **Chi-Square Test of Independence** | Are two categorical variables associated? | Contingency table (cross-tab) |
| **Chi-Square Goodness of Fit** | Does observed data match an expected distribution? | One categorical variable + expected proportions |

## Chi-Square Test of Independence

### When to Use
- Both variables are categorical (nominal or ordinal)
- Testing whether there is an association between them
- Each observation belongs to exactly one cell
- Expected frequencies ≥ 5 in most cells (see assumptions)

### How It Works

1. Build a **contingency table** (observed frequencies O)
2. Calculate **expected frequencies** E under the assumption of independence:

\[
E_{ij} = \frac{(\text{row total}_i) \times (\text{column total}_j)}{N}
\]

3. Compute the test statistic:

\[
\chi^2 = \sum_{i,j} \frac{(O_{ij} - E_{ij})^2}{E_{ij}}
\]

4. Compare against Chi-square distribution with df = (rows − 1) × (columns − 1)

Tip: Intuition: If variables are independent, observed frequencies should be close to expected frequencies. Large deviations → large χ² → evidence of association.

### Hypotheses
- **H₀**: The two variables are independent (no association)
- **H₁**: The two variables are associated

### Python Implementation

```python
import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

# Example: Is gender associated with product preference?
data = pd.DataFrame({
    'Gender':    ['Male', 'Female', 'Male', 'Female', 'Male',
                  'Female', 'Male', 'Female', 'Male', 'Female',
                  'Male', 'Female'],
    'Preference': ['A', 'A', 'B', 'A', 'B',
                   'B', 'A', 'C', 'C', 'A',
                   'B', 'C']
})

# Build contingency table
ct = pd.crosstab(data['Gender'], data['Preference'])
print("Observed frequencies:")
print(ct)

# Chi-square test
chi2, p_value, dof, expected = stats.chi2_contingency(ct)

print(f"\nChi-square statistic = {chi2:.3f}")
print(f"p-value              = {p_value:.4f}")
print(f"Degrees of freedom   = {dof}")
print(f"\nExpected frequencies:")
print(pd.DataFrame(expected, index=ct.index, columns=ct.columns).round(2))

if p_value < 0.05:
    print("\n→ Reject H₀: significant association between Gender and Preference")
else:
    print("\n→ Fail to reject H₀: no significant association detected")
```

## Effect Size: Cramér's V

A significant Chi-square tells you association exists; **Cramér's V** tells you how strong it is.

\[
V = \sqrt{\frac{\chi^2}{N \cdot \min(r-1, c-1)}}
\]

Range: 0 (no association) to 1 (perfect association)

```python
n = ct.values.sum()
min_dim = min(ct.shape[0] - 1, ct.shape[1] - 1)

cramers_v = np.sqrt(chi2 / (n * min_dim))
print(f"Cramér's V = {cramers_v:.3f}")
```

| Cramér's V | Interpretation (for 2×2) | Interpretation (larger tables) |
| ----------- | ------------------------ | ------------------------------ |
| 0.1–0.3 | Small effect | Weak association |
| 0.3–0.5 | Medium effect | Moderate association |
| > 0.5 | Large effect | Strong association |

Warning: Cramér's V thresholds vary by table size (number of rows/columns). Interpret with context.

## Assumptions & When to Use Fisher's Exact Test

### Chi-Square Assumptions

| Assumption | Guideline |
| ---------------------------------- | ------------------------------------------------------------ |
| **Independence of observations** | Each subject contributes to only one cell |
| **Expected frequency ≥ 5** | In at least 80% of cells; no cell should have expected < 1 |
| **Sufficient sample size** | Small samples violate the χ² approximation |

```python
# Check expected frequencies
print("Expected frequency check:")
print(pd.DataFrame(expected, index=ct.index, columns=ct.columns).round(1))
low_expected = (expected < 5).sum()
print(f"\nCells with expected < 5: {low_expected} out of {expected.size}")
```

### When to Use Fisher's Exact Test Instead

If **any expected frequency < 5** (especially in 2×2 tables), use **Fisher's Exact Test** instead:

```python
# Fisher's Exact Test — only for 2×2 tables
from scipy.stats import fisher_exact

# Example 2×2 table
table_2x2 = np.array([[8, 2],
                       [1, 9]])

odds_ratio, p_fisher = fisher_exact(table_2x2, alternative='two-sided')

print(f"Fisher's Exact Test p-value = {p_fisher:.4f}")
print(f"Odds Ratio                  = {odds_ratio:.3f}")
```

| Situation | Recommended Test |
| ---------------------------------------- | ----------------------------- |
| 2×2 table, all expected cells ≥ 5 | Chi-square (with continuity correction) |
| 2×2 table, any expected cell < 5 | Fisher's Exact Test |
| Larger tables, expected cells ≥ 5 | Chi-square |
| Larger tables, many expected cells < 5 | Combine categories or collect more data |

## Chi-Square Goodness of Fit

Tests whether observed category frequencies match an **expected (theoretical) distribution**.

### When to Use
- Testing if a die is fair (equal proportions expected)
- Testing if customer arrivals follow a specific distribution
- Comparing observed proportions against historical or theoretical benchmarks

### Hypotheses
- **H₀**: Observed frequencies match the expected distribution
- **H₁**: Observed frequencies do not match the expected distribution

```python
from scipy import stats
import numpy as np

# Example: Is a die fair? (Roll it 60 times)
observed = np.array([8, 10, 12, 9, 11, 10])  # counts for faces 1-6
expected_prop = np.array([1/6] * 6)           # equal probability

# Chi-square goodness of fit
chi2, p_value = stats.chisquare(f_obs=observed, f_exp=expected_prop * observed.sum())

print(f"Chi-square = {chi2:.3f}")
print(f"p-value    = {p_value:.4f}")
print(f"df         = {len(observed) - 1}")

if p_value < 0.05:
    print("→ Reject H₀: die does not appear to be fair")
else:
    print("→ Fail to reject H₀: no evidence the die is unfair")
```

**Custom expected proportions:**

```python
# Example: Is product preference consistent with last year's distribution?
observed   = np.array([45, 30, 25])           # this year
expected_p = np.array([0.50, 0.30, 0.20])    # last year's proportions

chi2, p = stats.chisquare(f_obs=observed, f_exp=expected_p * observed.sum())
print(f"Chi-square = {chi2:.3f},  p = {p:.4f}")
```

## Visualization

### Heatmap of Observed vs Expected

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats

observed_table = np.array([[15, 5],
                            [3, 12]])
row_labels = ['Group A', 'Group B']
col_labels = ['Yes', 'No']

chi2, p, dof, expected = stats.chi2_contingency(observed_table)
residuals = (observed_table - expected) / np.sqrt(expected)  # standardized residuals

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

# Observed counts heatmap
sns.heatmap(observed_table, annot=True, fmt='d', cmap='Blues',
            xticklabels=col_labels, yticklabels=row_labels,
            ax=axes[0], cbar=False)
axes[0].set_title('Observed Frequencies')

# Standardized residuals heatmap
sns.heatmap(residuals, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            xticklabels=col_labels, yticklabels=row_labels,
            ax=axes[1], cbar=True)
axes[1].set_title('Standardized Residuals\n(|r| > 2 → notable)')

plt.tight_layout()
plt.show()
```

Tip: Standardized residuals tell you *which cells* are driving the association. Cells with |residual| > 2 are notably over- or under-represented compared to what independence would predict.

### Grouped Bar Chart

```python
import pandas as pd
import matplotlib.pyplot as plt

ct_norm = pd.crosstab(data['Gender'], data['Preference'], normalize='index')
ct_norm.plot(kind='bar', figsize=(8, 4), color=['#4C72B0', '#DD8452', '#55A868'])
plt.title('Product Preference by Gender (Row Proportions)')
plt.ylabel('Proportion')
plt.xlabel('Gender')
plt.xticks(rotation=0)
plt.legend(title='Preference')
plt.tight_layout()
plt.show()
```

## Key Takeaways

| Concept | Key Point |
| ------------------------------- | ------------------------------------------------------------------------------ |
| **Chi-square of independence** | Tests whether two categorical variables are associated |
| **Chi-square goodness of fit** | Tests whether observed frequencies match expected proportions |
| **Fisher's Exact Test** | Use instead of Chi-square when any expected cell < 5 (especially in 2×2) |
| **Expected frequency rule** | ≥ 80% of cells should have expected ≥ 5; no cell should have expected < 1 |
| **Cramér's V** | Always report effect size alongside χ² and p-value |
| **Standardized residuals** | Reveal *which cells* drive the association |
| **Independence of obs.** | Each subject must appear in exactly one cell — cannot be violated |

## Why Chi-square Lives Here

Chi-square methods are non-parametric in the sense that they do not model means and variances of continuous outcomes. But they still rely on structure: categorical data, independent observations, and enough expected counts for the approximation to work.

Tip: Non-parametric does not mean "works on any sparse table". Very small expected counts still require exact alternatives.
