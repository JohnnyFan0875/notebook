# NumPy Package Documentation

NumPy 是 Python 科學計算的基礎層。只要你在做向量化運算、矩陣處理、抽樣模擬，或想理解 pandas / scikit-learn 背後怎麼吃資料，NumPy 幾乎都在場。

## Table of Contents

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

## Usage

- Each file contains examples with output and short explanations.
- Use this as a quick reference when working with arrays for data science, statistics, or linear algebra tasks.
- For related conversions (e.g., array -> DataFrame), see [Data Type Transformation](../data-type-transformation.md).

## 先掌握的三件事

1. `shape` 與 `axis` 的意義。
2. slicing 與 broadcasting 如何改變運算結果。
3. 何時該用向量化，而不是 Python `for` 迴圈。
4. 高維 array 裡每個 axis 代表什麼，不要只把它當成「更多括號」。
