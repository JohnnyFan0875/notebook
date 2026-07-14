# Semantic Models and Power BI

如果你想先建立 Power BI 平台本身的基本工作流，再回來看 semantic layer，可以先看 [Power BI Overview](power-bi-overview.md)。

## Why a Semantic Layer Exists

資料被擷取、清理、落地之後，還不代表分析者就能直接安全地使用它。

semantic model 的角色，是把底層資料整理成：

- 比較容易理解的 business-facing structure
- 可建立 relationships 的分析模型
- 能被 Power BI 或其他 BI 工具穩定消費的語意層

可以把它理解成：semantic layer 站在 raw tables 和最終報表之間，負責把技術性資料結構轉成較適合分析的邏輯資料表示。

## What a Semantic Model Does

semantic model 常見功能包括：

- 簡化複雜資料結構
- 建立跨表 relationships
- 讓 measures、filters、hierarchies 更容易重複使用
- 把權限與資料可見性控制放到報表層之前

如果沒有這一層，很多報表雖然也能做出來，但會變成每一份報表都各自重做邏輯，維護成本很快失控。

## Lakehouse, Warehouse, and Auto-Creation

在像 Microsoft Fabric 這類平台裡，semantic model 常能和 lakehouse 或 warehouse 更直接連動。

課程裡強調的一個重點是：

- semantic model 可以在建立 lakehouse / warehouse 時被自動建立

這代表語意層不再只是 BI 工具外掛，而是更早就進入資料平台設計的一部分。

## Relationships Matter

semantic model 最重要的工作之一，是把多張表之間的欄位關係明確化。

常見做法是：

- 找出 matching columns
- 用這些欄位建立 relationships
- 讓不同 tables 的資料能被一起分析

這一步的價值不只是 join 比較方便，而是讓報表與下游分析不必每次都重新猜資料該怎麼拼。

在 Power BI 實務裡，這通常代表：

- fact table 與 dimension table 的角色要清楚
- key 要能穩定建立 relationships
- 模型形狀最好盡量接近 star schema
- cross-filtering direction 要盡量可預期

不是所有可連的表都應該直接連上去；過度複雜的關聯網路會讓 filter propagation 和報表解讀都更難。

### Filter Direction

relationship 不只是「有沒有連上」，還包含 filter 如何傳播。

在 Power BI 裡，最常見的穩定做法是：

- filter 從 dimension 傳到 fact
- 盡量維持 single-direction relationships

這樣的好處是：

- filter path 較容易推理
- 報表結果較不容易出現意外傳播
- model behavior 更接近 star schema 的直覺

bi-directional filtering 並不是不能用，但它通常應該被視為例外，而不是預設。

### Bi-Directional Filtering as an Exception

bi-directional filtering 最常被拿來處理的一種需求，是：

- 只顯示與目前情境相關的 slicer entries

但它也會帶來代價：

- relationship path 更容易變複雜
- 兩表之間若出現多條路徑，模型推理會變難
- many-to-many 或複雜維度網路時更容易拖慢效能

所以比較穩的心法通常是：

- 先假設 single-direction
- 只有在特定互動需求真的需要時，才評估 bi-directional
- 如果可以用 measure 或更明確的邏輯替代，就盡量不要用雙向關係當萬用解法

### Multiple Relationships and Role Semantics

有些模型會在同兩張表之間需要多個 relationships，例如：

- order date
- ship date
- delivery date

在 Power BI 裡，這通常代表：

- 可以建立多個 relationships
- 但同時間通常只會有一個 active relationship

這個限制其實是好事，因為它迫使模型把主要語意先講清楚，而不是讓多條關係同時模糊地生效。

### Hierarchies Depend on Model Clarity

semantic model 也常負責提供 hierarchies，讓報表可以更自然地 drill down。

常見例子：

- year -> quarter -> month
- country -> state -> city
- category -> subcategory -> product

如果 hierarchy 的層級在業務世界本來就存在，通常可以把它視為 natural hierarchy。  
如果只是為了分析操作方便而組出多層切法，則更接近 artificial hierarchy。

兩者都能用，但前者通常比較容易被使用者理解。

## Reports Depend on Model Quality

Power BI 報表看起來像是視覺化問題，但實際上常受 semantic model 品質支配。

如果模型本身：

- relationships 不清楚
- 欄位命名不穩定
- measures 到處散落
- 權限邏輯沒有先設計

那報表再漂亮也很難長期維護。

所以「有效的 Power BI 報表」通常不是從畫圖開始，而是先從 model design 開始。

這也是為什麼在 Power BI 世界裡，常常會說：

- 好的 report 往往是好的 model 的結果
- 不好的 model 會把簡單視覺化也變成維護噩夢

## Security in Semantic Models

semantic layer 的另一個核心角色，是把資料安全控制推進到分析消費層。

課程特別提到兩種常見控制方式：

- `RLS`: Row-Level Security
- `OLS`: Object-Level Security

### Row-Level Security

RLS 會限制使用者能看到哪些 rows。

它適合：

- 區域別資料隔離
- 業務單位各看各的數據
- 同一份模型服務多種角色，但每個角色只能看部分資料

在 Power BI / semantic model 世界裡，RLS 常透過角色與 DAX filters 配置。

如果需要做 dynamic RLS，常見做法是讓 DAX 依登入者身分決定可見資料範圍。  
來源內容特別提到 `USERPRINCIPALNAME()`：

- 會回傳使用者的 `UPN`
- 通常可視為 email address
- 在 Power BI Desktop 與 Service 之間的行為較一致

這讓模型可以依使用者身分套用不同過濾條件，形成 personalized dashboards，而不必為每個人各做一份報表。

### RLS Depends on Service-Side Assignment

課程裡還補了一個很重要的實務分工：

- roles 常在 `Power BI Desktop` 定義
- 使用者或群組的指派常在 `Power BI Service` 完成

這提醒我們，RLS 不是單純的 DAX 技巧，而是：

- model design
- service deployment
- user/group management

一起成立才會真的生效。

### RLS Limitations

RLS 雖然很重要，但不是零成本能力。

來源裡提到兩個很值得保留的限制：

- 額外的 row filtering 可能拖慢查詢效能
- 擁有較高資料集寫入 / 修改權限的人，通常不應被視為 RLS 的保護對象

所以比較穩的心法是：

- 用 RLS 保護 consumer-facing access
- 不要把它當成可以約束高權限作者的萬能機制

### Object-Level Security

OLS 會限制整個 object 的存取，例如：

- 某張 table
- 某個 column

它適合拿來保護比較敏感的欄位或結構，而不只是把資料列做過濾。

### Dataset Permissions

在 Service 端，semantic model 還有一層很實務的 `dataset permissions`。

來源把它拆成幾個常見能力：

- `Read`: 可用既有內容讀資料，但不代表能自由探索或發現所有相依內容
- `Build`: 可基於 dataset 建新內容
- `Reshare`: 可把存取再分享出去
- `Write`: 可修改 dataset metadata

這個拆法很有價值，因為它提醒我們：

- 看得到報表
- 能不能基於同一個模型再做新內容
- 能不能把權限再擴散給別人

其實是三件不同的事。

### Workspace Role and Dataset Capability Are Related but Not Identical

workspace role 常會影響 dataset permission 的上限，但兩者不是同一句話。

實務上最好分開想：

- workspace role: 你在協作容器裡能做什麼
- dataset permission: 你對某個 semantic model 能做什麼

這樣比較不容易因為「他看得到 report」就誤以為「他也能 build 新報表」。

### Sensitivity Labels

如果 semantic model 或報表承載敏感資訊，還可以再往上加一層 `sensitivity labels`。

這層的意義通常是：

- 標示內容敏感程度
- 配合組織的合規與保護流程
- 在匯出、分享或後續流通時保留保護語意

對 notebook 來說，最重要的不是操作步驟，而是先記住：

- security 不只是在 query 時過濾 rows
- 還包含內容離開報表之後，能不能被適當標示與保護

## Why This Matters for Data Engineering

semantic model 看起來比較像 BI 或 analytics engineering 的工作，但它和 data engineering 很有關係，因為：

- 上游 schema 設計會直接影響 relationship 建模
- 權限模型需要和 storage / governance 一起思考
- 若 ingestion 與 warehouse 建構不穩，semantic layer 也很難穩

換句話說，semantic layer 不是資料工程的外部世界，而是資料供應鏈的最後一段整理與控制。

## Practical Design Questions

在建立 semantic model 前，先回答這些問題通常很有幫助：

- 哪些 tables 應該直接暴露給報表使用
- 哪些欄位只是工程用途，不該出現在分析層
- relationships 應該如何定義才最符合 business logic
- 是否需要依角色做 row filtering
- 是否有敏感欄位需要用 OLS 隱藏

## Practical Reminders

- semantic model 的價值是降低報表重工，不只是多一層抽象。
- relationship 錯了，整份報表的數字都可能看起來合理卻完全錯。
- single-direction relationships 通常比雙向關係更穩，也更接近 star schema 的設計直覺。
- 若模型需要很多例外 filter paths，通常該先回頭檢查 schema 與 dimension 設計，而不是一直疊 relationship 設定。
- RLS 和 OLS 應該被當成分析層治理的一部分，而不是最後才補上的權限開關。
- 如果 lakehouse、warehouse、semantic model 是同一平台內協作，越早把命名、欄位與安全邊界講清楚，後面越省事。
- 在 Power BI 中，能用 star schema 清楚表達的模型，通常比讓 dimension 彼此互連的模型更穩。

[Back to Data Engineering](README.md)
