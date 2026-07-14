# Seaborn

Seaborn 建立在 Matplotlib 之上，擅長快速畫出統計型圖表，特別適合 exploratory data analysis、群組比較與直接以 DataFrame 為中心的工作流。

## 建議閱讀順序

1. [Basics](basics.md): 先掌握 theme、palette、`hue` 與 DataFrame-friendly 的畫圖方式。
2. [Distribution](distribution.md)、[Categorical](categorical.md)、[Relational](relational.md): 這三塊組成大部分 EDA 的核心圖表。
3. [Regression](regression.md) 與 [Matrix](matrix.md): 當你要處理相關性、回歸線、殘差或多變量檢視時再往下讀。

## 主題地圖

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

## Seaborn vs Matplotlib

| Aspect          | Seaborn                                                      | Matplotlib                                                         |
| --------------- | ------------------------------------------------------------ | ------------------------------------------------------------------ |
| **Focus**       | High-level, statistical visualization                        | Low-level, general-purpose plotting                                |
| **API**         | Simplified functions with sensible defaults (`sns.histplot`) | Explicit plotting with full control (`plt.hist`)                   |
| **Integration** | Works directly with Pandas DataFrames                        | Works with arrays/lists (DataFrames supported but less integrated) |
| **Themes**      | Built-in styles, palettes, contexts                          | Manual styling or `plt.style.use`                                  |
| **Best For**    | Quick, attractive, and statistical plots                     | Fine-grained, publication-quality customization                    |

## 這一章要解決什麼

- 如果我想快速從 DataFrame 畫出統計型圖表，應該先用哪一類 Seaborn API？
- `countplot`、`histplot`、`boxplot`、`violinplot`、`pairplot` 之間到底怎麼選？
- 什麼時候應該讓 Seaborn 負責語意映射，什麼時候該回到 Matplotlib 做細節控制？

## Practical Reminder

- Seaborn 讓你更快畫圖，但不會替你決定圖是否真的適合問題。
- 當版面或細節控制需求變高時，記得回到 Matplotlib 軸物件進一步調整。
