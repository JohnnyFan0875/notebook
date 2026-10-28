[LLM](../README.md) › [RAG](README.md) › Embedding 與語意搜尋

# Embedding 與語意搜尋 (Embeddings and Semantic Search)

Embedding 把一段文字對應成固定長度的向量，語意相近的文字向量也相近。這讓「依意思搜尋」成為可能，也是 RAG、推薦、分群與輕量分類的基礎。詞向量與 embedding 層的原理見 [文字與序列模型](../../deep-learning/nlp-and-transformers/text-and-sequence-models.md)。

## 概念

| 概念 | 意義 |
| --- | --- |
| Embedding 向量 | 一段文字（句子、段落）→ 數百到數千維向量；單一維度沒有可解讀的意義 |
| 相近向量 | 語意相近，即使用字不同（"cell death" ≈ "apoptosis"） |
| Cosine 相似度 | $\cos\theta = \dfrac{a \cdot b}{\lVert a \rVert \lVert b \rVert}$，比較方向；向量正規化後等於內積 |
| Bi-encoder | 問題與文件**各自**編碼成向量 → 可事先算好文件向量，檢索快 |
| Cross-encoder | 問題與文件**一起**輸入模型打分 → 較準但慢，用於 [reranking](rag-pipeline.md#檢索策略) |

| 搜尋方式 | 優點 | 缺點 |
| --- | --- | --- |
| 關鍵字（BM25） | 精確比對專有名詞、基因符號、ID | 找不到同義詞與改寫 |
| 語意（embedding） | 找到意思相近的改寫 | 對罕見術語、精確 ID 不敏感；可能回傳「主題相近但不相關」的結果 |
| Hybrid | 兩者分數合併 | 多一個需要調整的權重 |

> 生醫文字中基因符號、變異寫法、藥名很常見，純語意搜尋常把 `BRCA1` 與 `BRCA2` 視為幾乎相同。生醫 RAG 通常需要 [hybrid search](rag-pipeline.md#檢索策略)。

## 語意搜尋流程

```python
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")     # 通用小模型；生醫文字可比較領域模型
docs = ["Ferroptosis is an iron-dependent form of regulated cell death.",
        "Scanpy is a toolkit for single-cell RNA-seq analysis.",
        "GPX4 inhibition triggers lipid peroxidation."]
doc_emb = model.encode(docs, normalize_embeddings=True)          # (3, 384)

query_emb = model.encode(["iron-dependent cell death mechanisms"], normalize_embeddings=True)
scores = doc_emb @ query_emb.T                                    # 已正規化 → 內積 = cosine
order = np.argsort(-scores.ravel())                               # 由近到遠的文件索引；預期第 0 篇（ferroptosis）排第一
```

| 步驟 | 注意 |
| --- | --- |
| 文件與問題用**同一個** embedding 模型 | 不同模型的向量空間不相容；換模型要重算全部文件 |
| 部分模型要求加前綴 | 如 E5 系列的 `"query: "` / `"passage: "`；照 model card 做 |
| 輸入長度上限 | 超過會被截斷（常見 256–512 token）→ 先切段 |
| 儲存向量時一併存 ID、原文、metadata | 才能回溯來源、過濾、更新 |

| 選 embedding 模型 | 說明 |
| --- | --- |
| 看 MTEB 排行榜的**檢索**分數 | 但通用基準不代表你的領域；用自己的資料測 |
| 維度 | 越高越準但越耗記憶體；部分模型支援截短維度 |
| 多語言 | 中英混合資料要選多語言模型 |
| 部署 | API embedding（省事）vs 本機模型（資料不出機構、免費） |

## 豐富輸入 (Enriched Embeddings)

單一欄位資訊太少時，把多個屬性組合成一段文字再嵌入：

| 原始輸入 | 豐富後 |
| --- | --- |
| 論文標題 | 標題 + 摘要 + MeSH 詞 |
| 資料集名稱 | 名稱 + 物種 + 組織 + 技術平台 + 描述 |
| 文件段落 | 段落 + 文件標題 + 章節標題 |

章節標題對切分後的段落特別重要：「結果顯示顯著上升」單獨看不出在講什麼，加上「GPX4 表現量 / 結果」後才能被正確檢索。

## 其他用途

| 用途 | 做法 |
| --- | --- |
| 推薦相似項目 | 找與目前論文 / 資料集向量最近的 k 個 |
| 去重 | 相似度 > 門檻視為重複（如同一研究的多篇報告） |
| 分群、視覺化 | 向量做 [K-means](../../machine-learning/unsupervised-learning/clustering/README.md) / UMAP，觀察主題結構 |
| 零樣本分類 | 每個標籤寫一句描述並嵌入，文件分給最相近的標籤 |
| 作為特徵 | 向量餵給 [邏輯斯迴歸](../../machine-learning/supervised-learning/README.md) 等分類器；少量標註即可得到不錯的 baseline |

```python
labels = {"immunology": "immune cells, T cells, cytokines, antibodies",
          "neuroscience": "neurons, synapses, brain, neural circuits"}
label_emb = model.encode(list(labels.values()), normalize_embeddings=True)
pred = np.array(list(labels))[(doc_emb @ label_emb.T).argmax(axis=1)]
```

零樣本分類適合快速 baseline；標籤語意接近或高度專業時會失準，有標註資料就改用監督式分類。

## 從原型到向量資料庫

上面的 NumPy 做法把所有向量放在記憶體、每次查詢與全部文件比較（暴力搜尋），幾萬筆以內很夠用。資料量大、需要 metadata 過濾或持續更新時，改用 [向量資料庫](vector-databases.md)。
