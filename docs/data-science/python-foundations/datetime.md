# Datetime Module

Working with dates and times is a common task in Python. The `datetime` module provides classes for manipulating dates, times, and time intervals, while `dateutil` extends functionality for more advanced timezone handling.

## Import Packages

```python
import datetime
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from dateutil import tz
```

## Create Datetime Objects

```python
# Date only
dates = datetime(2016, 7, 16)

# Date and time
dt = datetime(2017, 10, 1, 15, 23, 25, 500000)
# Equivalent form:
# dt = datetime(year=2017, month=10, day=1, hour=15, minute=23, second=25, microsecond=500000)

# Current date and time (naive)
now = datetime.now()

# Current date and time in UTC
now_utc = datetime.now(timezone.utc)
```

## General Information

```python
# Today's date
today_date = datetime.today().date()

# Year and weekday
dates_year = dates.year
dates_day = dates.weekday()  # Monday=0, Sunday=6
```

## Formatting

Convert `datetime` objects to string in various formats:

```python
dates_isoformat = dates.isoformat()  # '2016-07-16'
dt_isoformat = dt.isoformat()        # '2017-10-01T15:23:25.500000'
```

Custom formatting with `strftime`:

```python
string_Ymd = dates.strftime('%Y/%m/%d')         # '2016/07/16'
string_YmdHMS = dt.strftime('%Y/%m/%d %H:%M:%S')  # '2017/10/01 15:23:25'
```

Parsing strings into datetime with `strptime`:

```python
dt = datetime.strptime("12/30/2017 15:19:13", "%m/%d/%Y %H:%M:%S")
```

## Timestamps

Convert Unix timestamps to `datetime`:

```python
ts = 1514665153.0
print(datetime.fromtimestamp(ts))  # 2017-12-30 15:19:13
```

## Replace Values

```python
dt_replace = dt.replace(minute=0)  # Replace only the minute
```

## Date Calculations

Perform arithmetic with `datetime` and `timedelta`:

```python
# Difference between two dates
duration = datetime(2016, 7, 17) - dates
duration_day = duration.days        # 1
duration_seconds = duration.total_seconds()

# Add a timedelta
td = timedelta(days=1, seconds=1)
new_date = dates + td
```

Comparing datetimes is also straightforward:

```python
asian_crisis = datetime(1997, 7, 2)
world_mini_crash = datetime(1997, 10, 27)

asian_crisis < world_mini_crash   # True
asian_crisis == world_mini_crash  # False
```

Creating relative dates should use `timedelta`, not manual day arithmetic:

```python
dt = datetime(2019, 1, 14)

# Safe
one_week_ago = dt - timedelta(days=7)

# Unsafe near month boundaries
# datetime(dt.year, dt.month, dt.day - 15)
```

## Timezones

Using `timezone` with `timedelta`:

```python
ET = timezone(timedelta(hours=-5))
dt = datetime(2017, 12, 30, 15, 9, 3, tzinfo=ET)
# 2017-12-30 15:09:03-05:00
```

Convert between timezones:

```python
# Change timezone
IST = timezone(timedelta(hours=5, minutes=30))
dt_IST = dt.astimezone(IST)   # 2017-12-31 01:39:03+05:30

dt_UTC = dt.astimezone(timezone.utc)  # 2017-12-30 20:09:03+00:00

# Set new timezone directly
dt_UTC = dt.replace(tzinfo=timezone.utc)  # 2017-12-30 15:09:03+00:00
```

Using `dateutil.tz` for named timezones:

```python
et = tz.gettz('America/New_York')
last = datetime(2017, 12, 30, 15, 9, 3, tzinfo=et)
# 2017-12-30 15:09:03-05:00
```

## Best Practices

- Always use `datetime` objects with timezone information (`tzinfo`) for applications that cross regions.
- Use `datetime.utcnow().replace(tzinfo=timezone.utc)` or `datetime.now(timezone.utc)` for consistent UTC timestamps.
- Prefer `dateutil.tz` for named timezones (`America/New_York`, `Asia/Taipei`) instead of fixed offsets.
- Use `timedelta` for safe date arithmetic instead of manually adjusting year, month, or day.
- If you compare datetimes from strings, parse them first with `strptime()` so the comparison happens on true datetime values.
