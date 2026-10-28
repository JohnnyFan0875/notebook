[Deep Learning](../README.md) › [訓練流程](README.md) › 模型存檔與載入

# 模型存檔與載入 (Saving and Loading Models)

存模型有兩個目的：**推論 / 分享**（只要權重）和**續訓**（還要 optimizer、scheduler、epoch 等狀態）。PyTorch 推薦存 `state_dict`（參數字典），而不是整個模型物件。

## 兩種方式

| 方式 | 存了什麼 | 優點 | 缺點 |
| --- | --- | --- | --- |
| **`state_dict`**（推薦） | 參數名稱 → tensor 的字典 | 與程式碼版本解耦、可安全載入 | 載入時要先用程式碼建立同樣架構 |
| 整個模型 `torch.save(model)` | pickle 整個物件 | 一行搞定 | 依賴原始類別定義與檔案路徑；PyTorch ≥ 2.6 預設拒絕載入 |

## 只存權重（推論、分享）

```python
import torch
from torch import nn

def build_model():
    return nn.Sequential(nn.Linear(10, 16), nn.ReLU(), nn.Linear(16, 2))

model = build_model()
torch.save(model.state_dict(), "model.pt")

# 載入：先建立相同架構，再填入權重
model = build_model()
model.load_state_dict(torch.load("model.pt", map_location="cpu"))   # GPU 上存的檔案在 CPU 機器也能載
model.eval()                                                         # 推論前必做
```

## Checkpoint（續訓）

```python
# 存
torch.save({
    "epoch": epoch,
    "model": model.state_dict(),
    "optimizer": optimizer.state_dict(),     # Adam 的動量狀態；沒存的話續訓會像重新開始
    "scheduler": scheduler.state_dict(),
    "best_val_loss": best_loss,
    "config": {"lr": 1e-3, "hidden": 16, "seed": 42},   # 重建模型所需的設定
}, f"ckpt_epoch{epoch}.pt")

# 讀
ckpt = torch.load("ckpt_epoch10.pt", map_location=device)
model.load_state_dict(ckpt["model"])
optimizer.load_state_dict(ckpt["optimizer"])
scheduler.load_state_dict(ckpt["scheduler"])
start_epoch = ckpt["epoch"] + 1
model.train()
```

## `weights_only`（PyTorch 2.6 起的改變）

`torch.load` 底層用 pickle，載入不明來源的檔案可能執行任意程式碼。PyTorch 2.6 起 `weights_only=True` 成為預設，只允許 tensor、基本型別與字典。

| 載入的內容 | 結果 |
| --- | --- |
| `state_dict`、含 tensor / 數字 / 字串的 checkpoint 字典 | 正常 |
| `torch.save(model)` 存的整個模型 | `UnpicklingError`；只有**信任來源**時才用 `weights_only=False` |
| checkpoint 裡有 NumPy 陣列、自訂物件 | 可能報錯 → 改存成 tensor 或基本型別 |

> 下載別人的模型時，優先選 `safetensors` 格式（Hugging Face 預設）：純權重、不能夾帶程式碼、載入更快。

## 部署格式

| 格式 | 用途 |
| --- | --- |
| `state_dict` (`.pt`) | 研究、同一套程式碼內使用 |
| `safetensors` | 分享權重（Hugging Face Hub） |
| `torch.export` / TorchScript | 脫離 Python 原始碼執行（TorchScript 已不再積極開發，新專案用 `torch.export`） |
| ONNX（`torch.onnx.export`） | 跨框架、跨語言推論（ONNX Runtime） |

上線、版本管理與監控見 [ML：上線與維運](../../machine-learning/production/README.md)；模型與資料版本一起追蹤見 [DVC](../../machine-learning/production/dvc.md)。

## 常見錯誤

| 現象 | 原因 | 修正 |
| --- | --- | --- |
| `Missing key(s)` / `Unexpected key(s)` | 架構不同，或多 GPU 訓練的參數名多了 `module.` 前綴 | 對齊架構；去掉前綴，或 `strict=False`（確認缺的是什麼再用） |
| 推論結果每次不同 / 偏低 | 忘了 `model.eval()` | 載入後呼叫 `eval()` |
| 續訓後 loss 突然跳高 | 沒載 optimizer / scheduler 狀態 | checkpoint 一起存 |
| `RuntimeError: Attempting to deserialize object on a CUDA device` | GPU 存的檔在 CPU 機器載入 | `map_location="cpu"` |
| 存了最後一個 epoch，不是最好的 | 沒有依 validation 指標存最佳 | 見 [early stopping](pytorch-training-loop.md#early-stopping) |
