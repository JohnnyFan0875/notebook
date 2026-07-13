# Graph Traversal: DFS and BFS

圖或樹的 traversal 問題，本質上是在問：

- 從某個起點出發
- 怎麼有系統地拜訪所有可到達的節點

最經典的兩種走法是：

- depth-first search (`DFS`)
- breadth-first search (`BFS`)

## DFS: Go Deep First

DFS 的直覺是一路往下走，走到底再回頭。

它很自然地對應到：

- recursion
- stack-like control flow

```python
def dfs(visited, graph, current):
    if current not in visited:
        print(current)
        visited.add(current)
        for neighbor in graph[current]:
            dfs(visited, graph, neighbor)
```

### DFS Mental Model

- 先盡量深入
- 碰到走不下去的地方再回溯

DFS 常見用途：

- exploring connected structure
- path existence checking
- cycle-related reasoning
- tree traversal patterns

## BFS: Explore Level by Level

BFS 的直覺是先看離起點最近的一圈，再看下一圈。

它通常需要 queue。

```python
import queue

def bfs(graph, start):
    visited = [start]
    q = queue.SimpleQueue()
    q.put(start)

    while not q.empty():
        current = q.get()
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.append(neighbor)
                q.put(neighbor)

    return visited
```

### BFS Mental Model

- 按距離層級逐步擴張
- 誰先被發現，通常代表誰更靠近起點

這也是 BFS 很適合 shortest-path intuition 的原因，特別是在 unweighted graphs 裡。

## Tree Traversal vs Graph Traversal

在 tree 裡，traversal 常常比較單純，因為通常沒有 cycle。

在 graph 裡，多半一定要記錄 `visited`，不然很容易重複走回同一個節點。

Key point: `visited` 不是小細節，而是 graph traversal 正確性的核心之一。

## BFS vs DFS: 何時哪個比較自然

| Method | Better intuition when... |
| --- | --- |
| BFS | target is likely close to the starting node |
| DFS | you want to go deep, explore branches, or reason recursively |

常見口語直覺：

- BFS: 一圈一圈往外擴
- DFS: 一條路一路鑽到底

## Data Structure Connection

DFS 和 BFS 的差異，不只是「兩個演算法名字不同」，而是它們背後使用的資料結構不同：

- DFS 常和 stack / recursion 對應
- BFS 常和 queue 對應

這也是為什麼資料結構和演算法最好一起學。

## Practical Reminders

- tree / graph traversal 的核心不是背模板，而是理解拜訪順序。
- graph 問題幾乎都要先想 `visited` 如何管理。
- 如果題目在問「最近、最少步數、按層展開」，BFS 常是很好的第一候選。

[Back to Computer Science Foundations](README.md)
