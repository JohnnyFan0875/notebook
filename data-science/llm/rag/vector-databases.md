[LLM](../README.md) › [RAG](README.md) › 向量資料庫

# 向量資料庫 (Vector Databases)

向量資料庫儲存 embedding 與 metadata，並用近似最近鄰 (approximate nearest neighbor, ANN) 索引在大量向量中快速找出最相近的幾筆。在 RAG 中它是檢索層：決定哪些段落有資格進入 prompt。

## 一筆紀錄存什麼

| 欄位 | 用途 |
| --- | --- |
| ID | 更新、刪除、去重（用穩定的 ID，如 `PMID:12345#chunk-3`） |
| 向量 | 相似度搜尋；維度必須與 embedding 模型一致 |
| 原文（或指向原文的參照） | 放進 prompt、顯示來源 |
| Metadata | 過濾與追溯：來源、年份、物種、文件類型、權限群組、embedding 模型版本 |

## ANN 索引

暴力搜尋 (exact / flat) 每次比較所有向量，O(N)；ANN 用索引結構只比較一小部分，換取速度，代價是偶爾漏掉真正的最近鄰（recall < 100%）。

| 索引 | 原理 | 特性 |
| --- | --- | --- |
| Flat | 全部比較 | 精確；幾萬到幾十萬筆內通常夠快 |
| HNSW | 多層鄰接圖，從上層粗略導航到下層精細搜尋 | 速度與 recall 都好，最常用；記憶體用量大 |
| IVF | 先 K-means 分群，只搜尋最近的幾群 | 適合大規模；需要訓練分群 |
| PQ（乘積量化） | 壓縮向量 | 大幅省記憶體，準確度下降 |

| 調整參數（以 HNSW 為例） | 效果 |
| --- | --- |
| `M`（每點連結數） | 大 → recall 高、記憶體多 |
| `ef_construction` | 大 → 建索引慢、品質好 |
| `ef_search` | 大 → 查詢慢、recall 高 |

```python
import faiss
import numpy as np

d = doc_emb.shape[1]
X = np.asarray(doc_emb, dtype="float32")               # faiss 需要 float32；已 L2 正規化

index = faiss.IndexFlatIP(d)                           # 精確內積（= cosine）
# index = faiss.IndexHNSWFlat(d, 32, faiss.METRIC_INNER_PRODUCT)   # 大量資料時改用 HNSW
index.add(X)
scores, ids = index.search(np.asarray(query_emb, dtype="float32"), k=5)
```

## 距離度量

| 度量 | 意義 | 何時用 |
| --- | --- | --- |
| Cosine | 方向相似 | 多數文字 embedding 的預設 |
| 內積 (dot product) | 方向 + 長度 | 向量已正規化時等同 cosine |
| 歐氏距離 (L2) | 幾何距離 | 正規化後與 cosine 排序相同 |

> 度量要和 embedding 模型訓練時的假設一致（看 model card）。部分資料庫預設是 L2，向量未正規化時結果會與 cosine 不同。

## Metadata 過濾與 Namespace

| 用途 | 例子 |
| --- | --- |
| 縮小範圍、提升相關性 | 只搜尋 `species == "human"` 且 `year >= 2020` |
| 權限控制 | 使用者只能檢索自己有權看的文件（`group in user.groups`） |
| 版本管理 | 新舊 embedding 模型的向量分開存放，比較後再切換 |
| 多租戶隔離 | 不同實驗室 / 客戶的資料分 namespace 或分索引 |

| 多租戶策略 | 隔離程度 | 代價 |
| --- | --- | --- |
| 共用索引 + metadata 過濾 | 低：漏寫過濾條件就會外洩 | 最簡單 |
| 共用索引 + namespace | 中 | 部分資源共用 |
| 每個租戶獨立索引 | 高 | 維運成本最高 |

> 權限不能只靠應用程式「記得加過濾條件」。敏感資料要在儲存層就隔離，並測試跨租戶查詢會不會回傳資料。

過濾時機也有差別：先過濾再搜尋 (pre-filtering) 結果完整，但過濾條件很嚴時 ANN 可能找不滿 k 筆；先搜尋再過濾 (post-filtering) 快，但可能過濾後剩很少筆。

## 寫入與更新

| 注意 | 做法 |
| --- | --- |
| 大量寫入 | 分批 upsert；控制速率；失敗批次可重試 |
| 文件更新 | 以穩定 ID upsert；刪除舊 chunk（文件變短時舊 chunk 會殘留） |
| 換 embedding 模型 | 全部重算，新舊索引並存比較後再切換 |
| 成本 | 託管服務常依儲存量、查詢量、向量維度計費；縮小搜尋範圍可同時省錢與提升相關性 |

## 工具比較

| 工具 | 類型 | 適合 |
| --- | --- | --- |
| FAISS | 函式庫（記憶體內） | 研究、批次處理、自行管理儲存 |
| Chroma、LanceDB | 嵌入式 / 本機資料庫 | 原型、個人或小團隊 |
| pgvector | PostgreSQL 擴充 | 已用 [PostgreSQL](../../databases/postgresql-psql-and-copy.md)；向量與關聯資料一起查詢、交易與權限沿用資料庫 |
| Qdrant、Weaviate、Milvus | 專用向量資料庫（可自架） | 大規模、需要豐富過濾與 hybrid search |
| Pinecone 等託管服務 | Serverless / 託管 | 不想維運；資料會存放在供應商 |
| Elasticsearch / OpenSearch | 搜尋引擎 + 向量 | 已有全文搜尋，要加 hybrid search |

```sql
-- pgvector：向量與一般欄位一起過濾
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE chunks (id text PRIMARY KEY, pmid int, year int, content text, embedding vector(384));
CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);

SELECT id, content, 1 - (embedding <=> :query_vec) AS cosine_sim   -- <=> 是 cosine 距離
FROM chunks
WHERE year >= 2020
ORDER BY embedding <=> :query_vec
LIMIT 5;
```

> 先用最簡單的方案（FAISS、Chroma 或 pgvector）。效能或規模真正成為瓶頸時才換專用服務：多數 RAG 系統的品質瓶頸在切分與檢索策略，而不在資料庫。
