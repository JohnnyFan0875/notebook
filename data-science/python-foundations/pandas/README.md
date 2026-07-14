# pandas Foundations

pandas 是資料科學最常用的表格資料工具，建立在 NumPy 之上，擅長處理欄位清理、篩選、彙總、轉換與時間序列欄位。這一章的重點是把資料操作拆成可預期的小步驟，避免寫出難以除錯的鏈式處理。

## 建議閱讀順序

1. [Creating Data](creating-data.md)、[Indexing and Slicing](indexing-slicing.md)、[Filtering](filtering.md): 先把最基本的資料框操作練順。
2. [Missing Data](missing-data.md)、[Dtypes and Strings](dtypes-strings.md)、[Categorical](categorical.md): 先處理欄位語意與型別，再做彙總。
3. [Updating](updating.md)、[Adding and Removing](adding-removing.md)、[Row Operations](row-operations.md): 學會穩定修改資料框，而不是邊試邊改。
4. [Sorting](sorting.md)、[Binning](binning.md)、[Sampling and Duplicates](sampling-duplicates.md): 這一層處理排序、抽樣、去重與分箱這些常見前置整理。
5. [Groupby](groupby.md)、[Statistics](statistics.md)、[Reshape and Merge](reshape-merge.md)、[Index and MultiIndex](index-multiindex.md): 這一層才是真正的分析工作底盤。
6. [Datetime](datetime.md)、[Time-series Visualization](time-series-visualization.md)、[Visualization](visualization.md) 與 [Performance](performance.md): 當資料開始變大、有時間結構，或要快速檢查圖形時再補上。

## 主題分組

- Data creation: `creating-data.md`
- Indexing and filtering: `indexing-slicing.md`, `filtering.md`
- Updating and reshaping: `updating.md`, `row-operations.md`, `reshape-merge.md`
- Performance patterns: `performance.md`
- Grouped analysis: `groupby.md`, `statistics.md`
- Missing data and dtypes: `missing-data.md`, `dtypes-strings.md`, `categorical.md`
- Time-related work: `datetime.md`, `time-series-visualization.md`
- Structure management: `adding-removing.md`, `index-multiindex.md`
- Sampling and duplicates: `sampling-duplicates.md`
- Ordering and binning: `sorting.md`, `binning.md`
- Quick charts: `visualization.md`

## 這一章要解決什麼

- 我該如何穩定地清理欄位、篩選列、更新值，而不是寫出難以除錯的鏈式處理？
- 哪些分析前置工作應該先做：缺值、型別、分類欄位、索引，還是 merge？
- 當資料框開始變大、變慢或時間欄位變複雜時，應該先看哪一組工具？

## 常見錯誤

- 把 view / copy 問題混在一起，導致更新結果不如預期。
- 沒先整理欄位型別就直接 groupby 或 merge。
- 看到缺失值就補，但沒有先確認缺失機制。
