# Efficient Training and Scaling

`notebook_temp/output` 裡的 `Efficient AI Model Training with PyTorch`、`Scalable AI Models with PyTorch Lightning` 等內容，核心其實都在回答同一件事：模型變大之後，怎麼在不破壞訓練正確性的前提下，把速度、記憶體與可維護性顧好。

## 先從最有感的優化開始

1. **DataLoader**：設定合適的 `batch_size`、`num_workers`、`pin_memory`
2. **device management**：明確把 model 與 tensor 移到同一個裝置
3. **mixed precision**：在支援的硬體上降低記憶體用量、提高吞吐量
4. **gradient accumulation**：當 GPU 放不下大 batch 時，用多步累積模擬
5. **checkpointing**：長訓練過程一定要可恢復

## 一個實用的 mixed precision 範例

```python
import torch
from torch import nn, optim

model = nn.Linear(128, 2).to("cuda")
optimizer = optim.Adam(model.parameters(), lr=1e-3)
scaler = torch.cuda.amp.GradScaler()

for inputs, targets in train_loader:
    inputs = inputs.to("cuda")
    targets = targets.to("cuda")

    optimizer.zero_grad()

    with torch.cuda.amp.autocast():
        outputs = model(inputs)
        loss = nn.CrossEntropyLoss()(outputs, targets)

    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

## 什麼時候該考慮 scaling 工具

- 單卡 GPU 記憶體不足
- 訓練時間長到中途失敗成本很高
- 需要多卡、多節點，或要更標準化地管理訓練 loop
- 要把訓練流程交給團隊其他人維護，而不是只靠單一 notebook

## 常見工具與用途

| 工具/方法 | 主要目的 |
| --- | --- |
| `torch.cuda.amp` | mixed precision |
| `torch.utils.data.DataLoader` | 穩定地批次載入資料 |
| gradient accumulation | 在固定記憶體下等效放大 batch |
| Hugging Face `Accelerate` | 簡化多裝置與混合精度訓練 |
| PyTorch Lightning | 把訓練 loop 結構化、模組化 |

## 常見錯誤

- 一看到 GPU 不夠就先調很大的 batch，結果 OOM。
- mixed precision 開了，卻沒有檢查數值穩定性。
- 只追求吞吐量，卻沒保留足夠的 validation 與 checkpoint。
- 多卡訓練後分數變了，卻沒有確認 random seed、batch norm、gradient sync 等差異。

## 小結

效率優化的前提永遠是訓練邏輯先正確。先確認 loss、metric、資料管線與 checkpoint 都穩，再做加速；否則你只是在更快地訓練出錯誤模型。
