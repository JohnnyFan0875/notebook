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

```python
img = np.zeros((100, 200, 3))
np.transpose(img, axes=(1, 0, 2)).shape
# (200, 100, 3)
```

- On higher-dimensional arrays, `transpose` can reorder axes explicitly.
- This is especially common for image or tensor-like data where height, width, and channels have different roles.

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

## Flip Along an Axis

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])

np.flip(matrix, axis=0)
# [[4 5 6]
#  [1 2 3]]

np.flip(matrix, axis=1)
# [[3 2 1]
#  [6 5 4]]
```

- `axis=0` flips rows.
- `axis=1` flips columns.
- For higher-dimensional arrays, you can also flip multiple axes at once.

```python
rgb = np.zeros((3, 3, 3), dtype=np.int32)
np.flip(rgb, axis=(0, 1)).shape
# (3, 3, 3)
```

這類操作在影像資料很常見，因為不同 axis 代表的通常不是同一種東西。

## High-Dimensional Axis Thinking

當 array 超過 2D 時，先不要急著操作，先問：

- `axis=0` 是什麼
- `axis=1` 是什麼
- `axis=2` 是什麼

例如 RGB 圖像常見 shape 是：

```python
rgb.shape
# (height, width, channels)
```

在這種情況下：

- `axis=0`: row / height
- `axis=1`: column / width
- `axis=2`: color channel

理解 axis 的語意，比死記函式更重要。

## Split and Stack

`split` 和 `stack` 很適合處理多通道資料。

### Split

```python
rgb = np.array([
    [[255, 0, 0], [255, 255, 0]],
    [[0, 255, 0], [0, 0, 255]],
])

red, green, blue = np.split(rgb, 3, axis=2)
red.shape
# (2, 2, 1)
```

- `np.split(..., axis=2)` 這裡是在 channel 維度切開。
- 切完後保留 trailing dimension，所以 shape 會是 `(h, w, 1)`，不是 `(h, w)`。

如果你真的要 2D channel，可以再 reshape 或 squeeze：

```python
red_2d = red.reshape((2, 2))
red_2d.shape
# (2, 2)
```

### Equal Division Rule

```python
np.split(rgb, 5, axis=2)
# ValueError
```

- `split` 必須能在指定 axis 上平均切開，否則會報錯。

### Stack

```python
red_2d = np.array([[255, 255], [0, 0]])
green_2d = np.array([[0, 255], [255, 0]])
blue_2d = np.array([[0, 0], [0, 255]])

stacked_rgb = np.stack([red_2d, green_2d, blue_2d], axis=2)
stacked_rgb.shape
# (2, 2, 3)
```

- `stack` 是把多個同 shape arrays 沿新 axis 疊起來。
- 這在重建多 channel image 或組 tensor 時很常見。

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
- **`transpose(..., axes=...)`**: reorder axes in higher-dimensional arrays.
- **`concatenate`**: join arrays along rows or columns.
- **`vstack` / `hstack`**: shortcuts for stacking vertically or horizontally.
- **`flip`**: reverse an array along one or more axes.
- **`split` / `stack`**: separate or rebuild arrays across a chosen axis.
- Be careful with dimension alignment.

## Practical Habit

在串接前先檢查：

```python
print(a.shape)
print(b.shape)
```

很多 `ValueError` 都只是因為你以為兩個陣列對得上，但實際上 axis 長度不同。

如果是 3D 以上資料，再多檢查一次：

```python
print(arr.shape)
print("axis meanings:", "0=?", "1=?", "2=?")
```

這個習慣對影像、embedding、sequence batch 或任何 tensor-like 資料都很有幫助。
