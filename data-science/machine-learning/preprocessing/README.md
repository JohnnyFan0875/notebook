# Preprocessing

Preprocessing 的目的，是把原始資料整理成模型可以穩定學習的特徵表示。這不只是語法問題，而是會直接影響泛化能力、資料洩漏風險與後續可部署性。

## 主題

- [Train-Test Split](train-test-split.md)
- [Imputation](imputation.md)
- [Categorical Encoding](categorical-encoding.md)
- [Feature Scaling](feature-scaling.md)
- [Outlier Handling](outlier-handling.md)
- [Feature Selection](feature-selection.md)

## 實務重點

- 不同模型對前處理敏感度不同，例如 [KNN](../supervised-learning/classification/knn.md) 與 [SVM](../supervised-learning/classification/svm.md) 對 scaling 很敏感，樹模型則相對不敏感。
- 前處理最好放進 [pipeline](../workflow/pipeline-basic.md)，才能和交叉驗證一起正確運作。
- `train-test-split` 雖然概念上屬於 workflow，但實作上與補值、編碼、縮放高度耦合，因此放在這裡一起讀最實用。

## 常見錯誤

- 在整份資料上先做補值或標準化。
- 對類別欄位任意 label encode，卻沒有意識到虛假的順序關係。
- 因為看到離群值就急著刪除，沒有先確認是資料錯誤還是真實極端觀測。

[Back to Machine Learning](../README.md)
