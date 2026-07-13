# Pandas: Reshaping & Merging

Reshaping and merging are essential for reorganizing data, joining datasets, and preparing for analysis. Pandas provides flexible tools like pivot, melt, stack/unstack, concat, and merge.

## Example Dataset

```python
import seaborn as sns
import pandas as pd

# Load iris dataset
iris = sns.load_dataset("iris").copy()

iris.head()
```

## Pivot Table

如果 key 組合在原資料中是唯一的，可以用 `.pivot()`；如果同一組 key 可能出現多筆，需要彙總，就用 `.pivot_table()`。

### `pivot()`

```python
iris.pivot(
    index="species",
    columns="sepal_width",
    values="petal_length",
)
```

- `.pivot()` 不做 aggregation。
- 如果同一組 `index + columns` 對應到多筆資料，會直接報錯。

```python
# Create a pivot table: mean petal_length by species and sepal_width
iris.pivot_table(
    index='species',
    values='petal_length',
    columns='sepal_width',
    aggfunc='mean',
    fill_value=0
)

# Pivot table with multiple aggregation functions
iris.pivot_table(
    index='species',
    values=['sepal_length', 'petal_width'],
    aggfunc={'sepal_length': 'mean', 'petal_width': 'sum'},
    fill_value=0
)
```

- `.pivot_table()` is flexible for summarization and reshaping.
- `.pivot_table()` 會先 aggregate，再 reshape。
- 當原始資料不是一對一映射時，通常優先想到 `pivot_table()`。

## Melt (Unpivot)

```python
# Convert wide to long format
iris.melt(
    id_vars=['species'],
    var_name='measurement',
    value_name='value'
)

# Melt only numeric columns
iris.melt(
    id_vars='species',
    value_vars=['sepal_length','sepal_width','petal_length','petal_width'],
    var_name='measurement',
    value_name='value'
)
```

- `.melt()` is useful for converting wide to long format.

## Concatenation

```python
# Vertical concatenation (stack rows)
pd.concat([iris, iris], ignore_index=True)

# Horizontal concatenation (align by index)
pd.concat([iris, iris[['petal_width']]], axis=1)

# Concatenate Series objects
series1 = pd.Series(['a','b','c','d'], index=['1','2','3','4'])
series2 = pd.Series(['e','f','g','h'], index=['5','6','7','8'])
pd.concat([series1, series2], ignore_index=True)
```

- `pd.concat()` stacks or aligns DataFrames/Series vertically or horizontally.

### Useful Concat Options

```python
pd.concat([df_jan, df_feb, df_mar], ignore_index=True)

pd.concat(
    [df_jan, df_feb, df_mar],
    keys=["jan", "feb", "mar"],
)

pd.concat([left, right], join="inner")
```

- `ignore_index=True` resets the concatenated index.
- `keys=` builds an outer index so you can track where each block came from.
- `join="inner"` keeps only shared columns when schemas differ.

### Verify Concatenation Integrity

```python
pd.concat([df_feb, df_mar], verify_integrity=True)
```

- `verify_integrity=True` checks whether the resulting index contains duplicates.
- This is useful when concatenation should preserve unique row labels but you are not fully sure the inputs are clean.

## Merging DataFrames

```python
# Basic merge on species
iris.merge(iris, on='species', suffixes=['_L','_R'])

# Ordered merge (useful for time series)
pd.merge_ordered(iris, iris, on='species')

# As-of merge (nearest key join, useful for time series)
iris_sorted = iris.sort_values('sepal_length')
pd.merge_asof(
    iris_sorted, iris_sorted,
    on='sepal_length',
    suffixes=['_L','_R']
)
```

- `merge`, `merge_ordered`, and `merge_asof` provide SQL-like joins.

### Spreadsheet Mental Model

如果你是從 Excel / Google Sheets 過來，可以先這樣對照：

- `left merge` 很像把右表當成 lookup table，依照左表 key 補欄位
- `inner merge` 很像做完 lookup 後，只保留兩邊都有對到的列
- `pd.concat(..., axis=0)` 很像把兩塊表上下貼起來
- `pd.concat(..., axis=1)` 很像把兩塊表左右貼起來

這個心智模型對入門很有用，但 pandas 比試算表更嚴格，因為它會保留 join cardinality 的影響。

### `VLOOKUP` Is Usually a Left Join

如果你過去常用 `VLOOKUP` 補欄位，pandas 裡最接近的通常是 `how="left"` 的 merge：

```python
fruit_colors.merge(
    fruit_prices,
    on="name",
    how="left",
)
```

可以這樣讀：

- 左表：我目前手上的主表
- 右表：我要拿來查值的 lookup table
- `on="name"`：共同 key
- `how="left"`：保留左表全部列，就算右表缺值也不丟列

這和很多人使用 `VLOOKUP` 的目的非常接近，只是 pandas 會直接回傳整張新表，而不是只補單一儲存格公式。

如果左右表的 key 名稱不同，就改用：

```python
left.merge(
    right,
    left_on="fruit_name",
    right_on="name",
    how="left",
)
```

### Merge Relationships Matter

一個 merge 最常見的 bug 不是語法錯，而是關聯型態判斷錯。

- `one_to_one`
- `one_to_many`
- `many_to_one`
- `many_to_many`

如果原本以為是 `one_to_one`，實際上卻是 `many_to_many`，merge 後列數可能會意外膨脹。

### Validate Merge Assumptions

```python
tracks.merge(specs, on="tid", validate="one_to_one")

albums.merge(tracks, on="aid", validate="one_to_many")
```

- `validate=` lets pandas check whether the merge shape matches your assumption.
- If the assumption is violated, pandas raises `MergeError` early instead of silently duplicating rows.

### Check Key Uniqueness Before Merging

在寫 merge 之前，先檢查 key 是否真的唯一，通常能擋掉大部分資料膨脹問題。

```python
games.duplicated("GameKey").sum()

plays.duplicated(["GameKey", "PlayId"]).sum()
```

- 結果是 `0` 代表這組 key 沒有重複。
- 單欄 key 與複合 key 要分開檢查。
- 如果你以為資料是一對一，但 `duplicated()` 不是 `0`，就應該先停下來確認資料結構。

### Joining on Multiple Keys

```python
pd.merge(
    df_left,
    df_right,
    on=["GameKey", "PlayId"],
    how="left",
)
```

- 當單一欄位不足以唯一識別列時，就要用複合 key。
- 這通常出現在事件資料、明細資料、交易資料。

### Joining on Different Column Names

如果左右表的 key 名稱不同，不需要先 rename。

```python
df1.merge(
    df2,
    left_on="GameKey",
    right_on="game-key",
    how="inner",
)
```

- `left_on=` / `right_on=` 可以直接描述對應關係。
- 只有在後續流程需要統一命名時，才值得先 rename。

### Column-to-Index Joins

有些資料表把 key 放在欄位，有些把 key 放在 index；pandas 可以直接混合 join。

```python
teams.merge(positions, left_on="player_id", right_index=True)

positions.merge(teams, left_index=True, right_on="player_id")
```

- `left_on=...` + `right_index=True` 表示左邊用欄位、右邊用 index。
- `left_index=True` + `right_on=...` 則是反過來。
- 這種寫法比先 `reset_index()` 再 merge 更直接。

### `.join()` as an Index-Based Shortcut

如果本來就是用 index 對 index 合併，`.join()` 會比 `merge()` 更短。

```python
left.join(right, how="left")
```

可以把它想成：

- `merge()` 比較通用
- `.join()` 偏向 index-oriented 的合併捷徑
- 當右表已經整理成 lookup-style index 時，`.join()` 很順手

### Anti Join Pattern

pandas 沒有內建 `anti join` 名稱，但可以用 `indicator=True` 很穩定地做。

```python
genres_tracks = genres.merge(
    top_tracks,
    on="gid",
    how="left",
    indicator=True,
)

missing_gid = genres_tracks.loc[
    genres_tracks["_merge"] == "left_only",
    "gid",
]
```

這個 pattern 很適合找：

- 主表中沒有匹配到的 key
- 維表缺失值
- join 後被遺漏的類別

如果你做的是 `outer merge`，`_merge` 欄位通常會出現：

- `left_only`
- `right_only`
- `both`

這很適合用來做資料盤點與 reconciliation。

### Working with Overlapping Column Names

當左右表有同名欄位但不是 join key 時，最好明確指定 suffix。

```python
current.merge(
    drafted,
    on="name",
    suffixes=("_current", "_drafted"),
)
```

- 不要完全依賴預設的 `_x` / `_y`。
- 自訂 suffix 之後，後續欄位來源會清楚很多。

### Sorting the Merge Output

如果你希望結果依照 key 排序，可以讓 merge 直接做：

```python
current.merge(
    drafted,
    on="name",
    sort=True,
)
```

- `sort=True` 會依 key 排序結果。
- 但如果你想保留左表原本順序，通常不要開這個選項。

### When to Use `merge_ordered()`

`merge_ordered()` 適合有順序的資料，特別是時間序列或事件序列。

```python
pd.merge_ordered(
    aapl,
    mcd,
    on="date",
    suffixes=("_aapl", "_mcd"),
)
```

可以把它想成：

- 還是 merge
- 但更在乎 key 的順序
- 常用在經濟資料、股價、報表時間軸

如果希望有序欄位在合併後向前延續，也可以用：

```python
pd.merge_ordered(
    aapl,
    mcd,
    on="date",
    fill_method="ffill",
)
```

- `fill_method="ffill"` 常見於時間序列對齊後的前值延續。

### When to Use `merge_asof()`

`merge_asof()` 適合「找最近但不一定完全相等的 key」，最常見的是時間戳對齊。

```python
pd.merge_asof(
    visa,
    ibm,
    on="date_time",
    suffixes=("_visa", "_ibm"),
)
```

也可以指定方向：

```python
pd.merge_asof(
    visa,
    ibm,
    on="date_time",
    direction="nearest",
)
```

實務上可以這樣記：

- `merge()`：key 要精確相等
- `merge_ordered()`：有序資料對齊
- `merge_asof()`：按最近 key 對齊

如果你是從試算表過來，`merge_asof()` 可以想成比較接近 `VLOOKUP(range_lookup=TRUE)` 的概念，但 pandas 版本更明確也更可控。

### Wide to Long Reminder

如果資料不是 join 問題，而是欄位結構太寬，通常要先想 `melt()`。

```python
social_fin_tall = social_fin.melt(
    id_vars=["financial", "company"],
    var_name="metric",
    value_name="value",
)
```

`melt()` 的本質是 unpivot：把多個欄位名稱壓成一個欄位，讓資料變成 tidy / long format。

### `wide_to_long()`

如果欄位名稱本身帶有規律，例如 `sales_2022`、`sales_2023`，`wide_to_long()` 會比手動 `melt()` 更乾淨。

```python
pd.wide_to_long(
    writers_norm,
    stubnames=["books"],
    i=["first", "last"],
    j="feature",
    sep="_",
    suffix=r"\w+",
)
```

它適合處理「欄位名稱中就藏著變數值」的 wide format。

### `explode()`

當一個欄位裡面存的是 list-like 值時，可以用 `.explode()` 把一列展成多列。

```python
cities = pd.DataFrame(
    {
        "city": ["Taipei", "Kaohsiung"],
        "zip_code": [["100", "103"], ["800", "801"]],
    }
)

cities.explode("zip_code")
```

常見搭配是先 `str.split()` 再 `explode()`：

```python
(
    cities.assign(zip_code=cities["zip_code"].str.split(","))
    .explode("zip_code")
    .reset_index(drop=True)
)
```

這在處理逗號分隔標籤、郵遞區號、ID list 時很實用。

## Key Takeaways

- `.pivot_table()` is powerful for summarization and reshaping.
- `.melt()` transforms wide to long format.
- `.stack()` and `.unstack()` convert between hierarchical and flat tables.
- `pd.concat()` appends or aligns DataFrames.
- `merge` operations join datasets on keys, similar to SQL joins.
