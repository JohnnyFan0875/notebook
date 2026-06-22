# Seaborn: Distribution Plots

Distribution plots help visualize the shape of a single variable’s distribution, compare across groups, and display density estimates. Seaborn provides **histplot**, **kdeplot**, and **displot** for flexible distribution visualization.

## Import Packages and Example Dataset

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Example dataset: Iris
iris = sns.load_dataset("iris")
```

## Histogram with `histplot`

```python
sns.histplot(data=iris, x="sepal_length", bins=20, color="skyblue", edgecolor="black")
plt.title("Histogram of Sepal Length")
plt.show()
```

- By default, the y-axis shows counts (number of observations per bin).
- `bins`: control number of intervals.
- `edgecolor`: improve readability.

## Grouped Histogram with Hue

```python
sns.histplot(data=iris, x="sepal_length", hue="species", multiple="stack")
plt.title("Stacked Histogram by Species")
plt.show()
```

- `hue`: subgroup categories by color.
- `multiple="stack"`: stack histograms; other options include `dodge` and `fill`.

## KDE Plot (Kernel Density Estimate)

```python
sns.kdeplot(data=iris, x="sepal_length", hue="species", cut=0)
plt.title("Kernel Density Estimate by Species")
plt.show()
```

- Smooth estimate of distribution.
- Default y-axis: probability density (area under curve = 1).
- `cut=0`: trims density at data limits.

## Cumulative Distribution

```python
sns.kdeplot(data=iris, x="sepal_length", hue="species", cumulative=True, cut=0)
plt.title("Cumulative Distribution")
plt.show()
```

- Shows cumulative probability (monotonically increasing curves).
- Useful for percentile interpretation.

## Displot (Figure-Level)

```python
sns.displot(data=iris, x="petal_length", hue="species", kind="kde", fill=True)
plt.show()
```

- `displot`: high-level wrapper that creates a **FacetGrid**.
- `kind`: choose `hist` or `kde`.
- `fill=True`: fill the KDE curve.

## Overlay Histogram and KDE

```python
sns.histplot(data=iris, x="petal_width", kde=True, bins=15, color="purple")
plt.title("Histogram + KDE Overlay")
plt.show()
```

- `kde=True`: overlay density curve on top of histogram.
- Combines discrete bin counts with smooth density.

## Difference Between `histplot` and `kdeplot`

- **Histogram**: y-axis shows **counts** (number of samples per bin).
- **KDE**: y-axis is **normalized**, so the total area under the curve = 1.
- Setting `stat="density"` in `histplot` makes it comparable to KDE.

**Example:**

```python
fig, ax = plt.subplots()
sns.histplot(data=iris, x="sepal_length", stat="density", bins=15, color="skyblue", label="Histogram")
sns.kdeplot(data=iris, x="sepal_length", color="red", label="KDE")
ax.legend()
plt.title("Histogram vs KDE")
plt.show()
```

- Both curves are now normalized for direct comparison.

## Comparison: Countplot vs Histplot

- **Countplot**: best for categorical/discrete variables.
- **Histplot**: best for continuous variables.

Example:

```python
sns.countplot(x="species", data=iris)
plt.title("Countplot (Categorical)")
plt.show()

sns.histplot(x="sepal_length", data=iris)
plt.title("Histplot (Continuous)")
plt.show()
```

## Key Takeaways

- Use **`histplot`** for histograms (discrete binning of continuous variables).
- Use **`kdeplot`** for smooth density estimation.
- Use **`displot`** for figure-level distribution visualization (supports `FacetGrid`).
- Overlay histogram + KDE for a balanced view of raw data and smooth distribution.
- Remember: histograms show **counts**, KDE normalizes to **area=1**.
