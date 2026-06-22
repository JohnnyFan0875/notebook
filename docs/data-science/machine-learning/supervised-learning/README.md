# Supervised Learning

Supervised learning 使用帶標籤資料來預測目標，是實務中最常見的建模情境。重點不只是哪個演算法最好，而是要先分清楚你是在預測類別還是連續數值，再搭配合適的評估與前處理方式。

## Sections

- [Classification](classification/README.md): predict categories or classes
- [Regression](regression/README.md): predict continuous numeric values
- [Ensemble](ensemble/README.md): combine multiple learners for stronger performance

## Recommended Order

1. Regression: start with linear models
2. Classification: learn [logistic regression](classification/logistic-regression.md), [KNN](classification/knn.md), trees, and [SVM](classification/svm.md)
3. Ensembles: move to [bagging](ensemble/bagging.md), [random forest](ensemble/random-forest.md)s, boosting, and [stacking](ensemble/stacking.md)

## 實務提醒

- 先做簡單、可解釋的 baseline，再往複雜模型前進。
- 同一個資料集上，模型差異常常小於資料切分與特徵工程差異。
- 分類問題要及早思考 threshold 與 class imbalance；回歸問題則要先確認誤差尺度與離群值容忍度。

## Related Notes

- [workflow/problem-framing.md](../workflow/problem-framing.md)
- [evaluation/README.md](../evaluation/README.md)
- [interpretability-and-diagnostics/README.md](../interpretability-and-diagnostics/README.md)

[Back to Machine Learning](../README.md)
