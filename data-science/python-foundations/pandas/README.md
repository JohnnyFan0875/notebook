# pandas Foundations

pandas 是資料科學最常用的表格資料工具，建立在 NumPy 之上，擅長處理欄位清理、篩選、彙總、轉換與時間序列欄位。這一章的重點是把資料操作拆成可預期的小步驟，避免寫出難以除錯的鏈式處理。

## 建議閱讀順序

| 順序 | 筆記 | 內容 |
| --- | --- | --- |
| 1 | [Creating Data](creating-data.md) | 由 dict / list 建立 Series、DataFrame；設定 index 與欄名（檔案讀取見 [Importing Data](../importing-data.md)） |
| 2 | [Selection](selection.md) | `loc` / `iloc`、boolean filtering、`query` |
| 3 | [Dtypes, Categorical and Strings](dtypes-categorical-strings.md) | `astype`、`category`、`.str` |
| 4 | [Missing Data](missing-data.md) | pandas / missingno 缺值 API |
| 5 | [Modifying](modifying.md) | 更新值、新增 / 刪除欄列 |
| 6 | [Ordering, Binning and Sampling](ordering-binning-sampling.md) | 排序、`cut` / `qcut`、抽樣、去重 |
| 7 | [Groupby](groupby.md)、[Statistics](statistics.md) | 分組彙總與描述統計 |
| 8 | [Reshape and Merge](reshape-merge.md)、[Index and MultiIndex](index-multiindex.md) | pivot / melt、merge / concat、階層索引 |
| 9 | [Performance](performance.md) | 向量化、`apply` vs 迴圈、row-wise 操作 |

時間欄位見 [Datetime](../datetime.md)；快速作圖見 [Pandas Plotting](../../data-manipulation-and-eda/visualization/pandas-plotting.md)。

## 這一章要解決什麼

- 我該如何穩定地清理欄位、篩選列、更新值，而不是寫出難以除錯的鏈式處理？
- 哪些分析前置工作應該先做：缺值、型別、分類欄位、索引，還是 merge？
- 當資料框開始變大、變慢或時間欄位變複雜時，應該先看哪一組工具？

## 常見錯誤

- 把 view / copy 問題混在一起，導致更新結果不如預期。
- 沒先整理欄位型別就直接 groupby 或 merge。
- 看到缺失值就補，但沒有先確認缺失機制。
