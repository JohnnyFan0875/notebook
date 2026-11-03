[Computing](../README.md) › [CS 基礎](README.md) › 搜尋演算法

# 搜尋演算法 (Search Algorithms)

給一個集合與目標值，判斷目標在不在、在哪裡。入門的比較是線性搜尋與二分搜尋；實務上「搜尋快不快」更常取決於資料結構（`set`、`dict`、索引），而不只是演算法名稱。

| 演算法 | 做法 | 最佳 | 最壞 | 前提 |
| --- | --- | --- | --- | --- |
| 線性搜尋 (linear search) | 從頭逐一比較 | `O(1)` | `O(n)` | 無 |
| 二分搜尋 (binary search) | 看中間值，每步排除一半 | `O(1)` | `O(log n)` | **已排序**、可隨機存取 |
| 雜湊查詢 (hash lookup) | 由 key 直接算出位置 | `O(1)` | `O(n)`（極少見） | 先建雜湊表，見 [非線性資料結構](non-linear-data-structures.md#雜湊表-hash-table) |

## 線性搜尋

```python
def linear_search(values, target):
    for i, value in enumerate(values):
        if value == target:
            return i
    return -1
```

仍然合理的時候：資料量小、沒排序且只查一次（排序要 `O(n log n)`，不划算）、資料來自 stream / iterator 無法跳著讀。

## 二分搜尋

```python
def binary_search(values, target):          # values 必須已排序
    left, right = 0, len(values) - 1
    while left <= right:
        mid = (left + right) // 2
        if values[mid] == target:
            return mid
        if values[mid] < target:
            left = mid + 1                      # 目標在右半
        else:
            right = mid - 1                     # 目標在左半
    return -1

def binary_search_recursive(values, target, left, right):   # 遞迴版：每次縮成子區間
    if left > right:
        return -1
    mid = (left + right) // 2
    if values[mid] == target:
        return mid
    if values[mid] < target:
        return binary_search_recursive(values, target, mid + 1, right)
    return binary_search_recursive(values, target, left, mid - 1)
```

n = 10⁶ 時二分搜尋最多比 20 次，線性搜尋最多比 10⁶ 次。快的原因不是演算法比較聰明，而是**利用了排序這個前提**。

| 常見錯誤 | 說明 |
| --- | --- |
| 資料沒排序就用 | 結果錯誤且不會報錯 |
| `left < right` vs `left <= right`、`mid ± 1` 寫錯 | 漏掉邊界或無限迴圈 |
| 自己手寫 | Python 用標準庫 `bisect`；NumPy 用 `np.searchsorted` |

```python
import bisect
import numpy as np

a = [3, 8, 15, 21, 42]
bisect.bisect_left(a, 21)             # 3：21 的位置（或應插入的位置）
bisect.insort(a, 10)                  # 插入並維持排序

starts = np.array([100, 500, 900])    # 已排序的區間起點
np.searchsorted(starts, [120, 950])   # [1, 3]：每個查詢值落在哪個區間之後
```

## 要先排序嗎？

| 查詢次數 | 選擇 |
| --- | --- |
| 1 次 | 線性搜尋，`O(n)` |
| k 次（k 大） | 先排序 `O(n log n)` + k 次二分 `O(k log n)`，或建 `set` / `dict` `O(n)` + k 次 `O(1)` |
| 範圍查詢（介於 a 與 b 之間） | 排序 + 二分（雜湊表做不到範圍查詢） |

> 生資例子：給定一批變異位置，查詢落在哪個基因區間。基因起點排序後用 `np.searchsorted`，或用區間樹 / [bedtools](../../biology/bioinformatics-tools/ngs-tools/bedtools.md) `intersect`；資料庫則靠 [索引](../../data-science/databases/README.md) 做同樣的事。
