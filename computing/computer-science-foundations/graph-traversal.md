[Computing](../README.md) › [CS 基礎](README.md) › 圖走訪

# 圖走訪：DFS 與 BFS (Graph Traversal)

從某個起點出發，有系統地拜訪所有可到達的節點。兩種經典走法：深度優先 (DFS) 一路走到底再回頭，廣度優先 (BFS) 一圈一圈往外擴。兩者的差別來自背後的資料結構：DFS 對應[堆疊](linear-data-structures.md#堆疊-stacklifo)（或遞迴），BFS 對應[佇列](linear-data-structures.md#佇列-queuefifo)。圖的表示法見 [非線性資料結構](non-linear-data-structures.md#圖的表示法-graph-representation)。

```text
        A                DFS（A 起）：A → B → D → E → C → F    一條路走到底再回溯
       / \               BFS（A 起）：A → B → C → D → E → F    先走完距離 1，再走距離 2
      B   C
     / \   \
    D   E   F
```

## 比較

| | DFS | BFS |
| --- | --- | --- |
| 策略 | 盡量深入，走不下去再回溯 | 依距離逐層擴張 |
| 資料結構 | 堆疊 / 遞迴 | 佇列 |
| 時間 | `O(V + E)` | `O(V + E)` |
| 記憶體 | 與路徑深度成正比 | 與最寬一層的節點數成正比 |
| 最短路徑（無權重圖） | 不保證 | **保證**：先被發現的就是最近的 |
| 適合 | 是否可達、找環、拓撲排序、連通元件、窮舉路徑 | 最少步數、最近的目標、逐層分析（幾度分隔） |

> 圖可能有環，**一定要記錄 `visited`**，否則會重複走回同一節點甚至無限迴圈。樹沒有環，走訪時可以省略。

## 實作

```python
from collections import deque

graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": [], "E": [], "F": []}

def dfs(graph, node, visited=None):            # 遞迴版
    if visited is None:
        visited = []
    visited.append(node)
    for nb in graph[node]:
        if nb not in visited:
            dfs(graph, nb, visited)
    return visited

def dfs_iterative(graph, start):               # 明確的堆疊：避免遞迴深度上限
    visited, stack = set(), [start]
    order = []
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node); order.append(node)
        stack.extend(reversed(graph[node]))    # 反轉以維持與遞迴版相同的順序
    return order

def bfs(graph, start):
    visited, q = {start}, deque([start])       # 放入佇列時就標記，避免重複加入
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for nb in graph[node]:
            if nb not in visited:
                visited.add(nb)
                q.append(nb)
    return order

def shortest_path(graph, start, goal):         # BFS + 記錄前一個節點 → 無權重最短路徑
    prev, q = {start: None}, deque([start])
    while q:
        node = q.popleft()
        if node == goal:
            path = []
            while node is not None:
                path.append(node); node = prev[node]
            return path[::-1]
        for nb in graph[node]:
            if nb not in prev:
                prev[nb] = node; q.append(nb)
    return None

dfs(graph, "A")                  # ['A', 'B', 'D', 'E', 'C', 'F']
bfs(graph, "A")                  # ['A', 'B', 'C', 'D', 'E', 'F']
shortest_path(graph, "A", "F")   # ['A', 'C', 'F']
```

| 細節 | 說明 |
| --- | --- |
| `visited` 用 `set` | `x in list` 是 `O(n)`，整體會變 `O(V²)` |
| BFS 在**加入佇列時**標記 | 等到取出才標記，同一節點可能被重複加入 |
| 遞迴 DFS 的深度 | Python 預設上限約 1000 層，大圖用迭代版 |
| 佇列用 `deque` | `list.pop(0)` 是 `O(n)` |

## 延伸演算法

| 問題 | 演算法 | 基礎 |
| --- | --- | --- |
| 加權圖最短路徑（權重非負） | Dijkstra | BFS + [堆積](non-linear-data-structures.md#堆積-heap) |
| 有負權重的最短路徑 | Bellman-Ford | 動態規劃 |
| DAG 的執行順序 | 拓撲排序 (topological sort) | DFS 後序反轉，或 Kahn 演算法（BFS） |
| 有沒有環 | DFS 遇到正在走訪路徑上的節點 | DFS |
| 連通元件 | 對每個未走訪的節點做 DFS / BFS | 兩者皆可 |

> 工作流程引擎（[Snakemake、Nextflow、Airflow](../workflow-engines/README.md)）把步驟依賴建成 DAG，再用拓撲排序決定執行順序、找出可以平行跑的步驟；有環就無法執行。

實務上用 `networkx`：`nx.bfs_tree`、`nx.shortest_path`、`nx.topological_sort`、`nx.connected_components`，見 [網路分析](../../data-science/network-analysis/README.md)。
