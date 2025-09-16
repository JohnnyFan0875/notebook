# Matplotlib: Scatter Plot

Scatter plots visualize the relationship between two continuous variables, highlighting correlation, clustering, and outliers.

## Import Packages and Example Dataset

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Example dataset: Iris
iris = sns.load_dataset("iris")
```

## Basic Scatter Plot

```python
fig, ax = plt.subplots()
ax.scatter(iris["sepal_length"], iris["sepal_width"], color="blue", label="Iris data")

ax.set_xlabel("Sepal Length (cm)")
ax.set_ylabel("Sepal Width (cm)")
ax.set_title("Iris Sepal Length vs Width")
ax.legend()
plt.show()
```

- `ax.scatter(x, y)`: plots points with `x` on the x-axis and `y` on the y-axis.
- Add `label` and `legend` for clarity.

## Multiple Groups

```python
fig, ax = plt.subplots()

for species, data in iris.groupby("species"):
    ax.scatter(data["sepal_length"], data["sepal_width"], label=species)

ax.set_xlabel("Sepal Length (cm)")
ax.set_ylabel("Sepal Width (cm)")
ax.set_title("Sepal Length vs Width by Species")
ax.legend()
plt.show()
```

- Different species are plotted in different colors.
- Grouping by categories shows clustering patterns.

## Customization: Marker Size and Color

```python
fig, ax = plt.subplots()
scatter = ax.scatter(
    iris["sepal_length"],
    iris["sepal_width"],
    c=iris["petal_length"],      # color scale
    s=iris["petal_width"] * 20,  # marker size
    cmap="viridis",
    alpha=0.7
)

ax.set_xlabel("Sepal Length (cm)")
ax.set_ylabel("Sepal Width (cm)")
ax.set_title("Scatter Plot with Color and Size Encoding")

# Add colorbar for context
plt.colorbar(scatter, ax=ax, label="Petal Length")
plt.show()
```

- `c`: controls marker colors (mapped to a numeric column).
- `s`: controls marker size (mapped to another column).
- `alpha`: transparency.
- `cmap`: colormap.

## Add Reference Lines

```python
fig, ax = plt.subplots()
ax.scatter(iris["sepal_length"], iris["sepal_width"], color="green")

# Add horizontal and vertical reference lines
ax.axhline(y=3, color="red", linestyle="--", label="y=3")
ax.axvline(x=6, color="blue", linestyle=":", label="x=6")

ax.set_title("Scatter Plot with Reference Lines")
ax.legend()
plt.show()
```

- `axhline` and `axvline` add reference thresholds.

## Subplots

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].scatter(iris["petal_length"], iris["petal_width"], color="purple")
axes[0].set_title("Petal Scatter")

axes[1].scatter(iris["sepal_length"], iris["petal_length"], color="orange")
axes[1].set_title("Sepal vs Petal")

plt.suptitle("Iris Scatter Plot Examples")
plt.show()
```

- Multiple scatter plots can be shown side-by-side for comparisons.

## Scatter with Trend Line

```python
import numpy as np

x = iris["sepal_length"]
y = iris["sepal_width"]

# Fit linear trend line
m, b = np.polyfit(x, y, 1)

fig, ax = plt.subplots()
ax.scatter(x, y, alpha=0.6)
ax.plot(x, m*x + b, color="red", label="Trend Line")
ax.set_title("Scatter with Linear Fit")
ax.legend()
plt.show()
```

- Use `np.polyfit` to overlay a regression line.

## Annotation

```python
fig, ax = plt.subplots()
ax.scatter(iris["sepal_length"], iris["sepal_width"], color="blue")

ax.annotate("Potential Outlier",
            xy=(iris["sepal_length"][100], iris["sepal_width"][100]),
            xytext=(7.5, 2.5),
            arrowprops={"arrowstyle": "->", "color": "gray"})

ax.set_title("Scatter Plot with Annotation")
plt.show()
```

- `annotate()`: highlights specific data points.

## Key Takeaways

- Scatter plots reveal **relationships** and **patterns** between two variables.
- Use **color, size, and transparency** to encode additional dimensions.
- Reference lines, subplots, and annotations enhance interpretability.
- Trend lines help show correlation direction and strength.
