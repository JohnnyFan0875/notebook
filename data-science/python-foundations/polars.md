# Polars

Polars 是一個以 expression 為核心的 DataFrame 工具，特別適合欄位選取、轉換、過濾與高效查詢。  
如果 pandas 常讓你用「逐步操作 DataFrame」思考，Polars 更鼓勵你用「描述整個查詢」的方式思考。

## Why Polars Feels Different

幾個很重要的特性：

- expression-first API
- 支援 eager 與 lazy 兩種模式
- 很多操作鼓勵一次描述完整 transformation
- `select()` 和 lazy planning 能幫助 query optimization

這代表 Polars 不只是另一個 DataFrame 套件，它也在引導你靠近 query engine 的思維。

## Reading Data

### Eager Mode

```python
import polars as pl

rentals = pl.read_csv("vacation_rentals.csv")
```

`read_csv()` 會直接把資料讀成 `DataFrame`。  
這種方式適合：

- 小到中型資料
- 想一步一步檢查結果
- 正在 debug

### Lazy Mode

```python
lazy_rentals = pl.scan_csv("vacation_rentals.csv")
```

`scan_csv()` 不會立刻把整份資料完整 materialize，而是先建立 query plan。  
這種方式適合：

- 資料較大
- 有多步 transformation
- 想讓 Polars 做 query optimization

## Core Mental Model: Expressions

Polars 很多操作不是直接「改 DataFrame」，而是先建立 expression，再交給 engine 執行。

最常見的入口是 `pl.col()`：

```python
rentals.select(
    pl.col("name"),
    pl.col("price"),
)
```

可以把 `pl.col()` 想成：

- 指定欄位
- 對欄位做計算
- 把這些計算組成新的查詢

## Selecting Columns

### Simple Selection

```python
rentals.select("name", "price")
```

Polars 通常偏好 `select()`，因為它比直接用 bracket subsetting 更符合 query planning。

### Why `select()` Matters

`select()` 不只是語法偏好，它也有助於優化。  
在 lazy mode 下，Polars 可以更明確知道最後真正需要哪些欄位。

## Transforming Columns

### Arithmetic with Expressions

```python
rentals.select(
    (pl.col("price") / pl.col("beds")).alias("price_per_bed")
)
```

這種寫法的重點是：

- 計算直接描述在 expression 裡
- 可以順便 rename
- 不需要先拆成很多臨時欄位

### Renaming with `alias()`

```python
rentals.select(
    pl.col("price").alias("nightly_price")
)
```

`alias()` 很重要，因為 expression 一多，如果沒有命名，輸出常會變得不好讀。

### Constants and Derived Columns

你也可以從常數建立 expression，或把新欄位加回原表。

```python
rentals.with_columns(
    (pl.col("price") * 0.9).alias("discount_price")
)
```

## `select()` vs `with_columns()`

這是 Polars 很核心的分別：

- `select()`: 只保留你指定的輸出欄位
- `with_columns()`: 保留原本欄位，另外新增或覆蓋欄位

### Use `select()` When

- 你想明確定義最後輸出
- 你想只保留少數欄位
- 你在 lazy mode 下想讓 projection 更清楚

### Use `with_columns()` When

- 你要在原資料上加新欄位
- 你想保留既有欄位並做增量轉換

## Filtering Rows

Polars 的過濾同樣是 expression-based：

```python
rentals.filter(
    pl.col("type") == "Villa"
)
```

也可以組多條件：

```python
rentals.filter(
    (pl.col("price") < 500) &
    (pl.col("beach") == True)
)
```

這種寫法的重點是：

- 條件本身也是 expression
- 過濾邏輯和查詢描述在同一層
- 在 lazy mode 下可一起被優化

## Dtype-Aware Operations

Polars 很強調 dtype-aware expressions。  
這代表很多字串、數值或型別轉換操作，都可以用欄位型別導向的方式表達。

例如字串長度：

```python
rentals.with_columns(
    pl.col("name").str.len_chars().alias("name_len")
)
```

甚至可以一次對某類型欄位操作：

```python
rentals.with_columns(
    pl.col(pl.String).str.len_chars()
)
```

這對 schema 明確、欄位很多的資料表特別方便。

## Lazy Query Planning

Polars lazy mode 最大的價值，是它會先累積查詢，再一起優化。

```python
query = (
    pl.scan_csv("vacation_rentals.csv")
    .select("name", "price")
)
```

真正執行時才 `collect()`：

```python
result = query.collect()
```

### Explain the Plan

```python
print(
    pl.scan_csv("vacation_rentals.csv")
    .select("name", "price")
    .explain()
)
```

這能幫你看到 query plan，例如 projection pushdown。  
從資料工作角度看，這很重要，因為它讓你知道 engine 是否真的只讀必要欄位。

## Eager vs Lazy

### Prefer Eager When

- 你在探索資料
- 你想一步一步看中間結果
- 你在 debug 某段 transformation

### Prefer Lazy When

- 你已經知道完整處理流程
- 你要鏈很多步驟
- 你在乎效能與 query optimization

一個很實用的心智模型是：

- `eager`: step-by-step
- `lazy`: full-query

## Practical Workflow

```python
import polars as pl

result = (
    pl.scan_csv("vacation_rentals.csv")
    .filter(pl.col("type") == "Villa")
    .with_columns(
        (pl.col("price") / pl.col("beds")).alias("price_per_bed")
    )
    .select("name", "price", "price_per_bed")
    .collect()
)
```

這段示範了 Polars 的典型思路：

1. 先建立 lazy source
2. 用 expression 過濾與轉換
3. 用 `select()` 定義輸出
4. 最後 `collect()`

## Practical Takeaways

- 把 Polars 想成 expression engine，比把它想成 pandas clone 更準。
- `select()` 與 `with_columns()` 的差異，是寫出可維護 Polars 程式的關鍵。
- eager mode 比較適合 debug；lazy mode 比較適合正式 pipeline。
- 當資料變大時，`scan_csv()` + `collect()` 通常比直接 `read_csv()` 更值得先考慮。
