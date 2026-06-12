# Seaborn: Matrix Plots

Matrix plots in Seaborn help visualize correlations and pairwise relationships across multiple variables. Common functions include **heatmap** and **pairplot**.

## Import Packages and Example Dataset

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Example dataset: Iris
iris = sns.load_dataset("iris")
```

## Heatmap (Correlation Matrix)

```python
corr = iris.corr()

sns.heatmap(corr, annot=True, cmap="coolwarm", center=0)
plt.title("Correlation Heatmap of Iris Dataset")
plt.show()
```

- `iris.corr()`: compute correlation matrix.
- `annot=True`: show correlation values inside cells.
- `cmap`: choose color map (e.g., "coolwarm", "viridis").
- `center=0`: set midpoint for diverging color palettes.

### Customization

```python
sns.heatmap(corr, annot=True, fmt=".2f", linewidths=0.5, square=True, cbar_kws={"shrink": 0.8})
plt.title("Customized Correlation Heatmap")
plt.show()
```

- `fmt=".2f"`: number formatting.
- `linewidths`: add separation lines between cells.
- `square=True`: make cells square.
- `cbar_kws`: control colorbar appearance.

## Pairplot

```python
sns.pairplot(data=iris)
plt.suptitle("Pairwise Relationships in Iris Dataset", y=1.02)
plt.show()
```

- Shows scatter plots for all variable pairs.
- Histograms or KDE plots appear along the diagonal.

### Select Variables

```python
sns.pairplot(data=iris, vars=["sepal_length", "sepal_width", "petal_length"])
plt.suptitle("Pairplot (Selected Variables)", y=1.02)
plt.show()
```

- `vars`: specify subset of variables.

### Group by Category

```python
sns.pairplot(data=iris, hue="species", diag_kind="kde", palette="Set1")
plt.suptitle("Pairplot by Species", y=1.02)
plt.show()
```

- `hue`: color-code by category.
- `diag_kind="kde"`: use KDE instead of histograms on the diagonal.
- `palette`: choose color palette.

## Key Takeaways

- **Heatmaps** visualize correlation matrices effectively.
- **Pairplots** reveal pairwise relationships and class separation.
- Use `hue` in pairplots to highlight grouping.
- Customize color maps, formats, and layouts for clarity.
