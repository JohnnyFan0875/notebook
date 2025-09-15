# NumPy Indexing and Slicing

This section covers indexing and slicing in NumPy arrays.

## Example Arrays

```python
import numpy as np

# Example 1D array
arr = np.arange(10)
print(arr)
# [0 1 2 3 4 5 6 7 8 9]

# Example 2D array (matrix)
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(matrix)
# [[1 2 3]
#  [4 5 6]]
```

## Basic Slicing

```python
arr[2:7]
# [2 3 4 5 6]

arr[:5]
# [0 1 2 3 4]

arr[-1]
# 9 (last element)

arr[::2]
# [0 2 4 6 8] (every second element)
```

## Indexing 2D Arrays (Matrix)

```python
matrix[0, 1]
# 2 (row 0, column 1)

matrix[:, 1]
# [2 5] (all rows, column 1)

matrix[1, :]
# [4 5 6] (row 1, all columns)

matrix[1, 1:3]
# [5 6] (row 1, columns 1 to 2)

matrix[0][2]
# 3 (row 0, column 2)

matrix[0, 2]
# 3 (same as above, preferred)
```

- Use `matrix[row, col]` format for clarity and performance.

## Shape Property

```python
matrix.shape
# (2, 3)
```

- Shape gives the dimensions (rows, columns).

## Summary

- **1D slicing**: Similar to Python lists (`arr[start:end:step]`).
- **2D indexing**: Use `matrix[row, col]` to access elements.
- **Colon (`:`)**: Selects entire row/column.
- **Negative index**: Access from the end.
