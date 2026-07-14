# NumPy Indexing and Slicing

This page covers array-style indexing in NumPy, where shape and axis position matter directly. If you need label-aware selection and dataframe-oriented access patterns, use [Pandas: Indexing and Slicing](../pandas/indexing-slicing.md).

This section covers indexing and slicing in NumPy arrays. 這是最常用、也最容易因 shape 搞混的地方。

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

### MATLAB-to-Python Indexing Mental Model

如果你有 MATLAB 背景，最容易出錯的不是語法，而是 indexing 規則：

- Python / NumPy 是 `0-based indexing`
- slicing 的右邊界不包含在結果內
- `:` 仍然保留「整段範圍」的感覺，但語意和 MATLAB 不完全一樣

```python
arr = np.array([16, 5, 9, 4, 2, 11, 7, 14])

arr[4:]
# [ 2 11  7 14]
```

這段如果用 MATLAB 心智模型來看，很容易誤以為 `arr[4:]` 是「從第 4 個元素開始」；但在 Python 裡，它其實是「從 index 4 開始」，也就是第 5 個元素。

Key point:

- MATLAB `v(5:end)` 常對應 Python `arr[4:]`
- Python `arr[a:b]` 讀成「從 a 開始，走到 b 之前」

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

如果你腦中還留著 MATLAB 的 `A(2:4, 1:2)`，Python / NumPy 對應會是：

```python
matrix[1:4, 0:2]
```

也就是 row / column 的位置概念還在，但索引起點從 1 改成 0，右邊界同樣不包含在切片內。

## Boolean Indexing

```python
arr[arr % 2 == 0]
# [0 2 4 6 8]
```

布林索引在資料清理與條件篩選時非常常用，但要注意條件陣列的 shape 必須對得上。

它不只可以拿來篩選，也可以直接做條件賦值：

```python
matrix = np.array([[16, 2], [3, 14]])
matrix[matrix > 12] = 10

print(matrix)
# [[10  2]
#  [ 3 10]]
```

這種寫法在從 MATLAB 過來時通常很快能上手，因為「符合條件的位置整批改值」的思路幾乎一樣。

## Shape Property

```python
matrix.shape
# (2, 3)
```

- Shape gives the dimensions (rows, columns).

## Common Pitfalls

- 忘記切片上限不包含結尾索引。
- 把 `matrix[0][2]` 和 `matrix[0, 2]` 混用而不理解差異。
- 布林條件 shape 不一致，導致 indexing error。

## Summary

- **1D slicing**: Similar to Python lists (`arr[start:end:step]`).
- **2D indexing**: Use `matrix[row, col]` to access elements.
- **Colon (`:`)**: Selects entire row/column.
- **Negative index**: Access from the end.
