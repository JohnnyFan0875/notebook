# Elastic Net Regression

Elastic Net 把 **L1 [regularization](../../foundations/regularization.md)** 與 **L2 regularization** 結合在一起。它特別適合特徵很多、彼此高度相關，且你希望同時做到係數收縮與部分特徵選擇的情境。

## Why Use Elastic Net

- handles correlated predictors better than pure Lasso
- can shrink coefficients while still setting some to zero
- useful when there are many features and multicollinearity

## 直覺理解

- Ridge 傾向把相關特徵一起縮小，但不會真的變成 0。
- Lasso 可能直接把某些特徵踢掉，但在高度相關時有時會選得不穩。
- Elastic Net 介於兩者之間，常是高維表格資料的實用折衷方案。

## Key Hyperparameters

- `alpha`: overall [regularization](../../foundations/regularization.md) strength
- `l1_ratio`: mix between L1 and L2
  - `1.0` means Lasso-like
  - `0.0` means Ridge-like

## Example

```python
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNet

pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("model", ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=42))
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
```

## Practical Notes

- standardize features before fitting
- tune both `alpha` and `l1_ratio`
- compare against Ridge and Lasso instead of assuming Elastic Net is always better

## When It Often Works Well

- 文字或 one-hot 後的高維特徵
- 生物統計、金融或行銷資料中常見的共線性問題
- 希望保留線性模型可解釋性，但需要更穩健正則化的情境

## Common Pitfalls

- 沒有做 scaling 就直接比較係數大小。
- 只調 `alpha`，沒有一起調 `l1_ratio`。
- 把係數變成 0 解讀成因果上「不重要」。

## Related Concepts

- [Regularization](../../foundations/regularization.md)
- [Lasso Regression](lasso.md)
- [Ridge Regression](ridge.md)
- [Feature Scaling](../../preprocessing/feature-scaling.md)

[Back to Regression](README.md)
