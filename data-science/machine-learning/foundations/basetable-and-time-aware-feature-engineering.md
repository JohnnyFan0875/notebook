[Machine Learning](../README.md) › [基礎概念](README.md) › Basetable 與時間感知特徵

# Basetable 與時間感知特徵工程 (Basetable and Time-Aware Feature Engineering)

很多表格預測專案真正難的不是選模型，而是把事件資料整理成一張可以安全訓練的 **basetable**：一列是一個預測單位（客戶、捐款人、病人、貸款申請），每欄是在某個 reference date 當下可得的特徵，再加上目標。

> Basetable 不是隨便 join 出來的大表，而是帶有明確時間邏輯的建模快照 (modeling snapshot)。

## 時間軸

```
 2016-01-01                2017-01-01                2018-01-01
     ├──── 特徵窗 ─────────────┤├──── 目標窗 ──────────────┤
                               ↑
                         reference date
     只能用這段資料算特徵          在這段觀察結果是否發生
```

| 時間點 | 定義 | 常見錯誤 |
| --- | --- | --- |
| Reference date | 假設做出預測的時間點 | 沒有明確定義，不同欄位各用各的時間 |
| 特徵窗 (feature window) | 建特徵時允許回看的歷史期間 | 用到 reference date 之後的事件 |
| 目標窗 (target window) | 預測之後觀察結果的期間 | 目標窗與特徵窗重疊 |

這三者沒先定清楚，後面的聚合、join、切分幾乎都會出錯。

## Basetable 的組成

| 欄位類型 | 例子 |
| --- | --- |
| 實體 ID | `donor_id`、`patient_id` |
| Reference date | 快照日期 |
| 靜態屬性 | 地區、註冊來源、產品類型 |
| 行為聚合 | 近 30 天交易次數、近 12 個月總金額 |
| 衍生特徵 | 會員年資、最近一次互動距今天數、年增率 |
| 目標 | 目標窗內是否發生事件 |

> 一個欄位的值在 reference date 當下還不知道，就不能進 basetable。

## 1. 先定義母體 (Population)

先決定哪些實體應該進入這次的預測任務，而不是拿到所有資料就丟給模型：

- 只納入 reference date 前已活躍的客戶
- 排除目標窗開始前就已流失 (churn) 的用戶
- 排除不在決策範圍內的對象

## 2. 時間相容的特徵

| 合法（只用 reference date 前的資訊） | 洩漏 |
| --- | --- |
| `lifetime = reference_date - member_since` | 用目標窗內的事件建特徵 |
| 過去一年總消費、互動次數 | 用最終狀態欄位回填過去的快照 |
| 最近一次購買距今天數 | 在整段歷史上直接取最新值 |

這些錯誤本質上都是 [資料洩漏](data-leakage.md)。

## 3. 聚合才是真正的特徵

表格模型的訊號多半來自事件的聚合（`sum`、`count`、`mean`、`max`、`min`、`nunique`、距上次事件天數），而且**變化趨勢 (evolution)** 常比絕對值更有訊號：去年與前年的差、近 3 個月平均 vs 更早 9 個月平均。很多問題真正想知道的不是「現在多高」，而是「最近在上升、下降，還是沉寂了」。

```python
import pandas as pd
from datetime import datetime

# 1. 特徵：2016 年的捐款總額（特徵窗 = 2016）
start_2016, start_2017 = datetime(2016, 1, 1), datetime(2017, 1, 1)
gifts_2016 = gifts[(gifts["date"] >= start_2016) & (gifts["date"] < start_2017)]
sum_2016 = (gifts_2016.groupby("id")["amount"].sum()
            .rename("sum_2016").rename_axis("donor_id").reset_index())
basetable = basetable.merge(sum_2016, how="left", on="donor_id")
basetable["sum_2016"] = basetable["sum_2016"].fillna(0)      # 沒捐款 = 0，不是缺失

# 2. 目標：2017 年（目標窗）捐款總額 > 500
start_target, end_target = datetime(2017, 1, 1), datetime(2018, 1, 1)
gifts_target = gifts[(gifts["date"] >= start_target) & (gifts["date"] < end_target)]
total = gifts_target.groupby("id")["amount"].sum()
basetable["target"] = basetable["donor_id"].isin(total.index[total > 500]).astype(int)
```

目標的規則（二元、計數、還是門檻化的聚合）與期間起訖都要明確寫下。

## 4. 季節性改變「最近」的意義

```python
gifts.groupby(gifts["date"].dt.month)["amount"].agg(["mean", "size"])   # 每月平均與筆數
```

季節性強時（零售、捐款、旅遊），用 2018 年 5 月的快照訓練去預測 2019 年 1 月，可能不如用 2018 年 1 月的快照合理。

> 對季節性問題，「季節上相近」常比「時間上最近」更有代表性。

## 5. 多個快照增加樣本數

單一快照的正類太少時，可以用多個 reference date 各建一張 basetable，再疊起來訓練：

```python
basetable = pd.concat([basetable_2018_03, basetable_2018_04], ignore_index=True)
```

| 注意 | 原因 |
| --- | --- |
| 每個快照都遵守同一套時間規則 | 否則特徵定義不一致 |
| 同一實體會重複出現 | 相鄰月份的快照幾乎一樣 → 驗證時要依實體分組（`GroupKFold`）或依時間切分 |
| 仍要考慮季節性 | 快照月份組成會影響模型 |

## 6. Predictor Insight Table

Basetable 建好後，先檢視每個特徵與目標的關係，而不是立刻換模型。Predictor insight table 對某個特徵分組，計算每組的**目標發生率 (Incidence)** 與**樣本數 (Size)**：

```python
def create_pig_table(df, target, variable):
    return (df.groupby(variable, observed=True)[target]
              .agg(Incidence="mean", Size="size")
              .reset_index())

# 連續變數先分箱
basetable["disc_age"] = pd.qcut(basetable["age"], 5)       # 依分位數：各箱樣本數相近
pig_table = create_pig_table(basetable, "target", "disc_age")
```

| 分箱 | 特性 | 適合 |
| --- | --- | --- |
| `pd.qcut()` | 依分位數切，各組樣本數平均 | 探索、穩定的樣本量 |
| `pd.cut()` | 依固定區間切（年齡帶、金額區間） | 業務語意、溝通 |

畫成 predictor insight graph（長條 = Size、折線 = Incidence）可以檢查：

| 檢查 | 看到時的意義 |
| --- | --- |
| Incidence 是否大致單調 | 不單調可能是真實的非線性，也可能是分箱問題 |
| 是否只有少數箱撐起效果 | 效果可能不穩定 |
| 高 Incidence 的組是否樣本很小 | 可能只是雜訊 |
| 奇怪的跳點 | 資料品質或分箱方式有問題 |

> 只看 Incidence 容易被小樣本騙，Size 一定要一起看。這張表不是因果分析，但很適合當特徵審查、模型合理性檢查，以及和業務端討論欄位意義的橋樑。

看到某組 Incidence 很高時，至少要問：樣本數夠嗎？可能只是雜訊嗎？這個欄位在 reference date 當下真的拿得到嗎？符合業務常識嗎？

## 建 basetable 前的檢查清單

1. 預測單位是誰？
2. Reference date 是哪一天？
3. 目標窗是什麼？目標規則是什麼？
4. 每個特徵在 reference date 當下都拿得到嗎？
5. 聚合窗只看過去嗎？
6. 母體定義清楚了嗎？
7. 有季節性嗎？需要相似月份或多快照嗎？

相關：[特徵工程原則](feature-engineering-principles.md)、[資料切分與洩漏](../workflow/data-splitting-and-leakage.md)、[存活分析](../../statistics/survival-analysis/README.md)（目標是「何時發生」而非「是否發生」時）。
