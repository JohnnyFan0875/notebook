# Kaggle Competition Workflow

Kaggle 競賽最容易讓人誤會的地方，是以為它只是「多試幾個模型，看 leaderboard 分數」。實際上，穩定進步的關鍵通常是 workflow 品質，而不是某個神奇模型。

## Core Loop

可以先把整體流程想成：

1. 理解比賽任務與評估指標
2. 建立 local validation
3. 做一個可靠 baseline
4. 逐步改 feature、model、validation 或 ensemble
5. 用 submission 驗證 local score 和 public leaderboard 是否一致

如果第二步沒有做對，後面所有 feature engineering 和 tuning 都可能只是在追假分數。

## Start with the Metric, Not the Model

競賽第一件事不是選 XGBoost 或 neural net，而是搞清楚：

- 預測目標是 regression、classification 還是 ranking
- 官方 metric 是 RMSE、AUC、log loss 還是別的
- 測試資料與訓練資料是否可能有時間差、群組差或分布漂移

很多 Kaggle 問題其實不是模型不夠強，而是 validation metric 和 competition metric 沒對齊。

## Build Local Validation Early

最基本情況可以先切出一塊 hold-out：

```python
from sklearn.model_selection import train_test_split

train_part, valid_part = train_test_split(
    train_df,
    test_size=0.3,
    random_state=123
)
```

但更重要的是切分方式要符合資料結構：

- i.i.d. tabular data -> `KFold`
- classification with class imbalance -> `StratifiedKFold`
- time-dependent data -> `TimeSeriesSplit`
- grouped entities -> group-aware split

Key point: good local validation 不只是「切一塊資料」，而是盡量模擬 competition test set 的生成方式。

## Compare Public Leaderboard with Local Score

submission 的角色不只是上傳分數，而是檢查你的 local validation 是否可信。

理想狀況是：

- local score 變好
- public leaderboard 也大致同步變好

如果兩者長期不一致，常見原因包括：

- validation strategy 和 test distribution 不匹配
- leakage
- public leaderboard sample 太小，波動太大
- 你正在過度適應 validation fold

## Baselines Should Be Simple but Honest

baseline 不是用來拿高分，而是用來提供穩定比較基準。

例如回歸問題，你可以先做：

- global mean baseline
- group mean baseline
- 簡單樹模型或線性模型

像這種 group mean baseline 就很常見：

```python
naive_prediction_groups = (
    train_df.groupby("passenger_count")["fare_amount"]
    .mean()
)
```

一個好的 baseline 至少要滿足：

- 可重現
- 評估方式正確
- 能讓你判斷新改動到底有沒有真的進步

## Feature Engineering Often Beats Fancy Modeling

在表格競賽裡，早期提升很多時候來自 feature engineering，而不是直接上更複雜模型。

常見方向：

- group aggregates
- count / frequency features
- time decomposition
- interaction features
- missingness indicators
- target-dependent encoding，但只能在正確 fold 內計算

尤其像 mean target encoding 這類方法，若不是在 fold 內做，幾乎很容易直接造成 leakage。

## Cross-Validation Is the Main Score, Not a Decoration

Kaggle workflow 裡，單次 hold-out 分數通常不夠穩。

更常見做法是：

- 跑 K-fold / StratifiedKFold / TimeSeriesSplit
- 取得每個 fold 的 validation score
- 再取平均作為主要比較指標

簡化來說：

```python
overall_validation_score = sum(fold_scores) / len(fold_scores)
```

真正重要的是：

- 不只看平均
- 也看各 fold 波動

如果平均分數變好，但 fold variance 很大，通常代表策略不夠穩。

## Tune Hyperparameters Only After the Pipeline Is Trustworthy

很多人太早開始調參，結果是在壞的 validation 上把錯誤流程調到最好看。

較穩的順序通常是：

1. 先把資料切分和 metric 對齊
2. 先做 baseline
3. 先把核心 features 做好
4. 再進入 hyperparameter tuning

手動 grid 其實也是很常見的起點：

```python
for candidate_alpha in alpha_grid:
    model = Ridge(alpha=candidate_alpha)
    # fit and score on validation
```

當搜尋空間變大時，再考慮 `RandomizedSearchCV`、Optuna 或其他更有效率的方法。

## Blending vs Stacking

競賽後期常見 ensemble。

先用一句話區分：

- blending: 直接把多個 submission / prediction 加權平均
- stacking: 用 out-of-fold predictions 當第二層模型輸入

blending 的好處是：

- 簡單
- 不容易出現額外實作錯誤

stacking 的好處是：

- 更有機會學到模型互補性

但 stacking 的前提是 OOF predictions 做得正確，否則非常容易 leakage。

## Practical Competition Habits

- 固定 random seed，減少比較時的噪音
- 保留每次實驗的資料版本、特徵集合與分數
- 把 folds 存起來，避免每次重新切不同資料
- submission 要有命名規則，不要只留 `submission_final_v7.csv`
- public leaderboard 只當訊號，不當唯一真相

## Common Failure Modes

- local validation 設計錯
- 在整份資料上做 target-aware feature engineering
- 把 public leaderboard 當 tuning set
- 沒有 baseline，導致每次改動都無法比較
- ensemble 很複雜，但單模基礎其實還不穩

## Takeaway

Kaggle workflow 的核心不是「找到最強模型」，而是建立一個能讓你穩定判斷什麼真的有效的驗證與實驗系統。
