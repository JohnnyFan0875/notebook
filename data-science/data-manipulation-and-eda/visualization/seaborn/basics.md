# Seaborn: Basics

This page introduces Seaborn as a higher-level statistical plotting interface. For direct control over figure objects, axes, and rendering details, see [Matplotlib: Basics](../matplotlib/basics.md).

Seaborn provides a high-level interface for drawing attractive and informative statistical graphics. It integrates tightly with Pandas DataFrames, making it easy to visualize datasets quickly.

## Import Packages and Example Dataset

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Example dataset: Iris
iris = sns.load_dataset("iris")
```

## Plotting with DataFrames

```python
sns.countplot(x="species", data=iris)
plt.title("Countplot of Iris Species")
plt.show()
```

- Seaborn works seamlessly with Pandas DataFrames.
- Specify `x`, `y`, and `data` directly.

## Loading Built-in Datasets

```python
# Load dataset from Seaborn repository
tips = sns.load_dataset("tips")
print(tips.head())
```

- Many built-in datasets are available: `iris`, `tips`, `flights`, `penguins`, etc.
- Dataset source: [Seaborn Data Repository](https://github.com/mwaskom/seaborn-data).

## FacetGrid vs AxesSubplot

| Object Type     | Example Functions              | Characteristics                     |
| --------------- | ------------------------------ | ----------------------------------- |
| **FacetGrid**   | `relplot()`, `catplot()`       | Creates multiple subplots in a grid |
| **AxesSubplot** | `scatterplot()`, `countplot()` | Creates a single plot               |

Example with `FacetGrid`:

```python
g = sns.catplot(x="species", data=iris, kind="count", col="species")
g.fig.suptitle("FacetGrid Example", y=1.05)
plt.show()
```

## Styling and Themes (Global)

```python
sns.set_style("whitegrid")   # Options: "white", "dark", "whitegrid", "darkgrid", "ticks"
sns.set_palette("RdBu")      # Color palettes: "RdBu", "PRGn", "Greys", or custom list
sns.set_context("talk")      # Context: "paper", "notebook", "talk", "poster"
sns.set(font_scale=1.2)      # Control font scale
```

- Styling functions are **global** and apply to both **FacetGrid** and **AxesSubplot** plots.
- Use `set_style` to change background and grid.
- Use `set_palette` to change colors.
- Use `set_context` to adapt plots for presentations or papers.

## Titles and Labels

### FacetGrid Example

```python
g = sns.catplot(x="species", data=iris, kind="count")

# Add figure-level title
g.fig.suptitle("Iris Species Count", y=1.03)

# Set axis labels and rotation
g.set(xlabel="Flower Species", ylabel="Count")
g.set_xticklabels(rotation=45)
plt.show()
```

### AxesSubplot Example

```python
ax = sns.scatterplot(x="sepal_length", y="sepal_width", data=iris)

ax.set_title("Scatter Plot Example")
ax.set_xlabel("Sepal Length")
ax.set_ylabel("Sepal Width")
plt.show()
```

- **FacetGrid**: use `.fig.suptitle()` and `.set()` methods.
- **AxesSubplot**: use Matplotlib’s `ax.set_title()`, `ax.set_xlabel()`, `ax.set_ylabel()`.
- Both support titles and labels; the difference is in the API.

## Legends

```python
g = sns.scatterplot(x="sepal_length", y="petal_length", data=iris, hue="species")
plt.legend(title="Species")
plt.show()
```

- Legends are automatically created when using `hue`.
- Customize with `plt.legend(labels=[...])` or remove with `g._legend.remove()`.

## Hue: Adding a Third Variable

```python
tips = sns.load_dataset("tips")

hue_colors = {"Yes": "black", "No": "red"}

sns.scatterplot(x="total_bill", y="tip",
                data=tips, hue="smoker",
                hue_order=["No", "Yes"],
                palette=hue_colors)
plt.title("Tips by Smoking Status")
plt.show()
```

- `hue`: adds a categorical or numeric grouping variable.
- `hue_order`: specify category order.
- `palette`: set custom colors.

## Key Takeaways

- Seaborn integrates with DataFrames, simplifying plot creation.
- Use built-in datasets (`sns.load_dataset`) for practice.
- **FacetGrid** supports multiple subplots; **AxesSubplot** supports single plots.
- Styling functions (`set_style`, `set_palette`, `set_context`) are global.
- Titles and labels can be added in both FacetGrid and AxesSubpl
