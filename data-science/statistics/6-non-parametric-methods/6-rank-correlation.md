# 6. Rank Correlation: Spearman ρ & Kendall τ

**Rank correlation methods** measure the relationship between two variables without assuming normality or linearity. Instead of raw values, they work on the **ranks** of observations.

> 📌 **Parametric equivalent**: Pearson r (covered in Descriptive Statistics – Bivariate Analysis)  
> 📌 **Key difference**: Pearson measures *linear* relationships; rank correlations measure *monotonic* relationships — whether one variable consistently increases or decreases as the other does, regardless of the rate.

---

## 6.1 When to Use Rank Correlation

| Condition                                     | Reason to Use Rank Correlation                                |
| --------------------------------------------- | ------------------------------------------------------------- |
| Data is not normally distributed               | Pearson r assumes bivariate normality                         |
| Data is ordinal (e.g., Likert scale ratings)  | Ranks are appropriate; means are not                          |
| Relationship is monotonic but not linear       | Rank correlation detects any consistent direction             |
| Severe outliers are present                    | Ranks reduce the influence of extreme values                  |
| Small sample sizes                             | Normality is hard to establish; rank methods are safer        |

---

## 6.2 Spearman's ρ (Rho)

Spearman's ρ is computed by **ranking** both variables and then applying the Pearson formula to the ranks.

$$\rho = 1 - \frac{6 \sum d_i^2}{n(n^2 - 1)}$$

where dᵢ is the difference in ranks for each pair (simplified formula, valid when there are no ties).

**Range**: −1 ≤ ρ ≤ +1  
**Interpretation**: Same as Pearson r — direction and strength of the monotonic relationship.

| ρ Value          | Interpretation                                              |
| ---------------- | ----------------------------------------------------------- |
| +1.0             | Perfect positive monotonic relationship                     |
| +0.7 to +0.99    | Very strong positive                                        |
| +0.4 to +0.69    | Moderate to strong positive                                 |
| +0.1 to +0.39    | Weak positive                                               |
| ≈ 0              | No monotonic relationship                                   |
| Negative values  | (Mirror above — as X increases, Y decreases consistently)   |

### Python Implementation

```python
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

df = load_iris(as_frame=True).frame

# ── Spearman Correlation ──
rho, p_value = stats.spearmanr(
    df['sepal length (cm)'],
    df['petal length (cm)']
)
print(f"Spearman ρ = {rho:.4f}")
print(f"p-value    = {p_value:.4f}")
```

### Spearman Correlation Matrix

```python
import pandas as pd

num_cols = ['sepal length (cm)', 'sepal width (cm)',
            'petal length (cm)', 'petal width (cm)']

spearman_matrix = df[num_cols].corr(method='spearman')
print(spearman_matrix.round(3))

# Heatmap
plt.figure(figsize=(7, 5))
sns.heatmap(spearman_matrix, annot=True, fmt='.2f',
            cmap='coolwarm', vmin=-1, vmax=1, center=0, square=True)
plt.title("Spearman Rank Correlation Matrix")
plt.tight_layout()
plt.show()
```

---

## 6.3 Kendall's τ (Tau)

Kendall's τ is based on the concept of **concordant and discordant pairs** rather than ranks directly.

For each pair of observations (i, j):
- **Concordant**: xᵢ > xⱼ **and** yᵢ > yⱼ (or both smaller) → same direction
- **Discordant**: xᵢ > xⱼ **but** yᵢ < yⱼ (or vice versa) → opposite direction

$$\tau = \frac{(\text{# concordant pairs}) - (\text{# discordant pairs})}{\binom{n}{2}}$$

**Range**: −1 ≤ τ ≤ +1

> 💡 τ values are typically smaller than ρ for the same dataset. This doesn't mean it's weaker — the scales are simply different. A τ of 0.6 is often considered comparable to a ρ of 0.75+.

### Python Implementation

```python
tau, p_value = stats.kendalltau(
    df['sepal length (cm)'],
    df['petal length (cm)']
)
print(f"Kendall τ  = {tau:.4f}")
print(f"p-value    = {p_value:.4f}")
```

---

## 6.4 Pearson vs Spearman vs Kendall: When to Use Which

| Criterion                     | Pearson r                      | Spearman ρ                     | Kendall τ                      |
| ----------------------------- | ------------------------------ | ------------------------------ | ------------------------------ |
| **Assumes normality**         | ✅ Yes                         | ❌ No                          | ❌ No                          |
| **Relationship type**         | Linear only                    | Monotonic                      | Monotonic                      |
| **Data type**                 | Continuous (Interval/Ratio)    | Ordinal or continuous          | Ordinal or continuous          |
| **Handles outliers**          | ❌ Sensitive                   | ✅ Robust                      | ✅ Robust                      |
| **Best for small n**          | Not ideal                      | Acceptable                     | ✅ Best                        |
| **Handles many ties**         | N/A                            | ⚠️ Weaker with many ties       | ✅ Better                      |
| **Interpretation**            | Linear strength                | Rank-based monotonic strength  | Proportion of concordant pairs |
| **Typical value magnitude**   | Highest                        | Middle                         | Lowest (but comparable meaning)|

> 💡 **General recommendation**:
> - Default: **Spearman ρ** — widely used, well-understood, good for most situations
> - Small samples or many ties: **Kendall τ** — more robust, better statistical properties
> - Normal continuous data, linear relationship confirmed by scatter plot: **Pearson r**

---

## 6.5 Full Comparison Example

```python
import numpy as np
from scipy import stats
from sklearn.datasets import load_iris

df = load_iris(as_frame=True).frame
x = df['sepal length (cm)']
y = df['petal length (cm)']

r,   p_r   = stats.pearsonr(x, y)
rho, p_rho = stats.spearmanr(x, y)
tau, p_tau = stats.kendalltau(x, y)

print("=" * 45)
print(f"{'Method':<15} {'Coefficient':>12} {'p-value':>12}")
print("-" * 45)
print(f"{'Pearson r':<15} {r:>12.4f} {p_r:>12.4f}")
print(f"{'Spearman ρ':<15} {rho:>12.4f} {p_rho:>12.4f}")
print(f"{'Kendall τ':<15} {tau:>12.4f} {p_tau:>12.4f}")
print("=" * 45)
```

---

## 6.6 Visualization: Scatter Plot with Rank Overlays

Always visualize before computing correlation. For rank correlations, you can show both the original relationship and the rank-transformed version.

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
from sklearn.datasets import load_iris

df = load_iris(as_frame=True).frame
x = df['sepal length (cm)']
y = df['petal length (cm)']

rho, _ = stats.spearmanr(x, y)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# ── Original scatter plot ──
axes[0].scatter(x, y, alpha=0.5, color='steelblue')
axes[0].set_xlabel('Sepal Length (cm)')
axes[0].set_ylabel('Petal Length (cm)')
axes[0].set_title(f'Original Values\nSpearman ρ = {rho:.3f}')

# ── Rank-transformed scatter plot ──
x_rank = x.rank()
y_rank = y.rank()
axes[1].scatter(x_rank, y_rank, alpha=0.5, color='coral')
axes[1].set_xlabel('Rank of Sepal Length')
axes[1].set_ylabel('Rank of Petal Length')
axes[1].set_title('Rank-Transformed Values\n(What Spearman Operates On)')

plt.tight_layout()
plt.show()
```

---

## 6.7 Monotonic vs Linear: Why It Matters

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(42)
x = np.linspace(1, 10, 50)

# Linear relationship
y_linear = 2 * x + np.random.normal(0, 1, 50)

# Monotonic but not linear (exponential)
y_mono = np.exp(0.4 * x) + np.random.normal(0, 2, 50)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

for ax, y, title in zip(
    axes,
    [y_linear, y_mono],
    ['Linear Relationship', 'Monotonic but Non-Linear']
):
    r,   _ = stats.pearsonr(x, y)
    rho, _ = stats.spearmanr(x, y)

    ax.scatter(x, y, alpha=0.6, color='steelblue')
    ax.set_title(f'{title}\nPearson r = {r:.3f}  |  Spearman ρ = {rho:.3f}')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

plt.tight_layout()
plt.show()
```

> 💡 **Key insight**: For a linear relationship, Pearson r ≈ Spearman ρ. For a non-linear monotonic relationship (like exponential growth), Pearson r underestimates the true monotonic strength while Spearman ρ captures it well.

---

## 6.8 Key Takeaways

| Concept                          | Key Point                                                                    |
| -------------------------------- | ---------------------------------------------------------------------------- |
| **Rank correlation**             | Measures monotonic relationships — any consistent direction, not just linear |
| **Spearman ρ**                   | The most widely used non-parametric correlation; good default choice         |
| **Kendall τ**                    | Better for small samples or data with many ties                              |
| **Pearson vs Spearman**          | If they disagree significantly, the relationship is probably non-linear       |
| **Always scatter plot first**    | Correlation coefficients miss non-monotonic patterns (U-shapes, clusters)    |
| **Correlation ≠ Causation**      | Applies equally to rank correlations                                         |

---

**← Previous:** [Categorical Association: Chi-Square](./5-chi-square.md)  
**↑ Back to:** [Non-parametric Methods – README](./README.md)
