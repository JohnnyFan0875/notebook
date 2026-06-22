# Recommendation Foundations

## What a Recommendation Problem Looks Like

推薦問題常見的輸入不是一般 tabular dataset，而是一張 interaction table：

- `user_id`
- `item_id`
- `rating`, `watch_time`, `click`, `purchase`, `play_count` 等互動訊號

模型要回答的通常不是「這筆資料屬於哪一類」，而是：

- 這個 user 可能喜歡哪些 items
- 這個 item 應該推薦給哪些 users
- 在候選集合裡，哪些項目應該排在前面

## Two Common Recommendation Families

### Content-Based Filtering

content-based filtering 依賴 item features。

常見特徵包括：

- genre
- language
- decade
- actors
- brand
- category

它的直覺是：如果使用者喜歡某類 item，就推薦 feature 上相近的其他 items。

### Collaborative Filtering

collaborative filtering 主要依賴 user-item interactions，而不是 item 的人工特徵表。

它的直覺是：

- 相似使用者可能喜歡相似項目
- 常被同一群人喜歡的 items 可能彼此相關

這也是 PySpark ALS 最常出現的場景。

## The User-Item Matrix View

很多推薦模型都可以從 user-item matrix 來理解：

- row 代表 user
- column 代表 item
- cell 代表 rating 或互動強度

這個矩陣通常非常 sparse，因為大多數使用者只接觸過極少數 items。

一個很重要的心智模型是：空白格不代表使用者討厭該 item，只代表目前沒有觀察到互動。

## Sparsity and Cold Start

推薦系統有兩個很常見的結構性問題。

### Sparsity

- 觀測到的 interactions 很少
- 很多 user 與 item 幾乎沒有足夠訊號
- 相似度或因子分解容易受稀疏性影響

### Cold Start

- 新 user 沒有歷史資料
- 新 item 還沒有曝光或互動
- 模型很難只靠 collaborative signal 直接做出好推薦

這也是為什麼很多實務系統不會只依賴單一推薦方法，而會把 popularity、內容特徵或 business rules 一起用上。

## Practical Reminders

- interaction data 的缺值不能直接當負樣本處理。
- collaborative filtering 很強，但對新 user 和新 item 特別脆弱。
- 如果 item metadata 很完整，content-based 方法通常能補足 cold-start 弱點。

[Back to Recommender Systems](README.md)
