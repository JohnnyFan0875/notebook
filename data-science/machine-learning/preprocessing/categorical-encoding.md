[Machine Learning](../README.md) › [前處理](README.md) › 類別編碼

# 類別編碼 (Categorical Encoding)

把類別變數轉成模型能用的數值。選法取決於**類別有沒有順序**、**類別數（基數 cardinality）多寡**，以及**模型種類**。

## 方法比較

| 方法 | 做法 | 適用 | 風險 |
| --- | --- | --- | --- |
| One-hot | 每個類別一個 0/1 欄 | 名目、低基數（< 數十類）；**安全預設** | 高基數時欄位爆量 |
| Dummy（`drop_first`） | One-hot 少一欄 | 未正則化的線性 / 邏輯斯迴歸（避免完全共線性） | 有正則化或樹模型時不需要 |
| Ordinal | 依順序給 0, 1, 2… | **有順序**的類別（S < M < L）；樹模型的低基數名目變數 | 用在線性模型的名目變數會捏造大小關係 |
| Frequency / count | 以出現比例 / 次數取代 | 高基數；頻率本身有意義 | 不同類別頻率相同會撞在一起 |
| Target encoding | 以該類別的平均目標值取代 | 高基數且與目標有關（郵遞區號、基因家族） | **極易洩漏**，必須交叉擬合 (cross-fitting) |
| Hashing | 雜湊到固定數量的欄 | 極高基數、串流資料 | 雜湊碰撞；不可解釋 |
| Binary | 類別編號轉二進位 | 中基數 | 需 `category_encoders` 套件；欄位語意不清 |
| 原生類別支援 | 模型直接處理 | `HistGradientBoosting(categorical_features=...)`、LightGBM、CatBoost | 依套件而定 |

## 用法

```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, TargetEncoder

df = pd.DataFrame({"size": ["S", "M", "L", "M", "S", "XL"],
                   "city": ["A", "B", "A", "C", "A", "B"]})

# 1. One-hot：handle_unknown 讓上線遇到新類別不報錯；min_frequency 把罕見類別併成一欄
ohe = OneHotEncoder(handle_unknown="infrequent_if_exist", min_frequency=2, sparse_output=False)
ohe.fit(df[["city"]]).get_feature_names_out()   # ['city_A', 'city_B', 'city_infrequent_sklearn']

# pandas 版（探索用；建模請用 sklearn，才能存進 pipeline）
pd.get_dummies(df["city"], drop_first=True, dtype=int)            # 欄位 B, C

# 2. Ordinal：明確指定順序，否則預設依字母排序
OrdinalEncoder(categories=[["S", "M", "L", "XL"]]).fit_transform(df[["size"]])   # 0, 1, 2, 1, 0, 3

# 3. Frequency：比例要用訓練資料算，再 map 到測試資料
freq = X_train["city"].value_counts(normalize=True)
X_test["city_freq"] = X_test["city"].map(freq).fillna(0)

# 4. Target encoding：sklearn ≥ 1.3 的 TargetEncoder 在 fit_transform 時自動做 cross-fitting
te = TargetEncoder(cv=5)                 # 平滑 (smooth="auto") 會把小類別拉向整體平均
X_train_te = te.fit_transform(X_train[["gene_family"]], y_train)   # 每筆用「不含自己 fold」的平均
X_test_te = te.transform(X_test[["gene_family"]])                   # 測試資料用全部訓練資料的平均

# 5. Hashing
from sklearn.feature_extraction import FeatureHasher
FeatureHasher(n_features=16, input_type="string").transform([[c] for c in df["city"]])
```

> sklearn 1.9 起 `TargetEncoder(shuffle=..., random_state=...)` 已 deprecated，改成傳入 CV 物件：`TargetEncoder(cv=KFold(5, shuffle=True, random_state=0))`。

## Target encoding 為什麼會洩漏

手動在整份訓練資料上算「類別平均目標值」，每一列的編碼都包含了**它自己的標籤**。類別越多、每類樣本越少，洩漏越嚴重。

模擬：300 個類別、2,000 筆、**目標是純隨機**（真正 AUC = 0.5）：

| 做法 | 5-fold CV AUC |
| --- | --- |
| 先在全資料上算類別平均，再做 CV | **0.71**（假訊號） |
| `TargetEncoder` 放在 pipeline 內 | 0.51 |

```python
# 錯：手動 groupby 平均後再 CV
means = y.groupby(X["gene_family"]).mean()
X_leak = X["gene_family"].map(means).to_frame()

# 對：放進 pipeline，每個 fold 重新 fit，且 fit_transform 內部再做 cross-fitting
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
pipe = make_pipeline(TargetEncoder(), LogisticRegression())
```

詳見 [資料洩漏](../foundations/data-leakage.md)。

## 怎麼選

```
類別有順序嗎？
├─ 是 → Ordinal（指定順序）
└─ 否 → 類別數？
         ├─ 少（< ~20）→ One-hot
         ├─ 中 → One-hot + min_frequency / max_categories，或 Target encoding
         └─ 多（數百以上）→ Target encoding（cross-fitting）、Frequency、Hashing、或模型原生類別支援
```

## 注意事項

| 注意 | 原因 |
| --- | --- |
| 編碼器放進 [Pipeline](../workflow/pipeline-basic.md) | 只從訓練資料學類別與統計量 |
| 上線會出現新類別 | `handle_unknown="ignore"` 或 `"infrequent_if_exist"` |
| 樹模型不一定需要 one-hot | 高基數 one-hot 反而讓樹難以切分；ordinal 或原生類別支援常更好 |
| 會隨時間變動的類別（客戶等級、診斷代碼版本） | 取 reference date 當下有效的值，不是最新狀態，見 [Basetable](../foundations/basetable-and-time-aware-feature-engineering.md) |
| 生資的高基數類別 | 基因 ID、細胞株、批次：先想清楚它是特徵還是**分組變數**（應該用 `GroupKFold`，而不是編碼進模型） |
