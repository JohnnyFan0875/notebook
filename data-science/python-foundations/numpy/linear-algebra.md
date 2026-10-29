[Python Foundations](../README.md) › [NumPy](README.md) › 線性代數

# 線性代數 (Linear Algebra)

迴歸、PCA、距離計算、神經網路底層都是矩陣運算。這篇是 `np.linalg` 的用法；概念（秩、特徵分解、SVD 的幾何意義）見 [線性代數基礎](../../statistics/multivariate-analysis/linear-algebra-foundations.md)。

## 乘積

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
c = np.array([1, 2, 3])
d = np.array([4, 5, 6])

A @ B                    # [[19 22] [43 50]]：矩陣乘法（同 np.matmul、2D 時同 np.dot）
A * B                    # [[ 5 12] [21 32]]：element-wise，不是矩陣乘法
c @ d                    # 32：向量內積 1·4 + 2·5 + 3·6
np.inner(A, B)           # [[17 23] [39 53]]：A 的列 · B 的列（= A @ B.T）
np.outer(c, d)           # 3×3：c[i] * d[j]
np.cross(c, d)           # [-3  6 -3]：3D 外積，垂直於 c 與 d
np.einsum("ij,jk->ik", A, B)   # 用索引記號寫任意乘積；batch 運算時很好用
```

| 函式 | 運算 | 注意 |
| --- | --- | --- |
| `@` / `np.matmul` | 矩陣乘法；>2D 時視為一疊矩陣（batch） | 推薦寫法 |
| `np.dot` | 1D 內積、2D 矩陣乘法 | >2D 行為與 `@` 不同，避免 |
| `*` | element-wise | 從 MATLAB / R 過來最常搞混（R 的 `%*%` 才是矩陣乘法） |
| `np.inner` / `np.outer` | 內積 / 外積 | |

## 解線性方程組

```python
b = np.array([5, 11])

np.linalg.solve(A, b)        # [1. 2.]：解 Ax = b（x + 2y = 5, 3x + 4y = 11）
np.linalg.inv(A)             # [[-2.   1. ] [ 1.5 -0.5]]
np.linalg.inv(A) @ b         # 結果相同，但較慢且數值較不穩定
np.linalg.det(A)             # -2.0000000000000004：浮點誤差，比較用 np.isclose
np.linalg.matrix_rank(A)     # 2

# 最小平方法：方程式比未知數多（迴歸）
X = np.column_stack([np.ones(4), [1, 2, 3, 4]])   # 截距 + 一個特徵
y = np.array([2.1, 3.9, 6.2, 7.8])
coef, *_ = np.linalg.lstsq(X, y, rcond=None)      # [0.15 1.94]：截距、斜率
```

> 不要用 `inv(A) @ b` 解方程式；用 `solve`（方陣）或 `lstsq`（迴歸、非方陣）。`inv` 只在真的需要反矩陣本身時用（例如共變異數矩陣的逆）。p > n 時 `XᵀX` 不可逆，需要正則化，見 [正則化](../../machine-learning/foundations/regularization.md)。

## 特徵分解與 SVD

```python
w, v = np.linalg.eig(A)      # w: [-0.372  5.372]；v 的每一「欄」是一個特徵向量
                             # NumPy 2.x 回傳 complex dtype（虛部 0），需要實數時取 .real

S = np.array([[2, 1], [1, 2]])          # 對稱矩陣（如共變異數矩陣）
w, v = np.linalg.eigh(S)                # [1. 3.]：實數、由小到大排序 → 對稱矩陣一律用 eigh

U, s, Vt = np.linalg.svd(X, full_matrices=False)   # X = U @ np.diag(s) @ Vt
np.linalg.norm(c)                       # 3.742：L2 norm
np.linalg.norm(c, ord=1)                # 6.0：L1 norm
```

| 函式 | 用途 |
| --- | --- |
| `eig` | 一般方陣的特徵值 / 向量 |
| `eigh` | 對稱 / Hermitian 矩陣：更快、保證實數、已排序 |
| `svd` | 任何矩陣；PCA 的實際計算方式（對中心化資料做 SVD，比對共變異數矩陣做 `eigh` 數值更穩） |
| `norm` | 向量長度、矩陣範數；L1 / L2 正則化的懲罰項 |

PCA 的實作與解讀見 [PCA](../../statistics/multivariate-analysis/pca.md)。資料大且稀疏（單細胞計數矩陣）時，改用 [`scipy.sparse`](../scipy-sparse.md) 與 `scipy.sparse.linalg.svds`，不要轉成稠密 array。
