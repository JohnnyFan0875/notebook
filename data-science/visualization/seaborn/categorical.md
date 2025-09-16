# Seaborn: Categorical Plots

Categorical plots (`catplot`) are used to visualize the distribution of a categorical variable or the relationship between a categorical and a numerical variable. They provide multiple plot types such as **count, bar, box, violin, boxen, and point plots**.

## Import Packages and Example Dataset

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Example dataset: Iris
iris = sns.load_dataset("iris")
```

## Count Plot

```python
sns.catplot(x="species", data=iris, kind="count")
plt.show()
```

- Shows frequency of each category.
- Equivalent to `sns.countplot()`.

```python
sns.catplot(y="species", data=iris, kind="count", order=["setosa","versicolor","virginica"])
plt.show()
```

- Switch `x` to `y` for horizontal orientation.
- `order`: specify custom category order.

## Bar Plot

```python
sns.catplot(x="species", y="sepal_length", data=iris, kind="bar", ci="sd")
plt.show()
```

- Displays mean of a numerical variable per category.
- Vertical lines show confidence intervals (default = 95%).
- `ci="sd"`: show standard deviation instead.

## Box Plot

```python
sns.catplot(x="species", y="sepal_length", data=iris, kind="box")
plt.show()
```

- Summarizes distribution with median, quartiles, whiskers, and outliers.
- `whis`: control whisker length (e.g., `whis=[5,95]` → show 5th–95th percentiles).
- `whis`: default = 1.5. Extend to the most extreme data point within 1.5 × IQR of the box. Any points beyond this range are considered `outliers` and plotted individually.
- `sym=''`: hide outliers.

## Violin Plot

```python
sns.catplot(x="species", y="petal_length", data=iris, kind="violin")
plt.show()
```

- Combines box plot with a kernel density estimate.
- Useful for showing distribution shape.

## Boxen Plot

```python
sns.catplot(x="species", y="petal_width", data=iris, kind="boxen")
plt.show()
```

- Variation of box plot designed for larger datasets.
- Provides more granularity in the tails.

## Point Plot

```python
sns.catplot(x="species", y="sepal_length", data=iris,
            kind="point", capsize=0.2)
plt.show()
```

- Points represent mean values; vertical lines show confidence intervals.
- Line plot has **quantitative** variable (usually time) on x-axis. Point plot has **categorical** variable on x-axis.
- `capsize`: adds caps to CI bars.
- `join=False`: remove connecting lines.
- `estimator`: change summary statistic (e.g., `estimator=np.median`).

## Faceting with Catplot

```python
sns.catplot(x="species", y="sepal_length",
            data=iris, kind="bar",
            col="species")
plt.show()
```

- Combine `catplot` with `col`/`row` to create small multiples.
- Each facet shows a subset of the data.

## Customization

```python
sns.set_style("whitegrid")
sns.set_palette("pastel")

sns.catplot(x="species", y="petal_width", data=iris,
            kind="violin", hue="species")
plt.show()
```

- Style options: `white`, `dark`, `whitegrid`, `darkgrid`, `ticks`.
- Palette options: predefined (`"pastel"`, `"RdBu"`) or custom lists.
- Rotate labels with `plt.xticks(rotation=45)`.

## FAQ: Countplot vs Histplot

- **Countplot**: for **categorical variables** (counts of categories).
- **Histplot**: for **continuous variables** (distribution into bins).

## Key Takeaways

- Use `catplot` with `kind` argument for categorical visualizations.
- `count`, `bar`, `box`, `violin`, `boxen`, and `point` plots cover most needs.
- Customize with `hue`, `order`, `whis`, `capsize`, and style settings.
- Faceting with `col`/`row` makes comparisons across subgroups easy.
