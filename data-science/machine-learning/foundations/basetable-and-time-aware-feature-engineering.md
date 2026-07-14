# Basetable and Time-Aware Feature Engineering

很多 tabular predictive modeling 專案，真正困難的地方不是先選模型，而是先把資料整理成一張可以安全訓練的 `basetable`。

`basetable` 可以先理解成：

- 一列代表一個 prediction unit，例如一位客戶、一個 donor、一筆 loan application
- 一欄代表在某個 reference date 當下可用的特徵
- 還會包含對應的 target

Key point: `basetable` 不是隨便 join 出來的一張大表，而是帶有明確時間邏輯的 modeling snapshot。

## The Core Timeline

實務上至少要先分清三件事：

1. `reference date`: 我們假設做出預測的時間點
2. `feature window`: 建立特徵時允許回看的歷史期間
3. `target window`: 預測之後，要觀察結果是否發生的期間

這三者如果沒有先定義清楚，後面的 aggregation、join、split 幾乎都很容易出錯。

## What Belongs in a Basetable

常見欄位包括：

- entity id
- reference date
- static attributes，例如地區、註冊來源、產品類型
- behavioral aggregates，例如近 30 天交易次數、近 12 個月總金額
- derived features，例如 lifetime、最近一次互動距今多久、年增率
- target

如果一個欄位的值在 reference date 當下其實還不知道，那它就不該進 basetable。

## Population Definition Comes First

建模前先定義「哪些 entity 應該進母體」。

例如：

- 只納入在 reference date 前已活躍的客戶
- 排除在 target window 開始前就已 churn 的用戶
- 排除不符合決策範圍的對象

Key point: 你不是先拿到所有資料再交給模型，而是先定義這次 prediction task 的 valid population。

## Time-Compliant Features

時間相容的特徵只使用 reference date 當下以前的資訊。

常見例子：

- `lifetime = reference_date - member_since`
- 過去一年總消費
- 過去一年互動次數
- 最近一次購買距今天數

常見錯誤則是：

- 用 target window 內的事件建立特徵
- 用最終狀態欄位回填過去 snapshot
- 在整段歷史資料上直接取最新值

這些本質上都屬於 [data leakage](data-leakage.md)。

## Aggregates Are Usually the Real Features

很多 tabular 模型的訊號其實不是原始事件，而是事件的聚合結果。

常見 aggregation 包括：

- `sum`
- `count`
- `mean`
- `max`
- `min`
- `nunique`

例如：

```python
gifts_2016 = gifts[
    (gifts["date"] >= start_2016)
    & (gifts["date"] < start_2017)
]

gifts_2016_by_donor = (
    gifts_2016.groupby("id")["amount"]
    .sum()
    .reset_index()
)
gifts_2016_by_donor.columns = ["donor_id", "sum_2016"]

basetable = basetable.merge(gifts_2016_by_donor, how="left", on="donor_id")
```

同一個原始 event table，通常可以衍生多種訊號：

- total amount
- event count
- average amount
- days since last event

## Evolutions Often Matter More Than Levels

絕對值重要，但變化方向常常更有訊號。

例如：

- 去年購買次數
- 過去兩年購買次數
- 去年與前一年差值
- 最近 3 個月平均 vs 更早 9 個月平均

這種 feature 在課程裡被稱為 evolutions，本質上就是 temporal change features。

Key point: 很多業務問題真正想知道的不是「目前值多高」，而是「它最近是在上升、下降，還是正在沉默」。

## Target Definition Must Also Respect Time

target 也不是任意從結果欄位抄進來。

你需要明確定義：

- target period 從哪天開始
- target period 到哪天結束
- target 的規則是 binary、count，還是 thresholded aggregate

例如：

```python
start_target = datetime(year=2017, month=1, day=1)
end_target = datetime(year=2018, month=1, day=1)

gifts_target = gifts[
    (gifts["date"] >= start_target)
    & (gifts["date"] < end_target)
]

gifts_target_byid = gifts_target.groupby("id")["amount"].sum().reset_index()
targets = list(gifts_target_byid["id"][gifts_target_byid["amount"] > 500])

basetable["target"] = [
    1 if donor_id in targets else 0
    for donor_id in basetable["donor_id"]
]
```

這裡的重點不是語法，而是 target 是在 reference date 之後才觀察到的結果。

## Seasonality Changes What "Recent" Means

如果資料有季節性，feature window 的選法不能只看「最近」。

例如零售、捐款、旅遊、節慶型流量，常會出現：

- 月份差異
- 週期性尖峰
- 假日效應

這時候要先檢查：

```python
gifts.groupby("month")["amount"].mean()
gifts.groupby("month").size()
```

如果 seasonality 很強，拿 `May 2018` 的 snapshot 訓練去預測 `January 2019`，可能就不如拿 `January 2018` 的 snapshot 更合理。

Key point: 對 seasonal problem 來說，「時間上最近」不一定比「季節上相近」更有代表性。

## Multiple Snapshots Can Increase Sample Size

有些業務問題單一 snapshot 的 target 太少，會讓 positive class 稀缺。

一個常見解法是：

- 用多個 reference dates 各自建立 basetable
- 確保每個 snapshot 都遵守同一套時間規則
- 再把多個 basetable 疊起來訓練

例如概念上：

```python
basetable = pd.concat(
    [basetable_april2018, basetable_march2018],
    ignore_index=True,
)
```

但要注意：

- 不同 snapshot 的同一 entity 可能重複出現
- validation 不應讓過度相近的 snapshot 同時落在 train 與 test
- seasonality 仍然要一起考慮

## Predictor Insight Tables And Graphs

在 basetable 建好之後，常見下一步不是立刻換模型，而是先看：

- 哪些欄位和 target incidence 有穩定關係
- 哪些欄位只是 sample 很小時看起來特別極端
- 哪些欄位雖然有預測力，但業務上難以解釋

一個很實用的工具是 predictor insight table。它的核心做法很簡單：

1. 針對某個 predictor 分組
2. 計算每組的 `Incidence`
3. 同時保留每組的 `Size`

例如：

```python
import numpy as np

def create_pig_table(df, target, variable):
    groups = df[[target, variable]].groupby(variable)
    pig_table = groups[target].agg(
        Incidence=np.mean,
        Size=np.size,
    ).reset_index()
    return pig_table
```

其中：

- `Incidence`: 該群組 target 的平均值或命中率
- `Size`: 該群組樣本數

Key point: 只看 incidence 容易被小樣本騙到，所以 `Size` 必須一起看。

## Continuous Variables Usually Need Binning First

如果 predictor 是連續變數，通常先離散化再看比較直覺。

```python
basetable["disc_age"] = pd.qcut(basetable["age"], 5)
pig_table = create_pig_table(basetable, "target", "disc_age")
```

常見做法包括：

- `pd.qcut()`: 依分位數切箱，讓每組樣本數比較平均
- `pd.cut()`: 用固定業務區間切箱，例如年齡帶、金額區間

兩者差異可以這樣記：

- `qcut`: 偏探索與穩定樣本量
- `cut`: 偏業務語意與可溝通性

## What These Graphs Help You Check

predictor insight graph 很適合拿來檢查：

- incidence 是否大致單調
- 是否只有極少數 bin 在撐起表面上的效果
- 某個類別的高 incidence 是否只是因為樣本太少
- 分箱後是否出現奇怪跳點，暗示資料品質或分箱方式有問題

這些圖不等於因果分析，也不等於模型係數解讀，但很適合當成：

- feature review
- model sanity check
- 和業務一起討論欄位含義的橋樑

## A Good Interpretation Habit

看到某個群組 incidence 很高時，至少要一起問：

1. 這個群組的 `Size` 大不大？
2. 這個差異是否可能只是 noise？
3. 這個欄位在 reference date 當下真的可得嗎？
4. 這個 pattern 是否符合業務常識？

如果曲線很好看，但欄位其實帶有 leakage、樣本太小，或只能事後才知道，那它就不該成為可上線的 predictor。

## A Practical Checklist

在建立 basetable 前，可以先問自己：

1. prediction unit 是誰？
2. reference date 是哪一天？
3. target window 是什麼？
4. 每個 feature 是否在 reference date 當下可得？
5. 聚合 window 是否只看過去？
6. population 是否已定義清楚？
7. 是否存在 seasonality，需要相似月份或多 snapshot？

## Related Concepts

- [Feature Engineering Principles](feature-engineering-principles.md)
- [Data Leakage](data-leakage.md)
- [Data Splitting and Leakage](../workflow/data-splitting-and-leakage.md)
- [Imputation](../preprocessing/imputation.md)

[Back to Foundations](README.md)
