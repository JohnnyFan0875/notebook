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
