[Data Science](../../README.md) › [Deep Learning](../README.md) › NLP 與 Transformer

# NLP 與 Transformer (NLP and Transformers)

序列資料（文字、DNA、蛋白質）怎麼變成 tensor、怎麼建模。從 tokenize 與 embedding、RNN / LSTM，到 attention 與 Transformer——現代 LLM 與蛋白質語言模型的共同骨架。

## 建議順序

```
token / embedding → RNN / LSTM（狀態傳遞） → attention → Transformer → 應用
                                                                   ├─ LLM：見 LLM 章節
                                                                   └─ DNA / 蛋白質：見生資應用
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [文字與序列模型](text-and-sequence-models.md) | tokenization（字元 / 子詞 / k-mer）、embedding、padding、RNN / LSTM / GRU | 序列怎麼變成 tensor？RNN 的限制是什麼？ |
| [Transformer 與 Attention](transformers-and-attention.md) | Q / K / V、scaled dot-product、multi-head、位置編碼、encoder vs decoder | attention 在算什麼？為什麼 Transformer 成為主流？ |

## 相關章節

| 主題 | 位置 |
| --- | --- |
| LLM 概念、prompt、RAG、fine-tuning（LoRA） | [LLM](../../llm/README.md)、[Fine-Tuning](../../llm/integration/fine-tuning.md) |
| 句向量與語意搜尋 | [Embeddings 與語意搜尋](../../llm/rag/embeddings-and-semantic-search.md) |
| 蛋白質 / DNA 語言模型 | [序列與蛋白模型](../bio-applications/sequence-and-protein-models.md) |
| 不用深度學習的文字分析（tf-idf、LDA） | [Text Analysis in R](../../r-foundations/text-analysis.md) |
