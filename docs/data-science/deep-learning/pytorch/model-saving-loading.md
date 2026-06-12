# Model Saving and Loading in PyTorch

## Overview

PyTorch provides flexible ways to **save and load models**, layers, and parameters.
This is useful for:

- Reusing trained models without retraining
- Transfer learning
- Resuming training
- Sharing models

## Saving and Loading Entire Layers

```python
import torch
import torch.nn as nn

# Example: define a layer
layer = nn.Linear(2, 3)

# Save the layer
torch.save(layer, "layer.pth")

# Load the layer
new_layer = torch.load("layer.pth")
print(new_layer)
```

⚠️ Saving entire layers or models directly (torch.save(model, ...)) also saves their class definitions. This can cause issues if code changes between saving and loading.

## Recommended Approach: State Dictionaries

```python
import torch
import torch.nn as nn

# Define a simple model
model = nn.Sequential(
    nn.Linear(10, 16),
    nn.ReLU(),
    nn.Linear(16, 2)
)

# Save state dictionary (save the weights)
torch.save(model.state_dict(), "model_state.pth")

# Load state dictionary
loaded_model = nn.Sequential(
    nn.Linear(10, 16),
    nn.ReLU(),
    nn.Linear(16, 2)
)
loaded_model.load_state_dict(torch.load("model_state.pth")) # Load the trained weights
loaded_model.eval()                                         # Set to evaluation mode
```

✅ This is the most robust method and recommended in production.

## Saving and Loading Entire Models

```python
# Save entire model
torch.save(model, "full_model.pth")

# Load entire model
model_loaded = torch.load("full_model.pth")
```

⚠️ Use this mainly for quick experiments, not for long-term model storage.

## Saving and Loading Optimizers

```python
import torch.optim as optim

optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# Save model + optimizer
checkpoint = {
    "epoch": 10,
    "model_state": model.state_dict(),
    "optimizer_state": optimizer.state_dict()
}
torch.save(checkpoint, "checkpoint.pth")

# Load
checkpoint = torch.load("checkpoint.pth")
model.load_state_dict(checkpoint["model_state"])
optimizer.load_state_dict(checkpoint["optimizer_state"])
start_epoch = checkpoint["epoch"]
```

## Best Practices

- Prefer **`state_dict()`** over saving entire models
- Always call **`model.eval()`** after loading for inference
- Save both **model** and **optimizer state** for resuming training
- Use **checkpoints** when training large models
- For reproducibility, also save **training settings** (epochs, learning rate, etc.)
