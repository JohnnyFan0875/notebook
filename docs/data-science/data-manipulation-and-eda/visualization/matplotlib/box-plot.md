# Matplotlib: Box Plot

Box plots (also known as whisker plots) display the distribution of numerical data and help detect outliers. They summarize datasets using five statistics: **minimum, first quartile (Q1), median, third quartile (Q3), and maximum**.

## Import Packages and Example Dataset

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Example dataset: Iris
iris = sns.load_dataset("iris")
```

## Basic Box Plot

```python
fig, ax = plt.subplots()
ax.boxplot(iris["sepal_length"])

ax.set_ylabel("Sepal Length (cm)")
ax.set_title("Box Plot of Sepal Length")
plt.show()
```

- Shows the median, interquartile range, and whiskers.
- Outliers are displayed as individual points.

## Multiple Box Plots

```python
fig, ax = plt.subplots()
ax.boxplot([iris["sepal_length"], iris["sepal_width"]])

ax.set_xticklabels(["Sepal Length", "Sepal Width"])
ax.set_ylabel("Measurement (cm)")
ax.set_title("Box Plots of Sepal Measurements")
plt.show()
```

- Pass a list of arrays to `ax.boxplot()` to compare multiple variables.

## Grouped Box Plot

```python
fig, ax = plt.subplots()

# Create grouped box plots by species
species = iris["species"].unique()
data = [iris.loc[iris["species"] == sp, "sepal_length"] for sp in species]
ax.boxplot(data, labels=species)

ax.set_ylabel("Sepal Length (cm)")
ax.set_title("Sepal Length by Species")
plt.show()
```

- Groups data by categories (species) for comparison.

## Horizontal Box Plot

```python
fig, ax = plt.subplots()
ax.boxplot(iris["petal_length"], vert=False)

ax.set_xlabel("Petal Length (cm)")
ax.set_title("Horizontal Box Plot of Petal Length")
plt.show()
```

- `vert=False`: draws a horizontal box plot.

## Customized Box Plot

```python
fig, ax = plt.subplots()
ax.boxplot(iris["sepal_width"],
           notch=True,           # notched box for median CI
           patch_artist=True,    # fill with color
           boxprops=dict(facecolor="lightblue", color="blue"),
           medianprops=dict(color="red"))

ax.set_ylabel("Sepal Width (cm)")
ax.set_title("Customized Box Plot")
plt.show()
```

- `notch=True`: shows a confidence interval around the median.
- `patch_artist=True`: allows coloring.
- Customize `boxprops`, `medianprops`, etc.

## Overlaying Data Points

```python
fig, ax = plt.subplots()
ax.boxplot(iris["petal_width"], positions=[1])

# Overlay scatter plot of actual values
x_positions = [1] * len(iris)
ax.scatter(x_positions, iris["petal_width"], color="gray", alpha=0.6)

ax.set_ylabel("Petal Width (cm)")
ax.set_title("Box Plot with Data Overlay")
plt.show()
```

- Combining box plot and scatter plot helps visualize raw data distribution.

## Key Takeaways

- Box plots summarize data using quartiles and highlight outliers.
- Variations: multiple, grouped, horizontal, customized.
- Overlaying raw data adds context beyond summary statistics.
- Useful for comparing distributions across categories (e.g., Iris species).
