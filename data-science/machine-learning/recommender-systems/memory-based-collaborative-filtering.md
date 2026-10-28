[Machine Learning](../README.md) › [推薦系統](README.md) › 記憶式協同過濾

# 記憶式協同過濾 (Memory-Based Collaborative Filtering)

最直觀的協同過濾：不學潛在因子，直接從 user-item 矩陣計算相似度。

| 方式 | 想法 | 常見用途 |
| --- | --- | --- |
| User-user | 找和你評分模式相似的使用者，推薦他們喜歡的 | 個人化推薦 |
| Item-item | 找和你喜歡的項目「被同一群人喜歡」的項目 | 「看了這個的人也看了」；實務上較穩定 |

## 流程

```python
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

ratings = pd.DataFrame({
    "user":   ["u1", "u1", "u1", "u2", "u2", "u3", "u3", "u3", "u4", "u4"],
    "title":  ["A",  "B",  "C",  "A",  "B",  "B",  "C",  "D",  "A",  "D"],
    "rating": [5,    4,    1,    4,    5,    2,    5,    4,    1,    5],
})

# 1. 長表 → user × item 矩陣
user_item = ratings.pivot(index="user", columns="title", values="rating")
user_item.isna().values.mean()        # 稀疏度 0.375（真實資料通常 > 0.99）

# 2. Mean-centering：扣掉每個使用者自己的平均分，再把缺失補 0
centered = user_item.sub(user_item.mean(axis=1), axis=0)
filled = centered.fillna(0)

# 3. 相似度
user_sim = pd.DataFrame(cosine_similarity(filled), index=filled.index, columns=filled.index)
item_sim = pd.DataFrame(cosine_similarity(filled.T), index=filled.columns, columns=filled.columns)
item_sim.loc["A"]          # B 0.17、C −0.55、D −0.74：喜歡 A 的人傾向不喜歡 C、D

# 4. 只用最相似的 k 個鄰居（且只取正相似度）
neighbors = user_sim.loc["u4"].drop("u4")
neighbors = neighbors[neighbors > 0].sort_values(ascending=False).head(10)   # u2 0.50、u3 0.11
```

### 為什麼要 mean-centering

| 問題 | 例子 |
| --- | --- |
| 每個人的評分尺度不同 | A 什麼都給 4–5 分；B 喜歡才給 3 分、不喜歡給 1 分 |
| 直接把缺失補 0 | 等於把「沒看過」當成「極度討厭」 |

扣掉個人平均後，數值代表「比這個人平常的標準好或差多少」；此時補 0 的意思是「未知項目不貢獻相似度」，而不是負評。這種做法等同於 centered cosine，和 Pearson 相關係數很接近。

### 預測評分

用鄰居對該項目的（中心化）評分加權平均，再加回自己的平均分：

$$
\hat{r}_{u,i} = \bar{r}_u + \frac{\sum_{v \in N(u)} \text{sim}(u,v)\,(r_{v,i} - \bar{r}_v)}{\sum_{v \in N(u)} \lvert \text{sim}(u,v) \rvert}
$$

$N(u)$ 是**有評過 i** 的最相似 k 個使用者。通常只取正相似度的鄰居；鄰居太少時預測不可靠，可退回項目平均或熱門度。

## 稀疏性的影響

| 影響 | 說明 |
| --- | --- |
| 共同評過的項目太少 | 相似度只靠一兩個項目決定，極不穩定 |
| 覆蓋率下降 | 很多使用者找不到足夠的鄰居 |
| 計算量 | 使用者數 n 時要算 n² 個相似度 |

對策：只保留互動數夠多的使用者 / 項目、要求最少共同評分數、改用 item-item、改用 [矩陣分解](collaborative-filtering-and-als.md)。

## 記憶式 vs 矩陣分解

| | 記憶式 CF | 矩陣分解 (ALS) |
| --- | --- | --- |
| 做法 | 直接用觀察到的矩陣算相似度 | 學習潛在因子 |
| 優點 | 直觀、好解釋、好做 baseline | 處理大型稀疏矩陣、準確度通常較高 |
| 缺點 | 對稀疏性敏感、難擴展 | 潛在因子難解釋、流程較重 |

> 記憶式協同過濾適合當 baseline、教學起點或中小型資料的快速方案。Item-item 相似度可以離線預先算好，服務時查表即可，所以上線比 user-user 容易。
