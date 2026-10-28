[資料處理與 EDA](../README.md) › [視覺化](README.md) › pandas Plotting

# pandas Plotting

`Series.plot()` / `DataFrame.plot()` 直接從資料畫圖，是 EDA 最快的第一眼：index 自動當 x 軸、每欄一條線、回傳 Matplotlib `Axes` 可以繼續調整。需要分組統計圖改用 [Seaborn](seaborn/README.md)，細節控制用 [Matplotlib](matplotlib/README.md)；存活曲線見 [存活分析視覺化](../../statistics/survival-analysis/visualization.md)。

## `kind` 速查

| `kind=` / 方法 | 圖 | 資料形狀 |
| --- | --- | --- |
| `"line"`（預設）/ `.plot.line()` | 折線 | index = x，每欄一條線 |
| `"bar"` / `"barh"` | 長條 | index = 類別，每欄一組 |
| `"hist"` | 直方圖 | 每欄一個分布 |
| `"box"` | 箱型圖 | 每欄一個箱子 |
| `"kde"` / `"density"` | 密度曲線 | 每欄一條（需 scipy） |
| `"area"` | 面積（預設堆疊） | 組成隨時間變化 |
| `"scatter"` / `"hexbin"` | 散布 / 六角格 | 需指定 `x=`、`y=` 欄名 |
| `"pie"` | 圓餅 | 少用，見 [圖表設計原則](chart-design-principles.md) |

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

iris = sns.load_dataset("iris")

# 1. 基本：回傳 ax，可再用 Matplotlib 調整
ax = iris["sepal_length"].plot.hist(bins=20, alpha=0.7, title="Sepal length")
ax.set_xlabel("cm")

# 2. 多欄：每欄一組
iris.plot(kind="box")                                   # 所有數值欄的箱型圖
iris[["sepal_length", "sepal_width"]].plot.hist(alpha=0.5, bins=20)
iris.plot.scatter(x="sepal_length", y="petal_length", c="petal_width", colormap="viridis")

# 3. 先彙總再畫：groupby 結果的 index 就是 x 軸
iris.groupby("species").mean().plot.bar(rot=0)

# 4. 每欄一個子圖
iris.plot(subplots=True, layout=(2, 2), figsize=(10, 6), sharex=True)
```

| 參數 | 用途 |
| --- | --- |
| `ax=` | 畫在既有的 axes 上（組合多張圖） |
| `subplots=True`、`layout=` | 每欄一個子圖 |
| `figsize`、`title`、`xlabel`、`ylabel`、`rot` | 常用外觀 |
| `logy=True` / `logx=True` | log 軸 |
| `colormap=` | 多欄時的色盤，如 `"Dark2"` |
| `secondary_y=["col"]` | 指定欄改用右側 y 軸 |

| 方法 | 差異 |
| --- | --- |
| `s.plot.hist()` | 回傳 `Axes`；接受 `title=` 等 `.plot` 共通參數 |
| `s.hist()` / `df.hist()` | 直接呼叫 Matplotlib `hist`；`df.hist()` 自動每欄一個子圖、`by=` 依類別分子圖；**不接受** `title=`（會報錯） |
| `df.boxplot(column=, by=)` | 依類別分組的箱型圖 |

## 時間序列

時間序列圖的目的：看趨勢、季節性、突變點與異常事件。關鍵是先有一個排序好的 `DatetimeIndex`。

```python
# 1. 準備：轉日期、設 index、排序
df["date"] = pd.to_datetime(df["date"], errors="coerce")   # 解析失敗 → NaT
ts = df.set_index("date").sort_index()

# 2. 第一眼 + 切一段時間放大
ax = ts["value"].plot(figsize=(12, 4), linewidth=1)
ts.loc["2020":"2021", "value"].plot()

# 3. 標出事件與區間
ax = ts["value"].plot()
ax.axvline("2020-03-01", color="tomato", linestyle="--")      # 事件日期
ax.axhline(100, color="gray", linestyle=":")                  # 門檻
ax.axvspan("2020-03-01", "2020-06-01", color="gray", alpha=0.2)

# 4. 平滑：rolling 視窗配合資料節奏（日資料 7 / 30、週資料 52、月資料 12）
ax = ts["value"].plot(alpha=0.3, label="raw")
ts["value"].rolling(window=30, center=True).mean().plot(ax=ax, label="30-day mean")
ax.legend()

# 5. 彙總到較粗的時間單位（pandas ≥ 2.2：月 / 季 / 年底用 ME / QE / YE）
ts["value"].resample("W").mean()
ts["value"].resample("ME").mean().plot()
ts["value"].resample("QE").sum()
ts["value"].resample("YE").mean()

# 6. 多條序列
ax = ts.plot(colormap="Dark2", figsize=(12, 5))
ax.legend(bbox_to_anchor=(1.0, 0.5), loc="center left")   # 圖例移到圖外
ts.plot(subplots=True, figsize=(12, 10), linewidth=0.5)    # 線太多改 small multiples
ts.plot.area()                                              # 組成比例隨時間變化
```

| 頻率 | pandas < 2.2 | pandas ≥ 2.2（3.x 舊別名已移除） |
| --- | --- | --- |
| 月底 | `"M"` | `"ME"` |
| 季底 | `"Q"` | `"QE"` |
| 年底 | `"Y"` / `"A"` | `"YE"` |
| 小時 | `"H"` | `"h"` |
| 日、週 | `"D"`、`"W"` | 不變 |

| 讀圖時問 | 下一步 |
| --- | --- |
| 有長期趨勢嗎？ | rolling mean、resample；分解見 [時間序列分解](../../statistics/time-series-analysis/decomposition.md) |
| 有季節性 / 重複週期嗎？ | 依月份或星期分組的箱型圖；[自相關](../../statistics/time-series-analysis/autocorrelation.md) |
| 有突變、尖峰、位階改變嗎？ | 對照事件時間（儀器更換、政策改變），用 `axvline` 標出 |
| 值的分布？ | `ts.plot.hist()`、`ts.plot.kde()`、`ts.boxplot()` |
| 多條序列擠在一起？ | `subplots=True` 或挑幾條重點序列 |

日期解析、時區與 `resample` 的細節見 [日期與時間](../../python-foundations/datetime.md)。
