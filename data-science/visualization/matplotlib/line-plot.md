# Matplotlib: Line Plot

Line plots are one of the most common ways to visualize continuous data. They show how a variable changes over time or along a sequence.

## Import Packages and Example Dataset

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Example dataset: Iris
iris = sns.load_dataset("iris")
```

## Basic Line Plot

```python
fig, ax = plt.subplots()
ax.plot(iris.index, iris["sepal_length"], marker="o", color="r", linestyle="--")

ax.set_xlabel("Index")
ax.set_ylabel("Sepal Length")
ax.set_title("Iris Sepal Length (Line Plot)")
plt.show()
```

- `marker`: style of points (`'o'`, `'s'`, `'^'`)
- `color`: line color
- `linestyle`: `'--'`, `'-'`, `':'`

## Multiple Lines

```python
fig, ax = plt.subplots()
ax.plot(iris.index, iris["sepal_length"], label="Sepal Length")
ax.plot(iris.index, iris["sepal_width"], label="Sepal Width")

ax.set_xlabel("Index")
ax.set_ylabel("Measurement (cm)")
ax.set_title("Sepal Length vs Width")
ax.legend()
plt.show()
```

- Use labels to distinguish multiple lines.
- `ax.legend()` adds a legend.

## Subplots

```python
fig, ax = plt.subplots(2, 1, sharex=True)
ax[0].plot(iris.index, iris["petal_length"], color="blue")
ax[0].set_ylabel("Petal Length")

ax[1].plot(iris.index, iris["petal_width"], color="green")
ax[1].set_xlabel("Index")
ax[1].set_ylabel("Petal Width")

plt.suptitle("Iris Petal Measurements")
plt.show()
```

- `sharex=True`: share x-axis scale.
- Useful for comparing multiple variables side-by-side.

## Error Bars

```python
import numpy as np

x = np.arange(10)
y = np.sin(x)
y_err = 0.2

fig, ax = plt.subplots()
ax.errorbar(x, y, yerr=y_err, fmt='-o', ecolor='gray', capsize=5)
ax.set_title("Line Plot with Error Bars")
plt.show()
```

- `yerr`: vertical error bars.
- `fmt`: marker and line style.
- `capsize`: adds caps to error bars.

## Reference Lines

```python
fig, ax = plt.subplots()
ax.plot(iris.index, iris["sepal_length"])

ax.axhline(y=6, color="red", linestyle="--", label="Reference Line")
ax.axvline(x=50, color="blue", linestyle=":", label="Sample Cutoff")
ax.legend()
plt.show()
```

- `axhline`: horizontal reference line.
- `axvline`: vertical reference line.

## Dual Axes

```python
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot(iris.index, iris["sepal_length"], color="blue", label="Sepal Length")
ax2.plot(iris.index, iris["petal_length"], color="red", label="Petal Length")

ax1.set_xlabel("Index")
ax1.set_ylabel("Sepal Length", color="blue")
ax2.set_ylabel("Petal Length", color="red")
plt.title("Dual Axis Line Plot")
plt.show()
```

- `twinx()`: overlay two plots with different y-axes.
- Useful for comparing two series with different scales.

## Annotation

```python
fig, ax = plt.subplots()
ax.plot(iris.index, iris["sepal_length"], color="blue")

ax.annotate("Outlier?",
            xy=(iris.index[10], iris["sepal_length"][10]),
            xytext=(20, 8),
            arrowprops={"arrowstyle": "->", "color": "gray"})

ax.set_title("Line Plot with Annotation")
plt.show()
```

- `annotate()`: highlight interesting points with text and arrows.

## Key Takeaways

- **Line plots** are used to show trends over an index or continuous variable.
- Customization includes markers, colors, styles, subplots, error bars, reference lines, dual axes, and annotations.
