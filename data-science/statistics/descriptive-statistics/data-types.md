[Statistics](../README.md) › [敘述統計](README.md) › 資料型態

# 資料型態與量尺 (Data Types & Measurement Scales)

資料型態決定能用哪些統計量、哪種圖、以及之後能做哪種檢定。型態判錯，後面整條分析都會被污染。

## 四種量尺 (NOIR)

| 量尺 | 大類 | 特性 | 集中趨勢 | 離散 | 圖 | 例子 |
| --- | --- | --- | --- | --- | --- | --- |
| **名目 (Nominal)** | 類別 (qualitative) | 無順序 | 眾數 | — | 長條圖 | 血型、物種、基因型 |
| **順序 (Ordinal)** | 類別 | 有順序，但間距不等 | 中位數、眾數 | IQR | 有序長條圖 | Likert 1–5、腫瘤分期 |
| **區間 (Interval)** | 數值 (quantitative) | 間距相等，**沒有真零點** | 平均數 | SD | 直方圖、Boxplot | 攝氏溫度、年份 |
| **比率 (Ratio)** | 數值 | 間距相等，**有真零點** | 平均數 / 中位數 | SD、IQR | 直方圖、Boxplot | 身高、濃度、read count |

- **真零點 (true zero)**：0 代表「完全沒有」。收入 0 = 沒收入（Ratio）；0°C 不代表沒有溫度（Interval）。所以可以說「收入是兩倍」，但不能說「20°C 是 10°C 的兩倍熱」。
- 量尺高低：Nominal < Ordinal < Interval < Ratio。**可以往下降級**（把 Ratio 當 Ordinal 用），**不能往上升級**。

數值型再細分：

| 類型 | 說明 | 例子 |
| --- | --- | --- |
| 連續 (continuous) | 範圍內任何值 | 身高、表現量 (expression level) |
| 離散 (discrete) | 只能是可數的整數 | 子女數、read count、突變數 |

結構化 (structured，表格) vs 非結構化 (unstructured，文字、影像、序列) 也會影響分析：非結構化資料通常要先萃取 / 標註，才能套用標準統計流程。

## 在 pandas 中檢查型態

```python
import seaborn as sns

df = sns.load_dataset("iris")

df.dtypes                       # 各欄型態：sepal_length float64 ... species object
df.describe()                   # 數值欄摘要：count / mean / std / min / quartiles / max
df.describe(include="object")   # 類別欄摘要：count / unique / top / freq
```

| pandas dtype | 可能的量尺 | 要注意 |
| --- | --- | --- |
| `int64`、`float64` | Interval / Ratio | 可能其實是編碼過的類別（1=男、2=女） |
| `object` | Nominal / Ordinal | 有沒有順序？ |
| `category` | Nominal / Ordinal | 順序型要設 `ordered=True` |
| `bool` | Nominal（二元） | 當類別處理 |
| `datetime64` | 特殊 | 用 [時間序列](../time-series-analysis/README.md) 方法 |

> **警告**
>
> - Likert 量表、腫瘤分期常被存成 `int64`，但本質是 **Ordinal**，不是數值。務必看資料字典 (data dictionary)。
> - **ID 與 metadata**（sample ID、檔案路徑、時間戳記）看起來像變數，但不該被當成量測值去算平均。

## 型態錯誤的常見後果

| 錯誤 | 後果 |
| --- | --- |
| 把類別 ID 拿去算平均 | 數字毫無意義 |
| 把 Ordinal 當成等距數值 | 平均數隱含「每級間距相等」的假設 |
| 日期存成字串 | 失去時間順序與間隔 |
| 類別變數直接丟進模型當數值 | 模型誤以為 3 > 2 > 1，見 [Categorical Encoding](../../machine-learning/preprocessing/categorical-encoding.md) |
