[Machine Learning](../README.md) › [推薦系統](README.md) › 評估與服務

# 推薦的評估與服務 (Evaluation and Serving)

產品交付的是 **top-N 清單**，不是單一評分預測；離線分數只是代理指標。這篇整理怎麼切資料、用哪些排序指標，以及推薦結果送出前的後處理。

## 切分資料

| 切法 | 做法 | 問題 |
| --- | --- | --- |
| 隨機切互動 | 隨機抽 20% 互動當測試 | 用未來的互動預測過去，過度樂觀 |
| **依時間切** | 某日期前訓練、之後測試 | 最接近上線情境（推薦用的通常是這個） |
| Leave-last-out | 每個使用者最後 1 個（或最後 n 個）互動當測試 | 常用於序列推薦 |
| 依使用者切 | 部分使用者完全留作測試 | 評估新使用者冷啟動 |

見 [資料洩漏](../foundations/data-leakage.md)：推薦資料的時間洩漏特別常見。

## 指標

| 指標 | 回答 | 適用 |
| --- | --- | --- |
| RMSE / MAE | 評分預測準不準 | 顯性評分；**和清單品質不一定相關** |
| Precision@K | 前 K 個推薦中有幾個是對的 | 推薦清單 |
| Recall@K | 使用者真正喜歡的項目被找回多少 | 推薦清單 |
| Hit rate@K | 前 K 個中至少有一個對的使用者比例 | Leave-one-out |
| MAP@K | 考慮對的項目排在第幾名的平均 precision | 排序品質 |
| **NDCG@K** | 排序品質；越前面的正確項目權重越高 | 最常用的排序指標 |
| Coverage | 被推薦過的項目佔全部項目的比例 | 是否只推熱門 |
| 多樣性 / 新穎性 | 清單內的差異程度 / 推薦冷門項目的程度 | 避免同質化 |

```python
import numpy as np
from sklearn.metrics import ndcg_score

def precision_recall_at_k(recommended, relevant, k):
    hits = len(set(recommended[:k]) & set(relevant))
    return hits / k, hits / len(relevant)

def ndcg_at_k(recommended, relevant, k):
    dcg = sum(1 / np.log2(rank + 2) for rank, item in enumerate(recommended[:k]) if item in relevant)
    idcg = sum(1 / np.log2(rank + 2) for rank in range(min(len(relevant), k)))
    return dcg / idcg

recommended = ["A", "B", "C", "D", "E"]       # 模型排序
relevant = {"B", "E", "F"}                    # 測試期間使用者實際互動的項目
precision_recall_at_k(recommended, relevant, k=3)   # (0.33, 0.33)：前 3 個中只有 B 對
ndcg_at_k(recommended, relevant, k=5)               # 0.478

# sklearn 版：每個候選的相關度 + 模型分數
ndcg_score([[0, 1, 0, 0, 1, 1]], [[5, 4, 3, 2, 1, 0]], k=5)   # 0.478（同上）
```

PySpark 3.0+ 有 `RankingEvaluator`（`precisionAtK`、`ndcgAtK`、`meanAveragePrecision`）。

> 離線評估只看得到「使用者實際互動過的項目」，沒被展示過的好項目會被當成錯誤；所以離線指標偏向懲罰新穎的推薦。最終要靠線上 A/B 測試（點擊率、留存、轉換）確認價值，見 [A/B 測試](../../statistics/experimental-design/ab-testing.md)。

## 服務前的後處理

| 步驟 | 說明 |
| --- | --- |
| 過濾已互動的項目 | 不要把剛看過、剛買過的推回去（除非是可重複消費的品項） |
| 業務規則 | 庫存、地區、年齡限制、合約 |
| 重排 (re-ranking) | 增加多樣性、打散同類、加入新項目探索 |
| 攤平輸出 | 巢狀的推薦結果整理成 `user_id, item_id, score, rank` |
| 冷啟動退路 | 沒有因子的新使用者 → 熱門度或內容式推薦 |

```python
# pandas：過濾已看過的項目並攤平
recs = recs.merge(history[["user_id", "item_id"]], on=["user_id", "item_id"],
                  how="left", indicator=True)
recs = recs[recs["_merge"] == "left_only"].drop(columns="_merge")
recs["rank"] = recs.groupby("user_id")["score"].rank(ascending=False, method="first")
top_n = recs[recs["rank"] <= 10]
```

在 Spark 中做法相同：`recommendForAllUsers` 的巢狀結果先 `explode` 攤平，再和歷史互動做 `left_anti` join 排除已看過的項目。

> RMSE 好看不等於推薦清單好用。離線評估、結果過濾與最終的輸出格式要一起設計。
