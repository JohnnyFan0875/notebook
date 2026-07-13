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

## `.plot()` as the Fastest First Pass

當你只是想快速看資料型態與大致趨勢，`DataFrame.plot()` 和 `Series.plot()` 通常是最快的第一步。

它的心智模型很簡單：

- 資料還在 pandas 裡
- 先不要急著切去 Matplotlib / Seaborn
- 直接用 `kind=` 指定圖型，快速檢查 pattern

常見 `kind` 包括：

- `line`
- `bar`
- `barh`
- `hist`
- `box`
- `kde` / `density`
- `area`
- `pie`
- `scatter`
- `hexbin`

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

如果你已經把資料整理成合適的 index 和欄位，pandas `.plot()` 往往比手寫 `plt.plot(...)` 更省力。

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

## Choosing Between pandas, Matplotlib, and Seaborn

可以把三者分成不同層級：

- pandas `.plot()`: 最快的 EDA 起手式
- Matplotlib: 需要更細的 figure / axes 控制時
- Seaborn: 需要較高階統計視覺化與預設美觀樣式時

也就是說，pandas `.plot()` 很適合回答：

- 這欄大概長什麼樣？
- 幾個欄位之間趨勢有沒有明顯異常？
- 這個欄位比較像該畫 line、bar 還是 hist？

當你需要更細緻的圖例、分面、回歸線或主題樣式，再往下切到 Matplotlib 或 Seaborn 會比較自然。

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
