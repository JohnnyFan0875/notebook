# NumPy Array Creation

## Example Array

```python
import numpy as np

# Create a simple 2x3 array
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr)
# Output:
# [[1 2 3]
#  [4 5 6]]
```

## Create from List

```python
arr_from_list = np.array([1, 2, 3])
print(arr_from_list)  # [1 2 3]
```

## Ranges

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

## Zeros, Ones, Identity

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

## Random Arrays

| Code Example                       | Reference                                                                                     |
| ---------------------------------- | --------------------------------------------------------------------------------------------- |
| `np.random.randint(0, 10, (2, 3))` | See [Random Integers](random-sampling.md#random-integers)                                     |
| `np.random.rand(3, 2)`             | See [Uniform Random Numbers](random-sampling.md#uniform-random-numbers)                       |
| `np.random.normal(3, 2)`           | See [Random Numbers from Distributions](random-sampling.md#random-numbers-from-distributions) |
| `np.random.choice([1, 2, 3], 5)`   | See [Random Choice](random-sampling.md#random-choice)                                         |

## Unique Elements from Array

```python
sample = np.array([1, 2, 2, 3, 4, 4, 5, 6])
unique, counts = np.unique(sample, return_counts=True)
print(unique)   # [1 2 3 4 5 6]
print(counts)   # [1 2 1 2 1 1]

# Convert to dictionary
count_dict = dict(zip(unique, counts))
print(count_dict)  # {1: 1, 2: 2, 3: 1, 4: 2, 5: 1, 6: 1}
```

## Summary

- Arrays can be created from lists, ranges, or random distributions.
- Utility functions like `zeros`, `ones`, and `eye` are useful for initializing.
- `unique` helps in extracting distinct elements with their frequencies.
