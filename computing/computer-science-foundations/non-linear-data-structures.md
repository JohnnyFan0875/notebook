[Computing](../README.md) › [CS 基礎](README.md) › 非線性資料結構

# 非線性資料結構 (Non-linear Data Structures)

非線性資料結構中，一個元素可以連到多個元素：樹 (tree) 表達階層、堆積 (heap) 隨時取出最小 / 最大值、雜湊表 (hash table) 用 key 直接查值、圖 (graph) 表達任意關係。Python 的 `dict` / `set`、`heapq`、檔案系統、基因本體 (GO)、交互作用網路都建立在這些結構上。線性結構見 [線性資料結構](linear-data-structures.md)。

## 選哪個

| 需求 | 結構 | 關鍵操作複雜度 | Python |
| --- | --- | --- | --- |
| 依 key 查值、判斷成員 | 雜湊表 | 查詢 / 插入 `O(1)` 平均 | `dict`、`set` |
| 維持排序、範圍查詢 | 平衡二元搜尋樹 | 查詢 / 插入 `O(log n)` | `sortedcontainers`（第三方）、`bisect` + `list` |
| 反覆取出最小 / 最大值 | 堆積 | 取出 `O(log n)`、看最小 `O(1)` | `heapq` |
| 階層關係 | 樹 | 走訪 `O(n)` | 巢狀物件、`anytree` |
| 任意關係、網路 | 圖 | 走訪 `O(V + E)` | `dict` 鄰接串列、`networkx` |
| 前綴搜尋 | 字典樹 (trie) | 查詢 `O(長度)` | 自己實作 |

## 樹 (Tree)

| 名詞 | 意義 |
| --- | --- |
| 根 (root) | 最上層的節點 |
| 父 / 子 (parent / child) | 直接相連的上下層 |
| 葉 (leaf) | 沒有子節點 |
| 深度 / 高度 (depth / height) | 從根到節點的邊數 / 從節點到最深葉的邊數 |
| 二元樹 (binary tree) | 每個節點最多兩個子節點 |
| 子樹 (subtree) | 某節點與其所有後代 |

樹是**沒有環 (cycle) 的連通圖**：n 個節點恰好 n − 1 條邊。例子：檔案系統、HTML DOM、決策樹、演化樹 (phylogenetic tree)、階層分群的樹狀圖 (dendrogram)。

| 走訪順序 | 順序 | 用途 |
| --- | --- | --- |
| 前序 (pre-order) | 根 → 左 → 右 | 複製樹、列印目錄結構 |
| 中序 (in-order) | 左 → 根 → 右 | BST 依大小輸出 |
| 後序 (post-order) | 左 → 右 → 根 | 計算目錄大小（先算子再算父）、刪除樹 |
| 層序 (level-order) | 逐層 | [BFS](graph-traversal.md) |

### 二元搜尋樹 (Binary Search Tree, BST)

每個節點：左子樹所有值 < 節點值 < 右子樹所有值。查詢時每步往左或往右，像[二分搜尋](search-algorithms.md)。

```python
class BSTNode:
    def __init__(self, key):
        self.key, self.left, self.right = key, None, None

def insert(node, key):
    if node is None:
        return BSTNode(key)
    if key < node.key:
        node.left = insert(node.left, key)
    else:
        node.right = insert(node.right, key)
    return node

def contains(node, key):
    while node:
        if key == node.key:
            return True
        node = node.left if key < node.key else node.right
    return False

def in_order(node):                        # 中序走訪 → 由小到大
    return in_order(node.left) + [node.key] + in_order(node.right) if node else []

root = None
for k in [50, 30, 70, 20, 40, 60]:
    root = insert(root, k)
contains(root, 40)      # True
in_order(root)          # [20, 30, 40, 50, 60, 70]
```

| 情況 | 高度 | 查詢 |
| --- | --- | --- |
| 平衡 | `O(log n)` | `O(log n)` |
| 依序插入已排序資料 | 退化成鏈結串列，高度 n | `O(n)` |

實務用自動平衡的變體（紅黑樹、AVL、B-tree）。資料庫索引用的是 **B-tree / B+tree**：每個節點存很多 key，樹很矮，配合磁碟分頁讀取，見 [資料庫](../../data-science/databases/README.md)。

## 堆積 (Heap)

完全二元樹，且每個父節點 ≤ 子節點（min-heap），所以**根永遠是最小值**。通常用陣列儲存：索引 i 的子節點在 `2i+1`、`2i+2`。

| 操作 | 複雜度 |
| --- | --- |
| 看最小值 | `O(1)` |
| 插入 / 取出最小值 | `O(log n)` |
| 由 list 建堆 (`heapify`) | `O(n)` |

```python
import heapq

tasks = []
heapq.heappush(tasks, (2, "align"))        # (優先度, 工作)：tuple 依第一個元素比較
heapq.heappush(tasks, (1, "qc"))
heapq.heappush(tasks, (3, "report"))
heapq.heappop(tasks)                       # (1, 'qc')：永遠取出最小

heapq.nlargest(3, [5, 1, 9, 7, 3])         # [9, 7, 5]：前 k 名，O(n log k)
# Python 只有 min-heap；要 max-heap 就存負值
```

用途：優先佇列 (priority queue)、工作排程、Dijkstra 最短路徑、取前 k 名、合併多個已排序檔案（k-way merge）、[堆積排序](sorting-algorithms.md)。

## 雜湊表 (Hash Table)

用雜湊函數 (hash function) 把 key 轉成陣列位置，查詢、插入、刪除平均 `O(1)`。Python 的 `dict` 與 `set` 就是雜湊表。

```text
key "TP53" ──hash()──► 8172...  ──mod 表大小──► 第 3 格 ──► value
```

| 概念 | 說明 |
| --- | --- |
| 碰撞 (collision) | 不同 key 對到同一格；以鏈結 (chaining) 或開放定址 (open addressing) 處理 |
| 負載因子 (load factor) | 元素數 / 格數；太高時擴容並重新雜湊（攤銷 `O(1)`） |
| key 必須可雜湊 | 不可變型別：`str`、`int`、`tuple`；`list`、`dict` 不能當 key |
| 無序 | 不能做範圍查詢；Python 3.7+ 的 `dict` 保留插入順序，但那不是依 key 排序 |

```python
gene_len = {"TP53": 19149, "BRCA1": 81189}
gene_len.get("EGFR", 0)                    # 找不到回傳預設值

seen = set(known_ids)                      # O(n) 建表
new = [x for x in ids if x not in seen]    # 每次 O(1)；用 list 會變 O(n·m)

from collections import Counter, defaultdict
Counter(["A", "C", "A", "G"])              # Counter({'A': 2, 'C': 1, 'G': 1})：k-mer、類別計數
by_chrom = defaultdict(list)               # 分組
```

> 雜湊的其他用途：[檢查碼](../developer-tools/checksums.md)（MD5 / SHA-256 驗證檔案完整性）、資料去重、分散式系統的資料分片。

## 圖的表示法 (Graph Representation)

圖 G = (V, E)：節點 (vertex / node) 與邊 (edge)。

| 類型 | 說明 | 例子 |
| --- | --- | --- |
| 無向 / 有向 | 邊有無方向 | PPI 網路 / 調控網路、引用關係 |
| 加權 | 邊有權重 | 道路距離、交互作用信心分數 |
| 有向無環圖 (DAG) | 有方向且無環 | 工作流程依賴（[Snakemake、Nextflow、Airflow](../workflow-engines/README.md)）、Git commit 歷史、GO 本體 |

| 表示法 | 結構 | 空間 | 查「u、v 是否相連」 | 列出 u 的鄰居 | 適合 |
| --- | --- | --- | --- | --- | --- |
| 鄰接串列 (adjacency list) | 每個節點 → 鄰居清單 | `O(V + E)` | `O(deg u)`（用 set 則 `O(1)`） | `O(deg u)` | **稀疏圖**（多數真實網路） |
| 鄰接矩陣 (adjacency matrix) | V × V 矩陣，`A[u][v] = 1` 或權重 | `O(V²)` | `O(1)` | `O(V)` | 稠密圖、矩陣運算 |
| 邊列表 (edge list) | `(u, v, w)` 的清單 | `O(E)` | `O(E)` | `O(E)` | 檔案儲存與交換（TSV） |

```python
# 鄰接串列：dict of lists
graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}

# 由邊列表建圖
edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]
from collections import defaultdict
adj = defaultdict(list)
for u, v in edges:
    adj[u].append(v)               # 無向圖再加 adj[v].append(u)

# 鄰接矩陣：大型稀疏圖用 scipy.sparse 存
import numpy as np
nodes = ["A", "B", "C", "D"]
idx = {n: i for i, n in enumerate(nodes)}
A = np.zeros((4, 4), dtype=int)
for u, v in edges:
    A[idx[u], idx[v]] = 1
```

> 10,000 個基因的交互作用網路：鄰接矩陣要 10⁸ 格，鄰接串列只存實際的邊。單細胞的 kNN 圖也用稀疏矩陣儲存，見 [scipy.sparse](../../data-science/python-foundations/scipy-sparse.md)。走訪演算法見 [圖走訪](graph-traversal.md)；中心性、社群偵測等分析見 [網路分析](../../data-science/network-analysis/README.md)。
