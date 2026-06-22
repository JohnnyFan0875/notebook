# Model Saving and Loading

PyTorch provides flexible ways to save and load models, layers, and parameters. 這不只是方便重用模型，也直接影響你是否能穩定恢復訓練、做遷移學習，或把推論服務搬到另一台機器。

## 常見需求

- reusing trained models without retraining
- transfer learning
- resuming training
- sharing models

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

Saving entire layers or models directly with `torch.save(model, ...)` also saves their class definitions. 這在快速實驗時很方便，但當程式碼版本改變時容易出現相容性問題。

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

這通常是最穩健、也最適合長期保存與 production 的做法。

## Saving and Loading Entire Models

```python
# Save entire model
torch.save(model, "full_model.pth")

# Load entire model
model_loaded = torch.load("full_model.pth")
```

Save-and-load 整個 model object 較適合快速實驗，不適合作為長期保存策略。

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

## Recommended Checkpoint Pattern

除了模型權重，實務上通常還會一起保存：

- current epoch
- optimizer state
- scheduler state
- random seed
- validation metric

這樣當訓練中斷時，才能更接近原狀恢復。

## Common Pitfalls

- 載入權重後忘記 `model.eval()` 就直接做 inference。
- 只存模型，不存 optimizer 與訓練設定，導致無法真正續訓。
- 在不同裝置間載入時，沒有處理 `map_location`。
