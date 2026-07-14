# Text Representations and Embeddings

在文字任務中，模型無法直接吃字串，第一步一定是把 token 轉成數值表示。`notebook_temp/output` 裡的 `Deep Learning for Text with PyTorch` 與多個 NLP 課程，核心共同點都在這裡。

## 從文字到 tensor 的基本流程

1. tokenize：把句子切成 token
2. build vocabulary：建立 token 到 index 的對應
3. numericalize：把 token 序列轉成整數序列
4. pad / truncate：對齊 batch 長度
5. embedding：把整數 index 映射成可學習的 dense vector

## Bag-of-Words vs Embeddings

| 方法 | 特點 | 限制 |
| --- | --- | --- |
| Bag-of-Words | 簡單、可解釋 | 不保留語序、維度高且稀疏 |
| Embedding | 緊湊、可學語意相似性 | 需要訓練或預訓練表示 |

## Minimal Example

```python
import torch
from torch import nn

vocab = {"<pad>": 0, "i": 1, "love": 2, "nlp": 3}
tokens = ["i", "love", "nlp"]
ids = torch.tensor([vocab[token] for token in tokens])

embedding = nn.Embedding(num_embeddings=len(vocab), embedding_dim=8)
embedded = embedding(ids)

print(embedded.shape)  # torch.Size([3, 8])
```

## 為什麼 embedding 有用

- 把離散 token 轉成可學習連續表示
- 類似語境的詞可能學到相近向量
- 可以作為 RNN、CNN、Transformer 的輸入基礎

## 常見陷阱

- tokenization 規則和推論時不一致
- 忘記處理 OOV 詞或 padding token
- 把 embedding 當成天然可解釋的語意空間，而忽略資料與任務影響
