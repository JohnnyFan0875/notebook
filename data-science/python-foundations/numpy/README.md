# NumPy Foundations

NumPy 是 Python 科學計算的基礎層。只要你在做向量化運算、矩陣處理、抽樣模擬，或想理解 pandas / scikit-learn 背後怎麼吃資料，NumPy 幾乎都在場。

## 建議閱讀順序

| 筆記 | 內容 |
| --- | --- |
| [Array Basics](array-basics.md) | `ndim` / `shape` / `size` / `dtype`；`arange`、`linspace`、`zeros`、`eye`；1D / 2D slicing、負索引 |
| [Vectorization and Reshape](vectorization-and-reshape.md) | element-wise 運算、broadcasting、`nditer`、boolean 運算；`reshape`、`transpose`、`concatenate` / `stack` / `split` |
| [Random and Statistics](random-and-statistics.md) | `normal`、`randint`、`choice`、`seed`；mean / median / quantile、IQR、z-score、MAD、log / sqrt / Box-Cox |
| [Linear Algebra](linear-algebra.md) | `dot`、`inner`、`cross`、`inv`、`eig`、`solve` |

## 這一章要解決什麼

- 什麼是 `shape`、`axis`、broadcasting，為什麼很多錯都出在這裡？
- 何時該保留 NumPy array，何時該轉成 pandas DataFrame？
- 哪些運算該向量化，哪些情境可以接受明確迴圈？
- 如果後面要接機器學習、深度學習或統計模擬，哪些 NumPy 觀念是共用底層？

## 使用方式

- Each file contains examples with output and short explanations.
- Use this section as both a learning path and a quick reference when working with arrays for data science, statistics, or linear algebra tasks.
- For related conversions (e.g., array -> DataFrame), see [Data Type Transformation](../importing-data.md#格式互轉-data-type-transformation).

## 先掌握的三件事

1. `shape` 與 `axis` 的意義。
2. slicing 與 broadcasting 如何改變運算結果。
3. 何時該用向量化，而不是 Python `for` 迴圈。
4. 高維 array 裡每個 axis 代表什麼，不要只把它當成「更多括號」。
