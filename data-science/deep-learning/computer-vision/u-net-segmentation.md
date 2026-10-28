[Deep Learning](../README.md) › [電腦視覺](README.md) › U-Net 影像分割

# U-Net 影像分割 (U-Net Segmentation)

分割 (segmentation) 要替每個像素給一個標籤：哪些像素是細胞核、哪些是腫瘤。U-Net（Ronneberger et al., 2015，原本就是為生醫影像設計）用「先壓縮再放大」的 encoder-decoder 結構，加上跨層的 skip connection 保留細節，至今仍是生醫影像分割的基本架構。

不訓練模型的閾值 / 分水嶺分割見 [影像分析](../../image-analysis/README.md)；資料量少、對比清楚時那些方法常已足夠。

## 架構

```
輸入 (1, 256, 256)                                              輸出 (K, 256, 256)
   │                                                                   ▲
   ▼ conv×2 ──────────────── skip（複製並串接）──────────────► conv×2   │
   ▼ pool ↓ 128                                                ↑ up 256
     conv×2 ──────────── skip ─────────────────────────► conv×2
     ▼ pool ↓ 64                                       ↑ up 128
       conv×2 ─────── skip ──────────────────► conv×2
       ▼ pool ↓ 32                           ↑ up 64
              bottleneck conv×2（最抽象、解析度最低）
  encoder（收縮路徑）：抓「是什麼」              decoder（擴張路徑）：放回「在哪裡」
```

| 部分 | 作用 |
| --- | --- |
| Encoder | 卷積 + pooling，解析度降低、通道數增加，學語意特徵；可直接換成預訓練的 ResNet |
| Decoder | 上採樣（`ConvTranspose2d` 或插值）回原解析度 |
| **Skip connection** | 把 encoder 同解析度的特徵圖串接到 decoder，補回 pooling 丟掉的邊界細節 |
| 輸出層 | `1×1` 卷積 → 每像素 K 個 logits |

## 最小實作

```python
import torch
from torch import nn

def block(c_in, c_out):
    return nn.Sequential(
        nn.Conv2d(c_in, c_out, 3, padding=1), nn.BatchNorm2d(c_out), nn.ReLU(inplace=True),
        nn.Conv2d(c_out, c_out, 3, padding=1), nn.BatchNorm2d(c_out), nn.ReLU(inplace=True),
    )

class UNet(nn.Module):
    def __init__(self, c_in=1, n_classes=2, base=32):
        super().__init__()
        self.enc1, self.enc2 = block(c_in, base), block(base, base * 2)
        self.bottleneck = block(base * 2, base * 4)
        self.up2, self.dec2 = nn.ConvTranspose2d(base * 4, base * 2, 2, stride=2), block(base * 4, base * 2)
        self.up1, self.dec1 = nn.ConvTranspose2d(base * 2, base, 2, stride=2), block(base * 2, base)
        self.head = nn.Conv2d(base, n_classes, 1)
        self.pool = nn.MaxPool2d(2)

    def forward(self, x):
        e1 = self.enc1(x)                                    # (N, 32, H, W)
        e2 = self.enc2(self.pool(e1))                        # (N, 64, H/2, W/2)
        b = self.bottleneck(self.pool(e2))                   # (N, 128, H/4, W/4)
        d2 = self.dec2(torch.cat([self.up2(b), e2], dim=1))  # skip：沿通道串接
        d1 = self.dec1(torch.cat([self.up1(d2), e1], dim=1))
        return self.head(d1)                                 # (N, K, H, W) logits

UNet()(torch.randn(2, 1, 128, 128)).shape                    # torch.Size([2, 2, 128, 128])
```

> 輸入邊長要能被 $2^{\text{下採樣次數}}$ 整除（這裡是 4），否則 skip 串接時尺寸對不上；先 padding 或裁切。實務上用現成套件（下方）而非自己寫。

## Loss：前景很少時用 Dice

細胞核或病灶常只佔幾 % 的像素。只用交叉熵時，全部預測背景也能得到很低的 loss。Dice 直接衡量預測與真實遮罩的重疊：

$$
\text{Dice} = \frac{2|P \cap G|}{|P| + |G|}, \qquad L_{\text{Dice}} = 1 - \frac{2\sum p_i g_i + \epsilon}{\sum p_i + \sum g_i + \epsilon}
$$

```python
import torch.nn.functional as F

def dice_loss(logits, target, eps=1.0):            # 二元：logits (N,1,H,W)，target 0/1 float
    p = torch.sigmoid(logits)
    inter = (p * target).sum(dim=(1, 2, 3))
    union = p.sum(dim=(1, 2, 3)) + target.sum(dim=(1, 2, 3))
    return 1 - ((2 * inter + eps) / (union + eps)).mean()

loss = F.binary_cross_entropy_with_logits(logits, target) + dice_loss(logits, target)   # 常見組合
```

## 評估指標

| 指標 | 定義 | 注意 |
| --- | --- | --- |
| Dice（= 像素層級 F1） | $2TP / (2TP + FP + FN)$ | 最常用；小物件上很敏感 |
| IoU / Jaccard | $TP / (TP + FP + FN)$ | Dice = 2·IoU / (1 + IoU) |
| Hausdorff 距離（HD95） | 邊界最大偏差（取 95 百分位） | 重視邊界精確度（放射治療勾畫） |
| 實例層級 AP / F1 | 以 IoU 門檻配對個別物件 | 細胞計數任務：兩個黏在一起的細胞被當成一個，像素 Dice 仍高 |

> 像素準確率 (pixel accuracy) 幾乎沒有意義：前景 2% 時全猜背景就有 98%。和 [類別不平衡](../../machine-learning/evaluation/class-imbalance.md) 是同一個問題。

## 生醫影像實務

| 議題 | 做法 |
| --- | --- |
| 影像太大（全切片、3D 體積） | 切成重疊的 patch / tile 訓練與推論，再拼回（重疊區取平均避免邊緣效應） |
| 3D 影像（CT、MRI、共軛焦 z-stack） | 3D U-Net（`Conv3d`）；記憶體吃緊時用 2.5D（相鄰切片當通道） |
| 標註昂貴 | 預訓練 encoder、半自動標註再人工修正（Cellpose 的 human-in-the-loop）、只標部分切片 |
| 相鄰細胞要分開 | 實例分割：預測距離圖 / 流場再後處理（StarDist、Cellpose），而非單純前景遮罩 |
| 不同醫院 / 染色 / 掃描儀 | augmentation（強度、彈性變形）、stain normalization；在外部資料驗證 |
| 切分 | 以病人 / 樣本為單位，同一張切片的 patch 不能跨 train / test |

## 現成工具

| 工具 | 用途 | 何時用 |
| --- | --- | --- |
| **nnU-Net** | 依資料集自動決定前處理、架構、訓練設定的 U-Net 框架 | 醫學影像（CT、MRI）語意分割的強 baseline，通常先試它 |
| **Cellpose** | 通用細胞 / 細胞核實例分割，有預訓練模型 | 顯微影像細胞分割，常不需重新訓練 |
| **StarDist** | 以星形多邊形表示物件的細胞核分割 | 圓形 / 凸形細胞核 |
| MONAI | PyTorch 的醫學影像函式庫（3D transforms、Dice loss、U-Net、滑動視窗推論） | 自建醫學影像流程 |
| `segmentation_models_pytorch` | 各種 encoder（ResNet、EfficientNet）+ U-Net 等 decoder | 2D 自然 / 病理影像，快速換骨幹 |
