# Reports in Power BI

在 Power BI 裡，`report` 不是單純一張圖表頁。  
更準確地說，它是一個可以承載多頁、互動、導覽、tooltip、Q&A 與狀態切換的分析介面。

如果 [Report Design in Power BI](report-design-in-power-bi.md) 比較偏 UX 原則，這篇比較偏 Power BI report 本身有哪些能力，以及它和 dashboard 的差異在哪裡。

## Reports vs Dashboards

Power BI 很常把 `report` 和 `dashboard` 放在一起談，但它們解決的問題不完全相同。

可以先這樣理解：

- `dashboard`: 單頁、快速、偏監控與摘要
- `report`: 多頁、互動、偏探索與分析流程

課程裡對兩者的對比很清楚：

- dashboard 常用來看 critical business / operational metrics
- dashboard 通常較少互動
- report 則更像 application-like experience
- report 可以有 multiple pages 與 interactive functionality

## When to Choose a Dashboard

比較適合 dashboard 的情境通常是：

- 需要 rapid analysis
- 使用者停留時間短
- engagement opportunities 很有限
- 重點是快速知道現在狀況是否正常

這種情境比較像 operational monitoring，而不是深入探索。

## When to Choose a Report

比較適合 report 的情境通常是：

- 需要 detailed analysis
- 使用者會主動探索
- 有較好的輸入裝置與較大畫面
- 分析流程需要跨多個頁面或多個互動狀態

換句話說，如果使用者不是只看一眼，而是要一路問下去，通常更像 report 問題。

## Paginated Reports

課程另外提到一種很容易和一般 Power BI report 混淆的東西：`paginated reports`。

它可以先理解成：

- pixel-perfect report
- 更偏 written page
- 通常由 `Power BI Report Builder` 建立

這種報表的重點不是互動探索，而是精準輸出與排版穩定。  
如果需求偏列印、正式文件、固定版面，就比較接近 paginated report，而不是互動式 report。

## A Useful Mental Split

可以先把三者分開記：

- dashboard: 看現在
- interactive report: 問問題
- paginated report: 固定輸出

這樣比較不會把不同需求全塞進同一種 artifact。

## Reports as Structured Navigation

這份課程很強調一件事：  
report 不只是視覺化集合，它也應該有 story structure。

其中一個關鍵觀念是：

- stories benefit from structure
- structured navigation helps tell the story

所以好的 report 通常不是把頁面做完就算，而是讓使用者知道：

- 我現在在哪一層
- 下一步能去哪裡
- 哪些頁面屬於同一段分析脈絡

一個很實用的原則是：

- `one page = one topic`

也就是每一頁最好回答一組相對集中的問題，而不是把不相關的 visuals 隨機攤開。

## Start With an Overview, Then Drill Down

case-study 類報表很適合先用 overview page 開場，再把後續頁面分給不同分析主題。

例如：

- page 1: overall KPI 與 top findings
- page 2: reason breakdown
- page 3: geography or segment analysis
- page 4: deeper diagnostics or action view

這樣的好處是：

- stakeholder 先拿到高層摘要
- analyst 或 power user 還能再往下追
- 整份 report 比較像分析流程，而不是圖表倉庫

## Bookmarks as State

雖然我們已經在報表設計筆記提過 bookmarks，但這份課程補了一個很重要的角度：

- bookmark 不是瀏覽器書籤
- 它是對 Power BI 報表某個 pre-defined state 的捕捉

這個 state 可能包含：

- currently selected page
- filter settings
- slicer selections
- visual selection state
- sort order
- drill location
- visibility of objects

這個清單很有價值，因為它讓你比較精確地理解：bookmark 保存的不是單一畫面，而是一組互動上下文。

## Buttons and Navigation

report 的互動性很大一部分來自 buttons。

Power BI buttons 常見可以做的事情包括：

- drill through to a new page
- navigate to a specific page
- select a bookmark
- navigate to a web URL

這使 report 可以從「多頁文件」變成「有路徑的分析應用」。

## End-User Interactions Inside Reports

除了 navigation，report 的另一個核心價值是讓使用者自己追問資料。

最常見的互動能力包括：

- `drill-down`
- `drillthrough`
- `cross-filtering`
- slicers
- filters

這些能力讓 report 不只是被閱讀，而是被操作。

## Drill-Down vs Drillthrough

這兩個名字很像，但解決的問題不同：

- `drill-down`: 沿著同一個 hierarchy 往更細層看
- `drillthrough`: 帶著某個資料點的上下文跳到另一個細節頁

可以把它們理解成：

- drill-down 是在同一條樹上往下走
- drillthrough 是切到另一個專門看細節的頁面

如果來源資料本來就有層級，例如：

- 年 -> 季 -> 月
- 地區 -> 城市 -> 門市

那 drill-down 通常很自然。  
如果你想看某個點背後的完整情境，drillthrough 往往更合適。

## Cross-Filtering

`cross-filtering` 的價值在於：

- 點一個 visual
- 觀察其他 visuals 如何跟著收斂或重算

它很適合：

- 對照不同維度
- 看某個分群對其他指標的影響
- 快速找關聯，而不必一直重設報表

不過這也再次提醒：互動要被設計。  
如果每個 visual 都互相影響，但使用者不知道為什麼，報表反而會更難用。

換句話說，interactivity 最好服務明確問題，例如：

- 哪個 segment 的 churn 最嚴重
- 哪個 region 對某個 KPI 拉動最大
- 某個 reason category 會連動哪些其他指標

而不是只是展示工具功能。

## Slicers and Filter Scope

對 end user 來說，slicers 與 filters 是最日常的控制元件。

來源裡提到幾種常見 slicer：

- `relative date slicer`
- `hierarchical slicer`
- list-based slicer

也提到三種常見 filter scope：

- `visual-level filter`
- `page-level filter`
- `report-level filter`

這些能力合在一起的價值是：

- 同一份報表可以被不同角色重複使用
- 使用者可以自己縮小問題，而不必一直回頭找報表作者

## Explore as a Safe Sandbox

對 end user 而言，`Explore` 是一個很實用的補充能力。

它比較像：

- 不改壞既有 report 的 ad-hoc analysis
- 快速試資料欄位與基本 visual
- 幫正式報表前的問題探索做前哨

但要記得它的邊界：

- 它是 temporary
- formatting 能力有限
- 不適合當 final report

所以比較好的定位是：

- `report`: 穩定交付物
- `Explore`: 安全的試算與試問空間

## Navigator

課程提到 `Navigator` 是一個很實用的 built-in capability。

它的好處包括：

- 可以依 pages 或 bookmarks 自動建立導覽
- page navigator 會和 report pages 自動同步
- button title 會跟 page display name 對齊
- 順序會依你定義的頁面順序更新

這很適合用來降低手動維護導航按鈕的成本。

## Custom Tooltips

Power BI report 還有一種常被低估的能力：`custom tooltips`。

可以先把它理解成：

- 一個在 mouse-over 時出現的 tooltip page
- 可以做 item tooltip
- 也可以做 help tooltip
- 本身不是 interactive

它的價值在於：  
你不必把所有輔助資訊直接塞進主畫面，而可以在需要時才顯示補充上下文。

這其實和 progressive disclosure 很一致。

## Button States and Styling

按鈕不只是功能元件，也有狀態設計。

課程整理的四種 button states 是：

- default
- on hover
- on press
- disabled

這些狀態可以影響：

- text
- icon
- outline
- fill

這讓報表的互動提示更明確，也讓使用者更容易知道哪些元件可點、已選、或暫時不可用。

## Unicode, Symbols, and Small UI Signals

課程有提到 `Unicode symbols and emoji`。  
對 notebook 來說，不必把它當主軸，但值得保留一個設計提醒：

- 報表有時可以用簡單符號提升辨識性
- 但符號應該輔助語意，而不是取代語意

所以這類元素適合當作 lightweight cue，而不應該變成整個報表資訊編碼的核心。

## Q&A in Reports

這個項目最值得另外留下來的部分，是 `Q&A`。

Power BI 的 Q&A 可以先理解成：

- 讓使用者用自然語言問資料
- 系統再嘗試生成對應 visual

常見能力包括：

- natural language queries
- auto-complete
- spelling corrections
- preview answers
- 提示哪些字詞它不理解

## How Q&A Works

Q&A 的基本模式是：

- 直接用 column 或 measure name 提問
- 用 `by`、`grouped by`、`where` 等語句表達 grouping 與 filtering

像這樣的問題：

- `Actual Amount by Cost Center grouped by Date`

系統會讀取 query，然後決定適合的 visual。

這件事的關鍵不是 NLP 多神奇，而是：

- model 命名要夠清楚
- measure 與欄位語意要夠 business-friendly
- synonyms 要被妥善管理

## Requesting a Specific Visual

Q&A 還能用 `as {visual}` 指定想要的圖表類型，例如：

- `as table`
- `as treemap`
- `as pie chart`

但要注意：

- 對 visual 的控制仍有限
- 它更像快速生成入口
- 之後仍可轉成一般 visual 再細調

所以 Q&A 比較像 accelerate exploration，而不是完整取代報表作者。

## Synonyms and Teach Q&A

Q&A 能不能好用，很大一部分取決於語意維護。

來源裡特別提到：

- 可以為同一欄位定義 multiple terms
- 可用 suggested values，也可手動定義
- 不要讓 synonyms 重疊

另外 `Teach Q&A` 的角度也很實用：

- nouns 比較像 data fields
- adjectives 比較像 filters

這提醒我們：Q&A 不是隨便加別名而已，而是在管理使用者會怎麼用語言碰資料。

## Making Q&A Work Better

要讓 Q&A 更穩，這幾點很重要：

- 欄位與 measures 命名要 business-friendly
- 不要用太技術或太縮寫的名稱
- 適度建立 terms 與 synonyms
- 可以提供 sample questions

例如：

- `Actual Amount` 通常就比 `amt_act` 好很多

Q&A 的可用性，最後還是回到 semantic model 的可理解性。

## Practical Heuristics

- 想要快速監控時，先想 dashboard；想讓使用者一路探索時，先想 report。
- 若需求偏列印、固定版面或精準輸出，通常更像 paginated report。
- bookmark 保存的是一組狀態，不只是頁面快照。
- drill-down、drillthrough、cross-filtering 各自解不同問題，不要混成同一種互動。
- Navigator 很適合用來維持多頁 report 的結構一致性。
- slicer 與 filter scope 越清楚，end user 越能自己追問題。
- custom tooltip 適合放輔助上下文，不適合承擔主要互動流程。
- `Explore` 適合探索，不適合拿來取代正式報表交付。
- 想讓 Q&A 好用，先把 model 的命名與 synonyms 管好。

## Relation to Other Notes

- 如果你想看報表層的互動與 UX 心法，可以先看 [Report Design in Power BI](report-design-in-power-bi.md)。
- 如果你想從消費者角度理解 Service 內的使用方式，可以接著看 [Power BI Service for End Users](power-bi-service-for-end-users.md)。
- 如果你想看報表背後的模型與 relationships，可以接著看 [Semantic Models and Power BI](semantic-models-and-power-bi.md)。
- 如果你想看報表指標怎麼被 measures 與 context 驅動，可以接著看 [DAX in Power BI](dax-in-power-bi.md)。

## Mental Model

一句話總結：

Power BI 的 reports，可以先理解成用 `multi-page interaction + stateful navigation + controlled exploration + semantic querying` 把資料模型包成可探索的分析應用。
