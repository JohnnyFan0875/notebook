# Support Vector Machine (SVM)

Support Vector Machines are supervised learning models that try to find a decision boundary with the largest possible margin between classes.

## Core Idea

- The decision boundary is defined by a subset of training points called **support vectors**.
- A larger margin often improves [generalization](../../foundations/generalization.md).
- Kernels allow SVMs to model non-linear boundaries.

## 什麼是 margin

可以把 SVM 想成在找一條不只是能把類別分開，還要盡量離兩邊資料點都遠一點的分界線。這個「留白距離」就是 margin。支持這條邊界的少數點，就是 support vectors。

## Important Hyperparameters

- `C`: controls the tradeoff between margin size and training error
- `kernel`: `linear`, `rbf`, `poly`, or `sigmoid`
- `gamma`: controls how far the influence of each point reaches for kernels such as `rbf`

## 什麼時候適合用

- 特徵維度高、樣本數中等的問題
- 邊界明顯、類別可分性不錯的情境
- 想要強力 baseline 來對照樹模型或邏輯斯回歸時

## Practical Notes

- SVM is sensitive to [feature scaling](../../preprocessing/feature-scaling.md).
- Linear SVM works well in high-dimensional settings, including some text problems.
- Kernel SVM can be powerful but may become slow on large datasets.
- `probability=True` 會增加訓練成本，因此只有真的需要機率輸出時再開。

## Example

```python
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("model", SVC(kernel="rbf", C=1.0, gamma="scale", probability=True))
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
```

## When to Use

- Medium-sized datasets
- Clear margin-based classification problems
- High-dimensional tabular or text-like features

## Common Pitfalls

- 忘記做 scaling，導致距離概念失真。
- 在很大的資料集上直接用 RBF kernel，訓練時間爆炸。
- 把 SVM 機率輸出當成天然可靠，卻沒有檢查 [calibration](../../evaluation/classification-thresholds-and-calibration.md)。

## Related Concepts

- [Feature Scaling](../../preprocessing/feature-scaling.md)
- [Hyperparameter Tuning](../../workflow/hyperparameter-tuning.md)
- [Regularization](../../foundations/regularization.md)
- [Confusion Matrix](../../evaluation/confusion-metrics.md)

[Back to Classification](README.md)
