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

## 與其他章節的關係

- [Data Engineering](../data-engineering/README.md): 決定 event log 是否有穩定的 case id、activity、timestamp 與 resource 欄位。
- [Statistics](../statistics/README.md): 幫助你判讀等待時間、分布偏態、異常 case 與不確定性。
- [Operations Research](../operations-research/README.md): 當你要把流程觀察轉成排程、容量或配置決策時，這兩章會接起來。
- [Network Analysis](../network-analysis/README.md): 若流程被轉成 handoff network 或 activity transition graph，兩章的視角會互補。

## 實務提醒

- 沒有一致的 case 定義時，後面的 trace、throughput 與 bottleneck 分析都會不可靠。
- 很多流程問題不是演算法抓不到，而是事件資料缺欄、時間戳不準或 resource naming 不一致。
- process analytics 通常先回答「發生了什麼」，再進一步問「該怎麼改善」。
