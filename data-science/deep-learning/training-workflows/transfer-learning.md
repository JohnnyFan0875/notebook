[Deep Learning](../README.md) › [訓練流程](README.md) › 遷移學習

# 遷移學習 (Transfer Learning)

拿在大型資料上預訓練好的模型，改用在自己的任務。前幾層學到的通用特徵（影像的邊緣與紋理、蛋白質序列的演化約束）可以直接沿用，只需少量標註資料就能訓練。生資資料常只有幾百個樣本，遷移學習通常是**第一個該試的做法**。

## 三種策略

| 策略 | 做法 | 適合 |
| --- | --- | --- |
| 抽 embedding（feature extraction） | 預訓練模型只做推論，輸出向量接 logistic 迴歸 / 隨機森林 | 樣本極少（幾十～幾百）、算力有限；也是最好的 baseline |
| 凍結骨幹、訓練新分類頭 | 骨幹 `requires_grad=False`，只訓練最後一層 | 資料少、與預訓練任務相近 |
| Fine-tuning | 全部或後幾層一起訓練，學習率小 | 資料較多、或與預訓練資料差異大（自然影像 → 病理切片） |
| 參數高效微調（LoRA 等） | 只訓練少量新增參數 | 大型 Transformer；見 [LLM：Fine-Tuning](../../llm/integration/fine-tuning.md) |

```
資料量 ↑
  │  與預訓練資料「相似」         與預訓練資料「不同」
  │  ───────────────────────     ─────────────────────────
多 │  fine-tune 全部              fine-tune 全部（或從頭訓練）
少 │  凍結骨幹 + 新分類頭          抽 embedding 接簡單模型；fine-tune 後幾層
```

## 影像：torchvision

```python
import torch
from torch import nn
from torchvision.models import resnet50, ResNet50_Weights

weights = ResNet50_Weights.DEFAULT                 # 取代舊的 pretrained=True（已棄用）
model = resnet50(weights=weights)
preprocess = weights.transforms()                  # 預訓練時用的 resize / normalize，推論要一致

# 1. 凍結骨幹
for p in model.parameters():
    p.requires_grad = False

# 2. 換分類頭（新建的層預設 requires_grad=True）
model.fc = nn.Linear(model.fc.in_features, 3)

# 3. optimizer 只收可訓練參數
optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=1e-3)

# 4. 之後要 fine-tune：解凍最後一個 stage，用分層學習率
for p in model.layer4.parameters():
    p.requires_grad = True
optimizer = torch.optim.AdamW([
    {"params": model.layer4.parameters(), "lr": 1e-5},
    {"params": model.fc.parameters(),     "lr": 1e-3},
])
```

## 序列：Hugging Face

```python
from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification

name = "facebook/esm2_t12_35M_UR50D"               # 蛋白質語言模型；文字任務換成 BERT 類模型即可

# 1. 抽 embedding（不訓練）
tok, enc = AutoTokenizer.from_pretrained(name), AutoModel.from_pretrained(name).eval()
with torch.no_grad():
    out = enc(**tok(["MKTAYIAKQR"], return_tensors="pt"))
emb = out.last_hidden_state.mean(dim=1)            # 對 token 平均 → 每條序列一個向量（不同長度時要排除 padding）

# 2. 加分類頭整個 fine-tune
clf = AutoModelForSequenceClassification.from_pretrained(name, num_labels=2)
```

蛋白質 / DNA 預訓練模型的選擇見 [序列與蛋白模型](../bio-applications/sequence-and-protein-models.md)。

## 常見陷阱

| 陷阱 | 說明 |
| --- | --- |
| 前處理和預訓練時不一致 | ImageNet 模型要用同樣的 normalize 平均 / 標準差；tokenizer 必須和模型配套 |
| 凍結層的 BatchNorm 仍在更新 | `requires_grad=False` 不會停止 BN 更新 running mean / var；要對這些層呼叫 `.eval()` |
| fine-tune 學習率太大 | 預訓練權重被快速破壞（catastrophic forgetting）；骨幹用 1e-5～1e-4 |
| optimizer 收到凍結參數 | 不會報錯但浪費記憶體；用 `requires_grad` 過濾 |
| 用參數名字串判斷層（`"1" in name`） | `"10.weight"` 也會符合；改用模組屬性（`model.layer4`）或 `named_children()` |
| 預訓練資料與測試集重疊 | 公開蛋白質模型的訓練集可能包含你的 test 序列，分數會虛高；要檢查序列相似度 |
| 影像域差太大 | 自然影像預訓練 → 灰階醫學影像仍常有幫助，但領域內預訓練模型（病理、放射）通常更好 |
