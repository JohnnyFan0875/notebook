[Deep Learning](../README.md) › [電腦視覺](README.md) › 卷積神經網路

# 卷積神經網路 (Convolutional Neural Networks, CNN)

CNN 用小卷積核 (kernel) 掃過影像，同一組權重在每個位置共用。這帶來兩個好處：參數量遠少於全連接層，而且同一個特徵（邊緣、細胞核紋理）無論出現在哪裡都能被偵測到。

## 為什麼不用全連接層

| 做法 | 224×224×3 影像接 1,000 個單元的參數量 | 空間結構 |
| --- | --- | --- |
| 攤平後接 `Linear` | 約 1.5 億 | 丟失；像素位置一移動就是不同輸入 |
| `Conv2d(3, 64, kernel_size=3)` | 3×3×3×64 + 64 = 1,792 | 保留；局部連接、權重共享 |

## 元件

| 元件 | 作用 | PyTorch |
| --- | --- | --- |
| 卷積 (convolution) | 擷取局部特徵；輸出通道數 = kernel 數 | `nn.Conv2d(C_in, C_out, kernel_size, stride, padding)` |
| 激活 | 非線性 | `nn.ReLU()` |
| Normalization | 穩定訓練 | `nn.BatchNorm2d(C)`，見 [Normalization](../fundamentals/regularization-and-normalization.md#batchnorm-vs-layernorm) |
| Pooling | 降低空間解析度、增加對小位移的容忍 | `nn.MaxPool2d(2)` |
| Global average pooling | 每個通道取平均 → 長度 C 的向量，與輸入大小無關 | `nn.AdaptiveAvgPool2d(1)` |
| 分類頭 | 向量 → 類別 logits | `nn.Linear(C, K)` |

逐層堆疊後，前面的層學邊緣與紋理，後面的層組合成更高階的形狀；每個輸出位置「看得到」的輸入範圍（感受野 receptive field）隨深度擴大。

## 輸出尺寸

$$
H_{out} = \left\lfloor \frac{H_{in} + 2 \cdot \text{padding} - \text{kernel}}{\text{stride}} \right\rfloor + 1
$$

| 設定 | 64×64 輸入 → 輸出 |
| --- | --- |
| `kernel=3, padding=1, stride=1` | 64×64（"same"） |
| `kernel=3, padding=0` | 62×62 |
| `kernel=3, padding=1, stride=2` | 32×32 |
| `MaxPool2d(2)` | 32×32 |

## 影像分類模型

```python
import torch
from torch import nn

model = nn.Sequential(
    nn.Conv2d(3, 16, kernel_size=3, padding=1), nn.BatchNorm2d(16), nn.ReLU(),
    nn.MaxPool2d(2),                                   # 64 → 32
    nn.Conv2d(16, 32, kernel_size=3, padding=1), nn.BatchNorm2d(32), nn.ReLU(),
    nn.MaxPool2d(2),                                   # 32 → 16
    nn.Flatten(),                                      # 32 × 16 × 16 = 8192
    nn.Linear(32 * 16 * 16, 64), nn.ReLU(),
    nn.Linear(64, 4),                                  # 4 類 logits
)
x = torch.randn(8, 3, 64, 64)                          # (batch, channels, height, width)
model(x).shape                                         # torch.Size([8, 4])
```

> 不想手算 flatten 後的維度：用 `nn.AdaptiveAvgPool2d(1)` + `nn.Flatten()` + `nn.Linear(32, 4)`（輸入大小改變也能用），或 `nn.LazyLinear(64)`。

## 資料管線

```python
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import v2 as T

train_tf = T.Compose([
    T.RandomResizedCrop(224, scale=(0.8, 1.0)),
    T.RandomHorizontalFlip(),
    T.ToImage(), T.ToDtype(torch.float32, scale=True),           # 取代舊的 ToTensor()
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),   # ImageNet 統計量（用預訓練模型時）
])
eval_tf = T.Compose([
    T.Resize(256), T.CenterCrop(224),                            # 無隨機性
    T.ToImage(), T.ToDtype(torch.float32, scale=True),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
train_ds = datasets.ImageFolder("data/train", transform=train_tf)   # 子資料夾名稱 = 類別
train_loader = DataLoader(train_ds, batch_size=32, shuffle=True, num_workers=4)
```

訓練迴圈見 [PyTorch 訓練迴圈](../training-workflows/pytorch-training-loop.md)；資料少時直接用 [預訓練模型](../training-workflows/transfer-learning.md)，幾乎一定比從頭訓練好。

## 經典架構

| 架構 | 關鍵想法 | 現況 |
| --- | --- | --- |
| LeNet / AlexNet / VGG | 卷積 + pooling 堆疊；VGG 全用 3×3 | 教學用 |
| **ResNet** | 殘差連接 (residual connection)：$y = F(x) + x$，梯度可直接走捷徑 → 可訓練上百層 | 最常用的 baseline 骨幹 |
| EfficientNet / ConvNeXt | 系統化縮放深度、寬度、解析度 / 現代化 CNN 設計 | 準確率與效率兼顧 |
| U-Net | encoder-decoder + skip connection | 分割，見 [U-Net](u-net-segmentation.md) |
| Vision Transformer (ViT) | 影像切成 patch 當 token，用 [Transformer](../nlp-and-transformers/transformers-and-attention.md) | 大資料 / 大型預訓練時表現佳；病理基礎模型多採用 |

## 1D CNN：序列也能用

卷積不限於影像。DNA 序列 one-hot 成 `(4, L)` 後，用 `nn.Conv1d` 掃描，kernel 等同於可學習的 motif（PWM）偵測器：

```python
x = torch.randn(8, 4, 1000)                            # (batch, A/C/G/T, 序列長度)
nn.Conv1d(4, 64, kernel_size=19, padding="same")(x).shape   # torch.Size([8, 64, 1000])
```

詳見 [序列與蛋白模型](../bio-applications/sequence-and-protein-models.md)。

## 輸出與評估

| 項目 | 做法 |
| --- | --- |
| 預測類別 | `logits.argmax(dim=1)` |
| 類別機率 | `logits.softmax(dim=1)`；訓練時不要先 softmax（[CrossEntropyLoss](../fundamentals/loss-functions.md) 內含） |
| 評估 | 混淆矩陣、每類 recall、AUROC，見 [模型評估](../../machine-learning/evaluation/README.md) |
| 模型在看哪裡 | Grad-CAM 熱圖；可檢查是否依賴非病灶線索（尺標、文字標記、掃描儀邊框） |

## 常見錯誤

| 錯誤 | 說明 |
| --- | --- |
| `Linear` 維度不合 | 沒算對卷積 / pooling 後的尺寸；用上方公式或 adaptive pooling |
| 通道順序錯 | PyTorch 是 `(N, C, H, W)`；NumPy / PIL / Keras 常是 `(H, W, C)` → `permute(2, 0, 1)` |
| augmentation 也套在 validation | validation 只做 resize / normalize，不能有隨機變換 |
| 同一病人的影像跨 train / test | 依病人切分（見 [訓練迴圈](../training-workflows/pytorch-training-loop.md#資料切分dl-特有的陷阱)） |
| 捷徑學習 (shortcut learning) | 模型學到醫院、掃描儀或標記而非病灶；用外部醫院資料驗證、看 Grad-CAM |
| 樣本少卻從頭訓練深層 CNN | 嚴重過擬合；改用預訓練模型 |
