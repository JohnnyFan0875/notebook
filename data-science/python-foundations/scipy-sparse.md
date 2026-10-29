[Data Science](../README.md) › [Python Foundations](README.md) › scipy.sparse

# 稀疏矩陣 (scipy.sparse)

大部分元素是 0 的矩陣只存非零值與位置。單細胞計數矩陣（90% 以上是 0）、文字的詞頻矩陣、one-hot 編碼、網路的 adjacency matrix 都是典型例子；用 dense array 存會浪費十倍以上記憶體，甚至根本放不進 RAM。

## 儲存格式

| 格式 | 內部結構 | 擅長 | 不擅長 | 典型用途 |
| --- | --- | --- | --- | --- |
| COO (`coo_array`) | `(row, col, data)` 三個陣列 | 一次建好、轉檔 | 索引、運算 | 從檔案 / 三元組建立，再轉 CSR |
| CSR (`csr_array`) | 每列的非零值連續存放（`data`、`indices`、`indptr`） | **取列**、矩陣乘向量、列運算 | 取欄、改變非零結構 | 細胞 × 基因（取一個細胞）、scikit-learn 輸入 |
| CSC (`csc_array`) | 每欄連續存放 | **取欄**、欄運算 | 取列 | 取單一基因、`svds` 某些情況 |
| LIL / DOK | list / dict | 逐格修改 | 運算慢 | 增量建構，完成後轉 CSR |

```
CSR：data    = [3, 1, 5, 2, 4]       非零值，依列排好
     indices = [0, 2, 1, 0, 2]       每個值的欄號
     indptr  = [0, 2, 3, 5]          第 i 列是 data[indptr[i]:indptr[i+1]]
            → [[3, 0, 1],
               [0, 5, 0],
               [2, 0, 4]]
```

記憶體約為 `nnz × (值大小 + 索引大小) + 列數 × 索引大小`。10,000 × 2,000、密度 5% 的 float32 矩陣：dense 80 MB，CSR 約 8 MB。密度超過約 30–50% 時稀疏格式反而更大更慢，直接用 dense。

## `*_array` vs `*_matrix`

SciPy 現在建議用 `csr_array` 等**稀疏陣列**；舊的 `csr_matrix` 模仿已棄用的 `np.matrix`，行為不同：

| 操作 | `csr_array`（新） | `csr_matrix`（舊） |
| --- | --- | --- |
| `A * B` | 逐元素相乘 | **矩陣乘法** |
| `A @ B` | 矩陣乘法 | 矩陣乘法 |
| `A.sum(axis=0)` | 1-D `ndarray`，shape `(n,)` | 2-D `np.matrix`，shape `(1, n)` |
| 建構 | `sp.random_array`、`sp.diags_array`、`sp.eye_array` | `sp.random`、`sp.diags`、`sp.eye` |

> 很多套件（含 AnnData、scikit-learn 的部分輸出）仍會回傳 `*_matrix`。寫 `A @ B` 表示矩陣乘、`A.multiply(B)` 表示逐元素乘，並用 `np.asarray(x).ravel()` 把 sum / mean 的結果攤平，兩種型別都不會出錯。檢查是否為稀疏用 `sp.issparse(A)`。

## 常用操作

```python
import numpy as np
import scipy.sparse as sp

# 1. 建立：三元組 → COO → CSR（重複位置會相加）
row = np.array([0, 0, 1, 2, 2]); col = np.array([0, 2, 1, 0, 2]); val = np.array([3, 1, 5, 2, 4])
X = sp.coo_array((val, (row, col)), shape=(3, 3)).tocsr()
X.nnz                                      # 5
X.toarray()                                # 轉 dense：只在確定放得下時用

rng = np.random.default_rng(0)
A = sp.random_array((10_000, 2_000), density=0.05, format="csr", rng=rng, dtype=np.float32)

# 2. 彙總：攤平成 1-D
libsize = np.asarray(A.sum(axis=1)).ravel()         # 每列總和（每個細胞的 library size）
mean = np.asarray(A.mean(axis=0)).ravel()           # 每欄平均（含 0）
var = np.asarray(A.multiply(A).mean(axis=0)).ravel() - mean**2   # 欄變異數，不必 densify
detected = np.asarray((A > 0).sum(axis=0)).ravel()  # 每個基因在幾個細胞被偵測到

# 3. 只動非零值的轉換：直接改 .data（0 仍是 0）
B = A.copy()
B.data = np.log1p(B.data)                           # log1p(0) = 0，稀疏結構不變

# 4. 列標準化：左乘對角矩陣，結果仍是稀疏
N = sp.diags_array(1 / libsize) @ A                 # 每列總和 = 1

# 5. 切片：CSR 取列快、CSC 取欄快
A[[0, 5, 9]]                                        # 取列
A.tocsc()[:, :10]                                   # 大量取欄前先轉 CSC

# 6. 線性代數：截斷 SVD（不中心化，所以不是嚴格的 PCA）
from scipy.sparse.linalg import svds
u, s, vt = svds(A, k=50)

# 7. 存檔
sp.save_npz("counts.npz", A); A = sp.load_npz("counts.npz")
```

## 常見陷阱

| 陷阱 | 後果 | 正確做法 |
| --- | --- | --- |
| 減平均、z-score（`A - mean`） | 所有 0 變非 0 → 變成 dense，記憶體爆掉 | 只縮放不中心化（`StandardScaler(with_mean=False)`），或先選基因再 densify |
| `A + 1`、`np.exp(A)` 這類讓 0 變非 0 的運算 | 稀疏陣列直接報錯（`NotImplementedError`）或回傳 dense | 改用保 0 的轉換（`log1p`、`sqrt`）並作用在 `.data` |
| 對 CSR 逐格指定新的非零值 | `SparseEfficiencyWarning`，每次都重建結構，非常慢 | 用 LIL / COO 建好再轉 CSR |
| `A.sum(axis=0)` 結果再拿去 broadcast | `np.matrix` 的 shape `(1, n)` 造成意外的 2-D 結果 | `np.asarray(...).ravel()` |
| `A * B` 意義不明 | `csr_matrix` 是矩陣乘、`csr_array` 是逐元素乘 | 一律用 `@` 與 `.multiply()` |
| 隨手 `.toarray()` / `.todense()` | 單細胞百萬細胞矩陣放不進記憶體 | 只在小子集（幾個基因、一個 cluster）上 densify |
| 整數計數存成 float64 | 記憶體加倍 | 計數用 `int32` / `float32` |

## 與其他工具的銜接

| 工具 | 支援情況 |
| --- | --- |
| scikit-learn | 多數模型直接吃 CSR（`LogisticRegression`、`TruncatedSVD`、`NearestNeighbors`）；`PCA` 對稀疏輸入只支援 `svd_solver="arpack"` / `"covariance_eigh"`（內部隱式中心化，不會 densify） |
| pandas | `pd.DataFrame.sparse.from_spmatrix(A)`；但大型矩陣保持在 scipy / AnnData，不要轉 DataFrame |
| AnnData / scanpy | `adata.X` 通常就是 CSR，見 [AnnData 與 scanpy](anndata-and-scanpy.md) |
| NetworkX | `nx.to_scipy_sparse_array(G)`，見 [有向網路與結構指標](../network-analysis/directed-networks-and-structural-metrics.md) |
| R | `Matrix::dgCMatrix`（= CSC）；Seurat / SingleCellExperiment 的計數矩陣都是它 |

相關：[NumPy 線性代數](numpy/linear-algebra.md)、[Efficient Python](performance-and-scaling/efficient-python.md)、[Scalable Processing](../data-engineering/scalable-processing-and-out-of-core.md)。
