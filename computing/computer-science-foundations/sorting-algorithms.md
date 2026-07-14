# Sorting Algorithms

sorting algorithm 的目標是把一組無序資料整理成有序資料，例如升冪、降冪或自訂規則順序。

排序常常不是最終目的，而是後續操作的準備步驟，例如：

- 更快搜尋
- 更穩定比較
- 更容易合併或去重

## Four Useful Teaching Examples

### Bubble Sort

bubble sort 反覆比較相鄰元素，順序錯了就交換。

```python
def bubble_sort(values):
    items = values[:]
    n = len(items)

    for end in range(n - 1, 0, -1):
        for i in range(end):
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
    return items
```

特點：

- 很直觀
- 適合教學
- 大資料時效率差

典型複雜度：

- worst case: `O(n^2)`

### Selection Sort

selection sort 每輪找出剩餘區間中的最小值，放到前面。

```python
def selection_sort(values):
    items = values[:]

    for i in range(len(items)):
        min_idx = i
        for j in range(i + 1, len(items)):
            if items[j] < items[min_idx]:
                min_idx = j
        items[i], items[min_idx] = items[min_idx], items[i]
    return items
```

特點：

- 思路清楚
- 交換次數通常不多
- 仍然是 quadratic family

### Insertion Sort

insertion sort 把每個新元素插入前面已排序區間的正確位置。

```python
def insertion_sort(values):
    items = values[:]

    for i in range(1, len(items)):
        key = items[i]
        j = i - 1
        while j >= 0 and items[j] > key:
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = key
    return items
```

特點：

- 小資料或近乎排序資料時常不錯
- 很適合理解「維持局部有序」

### Merge Sort

merge sort 使用 divide and conquer：

1. 把序列切成更小子序列
2. 各自排序
3. 再把兩個已排序結果 merge 起來

```python
def merge_sort(values):
    if len(values) <= 1:
        return values

    mid = len(values) // 2
    left = merge_sort(values[:mid])
    right = merge_sort(values[mid:])

    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
```

特點：

- 結構清楚
- 擴展性比 `O(n^2)` 類演算法好很多
- 通常需要額外記憶體來 merge

典型複雜度：

- `O(n log n)`

## Quicksort Intuition

quicksort 也屬於 divide and conquer，但不是先切半再合併，而是：

1. 選 pivot
2. 把小於 pivot 的放左邊，大於 pivot 的放右邊
3. 對左右子區間遞迴處理

Key point: quicksort 平均情況很強，但效能很依賴 partition 品質與 pivot 選擇。

## Why `O(n log n)` Matters

當資料變大時，`O(n^2)` 和 `O(n log n)` 的差距會很快放大。

所以 practical lesson 通常不是：

- 背哪個排序「最強」

而是：

- 小資料時簡單方法常夠用
- 大資料時成長率決定可不可行

## Which Sort Teaches What

| Algorithm | Best teaching value |
| --- | --- |
| Bubble sort | adjacent swaps and repeated passes |
| Selection sort | choosing the next correct element |
| Insertion sort | maintaining a sorted prefix |
| Merge sort | divide and conquer |
| Quicksort | partitioning around a pivot |

## Practical Reminder

在 Python 實務裡，你通常直接用內建 `sorted()` 或 `.sort()`，因為標準庫實作已經很成熟。

學排序演算法的目的，多半是：

- 理解 complexity
- 建立 divide-and-conquer 直覺
- 看懂不同資料流程的 tradeoff

[Back to Computer Science Foundations](README.md)
