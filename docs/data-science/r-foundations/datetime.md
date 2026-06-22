# Date and Time in R

日期時間在 R 裡很容易表面上「看起來像字串」，但在分析流程中必須盡早轉成正確型別。否則排序、比較、分組與時間差計算都可能出錯。

## Core Classes

R 內最常見的時間型別有兩類：

- `Date`: 只有日曆日期，例如 `2024-06-19`
- `POSIXct` / `POSIXlt`: 同時包含日期、時間與時區

```r
today <- Sys.Date()
class(today)
# [1] "Date"

now <- Sys.time()
class(now)
# [1] "POSIXct" "POSIXt"
```

實務上，日資料通常用 `Date` 就足夠；只要牽涉盤中時間、log 時間戳或跨時區事件，再用 `POSIXct`。

## Parsing Dates

ISO 8601 格式最穩定，R 能直接辨識：

```r
as.Date("2024-06-19")
as.Date("2024/06/19")
```

如果來源是月日年這類模糊格式，要明確提供 `format`：

```r
as.Date("06/19/2024", format = "%m/%d/%Y")
```

常用格式代碼：

| Format | Meaning |
| --- | --- |
| `%d` | day of month |
| `%m` | month number |
| `%y` | two-digit year |
| `%Y` | four-digit year |
| `%b` | abbreviated month name |
| `%B` | full month name |

Key point: 不要依賴 R 自動猜格式，尤其是 `01/02/2024` 這種有歧義的字串。

## Extracting Calendar Parts

轉成日期型別後，才能安全提取日曆資訊：

```r
x <- as.Date("2024-06-19")

weekdays(x)
months(x)
quarters(x)
```

這些欄位常用來做：

- 週期性探索，例如 weekday effect
- 月度或季度彙總
- 報表切分與時間特徵工程

## Date Arithmetic

日期可以直接比較，也可以做差：

```r
start <- as.Date("2024-01-01")
end <- as.Date("2024-06-19")

end > start
end - start
```

這對持有期間、觀察窗長度、事件前後天數計算都很常見。

## Common Mistakes

- 把日期留在 `character` 型別就直接排序，結果變成字典序而不是時間序。
- 來源格式不是 ISO 8601，卻沒有指定 `format`。
- 需要時間戳與時區時仍使用 `Date`，導致日內資訊全部遺失。
- 混用不同時區資料卻沒有先標準化。

## Practical Workflow

1. 匯入資料後先用 `class()` 或 `str()` 確認時間欄位型別。
2. 先把原始字串轉成 `Date` 或 `POSIXct`。
3. 再做篩選、排序、差值與 calendar feature 提取。
4. 如果結果會影響交易日、事件時間或跨區資料，明確處理時區。
