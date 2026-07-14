# NumPy Linear Algebra

This section demonstrates linear algebra operations in NumPy.

## Example Arrays

```python
import numpy as np

# Example 2x2 matrices
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Example vectors
C = np.array([1, 2, 3])
D = np.array([4, 5, 6])
```

## Matrix Multiplication (Dot Product)

```python
np.dot(A, B)
# [[19 22]
#  [43 50]]
```

- Standard matrix multiplication: row-by-column.

```python
np.dot(C, D)
# 32
```

- Dot product of two vectors = sum of element-wise multiplication.

## Inner Product

```python
np.inner(A, B)
# [[17 23]
#  [39 53]]
```

- Inner product treats rows as vectors and computes dot products.

```python
np.inner(C, D)
# 32
```

- Same as dot product for 1D vectors.

## Cross Product

```python
np.cross(C, D)
# [-3  6 -3]
```

- Cross product is specific to 3D vectors and results in another 3D vector perpendicular to both.

## Matrix Inverse

```python
np.linalg.inv(A)
# [[-2.   1. ]
#  [ 1.5 -0.5]]
```

- The inverse matrix is such that `A @ A_inv = Identity`. Not all matrices are invertible.

## Eigenvalues and Eigenvectors

```python
eigenvalues, eigenvectors = np.linalg.eig(A)
print(eigenvalues)
# [-0.37228132  5.37228132]
print(eigenvectors)
# [[-0.82456484 -0.41597356]
#  [ 0.56576746 -0.90937671]]
```

- Eigenvalues measure how much a vector is stretched. Eigenvectors are the directions that remain unchanged except for scaling.

## Outer Product

```python
np.outer(C, D)
# [[ 4  5  6]
#  [ 8 10 12]
#  [12 15 18]]
```

- Creates a matrix where each element is the product of an element from `C` and `D`.

## Remainder

```python
np.remainder(C, D)
# [1 2 3]
```

- Element-wise remainder after division.

## Solve Linear System

```python
b = np.array([5, 11])
np.linalg.solve(A, b)
# [1. 2.]
```

- Solves the system of linear equations `Ax = b`.

## Summary

- **Dot / Inner product**: measures projection or similarity between vectors/matrices.
- **Cross product**: perpendicular vector in 3D.
- **Inverse & determinant**: matrix algebra properties, important for solving systems.
- **Eigenvalues/vectors**: fundamental in transformations and dimensionality reduction.
- **Element-wise arithmetic**: common operations for arrays.
- **Linear system solving**: direct computation of unknown variables from equations.
