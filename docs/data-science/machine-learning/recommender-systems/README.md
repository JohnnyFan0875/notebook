# Recommender Systems

推薦系統的目標不是單純預測一個分數，而是幫使用者在大量候選項目中找到更可能有興趣的內容。它常出現在電商、影音平台、音樂、廣告與內容排序場景，因此除了模型本身，也很在意資料形狀、候選集合、冷啟動與最終呈現方式。

## Sections

- [Foundations](foundations.md): recommendation problem framing, user-item matrix, sparsity, and cold start
- [Content-Based Filtering](content-based-filtering.md): item vectors, TF-IDF, user profiles, and metadata-driven recommendation
- [Memory-Based Collaborative Filtering](memory-based-collaborative-filtering.md): pivot matrices, mean-centering, cosine similarity, and KNN intuition
- [Collaborative Filtering and ALS](collaborative-filtering-and-als.md): matrix factorization and PySpark ALS workflow
- [Explicit vs. Implicit Feedback](explicit-vs-implicit-feedback.md): ratings, clicks, plays, and confidence weighting
- [Evaluation and Serving](evaluation-and-serving.md): offline metrics, filtering seen items, and practical output shaping

## Why This Topic Is Different

推薦系統和一般分類或回歸問題有幾個差異：

- 輸出通常是 ranked list，而不是單一標籤
- user 與 item 都有身分，資料天然是 interaction table
- matrix 很稀疏，缺值不等於負樣本
- 新使用者與新商品常造成 cold start

## Practical Reminder

不要把 recommendation task 簡化成「預測分數」就結束。真正在產品裡有沒有價值，還取決於候選集合、過濾規則、探索策略與使用者體驗。

[Back to Machine Learning](../README.md)
