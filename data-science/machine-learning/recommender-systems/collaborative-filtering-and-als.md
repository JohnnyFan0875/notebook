# Collaborative Filtering and ALS

## Why ALS Shows Up Often

在大型推薦資料裡，直接對完整 user-item matrix 做運算通常不切實際，因此常改用 matrix factorization。

ALS 是 `Alternating Least Squares`，可以把原本巨大的互動矩陣拆成兩個較低維的 latent factor matrices：

- user latent features
- item latent features

模型學到的不是「電影是喜劇還是動作片」這種明確標籤，而是一組能解釋偏好模式的 latent features。

## ALS Intuition

很粗略地說，ALS 會交替進行兩件事：

1. 先固定 item factors，更新 user factors
2. 再固定 user factors，更新 item factors

反覆交替後，模型會逐步找到一組能較好重建已觀察互動的因子表示。

## PySpark ALS Mental Model

在 PySpark 裡，ALS 常見欄位設定包括：

- `userCol`
- `itemCol`
- `ratingCol`

典型寫法會像：

```python
ALS(
    userCol="userId",
    itemCol="movieId",
    ratingCol="rating",
    rank=25,
    maxIter=100,
    regParam=0.05,
    alpha=40,
    nonnegative=True,
    coldStartStrategy="drop",
    implicitPrefs=False,
)
```

其中比較值得先理解的是：

- `rank`: latent features 數量
- `maxIter`: 交替更新的迭代次數
- `regParam`: regularization 強度
- `alpha`: implicit feedback 場景的 confidence scaling
- `coldStartStrategy="drop"`: 評估或推論時略過無法產生預測的冷啟動列
- `implicitPrefs`: 決定模型把資料當 explicit 還是 implicit feedback

## Tuning Priorities

ALS 調參時，最常先碰到的是：

- `rank` 太小，模型表達能力不足
- `rank` 太大，容易增加成本或過擬合
- `regParam` 太低，模型可能記住噪音
- `maxIter` 不夠，模型還沒收斂到穩定狀態

在實務上，這些超參數不應脫離資料密度、互動量與評估指標單獨看待。

## Data Shape Matters

ALS 適合的資料通常至少要整理成：

- 一列一筆 interaction
- 穩定的 user / item identifiers
- 清楚定義的 rating 或 interaction strength

如果原始資料還是事件流、字串欄位混亂或 session log，通常要先完成資料清理與彙整，再進入 ALS。

## Practical Reminders

- ALS 是 collaborative filtering 的重要工具，但不是所有推薦問題的預設答案。
- latent factors 可用來捕捉偏好結構，但通常不具直接可解釋性。
- 先把資料整理成乾淨的 interaction table，通常比微調超參數更重要。

[Back to Recommender Systems](README.md)
