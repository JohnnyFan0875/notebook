[視覺化](../README.md) › [Matplotlib](README.md) › 折線圖

# 折線圖 (Line Plot)

折線圖呈現一個變數沿著有順序的 x（時間、劑量、濃度、訓練 epoch）的變化。x 沒有順序（類別、樣本編號）時連線沒有意義，改用點圖或長條圖。

```python
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

flights = sns.load_dataset("flights")
yearly = flights.groupby("year")["passengers"].agg(["mean", "std"])

fig, axes = plt.subplots(1, 3, figsize=(13, 3.5), layout="constrained")

# 1. 多條線 + 圖例：每條線給 label
for month in ["Jan", "Jul"]:
    d = flights[flights["month"] == month]
    axes[0].plot(d["year"], d["passengers"], marker="o", label=month)
axes[0].legend(title="Month")

# 2. 誤差線：yerr 可以是常數、陣列，或 (下, 上) 兩列
axes[1].errorbar(yearly.index, yearly["mean"], yerr=yearly["std"], fmt="-o", capsize=4, ecolor="gray")
axes[1].set_title("Mean ± SD across months")

# 3. 誤差帶 + 參考線 / 參考區間
axes[2].plot(yearly.index, yearly["mean"], color="steelblue")
axes[2].fill_between(yearly.index, yearly["mean"] - yearly["std"],
                     yearly["mean"] + yearly["std"], alpha=0.3, color="steelblue")
axes[2].axhline(300, color="tomato", linestyle="--", label="target")
axes[2].axvline(1955, color="gray", linestyle=":")
axes[2].axvspan(1958, 1960, color="gray", alpha=0.2)
axes[2].legend()
```

| 參數 / 方法 | 用途 |
| --- | --- |
| `marker` | 點形狀：`"o"`、`"s"`、`"^"`、`"."` |
| `linestyle` | `"-"`、`"--"`、`":"`、`"-."`、`"none"` |
| `color` | 名稱（`"steelblue"`）、`"tab:blue"`、`"C0"`（預設色環第 1 色）、hex |
| `ax.errorbar(x, y, yerr=, fmt=, capsize=)` | 誤差線；`fmt` 同時設定點與線 |
| `ax.fill_between(x, low, high, alpha=)` | 誤差帶 / 信賴帶 |
| `ax.axhline` / `ax.axvline` | 水平 / 垂直參考線（門檻、事件日期） |
| `ax.axhspan` / `ax.axvspan` | 標出一段數值或時間區間 |

> 誤差線一定要在圖說寫明是 SD、SE 還是 95% CI，見 [圖表設計原則](../chart-design-principles.md#常見誤導)。

## 子圖比較

```python
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.plot(yearly.index, yearly["mean"]); ax1.set_ylabel("Mean")
ax2.plot(yearly.index, yearly["std"]);  ax2.set_ylabel("SD")
```

兩個變數單位不同時，上下子圖共用 x 軸通常比雙 y 軸更不易誤導；真的需要雙軸見 [進階：雙軸與註解](advanced.md)。

## 時間序列

x 為日期時，先把日期轉成 `datetime64` 並排序，Matplotlib 會自動格式化刻度；rolling、resample 等時間序列圖見 [pandas Plotting](../pandas-plotting.md#時間序列)。
