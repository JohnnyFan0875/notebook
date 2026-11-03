# Advanced Excel Functions

這份筆記整理 Excel 裡幾個很常見、但一旦掌握就能大幅提升分析效率的進階函數族群。

## When These Functions Matter

- `VLOOKUP` 或 `HLOOKUP` 開始卡在方向限制時。
- 你需要做 `2D lookup`，而不是只在單一欄位中查值。
- 你想依使用者選擇動態改變範圍、指標或圖表。
- 你需要在大型表格裡做帶條件的彙總，而且條件邏輯不只單一 `AND`。

## Lookup Upgrades

### Why `VLOOKUP` Is Not Enough

`VLOOKUP` 的主要限制不是它不能查值，而是它假設：

- lookup value 在左邊
- return value 在右邊
- 查找方向基本上是固定的

這讓它在欄位位置常變動、或需要往左查找時變得脆弱。

### `XLOOKUP`

`XLOOKUP` 可以把查找欄位與回傳欄位分開指定，因此查找方向更自由。

```excel
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])
```

實務上可以把它理解成：

- 在 `lookup_array` 找目標
- 從同列或同欄的 `return_array` 回傳結果
- 不需要像 `VLOOKUP` 那樣用欄位編號硬算位置

適合情境：

- 往左查找
- 欄位位置會調整
- 想順便處理找不到值時的預設輸出

### `INDEX` and `MATCH`

如果 `XLOOKUP` 不可用，或你想更明確地分開「定位」與「取值」，`INDEX` + `MATCH` 很實用。

`MATCH` 負責找位置：

```excel
=MATCH(lookup_value, lookup_array, 0)
```

`INDEX` 負責根據位置取值：

```excel
=INDEX(array, row_num, [column_num])
```

兩者結合後的基本心智模型是：

```excel
=INDEX(return_array, MATCH(lookup_value, lookup_array, 0))
```

### `2D lookup`

當資料是矩陣而不是單一欄位時，可以同時對 row 與 column 做 `MATCH`：

```excel
=INDEX(array, MATCH(row_key, row_labels, 0), MATCH(column_key, column_labels, 0))
```

這比把資料硬攤平成單欄查找更自然，也更適合交叉表。

## Dynamic Referencing with `OFFSET`

### What `OFFSET` Does

`OFFSET` 會從某個起點出發，往上下左右移動，然後回傳新的參照範圍。

可以先用概念理解：

- 起點在哪裡
- 往下幾列
- 往右幾欄
- 最後回傳哪個 cell 或 range

它特別適合：

- 新列或新欄會持續加入的資料
- 相對於某個基準點抓資料
- 建立動態範圍或動態圖表

### `OFFSET` with `MATCH`

當欄位位置不是固定值，而是由某個 label 決定時，可以用 `MATCH` 算出位移量，再交給 `OFFSET`。

```excel
=OFFSET(A5, 1, MATCH($B$1, Weeks, 0))
```

這類寫法的思路是：

- `MATCH` 找出目標欄位在第幾個位置
- `OFFSET` 從基準點偏移到正確欄位
- 最後取得對應值或範圍

### Practical Warning

`OFFSET` 很靈活，但公式也更難讀。當 workbook 已經很大、相依關係很多時：

- 先確認基準點是否穩定
- 優先搭配 named ranges
- 如果只是單純查值，通常先考慮 `XLOOKUP` 或 `INDEX` + `MATCH`

## Conditional Aggregation at Scale

### `SUMIFS`, `COUNTIFS`, `AVERAGEIFS`

這組函數適合直接在資料表上做條件式聚合：

- `SUMIFS`: 帶條件加總
- `COUNTIFS`: 帶條件計數
- `AVERAGEIFS`: 帶條件平均

例如：

```excel
=COUNTIFS(B:B, "Yes", E:E, "Florida")
```

這很適合多個 `AND` 條件，但遇到複雜 `OR` 條件時，公式通常會開始變長，甚至需要把多個 `COUNTIF(S)` 手動相加。

## Database Functions

### Why They Exist

Excel 還有一組較少人用、但很適合條件邏輯整理的 database functions：

- `DSUM`
- `DCOUNT`
- `DAVERAGE`
- `DMIN`
- `DMAX`

它們共用同一種思路：

```excel
=DFUNCTION(database, field, criteria)
```

三個核心參數：

- `database`: 含 header 的資料表
- `field`: 要彙總的欄位，可以是欄名、欄位索引或 header cell
- `criteria`: 另一塊 criteria table，用來表達篩選條件

### Why Criteria Tables Are Useful

database functions 的強項不是公式比較短，而是條件表達更清楚：

- 同一列通常可視為 `AND`
- 不同列通常可視為 `OR`
- 可以使用 `>`, `<`, `<>` 等運算子
- 可以搭配 `*`、`?` 這類 wildcard

例如：

```excel
=DSUM(A1:F6, "Sales", H1:J2)
```

如果把 criteria 範圍從 `H1:J2` 擴成 `H1:J3`，就能自然加入另一組 `OR` 條件。

### Practical Heuristic

可以這樣選：

- 條件簡單、只是日常報表: 先用 `SUMIFS` / `COUNTIFS` / `AVERAGEIFS`
- 條件開始像一張小規則表: 可以考慮 `DSUM` 一類的 database functions
- 邏輯太複雜、資料太大: 考慮改用 Power Query、SQL 或 Python

## Named Ranges Still Matter

這些進階函數一旦搭配 named ranges，可讀性會好很多。

例如：

- `Weeks`
- `Sales`
- `Categories`
- `Months`

比起直接寫 `B2:D400`，語意會清楚許多，也更不怕範圍位移時整串公式變得難懂。

## Mental Model

可以把這份筆記濃縮成四句話：

- `XLOOKUP` 解決方向受限的查找問題。
- `INDEX` + `MATCH` 解決需要彈性定位的查找問題。
- `OFFSET` 解決動態參照與動態範圍問題。
- `DSUM` 這類 database functions 解決條件邏輯更像小型規則表的彙總問題。
