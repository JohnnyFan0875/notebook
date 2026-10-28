# Pandas Plotting

This note is about quick plotting directly from a `Series` or `DataFrame` during exploratory work. For survival-analysis visuals such as Kaplan-Meier curves and Cox diagnostics, see [Visualization in Survival Analysis](../../statistics/survival-analysis/visualization.md).

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

## Pandas: Time Series Visualization

Time series visualization is not just "draw a line chart". The real goal is to see change over time, detect trend and seasonality, compare periods, and highlight unusual events.

### Start with a Real Datetime Index

Most time-series plotting problems start with the date column still being plain text.

```python
import pandas as pd

df["datestamp"] = pd.to_datetime(df["datestamp"], errors="coerce")
df = df.set_index("datestamp").sort_index()
```

- use `errors="coerce"` to turn bad parses into `NaT`
- sort by time before plotting, rolling, or resampling
- a `DatetimeIndex` makes slicing, aggregation, and plotting much easier

### First Plot

```python
import matplotlib.pyplot as plt

ax = df.plot()
plt.show()
```

For a single time series, this is the default starting point:

- x-axis: time
- y-axis: observed values
- one line per column

If the chart already looks noisy or unreadable, that is usually a signal to aggregate, smooth, or subset the data before styling it further.

### Basic Plot Styling

```python
plt.style.use("fivethirtyeight")

ax = df.plot(
    figsize=(12, 5),
    fontsize=12,
    linewidth=2,
    linestyle="-",
    color="steelblue",
)
ax.set_title("CO2 Levels Over Time", fontsize=16)
ax.set_ylabel("CO2")
```

Useful knobs:

- `figsize=` controls readability
- `linewidth=` makes long series easier to inspect
- `linestyle=` can separate raw vs summary series
- `fontsize=` matters when the x-axis is dense
- `plt.style.use(...)` is a quick way to change the chart feel consistently

You can inspect available style sheets with:

```python
print(plt.style.available)
```

### Slice Before You Plot

Long time series often become clearer when you zoom into a period of interest.

```python
df_subset = df.loc["1960":"1970"]
ax = df_subset.plot(color="blue", fontsize=14)
```

- date slicing works naturally once the index is datetime-like
- plotting a focused window is often better than plotting everything at once
- this is especially helpful when investigating regime changes or events

### Annotate Important Dates and Thresholds

Reference lines make plots easier to read when you need to explain why a period matters.

```python
ax = discoveries.plot(color="blue")
ax.axvline("1969-01-01", color="red", linestyle="--")
ax.axhline(4, color="green", linestyle="--")
```

Use:

- `ax.axvline(...)` for event dates
- `ax.axhline(...)` for thresholds or targets

You can also highlight ranges:

```python
ax.axvspan("1964-01-01", "1968-01-01", color="red", alpha=0.3)
ax.axhspan(6, 8, color="green", alpha=0.3)
```

- `axvspan()` highlights a time interval
- `axhspan()` highlights a value band

### Smooth with Rolling Windows

Raw series often contain short-term variation that hides the longer pattern.

```python
co2_levels_mean = co2_levels.rolling(window=52).mean()
ax = co2_levels_mean.plot()
ax.set_title("52-week Rolling Mean")
```

- rolling averages reduce short-term noise
- the window should match the business or calendar rhythm you care about
- common examples: `7`, `30`, `52`, `12`

A rolling mean is useful when you want to emphasize trend or cycle rather than week-to-week fluctuation.

### Aggregate Before Comparing Periods

Sometimes the better chart is not the raw series but a monthly, quarterly, or yearly summary.

```python
co2_levels_by_month = co2_levels.resample("M").mean()
co2_levels_by_month.plot()
```

Common patterns:

```python
ts.resample("W").mean()
ts.resample("M").mean()
ts.resample("Q").sum()
ts.resample("Y").mean()
```

- use `mean()` for average level
- use `sum()` for accumulated totals
- aggregation is often the cleanest way to reveal seasonality

### Distribution Views for a Time Series

A time series is still a distribution of values, not just a path over time.

#### Boxplot

```python
ax = df.boxplot()
ax.set_title("Boxplot of Time Series Values")
```

Useful for:

- spotting spread
- comparing typical range
- finding possible outliers

#### Histogram

```python
ax = df.plot(kind="hist", bins=100)
ax.set_title("Histogram of Time Series Values")
```

Useful for:

- checking skew
- seeing whether values cluster into ranges
- comparing raw scale across periods or series

#### Density Plot

```python
ax = df.plot(kind="density", linewidth=2)
ax.set_title("Density Plot of Time Series Values")
```

Useful for:

- a smoother view of the value distribution
- comparing multiple series without histogram bin sensitivity

### Multiple Time Series on One Plot

When several related series share the same time index, plotting them together is the fastest comparison.

```python
plt.style.use("fivethirtyeight")
ax = df.plot(figsize=(12, 4), fontsize=14)
```

This is good for:

- relative level comparison
- seeing co-movement
- spotting divergence periods

If the default colors are too similar, choose a colormap explicitly.

```python
ax = df.plot(colormap="Dark2", figsize=(14, 7))
```

### Area Plots

If the goal is composition or cumulative visual mass, area charts can work well.

```python
ax = df.plot.area(figsize=(12, 4), fontsize=14)
```

Best for:

- components of a whole
- relative contribution over time

Be careful: area plots can hide exact line shapes when too many series overlap.

### Move the Legend Out of the Way

Multi-series plots often become unreadable because the legend covers the data.

```python
ax = jobs_by_month.plot(figsize=(12, 5), colormap="Dark2")
ax.legend(bbox_to_anchor=(1.0, 0.5), loc="center left")
```

This is a small change, but it greatly improves readability when many lines are present.

### Facet Plots for Many Series

When overlaying many lines becomes cluttered, separate them into small multiples.

```python
jobs.plot(
    subplots=True,
    figsize=(12, 10),
    linewidth=0.5,
)
```

- `subplots=True` gives each column its own axis
- this is often better than one giant multi-line chart
- facet-style plots help compare shape without line overlap

### ACF / PACF and Decomposition

ACF / PACF 與趨勢—季節分解見 [自相關](../../statistics/time-series-analysis/autocorrelation.md) 與 [分解](../../statistics/time-series-analysis/decomposition.md)。

### Reading Checklist

When looking at a time-series chart, ask:

- Is there a long-term trend?
- Is there seasonality or repeating structure?
- Are there sudden breaks, spikes, or level shifts?
- Would aggregation make the pattern easier to see?
- Does smoothing reveal a clearer signal?
- Should this be one combined chart or multiple subplots?

### Key Takeaways

- Convert time columns to `datetime64` and use a datetime index early.
- Slice, aggregate, or smooth before over-styling a noisy chart.
- Use annotations and spans to explain events and thresholds.
- Compare raw series, rolling summaries, and resampled aggregates for different views of the same process.
- For serious time-series reading, go beyond line charts into ACF, PACF, and decomposition.
