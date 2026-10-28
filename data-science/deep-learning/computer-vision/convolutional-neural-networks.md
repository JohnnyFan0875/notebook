# Convolutional Neural Networks

CNN 是影像任務的經典起點。它的核心不是「神經網路比較深」，而是利用卷積核與局部感受野，讓模型更有效率地學到空間結構。

## 為什麼影像不適合直接全連接

若直接把影像攤平成一大串數值再接全連接層，參數量會暴增，而且模型很難利用鄰近像素之間的空間關係。

CNN 的做法是：

- 用小卷積核掃過局部區域
- 共享權重，減少參數量
- 逐層從邊緣、紋理到更高階特徵

## CNN 的常見元件

| 元件 | 作用 |
| --- | --- |
| convolution | 擷取局部特徵 |
| activation | 加入非線性 |
| pooling | 降低空間解析度、增加穩健性 |
| batch normalization | 穩定訓練 |
| fully connected head | 做最終分類 |

## PyTorch Skeleton

```python
from torch import nn

model = nn.Sequential(
    nn.Conv2d(3, 16, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Conv2d(16, 32, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(32 * 16 * 16, 64),
    nn.ReLU(),
    nn.Linear(64, 4),
)
```

## 該注意哪些 shape

- `Conv2d` 的輸入通常是 `(batch, channels, height, width)`
- pooling 會改變高與寬
- 接到 `Linear` 前，務必確認 flatten 後的維度

## 影像分類流程

1. 準備資料集與標籤
2. 做 resize、normalize、augmentation
3. 用 `DataLoader` 建立 mini-batch
4. 定義模型與 loss
5. 訓練並監控 validation 表現
6. 檢查 confusion matrix、錯誤樣本與 class imbalance

| 前處理 | 作用 |
| --- | --- |
| `Resize` | 統一輸入大小 |
| `ToTensor` | 把影像轉成 tensor |
| `Normalize` | 讓像素分布穩定 |
| augmentation | flip、crop、color jitter；只套在 train |

```python
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
])
train_ds = datasets.FakeData(size=512, image_size=(3, 64, 64), num_classes=4, transform=transform)
train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)

criterion = nn.CrossEntropyLoss()                       # model 用上面的 CNN skeleton（64×64 輸入 → 32×16×16）
optimizer = optim.Adam(model.parameters(), lr=1e-3)
```

## 輸出該怎麼看

- 多類別分類時，輸出通常是 logits，不是機率。
- 要看預測類別時，常用 `argmax(dim=1)`。
- 要看類別機率時，可再接 `softmax`，但訓練時的 `CrossEntropyLoss` 不需要你手動先做 softmax。

## 常見錯誤

- 忘記算卷積與 pooling 後的輸出 shape，導致 `Linear` 維度不合。
- 把 `CrossEntropyLoss` 和手動 `Softmax` 疊在一起用。
- augmentation 只套在 train，卻忘了 validation 也要至少做一致的 resize / tensor transform。
- 資料量不多卻訓練太深的 CNN，結果嚴重 overfitting；資料不多時先用 [Transfer Learning](../training-workflows/transfer-learning.md)。
- 只看訓練 accuracy，不看 validation loss 是否反而上升；accuracy 不錯也要回頭看哪些類別最常被混淆。

## 小結

CNN 是學影像 deep learning 最好的入門任務，因為它能把資料前處理、模型設計、shape 檢查、loss 與評估全部串起來。
