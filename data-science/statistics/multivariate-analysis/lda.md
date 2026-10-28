[Statistics](../README.md) › [多變量分析](README.md) › 線性判別分析

# 線性判別分析 (Linear Discriminant Analysis, LDA)

LDA 與邏輯斯迴歸是結果為類別時的兩種基本方法。邏輯斯迴歸的完整說明（log-odds、odds ratio、假設、延伸模型）見 [迴歸分析：邏輯斯迴歸](../regression-analysis/logistic-regression.md)；分類評估（混淆矩陣、ROC、門檻、校準）見 [ML: Evaluation](../../machine-learning/evaluation/README.md)。這篇著重 **LDA**，以及它和邏輯斯迴歸的取捨。多變量邏輯斯分類的 ML 實作（pipeline、L1 選特徵）見 [ML：邏輯斯迴歸](../../machine-learning/supervised-learning/classification/logistic-regression.md)、[正則化](../../machine-learning/foundations/regularization.md)。

## 兩者比較

| | 邏輯斯迴歸 | LDA (linear discriminant analysis) |
| --- | --- | --- |
| 直接建模 | $P(Y \mid X)$（判別式 discriminative） | $P(X \mid Y)$ + 類別先驗 → 用貝氏定理得 $P(Y \mid X)$（生成式 generative） |
| 假設 | log-odds 與 X 線性 | 各類別 X 為**多變量常態**、**共變異矩陣相同** |
| 決策邊界 | 線性 | 線性（共變異不同時 → QDA，二次邊界） |
| 輸出 | 機率 | 類別、機率、**降維後的判別軸** |
| 優勢 | 假設較弱、較穩健、係數好解釋 | 假設成立時更有效率；多類別、小樣本、類別分得很開時穩定；可做監督式降維 |

> 實務上二元分類多用邏輯斯迴歸；LDA 適合多類別問題與視覺化類別分離。

## 用法

找出讓**組間變異 / 組內變異**比值最大的特徵線性組合，也就是最能分開各類別的方向。

```python
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.model_selection import cross_val_score

iris = load_iris()
lda = LinearDiscriminantAnalysis()
Z = lda.fit_transform(iris.data, iris.target)          # 3 類 → 最多 K−1 = 2 個判別軸
lda.explained_variance_ratio_                          # 各判別軸解釋的組間變異比例

plt.scatter(Z[:, 0], Z[:, 1], c=iris.target, cmap="Set1", alpha=0.7)
plt.xlabel("LD1"); plt.ylabel("LD2"); plt.show()

cross_val_score(lda, iris.data, iris.target, cv=5).mean()                       # 當分類器用
cross_val_score(QuadraticDiscriminantAnalysis(), iris.data, iris.target, cv=5).mean()   # 共變異不同時
```

## LDA vs PCA

| | PCA | LDA |
| --- | --- | --- |
| 目標 | 最大化**總**變異 | 最大化**組間 / 組內**變異比 |
| 使用標籤 | 否（非監督） | **是**（監督） |
| 最多成分數 | min(n − 1, p) | **min(p, K − 1)**，K = 類別數 |
| 適合 | 降維、去雜訊、探索結構 | 分類、視覺化類別分離 |
| 分配假設 | 不需要 | 各類別常態、共變異相同 |

> 有標籤時，想看「類別能否被分開」用 LDA；想看「資料主要怎麼變動」用 PCA。注意：高維小樣本時 LDA 很容易過擬合（p 接近 n 時共變異矩陣不可逆），要用正則化版本（`shrinkage="auto"`，需 `solver="lsqr"`）並以交叉驗證評估。

## 選擇指南

| 情境 | 建議 |
| --- | --- |
| 二元結果、需要機率與可解釋係數 | 邏輯斯迴歸 |
| 多類別、預測變數近似常態 | LDA |
| 共變異矩陣明顯不同 | QDA |
| 監督式降維 + 分類 | LDA |
| 很多相關的預測變數 | 邏輯斯迴歸 + L1 / Elastic Net |
| 類別不平衡、不想做分配假設 | 邏輯斯迴歸（搭配類別權重），見 [Class Imbalance](../../machine-learning/evaluation/class-imbalance.md) |
