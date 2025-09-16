# Matplotlib Documentation

This folder contains structured notes and examples for **Matplotlib**, a Python library for creating static, interactive, and animated visualizations.

---

## 📂 Table of Contents

### [Basics](basics.md)

- Create figures and axes with `plt.subplots()`
- Add labels, titles, and ticks
- Adjust figure size, axis limits, and scales
- Apply styles and themes (`plt.style.use`)
- Save and clear figures
- Handle non-English characters with `rcParams`

### [Line Plot](line-plot.md)

- Basic line plots
- Multiple lines with legends
- Subplots
- Error bars
- Reference lines (`axhline`, `axvline`)
- Dual axes with `twinx`
- Annotations

### [Scatter Plot](scatter-plot.md)

- Basic scatter plots
- Grouping by categories
- Customize marker size and color (`c`, `s`, `cmap`, `alpha`)
- Reference lines
- Subplots for comparison
- Scatter with trend line (`np.polyfit`)
- Annotations

### [Bar Plot & Histogram](bar-histogram.md)

- Basic bar plots
- Grouped and stacked bars
- Horizontal bars (`ax.barh`)
- Histograms (`ax.hist`)
- Multiple histograms with overlay
- Density overlays (histogram + KDE)

### [Box Plot](box-plot.md)

- Basic box plots
- Multiple box plots
- Grouped box plots by category
- Horizontal box plots
- Customized box plots (notched, colored)
- Overlay raw data points

### [Advanced](advanced.md)

- Dual y-axis plots with `twinx`
- Annotating with arrows
- Combining dual axes and annotations
- Missing data visualization with **Missingno**

---

## 🔍 Matplotlib vs Pandas `.plot()`

| Aspect        | Matplotlib                                           | Pandas `.plot()`                                 |
| ------------- | ---------------------------------------------------- | ------------------------------------------------ |
| **API**       | Low-level, flexible plotting library                 | High-level wrapper on Matplotlib                 |
| **Use Cases** | Full control of plots, customizations, multiple axes | Quick visualization directly from DataFrames     |
| **Examples**  | `plt.bar(x, y)`, `ax.plot(x, y)`                     | `df.plot(kind='bar')`, `df.plot(kind='scatter')` |
| **Best For**  | Publication-quality, complex figures                 | Exploratory data analysis (EDA)                  |

For Pandas visualization examples, see [Pandas Visualization](../pandas/visualization.md).

---

## Key Takeaways

- Start with **Basics** to set up plots.
- Use **Line, Scatter, Bar/Histogram, and Box Plot** for common visualization needs.
- Explore **Advanced** for dual axes, annotations, and specialized tasks.
- Pandas `.plot()` is useful for quick EDA but relies on Matplotlib internally for rendering.
