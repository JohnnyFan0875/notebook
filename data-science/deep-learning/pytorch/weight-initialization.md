# Weight Initialization in PyTorch

## Overview

Weight initialization is crucial in deep learning because it sets the **starting point** for optimization.  
Good initialization can:

- Accelerate convergence
- Prevent vanishing/exploding gradients
- Improve final model performance

Poor initialization may cause:

- Very slow training
- Getting stuck in poor local minima
- Unstable gradients

---

## Reinitializing Layer Weights

Sometimes you want to **reset specific layers before retraining**:

- **Restart training from scratch**: Escape poor local minima
- **Test different initialization strategies**: Some strategies work better depending on architecture (e.g., CNNs, RNNs, Transformers)
- **Fine-tune a pre-trained model**: Reinitialize some layers while keeping others frozen

```python
import torch.nn as nn

# Example: reinitialize weights of a specific layer
nn.init.uniform_(layer.weight)

# Check range of initialized values
print(custom_layer.fc.weight.min(), custom_layer.fc.weight.max())
```

## Common Initialization Strategies

PyTorch provides several initialization methods in `torch.nn.init`:

### Uniform Initialization

```python
nn.init.uniform_(layer.weight, a=-0.1, b=0.1)
```

Fills weights with values from a uniform distribution [_a_, _b_].

### Normal Initialization

```python
nn.init.normal_(layer.weight, mean=0.0, std=0.02)
```

Fills weights with values from a normal distribution.

### Xavier/Glorot Initialization

Designed for layers with **sigmoid/tanh** activations.

```python
nn.init.xavier_uniform_(layer.weight)
nn.init.xavier_normal_(layer.weight)
```

##Kaiming/He Initialization

Recommended for ReLU or LeakyReLU activations.

```python
nn.init.kaiming_uniform_(layer.weight, nonlinearity="relu")
nn.init.kaiming_normal_(layer.weight, nonlinearity="relu")
```

### Constant Initialization

```python
nn.init.constant_(layer.bias, 0.0)
```

Sets all bias values to a constant.

## Best Practices

- Match initialization to the activation function:
  - Sigmoid/tanh → Xavier
  - ReLU/LeakyReLU → Kaiming/He
- Always reinitialize weights and biases together if resetting layers
- For reproducibility, set a random seed before initialization
- In transfer learning, reinitialize only the final classifier layers (others can stay frozen)
