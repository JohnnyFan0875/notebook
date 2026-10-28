[Deep Learning](../README.md) › [基礎](README.md) › Tensor

# 張量 (Tensors in PyTorch)

Tensor 是 PyTorch 的基本資料結構：和 NumPy 陣列幾乎相同，多了兩件事——可以放到 GPU、可以自動微分 (autograd)。shape、broadcasting、索引規則與 [NumPy](../../python-foundations/numpy/README.md) 一致。

## 三個屬性

| 屬性 | 意義 | 常見問題 |
| --- | --- | --- |
| `shape` | 各維度大小 | 影像 `(N, C, H, W)`、序列 `(N, L, D)`；維度錯位是最常見的錯 |
| `dtype` | 資料型別 | 模型權重是 `float32`；分類標籤要 `int64`（`long`） |
| `device` | 在 CPU 還是 GPU | 模型與輸入必須在同一裝置，否則報錯 |

## 建立與操作

```python
import numpy as np
import torch

# 1. 建立
t = torch.tensor([[1., 2.], [3., 4.]])          # 從 list；有小數點 → float32
torch.zeros(2, 3); torch.ones(2, 3); torch.eye(3)
torch.rand(2, 3)                                 # U(0, 1)
torch.randn(2, 3)                                # N(0, 1)
torch.arange(0, 10, 2)                           # tensor([0, 2, 4, 6, 8])
torch.zeros_like(t)                              # 同 shape / dtype / device

# 2. 屬性與轉換
t.shape, t.dtype, t.device                       # torch.Size([2, 2]) torch.float32 cpu
t.to(torch.float16); t.long()                    # 改 dtype
device = "cuda" if torch.cuda.is_available() else "cpu"   # Apple 晶片可用 "mps"
t = t.to(device)

# 3. 運算
a = b = torch.tensor([[1., 2.], [3., 4.]])
a * b                                            # 逐元素
a @ b                                            # 矩陣乘法 = torch.matmul
a.T; a.sum(dim=0); a.mean(dim=1, keepdim=True)   # dim=0 沿列方向壓縮
a[0, :]; a[:, 1]                                 # 索引同 NumPy

# 4. 改形狀
x = torch.arange(6)
x.reshape(2, 3)                                  # 必要時會複製
x.view(2, 3)                                     # 不複製；非連續記憶體（如 .T 之後）會報錯
x.unsqueeze(0).shape                             # torch.Size([1, 6])   加 batch 維
torch.cat([a, b], dim=0).shape                   # torch.Size([4, 2])
torch.stack([a, b]).shape                        # torch.Size([2, 2, 2])  新增一維
```

## 自動微分 (Autograd)

`requires_grad=True` 的 tensor 會記錄運算圖，`backward()` 時用鏈鎖律算出梯度，存在 `.grad`。

```python
x = torch.tensor(2.0, requires_grad=True)
y = x**2 + 3*x + 1
y.backward()
x.grad                          # tensor(7.)   dy/dx = 2x + 3 = 7

# 推論、評估時關掉梯度追蹤：省記憶體、加速
with torch.no_grad():
    z = x * 2
x.detach()                      # 取出不追蹤梯度的副本（共享記憶體）
```

訓練迴圈中梯度如何流動見 [反向傳播](backpropagation.md)。

## 與 NumPy 互轉

```python
arr = np.array([1.0, 2.0])
t = torch.from_numpy(arr)        # 共享記憶體：改 arr，t 也會變
t.dtype                          # torch.float64 ← NumPy 預設 float64
t = torch.from_numpy(arr).float()   # 送進模型前轉 float32，否則 dtype 不合

out.detach().cpu().numpy()       # 模型輸出 → NumPy：先脫離運算圖、搬回 CPU
```

## 常見錯誤

| 錯誤訊息 / 現象 | 原因 | 修正 |
| --- | --- | --- |
| `mat1 and mat2 must have the same dtype` | 輸入是 `float64`（來自 NumPy / pandas）或整數 | `.float()` |
| `expected scalar type Long` | `CrossEntropyLoss` 的標籤是 float | 標籤 `.long()` |
| `Expected all tensors to be on the same device` | 模型在 GPU、輸入在 CPU | 兩者都 `.to(device)` |
| `Can't call numpy() on Tensor that requires grad` | 還連著運算圖 | `.detach().cpu().numpy()` |
| `view size is not compatible` | 記憶體不連續 | 改用 `reshape` 或先 `.contiguous()` |
| 結果每次不同 | 未固定 seed | `torch.manual_seed(42)`；完整可重現設定見 [訓練迴圈](../training-workflows/pytorch-training-loop.md#可重現性) |

> 能向量化就不要寫 Python 迴圈逐元素處理 tensor；GPU 的速度來自一次處理整批資料。
