[Python Foundations](../README.md) › [pandas](README.md) › 描述統計

# 描述統計 (Descriptive Statistics)

拿到新資料後的第一輪檢視：大小、型別、缺值、分布、類別頻率、欄位間相關。這篇是 pandas 的寫法；各統計量的意義與選擇見 [描述統計](../../statistics/descriptive-statistics/README.md)，整體 EDA 流程見 [EDA Workflow](../../data-manipulation-and-eda/eda-workflow.md)。array 層級的統計見 [NumPy 隨機與統計](../numpy/random-and-statistics.md)。

## 第一眼

```python
import pandas as pd
import seaborn as sns

iris = sns.load_dataset("iris")

iris.shape                    # (150, 5)
iris.info()                   # dtype、非缺值數、記憶體
iris.head(), iris.tail(), iris.sample(5, random_state=0)
iris.dtypes, iris.columns, iris.index
iris.nunique()                # 每欄唯一值數：找 ID 欄（= 列數）與常數欄（= 1）
iris.isna().sum()             # 每欄缺值數
iris.duplicated().sum()       # 完全重複的列：1
```

## 摘要統計

```python
iris.describe()                                  # 數值欄：count、mean、std、min、四分位數、max
iris.describe(include="all")                     # 加上類別欄：count、unique、top（眾數）、freq
iris.describe(percentiles=[0.05, 0.5, 0.95])     # 自訂百分位（偏態資料看尾端）

iris.mean(numeric_only=True)                     # 有字串欄時要 numeric_only=True，否則 TypeError
iris.median(numeric_only=True)
iris.std(numeric_only=True)                      # ddof=1（樣本標準差），與 NumPy 預設不同
iris.quantile([0.25, 0.5, 0.75], numeric_only=True)
iris.sem(numeric_only=True)                      # 標準誤
iris.skew(numeric_only=True)                     # 偏態：[0.31, 0.32, -0.27, -0.10]
iris.agg(["mean", "median", "std"], numeric_only=True)

iris["sepal_length"].nlargest(2)                 # 7.9, 7.7
iris["sepal_length"].idxmax()                    # 最大值所在的 index
```

## 類別頻率

```python
iris["species"].value_counts()                   # 次數，預設由多到少
iris["species"].value_counts(normalize=True)     # 比例
iris["species"].value_counts(dropna=False)       # 把缺值也算進來
iris.assign(wide=iris["sepal_width"] > 3)[["species", "wide"]].value_counts()   # 組合的次數

# 列聯表 (contingency table)
pd.crosstab(iris["species"], iris["sepal_width"] > 3.0)
# sepal_width  False  True
# setosa           8     42
# versicolor      42      8
# virginica       33     17
pd.crosstab(iris["species"], iris["sepal_width"] > 3.0, normalize="index")   # 列百分比
pd.crosstab(iris["species"], iris["sepal_width"] > 3.0, margins=True)        # 加總列 / 欄
pd.crosstab(iris["species"], iris["sepal_width"] > 3.0,
            values=iris["sepal_length"], aggfunc="median")                   # 格內放統計量
```

列聯表的檢定（卡方、Fisher）見 [scipy.stats 速查](../scipy-stats.md#檢定對照)。

## 相關與共變異數

```python
num = iris.select_dtypes("number")

num.corr()                          # Pearson（預設）
num.corr(method="spearman")         # 秩相關：非線性但單調、有離群值時
num.cov()
iris["sepal_length"].corr(iris["petal_length"])   # 0.872：兩欄之間
num.corrwith(iris["petal_length"])                # 每欄與某欄的相關

sns.heatmap(num.corr(), annot=True, cmap="coolwarm", vmin=-1, vmax=1)
```

> 全體與組內的相關可能相反：iris 的 sepal length 與 sepal width 整體相關 −0.12，但在 setosa 組內是 +0.74（`iris.groupby("species").corr()`）。組別是干擾因子時，先分組再看，見 [Simpson's Paradox](../../statistics/experimental-design/confounding-bias.md#simpsons-paradox)。

相關係數的選擇與解讀見 [雙變數描述](../../statistics/descriptive-statistics/bivariate.md)。高維資料（上千個基因）不要畫完整的相關熱圖，改看分群熱圖或 [PCA](../../statistics/multivariate-analysis/pca.md)。

## 有順序的資料：差分、累計、滑動視窗

這些運算依**列的順序**計算，先 `sort_values`（例如依日期）；有分組時加 `groupby`，避免跨組相減。

```python
ts = df.sort_values("date").set_index("date")["value"]

ts.diff()                           # 與前一筆的差
ts.pct_change()                     # 變化率
ts.shift(1)                         # 前一筆的值（lag）
ts.cumsum(), ts.cummax()            # 累計

ts.rolling(window=7).mean()                    # 7 筆滑動平均；前 6 筆是 NaN
ts.rolling(window=7, min_periods=3).mean()     # 至少 3 筆就算
ts.rolling("7D").mean()                        # 依時間視窗（index 需為日期）
ts.rolling(7, center=True).median()            # 置中、穩健
ts.expanding().mean()                          # 從頭累計的平均
ts.ewm(span=7).mean()                          # 指數加權

df["change"] = df.groupby("patient")["value"].diff()   # 每位病人內的變化
```

時間序列的自相關、分解等分析見 [時間序列分析](../../statistics/time-series-analysis/README.md)；resample 見 [日期與時間](../datetime.md#以時間為索引篩選與-resample)。
