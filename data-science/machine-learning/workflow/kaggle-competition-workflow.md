[Machine Learning](../README.md) › [工作流程](README.md) › Kaggle 競賽流程

# Kaggle 競賽流程 (Kaggle Competition Workflow)

Kaggle 競賽不是「多試幾個模型、看 leaderboard」。穩定進步的關鍵是建立一套能**可靠判斷改動是否有效**的驗證與實驗系統，而不是某個神奇模型。這套流程同樣適用於研究中的模型比較。

## 核心循環

```
理解任務與指標 → 建立 local validation → 可靠的 baseline
        ↑                                        ↓
  用 submission 檢查 local 與 public LB 是否同步 ← 逐步改特徵 / 模型 / ensemble
```

第二步沒做對，後面所有特徵工程與調參都只是在追假分數。

## 1. 先看指標，再看模型

| 確認 | 為什麼 |
| --- | --- |
| 任務是迴歸、分類還是排序 | 決定模型與損失 |
| 官方指標（RMSE、AUC、log loss…） | local validation 要用**同一個指標** |
| 測試資料與訓練資料是否有時間差、分組差、分布漂移 | 決定 local validation 怎麼切 |

很多時候問題不是模型不夠強，而是 validation 指標與競賽指標沒對齊。

## 2. 建立 local validation

| 資料結構 | 切法 |
| --- | --- |
| i.i.d. 表格 | `KFold` |
| 分類、類別不平衡 | `StratifiedKFold` |
| 有時間順序 | `TimeSeriesSplit` 或依時間切 |
| 有分組實體 | `GroupKFold` |

> 好的 local validation 不只是「切一塊出來」，而是盡量**模擬測試集的生成方式**。各種切法見 [交叉驗證](cross-validation.md)。

以 CV 平均作為主要比較指標，但也要看各 fold 的波動：平均變好但 fold 間變異很大，代表策略不穩。

```python
import numpy as np
from sklearn.model_selection import KFold

kf = KFold(n_splits=5, shuffle=True, random_state=123)
folds = list(kf.split(train_df))       # 存下來，每次實驗都用同一組 folds

fold_scores = []
for tr_idx, va_idx in folds:
    model.fit(X.iloc[tr_idx], y.iloc[tr_idx])
    fold_scores.append(metric(y.iloc[va_idx], model.predict(X.iloc[va_idx])))
np.mean(fold_scores), np.std(fold_scores)
```

## 3. 簡單但誠實的 baseline

Baseline 不是拿來拿高分，而是提供穩定的比較基準：可重現、評估方式正確、能判斷新改動是否真的進步。

```python
# 迴歸：全域平均 → 分組平均 → 簡單線性 / 樹模型
global_mean = train_df["fare_amount"].mean()
group_mean = train_df.groupby("passenger_count")["fare_amount"].mean()
pred = valid_df["passenger_count"].map(group_mean).fillna(global_mean)
```

見 [Baseline 與錯誤分析](../evaluation/baselines-and-error-analysis.md)。

## 4. 特徵工程通常勝過花俏模型

表格競賽早期的提升多半來自特徵：

| 方向 | 例子 |
| --- | --- |
| 分組聚合 | 每個使用者的平均消費、每家店的平均銷量 |
| 計數 / 頻率 | 類別出現次數 |
| 時間拆解 | 小時、星期、是否假日 |
| 交互作用 | 兩特徵相乘或相除 |
| 缺失指標 | 是否缺失 |
| Target encoding | **只能在 fold 內計算**，否則幾乎必然洩漏（見 [類別編碼](../preprocessing/categorical-encoding.md)） |

## 5. 流程可信後才調參

順序：切分與指標對齊 → baseline → 核心特徵 → [調參](hyperparameter-tuning.md)。太早調參，只是在壞的驗證上把錯誤流程調到最好看。

## 6. Ensemble：Blending vs Stacking

| | Blending | Stacking |
| --- | --- | --- |
| 做法 | 多個模型的預測直接加權平均 | 用各模型的 **out-of-fold (OOF) 預測**當第二層模型的輸入 |
| 優點 | 簡單、不容易出錯 | 能學到模型之間的互補性 |
| 風險 | 權重若在 validation 上調也會過擬合 | OOF 做錯就洩漏 |

見 [Stacking](../supervised-learning/ensemble/stacking.md)、[Voting](../supervised-learning/ensemble/voting.md)。

## 7. Public leaderboard 是訊號，不是真相

理想狀況是 local score 變好、public LB 也大致同步變好。長期不一致時：

| 可能原因 | 檢查 |
| --- | --- |
| Validation 切法與測試分布不符 | 測試集是否在時間上、分組上不同 |
| 洩漏 | 特徵是否用到測試時拿不到的資訊 |
| Public LB 樣本太小 | 波動本來就大，不要追 |
| 對 validation 或 public LB 過度調整 | 最後的 private LB 會掉（shake-up） |

## 實務習慣

| 習慣 | 原因 |
| --- | --- |
| 固定 random seed、存下 folds | 比較時減少雜訊 |
| 記錄每次實驗的資料版本、特徵集合、分數 | 知道哪個改動有效（可用 [MLflow](../production/mlflow.md)） |
| submission 有命名規則 | 不要只有 `submission_final_v7.csv` |
| 單模型穩定後再做 ensemble | 基礎不穩時 ensemble 只是掩蓋問題 |

## 常見失敗

| 失敗 | 結果 |
| --- | --- |
| Local validation 設計錯 | 所有改動的判斷都不可靠 |
| 在整份資料上做 target-aware 特徵 | 洩漏 |
| 把 public LB 當調參集 | Private LB 大幅下滑 |
| 沒有 baseline | 無法判斷改動是否有效 |
