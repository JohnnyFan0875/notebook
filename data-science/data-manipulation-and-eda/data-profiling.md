# Data Profiling

Data profiling 是 EDA 的第一層，重點在於快速辨識欄位品質與資料結構。它不像完整分析那麼深入，但非常適合當成每份新資料集的固定檢查清單。

## 檢查哪些面向

| 面向 | 你要問的問題 |
| --- | --- |
| 結構 | 有幾列幾欄？主鍵是什麼？一列代表什麼？ |
| 型別 | 數值、類別、日期、文字欄位是否判斷正確？ |
| 完整性 | 缺失值比例高嗎？是否集中在特定欄位或群體？ |
| 唯一性 | 主鍵是否重複？類別值是否有拼寫分裂？ |
| 合理性 | 值域、單位、日期順序是否合理？ |
| 一致性 | 同一欄位是否同時混入多種格式？ |

## pandas 實作範例

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

## 常見風險訊號

- `object` 欄位其實是數值，只是混入空字串或特殊字元。
- 日期欄位沒有轉成 datetime，導致排序與篩選錯誤。
- ID 欄位被誤拿去建模，造成偽訊號。
- 重複列來自資料重複匯入，而不是自然重複觀測。
- 缺失值不是隨機發生，而是流程中某一站沒有填。

## 建議輸出

做完 profiling 後，最好留下簡短紀錄：

- 哪些欄位需要轉型
- 哪些欄位要進一步清理
- 哪些欄位暫時排除
- 哪些欄位可能成為 target、feature 或分層變數

## 小結

Data profiling 的目的不是產生漂亮報表，而是降低後續分析踩雷機率。當你能在早期抓到型別、完整性與一致性問題，後面做統計與建模時會穩很多。
