[Python Foundations](../README.md) › [NumPy](README.md) › Array 基礎

# Array 基礎 (Array Basics)

`ndarray` 是「同一種 `dtype`、固定 `shape` 的多維數值陣列」。拿到任何 array，先看 `shape`、`ndim`、`dtype`，通常比印出內容更快判斷下一步。

## 屬性 (Properties)

```python
import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])

arr.shape, arr.ndim, arr.size, arr.dtype   # ((2, 3), 2, 6, dtype('int64'))
arr.itemsize, arr.nbytes                   # (8, 48)：每個元素 8 bytes，共 48 bytes
type(arr)                                  # numpy.ndarray
```

| 屬性 | 意義 | 例 |
| --- | --- | --- |
| `shape` | 各軸 (axis) 長度的 tuple | `(2, 3)` = 2 列 × 3 欄 |
| `ndim` | 軸數 | `2` |
| `size` | 元素總數 = `shape` 的乘積 | `6` |
| `dtype` | 元素型別 | `int64`、`float32`、`bool` |
| `nbytes` | 資料佔用的記憶體 | `size × itemsize` |

## dtype

`dtype` 決定記憶體用量、數值精度，以及下游套件能不能直接吃（PyTorch 預設 `float32`、sklearn 多半轉成 `float64`）。

| 類別 | 常見 dtype | 注意 |
| --- | --- | --- |
| 整數 | `int8` / `int32` / `int64`、`uint8` | **溢位不報錯，直接繞回** |
| 浮點 | `float32` / `float64` | `float32` 只有約 7 位有效數字 |
| 布林 | `bool` | 加總 = 計數、平均 = 比例 |
| 字串 / 物件 | `<U10`、`object` | `object` array 失去向量化速度，表格字串改用 pandas |

```python
np.array([1, 2]).dtype                          # int64（NumPy 2 起 Windows 也是 int64；1.x 在 Windows 是 int32）
np.array([1, 2.5]).dtype                        # float64：混合時向上轉型 (upcasting)
np.array([1, 2], dtype=np.float32)

# 1. 整數溢位：影像 (uint8) 相加最常踩到
np.array([200], dtype=np.uint8) + np.uint8(100)   # [44]  不是 300
np.array([127], dtype=np.int8) + 1                # [-128]
img.astype(np.int16) + 100                        # 先轉大型別再算

# 2. 浮點誤差：比較用 isclose，不要用 ==
0.1 + 0.2 == 0.3                                  # False
np.isclose(0.1 + 0.2, 0.3)                        # True
np.float32(16_777_217)                            # 16777216.0：float32 存不下所有 > 2**24 的整數

# 3. 轉型會產生新 array
arr.astype(np.float32)
```

> 計數資料（reads、UMI）用 `int64` 或 `float64` 存，不要為了省記憶體用 `int16`：深度大的樣本會溢位且沒有任何警告。

## 建立 Array

```python
np.array([[2, 3], [9, 0], [1, 4]])     # list of lists → 2D，shape (3, 2)

# 1. 等差 / 等比序列
np.arange(0, 10, 2)                    # [0 2 4 6 8]：不含終點，同 range()
np.linspace(0, 1, 5)                   # [0.   0.25 0.5  0.75 1.  ]：含終點，指定「個數」
np.logspace(0.1, 1, 5)                 # [ 1.26  2.11  3.55  5.96 10.  ]：10**linspace(0.1, 1, 5)
np.arange(0, 2 * np.pi, 0.01)          # 畫連續函數的 x 軸

# 2. 初始化
np.zeros((2, 3))                       # 全 0（float64）
np.ones((3,)) * 7                      # [7. 7. 7.]
np.full((2, 2), np.nan)                # 指定值
np.eye(3)                              # 單位矩陣
np.zeros_like(arr)                     # 與 arr 同 shape、同 dtype
np.empty((1000, 1000))                 # 不初始化（內容是垃圾值），之後一定會全部覆寫時才用

# 3. 唯一值與次數
sample = np.array([1, 2, 2, 3, 4, 4, 5, 6])
values, counts = np.unique(sample, return_counts=True)
values, counts                         # [1 2 3 4 5 6], [1 2 1 2 1 1]
dict(zip(values.tolist(), counts.tolist()))   # {1: 1, 2: 2, 3: 1, 4: 2, 5: 1, 6: 1}
```

`linspace` 給「點數」、`arange` 給「步長」；浮點步長的 `arange` 可能因誤差多或少一個點，需要精確點數時用 `linspace`。隨機 array 見 [隨機與統計](random-and-statistics.md#用-default_rng-抽樣)。

## 索引與切片 (Indexing & Slicing)

依位置與軸存取；需要依欄名、標籤選取時改用 [pandas 選取](../pandas/selection.md)。

```python
arr = np.arange(10)                    # [0 1 2 3 4 5 6 7 8 9]
arr[2:7]                               # [2 3 4 5 6]：start 包含、stop 不包含
arr[:5], arr[-1], arr[::2], arr[::-1]  # 前 5 個、最後一個、每隔一個、反轉

m = np.array([[1, 2, 3], [4, 5, 6]])
m[0, 1]                                # 2：列 0、欄 1
m[:, 1]                                # [2 5]：整欄 → shape (2,)
m[:, [1]]                              # [[2] [5]]：用 list 保留維度 → shape (2, 1)
m[1, 1:3]                              # [5 6]
m[0][2]                                # 3：可行，但先產生中間 array，慢且在賦值時易出錯；用 m[0, 2]

# 布林索引：篩選與條件賦值
arr[arr % 2 == 0]                      # [0 2 4 6 8]
m[m > 4] = 0                           # 符合條件的位置整批改值

# Fancy indexing：用整數 array 指定位置
m[[0, 1], [2, 0]]                      # [3 4]：取 (0,2) 與 (1,0)
```

| MATLAB / R | NumPy | 差異 |
| --- | --- | --- |
| `v(5:end)` / `v[5:length(v)]` | `v[4:]` | 0-based |
| `A(2:4, 1:2)` | `A[1:4, 0:2]` | 右邊界不包含 |
| `A(:, 2)` 保持欄向量 | `A[:, 1]` 變 1D | 要保留維度用 `A[:, [1]]` 或 `A[:, 1:2]` |
| `v[-1]`（R：刪掉第 1 個） | `v[-1]`（最後一個） | 負索引語意完全不同 |

## View vs Copy

切片 (slicing) 回傳的是 **view**：與原 array 共用同一塊記憶體，改 view 會改到原資料。這能省記憶體，但也是最常見的「我沒改它，它怎麼變了」來源。

| 操作 | 結果 | 改它會影響原 array？ |
| --- | --- | --- |
| 基本切片 `a[1:4]`、`a[:, 0]`、`a[::2]` | view | **會** |
| `reshape`、`.T`、`ravel()`（可行時） | view | **會** |
| 布林索引 `a[a > 0]`、fancy indexing `a[[0, 2]]` | copy | 不會 |
| `astype()`、`flatten()`、算術結果 `a + 1` | copy | 不會 |
| `.copy()` | copy | 不會 |

```python
a = np.arange(6)
v = a[1:4]
v[0] = 99
a                                      # [ 0 99  2  3  4  5]  原 array 被改到

np.shares_memory(a, v)                 # True
np.shares_memory(a, a[[1, 2]])         # False：fancy indexing 是 copy
a.reshape(2, 3).base is a              # True：.base 不是 None 代表是 view

sub = a[1:4].copy()                    # 要獨立修改就明確 copy

# 大 array 取一小段後想釋放原本的記憶體，也要 copy（view 會讓整塊原資料留在記憶體）
small = big[:100].copy(); del big
```

> 布林遮罩在等號**左邊**（`a[mask] = 0`）是直接寫回原 array；在右邊（`b = a[mask]`）是產生 copy。pandas 的對應問題見 [pandas 修改資料](../pandas/modifying.md#view-vs-copy-與-copy-on-write)。

## 常見錯誤

| 症狀 | 原因 | 解法 |
| --- | --- | --- |
| 切片少一個元素 | stop 不包含 | `a[i:j]` 讀成「從 i 到 j 之前」 |
| 取一欄後 shape 從 `(n, 1)` 變 `(n,)` | 整數索引會移除該軸 | `a[:, [k]]` 或 `a[:, k:k+1]` |
| 修改切片後原資料也變了 | 切片是 view | `.copy()` |
| `IndexError: boolean index did not match` | 遮罩 shape 與 array 不同 | 確認遮罩來自同一個 array 的同一軸 |
| 影像相加後顏色怪異 | `uint8` 溢位 | 先 `astype(np.int16)` 或 `float32` |
