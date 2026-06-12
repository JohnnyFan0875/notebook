# NumPy Random Sampling

## Example Setup

```python
import numpy as np

np.random.seed(42)  # Set seed for reproducibility
```

- Setting a seed ensures the same random numbers are generated each time.

## Random Numbers from Distributions

```python
np.random.normal(0, 1, 10)
# Example Output: [ 0.4967 -0.1383  0.6477  1.5230 -0.2341 -0.2341  1.5792  0.7674 -0.4695  0.5426]
```

- Normal distribution with mean `0` and standard deviation `1`, 10 samples.

```python
np.random.normal(loc=10, scale=2, size=(3, 5))
# 3x5 matrix, mean=10, std=2
# Example Output:
# [[10.99  8.72 11.30 13.05  9.53]
#  [ 8.53  9.54  8.54 11.54  9.54]
#  [ 9.35 11.91  8.75 10.75  9.75]]
```

## Uniform Random Numbers

```python
np.random.rand(3, 2)
# Example Output:
# [[0.42 0.72]
#  [0.  0.3 ]
#  [0.15 0.9 ]]
```

- Generates samples from uniform distribution over \[0,1).

## Random Integers

```python
np.random.randint(0, 10, size=5)
# Example Output: [6 3 7 4 6]
```

- Random integers between 0 (inclusive) and 10 (exclusive).

```python
np.random.randint(0, 10, (2, 3))
# Example Output:
# [[2 9 4]
#  [1 7 6]]
```

- 2x3 matrix of random integers.

## Random Choice

```python
np.random.choice(10, 5, replace=False)
# Example Output: [2 8 4 9 1]
```

- Randomly choose 5 unique numbers from range(0,10).

```python
weather = ['windy','cloudy','sunny','rainy']
weather_pick = np.random.choice(weather, size=(4,7), replace=True, p=[0.2,0.5,0.2,0.1])
print(weather_pick)
# Example Output (4x7 matrix of weather):
# [['cloudy' 'cloudy' 'rainy' 'cloudy' 'sunny' 'windy' 'cloudy']
#  ['cloudy' 'windy' 'sunny' 'rainy' 'cloudy' 'cloudy' 'cloudy']
#  ['windy'  'cloudy' 'sunny' 'cloudy' 'cloudy' 'cloudy' 'rainy']
#  ['cloudy' 'cloudy' 'windy' 'rainy' 'sunny'  'cloudy' 'cloudy']]
```

- Sampling with replacement, with specified probabilities `p` for each outcome.

```python
dice_random_choice = np.random.choice(list(range(1,7)), size=10, replace=True)
```

## Shuffle

```python
sample = np.arange(10)
np.random.shuffle(sample)
print(sample)
# Example Output: [8 1 5 0 7 2 9 4 3 6]
```

- `np.random.shuffle` randomly permutes the elements of an array in place along the first axis.

## Repeated Seeds for Same Output

```python
np.random.seed(1)
print(np.random.rand()) # 0.417022004702574
print(np.random.rand()) # 0.7203244934421581

np.random.seed(1)
print(np.random.rand()) # 0.417022004702574
print(np.random.rand()) # 0.7203244934421581
```

- Resetting the seed produces identical results — useful for reproducibility.

## Summary

- **`rand`**: uniform distribution over \[0,1).
- **`randn` / `normal`**: samples from normal distribution.
- **`randint`**: random integers in specified range.
- **`choice`**: sample elements with or without replacement.
- **`shuffle`**: randomly permute elements along the first axis.
- **Seed (`np.random.seed`)**: ensures reproducibility of results.
