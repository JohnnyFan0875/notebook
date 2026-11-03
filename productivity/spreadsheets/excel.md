# Excel

Excel 是以 grid 為核心的 spreadsheet 工具，適合用來輸入、整理、分析與視覺化表格資料。  
它的強項不只是「能做表」，而是能讓非工程背景使用者也能快速處理 tabular data、建立公式、做彙總與套用規則。

## Core Ideas

- `Workbook`: 一個 Excel 檔案，可以包含一個或多個 worksheet。
- `Worksheet`: 由 rows 和 columns 組成的工作表。
- `Cell`: row 與 column 的交叉位置。
- `Cell reference`: 例如 `B3`，用欄字母加列號定位一個 cell。
- `Range`: 一組 cell，例如 `A1:C10`。
- `Formula`: 以 `=` 開頭的計算式，可結合常數、cell reference 與 functions。
- `Formula bar`: 用來檢視或編輯目前 cell 內容。

## Why Excel Still Matters

- 適合快速整理中小型資料表與 ad hoc 分析。
- 對技術與非技術使用者都相對友善。
- 很適合做手動 review、資料錄入、初步檢查與簡易報表。
- 支援 sorting、filtering、formatting、validation 與 table-based summaries。
- 支援 shared workbooks、co-authoring、commenting 與 templates，方便協作與快速起步。

## Excel Online vs Desktop

可以先用很實務的方式區分：

- `Excel Online`: cloud-based、功能較精簡，適合基本任務與協作
- `Desktop Excel`: 本機版本、功能較完整，較適合進階操作與較複雜 workbook

這不是單純授權差異，而是工作方式的差異：

- 想快速共享與共同編修時，online 版本很方便
- 想使用更多進階能力時，desktop 版本通常更完整

## Structural Limits to Remember

- 單一 worksheet 上限大致是 `1,048,576` rows 與 `16,384` columns。
- 能否順暢開啟大型 workbook 仍受記憶體與系統資源影響。
- 當資料規模、版本控管需求或重複性流程變大時，通常應該往 database、Python、Power Query 或 BI 流程移動。

## Working Model

### Tables

Excel table 比一般 range 更適合當分析資料表，因為它通常提供：

- 明確的 header row
- 可延伸的 body rows
- 可開啟 totals row
- 結構化 references，可直接用欄名寫公式
- 對 sorting、filtering、formatting 與 validation 更友善

實務上，如果資料會持續增減列數，優先把資料區轉成 table，通常比裸 range 更穩定。

### Range Notation

`Range` 是一組 cells，例如 `A1:C10`。

公式裡常見的冒號 `:`，表示從起點 cell 到終點 cell 的連續範圍，例如：

- `B2:B11`: 第 `B` 欄從第 `2` 列到第 `11` 列
- `B:B`: 整個 `B` 欄

這是很多 aggregate function 的最基本語法。

### Sorting and Filtering

- `Filtering`: 暫時只顯示符合條件的資料列。
- `Sorting`: 依欄位值重新排列資料。
- 可依數值、文字、日期排序，也可依 `cell color`、`font color` 等格式排序。

先把資料整理成一致型別，再排序或篩選，會比混雜格式的欄位可靠很多。

## Data Management Features

### Named Ranges

Named range 是替一段 cells 命名，讓公式更容易讀，也比較不容易在大型 sheet 裡迷路。

適合情境：

- 重複引用同一段資料
- 想讓公式比 `A2:A500` 更有語意
- 需要集中管理公式依賴範圍

### Subtotals

Subtotal 適合在已排序資料上，依群組自動插入彙總結果，常見聚合包含：

- `SUM`
- `COUNT`
- `AVERAGE`

如果你的需求是正式分析報表，pivot table 通常更彈性；如果只是快速分組小計，subtotal 很方便。

### Data Validation

Data validation 用來限制輸入內容，避免資料在收集階段就失真。

常見用途：

- 限制輸入為日期、整數、特定範圍
- 建立 dropdown choices
- 阻止空值或非法值

這是 spreadsheet workflow 中最被低估、但最能提升資料品質的功能之一。

### Conditional Formatting

Conditional formatting 會根據規則自動改變儲存格外觀，適合：

- 標記異常值
- 顯示高低分布
- 快速掃描 deadline、重複值或 KPI 狀態

它很適合做視覺提示，但不應取代真正的資料清理或邏輯欄位。

## Common Function Patterns

### Text Functions

#### TEXTJOIN

Joins multiple values from a range or array into a single text string.

```excel
=TEXTJOIN(delimiter, ignore_empty, text1, [text2], ...)
```

- `ignore_empty`: Set to TRUE/FALSE to ignore/include empty cells.
- Example: `=TEXTJOIN(",", TRUE, A1:A100)`

#### LEFT

Returns the first characters from a string.

```excel
=LEFT(text, [num_chars])
```

- Example: `=LEFT("DataCamp", 4)` returns `Data`

#### RIGHT

Returns the last characters from a string.

```excel
=RIGHT(text, [num_chars])
```

- Example: `=RIGHT("DataCamp", 4)` returns `Camp`

### Lookup Functions

#### VLOOKUP

Searches for a value in the first column of a range and returns a value from another column in the same row.

```excel
=VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])
```

- `lookup_value`: The value to search for in the first column of `table_array`.
- `table_array`: The range of cells that contains the data.
- `col_index_num`: The column number to return, starting from `1`.
- `range_lookup`: Use `FALSE` for exact match, `TRUE` or omitted for approximate match.
- Example:

```excel
=VLOOKUP("test", A1:D10, 2, FALSE)
=VLOOKUP(A11, A1:D10, 2, FALSE)
```

### Aggregate Functions

這類函數把一組值濃縮成單一結果，最常見的是：

- `SUM()`: 加總
- `AVERAGE()`: 平均值
- `COUNT()`: 計數
- `MIN()`: 最小值
- `MAX()`: 最大值

`AVERAGE` 常見寫法：

```excel
=AVERAGE(B2:B11)
=AVERAGE(B:B)
=AVERAGE(Students[Test Score])
```

### Utility Formula

#### Count `delimiter`-Separated Elements in a Cell

Calculates how many values are separated by delimiter (comma for example) in a single cell.

```excel
=IF(A1<>"", LEN(A1) - LEN(SUBSTITUTE(A1, ",", "")) + 1, "empty")
```

- If `A1` is empty, return `empty`
- `LEN(A1)`: number of characters in `A1`
- `LEN(SUBSTITUTE(A1, ",", ""))`: number of characters excluding commas
- Difference in lengths plus `1` gives the number of delimited elements

## Practical Heuristics

- 先把 raw range 轉成 table，再開始寫公式。
- 能用 validation 擋掉錯誤輸入，就不要等到後面再人工清理。
- 當公式開始互相引用很多 sheet、很難追蹤時，通常代表流程該重構。
- Spreadsheet 適合操作與檢查；重複性高或資料量大的邏輯，盡量搬去 script 或 database。
- 如果同一份資料需要反覆清理、整併與重跑，通常該往 Power Query 移，而不是繼續堆手動步驟。

## Related Note

如果已經熟悉基礎公式，下一步可以看 [Advanced Excel Functions](advanced-excel-functions.md)，裡面整理了：

- `XLOOKUP`
- `INDEX` + `MATCH`
- `OFFSET`
- `DSUM` / `DCOUNT` / `DAVERAGE`

如果重點是把 raw workbook 整理成可分析資料，可以再看 [Excel Data Preparation Workflow](excel-data-preparation-workflow.md)。

如果重點是把輸入規則、dropdown、範圍限制與 business logic 擋在資料進表之前，可以再看 [Excel Data Validation](excel-data-validation.md)。

如果重點是把重複性高的資料匯入、清理與整併流程從 worksheet 抽離，可以再看 [Power Query in Excel](power-query-in-excel.md)。

如果重點是處理多表關聯、DAX、measures 與模型層分析，可以再看 [Power Pivot in Excel](power-pivot-in-excel.md)。
