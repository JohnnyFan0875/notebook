# Tensors in PyTorch

## Overview

A **tensor** is the fundamental building block of deep learning in PyTorch.

- Similar to NumPy arrays, but with additional features like GPU acceleration and automatic differentiation.
- Used to represent scalars, vectors, matrices, and higher-dimensional data.

## Creating Tensors

```python
import torch
import numpy as np

# Direct creation
tensor = torch.tensor([[1, 2], [3, 4]])

# From NumPy array
np_array = np.array([[1, 2], [3, 4]])
tensor_from_np = torch.from_numpy(np_array)

# Random tensor
rand_tensor = torch.rand(2, 3)

# Zeros and ones
zeros = torch.zeros(2, 2)
ones = torch.ones(3, 3)

# Identity matrix
eye = torch.eye(3)

# With specific dtype
float_tensor = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float32)
```

## Tensor Properties

```python
print(tensor.shape)   # dimensions
print(tensor.dtype)   # data type (float32, int64, etc.)
print(tensor.device)  # CPU or CUDA
```

- shape: Dimensions of the tensor
- dtype: Data type (float, int, bool, etc.)
- device: Location of the tensor (CPU or GPU)

To move to GPU:

```python
if torch.cuda.is_available():
    tensor = tensor.to("cuda")
```

## Basic Operations

```python
a = torch.tensor([[1, 2], [3, 4]])
b = torch.tensor([[1, 2], [3, 4]])

print(a + b)                 # elementwise addition
print(a * b)                 # elementwise multiplication
print(torch.matmul(a, b))    # matrix multiplication
print(a.T)                   # transpose
```

- Other useful operations:
  - Slicing: a[0, :]
  - Reshape: a.view(-1)
  - Concatenate: torch.cat((a, b), dim=0)

## Gradients and Autograd

Tensors can track computations for automatic differentiation.

```python
x = torch.tensor(2.0, requires_grad=True)
y = x**2 + 3*x + 1
y.backward()   # compute gradient dy/dx
print(x.grad)  # prints 7.0
```

## Interoperability with NumPy

- Convert PyTorch → NumPy:

```python
np_array = tensor.numpy()
```

- Convert NumPy → PyTorch:

```python
tensor = torch.from_numpy(np_array)
```

⚠️ Note: Both share the same memory! Changing one affects the other.

## Best Practices

- Use `torch.float32` for most models, but `torch.float16` or `torch.bfloat16` for mixed precision training.
- Use `to(device)` to explicitly move tensors between **CPU** and **GPU**.
- For reproducibility, set seeds:

```python
torch.manual_seed(42)
```

- Avoid using plain Python loops for tensor operations → prefer vectorized operations for speed.
