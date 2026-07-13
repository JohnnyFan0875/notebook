# Linear Data Structures

Linear data structures 的核心特徵是：元素沿著單一路徑排列，每個元素通常只和前後鄰居直接相關。

常見例子包括：

- linked list
- stack
- queue

這些結構很基礎，但它們對 insertion / removal 的位置限制不同，所以適合的任務也不同。

## Linked Lists

linked list 不是把元素放在連續記憶體裡，而是讓每個節點持有：

- 自己的資料
- 指向下一個節點的參考

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
```

### Singly vs. Doubly Linked List

| Type | Main idea | Tradeoff |
| --- | --- | --- |
| Singly linked list | each node points to the next node | simpler, less memory |
| Doubly linked list | each node points both forward and backward | easier backward traversal, more overhead |

linked list 的重點不是「比較高級」，而是：

- 在已知位置附近插入 / 刪除時很自然
- 不需要整段搬動後面的元素
- 但隨機存取很弱，不能像 array 一樣直接跳到第 `i` 個位置

### Linked Lists Are Good For

- dynamic insertion / deletion
- implementing stacks and queues
- navigation-style structures such as previous / next history

常見直覺例子：

- browser back / forward history
- playlist navigation
- other pointer-based data structures

## Stacks

stack 的規則是 `LIFO`:

- Last-In, First-Out

也就是最後放進去的元素，最先被拿出來。

常見操作：

- `push`: 放到頂端
- `pop`: 從頂端取出
- `peek`: 看頂端但不移除

```python
class Stack:
    def __init__(self):
        self.items = []

    def push(self, value):
        self.items.append(value)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]
```

### Stack Mental Model

stack 很適合處理「最近加入的東西先處理」的問題，例如：

- function call stack
- undo history
- expression parsing
- DFS-style traversal

Key point: stack 的限制不是缺點，而是它的行為定義。只允許頂端進出，讓某些流程變得非常自然。

## Queues

queue 的規則是 `FIFO`:

- First-In, First-Out

也就是最早放進去的元素，最先被移除。

常見操作：

- `enqueue`: 從尾端加入
- `dequeue`: 從前端取出
- `peek`: 看前端元素

```python
from collections import deque

q = deque()
q.append("task_a")      # enqueue
q.append("task_b")
first = q.popleft()     # dequeue
```

### Queue Mental Model

queue 很適合處理：

- tasks waiting in order
- producer / consumer pipelines
- BFS traversal
- scheduling and buffering

如果你用 Python，實務上通常比起自己手寫 queue 類別，更常直接使用：

- `collections.deque`
- `queue.SimpleQueue`
- 其他 thread-safe queue variants

## Choosing Between Them

| Structure | Access rule | Best intuition |
| --- | --- | --- |
| Linked list | follow links node by node | flexible insertion around known nodes |
| Stack | top only, LIFO | last thing in should be handled first |
| Queue | front out, back in, FIFO | process things in arrival order |

## Practical Reminders

- Python `list` 很方便，但不代表它是所有資料結構教學概念的最佳替代品。
- data structure 的價值，常來自它限制了哪些操作應該合法。
- 先問資料會怎麼流動，再選結構，而不是先背名稱。

[Back to Computer Science Foundations](README.md)
