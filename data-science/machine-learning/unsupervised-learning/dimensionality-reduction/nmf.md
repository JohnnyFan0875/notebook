[Machine Learning](../../README.md) › [非監督式學習](../README.md) › [降維](README.md) › NMF

# 非負矩陣分解 (Non-negative Matrix Factorization, NMF)

把非負矩陣 V（樣本 × 特徵）分解成兩個較小的非負矩陣：$V \approx W H$。因為不允許負值，成分只能「相加」不能「抵消」，得到的是**部分組成整體 (parts-based)** 的表示，通常比 [PCA](pca.md) 好解釋。

| 矩陣 | 形狀 | 意義（文字例） | 意義（基因表現例） |
| --- | --- | --- | --- |
| V | 樣本 × 特徵 | 文件 × 詞頻 | 樣本 × 基因 |
| W | 樣本 × k | 每篇文件含各主題的量 | 每個樣本中各「基因程式」的活性 |
| H | k × 特徵 | 每個主題由哪些詞組成 | 每個程式由哪些基因組成 |

| | PCA | NMF |
| --- | --- | --- |
| 值域 | 可正可負 | 非負 |
| 成分 | 正交、依變異排序 | 不正交、無排序 |
| 解讀 | 對比（正負抵消） | 加總（部分相加） |
| 唯一解 | 是 | 否（依初始化而異） |
| 資料 | 任意 | 必須非負（計數、表現量、像素） |

## 用法

```python
import numpy as np
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer

# 1. 小矩陣：4 篇文件 × 5 個詞
V = np.array([[5, 0, 3, 0, 2],
              [0, 3, 0, 2, 4],
              [1, 0, 4, 3, 0],
              [0, 1, 0, 5, 3]])
model = NMF(n_components=2, init="nndsvda", max_iter=1000, random_state=42)
W = model.fit_transform(V)       # 4 × 2：文件 1 幾乎只有主題 1，文件 2、4 以主題 2 為主
H = model.components_            # 2 × 5：主題 1 由詞 1、3 主導
model.reconstruction_err_        # 4.44（Frobenius norm，越小越好）

# 2. 文字主題
docs = ["I love programming in Python.", "Python and machine learning are awesome.",
        "I love data science and machine learning.", "Data science is my favorite field.",
        "I am learning about machine learning algorithms."]
vec = CountVectorizer(stop_words="english")
X = vec.fit_transform(docs)
nmf = NMF(n_components=2, max_iter=1000, random_state=1)
W = nmf.fit_transform(X)
terms = vec.get_feature_names_out()
[[terms[j] for j in topic.argsort()[::-1][:3]] for topic in nmf.components_]
# [['learning', 'machine', 'algorithms'], ['science', 'data', 'field']]

# 3. 用主題組成比較文件
from sklearn.metrics.pairwise import cosine_similarity
cosine_similarity(W)             # 文件間的主題相似度（非負時 0 到 1）
```

## 參數

| 參數 | 說明 |
| --- | --- |
| `n_components` (k) | 成分數；比較不同 k 的重建誤差與成分的可解釋性、穩定性 |
| `init` | `"nndsvda"`（預設之一，穩定）、`"random"`（需多次重跑） |
| `beta_loss` | `"frobenius"`（預設）；計數資料可用 `"kullback-leibler"`（需 `solver="mu"`） |
| `alpha_W`、`alpha_H`、`l1_ratio` | 正則化，可讓成分更稀疏 |

## 選 k 與穩定性

NMF 沒有唯一解，不同初始化可能得到不同成分。常見做法：對每個 k 多次重跑，選**重建誤差下降趨緩**且**成分在重跑間穩定**的 k（cNMF 的 consensus 方法即基於此）。

## 生資應用

| 應用 | 說明 |
| --- | --- |
| 突變特徵 (mutational signatures) | 腫瘤 × 96 種突變型態的計數矩陣 → 分解出 COSMIC signatures（SigProfiler） |
| 基因表現程式 | 單細胞資料中找共同活化的基因群（cNMF） |
| 腫瘤亞型 | 表現量矩陣分解後依 W 分群 |
| 空間轉錄體 / 細胞組成去卷積 | 部分方法基於 NMF |

> NMF 也用在 [推薦系統](../../recommender-systems/README.md)（使用者 × 項目的評分矩陣分解）。輸入有負值（例如標準化後的資料）時不能直接用，需先確認資料的尺度。
