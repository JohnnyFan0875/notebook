[Data Science](../README.md) › Network Analysis

# 網路分析 (Network Analysis)

當資料的重點是「誰和誰相連」，而不是單一列的特徵時，把資料表示成 graph 比一般表格更自然。核心不是畫出漂亮的圖，而是先定義 node、edge 與 edge 的意義，再問連結結構如何影響重要性、可達性、群聚與推薦。生資中常見的 PPI 網路、基因共表現網路、單細胞 kNN 圖都屬於這一類。

## 建議順序

```
入門（建圖、centrality、路徑、clique）→ 有向網路與結構指標（隨機基準、社群偵測）
   → 二分網路與時間演變（projection、時間切片）→ 案例（事件資料 → graph、生資網路）
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [網路分析入門](introduction-to-network-analysis.md) | node / edge 定義、graph 類型、degree / betweenness / closeness / eigenvector、最短路徑、clique、subgraph | 哪些節點重要？重要的意思是什麼？ |
| [有向網路與結構指標](directed-networks-and-structural-metrics.md) | in / out-degree、density、平均路徑長、transitivity、assortativity、reciprocity、隨機圖基準、社群偵測 | 整張網路的結構特殊嗎？有哪些群體？ |
| [二分網路與時間演變](bipartite-and-evolving-networks.md) | 二分圖、projection 與權重、edge 過濾、從 DataFrame 建圖、時間切片 | 兩類實體的關係怎麼分析？網路怎麼隨時間改變？ |
| [網路分析案例](network-analysis-case-studies.md) | 商品、Twitter、單車流動；PPI（STRING）、共表現網路（WGCNA）、單細胞 kNN 圖 + Leiden | 原始事件資料怎麼變成值得分析的 graph？ |

## 與其他章節的關係

| 主題 | 去哪裡 |
| --- | --- |
| graph 從表格轉換而來，前處理仍是基本功 | [Data Manipulation and EDA](../data-manipulation-and-eda/README.md) |
| 分群（社群偵測與 clustering 的關係） | [Clustering](../machine-learning/unsupervised-learning/clustering/README.md) |
| 用 graph 結構學節點表示、做節點分類 | [圖神經網路](../deep-learning/representation-learning/graph-neural-networks.md) |
| 在資料庫中做多跳查詢、階層展開 | [遞迴與階層查詢](../databases/recursive-and-hierarchical-sql.md) |
| 事件資料轉成流程轉移圖 | [流程探勘](../applied-domains/process-mining.md) |

| 工具 | 語言 | 適合 |
| --- | --- | --- |
| NetworkX | Python | 學習、中小型網路（數萬節點）、演算法齊全 |
| igraph | Python / R | 較大的網路、速度快、社群偵測方法多 |
| graph-tool、NetworKit | Python | 數百萬節點以上 |
| Cytoscape | GUI | 生物網路視覺化與註解 |
| scanpy（`sc.pp.neighbors`、`sc.tl.leiden`） | Python | 單細胞 kNN 圖與分群 |

> 圖長得漂亮不代表分析有意義；不同 centrality 回答不同問題，不應混成單一的「重要性」；從表格投影出來的網路要先確認 projection 規則沒有放大假訊號。
