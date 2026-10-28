[Python Foundations](../README.md) › [NumPy](README.md) › 隨機與統計

# 隨機抽樣與統計 (Random Sampling & Statistics)

模擬、bootstrap、隨機切分資料都靠亂數；可重現性取決於 seed 怎麼管理。統計部分是 array 層級的摘要；DataFrame 的分組統計見 [pandas 統計](../pandas/statistics.md)，機率分配與檢定見 [scipy.stats 速查](../scipy-stats.md)。

## 用 `default_rng` 抽樣

新程式一律用 `Generator`（`np.random.default_rng(seed)`）；`np.random.seed()` + `np.random.xxx()` 是共用全域狀態的舊 API。

```python
import numpy as np

rng = np.random.default_rng(42)          # 每次執行結果相同

rng.normal(0, 1, 5)                      # [ 0.305 -1.04   0.75   0.941 -1.951]
rng.normal(loc=10, scale=2, size=(2, 3)) # 2×3，mean=10、sd=2
rng.random((2, 2))                       # Uniform[0, 1)
rng.integers(0, 10, size=5)              # [4 2 0 5 8]：0 ≤ x < 10
rng.choice(10, 5, replace=False)         # 不重複抽 5 個
rng.choice(["windy", "cloudy", "sunny", "rainy"], size=7, p=[0.2, 0.5, 0.2, 0.1])  # 指定機率
rng.permutation(10)                      # 回傳打亂後的新 array
rng.shuffle(x)                           # 就地 (in place) 打亂第 0 軸，回傳 None
rng.binomial(n=10, p=0.3, size=5)        # 其他分配：poisson、negative_binomial、gamma…

# 重設 seed → 同樣的序列
np.random.default_rng(1).random(2)       # [0.512 0.950]
np.random.default_rng(1).random(2)       # [0.512 0.950]

# 簡單模擬：random walk
steps = np.random.default_rng(123).choice([-1, 1], size=100)
walk = steps.cumsum()                    # 每步 ±1，累加成路徑
```

| 舊 API（`np.random.`） | 新 API（`rng.`） | 差異 |
| --- | --- | --- |
| `seed(42)` | `default_rng(42)` | 不再有全域狀態 |
| `rand(3, 2)` | `random((3, 2))` | shape 用 tuple |
| `randn(n)` | `standard_normal(n)` | |
| `randint(0, 10, n)` | `integers(0, 10, n)` | 可加 `endpoint=True` 包含上限 |
| `normal` / `choice` / `binomial` | 同名 | |
| `shuffle(x)` | `shuffle(x)` / `permutation(x)` | |

> 把 `rng` 當參數傳進函式，而不是在函式裡各自 `default_rng()`：結果可重現，平行運算時也不會讓每個 worker 拿到相同序列（用 `rng.spawn(n)` 產生獨立子 generator，見 [平行運算](../performance-and-scaling/parallel.md#常見陷阱)）。sklearn 的 `random_state`、pandas 的 `.sample(random_state=)` 也都接受 `Generator`。

## 描述統計

```python
arr = np.array([1, 2, 3, 4, 5, 100])

np.mean(arr), np.median(arr)             # 19.17, 3.5：一個極端值就把平均拉走
arr.sum(), arr.min(), arr.max()          # 115, 1, 100
arr.argmin(), arr.argmax()               # 0, 5：極值的位置
arr.std(), arr.std(ddof=1)               # 36.17（母體）, 39.62（樣本）
arr.var(ddof=1)

np.quantile(arr, [0, 0.25, 0.5, 0.75, 1])   # [  1.    2.25  3.5   4.75 100.  ]
np.percentile(arr, 90)                      # 52.5（預設線性內插）

# 2D：指定 axis
X = np.array([[1, 2], [3, 4], [5, 6]])
X.mean(axis=0)                           # [3. 4.]：每欄
X.mean(axis=1)                           # [1.5 3.5 5.5]：每列

# 有缺值：nan 版本
y = np.array([1.0, np.nan, 3.0])
np.mean(y), np.nanmean(y)                # nan, 2.0
np.nanmedian(y), np.nanstd(y), np.isnan(y).sum()
```

| 注意 | 說明 |
| --- | --- |
| `ddof` | NumPy `std` / `var` 預設 `ddof=0`（除以 n）；pandas、R 預設 `ddof=1`（除以 n−1）。小樣本差很多 |
| NaN | 一般函式遇到 NaN 回傳 NaN；用 `np.nanmean` 等，或先處理缺值 |
| 分位數 | 預設 `method="linear"`，與 R 預設 type 7 相同；不同軟體結果略有差異是正常的 |

## 離散程度與離群值

```python
from scipy import stats

q1, q3 = np.percentile(arr, [25, 75])
q3 - q1                                  # 2.5：IQR
stats.iqr(arr)                           # 2.5
lower, upper = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
arr[(arr < lower) | (arr > upper)]       # [100]：Tukey fences

np.mean(np.abs(arr - arr.mean()))        # 26.94：平均絕對離差（受極端值影響）
stats.median_abs_deviation(arr)          # 1.5：中位數絕對離差 (MAD)，穩健

z = (arr - arr.mean()) / arr.std()
z.round(2)                               # [-0.5  -0.47 -0.45 -0.42 -0.39  2.23]
arr[np.abs(z) > 2]                       # [100]

robust_z = (arr - np.median(arr)) / (1.4826 * stats.median_abs_deviation(arr))
robust_z.round(1)                        # [ -1.1  -0.7  -0.2   0.2   0.7  43.4]
```

| 指標 | 對極端值 | 用途 |
| --- | --- | --- |
| 標準差 / z-score | 敏感：極端值會撐大 SD，反而讓自己的 z 變小（masking） | 近似常態的資料 |
| IQR / Tukey fences | 穩健 | 盒鬚圖、偏態資料 |
| 中位數絕對離差 (MAD) / robust z | 最穩健 | 小樣本、多個離群值 |

> 上例 100 的 z 只有 2.23：n 個點時，用母體 SD 算的 |z| 最大只能到 √(n−1)（n=6 時 2.24；用樣本 SD 則是 (n−1)/√n = 2.04）。小樣本用「|z| > 3」根本不可能抓到任何點，改用 robust z（43.4）或 IQR。離群值處理策略見 [Outlier Handling](../../machine-learning/preprocessing/outlier-handling.md)。

## 捨入與轉換

```python
num = np.array([-1.67, -1.01, 0.97, 1.63])
np.round(num, 1)                         # [-1.7 -1.   1.   1.6]
np.floor(num), np.ceil(num), np.trunc(num)   # 往下 / 往上 / 往 0
np.round(2.5), np.round(3.5)             # 2.0, 4.0：銀行家捨入（四捨六入五成雙），同 Python round()

np.log(arr), np.log2(arr), np.log10(arr)
np.log1p(np.array([0, 9, 99]))           # [0.    2.303 4.605]：log(1 + x)，計數資料有 0 時用
np.sqrt(arr)

from scipy.stats import boxcox
transformed, lam = boxcox(arr)           # λ ≈ -0.45；要求全部 > 0
```

| 轉換 | 適用 | 注意 |
| --- | --- | --- |
| `log` / `log2` | 右偏、倍數變化（表達量、濃度） | 不能有 0 或負值 |
| `log1p` / `log2(x + 1)` | 計數資料（含 0） | pseudocount 的大小會影響低表達結果 |
| `sqrt` | 計數資料，較溫和 | |
| Box-Cox | 自動找 λ 讓分布接近常態 | 只接受正值；含 0 / 負值用 Yeo-Johnson（`scipy.stats.yeojohnson`） |

轉換的統計意義見 [單變數數值描述](../../statistics/descriptive-statistics/univariate-numerical.md)；建模前的縮放見 [Feature Scaling](../../machine-learning/preprocessing/feature-scaling.md)。
