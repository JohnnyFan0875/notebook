# Linear Layer in PyTorch

## Overview

A **linear layer** (also called a fully connected or dense layer) performs a simple linear transformation:

\[
Y = XW^T + b
\]

- \( X \): input tensor (batch of input samples)
- \( W \): weight matrix (learnable parameters)
- \( b \): bias vector (learnable parameters)

This is the building block of **Multilayer Perceptrons (MLPs)**.

## Basic Example

```python
import torch
import torch.nn as nn

input_tensor = torch.tensor([[0, 1, 2]])
linear_layer = nn.Linear(in_features=3, out_features=2)
output_tensor = linear_layer(input_tensor)

print("Weights:\n", linear_layer.weight)
print("Bias:\n", linear_layer.bias)

# Formula:
# output = input * weight^T + bias
```

## Parameter Counting

Each neuron has:

- One weight per input feature
- One bias term

```python
model = nn.Sequential(
    nn.Linear(10, 18),  # input 10 → output 18
    nn.Linear(18, 5)    # input 18 → output 5
)

# First layer: 18 neurons × (10 + 1 bias) = 198 parameters
# Second layer: 5 neurons × (18 + 1 bias) = 95 parameters

total = 0
for parameter in model.parameters():
    total += parameter.numel()
print("Total parameters:", total)  # 293
```

## Manual Weights and Bias

You can manually set weights and biases for demonstration.

```python
layer = nn.Linear(2, 3)

# Manually assign values
with torch.no_grad():
    layer.weight = nn.Parameter(torch.tensor([[0.5, -0.3],
                                              [0.2,  0.8],
                                              [-0.7, 0.4]]))
    layer.bias = nn.Parameter(torch.tensor([0.1, -0.2, 0.3]))

x = torch.tensor([[2.0, 3.0]])
output = layer(x)
print(output)
```

### Step-by-Step Breakdown

Consider the example above with \( x = [2, 3] \):

\[
x \times W^T =
[2, 3] \times
\begin{bmatrix}
0.5 & -0.3 \\
0.2 & 0.8 \\
-0.7 & 0.4
\end{bmatrix}^T
\]

Breaking it down:

- **First output neuron**:  
  \((2 \times 0.5) + (3 \times -0.3) = 0.1\)

- **Second output neuron**:  
  \((2 \times 0.2) + (3 \times 0.8) = 2.8\)

- **Third output neuron**:  
  \((2 \times -0.7) + (3 \times 0.4) = -0.2\)

So, before bias:
\[
[0.1, \; 2.8, \; -0.2]
\]

Adding bias \([0.1, -0.2, 0.3]\):
\[
[0.2, \; 2.6, \; 0.1]
\]

✅ **Final output**: `[0.2, 2.6, 0.1]`

## Practical Notes

- `nn.Linear(in_features, out_features)` automatically initializes weights and biases.
- Initialization can be customized with methods like **Xavier** or **Kaiming** (see [Weight Initialization](weight-initialization.md)).
- Linear layers are often combined with **activation functions** (`ReLU`, `Sigmoid`, etc.) to build non-linear models (see [Activation functions](activation-functions.md)).
- Always check **parameter counts** when designing networks → helps avoid **underfitting** (too few parameters) or **overfitting** (too many parameters).
