# Transfer Learning in PyTorch

## Overview

Transfer learning leverages **pre-trained models** and adapts them to new tasks.  
This approach is widely used in deep learning when:

- Training data is limited
- Computational resources are constrained
- Pre-trained models capture general patterns (e.g., image features, language embeddings)

Common strategies:

1. **Feature extraction**: Freeze most layers, only train the final classifier.
2. **Fine-tuning**: Start with a pre-trained model and update selected layers.

---

## Freezing Layers (Feature Extraction)

To **freeze a layer’s weights**, set `requires_grad = False`.  
This prevents PyTorch from computing gradients for those parameters during backpropagation.
Only the unfrozen parameters will be updated during training.

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(64, 128),
    nn.Linear(128, 256)
)

# Freeze first layer weights
for name, param in model.named_parameters():
    if name == "0.weight":   # first layer's weight
        param.requires_grad = False
```

## Fine-Tuning

Fine-tuning involves unfreezing some layers (often later ones) and training them on new data.
This is especially useful when the pre-trained model’s features are relevant but require adaptation.

```python
# Example: unfreeze the last layer
for name, param in model.named_parameters():
    if "1" in name:  # refers to the second layer
        param.requires_grad = True
```

## Best Practices

- Use **pre-trained models** from libraries like torchvision.models or transformers
- For small datasets → freeze most layers and only train the classifier
- For larger datasets → fine-tune more layers or the entire network
- Always monitor validation accuracy to avoid overfitting
- Consider using different **optimizers** or **learning rates** for frozen vs. trainable layers