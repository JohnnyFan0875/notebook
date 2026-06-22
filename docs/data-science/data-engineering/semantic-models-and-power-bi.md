# Semantic Models and Power BI

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

## Reports Depend on Model Quality

Power BI 報表看起來像是視覺化問題，但實際上常受 semantic model 品質支配。

如果模型本身：

- relationships 不清楚
- 欄位命名不穩定
- measures 到處散落
- 權限邏輯沒有先設計

那報表再漂亮也很難長期維護。

所以「有效的 Power BI 報表」通常不是從畫圖開始，而是先從 model design 開始。

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

### Object-Level Security

OLS 會限制整個 object 的存取，例如：

- 某張 table
- 某個 column

它適合拿來保護比較敏感的欄位或結構，而不只是把資料列做過濾。

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
- RLS 和 OLS 應該被當成分析層治理的一部分，而不是最後才補上的權限開關。
- 如果 lakehouse、warehouse、semantic model 是同一平台內協作，越早把命名、欄位與安全邊界講清楚，後面越省事。

[Back to Data Engineering](README.md)
