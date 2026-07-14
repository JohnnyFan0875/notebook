# Feature Selection

## Overview

- **Feature selection** is the process of identifying and selecting the most relevant features (variables) from a dataset for use in model training.
- Goals:
  - Reduce **[overfitting](../foundations/overfitting-underfitting.md)** by eliminating irrelevant/noisy features.
  - Improve **accuracy** by focusing on informative features.
  - Reduce **computational cost** by working with fewer variables.

## Main Approaches

### 1. Filter Methods

- Evaluate the relevance of features independently of the machine learning model.
- Typically use **statistical tests** or **information-theoretic measures**.
- Examples:
  - **Correlation matrix**: Remove features highly correlated with each other.
  - **Chi-squared test** (for categorical data).
  - **Mutual information** (captures non-linear relationships).

```python
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectKBest, chi2

X, y = load_iris(return_X_y=True)
selector = SelectKBest(score_func=chi2, k=2)
X_new = selector.fit_transform(X, y)
print("Selected features (indices):", selector.get_support(indices=True))
```

### 2. Wrapper Methods

- Use a machine learning model to evaluate subsets of features.
- Computationally more expensive since they involve **repeated model training**.
- Examples:
  - **Recursive Feature Elimination (RFE)**.
  - Stepwise selection.

```python
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=200)
rfe = RFE(model, n_features_to_select=2)
rfe = rfe.fit(X, y)
print("Selected features (indices):", rfe.get_support(indices=True))
```

### 3. Embedded Methods

- Perform feature selection **during model training**.
- Feature importance is a natural byproduct of the algorithm.
- Examples:
  - **LASSO [regression](../supervised-learning/regression/README.md) (L1 penalty)**.
  - **Decision tree / Random forest feature importances**.

```python
from sklearn.linear_model import Lasso
import numpy as np

lasso = Lasso(alpha=0.1)
lasso.fit(X, y)
print("Feature coefficients:", np.round(lasso.coef_, 3))
```

### Critical Notes

- **[Data leakage](../foundations/data-leakage.md)**: Always perform feature selection **inside the [cross-validation](../workflow/cross-validation.md) loop** (not before splitting train/test data).
- **Interpretability**: Feature importance scores can differ depending on the method and the model. Interpret with caution.
- **Dimensionality reduction ≠ feature selection**: Techniques like [PCA](../unsupervised-learning/dimensionality-reduction/pca.md) create new features, while feature selection keeps a subset of the original ones.
- **Balance**: Removing too many features may underfit, while keeping too many may overfit.

## Interview Fast Comparison

如果面試官問 feature selection 方法差在哪，最穩的回答順序通常是：

- `filter`: 不依賴模型，先用統計量或規則篩欄位
- `wrapper`: 反覆訓練模型，直接比較不同欄位子集合
- `embedded`: 在模型訓練過程中一起做選擇

可以再補一句 trade-off：

- filter 最快，但通常最粗
- wrapper 最貼近最終模型表現，但最貴
- embedded 通常是速度與效果之間的折衷

## Quick Comparison Table

| Method | Uses model? | Can search subsets? | Main trade-off |
| --- | --- | --- | --- |
| Filter | No | Usually not directly | Fast, but may miss interaction effects |
| Wrapper | Yes | Yes | Strong but computationally expensive |
| Embedded | Yes | Partly | Efficient, but tied to chosen model |

## Why Teams Often Want Fewer Variables

在實務專案裡，變數選擇不只是為了分數。

模型帶太多欄位時，常見代價包括：

- 更容易 overfit
- 特徵管線更難維護
- 上線時需要更多資料依賴
- 解釋更困難
- 高相關欄位造成 multicollinearity 或重要性不穩定

Key point: 一個稍微簡單、但穩定而可維護的模型，常常比「多加十個欄位才多一點點分數」更有價值。

### Interview Prompt: Why Do Feature Selection?

高訊號回答通常不只講 accuracy，還會提到：

- 降低 overfitting
- 提升 interpretability
- 縮短 training time
- 降低資料依賴與上線複雜度

## Forward Stepwise Selection

forward stepwise 是一種常見的 wrapper heuristic：

1. 從空集合開始
2. 每輪把每個候選變數都試著加進來
3. 挑出讓驗證指標提升最多的那一個
4. 重複直到沒有明顯提升，或達到預設變數數量

例如如果你用 AUC 作為 ranking 指標，流程可以長這樣：

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

def auc_for_variables(variables, target, basetable):
    X = basetable[variables]
    y = basetable[target]

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    pred = model.predict_proba(X)[:, 1]
    return roc_auc_score(y, pred)
```

這個思路的價值在於：

- 它直接對著你真正關心的指標選變數
- 它比暴力搜尋所有子集合便宜很多
- 它能幫你觀察「多加一個欄位，是否真的還有邊際價值」

## Important Caveat on Stepwise Methods

stepwise 方法好用，但要小心：

- 若直接在同一份資料上反覆挑變數，會過度樂觀
- 被選進來的欄位不一定穩定，對抽樣或時間切片可能敏感
- 高相關欄位之間，誰被選進來有時只是偶然

Warning: 如果你要用 stepwise 或任何 supervised feature selection，評估必須放在 validation split 或 cross-validation 裡，而不是在整份資料上選完再宣稱效果很好。

## Common Interview Traps

- 先在整份資料上做 supervised selection，再切 train/test
- 把 feature importance 當成穩定真理，忽略相關特徵與模型依賴
- 把 PCA 說成 feature selection
- 只談分數，不談維護成本與資料取得成本

## When to Stop Adding Variables

常見停止條件包括：

- 已達預設欄位上限
- 指標提升非常小
- 測試集 AUC 不再改善
- 新增欄位雖然加分，但 maintenance cost 明顯變高

實務上不要只問「分數還能不能更高」，也要問：

- 這個欄位上線時拿不拿得到？
- 是否會增加時間 leakage 風險？
- 是否只是和現有欄位重複表達同一件事？

> Feature selection is an essential preprocessing step in machine learning [pipeline](../workflow/pipeline-basic.md)s. Combining multiple approaches (e.g., filter + embedded) often yields the most robust results.

## Related Concepts

- [Regularization](../foundations/regularization.md)
- [Feature Engineering Principles](../foundations/feature-engineering-principles.md)
- [Data Leakage](../foundations/data-leakage.md)
- [Pipeline Basics](../workflow/pipeline-basic.md)

[Back to Preprocessing](README.md)
