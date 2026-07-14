# Memory-Based Collaborative Filtering

memory-based collaborative filtering 是最直觀的協同過濾做法：不先學 latent factors，而是直接從 user-item interaction matrix 計算相似度。

常見的兩條路是：

- user-user similarity
- item-item similarity

## 從 Interaction Table 到 Pivot Matrix

通常先從長表轉成 user-item matrix：

```python
user_item = ratings.pivot(
    index="user",
    columns="title",
    values="rating",
)
```

這個 pivot matrix 的特徵是：

- row 是 user
- column 是 item
- 空白很多，而且空白不等於 dislike

## 缺值不能亂補

這是 memory-based recommendation 最常見的坑之一。

如果直接把所有 `NaN` 補成 `0` 再算相似度，通常等於偷偷把「沒看過」當成「中立或負向訊號」。

一個比較常見的折衷流程是：

1. 先對每個 user 做 mean-centering
2. 再把剩下的缺值補 `0`
3. 最後算 cosine similarity

```python
avg_ratings = user_item.mean(axis=1)
centered = user_item.sub(avg_ratings, axis=0)
filled = centered.fillna(0)
```

Key point: 這樣的 `0` 不代表「不喜歡」，而比較像「在去除個人基準分後，未知項目先暫時不貢獻相似度」。

## 為什麼要做 Mean-Centering

有些使用者天生分數給得高，有些人很嚴格。

例如：

- User A 所有電影都打 4 或 5 分
- User B 喜歡才打 3 分，不喜歡打 1 分

如果不先扣掉個人平均分，模型容易把「打分風格相近」誤當成「偏好相近」。

```python
avg_ratings = user_item.mean(axis=1)
centered = user_item.sub(avg_ratings, axis=0)
```

這一步的目的，是把注意力從絕對分數移到相對偏好。

## User-User Similarity

```python
from sklearn.metrics.pairwise import cosine_similarity

user_sim = cosine_similarity(filled)
user_sim_df = pd.DataFrame(
    user_sim,
    index=filled.index,
    columns=filled.index,
)
```

如果某兩個使用者相似度很高，代表他們在已觀察到的評分偏離模式上相近。

相似度可能是負的，表示兩者偏好方向相反。

## Item-Item Similarity

item-based collaborative filtering 只要把矩陣轉置即可：

```python
item_sim = cosine_similarity(filled.T)
item_sim_df = pd.DataFrame(
    item_sim,
    index=filled.columns,
    columns=filled.columns,
)
```

item-item 方法常在實務上更穩一些，因為 item 相對 user 通常變化沒那麼快。

## K-Nearest Neighbors 的直覺

完整 similarity matrix 可以直接用，但很多時候只保留最近的 `k` 個 neighbors 更實用。

```python
target = user_sim_df.loc["User_651"].drop("User_651")
neighbors = target.sort_values(ascending=False).head(10)
```

這樣做的好處是：

- 降低遠距、低品質相似度的影響
- 推薦邏輯更接近「找最像的幾個人」
- 計算和解釋都更簡單

## 一個常見的 Item-to-Item Pattern

針對單一 item 取最像的其他 items：

```python
similar_to_hobbit = (
    item_sim_df.loc["The Hobbit"]
    .drop("The Hobbit")
    .sort_values(ascending=False)
)
```

這種作法很適合做：

- 「看了這個的人也可能喜歡」
- 相似商品推薦
- related content modules

## Sparsity 對 Memory-Based 方法的影響

memory-based 方法對 sparsity 特別敏感，因為：

- 可比較的共評項目太少
- 相似度容易被少數重疊觀測主導
- user 數量大時，完整 pairwise similarity 成本很高

一個簡單的稀疏度量方式是：

```python
num_empty = user_item.isna().values.sum()
total = user_item.size
sparsity = num_empty / total
```

稀疏度高不代表模型不能用，但通常代表：

- naive neighbor methods 會不穩
- coverage 會下降
- 更需要 item metadata、popularity prior 或 factorization

## Memory-Based 與 ALS 的差異

| 方法 | 核心做法 | 優勢 | 弱點 |
| --- | --- | --- | --- |
| Memory-based CF | 直接用 observed matrix 算 similarity | 直觀、容易解釋、好做 baseline | 對 sparsity 敏感、擴展性較弱 |
| ALS / matrix factorization | 學 latent factors | 更能處理大型 sparse matrix | 可解釋性較低、建模流程較重 |

Key point: memory-based collaborative filtering 很適合當 baseline、教學起點、或小中型資料的快速方案，但不一定是大規模系統的終點。

## Practical Reminders

- 先確認缺值語意，再決定怎麼補。
- mean-centering 後再補 `0`，通常比原始分數直接補 `0` 更合理。
- user-based 和 item-based 都值得試，但 item-based 常更容易穩定 serving。

[Back to Recommender Systems](README.md)
