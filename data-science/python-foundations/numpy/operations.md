# NumPy Operations

## Example Arrays

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

C = np.array([1, 2, 3])
D = np.array([4, 5, 6])

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
```

## Element-wise Arithmetic

```python
a + b    # [5 7 9]
a - b    # [-3 -3 -3]
a * b    # [4 10 18]
a / b    # [0.25 0.4 0.5]
```

```python
np_li_m = np.array([1, 2, 3]) * 2  # [2 4 6] → Multiplying by a scalar scales every element
```

### Why NumPy Feels Different from Python Lists

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

## Interview Fast Comparison: `list` vs `ndarray`

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

## Negative, Add, Subtract, Multiply, Divide

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

## Mixed Types

```python
np.array([True, 1, 2]) + np.array([3, 4, False])
# [4 5 2]
```

- Boolean values are treated as integers (`True=1`, `False=0`).

## Iteration over Arrays

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

### Another Interview Angle: Indexing Style

list 和 array 還有一個很常被追問的差異是多維索引方式：

- nested list 常寫成 `x[i][j]`
- NumPy array 常直接寫成 `x[i, j]`

這不只是語法差異，也反映 NumPy 把多維資料當成單一陣列物件來處理，而不是「list 裡面再放 list」。

## Boolean Operations

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

## Boolean Operators with Multiple Conditions

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

## Boolean Indexing with DataFrames

```python
import pandas as pd
cars = pd.DataFrame({
    'cars_per_cap': [809, 731],
    'country': ['United States', 'Australia'],
    'drives_right': [True, False]
})

sel = cars[cars['drives_right']]
print(sel)
#    cars_per_cap      country  drives_right
# US          809  United States          True
```

- Boolean arrays can directly filter rows in pandas DataFrames.

# Transformations

For transformations (log, sqrt, Box-Cox), see [statistics.md](statistics.md#transformations)

## Summary

- **Element-wise arithmetic**: add, subtract, multiply, divide.
- **Negative/Add/Subtract/Multiply/Divide**: functional equivalents of operators.
- **Mixed types**: booleans treated as integers.
- **Iteration**: loop through array elements efficiently with `nditer`.
- **Boolean operations**: filtering and condition checking.
- **Logical operators**: `logical_or`, `logical_and` for combining conditions.
- **Boolean indexing in pandas**: integrate seamlessly with NumPy logic.
- 面試若問 `list` vs `ndarray`，先講 `dtype`、vectorization、efficiency，再講 indexing style。
