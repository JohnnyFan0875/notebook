# 1. Multivariate EDA

Before fitting any model, you need to understand the **joint structure of all your variables**. Multivariate EDA extends the univariate and bivariate tools from earlier modules to a setting where many variables must be considered simultaneously.

> 📌 **為什麼多變量 EDA 特別重要**：當變數超過兩個，人類的直覺開始失效。你可能以為兩個變數之間的關係很強，但在控制第三個變數後，這個關係可能消失或反轉——這就是辛普森悖論（Simpson's Paradox）。多變量 EDA 讓你在建模前就察覺這些複雜結構。

---

## 1.1 Loading the Dataset

We use the classic **Iris dataset** (and occasionally Wine dataset) throughout this module — small enough to visualize clearly, yet rich enough to demonstrate all key multivariate concepts.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris, load_wine

# Iris: 150 observations, 4 numerical features, 3 species classes
iris = load_iris(as_frame=True)
df = iris.frame
df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)

print(df.shape)
print(df.dtypes)
print(df.describe().round(2))
```

---

## 1.2 Correlation Matrix and Heatmap

The correlation matrix is the natural starting point for multivariate EDA with numerical data. It shows **all pairwise linear relationships at once**.

```python
num_cols = ['sepal length (cm)', 'sepal width (cm)',
            'petal length (cm)', 'petal width (cm)']

corr = df[num_cols].corr(method='pearson')

plt.figure(figsize=(7, 5))
sns.heatmap(
    corr,
    annot=True, fmt='.2f',
    cmap='coolwarm', vmin=-1, vmax=1, center=0,
    square=True, linewidths=0.5,
    cbar_kws={'shrink': 0.8}
)
plt.title('Pearson Correlation Matrix — Iris Features')
plt.tight_layout()
plt.show()
```

**Reading the heatmap:**

| Cell Value | Interpretation                              |
| ---------- | ------------------------------------------- |
| Close to +1 | Strong positive linear relationship        |
| Close to −1 | Strong negative linear relationship        |
| Near 0     | Little or no linear relationship            |
| Diagonal   | Always 1.0 — a variable correlates perfectly with itself |

> ⚠️ **Correlation heatmaps only capture linear relationships.** A correlation of 0 does not mean "no relationship" — it means no *linear* relationship. Always follow up with a pairplot to see the actual scatter.  
> 相關矩陣只顯示線性關係。相關係數為 0 不代表兩者無關，只代表沒有線性關係。

---

## 1.3 Pairplot

A pairplot shows **all bivariate scatter plots** for every pair of variables, with **univariate distributions on the diagonal**. Coloring by a categorical variable reveals whether groups separate.

```python
# Basic pairplot — color by species
g = sns.pairplot(
    df,
    hue='species',
    diag_kind='kde',       # KDE on diagonal
    plot_kws={'alpha': 0.5, 's': 30},
    palette='Set2'
)
g.figure.suptitle('Pairplot — Iris Dataset (colored by species)', y=1.02, fontsize=13)
plt.show()
```

**What to look for in a pairplot:**

| Pattern                          | Interpretation                                        |
| -------------------------------- | ----------------------------------------------------- |
| Clear separation between colors  | This variable pair has discriminatory power           |
| Tight clusters along a line      | Strong linear correlation                             |
| Clusters overlap                 | This pair alone can't separate the groups             |
| Bimodal KDE on diagonal          | The variable has a different distribution per group   |
| Curved scatter shape             | Non-linear relationship — correlation coefficient misleading |

> 💡 For pairplots with many variables (>8), the plot becomes hard to read. Use `vars=` to select a subset of the most interesting variables, or proceed directly to PCA.

---

## 1.4 Grouped Statistics

Before modeling, compute summary statistics **broken down by group**. This reveals whether groups differ on key variables.

```python
# Summary statistics per species
group_summary = df.groupby('species')[num_cols].agg(['mean', 'std']).round(3)
print(group_summary)

# Heatmap of group means — normalized for comparability
group_means = df.groupby('species')[num_cols].mean()
group_means_normalized = (group_means - group_means.mean()) / group_means.std()

plt.figure(figsize=(8, 4))
sns.heatmap(
    group_means_normalized,
    annot=True, fmt='.2f',
    cmap='RdBu_r', center=0,
    linewidths=0.5
)
plt.title('Standardized Group Means — Iris Species')
plt.ylabel('Species')
plt.tight_layout()
plt.show()
```

> 💡 **Standardizing before the group mean heatmap** puts all variables on the same scale — essential when variables have different units or ranges (e.g., cm vs grams vs dollars).

---

## 1.5 Parallel Coordinates Plot

A parallel coordinates plot draws a vertical axis for each variable and connects each observation with a line. It reveals **multivariate profiles** and group separation that scatter plots may miss.

```python
from pandas.plotting import parallel_coordinates

# Normalize to [0, 1] so axes are comparable
df_norm = df[num_cols].copy()
for col in num_cols:
    df_norm[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
df_norm['species'] = df['species']

plt.figure(figsize=(10, 5))
parallel_coordinates(df_norm, 'species', color=['#4CAF50', '#2196F3', '#F44336'], alpha=0.4)
plt.title('Parallel Coordinates Plot — Iris Dataset')
plt.ylabel('Normalized Value')
plt.tight_layout()
plt.show()
```

> 💡 When group lines cross between two axes, those two variables have **different rank orderings** across groups — a potential interaction or discriminating feature. When lines within a group stay parallel, those observations share a similar multivariate profile.

---

## 1.6 Detecting Multicollinearity

**Multicollinearity** occurs when two or more predictors are highly correlated with each other. It does not affect predictions but severely distorts coefficient estimates and their standard errors in regression models.

### Step 1: Correlation Matrix Screen

Any |r| > 0.8 between two predictors is a warning sign.

```python
# Flag highly correlated pairs
corr_matrix = df[num_cols].corr().abs()
upper_tri = corr_matrix.where(
    np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
)
high_corr = [(col, row, upper_tri.loc[row, col])
             for col in upper_tri.columns
             for row in upper_tri.index
             if upper_tri.loc[row, col] > 0.8]

print("Highly correlated pairs (|r| > 0.8):")
for var1, var2, r in high_corr:
    print(f"  {var1}  ↔  {var2}:  r = {r:.3f}")
```

### Step 2: Variance Inflation Factor (VIF)

VIF measures how much the variance of a coefficient is inflated due to correlation with other predictors.

$$\text{VIF}_j = \frac{1}{1 - R_j^2}$$

where $R_j^2$ is the R² from regressing variable j on all other predictors.

| VIF Value  | Interpretation                          |
| ---------- | --------------------------------------- |
| 1          | No multicollinearity                    |
| 1 – 5      | Moderate — generally acceptable         |
| 5 – 10     | High — investigate and consider removing|
| > 10       | Severe — must address before modeling   |

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd

X = df[num_cols].copy()
X_with_const = pd.DataFrame({'const': 1, **{col: X[col] for col in X.columns}})

vif_data = pd.DataFrame({
    'Feature': num_cols,
    'VIF': [variance_inflation_factor(X_with_const.values, i + 1)
            for i in range(len(num_cols))]
}).sort_values('VIF', ascending=False)

print(vif_data.round(2))
```

> ⚠️ High VIF does not mean the model is wrong — it means coefficient estimates are unstable and should be interpreted cautiously. Solutions include: removing one of the correlated predictors, using PCA to create uncorrelated components, or applying Ridge regression (which tolerates multicollinearity better).

---

## 1.7 Simpson's Paradox: A Multivariate Warning

Simpson's Paradox occurs when a relationship observed in the **aggregate data** reverses or disappears when the data is **broken down by group**. It is a vivid demonstration of why multivariate thinking matters.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

# Simulated example: study hours vs exam score, masked by department
n = 60
dept_A = pd.DataFrame({
    'hours': np.random.normal(8, 1, n),
    'score': np.random.normal(85, 3, n),
    'dept':  'Dept A'
})
dept_A['score'] += 0.5 * dept_A['hours']  # positive within-group

dept_B = pd.DataFrame({
    'hours': np.random.normal(4, 1, n),
    'score': np.random.normal(70, 3, n),
    'dept':  'Dept B'
})
dept_B['score'] += 0.5 * dept_B['hours']  # positive within-group

data = pd.concat([dept_A, dept_B])

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Aggregate view — misleadingly negative
axes[0].scatter(data['hours'], data['score'], alpha=0.4, color='gray')
m, b = np.polyfit(data['hours'], data['score'], 1)
x_line = np.linspace(data['hours'].min(), data['hours'].max(), 100)
axes[0].plot(x_line, m * x_line + b, color='tomato', linewidth=2)
axes[0].set_title(f'Aggregate View\nSlope = {m:.2f} (misleading!)')
axes[0].set_xlabel('Study Hours')
axes[0].set_ylabel('Exam Score')

# Grouped view — correct positive relationship
colors = {'Dept A': '#2196F3', 'Dept B': '#4CAF50'}
for dept, group in data.groupby('dept'):
    axes[1].scatter(group['hours'], group['score'],
                    alpha=0.5, color=colors[dept], label=dept)
    m_g, b_g = np.polyfit(group['hours'], group['score'], 1)
    x_g = np.linspace(group['hours'].min(), group['hours'].max(), 100)
    axes[1].plot(x_g, m_g * x_g + b_g, color=colors[dept], linewidth=2)

axes[1].set_title("Grouped View\nBoth departments: positive slope ✅")
axes[1].set_xlabel('Study Hours')
axes[1].legend()

plt.suptitle("Simpson's Paradox — Aggregate vs Grouped Analysis", fontsize=13, y=1.02)
plt.tight_layout()
plt.show()
```

> 💡 The aggregate trend appeared negative only because Dept A (higher hours, higher scores) was a different department from Dept B (lower hours, lower scores). The confounding variable (department) masked the true within-group relationship. Always ask: **"Is there a lurking variable I haven't controlled for?"**  
> 在得出任何因果結論之前，都要問自己：「有沒有第三個變數同時影響了這兩個變數？」

---

## 1.8 Key Takeaways

| Concept                        | Key Point                                                                           |
| ------------------------------ | ----------------------------------------------------------------------------------- |
| **Correlation heatmap first**  | Get an overview of all pairwise linear relationships before detailed analysis       |
| **Pairplot reveals shape**     | Correlation coefficients miss non-linear relationships — always visualize           |
| **Group differences matter**   | Compute grouped summaries before pooling data for modeling                          |
| **Parallel coordinates**       | Best tool for comparing multivariate profiles across many groups simultaneously     |
| **VIF > 10 is a problem**      | High VIF destabilizes regression coefficients — investigate before fitting          |
| **Simpson's Paradox is real**  | Aggregate relationships can be completely opposite to within-group relationships    |

---
