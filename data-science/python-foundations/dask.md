# Dask

## Overview

Dask 是 Python 生態中常見的平行與延遲執行工具，特別適合這兩種情境：

- 單機有多核心，但原本的 NumPy / pandas 工作流跑太慢
- 資料大到不想一次全部載入記憶體，想改成 partitioned、lazy 的執行模式

它的核心想法不是「把所有 Python 程式自動變快」，而是：

- 把工作拆成很多小任務
- 組成 task graph
- 交給 scheduler 用 threads 或 processes 執行
- 在真正需要結果時才 `compute()`

## Mental Model

可以先把 Dask 想成 NumPy / pandas 的平行版本，但這個說法只對一半。

更準確地說，Dask 提供兩層能力：

1. 高階 collection API
2. 底層 task scheduling

高階 collection 常見有：

- `dask.array`: 類似 NumPy array
- `dask.dataframe`: 類似 pandas DataFrame
- `dask.bag`: 適合非結構化或半結構化資料

而這些物件的共同特性是：

- 通常是 lazy evaluation
- 底層由多個 partition 或 chunk 組成
- 多數操作先建立任務，不會立刻算出結果

## Why Dask Feels Different from NumPy

NumPy 常見寫法是立刻建立完整陣列並直接計算：

```python
import numpy as np

x = np.ones((4000, 6000))
result = x.sum()
```

Dask array 則會把資料切成 chunks，並延後真正運算：

```python
import dask.array as da

x = da.ones((4000, 6000), chunks=(1000, 2000))
result = x.sum()

print(result)            # 還是 lazy object
print(result.compute())  # 真正執行
```

重點差異是：

- NumPy 預設 eager
- Dask 預設 lazy
- Dask 的 chunk 大小會直接影響平行度、排程成本與記憶體使用

## Chunking

`chunks=` 是理解 Dask array 的關鍵。

```python
x = da.ones((4000, 6000), chunks=(1000, 2000))
```

這代表一個大陣列會被切成很多較小區塊，Dask 再對每個區塊分別安排任務。

chunk 太大時：

- 平行度不夠
- 單一任務記憶體壓力高

chunk 太小時：

- scheduler overhead 會變大
- 任務太碎，反而不划算

所以 Dask 效能通常不是只看「有沒有平行化」，而是也很看 chunk 設計是否合理。

## Delayed Execution

如果你的工作流不是 array / dataframe 風格，而是一連串自訂 Python 函數，可以用 `dask.delayed()`。

```python
import dask

@dask.delayed
def load_data(path):
    return open(path).read()

@dask.delayed
def count_lines(text):
    return len(text.splitlines())

total = count_lines(load_data("example.txt"))
result = total.compute()
```

這種模式適合：

- 自訂 ETL pipeline
- 多步驟資料處理
- 想保留普通 Python 函數寫法，但又希望交給 Dask 排程

## Dask Bag

當資料不是整齊表格，而是：

- 文字評論清單
- JSON / dict list
- 半結構化事件資料

這時 `dask.bag` 比較合適。

```python
import dask.bag as db

reviews = [
    "Really good service",
    "Second time we've stayed here",
    "Great older hotel"
]

bag = db.from_sequence(reviews, npartitions=2)
lengths = bag.map(len)

print(lengths.compute())
```

可以把 bag 想成「可平行處理的 sequence」，特別適合 map / filter / fold 類型操作。

## Scheduler Choice

Dask 的其中一個重要選項是 scheduler。

常見觀念是：

- threads: 常用於 `dask.array`、`dask.dataframe`、`dask.delayed`
- processes: 常見於 `dask.bag`

可以顯式指定：

```python
result = x.compute(scheduler="threads")
result = x.compute(scheduler="processes")
```

或：

```python
import dask

result = dask.compute(x, scheduler="threads")
```

選擇時可以先抓大方向：

- 如果底層主要是 NumPy / pandas / C-extension 工作，threads 常常夠用
- 如果工作更偏 Python-level object processing，processes 可能更適合

但最終仍要看工作負載，不要只靠直覺。

## Dask vs Multiprocessing

它們都能利用多核心，但抽象層次不同。

`multiprocessing` 比較像：

- 你自己管理 process
- 自己決定 function 如何分派
- 自己處理很多流程細節

Dask 比較像：

- 你描述資料或任務依賴
- Dask 幫你建立 task graph
- scheduler 幫你安排執行

所以如果需求只是「把同一個 function 套到很多輸入」，`multiprocessing.Pool` 可能就夠了。  
如果需求已經進到 chunked arrays、lazy pipelines、半結構化資料處理，Dask 通常更自然。

## Common Pitfalls

- 忘記 `compute()`，以為結果已經真的算出來
- 沒有理解 chunk / partition 對效能的影響
- 小資料也硬上 Dask，結果排程成本大於收益
- 把 Dask 當成所有 Python 程式的自動加速器
- 沒有區分 threads 與 processes 的適用情境

## Practical Takeaway

Dask 最值得掌握的，不是某個單一 API，而是這個工作流：

1. 選對 collection 類型
2. 設計合理的 chunks 或 partitions
3. 先建立 lazy pipeline
4. 在真正需要輸出時才 `compute()`
5. 根據工作型態調整 scheduler

當你已經熟悉 NumPy、pandas 和 `multiprocessing` 的限制後，Dask 會是很自然的下一步。
