[Statistics](../README.md) › [多變量分析](README.md) › 邏輯斯迴歸與 LDA

# 邏輯斯迴歸與線性判別分析 (Logistic Regression & LDA)

結果為類別時的兩種基本方法。邏輯斯迴歸的完整說明（log-odds、odds ratio、假設、延伸模型）見 [迴歸分析：邏輯斯迴歸](../regression-analysis/logistic-regression.md)；分類評估（混淆矩陣、ROC、門檻、校準）見 [ML: Evaluation](../../machine-learning/evaluation/README.md)。這篇著重**多變量分類**與 **LDA**。

## 兩者比較

| | 邏輯斯迴歸 | LDA (linear discriminant analysis) |
| --- | --- | --- |
| 直接建模 | $P(Y \mid X)$（判別式 discriminative） | $P(X \mid Y)$ + 類別先驗 → 用貝氏定理得 $P(Y \mid X)$（生成式 generative） |
| 假設 | log-odds 與 X 線性 | 各類別 X 為**多變量常態**、**共變異矩陣相同** |
| 決策邊界 | 線性 | 線性（共變異不同時 → QDA，二次邊界） |
| 輸出 | 機率 | 類別、機率、**降維後的判別軸** |
| 優勢 | 假設較弱、較穩健、係數好解釋 | 假設成立時更有效率；多類別、小樣本、類別分得很開時穩定；可做監督式降維 |

> 實務上二元分類多用邏輯斯迴歸；LDA 適合多類別問題與視覺化類別分離。

## 邏輯斯迴歸：多變量分類流程

```python
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.metrics import classification_report, roc_auc_score, precision_recall_curve

cancer = load_breast_cancer(as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(
    cancer.data, cancer.target, test_size=0.2, random_state=42, stratify=cancer.target)

clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X_train, y_train)
y_prob = clf.predict_proba(X_test)[:, 1]
roc_auc_score(y_test, y_prob)
classification_report(y_test, (y_prob >= 0.5).astype(int), target_names=cancer.target_names)

# 依 F1 選門檻（門檻應依 FP / FN 的成本決定，0.5 只是慣例；正式做法要在驗證集上選）
prec, rec, thr = precision_recall_curve(y_test, y_prob)
f1 = 2 * prec * rec / (prec + rec + 1e-8)
thr[np.argmax(f1[:-1])]

# 30 個相關特徵 → L1 正則化做特徵選擇
lasso_logit = make_pipeline(StandardScaler(),
    LogisticRegressionCV(penalty="l1", solver="liblinear", cv=5)).fit(X_train, y_train)
(lasso_logit[-1].coef_ != 0).sum()
```

## LDA

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
