[Data Science](../README.md) › [應用領域](README.md) › 流程探勘

# 流程探勘 (Process Mining)

流程探勘分析的是 **event log**：每一列是「某個 case 在某個時間做了某個 activity（由某個 resource 執行）」。問題不是單筆資料的值，而是一個 case 從開始到結束實際經過哪些步驟、花多久、在哪裡出現變異與交接。

| 概念 | 意義 | 醫療流程中的對應 |
| --- | --- | --- |
| Case | 一個流程實例 | 一次就診 / 住院（encounter），或一位病人 |
| Activity | 流程中的一步 | 掛號、檢傷、抽血、影像、會診、入院、出院 |
| Timestamp | 事件時間 | EHR 醫令、報告、護理紀錄的時間戳 |
| Resource | 誰執行 | 科別、醫師、護理站、檢驗室 |
| Lifecycle | 開始 / 完成等狀態 | 檢驗開立 → 採檢 → 報告 |
| Trace / variant | 一個 case 經過的活動序列；相同序列的 case 屬於同一 variant | 病人路徑 (patient pathway)；與臨床指引比對 |
| Throughput time | case 從開始到結束的時間 | 急診滯留時間、door-to-needle time、住院天數 |

醫療是最典型的應用：EHR 本身就是 event log。實驗室流程（檢體收件 → 萃取 → 建庫 → 定序 → 分析 → 報告）也是。

> 醫療 event log 的時間戳常是「紀錄時間」而非「發生時間」，同一時刻大量批次寫入很常見；分析等待時間前先確認時間戳語意。等待時間多半右偏，用中位數與分位數描述，必要時以 [存活分析](../statistics/survival-analysis/README.md) 處理尚未結束的 case（設限）。

| 問題 | 方法 |
| --- | --- |
| 流程在真實資料中實際長什麼樣？ | process map、trace 分析 |
| 最常見的路徑是什麼？變異多大？ | variant 頻率 |
| 哪些 case 花最久？哪些活動最常重工？ | throughput time、重複活動 |
| 工作怎麼在 resource 之間交接？ | resource map、handover network |

工具：R `bupaR`（本篇範例）、Python `pm4py`。

## 建立 event log

原始資料是一張表，要明確指定哪些欄位扮演流程角色；這一步定義錯，後面的 trace、throughput 與 resource 分析都會一起偏掉。

```r
library(bupaR)

log <- event_data |>
  eventlog(
    case_id = "patient",
    activity_id = "handling",
    activity_instance_id = "handling_id",     # 同一活動的一次執行（含開始與完成兩筆事件）
    lifecycle_id = "registration_type",       # start / complete
    timestamp = "time",
    resource_id = "employee"
  )
# 每列只有一個時間點（沒有 start / complete）時，可用 simple_eventlog() / activitylog()

summary(log)                                  # case 數、activity 數、event 數、時間範圍
n_cases(log); n_activities(log)
```

```python
# Python：pm4py
import pm4py
df = pm4py.format_dataframe(df, case_id="patient", activity_key="handling", timestamp_key="time")
variants = pm4py.get_variants(df)
dfg, start, end = pm4py.discover_dfg(df)      # directly-follows graph
```

## 活動與 trace

```r
activities(log)              # absolute_frequency、relative_frequency：哪些是主幹、哪些是例外步驟
traces(log)                  # 每種 variant 與其頻率
trace_explorer(log, coverage = 0.8)   # 涵蓋 80% case 的最常見 variants
process_map(log)             # directly-follows 流程圖
```

活動頻率只回答「常不常出現」；trace 才回答「怎麼組成流程」。trace 分布非常分散代表流程變異高（醫療流程常如此），聚合時要更小心，先過濾到主要 variants 再畫流程圖，否則只剩一團義大利麵。

## Resource 與組織分析

```r
resources(log)                                              # 每個 resource 的工作量
resource_frequency(log, level = "resource-activity") |> plot()   # 誰執行哪些活動
resource_map(log)                                           # 工作從誰交到誰（handover network）
```

可以看出誰高度專精於少數活動、某些活動是否只靠少數人支撐（人員離開的風險）。看到專精程度差異時，不要直接下績效結論：角色分工本來就不同。handover network 可以接著用 [網路分析](../network-analysis/README.md) 的方法分析。

## 分析層級

很多 bupaR 指標都可以在不同粒度計算，同一個指標在不同層級回答不同問題：

```r
throughput_time(log, level = "log")              # 整體分布
throughput_time(log, level = "case")             # 每個 case
processing_time(log, level = "resource")         # 組織績效視角
number_of_repetitions(log, level = "activity")   # 重工
# 其他 level："trace"、"activity"、"resource-activity"
```

## 過濾

不先過濾，大型流程圖通常只剩雜訊。

```r
filter_throughput_time(log, interval = c(5, NA), units = "days")    # 超過 SLA 的慢案
filter_throughput_time(log, percentage = 0.5)                       # 最快的 50%
filter_throughput_time(log, interval = c(5, 10), units = "days", reverse = TRUE)  # 排除區間
filter_activity_frequency(log, percentage = 0.8)                    # 涵蓋 80% 事件的活動
filter_resource_frequency(log, interval = c(60, 900))
filter_trace_frequency(log, percentage = 0.8)                       # 主要 variants
```

## 把流程指標加回資料

```r
case_metrics <- log |>
  throughput_time(level = "case", units = "days", append = TRUE) |>
  mutate(on_time = throughput_time_case <= 7)
```

`append = TRUE` 把 case 層級指標接回事件資料，之後可以接一般 `dplyr` / `ggplot2` 分析、轉成業務規則（是否準時），或與 case metadata（病人特徵、科別）合併建模。append 後的欄名依指標而定（例如 `throughput_time_case`），用 `names()` 確認。

## 流程視覺化

| 圖 | 函式 | 看什麼 |
| --- | --- | --- |
| Activity presence | `activity_presence(log) \|> plot()` | 哪些活動幾乎每個 case 都有、哪些只在部分 variants |
| Trace length | `trace_length(log) \|> plot()` | 流程長度是否集中，有沒有異常長的 case |
| 起點與終點 | `start_activities(log, "activity")`、`end_activities(log, "activity")` | 入口與出口是否一致；很分散代表流程定義鬆散或紀錄不完整 |
| Dotted chart | `dotted_chart(log, x = "relative", sort = "duration")` | 每個 case 在相對時間軸上的活動分布，哪些活動卡在某些時段 |
| Process map | `process_map(log, performance(median, "hours"))` | 流程結構與活動間的等待時間 |

## 工作流程

1. 確認哪些欄位能組成 event log（case、activity、timestamp、resource、lifecycle）
2. 建立 event log 物件，確認欄位對應
3. 看規模：case、活動、事件數、時間範圍
4. 看活動與 trace，理解主流程與變異
5. 看 resource frequency 與 resource map，理解分工與交接
6. 用 throughput、trace length、重工等指標找瓶頸
7. 過濾聚焦在慢案、少見 variants 或高風險 case
8. 把 case 層級指標加回資料，接一般分析與報表；改善配置問題可接 [最佳化](optimization.md)

## 常見錯誤

| 錯誤 | 後果 |
| --- | --- |
| 把 event log 當普通交易表 | 忽略順序與 case 結構 |
| case / activity / timestamp 定義不清 | trace 錯誤 |
| 時間戳是紀錄時間卻當成發生時間 | 等待時間失真 |
| 一開始就畫完整流程圖 | 資訊過載 |
| 只看平均 throughput | 右偏分布被少數極端 case 拉高，也看不到 variant 差異 |
| 未完成的 case 直接算 throughput | 低估時間（設限問題） |
