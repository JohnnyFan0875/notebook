[Deep Learning](../README.md) › [NLP 與 Transformer](README.md) › 文字與序列模型

# 文字與序列模型 (Text and Sequence Models)

模型不能直接吃字串。序列要先切成 token、轉成整數 ID、再查表變成向量 (embedding)；之後才交給 RNN / LSTM 或 [Transformer](transformers-and-attention.md) 處理。同一套流程也適用於 DNA 與蛋白質序列。

## 從序列到 tensor

```
"I love NLP"  → tokenize → ["i", "love", "nlp"] → numericalize → [1, 2, 3]
                                                      ↓ pad 到同長度
                                                 [[1, 2, 3, 0, 0], ...]  (batch, L)
                                                      ↓ nn.Embedding
                                                 (batch, L, d) 的實數向量
```

## Tokenization

| 方式 | 例子 | 優點 | 缺點 |
| --- | --- | --- | --- |
| 字詞 (word) | `["unhappiness"]` | 直觀 | 詞彙表巨大、未見過的詞 (OOV) 無法處理 |
| 字元 (character) | `["u","n","h",...]` | 沒有 OOV | 序列很長 |
| **子詞 (subword)**：BPE、WordPiece、SentencePiece | `["un", "##happi", "##ness"]` | 兼顧詞彙量與 OOV | 切法依語料而定 |
| 單一殘基 / 鹼基 | 蛋白質 `M K T A Y`、DNA `A C G T` | 自然、無歧義 | 序列長 |
| k-mer | DNA `ACG CGT GTA`（k=3 重疊） | 帶入局部脈絡 | 詞彙量 $4^k$；重疊 k-mer 有資訊洩漏到相鄰 token 的問題 |

> 預訓練模型的 tokenizer 必須和模型配套使用（`AutoTokenizer.from_pretrained(同一個名稱)`）；自己訓練時，詞彙表只能從**訓練集**建立。

## Embedding

`nn.Embedding(vocab_size, d)` 就是一張可學習的查表矩陣：第 i 列是 token i 的向量，等同 one-hot 乘上權重矩陣，但更省記憶體。

```python
import torch
from torch import nn

vocab = {"<pad>": 0, "<unk>": 1, "i": 2, "love": 3, "nlp": 4}
ids = torch.tensor([[vocab.get(t, 1) for t in ["i", "love", "nlp"]]])   # 未知詞 → <unk>
emb = nn.Embedding(len(vocab), embedding_dim=8, padding_idx=0)          # pad 向量固定為 0、不更新
emb(ids).shape                                                           # torch.Size([1, 3, 8])
```

| 表示法 | 特點 |
| --- | --- |
| Bag-of-words / tf-idf | 不保留語序、高維稀疏；小資料文字分類仍是強 baseline |
| 靜態 embedding（word2vec、GloVe） | 每個詞一個固定向量；「bank」不分河岸或銀行 |
| 上下文 embedding（BERT、ESM） | 同一個 token 在不同句子 / 序列中向量不同 |

用預訓練模型產生句向量做語意搜尋見 [Embeddings 與語意搜尋](../../llm/rag/embeddings-and-semantic-search.md)；不用深度學習的 tidytext / tf-idf / LDA 見 [Text Analysis in R](../../r-foundations/text-analysis.md)。

> embedding 的相似度反映的是**訓練資料中的共現**，不保證是語意或生物功能上的相似；在下游任務上驗證，不要直接拿向量距離當結論。

## Padding 與 mask

batch 內序列長短不一時要補到同長，模型必須知道哪些位置是 padding：

| 模型 | 處理方式 |
| --- | --- |
| RNN | `pack_padded_sequence`，讓 RNN 跳過 padding |
| Transformer | `attention_mask` / `src_key_padding_mask`：padding 位置不被注意 |
| 池化成一個向量 | 平均時排除 padding：`(h * mask).sum(1) / mask.sum(1)` |
| Loss | `CrossEntropyLoss(ignore_index=pad_id)` |

## 循環神經網路 (RNN / LSTM / GRU)

RNN 一次讀一個 token，把目前為止的資訊壓縮進隱藏狀態 (hidden state) $h_t = f(x_t, h_{t-1})$。

| 模型 | 機制 | 特點 |
| --- | --- | --- |
| Vanilla RNN | 單一 tanh 更新 | 長序列梯度消失，記不住遠處資訊 |
| **LSTM** | 遺忘 / 輸入 / 輸出三個 gate + 細胞狀態 (cell state) | 能保留長距離資訊；過去序列任務的主力 |
| GRU | 兩個 gate，結構較簡單 | 參數較少，效果常與 LSTM 相近 |
| 雙向 (bidirectional) | 正向 + 反向各跑一次再串接 | 分類、標註任務常用；不能用於逐字生成 |

```python
class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, n_classes, d=64, hidden=128):
        super().__init__()
        self.emb = nn.Embedding(vocab_size, d, padding_idx=0)
        self.lstm = nn.LSTM(d, hidden, batch_first=True, bidirectional=True)
        self.head = nn.Linear(2 * hidden, n_classes)

    def forward(self, ids, lengths):                     # lengths：每條序列的實際長度
        x = nn.utils.rnn.pack_padded_sequence(self.emb(ids), lengths.cpu(),
                                              batch_first=True, enforce_sorted=False)
        _, (h, _) = self.lstm(x)                         # h: (2 方向, batch, hidden)
        return self.head(torch.cat([h[0], h[1]], dim=1))

model = LSTMClassifier(vocab_size=5000, n_classes=2)
model(torch.randint(1, 5000, (4, 20)), torch.tensor([20, 15, 9, 3])).shape   # torch.Size([4, 2])
```

## RNN vs Transformer

| 面向 | RNN / LSTM | Transformer |
| --- | --- | --- |
| 長距離依賴 | 資訊要一步步傳遞，容易衰減 | 任兩個位置直接相連 |
| 訓練平行化 | 不行（必須依序） | 可以（所有位置同時算） |
| 計算量對長度 L | $O(L)$ | $O(L^2)$（attention 矩陣） |
| 小資料 | 較容易訓練 | 從頭訓練需大量資料；通常用預訓練模型 |
| 現況 | 小型、串流、低延遲任務 | 主流；LLM、蛋白質語言模型 |

> 短文本分類、樣本少時，tf-idf + logistic 迴歸或小型 LSTM 常與大型模型差距不大，而且便宜、好解釋——先建 [baseline](../../machine-learning/evaluation/baselines-and-error-analysis.md)。
