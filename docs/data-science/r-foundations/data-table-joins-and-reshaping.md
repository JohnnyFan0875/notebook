# Joining and Reshaping with data.table

`data.table` 的 join 與 reshape 很適合資料量大、步驟密集，或你想把篩選、聚合、更新和合併寫成同一套語法時使用。

如果 `dplyr` 的重點是把資料操作表達得清楚，`data.table` 的重點通常是把操作壓進同一個高效工作流裡。要讀懂 join，先記住它的核心語法：

```r
DT[i, j, by]
```

- `i`：挑哪些列，或拿哪張表來 join。
- `j`：要計算、選出或更新什麼。
- `by`：要按哪個鍵分組。

## `merge()` 與 `DT[i, on = ...]`

在 `data.table` 裡有兩條常見路線：

- `merge()`：語意接近 base R，適合表達 full join、left join、inner join。
- `DT[i, on = ...]`：更貼近 `data.table` 原生工作流，適合把 join 和後續聚合、更新寫在一起。

```r
merge(demographics, shipping, by = "name")
merge(demographics, shipping, by = "name", all = TRUE)
merge(demographics, shipping, by = "name", all.x = TRUE)
merge(demographics, shipping, by = "name", all.y = TRUE)
```

對照關係可以這樣記：

- 預設 `merge()` 是 inner join。
- `all = TRUE` 是 full join。
- `all.x = TRUE` 是 left join。
- `all.y = TRUE` 是 right join。

## `DT[i, on = ...]` 的 join 心智模型

`x[i, on = ...]` 可以先理解成「拿 `i` 的 key 去 `x` 裡找對應列」。因此保留哪些列，常跟 `i` 這張表有關。

```r
demographics[shipping, on = .(name)]
shipping[demographics, on = .(name)]
shipping[demographics, on = .(name), nomatch = 0]
```

幾個常用判讀：

- `demographics[shipping, on = .(name)]`：預設偏向 right join 的效果。
- `shipping[demographics, on = .(name)]`：把順序對調後，可得到 left join 的效果。
- `nomatch = 0`：只保留成功配對列，等同 inner join。
- 如果要 full join，通常直接用 `merge(..., all = TRUE)` 比較直觀。

### `on` 的寫法

```r
shipping[demographics, on = .(name)]
shipping[demographics, on = list(name)]

join_key <- "name"
shipping[demographics, on = join_key]
```

如果兩張表欄位名稱不同：

```r
customers[web_visits, on = .(name = person)]
customers[web_visits, on = c("name" = "person")]
```

多鍵 join 也是同樣概念：

```r
merge(purchases, web_visits, by = c("name", "date"))
purchases[web_visits, on = .(name, date)]
```

## Key 與 `setkey()`

如果某些欄位會反覆被拿來 join、排序或查找，可以先設 key。

```r
setkey(dt1, customer_id)
setkey(dt2, customer_id)

dt1[dt2, nomatch = 0]
```

多個欄位也可以：

```r
setkey(DT, key1, key2)

keys <- c("key1", "key2")
setkeyv(DT, keys)
```

實務上要注意：

- `setkey()` 會改變資料表本身的排序與 key 狀態。
- 如果你只是偶爾 join 一次，直接用 `on = ...` 往往已經夠用。
- 如果是重複查找、反覆 join，同一組 key 值值得明確設起來。

## Join 後立刻聚合

`data.table` 很強的一點，是 join 完可以直接在同一行做 `j` 與 `by`。

```r
demographics[shipping,
  on = .(name),
  .(avg_age = mean(age)),
  by = .(gender)
]
```

如果要按照 `i` 的每一列各自做計算，可以用 `by = .EACHI`：

```r
DT1[DT2, on = .(id), .(n = .N, total = sum(value)), by = .EACHI]
```

這很適合：

- 每個查詢條件對應一組彙總。
- 每個 lookup row 都想得到自己的統計結果。
- 避免先 join 出大表，再額外 group 一次。

## 常見 join 問題

### 欄位型別不一致

`data.table` 對 join key 的型別很嚴格。像 integer 對 character 這種情況會直接報錯，而不是默默幫你轉型。

```r
customers[web_visits, on = .(id)]
```

如果 `customers$id` 是 integer，但 `web_visits$id` 是 character，就需要先顯式轉型：

```r
web_visits[, id := as.integer(id)]
```

### 用錯 key 欄位

比起型別錯誤，更危險的是「剛好能 join，但意義完全錯」。例如把 `age` 對到 `duration`，或把地址對到姓名，程式可能跑得動，結果卻是假的。

整理 join 前，至少先確認：

- 兩邊 key 代表的是不是同一個實體。
- key 值粒度是否一致。
- 是否應該是一對一、一對多，還是多對多。

### 完全沒有共同值

如果 key 沒有任何交集：

- inner join 會回空表。
- left / right join 會留下大量 `NA`。
- full join 會看起來像兩張表硬被拼在一起。

這通常不是語法問題，而是 key 選錯或前處理不一致。

## 多對多 join 與 `allow.cartesian`

當兩邊 key 都有重複值時，join 可能導致列數急遽膨脹。`data.table` 會對這種 cartesian expansion 很謹慎。

```r
site1_ecology[site2_ecology, on = .(genus), allow.cartesian = TRUE]
```

只有在你非常確定多對多配對是預期行為時，才打開 `allow.cartesian = TRUE`。否則先檢查重複：

```r
duplicated(site1_ecology, by = "genus")
unique(site1_ecology, by = "genus")
```

建議先回答兩個問題：

- key 原本是否應該唯一？
- 如果不唯一，列數膨脹是否真的是你要的分析單位？

### 只取第一筆或最後一筆

如果同一個 key 有多筆對應，但你只想取其中一筆：

```r
site1_ecology[site2_ecology, on = .(genus), mult = "first"]
children[parents, on = .(parent = name), mult = "last"]
```

`mult = "first"` / `"last"` 可以快速限制匹配結果，但前提是你真的知道「第一筆」或「最後一筆」代表什麼。否則只是把資料問題藏起來。

## 合併多張 data.table

### `rbind()` 與 `rbindlist()`

```r
rbind(sales_2015, sales_2016)

tables <- list(sales_2015, sales_2016, sales_2017)
rbindlist(tables)
```

- `rbind()`：適合少量、直接列出的資料表。
- `rbindlist()`：適合你手上已經是一個 list。

### `idcol`

```r
rbindlist(
  list("2015" = sales_2015, "2016" = sales_2016),
  idcol = "year"
)
```

`idcol` 很適合把來源資訊保留下來，避免合併後分不清哪一列來自哪個批次、年份或檔案。

### `fill = TRUE`

```r
rbindlist(
  list(sales_2015, sales_2016),
  use.names = TRUE,
  fill = TRUE
)
```

如果欄位不完全一致，`fill = TRUE` 會補上缺的欄位並填 `NA`。這在批次整併半結構化資料時很常用，但也代表你後面要更小心欄位品質。

## `melt()` 與 `dcast()`

`data.table` 內建 reshape 工具，跟 `tidyr::pivot_longer()` / `pivot_wider()` 的角色很像。

### 寬轉長

```r
sales_long <- melt(
  sales_wide,
  id.vars = c("quarter", "department"),
  variable.name = "year",
  value.name = "amount"
)
```

適合情境：

- 多個年份或測量欄位散在不同 columns。
- 想把欄名轉成可分組的資料值。

### 長轉寬

```r
dcast(sales_long, quarter ~ department + year, value.var = "amount")
dcast(sales_long, season ~ year, value.var = "amount")
```

使用 `dcast()` 前先想清楚：

- 哪些欄位是 row id。
- 哪些欄位要展成新欄名。
- 如果同一格有多筆值，是否需要 `fun.aggregate`。

## 實務判斷

- 如果你要的是易讀性與團隊共用語意，`dplyr` join 往往更友善。
- 如果你要把 join、聚合、更新、reshape 串成單一高效工作流，`data.table` 很有優勢。
- 在 `data.table` 裡，語法會跑不代表 key 是對的；先驗證 key 的語意與唯一性，比記住 `nomatch` 或 `mult` 更重要。
