# Matplotlib: Advanced Topics

This section covers advanced Matplotlib techniques, including plotting different variables on dual axes, using annotations effectively, and integrating with other visualization tools.

## Import Packages and Example Dataset

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Example dataset: Iris
iris = sns.load_dataset("iris")
```

## Dual Y-Axis Plot (Different Variables)

Sometimes it is useful to compare two variables with different scales on the same x-axis.

```python
x = iris.index
y1 = iris["sepal_length"]
y2 = iris["petal_length"]

fig, ax1 = plt.subplots()

# First variable
ax1.plot(x, y1, color="blue")
ax1.set_xlabel("Index")
ax1.set_ylabel("Sepal Length (cm)", color="blue")
ax1.tick_params(axis='y', colors="blue")

# Second variable on twin y-axis
ax2 = ax1.twinx()
ax2.plot(x, y2, color="red")
ax2.set_ylabel("Petal Length (cm)", color="red")
ax2.tick_params(axis='y', colors="red")

plt.title("Dual Y-Axis Plot: Sepal vs Petal Length")
plt.show()
```

- `twinx()`: creates a new y-axis sharing the same x-axis.
- Useful when comparing variables with different scales.

## Annotating Plots with Arrows

Annotations add context to specific data points.

```python
fig, ax = plt.subplots()
ax.plot(iris.index, iris["sepal_length"], color="blue")

ax.annotate("Notable Point",
            xy=(iris.index[10], iris["sepal_length"][10]),
            xytext=(20, 8),
            arrowprops={"arrowstyle": "->", "color": "gray"})

ax.set_title("Annotation Example")
plt.show()
```

- `annotate()`: add labels pointing to data points.
- `arrowprops`: customize arrow style, color, shape.

## Combining Dual Axes and Annotation

```python
x = pd.date_range("2000-01", periods=50, freq="M")
y1 = np.sin(np.linspace(0, 3*np.pi, 50))
y2 = np.cos(np.linspace(0, 3*np.pi, 50))

fig, ax1 = plt.subplots(figsize=(8,4))

ax1.plot(x, y1, color="blue")
ax1.set_ylabel("Sine Wave", color="blue")

ax2 = ax1.twinx()
ax2.plot(x, y2, color="red")
ax2.set_ylabel("Cosine Wave", color="red")

# Add annotation
ax2.annotate("Phase difference",
             xy=(x[15], y2[15]),
             xytext=(x[5], -0.5),
             arrowprops={"arrowstyle": "->", "color": "gray"})

plt.title("Dual Y-Axis with Annotation")
plt.show()
```

- Demonstrates combining advanced features.

## Missing Data Visualization with Missingno

`missingno` is a small library that provides a simple way to visualize missing data patterns. It uses Matplotlib under the hood.

```python
import missingno as msno

# Example: airquality dataset
airquality = sns.load_dataset("titanic").drop(columns=["alive"])  # simulate missingness

msno.matrix(airquality.sort_values("age"))
plt.show()
```

- `msno.matrix()`: visualizes missing values in a matrix plot.
- Helps identify patterns in missing data.

## Key Takeaways

- Use **dual axes** (`twinx`) for comparing variables with different scales.
- **Annotations** enhance interpretability by highlighting points of interest.
- Combine features (dual axes + annotations) for advanced storytelling.
- Specialized libraries like **missingno** extend Matplotlib for domain-specific tasks (e.g., missing data visualization).
