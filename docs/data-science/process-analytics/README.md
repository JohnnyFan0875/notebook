# Process Analytics

這個模組整理的是 event log 與流程資料的分析方式。重點不是單筆 transaction 本身，而是很多事件串起來之後，整個流程如何運作、在哪裡變慢、哪些變體最常出現，以及工作如何在不同角色之間流動。

Key point: process analytics 問的不是「某一筆資料值是多少」，而是「一個 case 從開始到結束，實際經過了哪些步驟、花了多久、由誰執行、又在哪裡出現變異」。

## Topics

- [Event Logs and Process Analytics in R](event-logs-and-process-analytics-in-r.md)

## 這個模組回答什麼問題

- 一個 business process 在真實資料裡實際長什麼樣子？
- 最常見的 trace 是什麼？流程變異有多大？
- 哪些 case 花最久？哪些活動最常重工？
- 工作是如何在不同 resource 之間交接的？

## 建議閱讀順序

1. 先看 [Data Engineering](../data-engineering/README.md)，理解 event log 是怎麼被收集與整理出來的。
2. 再看 [Data Manipulation and EDA](../data-manipulation-and-eda/README.md)，建立對時間欄位、缺值與資料品質的基本敏感度。
3. 再看 [Event Logs and Process Analytics in R](event-logs-and-process-analytics-in-r.md)，建立 case、activity、trace、resource 與 throughput 的整體 workflow。
4. 如果之後想從「現在流程如何運作」走向「應該怎麼改善」，再接 [Operations Research](../operations-research/README.md)。
