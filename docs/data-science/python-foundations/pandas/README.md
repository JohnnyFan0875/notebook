# pandas

pandas 是資料科學最常用的表格資料工具，建立在 NumPy 之上，擅長處理欄位清理、篩選、彙總、轉換與時間序列欄位。這一章的重點是把資料操作拆成可預期的小步驟，避免寫出難以除錯的鏈式處理。

## Topics in This Folder

- Data creation: `creating-data.md`
- Indexing and filtering: `indexing-slicing.md`, `filtering.md`
- Updating and reshaping: `updating.md`, `reshape-merge.md`
- Grouped analysis: `groupby.md`, `statistics.md`
- Missing data and dtypes: `missing-data.md`, `dtypes-strings.md`, `categorical.md`
- Time-related work: `datetime.md`
- Structure management: `adding-removing.md`, `index-multiindex.md`
- Sampling and duplicates: `sampling-duplicates.md`
- Ordering and binning: `sorting.md`, `binning.md`

## 建議起手式

1. 先學 `creating-data`、`indexing-slicing`、`filtering`。
2. 接著學 `missing-data`、`dtypes-strings`、`categorical`。
3. 再往 `groupby`、`reshape-merge`、`statistics` 推進。

## 常見錯誤

- 把 view / copy 問題混在一起，導致更新結果不如預期。
- 沒先整理欄位型別就直接 groupby 或 merge。
- 看到缺失值就補，但沒有先確認缺失機制。
