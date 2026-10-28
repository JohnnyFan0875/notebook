# EDA Workflow

探索式資料分析的目標不是一次把所有圖都畫完，而是用最少的步驟，快速建立對資料的可信理解。好的 EDA workflow 會讓你在建模前先發現資料偏差、欄位定義問題與潛在風險。


## 第一步：Data Profiling

Data profiling 是 EDA 的第一層，重點在於快速辨識欄位品質與資料結構。它不像完整分析那麼深入，但非常適合當成每份新資料集的固定檢查清單。

### 檢查哪些面向

| 面向 | 你要問的問題 |
| --- | --- |
| 結構 | 有幾列幾欄？主鍵是什麼？一列代表什麼？ |
| 型別 | 數值、類別、日期、文字欄位是否判斷正確？ |
| 完整性 | 缺失值比例高嗎？是否集中在特定欄位或群體？ |
| 唯一性 | 主鍵是否重複？類別值是否有拼寫分裂？ |
| 合理性 | 值域、單位、日期順序是否合理？ |
| 一致性 | 同一欄位是否同時混入多種格式？ |

### pandas 實作範例

```python
import pandas as pd
import seaborn as sns

penguins = sns.load_dataset("penguins")

profile = pd.DataFrame({
    "dtype": penguins.dtypes,
    "missing_ratio": penguins.isna().mean(),
    "n_unique": penguins.nunique(dropna=False),
})

profile
```

接著可以對數值欄位補上摘要統計：

```python
penguins.describe().T
```

對類別欄位則優先看：

```python
for col in ["species", "island", "sex"]:
    print(col)
    print(penguins[col].value_counts(dropna=False))
    print()
```

### 常見風險訊號

- `object` 欄位其實是數值，只是混入空字串或特殊字元。
- 日期欄位沒有轉成 datetime，導致排序與篩選錯誤。
- ID 欄位被誤拿去建模，造成偽訊號。
- 重複列來自資料重複匯入，而不是自然重複觀測。
- 缺失值不是隨機發生，而是流程中某一站沒有填。

### 建議輸出

做完 profiling 後，最好留下簡短紀錄：

- 哪些欄位需要轉型
- 哪些欄位要進一步清理
- 哪些欄位暫時排除
- 哪些欄位可能成為 target、feature 或分層變數

Data profiling 的目的不是產生漂亮報表，而是降低後續分析踩雷機率。當你能在早期抓到型別、完整性與一致性問題，後面做統計與建模時會穩很多。

## 一個可重複使用的流程

1. 了解分析問題：先確認目標變數、資料來源、觀測單位與時間範圍。
2. 盤點資料結構：看列數、欄位數、資料型別、主鍵與索引。
3. 做資料品質檢查：缺失值、重複值、不合理範圍、格式不一致。
4. 看單變數分布：數值欄位看偏態、極端值；類別欄位看不平衡與稀有類別。
5. 看變數關係：數值對數值、類別對數值、時間對數值。
6. 建立初步假設：哪些變數可能重要？哪些欄位可能有 leakage？
7. 記錄後續動作：哪些欄位要修、刪、轉型、合併或保留註記。

## 初學者最常漏掉的地方

- 只看 `head()`，沒看 `tail()`、`sample()` 與整體分布。
- 只看平均值，沒有看中位數、四分位距與離群值。
- 忽略類別拼寫不一致，例如 `"NY"`、`"New York"`、`"new york"`。
- 看到缺失值就直接填補，沒有先釐清缺失機制與業務意義。
- 先做編碼與標準化，再切 train/test，導致資料洩漏。

## 一個簡單的起手式

```python
import pandas as pd
import seaborn as sns

tips = sns.load_dataset("tips")

tips.info()
tips.describe(include="all").T
tips.isna().mean().sort_values(ascending=False)
tips.duplicated().sum()
```

上面這幾步不能取代完整分析，但足以在 1 到 2 分鐘內抓到結構、缺失與欄位型態。

## 如何判讀 EDA 結果

- 如果資料量比想像中少，先確認是否過濾過頭或 join 掉了資料。
- 如果某些欄位幾乎全空，先確認它們是否真的對問題重要。
- 如果類別分布極不平衡，後續建模時要提早考慮抽樣策略與評估指標。
- 如果時間欄位有明顯制度變更點，後續切分資料時要避免隨機切分造成錯誤樂觀。

## 小結

EDA 的價值在於讓後面的每一步更穩。當你能清楚回答「資料從哪裡來、長什麼樣、哪裡不可靠、接下來要怎麼處理」，才適合往統計檢定或模型訓練前進。
