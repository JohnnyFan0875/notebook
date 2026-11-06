[Computing](../README.md) › CS 基礎

# 電腦科學基礎 (Computer Science Foundations)

程式如何被執行、演算法怎麼評估效率、資料結構如何決定哪些操作快，以及計算本身的理論極限。對資料工作者最實用的是：看懂複雜度，選對資料結構（`set` / `dict` vs `list`），知道為什麼向量化與索引會快。

## 建議順序

```text
電腦架構 → 演算法與複雜度 → 線性資料結構 → 非線性資料結構 → 搜尋 → 排序 → 圖走訪
                                                                    └─ 延伸：可計算性、程式設計範式
```

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [電腦架構與程式執行](computer-architecture-and-program-execution.md) | CPU、記憶體階層、二進位、編譯 vs 直譯 vs JIT | 程式怎麼被硬體執行？為什麼有的語言快？ |
| [演算法與複雜度](algorithms-and-complexity.md) | Big-O、最佳 / 平均 / 最壞、成長曲線、設計策略 | 資料變大 10 倍，程式會慢多少？ |
| [線性資料結構](linear-data-structures.md) | 陣列、鏈結串列、堆疊、佇列、`deque` | 依序存取的資料該用哪種結構？ |
| [非線性資料結構](non-linear-data-structures.md) | 樹、BST、堆積、雜湊表、圖的表示法 | 查詢、排序維持、取最小值、表達關係用什麼？ |
| [搜尋演算法](search-algorithms.md) | 線性 vs 二分搜尋、`bisect`、`searchsorted` | 要先排序嗎？怎麼查最快？ |
| [排序演算法](sorting-algorithms.md) | 五種排序、穩定性、實測耗時、`sorted` / `heapq` | 排序的成本與選擇？ |
| [圖走訪](graph-traversal.md) | DFS、BFS、最短路徑、拓撲排序 | 怎麼有系統地走過一張圖？ |
| [可計算性與圖靈機](computability-and-turing-machines.md) | 自動機層級、圖靈機、停機問題、P vs NP | 哪些問題理論上不可能解？ |
| [程式設計範式](programming-paradigms.md) | 程序式、函數式、物件導向、宣告式 | 程式該怎麼組織？ |

延伸：效能實務見 [效能與擴展](../../data-science/python-foundations/performance-and-scaling/README.md)，網路分析見 [網路分析](../../data-science/network-analysis/README.md)。
