# NumPy Reshape and Concatenate

`reshape` 與 `concatenate` 是把陣列重新整理成模型或函式需要格式的基本功。遇到維度錯誤時，先回頭看 shape，通常就能找到原因。

## Example Arrays

```python
import numpy as np

# Example 1D arrays
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Example 2D array
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr)
# [[1 2 3]
#  [4 5 6]]
```

## Reshape

```python
arr.reshape(-1)
# [1 2 3 4 5 6]
```

- Flattens the matrix into a 1D array.

```python
arr.reshape(3, 2)
# [[1 2]
#  [3 4]
#  [5 6]]
```

- Changes shape into 3 rows and 2 columns. The total number of elements must remain the same.

```python
arr.reshape(2, -1)
# [[1 2 3]
#  [4 5 6]]
```

- `-1` lets NumPy infer one dimension automatically.

## Transpose

```python
arr.T
# [[1 4]
#  [2 5]
#  [3 6]]
```

- Swaps rows and columns.

## Concatenate

```python
np.concatenate([a, b])
# [1 2 3 4 5 6]
```

- Joins 1D arrays end-to-end.

```python
np.concatenate((arr, arr), axis=0)
# [[1 2 3]
#  [4 5 6]
#  [1 2 3]
#  [4 5 6]]
```

- Concatenates along rows (axis=0).

```python
np.concatenate((arr, arr), axis=1)
# [[1 2 3 1 2 3]
#  [4 5 6 4 5 6]]
```

- Concatenates along columns (axis=1).

## Stack Vertically and Horizontally

```python
np.vstack([a, b])
# [[1 2 3]
#  [4 5 6]]
```

- Stacks 1D arrays as rows.

```python
np.hstack([a, b])
# [1 2 3 4 5 6]
```

- Stacks 1D arrays horizontally (similar to concatenate for 1D).

## Reshape Before Concatenate

```python
Z = [7, 8]
np.concatenate((arr, np.array(Z).reshape(1, 2)), axis=0)
# Error: dimension mismatch because arr is 2x3 and reshaped Z is 1x2
```

- Shapes must align on the concatenation axis. Reshaping is often needed to make them compatible.

## Summary

- **`reshape`**: change the structure while preserving data size.
- **`T` (transpose)**: flip rows and columns.
- **`concatenate`**: join arrays along rows or columns.
- **`vstack` / `hstack`**: shortcuts for stacking vertically or horizontally.
- Be careful with dimension alignment.

## Practical Habit

在串接前先檢查：

```python
print(a.shape)
print(b.shape)
```

很多 `ValueError` 都只是因為你以為兩個陣列對得上，但實際上 axis 長度不同。
