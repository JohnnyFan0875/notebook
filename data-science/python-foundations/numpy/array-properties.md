# NumPy Array Properties

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
