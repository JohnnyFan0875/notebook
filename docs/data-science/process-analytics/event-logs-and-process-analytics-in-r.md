# Event Logs and Process Analytics in R

process analytics 的核心資料結構不是一般寬表，而是 event log。每一列代表某個 case 在某個時間點發生了一個 activity，當很多列依時間串起來後，才形成一條完整流程。

## What Makes Process Data Different

一般分析常把每列資料看成獨立觀測；process data 則更關心：

- `case`：流程實例，例如一位病人、一張訂單、一個申請案
- `activity`：流程中的一步，例如 `register`、`approve`、`ship`
- `timestamp`：事件發生時間
- `resource`：誰執行了這一步
- `trace`：某個 case 經過的一整串 activities

Key point: 單看 activity frequency 不夠，因為流程分析真正關心的是順序、持續時間、變體與交接。

## First Glimpse of an Event Log

開始分析前，先做最基本的 scope check：

- 有多少 cases？
- 有多少 distinct activities？
- 有多少 events？
- 資料涵蓋哪段時間？

在 `bupaR` 裡，最直接的起點是：

```r
library(bupaR)

summary(learning)
n_cases(learning)
n_activities(learning)
```

這一步很像 EDA，只是 focus 從欄位分布轉成流程規模與流程粒度。

## Creating an Event Log Object

原始 event data 通常先是一張表，之後要明確指定哪些欄位扮演流程角色：

```r
event_data %>%
  eventlog(
    case_id = "patient",
    activity_id = "handling",
    activity_instance_id = "handling_id",
    timestamp = "time",
    lifecycle_id = "registration_type",
    resource = "employee"
  )
```

這些欄位大致代表：

- `case_id`：哪個流程實例
- `activity_id`：做了哪個活動
- `activity_instance_id`：同一活動的具體執行實例
- `timestamp`：發生時間
- `lifecycle_id`：開始 / 完成等 lifecycle 狀態
- `resource`：由誰執行

如果這一步定義錯，後面的 trace、throughput 與 resource analysis 都會一起偏掉。

## Activities and Their Frequencies

一個很實用的起點是先看有哪些活動：

```r
activity_labels(learning)
activities(learning)
```

`activities()` 會整理出像：

- `absolute_frequency`
- `relative_frequency`

這能幫你快速判斷：

- 哪些活動是流程主幹
- 哪些活動非常少見
- 是否存在例外或補救型步驟

但 activity 頻率只回答「常不常出現」，還沒有回答「如何組成流程」。

## Traces Describe Process Variants

每個 case 都會形成一條 trace，也就是活動序列。這是流程分析最有代表性的物件之一。

```r
traces(learning)
trace_explorer(learning)
```

trace analysis 幫你回答：

- 最常見的流程變體是什麼？
- 流程是否高度標準化？
- 是否有大量例外路徑？

如果 trace 分布非常分散，通常表示流程變異高，後續要更小心地做 aggregation。

## Resource and Organizational Analysis

process analytics 不只看 control flow，也很常看工作怎麼在人之間流動。

先看有哪些角色或員工：

```r
resource_labels(log_hospital)
resources(log_hospital)
```

接著可以看 resource 與 activity 的對應關係：

```r
log_hospital %>%
  resource_frequency(level = "resource-activity")

log_hospital %>%
  resource_frequency(level = "resource-activity") %>%
  plot()
```

這個矩陣很適合拿來看：

- 誰執行哪些任務
- 是否有人高度專精於少數活動
- 是否某些活動只靠少數人支撐，存在 brain drain 風險

若想看工作交接：

```r
resource_map(log_hospital)
```

這會把焦點從「誰做了什麼」轉成「工作從誰交到誰」，比較接近 handover network。

## Granularity Levels Matter

課程裡很值得保留的一個概念，是很多 process metric 都可以在不同粒度計算：

```r
<process_metric>(level = "log")
<process_metric>(level = "trace")
<process_metric>(level = "case")
<process_metric>(level = "activity")
<process_metric>(level = "resource")
<process_metric>(level = "resource-activity")
```

同一個 metric 在不同 level 代表的問題不一樣。例如：

- `processing_time(level = "resource")`：偏 organizational performance
- `number_of_repetitions(level = "resource")`：把 control-flow 指標映到 resource 視角

Key point: process metric 不只是函式名，還包含「在哪個 level 看」這個分析決定。

## Filtering Cases and Variants

process analytics 常常不是直接分析整個 log，而是先把案例過濾出來。

例如依 throughput time 篩 case：

```r
filter_throughput_time(log, interval = c(5, 10))
filter_throughput_time(log, percentage = 0.5)
filter_throughput_time(log, interval = c(5, NA), units = "days")
filter_throughput_time(log, interval = c(5, 10), units = "days", reverse = TRUE)
```

這些過濾方式分別適合：

- 只看某段週期內的 cases
- 只看最慢或最快的一部分案例
- 挑出超過 SLA 的超時案例
- 反向排除特定區間

除了 case duration，也能依頻率過濾：

```r
filter_activity_frequency(log, interval = c(50, 100))
filter_activity_frequency(log, percentage = 0.8)
filter_resource_frequency(log, interval = c(60, 900))
filter_resource_frequency(log, percentage = 0.6)
```

這對大型流程圖很重要，因為不先過濾，畫出來的流程常常只剩噪音。

## Appending Process Metrics Back to Data

一個很實用的 workflow 是把流程指標直接加回原始事件資料：

```r
log %>%
  throughput_time(level = "case", units = "days", append = TRUE)

log %>%
  throughput_time(level = "case", units = "days", append = TRUE) %>%
  mutate(on_time = processing_time_case <= 7)
```

這樣做的好處是：

- 後續可接一般 `dplyr` / `ggplot2` workflow
- 可以把流程指標轉成 business rule，例如 `on_time`
- 更容易和 case-level metadata 合併

除了 throughput，課程也提到還能補上：

- case length
- rework amount
- activity frequency
- resource specialization

## Useful Process Views

除了傳統表格摘要，幾種圖特別適合 process data：

### Activity Presence

```r
activity_presence(otc) %>% plot()
```

用來看哪些活動在流程中經常出現、哪些只出現在部分變體。

### Trace Length

```r
trace_length(otc) %>% plot()
```

適合快速看流程長短是否集中，還是存在很多 unusually long cases。

### Start and End Activities

```r
start_activities(otc, "activity") %>% plot()
end_activities(otc, "activity") %>% plot()
```

這對檢查流程入口與出口是否一致很有幫助。若 start / end activities 很分散，可能代表流程定義鬆散或資料記錄不完整。

### Dotted Chart

```r
otc %>% dotted_chart(x = "relative", sort = "duration")
```

dotted chart 很適合看：

- 各 case 在相對時間軸上的活動分布
- 長流程和短流程的差異
- 哪些活動常卡在某些區段

它不像單一 KPI 那樣壓縮資訊，而是保留 case-level 時間結構。

## A Practical Workflow

如果你拿到 hospital flow、order-to-cash、support tickets 或 claims log，可以照這個順序做：

1. 先確認哪些欄位能形成 event log。
2. 建立 event log object，確認 case / activity / timestamp / resource 對應。
3. 用 `summary()`、`n_cases()`、`n_activities()` 看流程規模。
4. 看 activities 與 traces，理解主流程與變體。
5. 看 resource frequency / resource map，理解組織分工與交接。
6. 用 throughput、trace length、rework 等 metric 找 bottleneck。
7. 視需要用 filtering 聚焦在慢案、少見變體或高風險案例。
8. 把 case-level metric append 回資料，再接一般分析與報表流程。

## Common Mistakes

- 把 event log 當普通 transaction table，忽略順序與 case 結構。
- `case_id`、`activity_id`、`timestamp` 定義不清，導致 trace 錯誤。
- 一開始就畫完整流程圖，結果資訊過載。
- 只看平均 throughput，卻不看 trace variation。
- 看到 resource specialization 就直接下績效結論，忽略角色分工本來就不同。
- 沒先處理 lifecycle / timestamp 問題，就直接做 process metric。
