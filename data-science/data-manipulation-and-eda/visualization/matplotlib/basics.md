[視覺化](../README.md) › [Matplotlib](README.md) › 基礎

# Matplotlib 基礎 (Basics)

一張圖由 `Figure`（整張畫布）與一個或多個 `Axes`（座標系，真正畫資料的地方）組成。掌握 `fig, ax = plt.subplots()` 之後，標籤、刻度、尺度、存檔都是對這兩個物件呼叫方法。高階的統計圖見 [Seaborn 基礎](../seaborn/basics.md)。

## 結構

```text
Figure                    fig：尺寸、整體標題、存檔
└── Axes (一或多個)        ax：資料、標題、軸標籤、圖例
    ├── XAxis / YAxis      刻度 (ticks)、刻度標籤、尺度 (linear / log)
    └── Artists            Line2D、PathCollection（散點）、Rectangle（長條）、Text …
```

## 建立與設定

```python
import matplotlib.pyplot as plt
import seaborn as sns

iris = sns.load_dataset("iris")

# 1. 建立：figsize 單位是英吋；layout="constrained" 自動避免標籤重疊
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.plot(iris.index, iris["sepal_length"], marker="o", color="tab:red", linestyle="--")

# 2. 標題與標籤（一次設定多個）
ax.set(title="Sepal length by index", xlabel="Index", ylabel="Sepal length (cm)")

# 3. 範圍、尺度、刻度
ax.set_xlim(0, 50)
ax.set_ylim(4, 8)
ax.set_yscale("log")                     # "linear"、"log"、"symlog"（含 0 或負值）、"logit"
ax.set_xticks(range(0, 51, 10))
ax.set_xticks([0, 25, 50], labels=["start", "mid", "end"])   # 位置與標籤一起設
ax.tick_params(axis="x", rotation=45)

# 4. 多子圖
fig, axes = plt.subplots(2, 2, figsize=(8, 6), sharex=True, layout="constrained")
axes[0, 0].hist(iris["sepal_length"])
fig.suptitle("Iris measurements")

# 5. 存檔與關閉
fig.savefig("iris.png", dpi=300, bbox_inches="tight")   # 點陣
fig.savefig("iris.pdf")                                  # 向量，論文用
plt.close(fig)        # 迴圈中大量產圖時一定要關，否則記憶體持續累積
```

| 想做 | 方法 |
| --- | --- |
| 改尺寸 | `plt.subplots(figsize=(w, h))` 或 `fig.set_size_inches(w, h)` |
| 子圖共用軸 | `sharex=True` / `sharey=True` |
| 不規則版面 | `fig.subplot_mosaic("AAB;CCB")` |
| 清空 vs 關閉 | `ax.cla()` 清一個 axes；`plt.clf()` 清整張 figure 但保留視窗；`plt.close(fig)` 釋放記憶體 |
| 在 notebook 顯示 | 最後一行回傳 figure 或呼叫 `plt.show()`；腳本中 `plt.show()` 會阻塞直到關閉視窗 |

## 樣式 (Style)

```python
plt.style.available                 # 列出內建樣式
plt.style.use("ggplot")             # 全域套用
with plt.style.context("seaborn-v0_8-whitegrid"):   # 只影響這個區塊
    fig, ax = plt.subplots()
plt.rcParams["font.size"] = 12      # 個別 rc 參數
```

> Matplotlib 3.6 起內建的 `"seaborn"` 系列樣式改名為 `"seaborn-v0_8-*"`；直接用 Seaborn 的外觀請改呼叫 `sns.set_theme()`。

## 中文字型

Matplotlib 預設字型沒有中文，會顯示成方框；設定系統上有的 CJK 字型：

| 平台 | 字型名稱 |
| --- | --- |
| Windows | `Microsoft JhengHei`（正黑體） |
| macOS | `PingFang TC`、`Heiti TC`、`Arial Unicode MS` |
| Linux | `Noto Sans CJK TC`（需安裝 `fonts-noto-cjk`） |

```python
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei", "PingFang TC", "Noto Sans CJK TC"]
plt.rcParams["axes.unicode_minus"] = False   # 負號改用 ASCII "-"，避免中文字型缺 U+2212 顯示成方框
```

> 要分享的程式或論文圖，圖內文字用英文最保險，不受對方字型影響。
