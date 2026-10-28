[Deep Learning](../README.md) › [基礎](README.md) › 損失函數

# 損失函數 (Loss Functions in PyTorch)

損失函數把「預測錯多少」變成一個可微分的數字，[反向傳播](backpropagation.md) 再依它的梯度更新權重。這篇講 PyTorch 的 API 與輸入格式；依任務選 loss、loss ↔ MLE、訓練損失 vs 評估指標見 [ML：損失函數](../../machine-learning/foundations/loss-functions.md)。

## 速查表

| 任務 | Loss | PyTorch | 模型輸出 | 標籤 |
| --- | --- | --- | --- | --- |
| 多類別單選 | 交叉熵 (cross-entropy) | `nn.CrossEntropyLoss()` | logits `(N, K)` | 類別索引 `(N,)`，`int64` |
| 二元 / 多標籤 | 二元交叉熵 (BCE) | `nn.BCEWithLogitsLoss()` | logits `(N,)` 或 `(N, K)` | 0 / 1，`float` |
| 迴歸 | 均方誤差 (MSE) | `nn.MSELoss()` | 實數 | 實數 |
| 迴歸（有離群值） | MAE / Huber | `nn.L1Loss()`、`nn.HuberLoss()` | 實數 | 實數 |
| 計數（reads、UMI） | Poisson NLL | `nn.PoissonNLLLoss()` | log 率（預設 `log_input=True`） | 計數 |
| 分布對齊（VAE、蒸餾） | KL 散度 | `nn.KLDivLoss(reduction="batchmean")` | **log 機率** | 機率 |
| 分割 | Dice / BCE + Dice | 自訂或 MONAI | 每像素 logits | 遮罩 |

> **最常見的錯**：`CrossEntropyLoss` 內部已經做 `log_softmax`，模型最後不要再接 `nn.Softmax`；`BCEWithLogitsLoss` 內含 sigmoid，比 `Sigmoid + BCELoss` 數值更穩定。疊兩次 softmax 不會報錯，但梯度變小、訓練變慢。

## 交叉熵 (Cross-Entropy)

$$
L = -\frac{1}{N}\sum_{i=1}^{N} \log p_{i, y_i}, \qquad p_i = \text{softmax}(z_i)
$$

只看正確類別的機率；正確類別機率越接近 1，loss 越接近 0。等於多項分布的負對數似然。

```python
import torch
from torch import nn

logits = torch.tensor([[2.1, -1.4, 0.8],
                       [1.2,  0.3, 1.8]])
target = torch.tensor([0, 2])                       # 類別索引，不是 one-hot

nn.CrossEntropyLoss()(logits, target)               # tensor(0.4183)
nn.CrossEntropyLoss(reduction="none")(logits, target)   # tensor([0.2645, 0.5721])
logits.softmax(dim=1)
# [[0.7676, 0.0232, 0.2092],
#  [0.3097, 0.1259, 0.5644]]
```

| 樣本 | 正確類別 | $p_y$ | $-\log p_y$ |
| --- | --- | --- | --- |
| 1 | 0 | 0.768 | 0.264 |
| 2 | 2 | 0.564 | 0.572 |
| 平均 | | | **0.418** |

常用參數：

| 參數 | 用途 |
| --- | --- |
| `weight=torch.tensor([...])` | 類別加權，處理 [類別不平衡](../../machine-learning/evaluation/class-imbalance.md) |
| `label_smoothing=0.1` | 目標從 one-hot 改成 0.9 / 0.1 分攤，減少過度自信 |
| `ignore_index=-100` | 跳過 padding token 或未標註像素 |
| `reduction="none"` | 回傳每個樣本的 loss（自訂加權、找難樣本） |

## 二元交叉熵 (BCE)

$$
L = -\frac{1}{N}\sum_i \big[y_i \log p_i + (1-y_i)\log(1-p_i)\big], \qquad p_i = \sigma(z_i)
$$

```python
logits = torch.tensor([2.2, -1.4, 1.4])
y = torch.tensor([1.0, 0.0, 1.0])                   # float
nn.BCEWithLogitsLoss()(logits, y)

# 正樣本稀少（如罕見變異致病）：pos_weight = 負樣本數 / 正樣本數
nn.BCEWithLogitsLoss(pos_weight=torch.tensor([9.0]))

# 多標籤：一個樣本可同時屬於多類（如一個蛋白質有多個 GO term）
# logits (N, K)、y (N, K) 的 0/1 矩陣，每一欄各自是一個二元問題
```

## 迴歸損失

```python
pred = torch.tensor([2.5, 0.0, 2.0])
target = torch.tensor([3.0, -0.5, 2.0])
nn.MSELoss()(pred, target)       # tensor(0.1667)  (0.25 + 0.25 + 0) / 3
nn.L1Loss()(pred, target)        # tensor(0.3333)
nn.HuberLoss(delta=1.0)(pred, target)   # 誤差小時像 MSE、大時像 MAE
```

> 計數資料（RNA-seq reads、UMI）直接用 MSE 會被高表現基因主導；常見做法是預測 log1p 後的值，或像 [scVI](../bio-applications/single-cell-deep-learning.md) 一樣直接用負二項 (negative binomial) 似然當 loss——與 [GLM 計數模型](../../statistics/regression-analysis/glm-count-models.md) 是同一個觀念。

## 其他

| Loss | 說明 |
| --- | --- |
| Hinge | SVM 用；PyTorch 有多類別版本 `nn.MultiMarginLoss()`，深度學習很少用 |
| `nn.CosineEmbeddingLoss`、`nn.TripletMarginLoss` | 度量學習 (metric learning)：讓相似樣本 embedding 靠近 |
| Contrastive (InfoNCE) | 自監督預訓練（CLIP 等）；通常寫成對相似度矩陣做 `CrossEntropyLoss` |
| 多個 loss 加權相加 | 多任務學習、VAE（重建 + KL）；權重是超參數 |
