# Pandas: Time Series Visualization

Time series visualization is not just "draw a line chart". The real goal is to see change over time, detect trend and seasonality, compare periods, and highlight unusual events.

## Start with a Real Datetime Index

Most time-series plotting problems start with the date column still being plain text.

```python
import pandas as pd

df["datestamp"] = pd.to_datetime(df["datestamp"], errors="coerce")
df = df.set_index("datestamp").sort_index()
```

- use `errors="coerce"` to turn bad parses into `NaT`
- sort by time before plotting, rolling, or resampling
- a `DatetimeIndex` makes slicing, aggregation, and plotting much easier

## First Plot

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

## Basic Plot Styling

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

## Slice Before You Plot

Long time series often become clearer when you zoom into a period of interest.

```python
df_subset = df.loc["1960":"1970"]
ax = df_subset.plot(color="blue", fontsize=14)
```

- date slicing works naturally once the index is datetime-like
- plotting a focused window is often better than plotting everything at once
- this is especially helpful when investigating regime changes or events

## Annotate Important Dates and Thresholds

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

## Smooth with Rolling Windows

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

## Aggregate Before Comparing Periods

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

## Distribution Views for a Time Series

A time series is still a distribution of values, not just a path over time.

### Boxplot

```python
ax = df.boxplot()
ax.set_title("Boxplot of Time Series Values")
```

Useful for:

- spotting spread
- comparing typical range
- finding possible outliers

### Histogram

```python
ax = df.plot(kind="hist", bins=100)
ax.set_title("Histogram of Time Series Values")
```

Useful for:

- checking skew
- seeing whether values cluster into ranges
- comparing raw scale across periods or series

### Density Plot

```python
ax = df.plot(kind="density", linewidth=2)
ax.set_title("Density Plot of Time Series Values")
```

Useful for:

- a smoother view of the value distribution
- comparing multiple series without histogram bin sensitivity

## Multiple Time Series on One Plot

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

## Area Plots

If the goal is composition or cumulative visual mass, area charts can work well.

```python
ax = df.plot.area(figsize=(12, 4), fontsize=14)
```

Best for:

- components of a whole
- relative contribution over time

Be careful: area plots can hide exact line shapes when too many series overlap.

## Move the Legend Out of the Way

Multi-series plots often become unreadable because the legend covers the data.

```python
ax = jobs_by_month.plot(figsize=(12, 5), colormap="Dark2")
ax.legend(bbox_to_anchor=(1.0, 0.5), loc="center left")
```

This is a small change, but it greatly improves readability when many lines are present.

## Facet Plots for Many Series

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

## Autocorrelation and Partial Autocorrelation

These are not ordinary business charts, but they are essential when the question is whether the series depends on its own past.

### ACF

```python
from statsmodels.graphics import tsaplots

fig = tsaplots.plot_acf(co2_levels["co2"], lags=40)
```

Use ACF when you want to inspect:

- repeated structure
- persistence
- possible seasonality

### PACF

```python
fig = tsaplots.plot_pacf(co2_levels["co2"], lags=40)
```

Use PACF when you want a cleaner view of direct lag relationships after accounting for earlier lags.

Mental model:

- `ACF` shows total lag correlation
- `PACF` shows more direct lag contribution

## Decompose Trend, Seasonality, and Residuals

When the line chart is too mixed together, decomposition separates the parts.

```python
import statsmodels.api as sm

decomposition = sm.tsa.seasonal_decompose(co2_levels["co2"])
fig = decomposition.plot()
```

You can also extract the components directly:

```python
decomp_seasonal = decomposition.seasonal
decomp_trend = decomposition.trend
decomp_resid = decomposition.resid
```

And plot them one by one:

```python
decomp_trend.plot(figsize=(14, 2))
decomp_seasonal.plot(figsize=(14, 2))
decomp_resid.plot(figsize=(14, 2))
```

This is useful when:

- the original chart mixes long-term direction and short-term repeating effects
- you want to compare trend separately from seasonal behavior

## Comparing Multiple Decomposed Series

For several time series, you can decompose each one and rebuild a DataFrame from a component such as trend.

```python
my_dict_trend = {}

for ts in jobs.columns:
    ts_decomposition = sm.tsa.seasonal_decompose(jobs[ts])
    my_dict_trend[ts] = ts_decomposition.trend

trend_df = pd.DataFrame.from_dict(my_dict_trend)
```

After that, compare the resulting component directly:

```python
trend_corr = trend_df.corr(method="spearman")
```

If you want a visual summary:

```python
import seaborn as sns

fig = sns.clustermap(trend_corr, annot=True, linewidth=0.4)
```

This is a nice pattern when the question is not "what does one series look like?" but "which series move similarly over time?"

## Reading Checklist

When looking at a time-series chart, ask:

- Is there a long-term trend?
- Is there seasonality or repeating structure?
- Are there sudden breaks, spikes, or level shifts?
- Would aggregation make the pattern easier to see?
- Does smoothing reveal a clearer signal?
- Should this be one combined chart or multiple subplots?

## Key Takeaways

- Convert time columns to `datetime64` and use a datetime index early.
- Slice, aggregate, or smooth before over-styling a noisy chart.
- Use annotations and spans to explain events and thresholds.
- Compare raw series, rolling summaries, and resampled aggregates for different views of the same process.
- For serious time-series reading, go beyond line charts into ACF, PACF, and decomposition.
