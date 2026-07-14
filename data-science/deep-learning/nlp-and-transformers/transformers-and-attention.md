# Transformers and Attention

`Transformer Models with PyTorch` 的抽取內容證實目前 notebook 的 deep-learning 區塊原本明顯不足。transformer 不應該只出現在 LLM 應用章，而應作為 deep-learning 主教材的一部分。

## 為什麼 transformer 改變了文字建模

關鍵是 **attention**。它不再像 RNN 那樣一步一步傳遞狀態，而是讓每個 token 直接根據整個序列中的其他 token 分配注意力權重。

## 核心元件

- token embeddings
- positional encoding
- self-attention
- multi-head attention
- feed-forward network
- residual connection + layer normalization

## Self-Attention 的直覺

對每個 token 來說，模型都在問：

- 我現在該看序列中的哪些位置？
- 哪些詞對理解目前這個詞最重要？

這讓模型更容易捕捉長距離依賴，也更適合平行運算。

## 為什麼它和 LLM 有關

- 現代大多數 LLM 都建立在 transformer 架構上
- pretraining + fine-tuning / instruction tuning 都以 attention-based 架構為核心
- 這也是為什麼懂 transformer，比單純會呼叫 LLM API 更能理解模型限制

## 常見誤解

- attention map 看起來合理，不代表模型真的有可解釋因果邏輯
- transformer 很強，不代表所有任務都需要大型模型
- 架構變大不一定能解決資料標註品質差的問題
