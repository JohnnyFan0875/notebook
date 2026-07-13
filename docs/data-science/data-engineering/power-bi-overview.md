# Power BI Overview

Power BI 可以先理解成一個把資料整理、資料模型、視覺化與分享串起來的 BI 工作流。  
它不只是畫圖工具，而是讓資料從 `dataset -> model -> report -> shared consumption` 走完最後一段。

## Why It Matters

很多團隊以為 BI 工具只是報表外觀問題，但實際上 Power BI 同時碰到：

- data preparation
- data modeling
- interactive reporting
- cloud sharing and distribution

所以它的價值不只是「做 dashboard」，而是把資料轉成能被業務使用的分析介面。

## Core Components

### Power BI Desktop

`Power BI Desktop` 是本機端的分析與報表製作工具。

它通常負責：

- 載入資料
- 使用 Power Query Editor 做清理與轉換
- 建立模型
- 製作報表

可以把它理解成主要的 authoring environment。  
很多資料準備與報表設計工作，都是在 Desktop 完成。

### Power BI Service

`Power BI Service` 是 cloud-based 的分享與分發層。

它比較偏向：

- publish reports
- share and distribute content
- 協作與報表消費

簡單說：

- Desktop 偏建立
- Service 偏發布與使用

如果你想把資料來源、storage mode、gateway 與 refresh 這一層拆開來看，可以接著讀 [Data Connections in Power BI](data-connections-in-power-bi.md)。
如果你想從 report consumer / business user 的角度看 Service，接著讀 [Power BI Service for End Users](power-bi-service-for-end-users.md)。
如果你想看 KPI、scenario analysis、forecasting 與 capital budgeting 指標如何落到 Power BI 報表，接著讀 [Financial Analysis in Power BI](financial-analysis-in-power-bi.md)。
如果你想看 Power BI 和 `pandas` / `seaborn` 怎麼一起工作，可以接著讀 [Python in Power BI](python-in-power-bi.md)。

## A Simple Working Model

Power BI 的入門流程可以先想成：

1. 載入一個或多個 datasets
2. 用 Power Query Editor 清理資料
3. 建立基本 data model
4. 在 Report view 建第一份互動式報表
5. 用 Service 分享給其他人

這個流程看起來簡單，但它已經包含了 BI 工作裡最核心的幾個層次。

## Views in Power BI

課程裡反覆出現的三個 view 很值得先記住：

- `Table view`: 看資料表內容與欄位
- `Model view`: 看 tables 與 relationships
- `Report view`: 建立與編輯視覺化

這三個 view 其實就是三種思考層次：

- data
- structure
- presentation

如果報表有問題，先判斷它是資料內容、模型結構，還是視覺呈現的問題，通常會比較快找到根源。

## Data Preparation Is Part of BI

Power BI 不是把髒資料直接拿來畫圖。

在匯入階段，dataset 常見問題包括：

- 多餘欄位
- 不一致格式
- 多餘字元
- blank rows

所以資料清理不是前置雜事，而是 BI workflow 的一部分。  
Power Query Editor 在這裡扮演的角色，和 Excel / Fabric / Power Query 系列工具是一致的。

如果想把這一層再拆細來看，可以接著讀 [Data Preparation in Power BI](data-preparation-in-power-bi.md)。

## Visualizing Data

Power BI 的核心輸出是互動式視覺化，但真正重要的不是圖表數量，而是：

- 有沒有對應正確問題
- 能不能支援探索
- 篩選與互動是否合理

如果你想把 `report`、`dashboard`、bookmark state、tooltip 與 Q&A 這一層拆開來看，可以接著讀 [Reports in Power BI](reports-in-power-bi.md)。
如果你想把 Service 裡的分享、workspace、app、alerts 與 end-user exploration 拆開來看，可以接著讀 [Power BI Service for End Users](power-bi-service-for-end-users.md)。
如果你想從財務 KPI、what-if modeling 與投資決策指標的角度看報表，接著讀 [Financial Analysis in Power BI](financial-analysis-in-power-bi.md)。
如果你想從時間序列、MoM change、rolling average 與 decomposition tree 的角度看 Power BI，接著讀 [Trend Analysis in Power BI](trend-analysis-in-power-bi.md)。

常見視覺化類型包括：

- table
- matrix
- card
- multi-row card
- gauge chart
- KPI

這些元件各自適合不同任務：

- table / matrix 適合明細與交叉檢視
- card 類適合單一指標摘要
- gauge / KPI 類適合目標與表現差距

## Filtering and Interactivity

Power BI 的強項之一是讓使用者不是只看靜態圖，而是可以互動式地縮小問題範圍。

常見過濾層級有：

- `visual-level filters`
- `page-level filters`
- `report-level filters`

可以把它們理解成不同作用範圍的控制：

- 只影響單一 visual
- 影響同一頁
- 影響整份報表

這個分層很重要，因為很多報表混亂，不是因為圖做不好，而是因為 filter scope 沒設清楚。

### Controlling Interactions

互動不一定越多越好。

有些情況下，你反而要：

- 關掉某些 visual interaction
- 避免使用者誤以為所有圖都應該互相影響

所以 interactivity 應該被設計，不應該只是預設開著。

## Hierarchies and Drill-Down

Power BI 很常搭配：

- hierarchies
- drill-down paths
- sorting

這些能力的價值在於，使用者可以從較高層摘要一路往下看細節，而不是在同一層級塞滿所有資訊。

如果資料本身有天然層次，例如：

- 年 -> 季 -> 月
- 地區 -> 城市 -> 門市
- 類別 -> 子類別 -> 產品

那 hierarchy 和 drill-down 通常會比把全部欄位直接攤平更自然。

## Report Design Is Not the Same as Data Modeling

Power BI 很容易讓人混淆兩件事：

- 建模
- 做報表

這兩者當然相關，但最好分開思考：

- model 決定數字是否可信、欄位是否能重用
- report 決定資訊是否容易被理解與操作

這也是為什麼 Power BI 工作流通常不是從「選哪個圖」開始，而是從資料與模型是否穩開始。

如果你想把報表層的 progressive disclosure、themes、bookmarks 與 mobile layout 拆開來看，可以接著讀 [Report Design in Power BI](report-design-in-power-bi.md)。

## Relation to Semantic Models

如果你想理解 Power BI 背後更偏模型與治理的那一層，可以接著看 [Semantic Models and Power BI](semantic-models-and-power-bi.md)。

兩篇的分工可以簡單記成：

- `Power BI Overview`: 平台元件、工作流、視覺化與互動
- `Semantic Models and Power BI`: relationships、security、semantic layer 與可治理的分析模型

## Practical Heuristics

- 先確認資料與模型正確，再優化圖表外觀。
- 不要把所有互動都打開；先決定哪些 visual 應該互相影響。
- 選圖表前先問：使用者是要看明細、比較、趨勢，還是 KPI。
- filter scope 要明確，不然使用者很容易誤判數字變化原因。
- Desktop 和 Service 最好分工理解，不要把「做報表」和「分享報表」混成同一件事。

## Mental Model

一句話總結：

Power BI 是把資料清理、模型、互動式視覺化與分享交付串成同一條分析消費流程的 BI 平台。
