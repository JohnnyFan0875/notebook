[Productivity](../README.md) › [試算表](README.md) › 進階函數

# Excel 函數 (Excel Functions)

依用途整理常用函數：查找、條件聚合、邏輯、文字、日期、動態參照、資料庫函數。其他筆記提到函數時都連到這裡。

## 選哪個函數

| 想做的事 | 首選 | 替代 / 舊版 |
| --- | --- | --- |
| 依 key 帶回另一欄的值 | `XLOOKUP` | `INDEX` + `MATCH`、`VLOOKUP` |
| 交叉表 (2D) 查值 | `INDEX` + 兩個 `MATCH` | `XLOOKUP` 巢狀 |
| 多個 AND 條件的加總 / 計數 / 平均 | `SUMIFS` / `COUNTIFS` / `AVERAGEIFS` | — |
| 條件像一張規則表（含 OR） | `DSUM` / `DCOUNT` / `DAVERAGE` | 多個 `COUNTIFS` 相加 |
| 多層分類 | `IFS`、`SWITCH` | 巢狀 `IF`；規則多時改用查找表 |
| 依使用者選擇移動範圍 | `OFFSET` + `MATCH` | `INDEX` 回傳範圍（非易變） |
| 篩出符合條件的多列 | `FILTER`、`UNIQUE`、`SORT`（動態陣列，Microsoft 365） | 進階篩選 |

## 查找 (Lookup)

`VLOOKUP` 假設查找欄在最左、只能往右取值、用欄號定位，插入欄位就會取錯值。新版 Excel 優先用 `XLOOKUP`。

| 函數 | 語法 | 重點 |
| --- | --- | --- |
| `XLOOKUP` | `XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])` | 查找欄與回傳欄分開指定，可往左查；內建找不到時的預設值；預設精確比對 |
| `VLOOKUP` | `VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])` | 第 4 參數省略 = **近似比對**，幾乎都要寫 `FALSE` |
| `HLOOKUP` | `HLOOKUP(lookup_value, table_array, row_index_num, [range_lookup])` | 橫向版的 `VLOOKUP` |
| `MATCH` | `MATCH(lookup_value, lookup_array, 0)` | 回傳**位置**；`0` = 精確比對 |
| `INDEX` | `INDEX(array, row_num, [column_num])` | 依位置取值 |

```excel
=XLOOKUP(A2, Products[ID], Products[Name], "not found")
=VLOOKUP(A2, $A$1:$D$10, 2, FALSE)
=INDEX(return_array, MATCH(lookup_value, lookup_array, 0))
=INDEX(matrix, MATCH(row_key, row_labels, 0), MATCH(col_key, col_labels, 0))
```

> 找不到值回傳 `#N/A` 時，先檢查型別（數字 vs 文字的 `"123"`）與前後空白（`TRIM`），而不是急著包 `IFERROR`；`IFERROR` 會把真正的錯誤也一起藏起來。

## 條件聚合

| 公式 | 意義 |
| --- | --- |
| `=COUNTIFS(B:B, "Yes", E:E, "Florida")` | B 欄為 Yes **且** E 欄為 Florida 的列數 |
| `=SUMIFS(Sales[Amount], Sales[Region], "North", Sales[Date], ">="&DATE(2024,1,1))` | North 區 2024 年起的金額加總；比較運算子要用字串串接 |
| `=AVERAGEIFS(Scores[Score], Scores[Class], G2)` | 條件取自儲存格 |

`*IFS` 的條件之間是 AND；要 OR 就得把多個 `COUNTIFS` 相加，條件一多就該考慮下面的資料庫函數或 Power Query。

### 資料庫函數 (Database Functions)

`DSUM`、`DCOUNT`、`DAVERAGE`、`DMIN`、`DMAX` 共用 `=DFUNCTION(database, field, criteria)`：

| 參數 | 意義 |
| --- | --- |
| `database` | 含標題列的資料範圍 |
| `field` | 要彙總的欄（欄名、欄序號或標題儲存格） |
| `criteria` | 另一塊條件表：標題與資料表欄名相同；**同一列 = AND，不同列 = OR**；可用 `>`、`<>` 與萬用字元 `*`、`?` |

例：`=DSUM(A1:F6, "Sales", H1:J2)` 的條件表是標題列 + 一列條件（一組 AND）；範圍改成 `H1:J3` 就多一組 OR 條件。

| 情境 | 選擇 |
| --- | --- |
| 條件簡單的日常報表 | `SUMIFS` 系列 |
| 條件像一張可讓人維護的規則表 | 資料庫函數 |
| 邏輯複雜、資料量大 | Power Query、SQL、Python |

## 邏輯與分類

| 函數 | 語法 | 用途 |
| --- | --- | --- |
| `IF` | `IF(test, value_if_true, value_if_false)` | 二元判斷、建立旗標 (flag) |
| `AND` / `OR` / `NOT` | `AND(cond1, cond2, ...)` | 組合條件，常放在 `IF` 裡 |
| `IFS` | `IFS(test1, result1, test2, result2, ..., TRUE, fallback)` | 回傳第一個成立的結果；**沒有內建 else**，全部不成立時回傳 `#N/A`，所以最後補 `TRUE, fallback` |
| `SWITCH` | `SWITCH(expr, value1, result1, value2, result2, default)` | 等值對應：代碼 → 標籤、狀態轉換 |
| `IFERROR` | `IFERROR(value, value_if_error)` | 錯誤時的替代值（小心掩蓋問題） |

```excel
=IF(AND(C2>=1000, D2="VIP"), "high", "normal")
=IFS(B2>=90, "A", B2>=80, "B", B2>=70, "C", TRUE, "F")
=SWITCH(E2, "TW", "Taiwan", "JP", "Japan", "Other")
```

> 巢狀 `IF` 超過三層就難以維護；分類規則多時，做一張「門檻 → 標籤」的查找表，再用 `XLOOKUP(..., match_mode = -1)`（找小於等於的最大值）取代。

## 文字

| 函數 | 範例 | 結果 / 用途 |
| --- | --- | --- |
| `LEFT` / `RIGHT` / `MID` | `=LEFT("DataCamp", 4)` | `Data`；`RIGHT` → `Camp` |
| `LEN` | `=LEN(A2)` | 字元數：檢查 ID、電話長度是否一致 |
| `TRIM` / `CLEAN` | `=TRIM(CLEAN(A2))` | 去前後與多餘空白 / 不可列印字元 |
| `UPPER` / `LOWER` / `PROPER` | `=PROPER("jOHN")` | `John` |
| `SUBSTITUTE` | `=SUBSTITUTE(A2, "-", "")` | 取代字串 |
| `CONCAT` / `&` | `=A2 & "-" & B2` | 串接；`CONCAT` 不會自動加分隔符 |
| `TEXTJOIN` | `=TEXTJOIN(", ", TRUE, A2:C2)` | 自動插分隔符並可略過空白 |
| `TEXT` | `=TEXT(A2, "yyyy-mm-dd")` | 數字 / 日期轉成指定格式的文字 |
| `TEXTSPLIT`、`TEXTBEFORE`、`TEXTAFTER` | `=TEXTBEFORE(A2, "@")` | Microsoft 365 新增，比 `LEFT` + `FIND` 好讀 |

## 日期

| 函數 | 範例 | 用途 |
| --- | --- | --- |
| `TODAY` / `NOW` | `=TODAY()` | 今天日期，每次重算都會變（易變函數） |
| `DATE` | `=DATE(2024, 3, 1)` | 由年月日組成日期，比在公式裡寫字串可靠 |
| `YEAR` / `MONTH` / `DAY` | `=YEAR(A2)` | 拆出年月日 |
| `WEEKDAY` | `=WEEKDAY(A2, 2)` | 星期幾；`2` = 週一為 1 |
| `WORKDAY` | `=WORKDAY(A2, 10, Holidays)` | 加 10 個工作日（排除週末與假日表） |
| `NETWORKDAYS` | `=NETWORKDAYS(A2, B2, Holidays)` | 兩日期間的工作日數 |
| `EDATE` / `EOMONTH` | `=EOMONTH(A2, 0)` | 加減月份 / 當月最後一天 |
| `DATEDIF` | `=DATEDIF(A2, TODAY(), "y")` | 年齡、年資（未列在函數清單但可用） |

> Excel 日期本質是序號（1900-01-01 = 1），所以可以直接相減得到天數。看起來像日期、卻靠左對齊的值其實是文字，要先轉型。

## 動態參照：`OFFSET`

`OFFSET(reference, rows, cols, [height], [width])` 從起點往下 / 往右移動後回傳新的範圍，適合「依使用者選擇的週次取值」、動態圖表範圍。

| 公式 | 意義 |
| --- | --- |
| `=OFFSET(A5, 1, MATCH($B$1, Weeks, 0))` | `MATCH` 算出 B1 選的週次在第幾欄，`OFFSET` 從 A5 移過去取值 |
| `=SUM(OFFSET(B2, 0, 0, COUNTA(B:B)-1, 1))` | 從 B2 起、高度隨資料列數自動延伸的範圍（扣掉標題列） |

| 注意 | 說明 |
| --- | --- |
| 易變函數 (volatile) | 任何儲存格變動都重算，大型活頁簿會變慢 |
| 可讀性差 | 搭配已命名範圍；只是查值時改用 `XLOOKUP` / `INDEX` |
| 新版替代 | 資料放進 Table 後範圍自動延伸，多數動態範圍需求就不需要 `OFFSET` |

## 金融函數

`PMT`、`IPMT`、`PPMT`、`NPV`、`IRR` 等見 [貸款攤還表](loan-amortization.md)。
