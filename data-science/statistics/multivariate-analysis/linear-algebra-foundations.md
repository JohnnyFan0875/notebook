[Statistics](../README.md) › [多變量分析](README.md) › 線性代數基礎

# 多變量分析的線性代數基礎 (Linear Algebra Foundations)

多變量分析真正的難點，常常不是演算法名稱，而是能否把資料看成**向量、矩陣與線性轉換**。這些概念穩定後，PCA、多元迴歸、LDA 的數學形式都會變得自然。

## 核心概念速查

| 概念 | 數學 | 資料科學中的意義 |
| --- | --- | --- |
| 向量 (vector) | $x \in \mathbb{R}^p$ | 一筆觀測的 p 個特徵 = p 維空間中的一個點 / 方向 |
| 資料矩陣 (data matrix) | $X_{n \times p}$ | n 列觀測 × p 欄變數（基因表現矩陣常轉置為基因 × 樣本，注意方向） |
| 線性組合 (linear combination) | $a_1 v_1 + \cdots + a_k v_k$ | 迴歸配適值、PCA 分數、矩陣分解的近似，本質上都是線性組合 |
| 矩陣乘向量 | $Ax$ | 線性轉換：旋轉、伸縮、反射、投影；把資料搬到另一個座標系 |
| 線性方程組 | $Ax = b$ | 唯一解 / 無限多解 / 無解，取決於 A 的欄向量是否冗餘 |
| 秩 (rank) | 線性獨立的欄數 | rank < p → 有欄位是其他欄的線性組合（**完全共線性**，例如 dummy trap、p > n） |
| 正交 (orthogonal) | $x^\top y = 0$ | 兩個方向不重疊、不攜帶彼此的線性資訊 |
| 特徵向量 / 特徵值 (eigenvector / eigenvalue) | $Av = \lambda v$ | 經轉換後**方向不變**、只被伸縮 λ 倍的特殊方向 |
| 共變異矩陣 (covariance matrix) | $\Sigma = \frac{1}{n-1} X_c^\top X_c$（$X_c$ 已中心化） | 對角線 = 各變數變異；非對角線 = 兩兩共變異 |

## 與各方法的連結

| 方法 | 線性代數視角 |
| --- | --- |
| [PCA](pca.md) | 共變異矩陣的特徵分解：**特徵向量 = 主要變動方向**，**特徵值 = 該方向的變異量**；本質是**換基底 (change of basis)**：先旋轉座標軸，再只保留最有資訊的方向 |
| SVD | $X = U \Sigma V^\top$；PCA 實務上用 SVD 計算，數值更穩定 |
| [多元迴歸](../regression-analysis/multiple-linear-regression.md) | OLS 解 $\hat\beta = (X^\top X)^{-1} X^\top y$；配適值是 y 在 X 欄空間上的**投影** |
| 多重共線性 | $X^\top X$ 接近奇異（不可逆）→ 係數變異爆炸；Ridge 加上 λI 讓它可逆 |
| [LDA](lda.md) | 找讓組間 / 組內變異比最大的投影方向（廣義特徵值問題） |
| Embedding | 把物件（字、基因、細胞）映射到向量空間 |

```python
import numpy as np
from sklearn.datasets import load_iris

X = load_iris().data
Xc = X - X.mean(axis=0)                       # 中心化
cov = Xc.T @ Xc / (len(X) - 1)                # = np.cov(X, rowvar=False)

eigvals, eigvecs = np.linalg.eigh(cov)        # 對稱矩陣用 eigh
order = eigvals.argsort()[::-1]
eigvals, eigvecs = eigvals[order], eigvecs[:, order]
eigvals / eigvals.sum()                       # 各主成分解釋的變異比例

U, S, Vt = np.linalg.svd(Xc, full_matrices=False)   # SVD：Vt 的列 = 主成分方向
np.linalg.matrix_rank(X)                            # 秩
```

## 解讀習慣

| 看到 | 先問 |
| --- | --- |
| 矩陣乘法 | 這代表哪種轉換？ |
| 線性方程組 | 是唯一解、冗餘解，還是無解？ |
| 特徵向量 | 資料中最重要的變動方向是什麼？ |
| PCA | 新座標系長什麼樣？再談要保留幾個成分 |

> **常見錯誤**：在量尺差很多的變數上直接做 PCA，量級大的變數會主導結果；先標準化，見 [PCA](pca.md)。
