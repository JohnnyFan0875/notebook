[Machine Learning](../README.md) › [工作流程](README.md) › 資料切分與洩漏

# 資料切分與洩漏 (Data Splitting and Leakage)

[資料洩漏](../foundations/data-leakage.md) 讓驗證分數好於現實。這篇是實作面：用什麼順序、什麼切法避免洩漏。洩漏型態的完整清單見基礎概念那篇。

## 正確順序

```
1. 定義預測單位與時間點
2. 依問題結構切分 ──► train │ (validation) │ test（test 鎖起來）
3. 只在 train 上 fit 前處理（放進 Pipeline）
4. 用 validation 或交叉驗證選模型、調參
5. 最後在 test 上評估一次
```

## 切分策略

| 策略 | 何時用 | sklearn |
| --- | --- | --- |
| 隨機切分 | 觀測彼此獨立且同分布 (i.i.d.) | `train_test_split`、`KFold` |
| 分層切分 | [分類](../supervised-learning/classification/README.md)，尤其 [類別不平衡](../evaluation/class-imbalance.md) | `stratify=y`、`StratifiedKFold` |
| 分組切分 | 同一使用者 / 病人 / 裝置 / 店家 / 批次有多筆資料 | `GroupShuffleSplit`、`GroupKFold` |
| 時間切分 | 預測未來、資料有時間順序 | `TimeSeriesSplit`、依日期切 |
| 快照感知切分 | 同一實體在多個 reference date 各有一筆（[Basetable](../foundations/basetable-and-time-aware-feature-engineering.md)） | 依實體分組或依快照日期切 |
| 外部驗證 | 要宣稱能用在其他醫院 / 族群 / 平台 | 用另一個來源當 test |

```python
from sklearn.model_selection import train_test_split, GroupShuffleSplit

# 分層隨機切分
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

# 依病人分組切分：同一病人的所有樣本只會在 train 或 test 其中一邊
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
train_idx, test_idx = next(gss.split(X, y, groups=patient_id))

# 依時間切分
train = df[df["date"] < "2024-01-01"]
test = df[df["date"] >= "2024-01-01"]
```

各種 CV 切法的圖解見 [交叉驗證](cross-validation.md)；`train_test_split` 的參數細節見 [Train-Test Split](../preprocessing/train-test-split.md)。

## 預防洩漏

| 做法 | 防止的洩漏 |
| --- | --- |
| 前處理放進 [`Pipeline`](pipeline-basic.md) / `ColumnTransformer` | 補值、縮放、編碼、特徵選擇在全資料上 fit |
| Target encoding 在 fold 內計算 | 用到驗證資料的目標值 |
| 測試集只用一次 | 對測試集過度調參 |
| 逐欄確認預測時點可得性 | 目標洩漏、時間洩漏 |
| 分組資料依實體切 | 同一實體跨 train / test |
| 時間資料用過去訓練、未來驗證 | 用未來預測過去 |
| 多快照資料避免同一實體的相鄰快照跨 train / validation | 驗證列只是訓練列的「下個月版本」 |

## 心智模型

> 每個特徵都問：**預測當下我真的知道這個值嗎？**
>
> 多快照問題再多問一句：**這筆驗證資料，是不是只是某筆訓練資料的隔月版本？** 如果是，分數仍可能過度樂觀。
