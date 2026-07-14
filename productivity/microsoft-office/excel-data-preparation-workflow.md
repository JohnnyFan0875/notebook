# Excel Data Preparation Workflow

這份筆記整理的是用 Excel 做資料準備時的一條實務工作流。重點不是把每個功能背起來，而是知道什麼順序比較穩、哪些工具各自解什麼問題。

## Why Preparation Comes First

分析品質通常不是先被模型限制，而是先被資料品質限制。

在 Excel 裡，data preparation 通常至少包含三件事：

- `cleaning`: 把錯誤、重複、雜訊與不一致格式處理掉
- `transforming`: 把原始欄位整理成比較能分析的欄位
- `organizing`: 讓資料的結構、欄位與摘要方式更容易使用

如果原始資料還沒整理好，就直接開始做公式、圖表或 pivot，後面通常會花更多時間返工。

## A Practical Preparation Sequence

可以先把流程想成下面這條線：

1. 匯入或收集 raw data
2. 檢查資料型別與格式
3. 去重、修正錯誤、補齊缺漏
4. 用文字與日期函數衍生欄位
5. 用邏輯函數建立 flags 或 categories
6. 用 lookup 從其他 sheet 補資訊
7. 用 PivotTable 檢查是否已經足夠乾淨、能進分析

## 1. Bring Data In Carefully

### Common Input Paths

Excel 常見的資料來源有：

- 手動輸入
- database 匯出
- `CSV`
- `text files`
- `HTML` / web table

這一步最重要的不是「匯進來就好」，而是匯入後馬上確認：

- 每欄是不是正確型別
- 分隔符號有沒有拆對
- 日期是不是被錯讀
- ID 欄位有沒有被 Excel 自動轉格式

### Practical Heuristic

如果原始資料來自多個檔案或多個 sheet，先不要急著做複雜分析。先確認每一份資料的欄位語意與粒度一致，否則後面 merge 起來很容易出錯。

## 2. Clean the Raw Table

### Remove Duplicates Carefully

`Remove Duplicates` 是很有用的功能，但它不是「看到重複就刪」。

真正該問的是：

- 這是重複紀錄，還是本來就該重複出現的合法事件？
- 判斷重複應該用哪幾個欄位作 key？

重點不是把資料列變少，而是只移除「不該存在的重複」。

### Sorting and Filtering

很多品質問題其實不是透過公式先發現，而是靠排序與篩選先看到異常：

- 某欄突然出現空白
- 同一欄混入不同格式
- 類別拼字不一致
- 數值範圍明顯不合理

在 Excel 裡，sorting 與 filtering 是最便宜的初步 QA。

### Fill Features

Excel 的 fill features 很適合做規則明確的小型清理：

- `Flash Fill`: 根據既有樣式自動補出模式
- `Fill Series`: 用於日期、編號或序列型欄位

適合情境：

- 從全名抽出某種固定格式
- 建立連續日期
- 快速補齊有穩定規律的欄位

但如果轉換規則很複雜或很難驗證，就不要太依賴 Flash Fill 的猜測結果。

## 3. Fix Types and Create Derived Fields

### Text Functions

#### `LEN`

```excel
=LEN(text)
```

適合用來檢查字串長度是否合理，例如：

- phone number 長度異常
- ID 格式不一致
- 某些欄位多了空白或特殊字元

#### `CONCAT`

```excel
=CONCAT(text1, [text2], ...)
```

適合把多欄文字合併成一欄，例如：

- 地址欄位整併
- 類別標籤拼接
- 建立 composite key

如果要自己控制分隔符，需要手動加 delimiter。

#### `TEXTJOIN`

```excel
=TEXTJOIN(delimiter, ignore_empty, text1, [text2], ...)
```

比 `CONCAT` 更適合處理：

- 多欄合併
- 要自動插入分隔符
- 想忽略空值

這在把多欄描述整理成單一欄位時很方便。

### Date Functions

#### `TODAY`

```excel
=TODAY()
```

常見用途：

- 顯示表格最後更新日期
- 建立相對於今天的判斷
- 做 aging / overdue 類欄位

#### `WEEKDAY`

```excel
=WEEKDAY(serial_number, [return_type])
```

適合把日期轉成星期資訊，常見於：

- 銷售日 vs 平日/假日分析
- 排班與營運規則
- 依星期聚合資料

#### `WORKDAY`

```excel
=WORKDAY(start_date, days, [holidays])
```

適合做工作日推算，例如：

- 預估完成日
- 員工可用時間
- SLA / deadline 類欄位

這比單純加天數更接近真實營運節奏，因為它能排除週末與假期。

## 4. Use Logical Functions to Prepare Analysis-Friendly Columns

很多資料準備其實不是在「算答案」，而是在把原始欄位轉成更容易 filter、group、aggregate 的欄位。

### Core Logical Functions

#### `AND`

```excel
=AND(logical1, [logical2], ...)
```

用在多個條件都要成立時。

#### `OR`

```excel
=OR(logical1, [logical2], ...)
```

用在多個條件只要一個成立即可。

#### `NOT`

```excel
=NOT(logical)
```

用在想排除某條件或反轉布林判斷時。

#### `IF`

```excel
=IF(logical_test, value_if_true, value_if_false)
```

最常見用途不是單純做 yes/no，而是：

- 建立 `flag`
- 分群
- 把 raw values 轉成分析欄位

### Combined Logical Patterns

很常見的資料準備模式包括：

```excel
=IF(AND(...), value_if_true, value_if_false)
=IF(OR(...), value_if_true, value_if_false)
=IF(NOT(...), value_if_true, value_if_false)
```

這些公式的用途通常是：

- 建立過濾旗標
- 標記高價值或高風險紀錄
- 加入新的 categorical variable

### Nested `IF`

當分類不只兩種時，可以用 nested `IF`：

```excel
=IF(test_1, result_1, IF(test_2, result_2, fallback))
```

它在 Excel 資料準備裡很常見，但也很容易失控。規則一旦超過幾層，就要開始警覺：

- 公式是否還看得懂
- 規則是否該外移成 lookup table
- 是否該改用更適合的工具

## 5. Enrich Data with Lookup Functions

如果某張資料表缺少描述欄位，Excel 常用 lookup 從其他 sheet 或檔案補資訊。

### `VLOOKUP`

```excel
=VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])
```

可以把它理解成：

- 在第一欄找 `lookup_value`
- 回傳同列中指定欄位的值

適合：

- 根據 ID 帶回名稱
- 把 reference table 的欄位補進主表

實務上多半優先用 `FALSE` 做 exact match，避免近似匹配帶來不明顯的錯誤。

### `HLOOKUP`

```excel
=HLOOKUP(lookup_value, table_array, row_index_num, [range_lookup])
```

概念和 `VLOOKUP` 類似，只是改成橫向搜尋。

它比 `VLOOKUP` 少見，但在橫向表頭排列的資料中還是有用。

## 6. Check Readiness with PivotTables

資料準備不是等到 100% 完美才算完成，而是至少要到「可以穩定做摘要與分析」。

`PivotTable` 很適合拿來檢查這件事，因為它能快速暴露：

- 類別拼字不一致
- 日期欄位無法正常 group
- 數值欄位其實被當文字
- 關鍵欄位空值太多

同時，PivotTable 也能開始把準備後的資料轉成可分析結構：

- aggregate and organize data in dynamic tables
- transform rows to columns, and vice versa
- group, filter, and summarize large volumes of records

如果 pivot 很難做、欄位一直不順、grouping 常失敗，通常代表資料還沒準備好。

## 7. A Good Excel Preparation Mindset

可以用這幾條原則收斂：

- 先確認型別，再開始大量寫公式。
- 先分清「非法重複」和「合法重複」，再用 `Remove Duplicates`。
- 先建立 flags 與 categories，再做群組分析。
- 先用 lookup 補齊描述欄位，再做彙總。
- 用 PivotTable 當 readiness check，而不是只把它當報表工具。

## When to Move Beyond Excel

Excel 很適合中小型、需要人工判讀的 data preparation，但如果開始出現以下情況，就該考慮往 Power Query、SQL、Python 或 BI 流程移動：

- 每週都要重複做同一套清理
- 需要處理多來源、多檔案整併
- 公式變得又長又難查錯
- 資料量大到 workbook 明顯變慢
- 清理邏輯需要可重跑、可版本控管

## Mental Model

這份筆記可以濃縮成一句話：

Excel data preparation 的核心，不是學很多功能，而是把 raw table 逐步變成 `clean -> typed -> enriched -> filterable -> summarizable` 的分析底稿。
