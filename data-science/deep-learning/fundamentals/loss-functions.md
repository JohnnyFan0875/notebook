# Loss Functions

A **loss function** (or cost function) measures how well the model’s predictions match the true labels.
It provides feedback to update model weights via **gradient descent** and **backpropagation**.

This note focuses on **deep-learning training mechanics**: PyTorch loss APIs, differentiable objectives, and how losses drive backpropagation. For the higher-level machine-learning perspective on choosing a loss by task and separating training loss from evaluation metrics, see [Machine Learning: Loss Functions](../../machine-learning/foundations/loss-functions.md).

- Wrong predictions → high loss
- Correct predictions → low loss

## Cross-Entropy Loss

The most common loss for classification tasks.

**Formula:**

For a single sample with true label \(y\) and predicted probabilities \(p\):

\[
L = -\log(p_y)
\]

For multiple samples (average over N):

\[
L = -\frac{1}{N} \sum*{i=1}^N \log(p*{i,y_i})
\]

- Equivalent to **Softmax + Negative Log-Likelihood**.
- Encourages the correct class probability to be high.

**PyTorch Example:**

```python
import torch
import torch.nn as nn

# Example: 3 classes, 2 samples
logits = torch.tensor([[2.1, -1.4, 0.8],
                       [1.2,  0.3, 1.8]], dtype=torch.float32)
target = torch.tensor([0, 2])  # class indices

loss_fn = nn.CrossEntropyLoss()
loss = loss_fn(logits, target)

print(f'Loss: {loss.item()}')
```

## Explanation (Cross-Entropy Example)

- For the first sample:
  Softmax probabilities: _p_ = Softmax([2.1,−1.4,0.8]) = [0.767,0.023,0.208]
  Correct class = 0 → loss = \(-\log(0.767) ≈ 0.264\)

- For the second sample:
- Softmax probabilities: _p_ = Softmax([1.2,0.3,1.8]) = [0.307,0.125,0.568]
  Correct class = 2 → loss = \(-\log(0.568) ≈ 0.574\)

- Final average = (0.264 + 0.574) / 2 ≈ **0.419**

## Mean Squared Error (MSE)

**Formula:**

\[
L = \frac{1}{N} \sum\_{i=1}^N (y_i - \hat{y}\_i)^2
\]

- Common for **regression tasks**.
- Penalizes large deviations more heavily.
- Not ideal for classification (outputs may not represent probabilities).

**PyTorch Example:**

```python
import torch
import torch.nn as nn

loss_fn = nn.MSELoss()
pred = torch.tensor([2.5, 0.0, 2.0])
target = torch.tensor([3.0, -0.5, 2.0])
loss = loss_fn(pred, target)
print(loss.item())
```

## Binary Cross-Entropy (BCE)

Used for **binary classification tasks**.

**Formula:**

\[
L = -\frac{1}{N} \sum\_{i=1}^N \left[ y_i \log(p_i) + (1 - y_i) \log(1 - p_i) \right]
\]

- Each sample has a target \(y \in \{0,1\}\).
- Predictions are probabilities \(p \in (0,1)\), usually from a **sigmoid**.

**PyTorch Example:**

```python
import torch
import torch.nn as nn

loss_fn = nn.BCELoss()
pred = torch.tensor([0.9, 0.2, 0.8], dtype=torch.float32)
target = torch.tensor([1.0, 0.0, 1.0], dtype=torch.float32)
loss = loss_fn(pred, target)
print(loss.item())
```

⚠️ For numerical stability, prefer nn.BCEWithLogitsLoss(), which combines Sigmoid + BCE in a single function.

## Hinge Loss (for SVMs)

**Formula:**

\[
L = \frac{1}{N} \sum\_{i=1}^N \max(0, 1 - y_i \cdot \hat{y}\_i)
\]

- Used in **Support Vector Machines (SVMs)**.
- Encourages **margin maximization** between classes.

⚠️ PyTorch does not include Hinge Loss in `nn`, but it can be implemented manually or accessed via `torch.nn.functional`.

## 📌 Summary

- **CrossEntropyLoss:** Standard for multi-class classification.
- **BCE / BCEWithLogitsLoss:** For binary classification.
- **MSELoss:** For regression tasks.
- **Hinge Loss:** For margin-based classifiers (e.g., SVMs).

Loss functions provide the **signal for backpropagation**, guiding the network to update its weights toward minimizing errors.

| Loss Function                  | Typical Use                | Formula (simplified)                             | PyTorch API                               |
| ------------------------------ | -------------------------- | ------------------------------------------------ | ----------------------------------------- |
| **Mean Squared Error (MSE)**   | Regression                 | $L = \frac{1}{N}\sum (y - \hat{y})^2$            | `nn.MSELoss()`                            |
| **Binary Cross-Entropy (BCE)** | Binary classification      | $L = -\frac{1}{N}\sum [y\log(p)+(1-y)\log(1-p)]$ | `nn.BCELoss()` / `nn.BCEWithLogitsLoss()` |
| **Cross-Entropy Loss**         | Multi-class classification | $L = -\log(p_{y})$                               | `nn.CrossEntropyLoss()`                   |
| **Hinge Loss**                 | Support Vector Machines    | $L = \max(0, 1 - y\hat{y})$                      | Manual / `torch.nn.functional`            |
| **KL Divergence**              | Probabilistic models       | $D_{KL}(P \| Q) = \sum P \log(P/Q)$              | `nn.KLDivLoss()`                          |

## 🔗 Related

- [Activation Functions](activation-functions.md) → Softmax & Sigmoid are closely tied to Cross-Entropy and BCE.
- [Backpropagation](backpropagation.md) → Gradients of the loss function are propagated through the network to update weights.
