[視覺化](../README.md) › [Matplotlib](README.md) › 進階：雙軸與註解

# 進階：雙軸與註解 (Dual Axes & Annotation)

兩個常用來「說故事」的工具：雙 y 軸把不同單位的變數放在同一條 x 軸上，註解 (annotation) 把讀者的目光帶到關鍵點。

## 雙 y 軸 (`twinx`)

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

x = pd.date_range("2000-01", periods=50, freq="ME")     # pandas ≥ 2.2：月底頻率是 "ME"，"M" 已移除
temp = 20 + 8 * np.sin(np.linspace(0, 3 * np.pi, 50))
cases = 100 + 40 * np.cos(np.linspace(0, 3 * np.pi, 50))

fig, ax1 = plt.subplots(figsize=(8, 4), layout="constrained")
ax1.plot(x, temp, color="tab:blue")
ax1.set_ylabel("Temperature (°C)", color="tab:blue")
ax1.tick_params(axis="y", colors="tab:blue")

ax2 = ax1.twinx()                                        # 共用 x 軸的第二個 y 軸
ax2.plot(x, cases, color="tab:red")
ax2.set_ylabel("Cases", color="tab:red")
ax2.tick_params(axis="y", colors="tab:red")
```

| 方法 | 用途 |
| --- | --- |
| `ax.twinx()` | 共用 x、右側新 y 軸 |
| `ax.twiny()` | 共用 y、上方新 x 軸 |
| `ax.secondary_yaxis("right", functions=(f, f_inv))` | 同一變數的另一種單位（°C ↔ °F、log2 ↔ 原始倍數），不畫新資料 |

> 雙軸的兩個刻度可以任意縮放，讓兩條線看起來多相關都可以。優先考慮上下子圖共用 x 軸，或把兩個變數標準化到同一尺度；真的要用時，軸標籤顏色要與線條一致。若只是同一變數換單位，用 `secondary_yaxis` 不會有這個問題。

## 註解 (`annotate`)

```python
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.plot(x, cases, color="tab:red")

i = cases.argmax()
ax.annotate(
    f"peak: {cases[i]:.0f}",
    xy=(x[i], cases[i]),                  # 箭頭指向的資料點
    xytext=(x[i + 8], cases[i] - 10),     # 文字位置（資料座標）
    arrowprops={"arrowstyle": "->", "color": "gray"},
)
ax.text(0.02, 0.95, "n = 50 months", transform=ax.transAxes, va="top")   # 相對 axes 的位置（0–1）
ax.axvspan(x[10], x[20], color="gray", alpha=0.2)                        # 標出一段期間
```

| 方法 | 用途 |
| --- | --- |
| `ax.annotate(text, xy, xytext, arrowprops)` | 帶箭頭的文字；`textcoords="offset points"` 讓 `xytext` 改成相對 `xy` 的位移 |
| `ax.text(x, y, s, transform=ax.transAxes)` | 固定在圖框角落的文字（n、p 值、面板字母 A / B） |
| `ax.axvspan` / `ax.axhspan` | 標出時間區間或數值範圍 |
| `ax.bar_label(container)` | 長條上的數值標籤 |

> 散布圖中標出多個基因名稱時，文字常互相重疊；可用 `adjustText` 套件自動排開（R 對應 `ggrepel`）。

## 相關

| 主題 | 連結 |
| --- | --- |
| 參考線 `axhline` / `axvline` | [折線圖](line-plot.md) |
| 缺失值視覺化（`missingno`） | [pandas 缺值](../../../python-foundations/pandas/missing-data.md#3-missingno-視覺化) |
