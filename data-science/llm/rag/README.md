[Data Science](../../README.md) › [LLM](../README.md) › RAG

# 檢索增強生成 (Retrieval-Augmented Generation, RAG)

RAG 在生成前先從文件庫檢索相關段落，放進 prompt，讓模型根據**可追溯的來源**回答，而不是只靠參數記憶。適合內部 SOP、論文庫、資料庫說明文件的問答。

## 建議順序

```
Embedding（文字 → 向量、相似度）→ 向量資料庫（索引、過濾、規模化）→ RAG Pipeline（切分、檢索、grounding、評估）
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Embedding 與語意搜尋](embeddings-and-semantic-search.md) | embedding 模型、cosine 相似度、語意 vs 關鍵字搜尋、推薦、零樣本分類 | 怎麼用「意思」而不是「字面」找文件？ |
| [向量資料庫](vector-databases.md) | ANN 索引（HNSW、IVF）、metadata 過濾、namespace、工具比較 | 文件很多時怎麼快速檢索？ |
| [RAG Pipeline](rag-pipeline.md) | 載入與切分、hybrid search、reranking、prompt grounding、引用、評估、進階做法 | 怎麼組出可信、可評估的問答系統？ |

> Chunking 與 prompt grounding 通常比選哪個向量資料庫更影響結果。
