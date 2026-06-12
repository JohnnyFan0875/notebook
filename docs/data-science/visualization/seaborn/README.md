# Seaborn Documentation

This folder contains structured notes and examples for **Seaborn**, a Python library for statistical data visualization built on top of Matplotlib.

## 📂 Table of Contents

### [Basics](basics.md)

- Load built-in datasets with `sns.load_dataset`
- Plot directly from DataFrames
- Difference between **FacetGrid** and **AxesSubplot**
- Styling and themes (`set_style`, `set_palette`, `set_context`)
- Titles, labels, legends
- Using `hue` to add a third variable

### [Relational Plots](relational.md)

- Scatter plots with `relplot(kind='scatter')`
- Line plots with `relplot(kind='line')`
- Encoding additional dimensions with `hue`, `size`, `style`, `alpha`
- Faceting by row/column
- Confidence intervals in line plots
- Multiple observations per x-value

### [Categorical Plots](categorical.md)

- Count plots
- Bar plots
- Box plots (`whis` parameter, outliers)
- Violin plots
- Boxen plots (large datasets)
- Point plots (`capsize`, `estimator`)
- Faceting with `col`/`row`
- Style and palette customization
- FAQ: Countplot vs Histplot

### [Distribution Plots](distribution.md)

- Histograms with `histplot`
- Grouped histograms with `hue`
- KDE plots (`kdeplot`)
- Cumulative distributions
- Displot (`displot(kind='hist'|'kde')`)
- Overlay histogram + KDE
- Difference between `histplot` and `kdeplot`
- Countplot vs Histplot

### [Regression Plots](regression.md)

- Linear regression with `regplot`
- Polynomial regression (`order=n`)
- Logistic regression (`logistic=True`)
- Residual plots (`residplot`)
- Quantile-Quantile (QQ) plots (Statsmodels)
- Scale-location plots (homoscedasticity check)
- Higher-level regression with `lmplot`

### [Matrix Plots](matrix.md)

- Correlation heatmaps (`heatmap`)
- Customizing heatmaps (formatting, linewidths, colorbars)
- Pairwise scatter plots (`pairplot`)
- Grouping in pairplots with `hue`
- Choosing diagonal plots (`diag_kind='kde'`)

## 🔍 Seaborn vs Matplotlib

| Aspect          | Seaborn                                                      | Matplotlib                                                         |
| --------------- | ------------------------------------------------------------ | ------------------------------------------------------------------ |
| **Focus**       | High-level, statistical visualization                        | Low-level, general-purpose plotting                                |
| **API**         | Simplified functions with sensible defaults (`sns.histplot`) | Explicit plotting with full control (`plt.hist`)                   |
| **Integration** | Works directly with Pandas DataFrames                        | Works with arrays/lists (DataFrames supported but less integrated) |
| **Themes**      | Built-in styles, palettes, contexts                          | Manual styling or `plt.style.use`                                  |
| **Best For**    | Quick, attractive, and statistical plots                     | Fine-grained, publication-quality customization                    |

## Key Takeaways

- Seaborn provides **high-level abstractions** for common statistical plots.
- Built on Matplotlib: anything you can do in Matplotlib can also be combined with Seaborn.
- Excellent integration with Pandas makes it ideal for **EDA (exploratory data analysis)**.
- Use Seaborn for **quick and attractive plots**, Matplotlib for **full customization**.
