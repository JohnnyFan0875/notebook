# NumPy Vectorization, Broadcasting and Reshape

## NumPy Operations

### Example Arrays

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

C = np.array([1, 2, 3])
D = np.array([4, 5, 6])

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
```

### Element-wise Arithmetic

```python
a + b    # [5 7 9]
a - b    # [-3 -3 -3]
a * b    # [4 10 18]
a / b    # [0.25 0.4 0.5]
```

```python
np_li_m = np.array([1, 2, 3]) * 2  # [2 4 6] → Multiplying by a scalar scales every element
```

#### Why NumPy Feels Different from Python Lists

很多人第一次學 NumPy，真正的轉折點不是語法，而是發現 array 的算術語意和 list 不一樣。

```python
height = [1.73, 1.68, 1.71]
weight = [65.4, 59.2, 63.6]

# weight / height  # TypeError
```

普通 Python `list` 不支援這種 element-wise 數值運算；但 NumPy array 可以：

```python
np_height = np.array(height)
np_weight = np.array(weight)

bmi = np_weight / np_height ** 2
```

Key point: Python `list` 是通用容器，NumPy `ndarray` 是數值陣列。當你需要整批數值一起算，array 才是自然抽象。

### Interview Fast Comparison: `list` vs `ndarray`

如果面試官直接問 list 和 NumPy array 的差別，最值得先講的是：

- `list` 是 general-purpose container
- `ndarray` 是 numerical array

然後再補三個高頻差異：

- array 通常要求較一致、較具體的 `dtype`
- array 支援 element-wise numeric operations
- array 在大量數值運算時通常更有效率

也可以補一句容易拿分的對照：

- 如果你要裝 heterogeneous Python objects，`list` 比較自然
- 如果你要做向量化計算，`ndarray` 比較自然

### Negative, Add, Subtract, Multiply, Divide

```python
np.negative(A)
# [[-1 -2]
#  [-3 -4]]

np.add(A, B)
# [[ 6  8]
#  [10 12]]

np.subtract(A, B)
# [[-4 -4]
#  [-4 -4]]

np.multiply(C, D)
# [ 4 10 18]

np.divide(C, D)
# [0.25 0.4  0.5 ]
```

- These functions are the functional form equivalents of standard operators (`+`, `-`, `*`, `/`).

### Mixed Types

```python
np.array([True, 1, 2]) + np.array([3, 4, False])
# [4 5 2]
```

- Boolean values are treated as integers (`True=1`, `False=0`).

### Iteration over Arrays

```python
arr = np.arange(6).reshape(2, 3)
for x in np.nditer(arr):
    print(x)
# 0 1 2 3 4 5
```

- `np.nditer` provides an efficient way to iterate over every element of an array.

```python
b = np.array([[[1,2],[3,4]], [[5,6],[7,8]]])

for i in b:
    for j in i:
        for k in j:
            print(k, end=' ')
# 1 2 3 4 5 6 7 8

for i in np.nditer(b):
    print(i, end=' ')
# 1 2 3 4 5 6 7 8
```

- Multi-dimensional arrays can be iterated manually with nested loops or flattened using `nditer`.

#### Another Interview Angle: Indexing Style

list 和 array 還有一個很常被追問的差異是多維索引方式：

- nested list 常寫成 `x[i][j]`
- NumPy array 常直接寫成 `x[i, j]`

這不只是語法差異，也反映 NumPy 把多維資料當成單一陣列物件來處理，而不是「list 裡面再放 list」。

### Boolean Operations

```python
arr = np.array([1, 2, 3, 4, 5])

arr > 2
# [False False  True  True  True]

arr[arr > 2]
# [3 4 5]

np.any(arr > 4)  # True
np.all(arr > 0)  # True

(arr > 2).sum()
# 3 → number of elements greater than 2
```

- Boolean indexing is powerful for filtering arrays.

### Boolean Operators with Multiple Conditions

```python
my_house = np.array([18.0, 20.0, 10.75, 9.50])
your_house = np.array([14.0, 24.0, 14.25, 9.0])

# my_house greater than 18.5 or smaller than 10
my_house[np.logical_or(my_house > 18.5, my_house < 10)]
# [20.   9.5]

# Both my_house and your_house smaller than 11
np.logical_and(my_house < 11, your_house < 11)
# [False False False  True]
```

- `np.logical_or` and `np.logical_and` combine boolean conditions element-wise.

### Summary

- **Element-wise arithmetic**: add, subtract, multiply, divide.
- **Negative/Add/Subtract/Multiply/Divide**: functional equivalents of operators.
- **Mixed types**: booleans treated as integers.
- **Iteration**: loop through array elements efficiently with `nditer`.
- **Boolean operations**: filtering and condition checking.
- **Logical operators**: `logical_or`, `logical_and` for combining conditions.
- 面試若問 `list` vs `ndarray`，先講 `dtype`、vectorization、efficiency，再講 indexing style。

## NumPy Reshape and Concatenate

`reshape` 與 `concatenate` 是把陣列重新整理成模型或函式需要格式的基本功。遇到維度錯誤時，先回頭看 shape，通常就能找到原因。

### Example Arrays

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

### Reshape

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

### Transpose

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

### Concatenate

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

### Stack Vertically and Horizontally

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

### Flip Along an Axis

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

### High-Dimensional Axis Thinking

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

### Split and Stack

`split` 和 `stack` 很適合處理多通道資料。

#### Split

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

#### Equal Division Rule

```python
np.split(rgb, 5, axis=2)
# ValueError
```

- `split` 必須能在指定 axis 上平均切開，否則會報錯。

#### Stack

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

### Reshape Before Concatenate

```python
Z = [7, 8]
np.concatenate((arr, np.array(Z).reshape(1, 2)), axis=0)
# Error: dimension mismatch because arr is 2x3 and reshaped Z is 1x2
```

- Shapes must align on the concatenation axis. Reshaping is often needed to make them compatible.

### Summary

- **`reshape`**: change the structure while preserving data size.
- **`T` (transpose)**: flip rows and columns.
- **`transpose(..., axes=...)`**: reorder axes in higher-dimensional arrays.
- **`concatenate`**: join arrays along rows or columns.
- **`vstack` / `hstack`**: shortcuts for stacking vertically or horizontally.
- **`flip`**: reverse an array along one or more axes.
- **`split` / `stack`**: separate or rebuild arrays across a chosen axis.
- Be careful with dimension alignment.

### Practical Habit

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
