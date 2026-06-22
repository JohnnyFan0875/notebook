# Pandas: Visualization

Pandas integrates with Matplotlib, allowing you to quickly visualize data directly from a DataFrame or Series using the `.plot()` and `.hist()` methods.

## Import Packages and Example Dataset

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Example dataset: Iris
iris = sns.load_dataset("iris")
```

## Bar and Line Plots (Single Column)

If the DataFrame has only an index and one column:

```python
# Bar plot
iris[["sepal_length"]].head(10).plot(kind="bar", title="Bar Plot: Sepal Length")
plt.show()

# Line plot
iris[["sepal_length"]].head(10).plot(kind="line", title="Line Plot: Sepal Length")
plt.show()
```

- `kind='bar'`: vertical bar plot.
- `kind='line'`: default plot (line graph).

For time series, it is often better to set the date column as the index first:

```python
prices = pd.DataFrame({
    "Date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
    "Close": [100, 102, 101]
})

prices = prices.set_index("Date")
prices.plot(y="Close", title="Close Price Over Time")
plt.show()
```

- A datetime index makes time-order plots more natural.
- This pattern is especially common in finance, where the x-axis is almost always a trading date.

## Scatter Plot (Multiple Columns)

```python
iris.plot(x="sepal_length", y="petal_length", kind="scatter", title="Scatter Plot: Sepal vs Petal Length")
plt.show()
```

- `x` and `y`: specify columns.
- `title`: add a title directly.

## Box Plot

```python
iris.plot(kind="box", title="Box Plot of Iris Features")
plt.show()
```

- Creates box plots for all numeric columns.

## Matplotlib Equivalent

Pandas `.plot()` is built on Matplotlib. You can achieve the same with direct calls:

```python
subset = iris[["sepal_length"]].head(10)

plt.bar(subset.index, subset.values.flatten())
plt.plot(subset.index, subset.values.flatten(), marker="o", color="red")
plt.title("Matplotlib Equivalent of Pandas Plot")
plt.show()
```

- `plt.bar`: equivalent to `df.plot(kind='bar')`.
- `plt.plot`: equivalent to `df.plot(kind='line')`.

## Histogram (Single Column)

```python
iris["sepal_length"].plot.hist(bins=10, alpha=0.7, title="Histogram of Sepal Length")
plt.show()
```

- `plot.hist()`: histogram wrapper.
- Equivalent to `iris["sepal_length"].hist()` but with fewer options.

## Histogram (Multiple Columns)

```python
iris[["sepal_length", "sepal_width"]].plot.hist(alpha=0.5, bins=20)
plt.legend(["Sepal Length", "Sepal Width"])
plt.title("Overlayed Histograms")
plt.show()
```

- Overlay multiple histograms by selecting multiple columns.
- Use `alpha` for transparency.

## Comparison: `Series.hist()` vs `Series.plot.hist()`

```python
# Same basic output
iris["petal_length"].plot.hist(title="plot.hist version")
plt.show()

iris["petal_length"].hist(title="hist version")
plt.show()
```

- `plot.hist()`: simpler, fewer options.
- `hist()`: more arguments (e.g., cumulative, density, stacked).

## Key Takeaways

- Use **`df.plot()`** for quick visualization of DataFrames and Series.
- Supports multiple kinds: `line`, `bar`, `scatter`, `box`, `hist`.
- Equivalent Matplotlib calls (`plt.bar`, `plt.plot`, `plt.hist`) provide more control.
- `Series.hist()` offers more flexibility than `Series.plot.hist()`.
- Ideal for **exploratory data analysis (EDA)** when working directly with DataFrames.
