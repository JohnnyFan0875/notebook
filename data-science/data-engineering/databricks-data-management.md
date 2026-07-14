# Databricks Data Management

在 Databricks 裡，資料管理不只是把資料存進 Delta table。真正的工作通常還包括：

- 決定 table 由誰管理生命周期
- 決定資料能不能回看歷史版本
- 決定哪些資產該做成 view
- 決定誰能看、誰能改、誰能擁有敏感資料

如果 [Databricks Foundations](databricks-foundations.md) 比較偏平台心智模型，這篇更偏向資料資產落地後的管理面。

## Delta Lake as a Management Layer

Delta Lake 的價值不只在效能，也在於它讓 table 更容易被長期管理。

這門課整理出的幾個核心特性是：

- ACID transactions
- transaction log
- schema enforcement
- time travel
- 同時支援 batch 與 streaming processing

這些能力合在一起，讓 Delta table 不只是檔案集合，而是更像一個可被治理、可被更新、可被追溯的 data asset。

## Time Travel and Historical Review

`time travel` 是 Delta 很實用的一個能力，因為它讓團隊可以回看舊版本資料。

這在實務上很有價值，因為它支援：

- historical review
- 追查資料在某次更新前後的差異
- debug pipeline 錯誤或意外覆寫
- 回答「當時看到的資料是什麼」

如果資料平台不能回看歷史，很多資料品質問題只能靠猜；time travel 讓這件事可驗證得多。

## Unified Batch and Streaming Thinking

課程也強調 Delta 可以同時支援 batch 和 streaming workflows。

這代表團隊不需要為了不同處理模式維護完全不同的 storage mental model。從管理角度看，這有幾個好處：

- 減少重複資料管線
- 降低處理流程分裂的複雜度
- 讓同一份 data asset 能同時服務不同更新節奏

## Table Persistence

一個很容易被忽略，但其實非常重要的概念是 `table persistence`。

它影響的是：

- 資料實際存在哪裡
- table 被刪掉時資料會不會跟著刪
- lifecycle 由平台管還是由團隊自己管
- 後續維運與合規責任落在哪一側

Databricks 課程裡把它先分成兩類：

- `managed tables`
- `unmanaged tables`

## Managed vs. Unmanaged Tables

### Managed Tables

`managed table` 比較像由 Databricks 幫你管理資料位置與生命周期。

課程裡的高層特點包括：

- Databricks 管 data location 與 lifecycle
- 刪掉 table 時，資料通常也跟著刪除
- 適合比較簡單、集中式的管理模式

它的優點是方便，但也代表你要接受平台對 lifecycle 的更高參與度。

### Unmanaged Tables

`unmanaged table` 則比較接近團隊自己控制底層儲存位置與生命周期。

課程裡提到的重點包括：

- 採較 decentralised 的管理方式
- 團隊自行控制 data storage location 與 lifecycle
- 刪掉 table definition 不一定會刪除底層資料
- 比較適合 custom storage 或 compliance requirements

它的彈性更高，但也意味著要承擔更多治理與維運責任。

### Practical Tradeoff

可以用這個方式快速判斷：

- 想要簡化管理、讓平台幫忙承接更多 lifecycle 工作時，managed table 通常更自然
- 已經有既定儲存規則、跨系統共享需求或合規限制時，unmanaged table 往往更合適

關鍵不是哪一種永遠比較好，而是 ownership 和 lifecycle 該放在哪一邊。

## Databases, Tables, and Organizational Structure

課程裡也提醒一件很基本但很重要的事：資料結構如果一開始沒整理好，後面治理成本會迅速上升。

在 Databricks 裡，常見做法會先把資料放進有組織的層級，例如：

- database / schema 用來分組相關 tables
- tables 保存主要結構化資料
- 之後再根據需要建立 views 或更高階消費層

這件事聽起來很基本，但它直接影響：

- 資料能不能被快速找到
- 權限能不能被合理地套用
- 團隊能不能理解哪些表屬於同一主題

## Views and Temporary Views

這門課還有一個很值得留下來的重點：不要把所有資料邏輯都直接暴露在 base tables 上。

`view` 的價值通常包括：

- 提供較乾淨、較穩定的查詢入口
- 隱藏不必要的複雜度
- 讓多個使用者共用一致的 business logic

而 `temp view` 則比較適合：

- 暫時性的分析流程
- 中間轉換步驟
- notebook / session 內部工作

可以把它們理解成：

- table 比較像主要資料資產
- persistent view 比較像共享邏輯介面
- temp view 比較像短生命週期的工作台中介層

## Data Explorer and Asset Governance

課程裡用 `Data Explorer` 來說明 Databricks 中資料探索與治理入口的價值。

它的重要性在於：

- 快速找到並管理 table assets
- 直接做權限治理
- 預覽與檢查敏感資料
- 指派 ownership

這種入口的價值不是只有「UI 好用」，而是讓資料治理不必完全依賴每個人各自記住 table 名稱與權限細節。

## Access Rights and Access Levels

資料管理一定會碰到 access control，而這門課有一個很好的提醒：權限不是只有「能不能進去」，而是 access level 的差異會改變風險。

高層來看：

- `read-only` 適合只需要查看資料的角色
- 更高權限則可能包含更新、維護或管理能力

這種區分很重要，因為許多資料風險不是來自外部入侵，而是內部權限過大。

實務上至少要定期檢查：

- 誰只需要看
- 誰真的需要改
- 誰應該是 asset owner

## Sensitive Data and PII

課程也特別拉出 `PII`。

這提醒我們：Databricks 裡的資料治理不是純技術問題，也常直接連到法規與產業要求。

幾個重點包括：

- PII 會因產業與地區規範不同而有不同風險
- healthcare、finance、government 等情境通常要求更嚴格
- 資料儲存、存取與分享都可能受法規約束
- 權限與 ownership 設計必須跟敏感度一起考慮

換句話說，敏感資料不只是「一張重要表」，而是整個 access model、audit 與 lifecycle 都要更謹慎。

## Practical Reminders

- Delta 的價值不只是快，而是更容易支援一致性、追溯與長期維護。
- managed table 和 unmanaged table 的差異，本質上是 ownership 與 lifecycle 的差異。
- 如果 view strategy 不清楚，團隊很容易直接把 base tables 當最終消費層，之後會越來越亂。
- 權限治理要關注 access level，而不只是有沒有 permission。
- PII 與敏感資料治理不該等到資料進平台後才補想，最好在 asset 設計時就一起決定 ownership、visibility 與 retention。

[Back to Data Engineering](README.md)
