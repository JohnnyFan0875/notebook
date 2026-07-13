# Cross-Validation Methods

Cross-validation is a resampling method used to evaluate machine learning models on a limited data sample. It helps reduce [overfitting](../foundations/overfitting-underfitting.md) and provides a more reliable estimate of model performance.

## Interview Fast Answer

如果面試官問「為什麼要做 cross-validation」，最穩的回答通常是：

- 單一次 split 太不穩
- cross-validation 能更可靠地估計 generalization
- 對資料量有限時尤其重要

可以再補一句：

- cross-validation 是 model evaluation / model selection 的工具，不是 final test set 的替代品

## Bootstrapping vs Cross-Validation

這兩者很容易被一起問到。

- **Cross-validation**: 重複切分資料，主要拿來估計模型在 unseen data 上的表現
- **Bootstrapping**: 對資料做有放回抽樣，常拿來估計統計量不確定性，或作為 bagging 的資料來源

簡單記法：

- CV 比較偏 evaluation of predictive performance
- bootstrap 比較偏 resampling-based uncertainty estimation 或 ensemble sampling

## K-Fold Cross-Validation

- Splits dataset into **k equal-sized folds**.
- For each iteration, use **k-1 folds for training** and **1 fold for validation**.
- Repeat k times → average the results.

```python
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
import numpy as np

# Dataset
data = load_iris()
X, y = data.data, data.target

# Model
model = LogisticRegression(max_iter=200)

# K-Fold
kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(model, X, y, cv=kf, scoring='accuracy')

print("Cross-validation scores:", cv_scores)
print("Mean accuracy:", np.mean(cv_scores))
```

**Critical Notes:**

- Shuffling is recommended to ensure randomness.
- Higher k (e.g., 10) → more stable estimates but higher computation.

## Train-Validation Split + Cross-Validation (Kaggle-style)

- Used when the **test set has no labels** (common in Kaggle competitions).
- Split `train.csv` into **training + hold-out validation sets**.
- Perform cross-validation on the training portion, then evaluate the hold-out validation set separately.

```python
import pandas as pd
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

data = pd.read_csv('train.csv')
X = data.drop('target', axis=1)  # Features
y = data['target']  # Target variable

# Train-validation split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

kf = KFold(n_splits=5, shuffle=True, random_state=42)
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier(n_estimators=100, random_state=42))
])

cv_scores = cross_val_score(pipeline, X_train, y_train, cv=kf, scoring='accuracy')

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_val)
final_accuracy = accuracy_score(y_val, y_pred)

print("Cross-validation scores:", cv_scores)
print("Final hold-out validation accuracy:", final_accuracy)
```

**Critical Notes:**

- Ensures both CV accuracy and an independent validation score.
- Commonly used when the competition test set has no labels.
- Keep preprocessing inside the [pipeline](pipeline-basic.md) so each fold learns only from its training portion.

## Direct K-Fold Split (without hold-out set)

- Use all of `train.csv` with K-Fold.
- Each fold is used once as validation, results are averaged.

```python
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

data = pd.read_csv('train.csv')
X = data.drop('target', axis=1)
y = data['target']

kf = KFold(n_splits=5, shuffle=True, random_state=42)

fold_accuracies = []

for train_index, test_index in kf.split(X):
    cv_train, cv_test = X.iloc[train_index], X.iloc[test_index]
    cv_train_labels, cv_test_labels = y.iloc[train_index], y.iloc[test_index]

    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    pipeline.fit(cv_train, cv_train_labels)
    y_pred = pipeline.predict(cv_test)

    acc = accuracy_score(cv_test_labels, y_pred)
    fold_accuracies.append(acc)

mean_accuracy = sum(fold_accuracies) / len(fold_accuracies)
print("Mean accuracy:", mean_accuracy)
```

**Critical Notes:**

- No separate hold-out set is used.
- Provides a good estimate of [generalization](../foundations/generalization.md) error, but cannot check on unseen validation data.

## Stratified K-Fold Cross-Validation

- Ensures that each fold maintains the **same class distribution** as the original dataset.
- Important for [**imbalanced classification problems**](../evaluation/class-imbalance.md).

```python
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np

# Example dataset
train_df = pd.read_csv('train.csv')
X = train_df.drop(columns=['target'])
y = train_df['target']

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
accuracies = []

for train_index, val_index in skf.split(X, y):
    X_train, X_val = X.iloc[train_index], X.iloc[val_index]
    y_train, y_val = y.iloc[train_index], y.iloc[val_index]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)

    acc = accuracy_score(y_val, y_pred)
    accuracies.append(acc)

print("Average StratifiedKFold accuracy:", np.mean(accuracies))
```

**Critical Notes:**

- Always use **StratifiedKFold** for [classification](../supervised-learning/classification/README.md) to avoid biased folds.
- Useful for small or **imbalanced datasets**.

### Interview Prompt: Which CV Split Should I Use?

常見的高訊號回答是：

- classification: 優先考慮 `StratifiedKFold`
- regression / general tabular task: `KFold`
- time-ordered data: `TimeSeriesSplit`
- extremely small data: 可能提高 `k`，但要考慮 variance 與 computation

## Time Series Split

- Used for **time-dependent data**.
- Ensures training data always comes **before validation data** (no look-ahead bias).

```python
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd

# Load time series data
df = pd.read_csv('train.csv', parse_dates=['Date'])
df = df.sort_values('Date')

features = [col for col in df.columns if col not in ['Date', 'Target']]
X, y = df[features], df['Target']

tscv = TimeSeriesSplit(n_splits=5)
fold_scores = []

for fold, (train_index, val_index) in enumerate(tscv.split(X), 1):
    X_train, X_val = X.iloc[train_index], X.iloc[val_index]
    y_train, y_val = y.iloc[train_index], y.iloc[val_index]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)

    rmse = mean_squared_error(y_val, y_pred, squared=False)
    fold_scores.append(rmse)

print("Average RMSE across folds:", np.mean(fold_scores))
```

**Critical Notes:**

- Must preserve **temporal order** of data.
- Do **not shuffle** in time series problems.
- Commonly used in finance, forecasting, and sequential datasets.

## Key Takeaways

- **K-Fold:** General method for cross-validation.
- **Train-Validation + CV:** Kaggle-style when test labels are unavailable.
- **Direct K-Fold:** Uses all training data in k folds.
- **Stratified K-Fold:** Use for classification, especially with class imbalance.
- **Time Series Split:** Use when data has a natural order over time.
- Cross-validation improves [generalization](../foundations/generalization.md) but increases computational cost.
- Preprocessing that learns from data should happen inside each fold, usually via a [pipeline](pipeline-basic.md).

## Common Interview Traps

- 把 CV score 當 final test performance
- 先做 scaling / imputation / feature selection，再把處理後資料送進 CV
- 在 class imbalance 問題上仍用普通 `KFold`
- 在 time series 資料上 shuffle

## Related Concepts

- [Generalization](../foundations/generalization.md)
- [Data Leakage](../foundations/data-leakage.md)
- [Class Imbalance](../evaluation/class-imbalance.md)
- [Hyperparameter Tuning](hyperparameter-tuning.md)

[Back to Workflow](README.md)
