# Data Modeling Foundations

data modeling 的目標，是先把資料世界中的實體、屬性與關係整理清楚，再決定資料要如何落成 table、如何被分析，以及哪些欄位應該透過 key 串起來。

這件事不是只為了畫圖。建模做得好，後續的資料清理、資料整合、權限設計、查詢邏輯與分析模型都會更穩定。

## Why Data Modeling Matters

- 幫團隊先釐清 business entities 是什麼
- 降低欄位重複、命名混亂與關聯不一致
- 讓後續的 relational model、ER model 與 analytical model 有共同基礎

如果一開始沒有先釐清實體與關係，之後常會出現這些問題：

- 同一個概念被存在多個地方
- 關聯欄位格式不一致，導致 join 不穩
- 下游分析表雖然能查，但語意上其實已經偏掉

## Entities, Attributes, and Relationships

在最基本的資料建模語言裡：

- `entity`: 代表一個可被獨立辨識的對象，例如 customer、order、product
- `attribute`: entity 的描述欄位，例如 customer name、order date、product category
- `relationship`: entities 之間的連結方式，例如 customer places order、order contains product

這個層次的重點不是 SQL，而是先把世界拆成可管理的結構。

## Relationship Cardinality

relationship cardinality 用來描述兩個 entities 之間關聯出現的次數。

常見情況包括：

- `one-to-one`: 一筆資料對應另一筆資料
- `one-to-many`: 一個 entity 可以對應多筆另一方資料
- `many-to-many`: 兩邊都可能對應多筆資料

cardinality 很重要，因為它會直接影響：

- foreign key 應該放在哪一側
- 是否需要 bridge / junction table
- 後續 join 結果會不會被意外放大

## Primary Keys and Foreign Keys

key 的角色，是讓資料表之間的識別與連結變得明確。

### Primary Key

`primary key` 用來唯一識別一筆資料。

一個好的 primary key 通常應該：

- 對每筆記錄唯一
- 盡量穩定，不隨業務欄位頻繁變動
- 讓下游關聯可以清楚指向同一筆資料

實務上常見兩類：

- `natural key`: 直接來自業務系統，例如會員編號、商品代碼
- `surrogate key`: 額外產生的內部識別碼，例如流水號或 UUID

### Foreign Key

`foreign key` 用來表示某筆資料依附或指向另一張表中的主鍵。

它的價值在於：

- 把 relationship 落成可查詢的 table 結構
- 讓資料關聯不是靠欄位名稱猜測，而是有明確連接邏輯
- 幫助團隊追蹤哪些 entity 之間有依賴

## Normalization

normalization 是把資料整理成較少重複、較少異常更新風險的過程：同一個事實不要存在多處、更新不要牽動很多列、刪一筆資料不要順手刪掉其他資訊。它最常用在交易型或上游整合型的 relational design；分析型模型則常在可接受的前提下做部分反正規化。

1NF–3NF、functional / partial / transitive dependency 與 update / insert / delete anomaly 的完整說明見 [Database Normalization](../databases/database-normalization.md)。

## ER Modeling as an Intermediate Design Layer

ER model 的價值，在於它位在 business understanding 和 physical implementation 之間。

它通常幫我們做到三件事：

- 用 entity 與 relationship 把業務概念講清楚
- 把複雜資料拆成較可管理的結構
- 在真正落成資料表前，先檢查 cardinality 與 key design 是否合理

如果把 star schema 視為面向分析消費的下游模型，那 ER / normalized model 比較像是上游結構設計的整理層。

## Normalized Models vs. Analytical Models

normalized relational model 和 dimensional model 不是互斥，而是常常服務不同目標。

- normalized model 比較重視一致性、去重與資料維護
- dimensional model 比較重視查詢理解性、彙總效率與分析消費體驗

很多資料平台會先在上游整理好 entities、keys 與 relationships，再於下游轉成 star schema 或其他分析模型。

## Practical Reminders

- 先釐清 grain、entity 與 relationship，再急著建 table。
- key design 不是實作細節，而是整個模型能不能穩定被 join 的基礎。
- many-to-many 關係若被硬塞進單一欄位，後面通常都要補更痛的清理成本。
- 正規化不是目的本身；它是在一致性與使用便利性之間取得平衡的工具。
- upstream relational model 和 downstream analytical model 常常都需要，只是服務不同階段。

[Back to Data Engineering](README.md)
