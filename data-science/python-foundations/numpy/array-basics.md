# NumPy Array Basics: Properties, Creation and Indexing

## NumPy Array Properties

在 NumPy 裡，理解 array 的「形狀」比記函式名稱更重要。很多運算錯誤不是因為公式錯，而是因為你沒有先確認資料到底是一維、二維，還是更高維。

### Example Array

```python
import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr)
# [[1 2 3]
#  [4 5 6]]
```

### Number of Dimensions

```python
arr.ndim
# 2
```

- `ndim` gives the number of dimensions (axes). Here, the array is 2D (rows and columns).

### Shape of Array

```python
arr.shape
# (2, 3)
```

- `shape` returns a tuple representing the size of each dimension.
  Here, 2 rows × 3 columns.

### Total Number of Elements

```python
arr.size
# 6
```

- `size` gives the total number of elements across all dimensions.

### Data Type of Elements

```python
arr.dtype
# dtype('int64')
```

- `dtype` shows the data type of array elements. Can be `int32`, `int64`, `float32`, etc.

#### Why `dtype` Matters

- 它會影響記憶體用量。
- 它會影響數值精度。
- 有些演算法或套件預期特定型別，例如 `float32` 或 `float64`。

### Type of Object

```python
type(arr)
# <class 'numpy.ndarray'>
```

- Confirms that the object is a NumPy array (`ndarray`).

### Summary

- **`ndim`** → number of dimensions (axes).
- **`shape`** → size along each axis.
- **`size`** → total number of elements.
- **`dtype`** → element type.
- **`type`** → confirms it’s a NumPy array.

### Practical Habit

每次拿到新 array 時，先看：

```python
arr.shape, arr.ndim, arr.dtype
```

這通常比直接印全部內容更能幫你快速判斷下一步怎麼操作。

## NumPy Array Creation

### Example Array

```python
import numpy as np

# Create a simple 2x3 array
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr)
# Output:
# [[1 2 3]
#  [4 5 6]]
```

### Create from List

```python
arr_from_list = np.array([1, 2, 3])
print(arr_from_list)  # [1 2 3]
```

如果輸入是 list of lists，NumPy 會把它轉成 2D array：

```python
list_of_lists = [[2, 3], [9, 0], [1, 4]]
arr = np.array(list_of_lists)

print(arr)
# [[2 3]
#  [9 0]
#  [1 4]]

print(arr.shape)
# (3, 2)
```

這是從一般 Python 容器進入「矩陣式思考」的常見起點。

### Ranges

```python
# Using arange
np.arange(0, 10, 2)
# Output: [0 2 4 6 8]

# Using linspace
np.linspace(0, 1, 5)
# Output: [0.   0.25 0.5  0.75 1.  ]

# Using logspace
np.logspace(0.1, 1, 5)
# Output: [1.25892541 2.11348904 3.54813389 5.95662144 10.        ]
```

`np.arange(start, stop, step)` 的停止規則和 Python slice / `range()` 一樣，也是「包含起點、不包含終點」。

```python
np.arange(0, 2 * np.pi, 0.01)
```

這種寫法很常用在建立連續函數的 x 軸資料，例如畫 sine / cosine 曲線。

### Zeros, Ones, Identity

```python
np.zeros((2, 3))
# Output:
# [[0. 0. 0.]
#  [0. 0. 0.]]

np.ones((3, 3))
# Output:
# [[1. 1. 1.]
#  [1. 1. 1.]
#  [1. 1. 1.]]

np.ones((3,)) * 7
# Output: [7. 7. 7.]

np.eye(3)
# Output:
# [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]]
```

### Random Arrays

| Code Example                       | Reference                                                                                     |
| ---------------------------------- | --------------------------------------------------------------------------------------------- |
| `np.random.randint(0, 10, (2, 3))` | See [Random Integers](random-and-statistics.md#random-integers)                                     |
| `np.random.rand(3, 2)`             | See [Uniform Random Numbers](random-and-statistics.md#uniform-random-numbers)                       |
| `np.random.normal(3, 2)`           | See [Random Numbers from Distributions](random-and-statistics.md#random-numbers-from-distributions) |
| `np.random.choice([1, 2, 3], 5)`   | See [Random Choice](random-and-statistics.md#random-choice)                                         |

### Unique Elements from Array

```python
sample = np.array([1, 2, 2, 3, 4, 4, 5, 6])
unique, counts = np.unique(sample, return_counts=True)
print(unique)   # [1 2 3 4 5 6]
print(counts)   # [1 2 1 2 1 1]

# Convert to dictionary
count_dict = dict(zip(unique, counts))
print(count_dict)  # {1: 1, 2: 2, 3: 1, 4: 2, 5: 1, 6: 1}
```

### Summary

- Arrays can be created from lists, ranges, or random distributions.
- Utility functions like `zeros`, `ones`, and `eye` are useful for initializing.
- `unique` helps in extracting distinct elements with their frequencies.

## NumPy Indexing and Slicing

This page covers array-style indexing in NumPy, where shape and axis position matter directly. If you need label-aware selection and dataframe-oriented access patterns, use [Pandas: Indexing and Slicing](../pandas/selection.md).

This section covers indexing and slicing in NumPy arrays. 這是最常用、也最容易因 shape 搞混的地方。

### Example Arrays

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

### Basic Slicing

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

#### MATLAB-to-Python Indexing Mental Model

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

### Indexing 2D Arrays (Matrix)

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

### Boolean Indexing

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

### Shape Property

```python
matrix.shape
# (2, 3)
```

- Shape gives the dimensions (rows, columns).

### Common Pitfalls

- 忘記切片上限不包含結尾索引。
- 把 `matrix[0][2]` 和 `matrix[0, 2]` 混用而不理解差異。
- 布林條件 shape 不一致，導致 indexing error。

### Summary

- **1D slicing**: Similar to Python lists (`arr[start:end:step]`).
- **2D indexing**: Use `matrix[row, col]` to access elements.
- **Colon (`:`)**: Selects entire row/column.
- **Negative index**: Access from the end.
