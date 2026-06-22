# Transfer Learning

Transfer learning leverages pre-trained models and adapts them to new tasks. 它在資料量有限、訓練成本高，或預訓練模型已經學到通用特徵時特別有價值。

## 什麼時候特別適合

- 影像分類資料不多，但可借用 ImageNet 預訓練 backbone
- NLP 任務想利用已訓練好的語意表示
- 沒有足夠算力從頭訓練大型模型

## Common strategies

1. **Feature extraction**: freeze most layers, only train the final classifier
2. **Fine-tuning**: start with a pre-trained model and update selected layers

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

## 實務上怎麼選

- 資料很少、和原任務很像：先用 feature extraction。
- 資料較多、和原任務有差異：逐步 fine-tune 後段或整個模型。
- 若新任務和原任務差太遠，預訓練特徵不一定有幫助。

## Best Practices

- Use **pre-trained models** from libraries like torchvision.models or transformers
- For small datasets → freeze most layers and only train the classifier
- For larger datasets → fine-tune more layers or the entire network
- Always monitor validation accuracy to avoid overfitting
- Consider using different **optimizers** or **learning rates** for frozen vs. trainable layers

## Common Pitfalls

- 忘記只把 `requires_grad=True` 的參數交給 optimizer。
- 一開始就用過大的 learning rate fine-tune，導致預訓練權重被快速破壞。
- 凍結層後卻忘了處理 BatchNorm / eval mode 的行為差異。
