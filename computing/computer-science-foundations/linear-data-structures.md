[Computing](../README.md) › [CS 基礎](README.md) › 線性資料結構

# 線性資料結構 (Linear Data Structures)

線性資料結構的元素沿單一路徑排列，每個元素只與前後相鄰。它們的差別在於**允許在哪裡新增、移除、存取**；這些限制不是缺點，而是定義了結構的行為，讓某些流程變得自然。非線性的樹、堆積、雜湊表、圖見 [非線性資料結構](non-linear-data-structures.md)。

## 比較

| 結構 | 存取規則 | 索引存取 | 頭部插入 / 刪除 | 尾部插入 / 刪除 | Python |
| --- | --- | --- | --- | --- | --- |
| 陣列 / 動態陣列 (array) | 連續記憶體，依索引 | `O(1)` | `O(n)`（後面全部搬移） | `O(1)` 攤銷 | `list`、NumPy `ndarray` |
| 鏈結串列 (linked list) | 從頭沿指標逐一走 | `O(n)` | `O(1)` | `O(1)`（有尾指標時） | 少直接用 |
| 堆疊 (stack) | 只在頂端進出，LIFO | — | — | `O(1)` | `list` 的 `append` / `pop` |
| 佇列 (queue) | 尾端進、前端出，FIFO | — | `O(1)` 出 | `O(1)` 進 | `collections.deque` |
| 雙端佇列 (deque) | 兩端都可進出 | `O(n)` | `O(1)` | `O(1)` | `collections.deque` |

> 用 `list.pop(0)` 當佇列是常見的效能陷阱：每次都要把後面所有元素往前搬，`O(n)`。改用 `deque.popleft()`。

## 鏈結串列 (Linked List)

元素不放在連續記憶體，而是每個節點存自己的資料與指向下一個節點的參考。

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None          # 雙向鏈結串列再加 self.prev

head = Node("a"); head.next = Node("b"); head.next.next = Node("c")
node = head
while node:                       # 走訪：只能從頭沿指標前進
    print(node.data)
    node = node.next
```

| 類型 | 指標 | 取捨 |
| --- | --- | --- |
| 單向 (singly) | 只指向下一個 | 簡單、省記憶體 |
| 雙向 (doubly) | 前後都指 | 可往回走、刪除已知節點 `O(1)`；多一個指標的開銷 |

| 適合 | 不適合 |
| --- | --- |
| 在已知節點附近頻繁插入 / 刪除（不必搬動後面的元素） | 需要依索引隨機存取第 i 個 |
| 實作堆疊、佇列、LRU 快取 | 需要快取友善的連續掃描（陣列快很多） |
| 上一頁 / 下一頁、播放清單 | — |

## 堆疊 (Stack)：LIFO

後進先出 (Last-In, First-Out)：最後放進去的最先拿出來。

| 操作 | 意義 | Python `list` |
| --- | --- | --- |
| `push` | 放到頂端 | `s.append(x)` |
| `pop` | 從頂端取出 | `s.pop()` |
| `peek` | 看頂端不移除 | `s[-1]` |

```python
def balanced(text):                       # 括號是否成對：典型的堆疊問題
    pairs, stack = {")": "(", "]": "[", "}": "{"}, []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack

balanced("f(a[i], {b})")    # True
balanced("(]")              # False
```

用途：函式呼叫堆疊 (call stack，遞迴太深會 stack overflow / Python `RecursionError`)、復原 (undo)、運算式解析、括號比對、[DFS](graph-traversal.md)。

## 佇列 (Queue)：FIFO

先進先出 (First-In, First-Out)：最早放進去的最先移除。

```python
from collections import deque

q = deque()
q.append("task_a")          # enqueue：尾端加入
q.append("task_b")
q.popleft()                 # dequeue：前端取出 → 'task_a'
q[0]                        # peek → 'task_b'

recent = deque(maxlen=3)    # 固定長度：滿了自動丟掉最舊的（滑動視窗）
```

| 用途 | 例子 |
| --- | --- |
| 依到達順序處理工作 | 工作排程、[Slurm](../workflow-engines/README.md) 等批次系統的等待佇列 |
| 生產者 / 消費者 | 多執行緒用 `queue.Queue`（thread-safe）；多程序用 `multiprocessing.Queue` |
| 逐層擴展 | [BFS](graph-traversal.md) |
| 緩衝 | 串流資料、訊息佇列 (Kafka、RabbitMQ) |

> 先問資料怎麼流動（最新的先處理？依到達順序？要隨機存取？），再選結構；Python `list` 很方便，但不是所有情境的最佳選擇。
