[Machine Learning](../README.md) › [前處理](README.md) › Train-Test Split

# 訓練 / 測試切分 (Train-Test Split)

把資料分成訓練集（配適模型）與測試集（評估在沒看過的資料上的 [泛化](../foundations/generalization.md) 能力）。**先切分，再 fit 任何會從資料學習的前處理**。洩漏型態與預防見 [資料洩漏](../foundations/data-leakage.md)。

## 正確順序

```
1. 定義預測單位與時間點
2. 依問題結構切分 ──► train │ (validation) │ test（test 鎖起來）
3. 只在 train 上 fit 前處理（放進 Pipeline）
4. 用 validation 或交叉驗證選模型、調參
5. 最後在 test 上評估一次
```

## 切分比例

| 比例（train / test） | 何時用 |
| --- | --- |
| 80 / 20 | 常用預設 |
| 70 / 30 | 資料量中等，想要更穩定的測試估計 |
| 90 / 10 或更少 | 資料很大（數十萬筆以上），小比例的測試集已足夠 |
| 不切、改用 CV | 樣本很小（幾十到幾百）；單次切分的測試分數波動太大，見 [交叉驗證](../workflow/cross-validation.md) |

> 測試集大小決定估計的精確度。只有 30 個測試樣本、accuracy 0.8 時，95% 信賴區間約 ±0.14（$1.96\sqrt{0.8 \times 0.2 / 30}$），見 [評估指標的不確定性](../evaluation/metric-uncertainty.md)。

## 三分法：Train / Validation / Test

| 集合 | 用途 | 使用次數 |
| --- | --- | --- |
| Train | 配適模型與前處理 | 反覆 |
| Validation | 比較模型、[調參](../workflow/hyperparameter-tuning.md)、調閾值 | 反覆 |
| Test | 最終評估 | **一次** |

```python
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# 1. 先切出 test（20%），再從剩下的切出 validation（0.25 × 80% = 20%）→ 60 / 20 / 20
X_tmp, X_test, y_tmp, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_tmp, y_tmp, test_size=0.25, stratify=y_tmp, random_state=42)

# 2. 前處理只在 train 上 fit：用 pipeline 最不容易出錯
model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression())
model.fit(X_train, y_train)
model.score(X_val, y_val)        # 選模型、調參
# ... 全部決定後
model.score(X_test, y_test)      # 只看一次
```

| 參數 | 說明 |
| --- | --- |
| `test_size` | 比例（0.2）或筆數（200） |
| `stratify=y` | 分類時保持類別比例；[類別不平衡](../evaluation/class-imbalance.md) 時必用 |
| `random_state` | 固定切法，讓結果可重現 |
| `shuffle=False` | 時間序列依原順序切（資料須先依時間排序） |

## 切分策略

隨機切分只適用於觀測彼此獨立且同分布 (i.i.d.)；其他情況要依資料結構切。

| 策略 | 何時用 | sklearn |
| --- | --- | --- |
| 隨機切分 | 觀測彼此獨立且同分布 | `train_test_split`、`KFold` |
| 分層切分 | [分類](../supervised-learning/classification/README.md)，尤其 [類別不平衡](../evaluation/class-imbalance.md) | `stratify=y`、`StratifiedKFold` |
| 分組切分 | 同一使用者 / 病人 / 裝置 / 店家 / 批次有多筆資料 | `GroupShuffleSplit`、`GroupKFold` |
| 時間切分 | 預測未來、資料有時間順序 | `TimeSeriesSplit`、依日期切 |
| 快照感知切分 | 同一實體在多個 reference date 各有一筆（[Basetable](../foundations/basetable-and-time-aware-feature-engineering.md)） | 依實體分組或依快照日期切 |
| 外部驗證 | 要宣稱能用在其他醫院 / 族群 / 平台 | 用另一個來源當 test |

```python
from sklearn.model_selection import GroupShuffleSplit

# 依病人分組切分：同一病人的所有樣本只會在 train 或 test 其中一邊
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
train_idx, test_idx = next(gss.split(X, y, groups=patient_id))

# 依時間切分
train = df[df["date"] < "2024-01-01"]
test = df[df["date"] >= "2024-01-01"]
```

各種 CV 切法的圖解見 [交叉驗證](../workflow/cross-validation.md)。

> 不要手動先對全部資料 `fit_transform` 再切分；把前處理放進 [Pipeline](../workflow/pipeline-basic.md)，切分後的 `fit` 自然只用到訓練資料。
