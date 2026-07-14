# Joining Data with dplyr

join 幾乎是所有資料整理流程裡最容易「語法沒報錯，但結果已經歪掉」的步驟。`dplyr` 讓 join 語法很順，但真正重要的不是背下 `left_join()` 名稱，而是先想清楚 key、grain 與 unmatched rows 應該怎麼處理。

## The Core Mental Model

在做任何 join 前，先回答三件事：

1. 每張表的一列代表什麼 observation
2. 哪些欄位是用來對齊的 key
3. 你要保留的是交集、左表 universe，還是雙方全部資料

Key point: join 的本質不是「把兩張表貼在一起」，而是依照 key 對 observation 重新配對。

## `inner_join()`

`inner_join()` 只保留兩邊都能配對成功的列。

```r
library(dplyr)

sets %>%
  inner_join(themes, by = "theme_id")
```

適合情境：

- 你只關心 matched records
- 缺少對應 key 的列應該被排除
- 下游分析只想在交集 universe 上進行

Warning: `inner_join()` 很容易讓資料量變少，但如果你沒特別檢查，常常不會第一時間發現有資料被 silently 掉了。

## `left_join()`

`left_join()` 會保留左表全部列，右表有 match 就補欄位，沒有 match 就補 `NA`。

```r
inventory_parts_joined <- inventories %>%
  left_join(inventory_parts, by = c("id" = "inventory_id"))
```

這通常是分析工作裡最常用的 join，因為：

- 左表通常是你定義好的主 universe
- 右表只是來 enrich 左表
- unmatched rows 保留下來比較容易 debug

如果你的問題是「以主表為基準補 lookup 欄位」，預設先想 `left_join()` 通常比較安全。

## `right_join()` and `full_join()`

`right_join()` 是保留右表全部列；`full_join()` 則保留兩邊所有列。

```r
left %>%
  right_join(right, by = "id")

left %>%
  full_join(right, by = "id")
```

實務上：

- `right_join()` 語意上和交換左右表再 `left_join()` 很像
- `full_join()` 更適合資料比對、資料稽核與 coverage 檢查

如果目標是找出哪些 key 只存在某一側，`full_join()` 常比直接看單表摘要更直觀。

## Filtering Joins: `semi_join()` and `anti_join()`

不是所有 join 都是為了補欄位。有時你只是想用另一張表當過濾條件。

### `semi_join()`

保留左表中「有 match」的列，但不帶入右表欄位。

```r
orders %>%
  semi_join(valid_customers, by = "customer_id")
```

適合：

- 只想確認某筆資料是否存在於另一張表
- 想把左表限制在某個 reference set

### `anti_join()`

保留左表中「沒有 match」的列。

```r
orders %>%
  anti_join(valid_customers, by = "customer_id")
```

這在資料品質檢查非常好用，因為它直接回答：

- 哪些 key 沒對上
- 哪些值需要補 mapping
- 哪些列會在 `inner_join()` 裡被丟掉

## Joining on Different Column Names

左右表的 key 名稱不一樣時，要明確指定對應關係：

```r
inventories %>%
  inner_join(inventory_parts, by = c("id" = "inventory_id"))
```

這表示：

- 左表的 `id`
- 對右表的 `inventory_id`

Key point: key 名稱不同本身不是問題，模糊不清的對應才是問題。

## Joining on Multiple Keys

當唯一鍵不是單一欄位，而是欄位組合時，可以在 `by` 裡放多個鍵：

```r
batmobile %>%
  inner_join(
    batwing,
    by = c("part_num", "color_id"),
    suffix = c("_batmobile", "_batwing")
  )
```

如果左右表欄名不同，也可以寫成：

```r
left_join(x, y, by = c("a" = "b", "c" = "d"))
```

這比手動先拼 composite key 更清楚，因為它保留了每個欄位的原始語意。

## Overlapping Column Names and `suffix`

當左右表有同名欄位，但不是 join key 時，`dplyr` 會自動加 suffix。你也可以自己指定：

```r
left_join(
  batmobile,
  batwing,
  by = c("part_num", "color_id"),
  suffix = c("_batmobile", "_batwing")
)
```

這很重要，因為 join 後最容易搞混的不是 key，而是那些看起來都叫 `quantity`、`name`、`status` 的欄位。

## Join Cardinality Matters

join 出錯最常見的原因不是型別不合，而是 cardinality 沒想清楚。

常見情況：

- one-to-one
- many-to-one
- one-to-many
- many-to-many

如果你本來以為是 lookup-style many-to-one，但右表 key 其實不唯一，join 後列數就可能被意外放大。

Practical check:

```r
right_tbl %>%
  count(key) %>%
  filter(n > 1)
```

在正式 join 前先確認 key uniqueness，通常比 join 後才回頭查為什麼數字膨脹更省時間。

## Join Then Validate

join 完不要只看前幾列，至少檢查：

- row count 有沒有異常放大或縮小
- join key 有沒有大量 `NA`
- 重要欄位的 missingness 是否突然增加
- 分組摘要是否還符合商業常識

例如：

```r
nrow(left_tbl)
nrow(joined_tbl)

joined_tbl %>%
  summarize(missing_name = sum(is.na(name)))
```

Key point: join 是資料語義變更，不只是資料框操作。每次 join 後都應該做 sanity check。

## Practical Workflow

1. 先定義主表 grain。
2. 明確寫出 join key，而不是依賴隱含同名欄位。
3. 先檢查右表 key 是否唯一。
4. 依需求選 `inner`、`left`、`full` 或 filtering joins。
5. join 後立刻檢查 row count、`NA` 與重複放大問題。

## Common Mistakes

- 還沒確認 observation unit 就直接 join。
- 該用 `left_join()` 補欄位，卻用了 `inner_join()` 導致資料被丟掉。
- 忘了右表 key 不唯一，結果 row count 爆增。
- 左右表有同名欄位卻沒注意 suffix，後面讀錯欄位。
- 只看語法成功，沒檢查 join 後的 row count 和缺值分布。
