[Data Science](../README.md) › [Python Foundations](README.md) › 日期與時間

# 日期與時間 (Datetime)

前半是 Python 標準庫（`datetime`、`timedelta`、`zoneinfo`），後半是 [pandas datetime 欄位](#pandas-datetime-欄位)（`pd.to_datetime`、`.dt`、`DatetimeIndex`、resample）。R 的對應寫法見 [R 日期與時間](../r-foundations/datetime.md)。

| 型別 | 表示 | 例子 |
| --- | --- | --- |
| `date` | 日期 | 採樣日 `2024-03-15` |
| `datetime` | 日期 + 時間（可帶時區） | 儀器輸出時間戳 |
| `timedelta` | 時間長度 | 處理後 48 小時 |
| `pd.Timestamp` / `DatetimeIndex` | pandas 版 datetime（向量化） | 整欄時間 |
| `pd.Timedelta` / `pd.DateOffset` | 固定長度 / 日曆偏移（「下個月」） | `+ pd.DateOffset(months=1)` |

## 建立、解析與格式化

```python
from datetime import date, datetime, timedelta, timezone

d = datetime(2016, 7, 16)                          # 只有日期 → 00:00:00
dt = datetime(2017, 10, 1, 15, 23, 25, 500000)     # 年月日時分秒微秒
now_utc = datetime.now(timezone.utc)               # 現在（UTC，aware）
date.today()

d.year, d.weekday()                                # 2016, 5（Monday=0, Sunday=6）
dt.date(), dt.time()

# datetime → 字串
d.isoformat()                                      # '2016-07-16T00:00:00'
d.date().isoformat()                               # '2016-07-16'
dt.strftime("%Y/%m/%d %H:%M:%S")                   # '2017/10/01 15:23:25'

# 字串 → datetime
datetime.strptime("12/30/2017 15:19:13", "%m/%d/%Y %H:%M:%S")
datetime.fromisoformat("2024-03-15T14:30:00+08:00")   # ISO 8601 首選，3.11+ 接受大多數 ISO 寫法

# Unix timestamp → datetime：一定要指定 tz，否則依「執行這台電腦」的時區解讀
datetime.fromtimestamp(1514665153, tz=timezone.utc)   # 2017-12-30 20:19:13+00:00

dt.replace(minute=0, second=0, microsecond=0)      # 截到整點
```

| 代碼 | 意義 | 代碼 | 意義 |
| --- | --- | --- | --- |
| `%Y` | 4 位數年 | `%H` | 24 小時制 |
| `%m` | 月（01–12） | `%I` / `%p` | 12 小時制 / AM、PM |
| `%d` | 日 | `%M` / `%S` | 分 / 秒 |
| `%B` / `%b` | 月份全名 / 縮寫 | `%f` | 微秒 |
| `%A` / `%a` | 星期全名 / 縮寫 | `%z` | UTC 偏移（`+0800`） |
| `%j` | 一年中第幾天 | `%%` | 字面 `%` |

> 存檔、交換資料一律用 ISO 8601（`2024-03-15` / `2024-03-15T14:30:00Z`）：字典序 = 時間序，也沒有 `03/04` 是 3 月 4 日還是 4 月 3 日的歧義。

## 日期運算

```python
datetime(2016, 7, 17) - d                          # timedelta(days=1)
(datetime(2016, 7, 17) - d).total_seconds()        # 86400.0
d + timedelta(days=1, hours=6)
d - timedelta(weeks=1)                             # 用 timedelta，不要手動改 day（月底會出錯）
datetime(1997, 7, 2) < datetime(1997, 10, 27)      # True：比較前先 parse，不要比字串

# 「加一個月」不是固定天數：timedelta 沒有 months，用 dateutil 或 pandas
from dateutil.relativedelta import relativedelta
datetime(2024, 1, 31) + relativedelta(months=1)    # 2024-02-29（自動夾到月底）
```

## 時區 (Timezones)

| | naive | aware |
| --- | --- | --- |
| 有 `tzinfo`？ | 否 | 是 |
| 意義 | 只是牆上時間的字面值 | 能對齊到 UTC 的確切時刻 |
| 能互相比較 / 相減？ | naive 與 aware 混用會 `TypeError` | |

| 操作 | 效果 | pandas 對應 |
| --- | --- | --- |
| `replace(tzinfo=...)` | **只貼標籤**，牆上時間不變 | `.dt.tz_localize()` |
| `astimezone(...)` | **換算**到另一時區，同一時刻 | `.dt.tz_convert()` |

```python
from zoneinfo import ZoneInfo                      # 3.9+ 標準庫；Windows 需 pip install tzdata

ny = ZoneInfo("America/New_York")
dt = datetime(2017, 12, 30, 15, 9, 3, tzinfo=ny)   # 2017-12-30 15:09:03-05:00
dt.astimezone(timezone.utc)                        # 2017-12-30 20:09:03+00:00
dt.astimezone(ZoneInfo("Asia/Kolkata"))            # 2017-12-31 01:39:03+05:30

dt.replace(tzinfo=timezone.utc)                    # 15:09:03+00:00：錯把當地時間標成 UTC，偏了 5 小時

fixed = timezone(timedelta(hours=-5))              # 固定偏移：不處理夏令時間，盡量用具名時區

# 夏令時間 (DST) 陷阱：同一 aware 時區內的加減是「牆上時間」運算
a = datetime(2024, 3, 10, 1, 30, tzinfo=ny)
a + timedelta(hours=1)                             # 02:30-05:00：當天 02:00–03:00 根本不存在
(a.astimezone(timezone.utc) + timedelta(hours=1)).astimezone(ny)   # 03:30-04:00：正確
```

| 原則 | 說明 |
| --- | --- |
| 內部一律存 UTC | 只有顯示給人看時才轉當地時間 |
| 用具名時區 | `ZoneInfo("Asia/Taipei")`，不用固定偏移；舊程式的 `pytz` / `dateutil.tz` 可換掉 |
| 跨 DST 的計算先轉 UTC | 量測經過時間、排程間隔 |
| 不要用 `datetime.utcnow()` | 回傳 naive 物件，3.12 起已棄用；改 `datetime.now(timezone.utc)` |

## pandas datetime 欄位

### 讀檔與轉型

```python
import pandas as pd

rides = pd.read_csv("rides.csv", parse_dates=["start", "end"])   # 讀檔時直接轉

s = pd.Series(["2024-01-01", "bad", "2024-06-20"])
pd.to_datetime(s, errors="coerce")                 # 無法解析的變 NaT（Not a Time）
pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")  # 指定格式：更快，且避免猜錯
pd.to_datetime(["03/04/2024"], dayfirst=True)      # 2024-04-03：歐洲格式
pd.to_datetime(df["ts"], unit="s", utc=True)       # Unix 秒數

df["when"] = pd.to_datetime(df["date"] + " " + df["time"], errors="coerce")  # 日期、時間分兩欄時先合併
```

> `errors="coerce"` 會把錯誤靜默變成 `NaT`。轉完務必 `.isna().sum()` 檢查，數量異常多通常代表格式猜錯（例如混了 `MM/DD` 與 `DD/MM`）。

### 取成分、格式化與運算

```python
t = df["measurement_date"]
t.dt.year, t.dt.month, t.dt.day                    # 數值成分
t.dt.day_name()                                    # 'Monday'...
t.dt.dayofweek                                     # Monday=0
t.dt.quarter, t.dt.isocalendar().week
t.dt.normalize()                                   # 去掉時間，只留日期（仍是 datetime）
t.dt.floor("h")                                    # 截到整點
t.dt.strftime("%d-%m-%Y")                          # → 字串

(pd.Timestamp.today() - t).dt.days                 # 距今天數：相減得 Timedelta
(df["end"] - df["start"]).dt.total_seconds() / 60  # 持續分鐘數
t + pd.Timedelta(days=30)                          # 固定長度
t + pd.DateOffset(months=1)                        # 日曆月：01-31 → 02-29

df[t > "2024-01-03"]                               # 可直接和字串比較
df[t.between("2024-01-01", "2024-03-31")]

# 時區：localize 貼標籤，convert 換算
df["start"].dt.tz_localize("America/New_York").dt.tz_convert("UTC")
```

`DatetimeIndex` 的成分直接用 `df.index.month`、`df.index.day_name()`，不需要 `.dt`。

### 以時間為索引：篩選與 resample

```python
ts = df.set_index("measurement_date").sort_index()
ts.loc["2024-01"]                                  # 部分字串索引：整個一月
ts.loc["2024-01-15":"2024-02-15"]                  # 時間切片（含兩端）

ts["value"].resample("D").mean()                   # 每天一筆，沒資料的天補 NaN
ts["value"].resample("W").sum()
ts["value"].resample("ME").mean()                  # 月底；pandas 2.2+ 用 "ME"，舊寫法 "M" 已棄用
ts["value"].rolling("7D").mean()                   # 7 天移動平均

ts.groupby(ts.index.month)["value"].mean()         # 季節性：所有年的一月合在一起
```

| 寫法 | 結果 | 用途 |
| --- | --- | --- |
| `groupby(index.month)` | 最多 12 列，跨年合併同月份 | 比較季節型態 |
| `resample("ME")` | 每個實際月份一列，依時間排序 | 得到正規時間序列 |

| 頻率代碼 | 意義 | 頻率代碼 | 意義 |
| --- | --- | --- | --- |
| `D` | 日 | `ME` / `MS` | 月底 / 月初 |
| `h` / `min` / `s` | 時 / 分 / 秒 | `QE` | 季底 |
| `W` | 週（預設週日結束） | `YE` | 年底 |
| `B` | 營業日 | | |

時間序列建模（趨勢、季節分解、自相關）見 [時間序列分析](../statistics/time-series-analysis/README.md)；畫時間序列圖見 [pandas 繪圖](../data-manipulation-and-eda/visualization/pandas-plotting.md)。
