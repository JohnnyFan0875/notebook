# Image Classification Workflow

來自 `Deep Learning for Images with PyTorch` 的內容，最值得抽出的不是某一個 API，而是一個完整的影像分類流程：資料如何進來、標籤怎麼對應、模型輸出怎麼解讀、驗證要看什麼。

## 影像分類流程

1. 準備資料集與標籤
2. 做 resize、normalize、augmentation
3. 用 `DataLoader` 建立 mini-batch
4. 定義模型與 loss
5. 訓練並監控 validation 表現
6. 檢查 confusion matrix、錯誤樣本與 class imbalance

## 常見資料前處理

- `Resize`：統一輸入大小
- `ToTensor`：把影像轉成 tensor
- `Normalize`：讓像素分布穩定
- augmentation：如 flip、crop、color jitter

## Minimal Example

```python
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
])

train_ds = datasets.FakeData(
    size=512,
    image_size=(3, 64, 64),
    num_classes=4,
    transform=transform,
)

train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)

model = nn.Sequential(
    nn.Flatten(),
    nn.Linear(3 * 64 * 64, 128),
    nn.ReLU(),
    nn.Linear(128, 4),
)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)
```

## 輸出該怎麼看

- 多類別分類時，輸出通常是 logits，不是機率。
- 要看預測類別時，常用 `argmax(dim=1)`。
- 要看類別機率時，可再接 `softmax`，但訓練時的 `CrossEntropyLoss` 不需要你手動先做 softmax。

## 初學者常見陷阱

- 把 `CrossEntropyLoss` 和手動 `Softmax` 疊在一起用。
- augmentation 只套在 train，卻忘了 validation 也要至少做一致的 resize / tensor transform。
- accuracy 不錯就停止檢查，沒有回頭看哪些類別最常被混淆。

## 什麼時候先用 transfer learning

若資料量不大，通常比起自己從頭訓練 CNN，先用 [Transfer Learning](../training-workflows/transfer-learning.md) 會更穩、更省時間。
