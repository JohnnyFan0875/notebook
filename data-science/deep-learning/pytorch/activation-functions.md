# Activation Functions

Activation functions introduce **non-linearity** into neural networks.  
Without them, a deep neural network would behave like a linear model, no matter how many layers it has.

## 1. Sigmoid Function

**Formula:**

\[
\sigma(x) = \frac{1}{1 + e^{-x}}
\]

- **Range:** (0, 1)
  - For large negative x → output → 0.
  - For large positive x → output → 1.
  - At x = 0 → output = 0.5.
- **Use case:** Binary classification (probability output).
- **Limitations:**
  - Saturates at extreme values (gradients near 0).
  - Leads to **vanishing gradient problem** in deep networks.

![Image](https://editor.analyticsvidhya.com/uploads/94469sig%20derivative.png)

**PyTorch Example:**

```python
import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(6, 4),
    nn.Linear(4, 1),
    nn.Sigmoid()
)
```

## 2. Softmax Function

**Formula:**

\[
\text{Softmax}(x_i) = \frac{e^{x_i}}{\sum_j e^{x_j}}
\]

- **Range:** (0, 1), with all outputs summing to 1.
- **Use case:** Multi-class classification.
- Each output represents the probability of belonging to a class.
- Behavior: Converts a vector of scores (logits) into a probability distribution.
- **Limitation:** Still susceptible to saturation at extreme logits.
- Graph
  - **2-class case**: Looks similar to sigmoid (because softmax with 2 classes reduces to sigmoid).
  - **3+ classes**: You don’t get a single curve; you get multiple probability curves that compete — when one class probability goes up, others go down.

**PyTorch Example:**

```python
import torch
import torch.nn as nn

logits = torch.tensor([[1.0, 2.0, 3.0, 4.0]])
softmax = nn.Softmax(dim=-1)
print(softmax(logits))
```

## 3. ReLU (Rectified Linear Unit)

**Formula:**

\[
f(x) = \max(0, x)
\]

### Properties

- Introduces **sparsity** (some neurons inactive).
- Efficient to compute.
- Prevents **vanishing gradient** for positive values.

### Limitation

- Neurons with negative inputs have gradient 0 → **dead neurons** (neuron will not update during backpropagation).

![Image](https://pica.zhimg.com/v2-58ed41447e25974904be6fd1c5f21490_1440w.jpg)

### PyTorch Example

```python
import torch.nn as nn

relu = nn.ReLU()
```

## 4. Leaky ReLU

**Formula:**

\[
f(x) = \max(\alpha x, x), \quad \alpha \text{ is a small constant (e.g., 0.01)}
\]

### Improvement over ReLU

- For negative inputs, slope = **α** (not 0).
- Helps avoid the **dead neuron** problem.

### PyTorch Example

```python
import torch.nn as nn

leaky_relu = nn.LeakyReLU(negative_slope=0.05)
```

## Meaning of Activation Function Derivatives

In deep learning, the **derivative (gradient) of the activation function** is crucial because it directly affects  
**gradient descent** and **backpropagation**.

### Why the Derivative Matters

1. **Gradient Flow**

   - During backpropagation, we compute the derivative of the loss with respect to each layer’s parameters.
   - This requires the **chain rule**, where the derivative of the activation function is a key term.
   - If the derivative is too small → **vanishing gradients**.
   - If the derivative is too large → **exploding gradients**.

2. **Sensitivity of Nonlinear Transformation**

   - The derivative tells us how sensitive the output is to changes in the input.
   - Example: For the **sigmoid function**, at extreme inputs the slope is close to 0 → output hardly changes → learning stalls.

3. **Learning Efficiency**
   - The derivative shape influences how effectively gradients propagate.
   - **ReLU** has derivative = 1 for positive inputs → efficient gradient flow → faster training.
   - **Leaky ReLU** fixes the “dead neuron” issue of ReLU by keeping a small slope for negative inputs.

### Common Activation Functions and Derivatives

- **Sigmoid**  
  \[
  \sigma(x) = \frac{1}{1 + e^{-x}}, \quad
  \sigma'(x) = \sigma(x)(1 - \sigma(x))
  \]

  - Problem: For large |x|, derivative → 0 → vanishing gradients.

- **ReLU**  
  \[
  f(x) = \max(0, x), \quad
  f'(x) = \begin{cases}
  1 & x > 0 \\
  0 & x \leq 0
  \end{cases}
  \]

  - Advantage: Avoids vanishing gradients for positive inputs.
  - Limitation: Zero gradient for x ≤ 0 → “dead neurons”.

- **Leaky ReLU**  
  \[
  f(x) = \max(\alpha x, x), \quad
  f'(x) = \begin{cases}
  1 & x > 0 \\
  \alpha & x \leq 0
  \end{cases}
  \]
  - Fixes ReLU’s dead neuron problem by using a small slope α (e.g., 0.01) for negative inputs.

### Summary

- The **derivative of the activation function controls how gradients propagate**.
- It directly influences **learning ability** and **convergence speed**.
- Choosing an activation function requires considering its derivative:
  - Will it cause vanishing/exploding gradients?
  - Does it allow efficient learning?

## 📌 Summary

- **Sigmoid:** Good for binary classification but suffers from vanishing gradients.
- **Softmax:** Converts logits into class probabilities (multi-class tasks).
- **ReLU:** Default choice in hidden layers; simple and efficient.
- **Leaky ReLU:** Fixes ReLU’s dead neuron problem by allowing small gradients for negative inputs.

## 🔗 Related

- [Loss Functions](loss-functions.md) → Softmax is often combined with **CrossEntropyLoss**.
- [Backpropagation](backpropagation.md) → Gradients flow differently depending on the activation function.
