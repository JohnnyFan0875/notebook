# Network Analysis

這個模組整理的是把資料看成 graph 時常見的思考方式。當資料的重點不只在單一列或單一特徵，而在 entities 彼此之間如何連接、穿越、聚集與中介時，network analysis 就會比一般 tabular analysis 更自然。

Key point: network analysis 的核心不是畫出一張很酷的圖，而是先定義 node、edge 與 edge meaning，然後再問這個連結結構如何影響重要性、可達性、群聚與推薦。

## Topics

- [Introduction to Network Analysis](introduction-to-network-analysis.md)
- [Bipartite and Evolving Networks](bipartite-and-evolving-networks.md)
- [Directed Networks and Structural Metrics](directed-networks-and-structural-metrics.md)
- [Network Analysis Case Studies](network-analysis-case-studies.md)

## 這個模組回答什麼問題

- 哪些節點在網路裡最重要？
- 哪些路徑最短、最常被經過，或最有橋接價值？
- 哪些群體彼此緊密連接，哪些只是鬆散相鄰？

## 建議閱讀順序

1. 先看 [Understanding Data Science](../understanding-data-science.md)，確認 graph 只是資料表示法之一，不是獨立宇宙。
2. 再看 [Introduction to Network Analysis](introduction-to-network-analysis.md)，把 node、edge、centrality 與 subgraph 直覺建立起來。
3. 再看 [Bipartite and Evolving Networks](bipartite-and-evolving-networks.md)，把 projection、graph-from-DataFrame 與時間切片分析接起來。
4. 最後看 [Directed Networks and Structural Metrics](directed-networks-and-structural-metrics.md)，把 directedness、transitivity、random baseline 與 community detection 接到整體結構判讀上。
5. 補看 [Network Analysis Case Studies](network-analysis-case-studies.md)，把交易、文字互動與移動資料如何落成 graph 的實戰流程接起來。
