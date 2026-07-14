# Search Algorithms

搜尋演算法的核心問題很單純：

- 給你一個 collection
- 給你一個 target
- 判斷 target 在不在裡面，或它在哪裡

最常見的入門比較是 linear search 和 binary search。

## Linear Search

linear search 的做法是從頭掃到尾，逐一比較。

```python
def linear_search(values, target):
    for i, value in enumerate(values):
        if value == target:
            return i
    return -1
```

### 特性

- 不需要排序
- 寫法直接
- 最壞情況要看完整個序列

時間複雜度：

- best case: `O(1)`，第一個元素就找到
- worst case: `O(n)`，最後才找到或根本不存在

## Binary Search

binary search 的前提是資料已排序。

它每一步都看中間值，然後把搜尋範圍砍掉一半。

```python
def binary_search(values, target):
    left, right = 0, len(values) - 1

    while left <= right:
        mid = (left + right) // 2

        if values[mid] == target:
            return mid
        if values[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

### 特性

- 需要 sorted data
- 每次排除一半搜尋空間
- 在大集合裡通常比 linear search 快很多

時間複雜度：

- best case: `O(1)`
- worst case: `O(log n)`

Key point: binary search 的快，不是因為「比較聰明」，而是因為它利用了排序這個前提。

## Recursive View of Binary Search

binary search 也很適合拿來理解 recursion，因為每次都把問題縮成更小的子區間。

```python
def binary_search_recursive(values, target, left, right):
    if left > right:
        return -1

    mid = (left + right) // 2
    if values[mid] == target:
        return mid
    if values[mid] < target:
        return binary_search_recursive(values, target, mid + 1, right)
    return binary_search_recursive(values, target, left, mid - 1)
```

## When Linear Search Is Still Fine

不要因為 binary search 漂亮，就以為 linear search 沒用。

linear search 仍然很合理 when:

- 資料量很小
- 資料沒排序
- 只搜尋一次，不值得先排序
- 來源是 stream 或 iterator，不能任意跳索引

## A Useful Tradeoff Question

如果資料還沒排序，binary search 的真實問題其實變成：

- 你要搜尋幾次？
- 排序成本值不值得？

如果只查一次，小資料時直接 linear search 往往更簡單。
如果會重複查很多次，先排序再 binary search 通常更划算。

## Practical Reminders

- binary search 的前提是排序，不是可選優化。
- 先搞清楚資料是否可 random access，才能判斷 binary search 是否自然。
- 在真實程式裡，很多「搜尋快不快」其實是資料結構選擇問題，不只是演算法名稱問題。

[Back to Computer Science Foundations](README.md)
