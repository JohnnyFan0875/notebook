[Data Science](../../README.md) › [Python Foundations](../README.md) › NumPy

# NumPy

NumPy 的 `ndarray` 是 Python 數值計算的共同底層：pandas、scikit-learn、SciPy、PyTorch 都吃它或模仿它的介面。多數錯誤來自 `shape` / `axis` / `dtype` 沒對齊，而不是公式寫錯。

建議順序：array 基礎 → 向量化與 reshape → 隨機與統計 → 線性代數

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Array 基礎](array-basics.md) | `shape` / `ndim` / `dtype`、建立 array、索引與切片、view vs copy | 這個 array 長什麼樣？切片後改值會不會改到原本的？ |
| [向量化與 Reshape](vectorization-and-reshape.md) | element-wise 運算、broadcasting、布林遮罩、`reshape` / `transpose` / `concatenate` / `stack` / `split` | 怎麼不用迴圈一次算整批？維度對不上怎麼辦？ |
| [隨機與統計](random-and-statistics.md) | `default_rng` 抽樣、描述統計、分位數、z-score、轉換 | 怎麼做可重現的模擬？array 的摘要統計怎麼算？ |
| [線性代數](linear-algebra.md) | `@`、`solve`、`lstsq`、`inv`、`eig` / `eigh`、`svd` | 矩陣運算與解方程式怎麼寫才穩定？ |

| 相關 | 連結 |
| --- | --- |
| 表格資料（有欄名、index） | [pandas](../pandas/README.md) |
| 機率分配與檢定 | [scipy.stats 速查](../scipy-stats.md) |
| 迴圈太慢、要編譯 | [Efficient Python](../performance-and-scaling/efficient-python.md)（Numba） |
| 稠密 / 稀疏矩陣的實際應用 | [PCA](../../statistics/multivariate-analysis/pca.md) |
