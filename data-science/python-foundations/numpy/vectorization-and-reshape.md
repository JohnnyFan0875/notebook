[Python Foundations](../README.md) › [NumPy](README.md) › 向量化與 Reshape

# 向量化與 Reshape (Vectorization, Broadcasting & Reshape)

向量化 (vectorization) 是把「對每個元素做一次」寫成「對整個 array 做一次」，迴圈交給 NumPy 的 C 實作。broadcasting 決定不同 shape 的 array 怎麼配對，reshape 系列則把資料整理成函式或模型要的形狀。

## list vs ndarray

| | Python `list` | NumPy `ndarray` |
| --- | --- | --- |
| 定位 | 通用容器，可放不同型別 | 同一 `dtype` 的數值陣列 |
| `+` / `*` | 串接 / 重複 | element-wise 運算 |
| 多維索引 | `x[i][j]` | `x[i, j]` |
| 大量數值運算 | 慢（每個元素都是 Python 物件） | 快（連續記憶體 + C 迴圈） |

```python
import numpy as np

height = [1.73, 1.68, 1.71]
weight = [65.4, 59.2, 63.6]
# weight / height                      # TypeError：list 不支援 element-wise 運算
bmi = np.array(weight) / np.array(height) ** 2   # [21.85 20.98 21.75]
[1, 2] * 2                             # [1, 2, 1, 2]
np.array([1, 2]) * 2                   # [2 4]
```

## Element-wise 運算

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

a + b, a - b, a * b, a / b             # [5 7 9] [-3 -3 -3] [ 4 10 18] [0.25 0.4  0.5 ]
a ** 2, b // a, b % a                  # [1 4 9] [4 2 2] [0 1 0]
np.add(a, b), np.multiply(a, b)        # 運算子的函式版（可用 out=、where= 參數）
np.remainder(a, b)                     # [1 2 3]：同 a % b
np.sqrt(a), np.exp(a), np.log(a)       # ufunc：逐元素數學函式
np.array([True, 1, 2]) + np.array([3, 4, False])   # [4 5 2]：True=1、False=0
```

## Broadcasting

shape 不同的 array 運算時，NumPy 從**最後一軸往前**逐軸比對：

```text
規則：兩軸長度相等，或其中一個是 1（或不存在）→ 可以配對；長度 1 的軸會被「拉伸」

X:        (3, 2)          X:        (3, 2)          x[:, None]: (3, 1)
mean:        (2,)         v:           (3,)         x[None, :]: (1, 3)
結果:     (3, 2) ✓        比對 2 vs 3 → 錯誤 ✗       結果:       (3, 3) ✓ 外積式
```

```python
X = np.arange(6).reshape(3, 2)         # 3 個樣本 × 2 個特徵
X - X.mean(axis=0)                     # 每欄減欄平均：(3, 2) - (2,) → 中心化
(X - X.mean(axis=0)) / X.std(axis=0)   # 標準化 (z-score)

# 每列減列平均：要把 (3,) 變成 (3, 1)
X - X.mean(axis=1, keepdims=True)      # keepdims=True 保留被彙總的軸
X - X.mean(axis=1)[:, None]            # 等價：None / np.newaxis 插入長度 1 的軸

x = np.arange(3)
x[:, None] + x[None, :]                # [[0 1 2] [1 2 3] [2 3 4]]：所有配對

np.ones((3, 2)) + np.ones(3)           # ValueError: operands could not be broadcast together with shapes (3,2) (3,)
```

| `axis` | 方向 | `X` 為 (樣本 × 特徵) 時的意義 |
| --- | --- | --- |
| `axis=0` | 沿列往下彙總 → 每**欄**一個值 | 每個特徵的平均 |
| `axis=1` | 沿欄往右彙總 → 每**列**一個值 | 每個樣本的平均 |

> 生資表達矩陣常是「基因 × 樣本」，sklearn 預期「樣本 × 特徵」。先確認方向再選 `axis`，必要時 `.T`；做錯通常不會報錯，只是算出錯的東西。

## 布林運算與遮罩

```python
arr = np.array([1, 2, 3, 4, 5])
arr > 2                                # [False False  True  True  True]
arr[arr > 2]                           # [3 4 5]
(arr > 2).sum(), (arr > 2).mean()      # 3, 0.6：計數與比例
np.any(arr > 4), np.all(arr > 0)       # True, True

my_house = np.array([18.0, 20.0, 10.75, 9.50])
your_house = np.array([14.0, 24.0, 14.25, 9.0])
my_house[(my_house > 18.5) | (my_house < 10)]       # [20.   9.5]：| & ~，每個條件加括號
np.logical_and(my_house < 11, your_house < 11)      # [False False False  True]

# 條件賦值
np.where(arr > 2, "high", "low")                    # 二選一
np.select([arr < 2, arr < 4], ["s", "m"], default="l")   # 多條件，依序取第一個成立的
np.clip(arr, 2, 4)                                  # [2 2 3 4 4]：截斷到範圍內
```

`and` / `or` / `not` 只能用在單一布林值，用在 array 會出現 `ValueError: The truth value of an array ... is ambiguous`。

## 迭代

真的需要逐元素處理時，先想能不能向量化；不行再考慮 [Numba](../performance-and-scaling/efficient-python.md#迴圈無法避免時numba)。

```python
b = np.arange(8).reshape(2, 2, 2)
for row in b:                          # 只沿第 0 軸迭代，每次拿到 (2, 2)
    ...
for x in np.nditer(b):                 # 逐元素：0 1 2 ... 7
    ...
for x in b.ravel():                    # 同上，較常用
    ...
for idx, x in np.ndenumerate(b):       # 同時拿到索引 (i, j, k)
    ...
```

## Reshape 與轉置

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

arr.reshape(3, 2)                      # [[1 2] [3 4] [5 6]]：元素總數必須相同
arr.reshape(2, -1)                     # -1 由 NumPy 推算
arr.reshape(-1)                        # [1 2 3 4 5 6]：攤平（盡量回傳 view）
arr.ravel(), arr.flatten()             # 攤平：ravel 盡量 view，flatten 一定 copy
arr.T                                  # 轉置 → (3, 2)

img = np.zeros((100, 200, 3))          # (height, width, channels)
np.transpose(img, axes=(2, 0, 1)).shape   # (3, 100, 200)：channels-last → channels-first（PyTorch 慣例）
np.moveaxis(img, -1, 0).shape             # 同上，較易讀

x = np.zeros((5, 1, 3))
np.squeeze(x).shape                    # (5, 3)：移除長度 1 的軸
np.expand_dims(np.zeros(3), 0).shape   # (1, 3)：插入新軸（同 x[None, :]）

np.flip(arr, axis=0)                   # [[4 5 6] [1 2 3]]：上下翻
np.flip(arr, axis=1)                   # [[3 2 1] [6 5 4]]：左右翻
```

`reshape` 預設按列 (C order) 讀寫元素；從 R / MATLAB（按欄，Fortran order）轉過來的資料若排列錯亂，試 `order="F"`。

高維資料先寫下每個 axis 的意義再操作：

| 資料 | 常見 shape |
| --- | --- |
| RGB 影像 | `(height, width, channels)` |
| 影像 batch（PyTorch） | `(batch, channels, height, width)` |
| 序列 batch | `(batch, seq_len, features)` |
| one-hot DNA 序列 | `(n_seqs, length, 4)` |

## 合併與分割 (Concatenate, Stack, Split)

```python
a = np.array([1, 2, 3]); b = np.array([4, 5, 6])
arr = np.array([[1, 2, 3], [4, 5, 6]])

# 1. concatenate：沿「既有」的軸接起來，其他軸長度要一致
np.concatenate([a, b])                       # [1 2 3 4 5 6]
np.concatenate([arr, arr], axis=0)           # (4, 3)：上下接
np.concatenate([arr, arr], axis=1)           # (2, 6)：左右接
np.concatenate([arr, np.array([[7, 8]])])    # ValueError：axis 1 長度 3 vs 2

# 2. stack：沿「新」的軸疊起來，所有 array shape 必須相同
np.stack([a, b])                             # (2, 3)
np.stack([a, b], axis=1)                     # (3, 2)
np.vstack([a, b])                            # (2, 3)：1D 當列
np.hstack([a, b])                            # (6,)：1D 時等同 concatenate
np.column_stack([a, b])                      # (3, 2)：1D 當欄

# 3. split：沿某軸切開（預設要能整除）
rgb = np.zeros((2, 2, 3))
r, g, bl = np.split(rgb, 3, axis=2)          # 各 (2, 2, 1)：保留被切的軸
r.squeeze(axis=2).shape                      # (2, 2)
np.stack([r[..., 0], g[..., 0], bl[..., 0]], axis=2).shape   # (2, 2, 3)：重組
np.split(rgb, 5, axis=2)                     # ValueError：無法平均切
np.array_split(np.arange(7), 3)              # [0 1 2] [3 4] [5 6]：允許不整除
```

| 想做的事 | 函式 |
| --- | --- |
| 沿既有軸接 | `concatenate`（`vstack` / `hstack` 是捷徑） |
| 多個同 shape array → 多一維 | `stack` |
| 切開 | `split`（整除）/ `array_split`（不必整除） |
| 迴圈中累積結果 | 先收進 list，最後一次 `np.concatenate` / `np.stack`；不要每圈都 concatenate（每次都複製整個 array） |

## 常見錯誤

| 錯誤訊息 / 症狀 | 原因 | 解法 |
| --- | --- | --- |
| `operands could not be broadcast together` | 尾端軸長度不同且都不是 1 | 印 `a.shape, b.shape`；用 `[:, None]` 或 `keepdims=True` 對齊 |
| 結果 shape 是 (n, n) 而不是 (n,) | `(n,)` 與 `(n, 1)` 意外 broadcast | 統一成 1D 或 2D 再算 |
| `all the input array dimensions except for the concatenation axis must match` | concatenate 的其他軸長度不同 | 先 reshape / 轉置 |
| `cannot reshape array of size 6 into shape (4,)` | 元素數不符 | 檢查 `size` |
| 轉置後資料順序怪異 | 用 `reshape` 代替 `transpose` | reshape 不交換軸，換軸要用 `transpose` / `moveaxis` |

效能比較（迴圈 vs 向量化）見 [Efficient Python](../performance-and-scaling/efficient-python.md#向量化-vectorization)。
