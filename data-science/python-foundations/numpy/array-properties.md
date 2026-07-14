# NumPy Array Properties

在 NumPy 裡，理解 array 的「形狀」比記函式名稱更重要。很多運算錯誤不是因為公式錯，而是因為你沒有先確認資料到底是一維、二維，還是更高維。

## Example Array

```python
import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr)
# [[1 2 3]
#  [4 5 6]]
```

## Number of Dimensions

```python
arr.ndim
# 2
```

- `ndim` gives the number of dimensions (axes). Here, the array is 2D (rows and columns).

## Shape of Array

```python
arr.shape
# (2, 3)
```

- `shape` returns a tuple representing the size of each dimension.
  Here, 2 rows × 3 columns.

## Total Number of Elements

```python
arr.size
# 6
```

- `size` gives the total number of elements across all dimensions.

## Data Type of Elements

```python
arr.dtype
# dtype('int64')
```

- `dtype` shows the data type of array elements. Can be `int32`, `int64`, `float32`, etc.

### Why `dtype` Matters

- 它會影響記憶體用量。
- 它會影響數值精度。
- 有些演算法或套件預期特定型別，例如 `float32` 或 `float64`。

## Type of Object

```python
type(arr)
# <class 'numpy.ndarray'>
```

- Confirms that the object is a NumPy array (`ndarray`).

## Summary

- **`ndim`** → number of dimensions (axes).
- **`shape`** → size along each axis.
- **`size`** → total number of elements.
- **`dtype`** → element type.
- **`type`** → confirms it’s a NumPy array.

## Practical Habit

每次拿到新 array 時，先看：

```python
arr.shape, arr.ndim, arr.dtype
```

這通常比直接印全部內容更能幫你快速判斷下一步怎麼操作。
