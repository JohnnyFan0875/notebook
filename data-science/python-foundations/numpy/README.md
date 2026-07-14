# NumPy Foundations

NumPy 是 Python 科學計算的基礎層。只要你在做向量化運算、矩陣處理、抽樣模擬，或想理解 pandas / scikit-learn 背後怎麼吃資料，NumPy 幾乎都在場。

## 建議閱讀順序

1. [Array Properties](array-properties.md): 先建立 `shape`、`ndim`、`dtype` 與 axis 的語感。
2. [Array Creation](array-creation.md) 與 [Indexing & Slicing](indexing-slicing.md): 學會怎麼建立與安全存取 array。
3. [Operations](operations.md) 與 [Reshape & Concatenate](reshape-concatenate.md): 把向量化、broadcasting、重塑與拼接串起來。
4. [Statistics](statistics.md) 與 [Random Sampling](random-sampling.md): 接上描述統計、模擬與抽樣工作流。
5. [Linear Algebra](linear-algebra.md): 當問題開始涉及矩陣運算、投影或解方程式時再往下讀。

## 主題地圖

### [Array Properties](array-properties.md)

- Inspecting array structure and metadata:

  - `ndim` – number of dimensions
  - `shape` – size along each axis
  - `size` – total number of elements
  - `dtype` – element type
  - `type` – confirms `numpy.ndarray`

### [Array Creation](array-creation.md)

- Creating arrays in different ways:

  - From lists
  - Ranges: `arange`, `linspace`, `logspace`
  - Initialization: `zeros`, `ones`, `eye`
  - Random arrays (see Random Sampling for details)
  - `unique` elements

### [Indexing & Slicing](indexing-slicing.md)

- Accessing and modifying array elements:

  - 1D slicing (`arr[start:end:step]`)
  - 2D indexing (`matrix[row, col]`)
  - Negative indices
  - Using `:` for entire rows/columns

### [Reshape & Concatenate](reshape-concatenate.md)

- Reshaping and combining arrays:

  - `reshape`
  - `transpose (T)`
  - explicit axis reordering with `transpose(..., axes=...)`
  - `concatenate`
  - `vstack`, `hstack`
  - `flip`, `split`, `stack`

### [Random Sampling](random-sampling.md)

- Random number generation and reproducibility:

  - `rand`, `randn`
  - `normal`
  - `randint`
  - `choice` (with or without replacement, probability weights)
  - `shuffle`
  - `seed`

### [Operations](operations.md)

- Element-wise operations:

  - Arithmetic (`+`, `-`, `*`, `/`)
  - Functional equivalents: `add`, `subtract`, `multiply`, `divide`, `negative`
  - Mixed types (booleans with numbers)

- Iteration:

  - `nditer` for efficient iteration

- Boolean logic:

  - Comparisons (`>`, `<`, `==`)
  - `any`, `all`
  - Logical operators: `logical_or`, `logical_and`
  - Boolean indexing in pandas DataFrames

- See [Statistics](statistics.md#transformations) for transformations (log, sqrt, Box-Cox)

### [Linear Algebra](linear-algebra.md)

- Matrix and vector algebra:

  - `dot`, `inner`
  - `cross`
  - `inv` (inverse)
  - `eig` (eigenvalues and eigenvectors)
  - `outer`
  - `remainder`
  - `solve` linear systems

### [Statistics](statistics.md)

- Descriptive and inferential statistics:

  - `mean`, `median`
  - Aggregations: `sum`, `min`, `max`, `std`
  - Quantiles & percentiles
  - Interquartile range (IQR)
  - Z-score outlier detection
  - Rounding: `round`, `floor`, `ceil`
  - Mean Absolute Deviation (MAD)
  - Transformations: `log`, `sqrt`, `boxcox`

## 這一章要解決什麼

- 什麼是 `shape`、`axis`、broadcasting，為什麼很多錯都出在這裡？
- 何時該保留 NumPy array，何時該轉成 pandas DataFrame？
- 哪些運算該向量化，哪些情境可以接受明確迴圈？
- 如果後面要接機器學習、深度學習或統計模擬，哪些 NumPy 觀念是共用底層？

## 使用方式

- Each file contains examples with output and short explanations.
- Use this section as both a learning path and a quick reference when working with arrays for data science, statistics, or linear algebra tasks.
- For related conversions (e.g., array -> DataFrame), see [Data Type Transformation](../data-type-transformation.md).

## 先掌握的三件事

1. `shape` 與 `axis` 的意義。
2. slicing 與 broadcasting 如何改變運算結果。
3. 何時該用向量化，而不是 Python `for` 迴圈。
4. 高維 array 裡每個 axis 代表什麼，不要只把它當成「更多括號」。
