[視覺化](../README.md) › [Matplotlib](README.md) › 箱型圖

# 箱型圖 (Box Plot)

箱型圖用五個位置摘要一組數值的分布，適合並排比較多組並標出離群值。注意鬚 (whisker) 預設**不是**最小值與最大值。

## 怎麼讀

| 元素 | 意義（Matplotlib / Seaborn 預設） |
| --- | --- |
| 箱子下緣 / 上緣 | Q1（第 25 百分位）/ Q3（第 75 百分位）；箱高 = IQR |
| 箱中線 | 中位數 |
| 鬚 | 延伸到 **[Q1 − 1.5·IQR, Q3 + 1.5·IQR] 範圍內最極端的資料點**（`whis=1.5`） |
| 鬚外的點 | 標為離群值 (flier)；只是規則標記，不代表是錯誤資料 |
| notch（凹口） | 中位數的近似 95% CI：$\text{median} \pm 1.57 \cdot \text{IQR}/\sqrt{n}$；兩組凹口不重疊 ≈ 中位數有差異 |

> 箱型圖看不到雙峰與樣本數。n 小（< 30）或懷疑分布有多個峰時，疊加原始點或改用 violin plot，見 [圖表設計原則](../chart-design-principles.md#常見誤導)。

## 寫法

```python
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

iris = sns.load_dataset("iris")
groups = [d["sepal_length"].to_numpy() for _, d in iris.groupby("species")]
names = iris["species"].unique()

fig, axes = plt.subplots(1, 3, figsize=(14, 4), layout="constrained")

# 1. 分組箱型圖：傳入 list of arrays
axes[0].boxplot(groups, tick_labels=names)          # Matplotlib ≥ 3.9：labels= 已改名 tick_labels=

# 2. 水平 + notch + 填色
axes[1].boxplot(groups, tick_labels=names, orientation="horizontal",   # ≥ 3.10；舊版 vert=False
                notch=True, patch_artist=True,
                boxprops={"facecolor": "lightblue"}, medianprops={"color": "tomato"})

# 3. 疊加原始點（加一點水平抖動 jitter）
rng = np.random.default_rng(0)
axes[2].boxplot(groups, tick_labels=names, showfliers=False)   # 已畫原始點，就不重複畫離群點
for i, g in enumerate(groups, start=1):
    axes[2].scatter(i + rng.uniform(-0.12, 0.12, len(g)), g, s=10, alpha=0.5, color="gray")
```

| 參數 | 用途 |
| --- | --- |
| `whis` | 鬚的長度倍數（預設 1.5）；`whis=(5, 95)` 改為第 5–95 百分位 |
| `showfliers=False` | 不畫離群點 |
| `showmeans=True` | 加上平均數標記 |
| `widths` | 箱子寬度 |
| `positions` | 自訂每個箱子的 x 位置（做分組並排） |

| 版本差異 | 舊寫法 | 新寫法 |
| --- | --- | --- |
| Matplotlib 3.9 | `labels=` | `tick_labels=`（3.11 已移除 `labels=`） |
| Matplotlib 3.10 | `vert=False` | `orientation="horizontal"`（3.11 起 `vert` 會發出 deprecation warning） |

> 從 DataFrame 依欄位分組畫，Seaborn 的 `sns.boxplot(data=, x=, y=)` 或 `catplot(kind="box")` 更省事，見 [Seaborn 類別圖](../seaborn/categorical.md)。
