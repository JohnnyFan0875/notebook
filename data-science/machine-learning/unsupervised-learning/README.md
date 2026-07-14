# Unsupervised Learning

Unsupervised learning 在沒有標籤的情況下尋找資料結構，常用於探索、分群、降維與關聯規則挖掘。這類方法沒有單一標準答案，因此更需要搭配可視化、領域知識與穩定性檢查。

## Sections

- [Clustering](clustering/README.md): group similar observations
- [Dimensionality Reduction](dimensionality-reduction/README.md): compress features while preserving important structure
- [Association Rules](association-rules/README.md): discover co-occurrence patterns in transactional data
- [Anomaly Detection](anomaly-detection/README.md): rank rare, suspicious, or abnormal observations

## Typical Goals

- Exploration and segmentation
- Visualization of high-dimensional data
- Noise reduction or feature compression
- Pattern discovery without a prediction target
- Detection of rare or suspicious behavior

## 閱讀提醒

- 分群結果不等於真實世界自然存在的群體，它只是某種相似度定義下的切分。
- 降維圖看起來分得很開，不代表原始高維空間一定同樣清楚。
- 關聯規則中的高 confidence 也不等於因果，只是共現模式。

[Back to Machine Learning](../README.md)
