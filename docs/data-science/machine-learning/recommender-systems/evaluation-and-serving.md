# Evaluation and Serving Recommendations

## Offline Evaluation Is Only a Proxy

推薦系統離線評估時，常會先切 train / test，檢查模型對已知互動的預測能力。

在 explicit-rating 場景裡，RMSE 常被拿來衡量預測分數誤差。

但要記得：很多推薦產品最終要交付的是 top-N list，而不是單一 rating estimate，所以離線分數只能當 proxy，不是產品價值本身。

## Example Datasets

兩個很常見的教學資料集是：

- `MovieLens`: 明確評分資料，適合做 explicit recommendation 練習
- `Million Song Dataset`: 音樂互動資料，常用來理解 implicit recommendation

資料集本身的訊號種類，會直接影響你該怎麼切資料、選模型與解讀評估結果。

## Filtering Seen Items

模型產生推薦後，通常還需要做一輪後處理。

一個最基本的動作是：把使用者已經互動過的 items 排除掉，避免系統把剛看過或剛評分過的內容又原封不動推回去。

在 Spark workflow 裡，這通常可以透過：

- 先把 recommendation 結果展開
- 再和歷史 interactions 做 join
- 最後過濾已看過的 user-item pairs

這一步聽起來很工程，但其實直接影響推薦結果是否可用。

## Shaping Recommendation Output

很多協同過濾模型輸出的是 nested recommendations。要送到下游系統前，通常還要整理成較平坦的表格，例如：

- `user_id`
- `item_id`
- `score`
- `rank`

如果沒有把輸出清乾淨，下游服務、報表或人工檢查都會很難接手。

## Practical Reminders

- RMSE 好看不等於推薦清單真的好用。
- 離線評估、結果過濾與最終 serving format 應該一起設計。
- 真正上線後，通常還需要搭配線上指標與實驗驗證推薦是否帶來價值。

[Back to Recommender Systems](README.md)
