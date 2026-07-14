# Microsoft Fabric Environment Design and Deployment

## Why This Topic Matters

當資料平台開始同時承載 lakehouse、warehouse、semantic model、report 與 pipeline 時，問題往往不再只是「資料有沒有進來」，而是：

- 誰能進哪個 workspace
- 哪些 item 應該被一起管理
- compute capacity 是否足夠
- 變更要怎麼安全地從開發推到正式環境
- Git 與 deployment 流程能不能支援多人協作

Microsoft Fabric 把這些事情放在同一個平台裡，所以 environment design 會直接影響安全性、協作成本與發布穩定度。

## The Fabric Hierarchy

Fabric 可以先用一個由上而下的層級來理解：

1. `Tenant`: 組織層級的管理邊界
2. `Capacity`: 提供計算資源的層
3. `Workspace`: 團隊協作與管理 items 的容器
4. `Item`: 真正被建立與使用的物件，例如 reports、lakehouses、warehouses、notebooks

這些層不是嚴格一對一關係，但這個結構很有用，因為它提醒我們：權限、成本與變更管理不只發生在單一檔案或資料表上。

## Workspace as the Operational Boundary

workspace 是 Fabric 裡非常實務的一層，因為它通常同時承擔：

- 團隊協作邊界
- 權限分派邊界
- item 組織邊界
- 部分 lifecycle 管理邊界

可以把 workspace 想成 analytics project 的工作區，而不是單純資料夾。當 lakehouse、warehouse、semantic model、report 被放進同一個 workspace 時，團隊其實也在定義哪些資產應該被一起協作與一起治理。

## Capacity Is a Design Decision, Not Just a Billing Choice

Fabric `capacity` 不只是授權或費用問題，它也會影響：

- 可承受的計算負載
- 併發能力
- refresh 與查詢體驗
- 壓力測試與上線風險

課程裡提到一個很實務的做法：先評估預期活動量，再透過試用或 metrics app 觀察 Capacity Units 的使用情況，而不是只憑直覺選 SKU。

## The Fabric Capacity Metrics App

若平台提供像 `Fabric Capacity Metrics App` 這類工具，資料工程團隊可以把它視為容量治理的一部分。

它的價值在於：

- 觀察 resource consumption
- 確認 capacity 是否被過度使用
- 為擴容、授權調整或工作負載分配提供依據

這種監控思維很重要，因為 compute 問題如果只在使用者抱怨報表慢時才被發現，通常已經太晚。

## Git Integration in Fabric

當平台內同時有 notebooks、pipelines、lakehouse artifacts、reports 與 semantic models 時，版本控制就不只是工程偏好，而是多人協作的必要條件。

Fabric 這類平台的 Git integration 主要價值包括：

- 保留變更歷史
- 比較不同版本
- 支援多人協作
- 讓環境變更更接近可審查流程

基本術語可以維持簡單理解：

- `repository`: 被追蹤的專案資料夾
- `commit`: 某個時間點的快照
- `diff`: 版本差異
- `merge`: 合併不同變更

## Why Text-Based Artifacts Matter

課程有一個很好的提醒：在 Fabric 裡，許多元素能被表達成 JSON 或其他文字化檔案，這使它們更適合進 Git。

這件事的關鍵不是檔案格式本身，而是：

- 文字格式比較容易 diff
- review 比較容易
- merge 衝突比較有機會被理解與處理

如果 artifact 只能以 binary file 形式存在，版本控制通常就只剩「有變」和「沒變」，很難真的看懂改了什麼。

## Power BI File Types and Git Friendliness

Power BI 相關檔案就是一個很典型的例子：

| 類型 | 格式 | 是否含資料 | 是否含視覺化 | Git 友善度 |
| --- | --- | --- | --- | --- |
| Power BI Report | `.pbix` | Yes | Yes | 低 |
| Power BI Project | `.pbip` | Yes | Yes | 高 |
| Power BI Template | `.pbit` | No | Yes | 高 |
| Power BI Data Source | `.pbids` | Yes | No | 高 |

其中 `.pbix` 的問題在於它是 binary/compressed 格式，Git 雖然能追版本，但很難清楚比較內容差異。相對地，`.pbip` 這類 project-based 表示法比較適合團隊審查與協作。

## Deployment Stages

Fabric 的 deployment stages 可以先用最基本的三層心智模型理解：

- `Development`: 允許快速迭代與實驗，不直接影響正式使用者
- `Test`: 讓團隊先驗證變更，降低發布風險
- `Production`: 提供穩定版本，並配合較嚴格的安全與變更控制

這種分層的本質，和一般軟體工程的 dev/test/prod 很接近，只是作用對象變成分析資產與資料產品。

## Why Deployment Stages Reduce Risk

deployment stages 的實務價值通常包括：

- 避免 bug 一次影響所有使用者
- 在正式發布前先測試
- 更早發現缺漏或相依問題
- 讓團隊能安全迭代而不直接碰 live environment

對分析平台來說，這尤其重要，因為報表、semantic model 和上游資料物件常有連動，錯誤不一定立刻報錯，反而可能先悄悄變成錯數字。

## Deployment Pipelines and Pairing

deployment pipeline 的價值，是把跨 workspace 的發布流程從手動比對，變成較可控的 promotion 流程。

課程中有兩個很值得記住的概念：

- `paired items`: 目標 stage 中已有對應物件，部署時會以 source 為準覆寫
- `unpaired items`: 目標 stage 中沒有對應物件，部署時會建立新副本

這表示 deployment 不是單純複製貼上，而是帶著對應關係與覆寫語意在運作。若沒有先理解 pairing，部署後看到物件被覆蓋或新建，很容易誤判成系統異常。

## Manual Deploy vs. Managed Promotion

沒有 deployment pipeline 時，團隊常要手動：

1. 在原 workspace 儲存變更
2. 比較兩邊版本
3. 把新變更發布到另一個 workspace
4. 再檢查是否漏東西或出錯

這種流程不是不能做，而是很容易：

- 漏掉某些 item
- 不知道哪些相依物件也要一起移動
- 在壓力下做出不一致操作

deployment pipeline 的真正價值，不只是省步驟，而是讓 promotion 更可預期。

## XMLA Endpoints as an Automation Surface

對 semantic model 與 Power BI 生態來說，`XMLA endpoint` 可以視為一個更進階的自動化與管理介面。

常見用途包括：

- 批次更新多個 semantic models
- 事件驅動的自動 refresh
- tenant 級 refresh/monitoring 檢查
- 壓力測試與模擬活動
- 連接第三方工具或 Python scripts

這代表 semantic layer 並不只是 GUI 管理，也能進入更工程化、自動化的運維模式。

## Monitoring Capacity and Query Pressure

效能問題在 Fabric 裡常不是單一查詢太慢而已，也可能是 capacity 被整體工作負載耗盡。

幾個重要訊號包括：

- capacity usage 是否長期接近上限
- 某些查詢或 refresh 是否特別重
- 特定工作區或 item 是否造成資源爭用

如果平台提供 metrics app、system views 或 query monitoring 能力，這些都值得被當成日常觀測面板，而不是只有出事時才去看。

## Performance Tuning by Workload Type

不同 Fabric item 的效能問題，通常要用不同手法處理。

### Notebooks and Spark Workloads

對 notebooks 來說，常見做法包括：

- 利用 Spark History Server 看 stage 與執行瓶頸
- 用完就停止不需要的 Spark sessions
- join 前先減少進記憶體的資料量

### Dataflows

對 dataflows 來說，常見重點包括：

- 減少昂貴操作，例如不必要的排序
- 盡量利用 query folding，把計算推回來源系統
- 視資料量與複雜度決定是否開啟 staging

這些最佳化的共同原則是：不要讓同一份資料在錯的層反覆做昂貴轉換。

## Scale Up vs. Scale Out

當效能問題已經不是單一查詢邏輯可解時，就要回到容量設計。

- `Scale up`: 提高 SKU，換取更多單一 capacity 的計算能力
- `Scale out`: 把部分 workloads 移到其他 capacity，降低彼此爭用

scale up 比較像把同一台機器變強；scale out 比較像把不同工作負載拆開。

scale out 特別適合：

- production 與 non-production 分離
- 高優先報表與一般分析分離
- 不同業務部門各自隔離負載

## Delta Lake Table Maintenance

Fabric 的 lakehouse 若建立在 Delta Lake 之上，效能與成本也會受到 table maintenance 影響。

常見維護操作包括：

- `OPTIMIZE`: 把許多小 Parquet files 重新整理成較佳檔案大小
- `V-Order`: 在寫入或最佳化時使用額外排序最佳化
- `VACUUM`: 移除超過保留門檻、不再需要的舊檔

這些操作的重點不是「讓表看起來比較乾淨」，而是：

- 改善讀取效率
- 控制 small files 問題
- 降低不必要的 storage 成本

## Why Small Files Hurt

當 lakehouse table 由大量小檔組成時，常見後果包括：

- metadata overhead 增加
- 讀取效率下降
- 壓縮與分布不理想

課程裡提到一個很實務的準則：大型表載入後，通常值得做一次 optimize，把檔案大小整理到比較健康的範圍。

## Practical Automation Hooks

若團隊已經在 Spark notebook 維護 lakehouse tables，這些操作也可以進一步自動化，例如：

- Spark SQL 執行 `OPTIMIZE`
- 用 PySpark / DeltaTable API 做 compaction
- 在 session 層控制 V-Order

重點不是記指令，而是把 maintenance 視為資料平台運維的一部分，而不是等查詢變慢才臨時補救。

## Practical Design Questions

在規劃 Fabric 環境時，可以先問：

- workspace 應該依 team、domain 還是 lifecycle stage 劃分
- 哪些資產需要同時進 Git 與 deployment pipeline
- 哪些報表或 semantic models 還停留在不利 diff 的 binary 格式
- capacity sizing 是依實際負載還是只看授權最低門檻
- 發布流程是否已能在不碰 production 的情況下完成驗證
- 哪些 workload 應該 scale up，哪些應該直接隔離到另一個 capacity
- 哪些 lakehouse tables 需要固定 optimize / vacuum 維護節奏

## Practical Reminders

- workspace 不是單純收納盒，它其實是協作與治理邊界。
- capacity 選型若缺少 usage metrics，很容易變成用感覺買資源。
- 能文字化的 analytics artifact，通常比 binary artifact 更適合長期協作。
- deployment stage 的核心目標不是形式化流程，而是降低錯誤進入 production 的機率。
- paired / unpaired item 的行為要先理解，否則部署結果很容易看起來像「莫名其妙被改掉」。
- 效能問題不一定只能靠加大容量，有時候更有效的是把 workload 放到對的層、對的工具，或拆到不同 capacity。

[Back to Data Engineering](README.md)
