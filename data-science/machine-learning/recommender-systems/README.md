[Machine Learning](../README.md) › 推薦系統

# 推薦系統 (Recommender Systems)

目標不是預測單一分數，而是幫使用者從大量候選中找到可能感興趣的項目。除了模型本身，資料形狀、候選集合、冷啟動與最終呈現方式都很重要。

## 和一般分類 / 迴歸的差別

| 一般監督式學習 | 推薦系統 |
| --- | --- |
| 輸出一個標籤或數值 | 輸出**排序清單**（top-N） |
| 一列是一個樣本 | 資料是 user × item 的**互動表** |
| 缺失值通常要補 | 矩陣極度稀疏，**缺失 ≠ 不喜歡** |
| 新樣本也能預測 | 新使用者 / 新項目有**冷啟動**問題 |
| 隨機切分即可 | 通常要**依時間**切分 |

## 建議順序

```
基礎概念 → 內容式過濾 → 記憶式協同過濾 → 矩陣分解 (ALS) → 顯性 vs 隱性回饋 → 評估與服務
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [基礎概念](foundations.md) | 互動表、user-item 矩陣、稀疏性、冷啟動 | 推薦問題長什麼樣子？ |
| [內容式過濾](content-based-filtering.md) | Item 向量、TF-IDF、使用者 profile | 怎麼推薦「和你喜歡的東西相似」的項目？ |
| [記憶式協同過濾](memory-based-collaborative-filtering.md) | Mean-centering、user-user / item-item 相似度 | 「和你相似的人也喜歡」怎麼算？ |
| [矩陣分解與 ALS](collaborative-filtering-and-als.md) | 潛在因子、交替最小平方、PySpark ALS | 大型稀疏矩陣怎麼處理？ |
| [顯性 vs 隱性回饋](explicit-vs-implicit-feedback.md) | 評分 vs 點擊 / 播放、信心權重 | 行為資料怎麼當成偏好？ |
| [評估與服務](evaluation-and-serving.md) | Precision@K、NDCG、時間切分、過濾已看項目 | 推薦清單好不好？怎麼交付？ |

## 方法比較

| 方法 | 需要的資料 | 冷啟動 | 可解釋性 | 擴展性 |
| --- | --- | --- | --- | --- |
| 熱門度 (popularity) | 互動次數 | 新使用者可用 | 高 | 高 |
| 內容式 (content-based) | Item 特徵 | **新項目可用** | 高 | 高 |
| 記憶式協同過濾 | 互動矩陣 | 不行 | 中（「相似的人也買了」） | 低（兩兩相似度） |
| 矩陣分解 (ALS) | 互動矩陣 | 不行 | 低（潛在因子） | 高 |
| 混合式 (hybrid) | 兩者都有 | 較好 | 中 | 中 |

> 一定要先和**熱門度 baseline** 比。很多資料集上「推薦最熱門的項目」就很難打敗。

生資中也有同樣的結構：藥物 × 標靶、基因 × 疾病、病人 × 藥物反應的稀疏矩陣補全，常用相同的矩陣分解方法，也可搭配 [NMF](../unsupervised-learning/dimensionality-reduction/nmf.md)。
