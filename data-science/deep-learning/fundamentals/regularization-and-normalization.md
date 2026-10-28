[Deep Learning](../README.md) › [基礎](README.md) › 正則化與 Normalization

# 正則化與 Normalization (Regularization and Normalization)

深度網路參數常比樣本多很多，幾乎一定能把訓練集背下來。正則化限制模型「背答案」的能力；normalization 讓每層輸入的尺度穩定，深層網路才訓練得動。兩者常一起出現，但目的不同。

統計觀點的正則化（L1 / L2 ↔ 先驗）見 [ML：正則化](../../machine-learning/foundations/regularization.md)。

## 方法總覽

| 方法 | 類型 | 做什麼 | 常見設定 |
| --- | --- | --- | --- |
| Weight decay | 正則化 | 每步把權重往 0 拉 | AdamW `weight_decay=0.01`～`0.1` |
| Dropout | 正則化 | 訓練時隨機把神經元輸出設 0 | MLP 0.2～0.5；Transformer 0.1 |
| Early stopping | 正則化 | validation loss 不再進步就停 | 見 [訓練迴圈](../training-workflows/pytorch-training-loop.md#early-stopping) |
| Data augmentation | 正則化 | 對輸入做保持標籤不變的變換 | 影像翻轉、裁切；DNA 反向互補 |
| BatchNorm | normalization | 用 **batch 內**的平均 / 標準差標準化每個特徵 | CNN 每個 conv 後 |
| LayerNorm | normalization | 用**單一樣本內**所有特徵標準化 | Transformer、RNN |
| 小模型 / 預訓練 | 兩者皆非 | 減少要學的參數 | 樣本少時最有效 |

## Weight Decay

每次更新時額外把權重乘上 $(1 - \eta\lambda)$。在 SGD 下等價於 loss 加上 L2 懲罰 $\frac{\lambda}{2}\lVert w\rVert^2$（↔ 權重的常態先驗）；在 Adam 下兩者不等價，所以要用 **AdamW**。

```python
import torch
from torch import nn

# bias 與 normalization 層的參數通常不做 weight decay
decay, no_decay = [], []
for name, p in model.named_parameters():
    (no_decay if p.ndim == 1 else decay).append(p)
optimizer = torch.optim.AdamW([
    {"params": decay, "weight_decay": 0.01},
    {"params": no_decay, "weight_decay": 0.0},
], lr=1e-3)
```

## Dropout

訓練時每個神經元以機率 p 被丟掉，剩下的輸出乘上 $1/(1-p)$ 保持期望值不變；推論時不丟。效果類似同時訓練許多子網路再平均（ensemble）。

```python
model = nn.Sequential(
    nn.Linear(2000, 256), nn.ReLU(), nn.Dropout(p=0.5),
    nn.Linear(256, 2),
)

model.train()   # dropout 生效
model.eval()    # dropout 關閉；評估、推論前一定要切換
```

> 忘記 `model.eval()` 是最常見的 bug：每次推論結果都不同、validation 分數偏低。反過來，**刻意**在推論時開著 dropout 跑多次取變異，就是 MC dropout，可粗估預測不確定性。

## BatchNorm vs LayerNorm

對一個 `(batch N, features D)` 的輸入：

```
BatchNorm：每個特徵 d，用這個 batch 的 N 個值算 μ, σ     → 沿 batch 方向標準化
LayerNorm：每個樣本 n，用它自己的 D 個特徵算 μ, σ        → 沿特徵方向標準化
兩者之後都乘上可學習的 γ、加上 β
```

| 項目 | BatchNorm | LayerNorm |
| --- | --- | --- |
| 統計量來源 | batch 內的樣本 | 單一樣本內的特徵 |
| train / eval 行為 | **不同**：訓練用 batch 統計量並更新 running mean / var；eval 用 running 值 | 相同 |
| 對 batch size 敏感 | 是；batch < 8 時統計量雜訊大 | 否 |
| 常用於 | CNN（`nn.BatchNorm2d`） | Transformer、RNN、序列長度不一的資料 |
| 小 batch 的替代 | GroupNorm（`nn.GroupNorm`） | — |

```python
nn.Sequential(nn.Conv2d(3, 32, 3, padding=1, bias=False),   # 後接 BN 時 conv 的 bias 多餘
              nn.BatchNorm2d(32), nn.ReLU())
nn.LayerNorm(512)                                            # 對最後一維（d_model）標準化
```

> BatchNorm 的陷阱：(1) 3D 醫學影像或高解析度顯微影像常只能放 batch 1～2，BN 統計量不可靠，改用 GroupNorm / InstanceNorm；(2) [遷移學習](../training-workflows/transfer-learning.md) 凍結骨幹時，BN 層若仍在 train 模式，running 統計量會被新資料改掉；(3) 若一個 batch 全來自同一批次 (batch effect) 的樣本，BN 會把批次差異一起標準化掉，評估時行為又不同。

## Data Augmentation

只對**訓練集**做，而且變換後標籤必須不變。

| 資料 | 合理的 augmentation | 要小心 |
| --- | --- | --- |
| 自然影像 | 水平翻轉、隨機裁切、色彩抖動 | — |
| 顯微影像 | 90° 旋轉、翻轉、亮度 / 對比、彈性變形 | 染色差異大時考慮 stain normalization |
| 醫學影像（X 光、CT） | 小角度旋轉、平移、強度縮放 | 左右翻轉會改變解剖側別（心臟位置） |
| DNA 序列 | 反向互補 (reverse complement)、小幅平移 | 有方向性的訊號（轉錄方向）不能隨意反轉 |
| 表現量 / 表格 | 少用；可加小雜訊、mixup | 容易產生不真實的樣本 |

## 過擬合時的處理順序

```
validation loss 上升、train loss 持續下降
  ├─ 先確認不是資料洩漏或切分錯誤（同一病人 / 同源序列跨 train/val）
  ├─ 有預訓練模型？ → 遷移學習 / 只抽 embedding
  ├─ early stopping + weight decay
  ├─ augmentation（影像、序列）
  ├─ dropout、縮小模型
  └─ 收集更多資料（通常最有效）
```

學習曲線判讀見 [過擬合與欠擬合](../../machine-learning/foundations/overfitting-underfitting.md)。
