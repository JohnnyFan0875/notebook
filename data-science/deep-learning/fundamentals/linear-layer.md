[Deep Learning](../README.md) › [基礎](README.md) › 線性層

# 線性層 (Linear Layer)

線性層（又稱全連接層 fully connected、dense layer）對輸入做一次仿射轉換，是多層感知器 (MLP) 的基本單元，也是 CNN、Transformer 最後的分類頭。

$$
Y = XW^\top + b
$$

| 符號 | shape | 意義 |
| --- | --- | --- |
| $X$ | `(batch, in_features)` | 一批輸入 |
| $W$ | `(out_features, in_features)` | 權重；PyTorch 存的是轉置前的形狀 |
| $b$ | `(out_features,)` | 偏差 (bias) |
| $Y$ | `(batch, out_features)` | 輸出 |

單一線性層就是 [線性迴歸](../../statistics/regression-analysis/simple-linear-regression.md) / [logistic 迴歸](../../statistics/regression-analysis/logistic-regression.md)的線性部分；疊很多層但不加 [激活函數](activation-functions.md)，整體仍只是一個線性轉換。

## 手算一次

```python
import torch
from torch import nn

layer = nn.Linear(2, 3)
with torch.no_grad():                       # 手動設定參數時不要被 autograd 記錄
    layer.weight.copy_(torch.tensor([[ 0.5, -0.3],
                                     [ 0.2,  0.8],
                                     [-0.7,  0.4]]))
    layer.bias.copy_(torch.tensor([0.1, -0.2, 0.3]))

x = torch.tensor([[2.0, 3.0]])              # 必須是 float；整數輸入會報 dtype 錯誤
layer(x)                                    # tensor([[0.2000, 2.6000, 0.1000]])
```

| 輸出神經元 | $x \cdot w_j$ | + bias | 結果 |
| --- | --- | --- | --- |
| 1 | 2×0.5 + 3×(−0.3) = 0.1 | +0.1 | **0.2** |
| 2 | 2×0.2 + 3×0.8 = 2.8 | −0.2 | **2.6** |
| 3 | 2×(−0.7) + 3×0.4 = −0.2 | +0.3 | **0.1** |

## 參數量

每個輸出神經元有 `in_features` 個權重 + 1 個 bias：參數量 = `out × (in + 1)`。

```python
model = nn.Sequential(nn.Linear(10, 18), nn.Linear(18, 5))
# 第 1 層 18 × (10 + 1) = 198；第 2 層 5 × (18 + 1) = 95
sum(p.numel() for p in model.parameters())                     # 293
sum(p.numel() for p in model.parameters() if p.requires_grad)  # 只算可訓練的（凍結層之後有差）
```

> 生資常見的「20,000 個基因 → 512 個隱藏單元」第一層就有約 1,000 萬個參數，樣本卻只有幾百個——這是 [高維小樣本](../../machine-learning/foundations/high-dimensional-data.md) 問題，需要強正則化、先降維或改用預訓練表示。

## 實務提醒

| 項目 | 說明 |
| --- | --- |
| 預設初始化 | `nn.Linear` 建立時已隨機初始化；自訂方式見 [權重初始化](weight-initialization.md) |
| 不知道輸入維度 | `nn.LazyLinear(out_features)` 會在第一次 forward 時推斷 `in_features`（CNN flatten 後常用） |
| 輸出層 | 分類輸出維度 = 類別數，**不加 softmax**（loss 內含），見 [損失函數](loss-functions.md) |
| 層與層之間 | 加非線性（ReLU、GELU），否則多層等於一層 |
