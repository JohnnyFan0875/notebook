# Bivariate Analysis

**Bivariate analysis** examines the relationship between **two variables**. The appropriate method depends on the data types of both variables.

| Variable A | Variable B | Method |
| ------------------ | ------------------ | ---------------------------------------- |
| Numerical | Numerical | Correlation (Pearson, Spearman, Kendall) |
| Categorical | Categorical | Cross-tabulation (covered in the categorical univariate notes) |
| Numerical | Categorical | Group comparison, boxplot by group |
| Multiple Numerical | Multiple Numerical | Correlation matrix, heatmap |

Key point: Correlation ≠ Causation. A strong correlation tells you two variables move together — it does not tell you that one causes the other. Correlation does not mean causation, which is the most misunderstood concept in statistics.

## Numerical × Numerical: Correlation

### Pearson Correlation Coefficient (r)

Measures the **strength and direction of the linear relationship** between two continuous variables.

\[
r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}
\]

**Range**: −1 ≤ r ≤ +1

| r Value | Direction | Strength | Practical Meaning |
| --------------- | --------- | -------------- | ---------------------------------------------------- |
| +1.00 | Positive | Perfect | As X increases, Y increases perfectly proportionally |
| +0.70 to +0.99 | Positive | Very strong | Clear and consistent positive trend |
| +0.50 to +0.69 | Positive | Strong | Noticeable positive trend |
| +0.30 to +0.49 | Positive | Moderate | Some positive tendency |
| +0.10 to +0.29 | Positive | Weak | Slight positive tendency |
| ≈ 0.00 | None | Negligible | No linear relationship |
| Negative values | Negative | (mirror above) | Y decreases as X increases |

Tip: These thresholds are guidelines, not rules — context matters. A correlation of 0.3 might be weak in physics but very meaningful in social science research.

```python
import pandas as pd
from scipy import stats
from sklearn.datasets import load_iris

df = load_iris(as_frame=True).frame

# Method 1: scipy (also gives p-value)
r, p_value = stats.pearsonr(df['sepal length (cm)'], df['petal length (cm)'])
print(f"Pearson r = {r:.3f},  p-value = {p_value:.4f}")

# Method 2: pandas (quick, between two columns)
r_pandas = df['sepal length (cm)'].corr(df['petal length (cm)'])
print(f"Pearson r = {r_pandas:.3f}")
```

**Assumptions for Pearson r:**

| Assumption | How to Check |
| ---------------------------------------------- | ------------------- |
| Both variables are continuous (Interval/Ratio) | Check data types |
| Linear relationship | Scatter plot |
| Both variables approximately normal | Histogram, Q–Q plot |
| No severe outliers | Boxplot |

Warning: If these assumptions are violated, use Spearman ρ instead.

### Spearman's ρ (Rank Correlation)

Based on **ranked data** — detects monotonic relationships (where one variable consistently increases/decreases as the other does, but not necessarily linearly).

**Use when:**

- Data is ordinal
- Distribution is heavily skewed
- The relationship is monotonic but not linear
- Severe outliers are present

```python
rho, p = stats.spearmanr(df['sepal length (cm)'], df['petal length (cm)'])
print(f"Spearman ρ = {rho:.3f},  p-value = {p:.4f}")
```

### Kendall's τ (Tau)

Also rank-based — uses concordant and discordant pairs instead of ranks directly. More robust for small samples or data with many tied values.

```python
tau, p = stats.kendalltau(df['sepal length (cm)'], df['petal length (cm)'])
print(f"Kendall τ = {tau:.3f},  p-value = {p:.4f}")
```

### Choosing the Right Correlation Method

| Method | Data Type | Relationship Type | Handles Outliers? | Best For |
| -------------- | ------------------ | ----------------- | ----------------- | ---------------------------------------------- |
| **Pearson r** | Continuous, normal | Linear only | ❌ Sensitive | Standard correlation for clean numerical data |
| **Spearman ρ** | Ordinal or skewed | Monotonic | ✅ Robust | Non-normal data, ranked data, outliers present |
| **Kendall τ** | Ordinal, small n | Monotonic | ✅ Robust | Small samples, many ties |

Tip: When in doubt, use Spearman ρ — it makes fewer assumptions and is almost as efficient as Pearson when the data is normal. When in doubt, Spearman is a more conservative and safer choice.

### Visualization: Scatter Plot

Always visualize before computing correlation. A scatter plot reveals:

- Whether the relationship is actually linear
- The presence of outliers
- Clusters or subgroups in the data

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Simple scatter plot
sns.scatterplot(
    x='sepal length (cm)',
    y='petal length (cm)',
    data=df,
    alpha=0.6
)
plt.title(f"Sepal Length vs Petal Length  (r = {r:.3f})")
plt.show()

# With regression line
sns.regplot(
    x='sepal length (cm)',
    y='petal length (cm)',
    data=df,
    scatter_kws={'alpha': 0.5}
)
plt.title('Scatter Plot with Regression Line')
plt.show()
```

Warning: Anscombe's Quartet warning: Four datasets can have almost identical correlations but look completely different visually. Always plot first. Draw first, then calculate.

## Numerical × Categorical: Group Comparison

When one variable is numerical and the other is categorical, compare the numerical variable's distribution **across groups**.

```python
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris

iris = load_iris(as_frame=True)
df = iris.frame
df['species'] = iris.target_names[iris.target]

# Summary statistics by group
group_summary = df.groupby('species')['sepal length (cm)'].agg(
    Count='count',
    Mean='mean',
    Median='median',
    SD='std',
    IQR=lambda x: x.quantile(0.75) - x.quantile(0.25)
).round(3)
print(group_summary)
```

**Output example:**

| species | Count | Mean | Median | SD | IQR |
| ---------- | ----- | ----- | ------ | ----- | ----- |
| setosa | 50 | 5.006 | 5.000 | 0.352 | 0.400 |
| versicolor | 50 | 5.936 | 5.900 | 0.516 | 0.700 |
| virginica | 50 | 6.588 | 6.500 | 0.636 | 0.675 |

**Visualization options:**

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Boxplot by group — shows median, IQR, outliers
sns.boxplot(x='species', y='sepal length (cm)', data=df, ax=axes[0], palette='Set2')
axes[0].set_title('Sepal Length by Species (Boxplot)')

# Violin plot — shows distribution shape within each group
sns.violinplot(x='species', y='sepal length (cm)', data=df, ax=axes[1], palette='Set2')
axes[1].set_title('Sepal Length by Species (Violin Plot)')

plt.tight_layout()
plt.show()
```

| Chart | Best For |
| ----------------------------- | -------------------------------------------------------- |
| **Boxplot by group** | Comparing median and spread; spotting outliers per group |
| **Violin plot** | Seeing distribution shape within each group |
| **Bar chart with error bars** | Comparing means with variability indication |

## Multiple Numerical Variables: Correlation Matrix

When you have multiple numerical variables, a **correlation matrix** shows all pairwise correlations at once.

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Select numerical columns
num_cols = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
corr_matrix = df[num_cols].corr(method='pearson')

print(corr_matrix.round(3))
```

**Heatmap — the standard way to visualize a correlation matrix:**

```python
plt.figure(figsize=(7, 5))
sns.heatmap(
    corr_matrix,
    annot=True,       # show correlation values in cells
    fmt='.2f',        # 2 decimal places
    cmap='coolwarm',  # blue = negative, red = positive
    vmin=-1, vmax=1,  # fix scale to [-1, 1]
    center=0,
    square=True
)
plt.title('Correlation Matrix — Iris Dataset')
plt.tight_layout()
plt.show()
```

**Pairplot — scatter plots for all pairs with distributions on the diagonal:**

```python
sns.pairplot(df, hue='species', diag_kind='kde', palette='Set2')
plt.suptitle('Pairplot — Iris Dataset', y=1.02)
plt.show()
```

Tip: Reading a heatmap: - Dark red → strong positive correlation - Dark blue → strong negative correlation - White/light → near zero (no linear relationship) - Diagonal is always 1.0 (a variable is perfectly correlated with itself)

## Key Takeaways

| Concept | Key Point |
| ---------------------------------- | -------------------------------------------------------------------------------- |
| **Match method to data types** | Always check what types of variables you have before choosing a method |
| **Visualize first** | Scatter plots reveal patterns (or problems) that correlation coefficients miss |
| **Pearson vs Spearman** | Pearson for normal continuous data; Spearman when assumptions are violated |
| **Correlation ≠ Causation** | A high r does not mean X causes Y — always consider alternative explanations |
| **Heatmap for multiple variables** | Correlation matrix + heatmap is the most efficient overview of relationships |
| **Group comparison** | Use boxplot or violin plot when comparing a numerical variable across categories |

## Three Questions Before Interpreting a Relationship

1. Is the pattern really linear?
2. Is the apparent association driven by outliers or subgroups?
3. Could a third variable explain what you see?

Tip: Bivariate analysis is a screening stage, not a causal conclusion stage.
