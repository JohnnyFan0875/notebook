# Matplotlib: Basics

This section introduces the basics of Matplotlib, focusing on figure creation, labels, titles, ticks, scales, and saving figures.

## Import Packages and Example Dataset

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Example dataset: Iris
iris = sns.load_dataset("iris")
```

## Create a Basic Plot

```python
fig, ax = plt.subplots()
ax.plot(iris.index, iris["sepal_length"], marker='o', color='r', linestyle='--')

ax.set_xlabel("Index")
ax.set_ylabel("Sepal Length (cm)")
ax.set_title("Basic Line Plot: Sepal Length")
plt.show()
```

- `plt.subplots()`: creates a figure (`fig`) and axes (`ax`).
- `ax.plot()`: plots data with markers, colors, and line styles.

## Styling and Themes

```python
plt.style.use('ggplot')  # Other options: 'seaborn', 'grayscale'

fig, ax = plt.subplots()
ax.plot(iris.index, iris["petal_length"], color='blue')
ax.set_title("Styled Plot with ggplot Theme")
plt.show()
```

- `plt.style.use()`: apply predefined styles to plots.

## Set Size of Figure

```python
fig, ax = plt.subplots()
fig.set_size_inches(8, 4)
ax.plot(iris.index, iris["petal_width"], color='green')
ax.set_title("Customized Figure Size")
plt.show()
```

- `fig.set_size_inches(width, height)`: control output dimensions.

## Ticks and Labels

```python
fig, ax = plt.subplots()
ax.plot(iris.index[:10], iris["sepal_length"][:10], marker='o')

ax.set_xticks(range(0, 11, 2))
ax.set_xticklabels(["Zero","Two","Four","Six","Eight","Ten"])
ax.set_yticks([4, 5, 6, 7, 8])

ax.set_xlabel("Custom X Axis")
ax.set_ylabel("Sepal Length")
ax.set_title("Customized Ticks and Labels")
plt.show()
```

- `set_xticks()`, `set_yticks()`: control tick positions.
- `set_xticklabels()`: customize tick labels.

## Axis Limits and Scales

```python
fig, ax = plt.subplots()
ax.plot(iris.index, iris["sepal_length"])

ax.set_xlim(0, 50)
ax.set_ylim(4, 8)
ax.set_yscale('linear')  # Options: 'linear', 'log'

ax.set_title("Axis Limits and Scales")
plt.show()
```

- `set_xlim()`, `set_ylim()`: control visible ranges.
- `set_yscale('log')`: logarithmic scale.

## Save Figures

```python
fig, ax = plt.subplots()
ax.plot(iris.index, iris["petal_length"], color='purple')
ax.set_title("Saved Figure Example")

fig.savefig("iris_plot.png")
```

- `fig.savefig()`: saves figure to file in formats like PNG, PDF, SVG.

## Clear Figures

```python
plt.clf()  # clear the current figure
```

- Useful for scripts generating multiple plots in sequence.

## Handling Non-English Characters

```python
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
```

- Ensures proper display of non-English characters and minus signs.
- Reference
  - [Medium](https://medium.com/marketingdatascience/%E8%A7%A3%E6%B1%BApython-3-matplotlib%E8%88%87seaborn%E8%A6%96%E8%A6%BA%E5%8C%96%E5%A5%97%E4%BB%B6%E4%B8%AD%E6%96%87%E9%A1%AF%E7%A4%BA%E5%95%8F%E9%A1%8C-f7b3773a889b)
  - [PythonforDataScience (GitHub)](https://github.com/PyDataScience/PythonforDataScience/blob/master/Matplotlib/%E4%BD%9C%E5%9C%96%E9%A1%AF%E7%A4%BA%E4%B8%AD%E6%96%87.ipynb)

## Key Takeaways

- `plt.subplots()`: central for creating figures and axes.
- Customize plots with labels, ticks, limits, scales, and styles.
- Save figures with `fig.savefig()` for sharing or publications.
- Handle special cases (non-English characters) with `rcParams`.
