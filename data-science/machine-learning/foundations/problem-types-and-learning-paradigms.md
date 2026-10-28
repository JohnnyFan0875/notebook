[Machine Learning](../README.md) › [基礎概念](README.md) › 問題類型與學習範式

# 問題類型與學習範式 (Problem Types and Learning Paradigms)

選模型之前，先確認手上有什麼訊號（有沒有標籤）、需要什麼輸出。問題框錯，比模型選錯更難救。

## 學習範式 (Learning Paradigms)

| 範式 | 訓練訊號 | 例子 |
| --- | --- | --- |
| 監督式 (supervised) | 已標註的 (X, y) | 由基因表現預測腫瘤亞型 |
| 非監督式 (unsupervised) | 只有 X | 單細胞資料分群找細胞類型 |
| 半監督式 (semi-supervised) | 少量標註 + 大量未標註 | 少數人工標註的病理切片 + 大量未標註切片 |
| 自監督式 (self-supervised) | 從資料本身造出標籤（遮住一部分再預測） | 蛋白質語言模型（遮蔽胺基酸預測）、BERT |
| 強化學習 (reinforcement learning) | 行動後的獎勵訊號 | 分子設計、遊戲、機器人控制 |

## 問題類型

| 類型 | 輸出 | 例子 | 筆記 |
| --- | --- | --- | --- |
| 迴歸 (regression) | 連續值 | 房價、藥物反應 IC50 | [迴歸](../supervised-learning/regression/README.md) |
| 分類 (classification) | 類別 | 垃圾郵件、疾病 / 健康 | [分類](../supervised-learning/classification/README.md) |
| 排序 (ranking) | 項目的順序 | 搜尋結果、候選藥物優先序 | [推薦系統](../recommender-systems/README.md) |
| 分群 (clustering) | 群組 | 顧客分群、細胞類型 | [分群](../unsupervised-learning/clustering/README.md) |
| 降維 (dimensionality reduction) | 低維表示 | PCA、t-SNE 視覺化 | [降維](../unsupervised-learning/dimensionality-reduction/README.md) |
| 異常偵測 (anomaly detection) | 異常分數 | 詐欺、儀器異常 | [異常偵測](../unsupervised-learning/anomaly-detection/README.md) |
| 時間序列預測 (forecasting) | 未來值 | 下個月銷售 | [時間序列](../../statistics/time-series-analysis/README.md) |

## 為什麼問題類型重要

問題類型同時決定三件事：

| 決定 | 例子 |
| --- | --- |
| 能用哪些模型 | 分類不能直接用線性迴歸；排序問題用分類模型常不是最佳 |
| 資料怎麼切 | 時間序列不能隨機切；同一病人的多筆資料要分組切 |
| 哪些指標有意義 | 迴歸用 RMSE；不平衡分類不要只看 accuracy |

> 預測目標、決策時間點、分析單位（病人？樣本？細胞？）有任何一個不清楚，就先不要調模型。見 [問題定義](../workflow/problem-framing.md)。
