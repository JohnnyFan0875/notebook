# Seaborn: Relational Plots

Relational plots (`relplot`) are designed to visualize relationships between two or more variables. They can display data as **scatter plots** or **line plots**, and can be extended with additional dimensions (hue, size, style, col, row).

## Import Packages and Example Dataset

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Example dataset: Iris
iris = sns.load_dataset("iris")
```

## Basic Scatter Plot

```python
sns.relplot(x="sepal_length", y="sepal_width", data=iris, kind="scatter")
plt.show()
```

- Default `kind` is `scatter`.
- Use for simple two-variable relationships.

## Scatter Plot with Hue (Subgrouping)

```python
sns.relplot(x="sepal_length", y="sepal_width",
            data=iris, kind="scatter",
            hue="species")
plt.show()
```

- `hue`: adds a third variable via color.
- Helps show grouping (e.g., by species).

## Advanced Customization (Hue, Size, Style, Alpha)

```python
sns.relplot(x="sepal_length", y="petal_length",
            data=iris, kind="scatter",
            hue="species",                      # color by species
            size="petal_width",                 # scale marker size
            style="species",                    # marker style by species
            alpha=0.7)                          # transparency
plt.show()
```

- `size`: adjust point size based on a numeric variable.
- `style`: change marker type based on categories.
- `alpha`: control transparency.

## Faceting with Columns and Rows

```python
sns.relplot(x="sepal_length", y="sepal_width",
            data=iris, kind="scatter",
            col="species",                     # separate plots by species
            col_wrap=2)                        # wrap into 2 columns
plt.show()
```

- `col`/`row`: create grids of subplots based on categorical variables.
- `col_wrap`: wrap columns into multiple rows.

## Basic Line Plot

```python
flights = sns.load_dataset("flights")

sns.relplot(x="year", y="passengers",
            data=flights, kind="line")
plt.show()
```

- `kind='line'`: plot trends instead of scatter points.
- Often used for time series.

## Line Plot with Multiple Categories

```python
sns.relplot(x="year", y="passengers",
            data=flights, kind="line",
            hue="month",          # color by month
            style="month",        # different line styles
            markers=True,          # show points on lines
            dashes=False)          # disable dashed lines
plt.show()
```

- `markers=True`: show individual points.
- `dashes=False`: force all lines to be solid.

## Confidence Intervals in Line Plots

```python
sns.relplot(x="year", y="passengers",
            data=flights, kind="line",
            ci="sd")                   # shaded band shows ±1 standard deviation
plt.show()
```

- Default: 95% CI shaded region.
- `ci=None`: remove confidence intervals.

## Multiple Observations per X Value

```python
sns.relplot(x="sepal_length", y="sepal_width",
            data=iris, kind="line")
plt.show()
```

- Aggregates multiple y-values per x using mean.
- `ci`: controls the uncertainty band.

## Key Takeaways

- `relplot`: unified interface for **scatter** and **line** plots.
- Use **hue, size, style, alpha** for encoding more dimensions.
- Use **col/row faceting** to create subplots by categories.
- Line plots can display trends, multiple categories, and confidence intervals.
- Great for **exploring relationships** in multivariate data (e.g., Iris, Flights).
