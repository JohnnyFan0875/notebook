[Deep Learning](../README.md) › [訓練流程](README.md) › 高效訓練與擴展

# 高效訓練與擴展 (Efficient Training and Scaling)

模型或資料變大後，瓶頸會出現在 GPU 記憶體、資料讀取速度或單卡算力。前提是訓練邏輯先正確：loss、指標、資料切分、checkpoint 都穩了再加速，否則只是更快地訓練出錯誤的模型。

## 先找瓶頸

| 症狀 | 瓶頸 | 優先處理 |
| --- | --- | --- |
| `CUDA out of memory` | GPU 記憶體 | 混合精度 → 降 batch + gradient accumulation → gradient checkpointing |
| GPU 使用率（`nvidia-smi`）長期很低 | 資料讀取 | `num_workers`、`pin_memory`、預先轉檔（HDF5、Zarr、WebDataset） |
| GPU 滿載但仍太慢 | 計算量 | 混合精度、`torch.compile`、多 GPU |
| 每個 epoch 時間很長、中途常失敗 | 流程 | 定期存 [checkpoint](model-saving-loading.md#checkpoint續訓)，HPC 上配合排程器的時間上限 |

## 混合精度 (Mixed Precision)

大部分運算用 16-bit，必要處（loss、累加）保留 32-bit：記憶體約減半、支援的 GPU 上速度大幅提升。

| 格式 | 數值範圍 | 需要 `GradScaler` | 硬體 |
| --- | --- | --- | --- |
| `float16` | 小，梯度容易下溢成 0 | 是 | 多數 NVIDIA GPU |
| **`bfloat16`** | 與 float32 相同 | 否 | Ampere（A100、RTX 30 系列）以後；優先使用 |

```python
import torch
from torch import nn

device = "cuda"
model = model.to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
scaler = torch.amp.GradScaler("cuda")               # 取代舊的 torch.cuda.amp.GradScaler()（已棄用）

for x, y in train_loader:
    x, y = x.to(device, non_blocking=True), y.to(device, non_blocking=True)
    optimizer.zero_grad()
    with torch.autocast(device_type="cuda", dtype=torch.float16):   # 取代 torch.cuda.amp.autocast()
        loss = nn.functional.cross_entropy(model(x), y)
    scaler.scale(loss).backward()                    # 放大 loss，避免 fp16 梯度下溢
    scaler.unscale_(optimizer)                       # 要做 gradient clipping 時先 unscale
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    scaler.step(optimizer)
    scaler.update()

# bfloat16：不需要 scaler
with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
    loss = nn.functional.cross_entropy(model(x), y)
loss.backward(); optimizer.step()
```

## Gradient Accumulation

GPU 只放得下小 batch，但想要大 batch 的效果：累積多個小 batch 的梯度再更新一次。

```python
accum = 4                                            # 等效 batch = batch_size × 4
optimizer.zero_grad()
for i, (x, y) in enumerate(train_loader):
    loss = criterion(model(x.to(device)), y.to(device)) / accum   # 除以步數，梯度才是平均
    loss.backward()
    if (i + 1) % accum == 0:
        optimizer.step()
        optimizer.zero_grad()
```

> BatchNorm 仍只看到小 batch，accumulation 無法改善它的統計量；小 batch 時考慮 GroupNorm / LayerNorm（見 [Normalization](../fundamentals/regularization-and-normalization.md#batchnorm-vs-layernorm)）。

## 其他技巧

| 技巧 | 效果 | 用法 |
| --- | --- | --- |
| `torch.compile` | 編譯成融合的 kernel，常見 1.3～2 倍加速 | `model = torch.compile(model)`（PyTorch ≥ 2.0；Windows 支援較有限） |
| Gradient checkpointing | 不存中間 activation、backward 時重算；省記憶體、多花約 20～30% 時間 | `torch.utils.checkpoint.checkpoint`；Hugging Face 模型 `model.gradient_checkpointing_enable()` |
| `non_blocking=True` + `pin_memory=True` | CPU → GPU 傳輸與計算重疊 | 見上方程式 |
| 預先計算 embedding | 凍結骨幹時，embedding 只需算一次存起來 | 見 [遷移學習](transfer-learning.md) |
| `optimizer.zero_grad(set_to_none=True)` | 少一次記憶體寫入（新版已是預設） | — |

## 多 GPU 與框架

| 方式 | 說明 |
| --- | --- |
| `DistributedDataParallel` (DDP) | 每張 GPU 一份模型、各吃不同資料、同步梯度；多 GPU 的標準做法（`torchrun --nproc_per_node=4 train.py`） |
| `DataParallel` | 舊做法、單程序，較慢，不建議 |
| FSDP | 把參數、梯度、optimizer 狀態切分到各 GPU；模型大到單卡放不下時 |
| Hugging Face `Accelerate` | 同一份訓練迴圈切換單卡 / 多卡 / 混合精度，改動最少 |
| PyTorch Lightning | 把訓練迴圈結構化成 `LightningModule`，由 `Trainer` 處理裝置、精度、checkpoint、logging |

> 多 GPU 訓練後結果改變時，檢查：有效 batch size 變大（學習率是否要跟著調）、各程序的 seed、BatchNorm 是否要用 `SyncBatchNorm`、validation 指標是否在所有程序間正確彙總。

在 HPC 叢集上提交 GPU 工作（Slurm `--gres=gpu:1`）、管理 conda / 容器環境見 [容器與環境](../../../computing/containers-and-env/README.md)。
