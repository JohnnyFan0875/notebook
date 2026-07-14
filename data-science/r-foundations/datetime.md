# Date and Time in R

日期時間在 R 裡很容易表面上「看起來像字串」，但在分析流程中必須盡早轉成正確型別。否則排序、比較、分組與時間差計算都可能出錯。

這篇偏重 **R 的日期時間工作流**：`Date` / `POSIXct`、`lubridate`、解析、時區與日曆欄位提取。若你在 Python 標準庫工作，請看 [Datetime Module](../python-foundations/datetime.md)；若你在 pandas DataFrame 裡處理時間欄位，請看 [Pandas: Datetime Handling](../python-foundations/pandas/datetime.md)。

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

## Parsing with `lubridate`

當來源格式很多、分隔符不一致，或同一欄混有多種日期寫法時，`lubridate` 往往比手寫 `format` 更省力。

```r
library(lubridate)

ymd("2013-02-27")
ymd("2013.02.27")
ymd("2013 Feb 27th")

dmy("27-02-2013")
mdy("02-27-2013")
dmy_hm("27-02-2013 12:12pm")
```

這組函式的命名規則很直接：

- `ymd()`: year-month-day
- `dmy()`: day-month-year
- `mdy()`: month-day-year
- `*_hm()`, `*_hms()`: 額外包含 hour-minute 或 hour-minute-second

如果同一個欄位可能混有多種格式，可以用 `parse_date_time()`：

```r
parse_date_time("27-02-2013", orders = "dmy")

parse_date_time(
  c("27-02-2013", "2013 Feb 27th"),
  orders = c("dmy", "ymd")
)
```

Key point: `lubridate` 適合處理 messy input，但在正式資料管線裡，仍然應該盡量把上游格式標準化。

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

如果你需要明確指定輸出單位，可以用 `difftime()`：

```r
difftime(end, start, units = "days")
difftime(end, start, units = "weeks")
```

常見 `units` 包括：

- `"secs"`
- `"mins"`
- `"hours"`
- `"days"`
- `"weeks"`

`time1 - time2` 和 `difftime(time1, time2)` 的核心意思相同，但 `difftime()` 在你想明講單位時通常更清楚。

## `today()` and `now()`

如果你已經在用 `lubridate`，取得當前日期時間最常見的是：

```r
today()
now()
```

- `today()`: 回傳 `Date`
- `now()`: 回傳 `POSIXct`

這比只記 `Sys.Date()` 與 `Sys.time()` 更重要的地方在於，你要先想清楚自己需要的是「日曆日」還是「精確時間點」。

## Time Zones

只要資料跨地區、跨系統，或要對 log / API timestamp 做分析，時區就不能當成附帶資訊。

先確認系統預設時區：

```r
Sys.timezone()
OlsonNames()
```

- `Sys.timezone()`: 看目前 session 的預設時區
- `OlsonNames()`: 列出可用的 IANA timezone 名稱

建立 datetime 時，最好在一開始就把時區講清楚：

```r
meeting <- ymd_hms("2017-03-11 12:00:00", tz = "America/Los_Angeles")
tz(meeting)
```

Key point: timezone 應該視為 datetime 的一部分，不是之後再補的註解。

## `with_tz()` vs `force_tz()`

這兩個函式很容易混淆，但語意完全不同。

```r
meeting <- ymd_hms("2017-03-11 12:00:00", tz = "America/Los_Angeles")

with_tz(meeting, tzone = "America/New_York")
force_tz(meeting, tzone = "America/New_York")
```

- `with_tz()`: 保留同一個 instant，只改成另一個時區的顯示方式
- `force_tz()`: 保留牆上時鐘時間，重新指定它屬於哪個時區

直覺上可以這樣記：

- `with_tz()`: 「同一時刻，不同地區怎麼看」
- `force_tz()`: 「這個時鐘時間其實原本就該被解讀成另一個時區」

如果你把兩者用反，跨區事件排序與時間差常會直接錯掉。

## Common Mistakes

- 把日期留在 `character` 型別就直接排序，結果變成字典序而不是時間序。
- 來源格式不是 ISO 8601，卻沒有指定 `format`。
- 混有多種日期格式時只靠單一 parser，導致部分列悄悄變成 `NA`。
- 需要時間戳與時區時仍使用 `Date`，導致日內資訊全部遺失。
- 把 `with_tz()` 和 `force_tz()` 混用，結果改掉了事件實際時間點。
- 混用不同時區資料卻沒有先標準化。

## Practical Workflow

1. 匯入資料後先用 `class()` 或 `str()` 確認時間欄位型別。
2. 如果格式單一，用 `as.Date()` 或明確 `format`；如果格式混亂，再用 `lubridate`。
3. 先把原始字串轉成 `Date` 或 `POSIXct`，再做篩選、排序與時間差計算。
4. 如果需要週、月、季度或時段特徵，再提取 calendar parts。
5. 如果結果會影響交易日、事件時間或跨區資料，明確處理時區與輸出單位。
