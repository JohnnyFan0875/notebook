# Matplotlib: Bar Plot & Histogram

Bar plots and histograms are commonly used to show categorical counts and distributions of numerical data.

## Import Packages and Example Dataset

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Example dataset: Iris
iris = sns.load_dataset("iris")
```

## Basic Bar Plot

```python
species_counts = iris["species"].value_counts()

fig, ax = plt.subplots()
ax.bar(species_counts.index, species_counts.values, color="skyblue")

ax.set_xlabel("Species")
ax.set_ylabel("Count")
ax.set_title("Iris Species Count")
plt.show()
```

- `ax.bar(x, y)`: draws bars at categories in `x` with heights `y`.
- Useful for categorical comparisons.

## Grouped Bar Plot

```python
# Mean sepal length by species and sepal width rounded
iris_group = iris.groupby(["species", iris["sepal_width"].round()])["sepal_length"].mean().unstack()

fig, ax = plt.subplots()
iris_group.T.plot(kind="bar", ax=ax)

ax.set_xlabel("Sepal Width (rounded)")
ax.set_ylabel("Mean Sepal Length")
ax.set_title("Grouped Bar Plot: Sepal Length by Species & Sepal Width")
plt.show()
```

- Grouped bars show comparisons across multiple categorical variables.

## Stacked Bar Plot

```python
values = np.array([[5, 3, 2], [4, 7, 6]])
labels = ["Group1", "Group2", "Group3"]

fig, ax = plt.subplots()
ax.bar(labels, values[0], label="Category A")
ax.bar(labels, values[1], bottom=values[0], label="Category B")

ax.set_ylabel("Value")
ax.set_title("Stacked Bar Plot Example")
ax.legend()
plt.show()
```

- `bottom`: stacks bars on top of each other.

## Horizontal Bar Plot

```python
species_counts = iris["species"].value_counts()

fig, ax = plt.subplots()
ax.barh(species_counts.index, species_counts.values, color="lightgreen")

ax.set_xlabel("Count")
ax.set_ylabel("Species")
ax.set_title("Horizontal Bar Plot: Iris Species Count")
plt.show()
```

- `ax.barh()`: horizontal version of bar plot.

## Basic Histogram

```python
fig, ax = plt.subplots()
ax.hist(iris["sepal_length"], bins=10, color="orange", edgecolor="black")

ax.set_xlabel("Sepal Length (cm)")
ax.set_ylabel("Frequency")
ax.set_title("Histogram of Sepal Length")
plt.show()
```

- `ax.hist(data, bins)`: plots distribution.
- `bins`: number of intervals (default = 10).

## Multiple Histograms

```python
fig, ax = plt.subplots()

ax.hist(iris.loc[iris["species"]=="setosa", "sepal_length"], alpha=0.5, label="Setosa")
ax.hist(iris.loc[iris["species"]=="versicolor", "sepal_length"], alpha=0.5, label="Versicolor")
ax.hist(iris.loc[iris["species"]=="virginica", "sepal_length"], alpha=0.5, label="Virginica")

ax.set_xlabel("Sepal Length (cm)")
ax.set_ylabel("Frequency")
ax.set_title("Sepal Length Distribution by Species")
ax.legend()
plt.show()
```

- Overlay histograms using transparency (`alpha`).

## Density Overlay (Histogram + KDE)

```python
fig, ax = plt.subplots()

sns.histplot(iris["sepal_length"], kde=True, bins=15, color="skyblue", ax=ax)
ax.set_title("Histogram with Density Curve")
plt.show()
```

- `sns.histplot`: adds kernel density estimate (KDE) for smoother visualization.

## Key Takeaways

- **Bar plots**: compare categories (basic, grouped, stacked, horizontal).
- **Histograms**: show distribution of continuous variables.
- **Customization**: use color, edge styles, and transparency for clarity.
- Combine with **density curves** for better distributi
