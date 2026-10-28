[Data Science](../README.md) › [R Foundations](README.md) › 日期與時間

# 日期與時間 (Date and Time)

日期欄位讀進來常是字串，必須**盡早轉成日期型別**，否則排序變字典序、時間差算不出來。R 的核心型別是 `Date` 與 `POSIXct`，日常操作交給 `lubridate`。Python 對應見 [日期與時間（Python）](../python-foundations/datetime.md)。

| 型別 | 內容 | 底層 | 例子 |
| --- | --- | --- | --- |
| `Date` | 日曆日 | 自 1970-01-01 的天數 | 採樣日、診斷日 |
| `POSIXct` | 時間點 + 時區 | 自 1970-01-01 UTC 的秒數 | 儀器時間戳、log |
| `POSIXlt` | 拆開的時間（年、月、日… 的 list） | list | 少用；data frame 欄位避免用 |
| `hms`（`hms` 套件） | 一天中的時間 | 秒數 | 給藥時間 `08:30:00` |
| `difftime` / `Duration` / `Period` | 時間長度 | | 追蹤天數 |

```r
Sys.Date(); Sys.time()                  # base R
lubridate::today(); lubridate::now()    # 同上，可指定 tzone
```

## 解析

```r
# base R：ISO 8601 直接讀；其他格式要給 format
as.Date("2024-06-19")
as.Date("06/19/2024", format = "%m/%d/%Y")
as.POSIXct("2024-06-19 14:30:00", tz = "UTC")

# lubridate：函式名 = 欄位順序
library(lubridate)
ymd("2013-02-27"); ymd("2013.02.27"); ymd("2013 Feb 27th")   # 分隔符不拘
dmy("27-02-2013"); mdy("02-27-2013")
ymd_hms("2024-06-19 14:30:00", tz = "Asia/Taipei")
dmy_hm("27-02-2013 12:12pm")

# 同一欄混多種格式
parse_date_time(c("27-02-2013", "2013 Feb 27th"), orders = c("dmy", "ymd"))

# 匯入時直接指定型別
readr::read_csv("visits.csv", col_types = cols(visit_date = col_date("%d/%m/%Y")))
```

| 代碼 | 意義 | 代碼 | 意義 |
| --- | --- | --- | --- |
| `%Y` / `%y` | 4 / 2 位數年 | `%H` / `%M` / `%S` | 時 / 分 / 秒 |
| `%m` | 月（01–12） | `%I` + `%p` | 12 小時制 + AM/PM |
| `%d` | 日 | `%z` | UTC 偏移 `+0800` |
| `%b` / `%B` | 月份縮寫 / 全名（依 locale） | `%j` | 一年第幾天 |

> `01/02/2024` 是 1 月 2 日還是 2 月 1 日無法自動判斷。解析失敗的列會變 `NA`（lubridate 會發 warning `failed to parse`），解析後檢查 `sum(is.na(x))`。

### Excel 帶來的日期問題

| 問題 | 現象 | 處理 |
| --- | --- | --- |
| 序列日期 | 讀進來是 `45000` | `as.Date(45000, origin = "1899-12-30")`；`janitor::excel_numeric_to_date()` |
| 基因名被轉成日期 | `SEPT1` → `1-Sep`、`MARCH1` → `1-Mar` | 原始資料不要經過 Excel；HGNC 已改名為 `SEPTIN1`、`MARCHF1`；用 Ensembl ID |
| 1900 / 1904 日期系統 | Mac 舊檔差 4 年 | `readxl` 會自動處理；手動換算時注意 origin |

## 擷取與取整

```r
x <- ymd("2024-06-19")
year(x); month(x, label = TRUE); day(x)     # 2024, Jun, 19
wday(x, label = TRUE, week_start = 1)       # Wed（週一為一週開始）
yday(x); isoweek(x); quarter(x)             # 171, 25, 2
weekdays(x); months(x); quarters(x)         # base R 版本，依 locale

floor_date(x, "month")                      # 2024-06-01   月初
ceiling_date(x, "month") - days(1)          # 2024-06-30   月底
round_date(now(), "15 minutes")
```

```r
library(dplyr)
visits |>
  mutate(month = floor_date(visit_date, "month")) |>
  count(month)                              # 每月次數；比 format(x, "%Y-%m") 保留 Date 型別
```

## 日期運算：duration vs period

```r
start <- ymd("2024-01-01"); end <- ymd("2024-06-19")
end - start                                 # Time difference of 170 days
difftime(end, start, units = "weeks")       # 24.28571 weeks
as.numeric(end - start)                     # 170

# Period：日曆單位（月長不同、夏令時間會調整）
ymd("2024-01-31") + months(1)               # NA     2 月沒有 31 日
ymd("2024-01-31") %m+% months(1)            # 2024-02-29   回到月底
# Duration：固定秒數
ymd("2024-01-01") + ddays(30)

# 年齡、追蹤時間：用 interval 再除
interval(ymd("1980-05-20"), ymd("2024-06-19")) %/% years(1)   # 44   足歲
time_length(interval(start, end), "month")                   # 5.6
```

| 類型 | 建立 | 意義 | 適用 |
| --- | --- | --- | --- |
| Duration | `ddays()`、`dhours()`、`dyears()` | 固定秒數 | 精確經過時間（藥物半衰期） |
| Period | `days()`、`months()`、`years()` | 日曆單位 | 「下個月同一天」、年齡 |
| Interval | `interval(a, b)` / `a %--% b` | 有起訖點的區間 | 計算年齡、判斷是否重疊 `int_overlaps()` |

存活分析的追蹤時間計算見 [Kaplan-Meier](../statistics/survival-analysis/kaplan-meier.md)。

## 時區

```r
Sys.timezone()                              # session 預設時區
OlsonNames()                                # 可用的 IANA 名稱，如 "Asia/Taipei"

meeting <- ymd_hms("2017-03-11 12:00:00", tz = "America/Los_Angeles")
with_tz(meeting, "America/New_York")        # 15:00 EST   同一時刻，換時區顯示
force_tz(meeting, "America/New_York")       # 12:00 EST   同一鐘面時間，改成另一時區（時刻變了）
```

| 函式 | 改變了什麼 | 用途 |
| --- | --- | --- |
| `with_tz()` | 只改顯示，時刻不變 | 把 UTC log 轉成當地時間呈現 |
| `force_tz()` | 時刻改變，鐘面不變 | 修正「讀進來時時區標錯」 |

> 儲存與計算一律用 UTC，呈現時再 `with_tz()`。`as.POSIXct()` 不給 `tz` 會用執行電腦的時區解讀，同一程式在不同機器結果不同。

## 常見錯誤

| 錯誤 | 結果 | 對策 |
| --- | --- | --- |
| 日期留在 character 就排序 | `"10/1"` 排在 `"9/1"` 前 | 先轉 `Date` |
| 沒指定 format / orders | 部分列悄悄變 `NA` | 解析後檢查 NA 數 |
| 需要時間卻用 `Date` | 日內資訊遺失 | 用 `POSIXct` |
| `with_tz()` / `force_tz()` 用反 | 事件時間點錯 | 見上表 |
| `ifelse()` 回傳日期 | 變成數字 | `dplyr::if_else()` |
| `+ months(1)` 遇到 31 日 | `NA` | `%m+%` |
