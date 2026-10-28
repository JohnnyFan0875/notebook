# Text and Sequence Models

在文字任務中，模型無法直接吃字串，第一步一定是把 token 轉成數值表示；之後再用 RNN / LSTM / GRU 或 [Transformer](transformers-and-attention.md) 處理序列。

相關：句向量與語意搜尋見 [Embeddings and Semantic Search](../../llm/rag/embeddings-and-semantic-search.md)；不用深度學習的文字分析（tidytext、sentiment、LDA）見 [Text Analysis in R](../../r-foundations/text-analysis.md)。

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

## Sequence Models (RNN / LSTM / GRU)

在 transformer 成為主流前，文字深度學習大量依賴 RNN、LSTM、GRU 等 sequence models。即使現在很多專案直接用 transformer，理解 sequence modeling 仍然很重要，因為它幫助你掌握「語序」與「狀態傳遞」的基本概念。

### 這類模型在做什麼

- 一次讀入一個 token
- 把前面資訊壓進 hidden state
- 再用 hidden state 影響後續預測

### 為什麼會遇到限制

- 序列太長時，早期資訊難以保留
- 訓練難以平行化
- 容易有 vanishing / exploding gradients

### LSTM / GRU 的價值

它們透過 gating 機制，讓模型比較能保留重要資訊、忘記不重要資訊，因此比最基本的 vanilla RNN 更穩定。

### 常見任務

- sentiment analysis
- text classification
- language modeling
- sequence generation

### 判讀提醒

- 若你只是做短文字分類，簡單模型未必輸 transformer 太多。
- 若資料很少，sequence model 也可能比大 transformer 更容易穩定訓練。
- 若任務需要長距離依賴，transformer 通常更有優勢。
