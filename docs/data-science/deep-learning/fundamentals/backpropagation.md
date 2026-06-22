# Backpropagation

## Overview

Backpropagation is the key algorithm used to **train neural networks**.
It updates weights to reduce error by computing the gradient of the loss function with respect to each weight and adjusting weights in the opposite direction (via **gradient descent**).

**Core steps:**

1. Forward pass: compute predictions
2. Compare predictions with ground truth (loss)
3. Backward pass: compute gradients using the chain rule
4. Update weights using an optimizer (e.g., SGD, Adam)

## Mathematical Intuition

For a weight parameter \( w \):

\[
w \leftarrow w - \eta \cdot \frac{\partial L}{\partial w}
\]

- \( \eta \): learning rate
- \( L \): loss function
- \( \frac{\partial L}{\partial w} \): gradient of the loss w.r.t. the weight

## Simple PyTorch Example

```python
import torch
import torch.nn as nn
import torch.optim as optim

# Define a simple model
model = nn.Sequential(
    nn.Linear(16, 8),
    nn.Linear(8, 4),
    nn.Linear(4, 2),
    nn.Softmax(dim=1)
)

# Sample input and target
sample = torch.randn(1, 16)  # batch size 1, 16 features
target = torch.tensor([1])   # classification target (2 classes)

# Define loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.001)

# Forward + Backward + Update
prediction = model(sample)
loss = criterion(prediction, target)

optimizer.zero_grad()
loss.backward()
optimizer.step()

print("Loss:", loss.item())
```

## Training & Validation Loop with Accuracy Monitoring

```python
from torch.utils.data import DataLoader, TensorDataset
import torchmetrics
import torch.nn as nn
import torch.optim as optim
import torch

# Example dataset
X_train = torch.rand(100, 10)
y_train = torch.randint(0, 2, (100,))
X_val = torch.rand(20, 10)
y_val = torch.randint(0, 2, (20,))

train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=16, shuffle=True)
val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=16)

# Define simple model
model = nn.Sequential(
    nn.Linear(10, 16),
    nn.ReLU(),
    nn.Linear(16, 2)
)

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

num_epochs = 5
for epoch in range(num_epochs):

    ### Training Phase ###
    model.train()
    train_loss = 0.0
    train_acc = torchmetrics.Accuracy(task="multiclass", num_classes=2)

    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        train_loss += loss.item()
        train_acc.update(outputs.argmax(dim=1), labels)

    train_loss /= len(train_loader)
    train_accuracy = train_acc.compute()

    ### Validation Phase ###
    model.eval()
    val_loss = 0.0
    val_acc = torchmetrics.Accuracy(task="multiclass", num_classes=2)

    with torch.no_grad():
        for inputs, labels in val_loader:
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            val_loss += loss.item()
            val_acc.update(outputs.argmax(dim=1), labels)

    val_loss /= len(val_loader)
    val_accuracy = val_acc.compute()

    print(f"Epoch {epoch+1}/{num_epochs}: "
          f"Train Loss = {train_loss:.4f}, Train Acc = {train_accuracy:.2f}, "
          f"Val Loss = {val_loss:.4f}, Val Acc = {val_accuracy:.2f}")

    # Reset metrics
    train_acc.reset()
    val_acc.reset()
```

## Manual Weight Updates (for demonstration)

```python
# Access gradients for first layer
grad_w, grad_b = model[0].weight.grad, model[0].bias.grad

# Learning rate
lr = 0.001

# Manual update
model[0].weight.data -= lr * grad_w
model[0].bias.data   -= lr * grad_b
```

## Practical Notes

- **Learning rate is critical**
  - Too high → divergence
  - Too low → slow training
- Always call **`optimizer.zero_grad()`** before `loss.backward()`
- Use **validation sets** (`model.eval()`, `torch.no_grad()`) to monitor generalization
- Layers can be **frozen** for transfer learning (see [Transfer Learning](../training-workflows/transfer-learning.md))
- Weights can be **reinitialized** if stuck (see [Weight Initialization](weight-initialization.md))
