# Matplotlib

Matplotlib 提供最細緻的圖表控制能力，適合需要完整掌握 figure、axes、標註、刻度與輸出格式的情境。若你想知道 Seaborn 背後實際發生什麼，理解 Matplotlib 幾乎是必經之路。

## 建議閱讀順序

1. [Basics](basics.md): 先把 figure、axes、labels、style 與輸出流程建立起來。
2. [Line Plot](line-plot.md) 與 [Scatter Plot](scatter-plot.md): 這兩類圖最常出現在分析與模型診斷。
3. [Bar Plot & Histogram](bar-histogram.md) 與 [Box Plot](box-plot.md): 補上分布與群組比較的常用圖。
4. [Advanced](advanced.md): 需要註解、雙軸、客製版面或比較複雜的輸出時再讀。

## 主題地圖

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

## Matplotlib vs Pandas `.plot()`

| Aspect        | Matplotlib                                           | Pandas `.plot()`                                 |
| ------------- | ---------------------------------------------------- | ------------------------------------------------ |
| **API**       | Low-level, flexible plotting library                 | High-level wrapper on Matplotlib                 |
| **Use Cases** | Full control of plots, customizations, multiple axes | Quick visualization directly from DataFrames     |
| **Examples**  | `plt.bar(x, y)`, `ax.plot(x, y)`                     | `df.plot(kind='bar')`, `df.plot(kind='scatter')` |
| **Best For**  | Publication-quality, complex figures                 | Exploratory data analysis (EDA)                  |

For Pandas visualization examples, see [Pandas Visualization](../../../python-foundations/pandas/visualization.md).

## 這一章要解決什麼

- 當高階 API 不夠用時，我要怎麼直接控制 figure、axes、legend 與 annotation？
- 什麼時候應該回到 Matplotlib，而不是繼續疊加 pandas 或 Seaborn 的預設？
- 如果一張圖要拿去簡報、論文或正式報告，哪些底層控制最重要？

## Practical Reminder

- 先把軸、標籤與圖例設對，再追求視覺風格。
- 如果圖已經需要很多手工調整，通常 Matplotlib 會比高階 API 更可靠。
