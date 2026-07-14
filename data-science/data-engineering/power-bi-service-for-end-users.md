# Power BI Service for End Users

`Power BI Service` 對 end user 來說，不是建模工具，而是消費、探索、分享與協作分析內容的入口。

如果 [Power BI Overview](power-bi-overview.md) 比較偏整體平台工作流，這篇比較偏站在 report consumer 或 business user 的角度，理解在 Service 裡實際能做什麼。

## Why It Matters

很多 BI 專案最後失敗，不是因為模型算錯，而是因為最後一哩沒有被用起來。

對 end user 來說，真正重要的通常是：

- 能不能快速找到需要的 dashboard / report
- 能不能在不改壞既有報表的前提下探索資料
- 能不能和其他人共享同一套 insight
- 能不能在重要數字變化時被主動提醒

所以 Service 的價值，不只是 publish 報表，而是把分析內容變成可持續使用的 collaborative surface。

## Desktop vs Service

一個簡化分工可以先記成：

- `Desktop`: authoring
- `Service`: consumption, sharing, distribution

Desktop 比較偏：

- 建模型
- 做轉換
- 編輯 visual

Service 比較偏：

- 瀏覽與互動
- 分享與分發
- workspace 協作
- alerts 與日常使用

每個使用者通常也會有自己的 `My workspace`，比較像個人內容或暫存工作區。  
真正團隊協作與正式分發，通常還是應該回到 shared workspace / app 的脈絡來管理。

## What End Users Usually Value

來源裡反覆出現的 end-user 價值大致可以收斂成：

- user-friendly interface
- anywhere access
- interactive visualizations
- collaboration
- personalization

換句話說，end user 要的不是更多建模選項，而是更低摩擦的分析消費體驗。

## Workspaces vs Apps

這個區分很值得保留，因為很多人會把兩者混在一起。

### Workspaces

`workspaces` 比較像協作製作區。

它通常承載：

- dashboards
- reports
- semantic models
- paginated reports

重點是讓一群人共同建立、維護與管理內容。

另外一個容易忽略但很實務的點是 `workspace contacts`：

- 讓使用者知道這個 workspace 該找誰
- 預設常會落在 workspace admins
- 也可以另外指定聯絡人

這種設定雖然不是分析功能，但對大型組織裡的可維運性很重要。

### Apps

`apps` 比較像分發包。

它的特性更接近：

- 把已整理好的內容打包給較大範圍的 audience
- 可以按不同 audience group 控制誰看到什麼

一個簡化記法：

- workspace 用來共同創作
- app 用來穩定分發

### Organizational Apps vs Template Apps

來源還補了一個有用區分：

- `organizational app`: 發給組織內使用者
- `template app`: 給外部或更通用情境，讓使用者可以接自己的資料

對 notebook 來說，不必背所有產品細節，但值得記住：

- internal distribution 通常先想 organizational app
- 若目標是可重用的 packaged solution，才更像 template app

### Licensing as a Distribution Constraint

Power BI 的分發與協作能力，常會受 license 與 capacity 影響。

比較穩的心法是：

- 需要共同製作或頻繁使用進階功能的人，通常要有較完整的 authoring / collaboration 權限
- 純消費者能否低摩擦存取，常和內容是否放在對應 capacity 上有關

也就是說，license 不是採購細節，而是 distribution design 的一部分。

## Access Permissions

對 end user 來說，workspace permissions 不是治理細節，而是直接決定可做哪些事情。

來源整理的角色可以先粗略記成：

- `Admin`: 管 workspace 本身
- `Member`: 管成員與較高層級協作
- `Contributor`: 能新增或維護部分內容，但不等於全面管理
- `Viewer`: 以瀏覽與互動為主

實務上最重要的不是背定義，而是先弄清楚：

- 我是內容作者、協作者，還是純消費者
- 我需要修改資產，還是只需要看與互動

如果角色與權限對不齊，最常見的結果不是安全更高，而是：

- 使用者找不到該看的內容
- 協作者不能建立該建的資產
- 大家開始用繞路方式分享資料

## Interacting with Reports

Power BI Service 的 end-user 體驗，核心其實是互動，而不是靜態閱讀。

常見互動能力包括：

- slicers
- filters
- drill-down
- drillthrough
- cross-filtering

如果想把這些互動能力拆細看，可以接著讀 [Reports in Power BI](reports-in-power-bi.md)。

## Slicers and Filters

這份課程提到幾種很常見的使用方式：

- `relative date slicer`
- `hierarchical slicer`
- `slicer with a list of options`

以及不同作用範圍的 filter：

- `visual-level filter`
- `page-level filter`
- `report-level filter`

對 end user 來說，這些能力的意義是：

- 把同一份報表切成不同問題視角
- 不必改報表本體，也能縮小問題範圍

## Drill, Cross-Filtering, and Detail Navigation

end user 最常用到的探索能力，通常是：

- `drill-down`: 沿著 hierarchy 往更細層看
- `drillthrough`: 從某個資料點跳到關聯的細節頁
- `cross-filtering`: 點一個 visual，觀察其他 visual 如何一起改變

這三者可以先簡單分工：

- drill-down: 往下展開層級
- drillthrough: 跳到另一個更細的上下文
- cross-filtering: 在同頁比較多個視角

## Explore Pane

`Explore` 很值得留下，因為它代表一種「不改原報表也能試問問題」的使用方式。

它可以先理解成：

- ad-hoc analysis
- 不影響既有 report 的暫時探索空間
- 快速產生基本 visual 或 table

它適合：

- 先試一個想法
- 看某幾個欄位能不能形成有用視角
- 幫未來正式報表先做問題探索

但來源也提醒了幾個限制：

- 它是 temporary workspace
- formatting 能力有限
- 不適合拿來當 final reporting artifact

所以 `Explore` 比較像沙盒，不像正式報表交付物。

## Sharing and Alerts

Power BI Service 的另一個核心能力，是把 insight 主動送到人，而不是等人來找。

### Sharing

分享的真正價值不是轉貼連結，而是：

- 讓 stakeholders 對同一組數字有共同視角
- 降低各自解讀不同版本資料的風險
- 把分析變成可討論、可協作的工作物

實務上，分享不只是一個連結，也可能包含：

- 用 app 做穩定分發
- 直接分享 report
- 讓使用者訂閱固定報表輸出

### Data Alerts

`data alerts` 可以先理解成：

- 對關鍵指標設 threshold
- 達到條件時收到通知

這很適合：

- 監控重要 KPI
- 避免一直手動打開 dashboard
- 讓使用者在數字變化時能更快反應

來源也補了一個務實限制：

- alerts 比較偏特定視覺類型與 threshold-based 通知

所以它適合處理明確的監控訊號，不適合取代完整的分析流程。

### Report Subscriptions

除了 alerts，`report subscriptions` 也很值得保留。

它比較像：

- 定期把報表以 e-mail 形式送給自己或其他人
- 用固定節奏分發同一份內容

這種能力特別適合：

- 使用者不一定會主動登入 Service
- 需要週期性營運摘要
- 想把分析內容嵌進既有溝通節奏

可以把兩者分開記：

- subscription: 定期送
- alert: 事件到了才送

## Endorsement and Discoverability

當組織內開始有很多 datasets、reports、dataflows、apps 時，另一個問題會變成：

- 哪些內容值得信任
- 新使用者要先看哪一份

來源提到的 `endorsement` 很適合解這個問題。

### Promoted vs Certified

一個簡化分法：

- `promoted`: 某份內容被認為有價值，值得更多人注意
- `certified`: 經過更正式的審核或指定流程，可信度更高

這個機制的價值不是多一個 badge，而是降低內容發現成本。  
在報表與模型數量多的組織裡，discoverability 本身就是治理問題。

## Custom Visuals and Marketplace

課程也提到 `visual marketplace`。

對 notebook 來說，可以先保留一個務實結論：

- 標準 visual 不夠表達時，可以考慮 marketplace visuals
- 但它們應該是補充，不應該變成掩蓋資料設計問題的方法

先把問題講清楚，再決定是否真的需要非標準 visual，通常比較穩。

## Practical Heuristics

- 如果內容還在共同製作，先想 workspace；如果要穩定發給較大 audience，先想 app。
- end user 的核心工作通常是互動、探索、分享，不是重做報表。
- `Explore` 適合試想法，不適合取代正式報表。
- 重要 KPI 可以考慮用 alerts，把被動看報表變成主動接收訊號。
- 權限先對齊角色需求，再談協作流程，不然很容易要嘛太開、要嘛太卡。

## Relation to Other Notes

- 如果你想先建立整體 Power BI 工作流，可以先看 [Power BI Overview](power-bi-overview.md)。
- 如果你想理解互動式報表本身的能力，可以接著看 [Reports in Power BI](reports-in-power-bi.md)。
- 如果你想理解報表背後的模型與治理，可以接著看 [Semantic Models and Power BI](semantic-models-and-power-bi.md)。

## Mental Model

一句話總結：

Power BI Service for end users，可以先理解成 `shared consumption + controlled interaction + collaborative distribution` 的分析消費層。
