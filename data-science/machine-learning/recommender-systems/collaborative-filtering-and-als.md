[Machine Learning](../README.md) › [推薦系統](README.md) › 矩陣分解與 ALS

# 矩陣分解與 ALS (Matrix Factorization and ALS)

把巨大而稀疏的 user × item 矩陣 R 近似成兩個低維矩陣的乘積：每個使用者與每個項目各有一個長度 k 的**潛在因子 (latent factors)** 向量，預測評分就是兩者的內積。

$$
R \approx U V^\top, \qquad \hat{r}_{u,i} = \mathbf{u}_u^\top \mathbf{v}_i
$$

$$
\min_{U, V} \sum_{(u,i) \in \text{observed}} \big(r_{u,i} - \mathbf{u}_u^\top \mathbf{v}_i\big)^2 + \lambda \big(\lVert U \rVert^2 + \lVert V \rVert^2\big)
$$

只對**觀察到的**格子算誤差，空白格不參與。潛在因子不是「喜劇 / 動作片」這種明確標籤，而是能解釋偏好模式的抽象維度。

## ALS：交替最小平方

同時最佳化 U 和 V 很難，但固定其中一個後，另一個就是一般的 [Ridge 迴歸](../supervised-learning/regression/ridge.md)，有封閉解：

```
初始化 U、V
重複：
  固定 V，對每個使用者解 Ridge 迴歸 → 更新 U
  固定 U，對每個項目解 Ridge 迴歸 → 更新 V
```

每個使用者 / 項目可以平行求解，這是 ALS 適合分散式運算（Spark）的原因。

```python
import numpy as np

def als(R, mask, k=3, lam=0.1, iters=15, seed=0):
    """R：評分矩陣；mask：True = 有觀察到。"""
    rng = np.random.default_rng(seed)
    U = rng.normal(0, 0.1, (R.shape[0], k))
    V = rng.normal(0, 0.1, (R.shape[1], k))
    I = lam * np.eye(k)
    for _ in range(iters):
        for u in range(R.shape[0]):                       # 固定 V，更新每個使用者
            Vu = V[mask[u]]
            U[u] = np.linalg.solve(Vu.T @ Vu + I, Vu.T @ R[u, mask[u]])
        for i in range(R.shape[1]):                       # 固定 U，更新每個項目
            Ui = U[mask[:, i]]
            V[i] = np.linalg.solve(Ui.T @ Ui + I, Ui.T @ R[mask[:, i], i])
    return U, V

# 模擬：50 使用者 × 40 項目，真實 rank 3，只觀察到 30%
U, V = als(R, mask, k=3)
pred = U @ V.T
# 訓練 RMSE 0.24、未觀察格子的 RMSE 0.45；預測全域平均的 baseline RMSE 1.77
```

## PySpark ALS

```python
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

# 顯性評分（MovieLens）
als = ALS(userCol="userId", itemCol="movieId", ratingCol="rating",
          rank=25, maxIter=10, regParam=0.05,
          nonnegative=True, implicitPrefs=False,
          coldStartStrategy="drop")          # 預測時遇到沒見過的 user / item 就丟掉該列
model = als.fit(train)
pred = model.transform(test)
RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction").evaluate(pred)

model.recommendForAllUsers(10)               # 每個使用者的 top-10

# 隱性回饋（播放次數）：implicitPrefs=True 時 alpha 才有作用
ALS(userCol="userId", itemCol="songId", ratingCol="plays",
    implicitPrefs=True, alpha=40, rank=25, regParam=0.05, coldStartStrategy="drop")
```

| 參數 | 說明 | 調整 |
| --- | --- | --- |
| `rank` | 潛在因子數 k | 太小 → 表達力不足；太大 → 過擬合、成本高 |
| `regParam` | L2 正則化 λ | 太低 → 記住雜訊 |
| `maxIter` | 交替次數 | 太少 → 未收斂 |
| `implicitPrefs` | 顯性評分 or 隱性回饋 | 決定整個目標函數，見 [顯性 vs 隱性回饋](explicit-vs-implicit-feedback.md) |
| `alpha` | 隱性回饋的信心縮放 | **只在 `implicitPrefs=True` 時使用** |
| `nonnegative` | 因子限制為非負 | 較好解釋 |
| `coldStartStrategy` | `"nan"`（預設）或 `"drop"` | 評估時要用 `"drop"`，否則 NaN 讓 RMSE 變 NaN |

> 本機沒有 Java 環境，PySpark 範例未實際執行；參數語意已對照 PySpark 4.2 原始碼的參數說明確認。單機可用 `implicit` 套件（隱性回饋 ALS / BPR）或 `surprise`（顯性評分 SVD）。

## 實務提醒

| 提醒 | 說明 |
| --- | --- |
| 先整理資料 | 一列一筆互動、穩定的 user / item ID、明確定義的評分或互動強度 |
| 用交叉驗證調 `rank`、`regParam` | Spark：`CrossValidator` + `ParamGridBuilder` |
| 評估要用排序指標 | RMSE 好 ≠ 推薦清單好，見 [評估與服務](evaluation-and-serving.md) |
| 和熱門度 baseline 比 | 複雜模型不一定贏 |
| 冷啟動 | 新使用者 / 項目沒有因子 → 搭配 [內容式過濾](content-based-filtering.md) 或熱門度 |
| 加入偏差項 | 實務的矩陣分解常加使用者偏差、項目偏差與全域平均（如 Funk SVD） |
