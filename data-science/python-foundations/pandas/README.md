[Data Science](../../README.md) › [Python Foundations](../README.md) › pandas

# pandas

pandas 是 Python 處理表格資料的主力：建立在 NumPy 之上，多了欄名、index 對齊、缺值、分組與合併。本章以 pandas 3.x 為準（Copy-on-Write 與 `str` dtype 已是預設）。

```text
建立 / 讀入 → 選取 → 型別 → 缺值 → 修改 → 排序 / 分箱 / 去重 → 分組與統計 → reshape / merge → 效能與儲存
```

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [建立資料](creating-data.md) | Series / DataFrame 的建構方式、index 與欄名 | 手上的 dict / list / array 怎麼變成表格？ |
| [選取與篩選](selection.md) | `[]`、`loc` / `iloc`、布林遮罩、`query`、`isin` | 怎麼取出要的列與欄？ |
| [dtype、類別與字串](dtypes-categorical-strings.md) | `astype`、nullable dtype、`category`、`.str`、編碼 | 欄位型別對嗎？類別與文字怎麼處理？ |
| [缺值](missing-data.md) | 缺值標記、偵測、`missingno`、`fillna` / `dropna` / `interpolate` | 缺值在哪裡？怎麼刪、怎麼補？ |
| [修改資料](modifying.md) | view vs copy、Copy-on-Write、更新 / 新增 / 刪除欄列、`map` / `apply` | 為什麼改了沒反應（或改到原表）？ |
| [排序、分箱、抽樣與去重](ordering-binning-sampling.md) | `sort_values`、`cut` / `qcut`、`sample`、`drop_duplicates` | 怎麼排序、分組成區間、抽樣、去重？ |
| [分組彙總](groupby.md) | `groupby` + `agg` / `transform` / `filter` | 每組的統計量怎麼算、怎麼貼回原表？ |
| [描述統計](statistics.md) | `describe`、`value_counts`、相關、rolling | 資料的整體樣貌與欄位關係？ |
| [Reshape 與 Merge](reshape-merge.md) | `pivot` / `melt`、`concat`、`merge` / `join`、`merge_asof`、`explode` | 寬長表怎麼轉？多張表怎麼安全地合併？ |
| [Index 與 MultiIndex](index-multiindex.md) | `set_index`、階層索引、`stack` / `unstack` | 多層索引怎麼選取與重排？ |
| [效能](performance.md) | 向量化、`apply` vs 迴圈、group-wise 運算 | 為什麼這麼慢？怎麼改寫？ |
| [記憶體與儲存格式](memory-and-storage.md) | `memory_usage`、dtype 縮減、pyarrow、Parquet、HDF5 | 資料塞不進記憶體、讀寫太慢怎麼辦？ |

| 相關 | 連結 |
| --- | --- |
| 讀檔（CSV、Excel、JSON、資料庫） | [匯入資料](../importing-data.md) |
| 日期欄位、時區、resample | [日期與時間](../datetime.md) |
| 快速作圖 | [pandas Plotting](../../data-manipulation-and-eda/visualization/pandas-plotting.md) |
| 比 pandas 快、資料數 GB | [Polars](../performance-and-scaling/polars.md) |
| R 對應 | [dplyr / tidyr](../../r-foundations/README.md) |
| SQL 對應 | [SQL 查詢基礎](../../databases/sql-query-foundations.md) |
