[視覺化](../README.md) › [Seaborn](README.md) › 關係圖

# 關係圖 (Relational Plots)

兩個連續變數之間的關係：`scatterplot` 看點的分布，`lineplot` 看 y 隨有序的 x（時間、劑量）如何變化。`relplot(kind=...)` 是 figure-level 版，可以 facet。

## 散布圖

```python
import seaborn as sns
import matplotlib.pyplot as plt

iris = sns.load_dataset("iris")

# 1. hue / size / style 同時編碼三個額外變數
sns.scatterplot(data=iris, x="sepal_length", y="petal_length",
                hue="species", style="species", size="petal_width", alpha=0.7)

# 2. facet：每個物種一個子圖
sns.relplot(data=iris, x="sepal_length", y="sepal_width", col="species", col_wrap=2, height=3)
```

| 參數 | 對應 | 建議 |
| --- | --- | --- |
| `hue` | 顏色 | 最容易辨識，放最重要的分組 |
| `style` | 點形 / 線型 | 與 `hue` 用同一欄可提高色盲可讀性 |
| `size` | 點大小 / 線粗 | 數值欄位；大小差異不易精確比較 |
| `alpha` | 透明度 | 點多時降低 |
| `col` / `row` / `col_wrap` | 子圖 | 只在 `relplot` |

## 折線圖與彙總

`lineplot` 同一個 x 有多個 y 時，會**自動彙總**：畫平均線 + 95% bootstrap CI 誤差帶。

```python
flights = sns.load_dataset("flights")       # 每年 12 個月 → 每個 year 有 12 個值

# 1. 每年平均 + 95% CI（預設）
sns.lineplot(data=flights, x="year", y="passengers")

# 2. 改成 ± SD；或 errorbar=None 不畫
sns.lineplot(data=flights, x="year", y="passengers", errorbar="sd")

# 3. 每個月一條線，不彙總
sns.lineplot(data=flights, x="year", y="passengers", hue="month", palette="viridis")

# 4. 每個個體一條線（重複測量、單細胞軌跡）：units= 指定個體、estimator=None 關閉彙總
fmri = sns.load_dataset("fmri")
sns.lineplot(data=fmri.query("region == 'frontal'"), x="timepoint", y="signal",
             units="subject", estimator=None, lw=0.8, color="gray")
```

| 參數 | 用途 |
| --- | --- |
| `estimator` | 彙總函式，預設 `"mean"`；`None` 不彙總 |
| `errorbar` | `("ci", 95)`（預設）、`"sd"`、`("pi", 50)`、`None`；舊參數 `ci=` 已棄用 |
| `err_style` | `"band"`（預設，誤差帶）或 `"bars"`（誤差線） |
| `units` | 每個個體畫一條線，需搭配 `estimator=None` |
| `markers=True`、`dashes=False` | 加點標記、全部實線 |
| `sort=False` | 不依 x 排序（x 是軌跡順序時） |

> x 沒有順序時（如 iris 的 `sepal_length` 對 `sepal_width`），`lineplot` 照樣會彙總並連線，但這條線沒有意義，應該用散布圖。

> 重複測量的資料（同一受試者多個時間點），預設 CI 把每個觀測當獨立樣本，會低估不確定性；先算每人的值再彙總，或用 [混合效應模型](../../../statistics/regression-analysis/mixed-effects-models.md)。
