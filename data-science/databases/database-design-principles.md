# Database Design Principles

database design 的核心問題不是「這個系統用哪一種 SQL 語法」，而是先回答：資料到底要拿來做什麼。  
同樣一份資料，如果主要用途是支援交易、支援分析、支援共享查詢，設計重點會很不一樣。

## Start With Intended Use

設計資料庫前，先問幾個問題：

- 這套資料主要服務交易，還是分析
- 使用者最常做的是寫入更新，還是聚合查詢
- 查詢結果是給應用程式、分析師，還是報表使用者
- 權限是不是需要分層
- 之後最常被重複使用的 join / filter pattern 是什麼

同一份資料如果 intended use 不同，schema、normalization、view、access control 甚至 DBMS 選擇都會跟著變。

## OLTP vs OLAP

最基本的資料設計分野之一，是分清楚 OLTP 與 OLAP。

| Aspect | OLTP | OLAP |
| --- | --- | --- |
| Purpose | support daily transactions | report and analyze data |
| Design | application-oriented | subject-oriented |
| Data | up-to-date, operational | consolidated, historical |
| Query pattern | simple, frequent reads/writes | complex, aggregate-heavy queries |
| Typical users | many operational users | fewer analytical users |

### OLTP

OLTP 適合：

- 查單筆訂單
- 更新最新交易
- 寫入應用程式互動資料
- 維持業務流程當下狀態

它通常重視：

- 寫入一致性
- transaction safety
- 正規化設計
- 低延遲的單筆或小範圍操作

### OLAP

OLAP 適合：

- 找最忠誠客戶
- 計算最佳利潤商品
- 做跨時間、跨主題的彙總分析
- 支援報表與 BI

它通常重視：

- 聚合查詢效率
- 歷史資料保留
- subject-oriented organization
- 更適合分析的資料形狀，例如 dimensional model

## Schema As Blueprint

schema 可以視為 database 的 blueprint。  
它定義的不只是 table，還包括：

- fields / columns
- relationships
- indexes
- views
- constraints

在 relational database 裡，schema 通常是 schema-on-write：資料寫入前就要符合預先定義的結構。  
這和某些更彈性的系統形成對比，後者更接近 schema-on-read。

### Columns Have Domains

欄位型別不只是儲存格式，也是在定義欄位的 domain，也就是：

- 這個欄位可以接受什麼值
- 可以對它做哪些運算
- 系統要如何一致地儲存它

例如：

```sql
CREATE TABLE students (
  ssn           INTEGER,
  name          VARCHAR(64),
  dob           DATE,
  average_grade NUMERIC(3, 2),
  tuition_paid  BOOLEAN
);
```

這類 attribute constraint 的價值是：

- 避免把日期、文字、數值混用
- 讓資料庫能正確套用比較、排序、聚合與驗證
- 讓 foreign key 與 join 欄位更容易維持一致

如果外鍵和它參照的主鍵型別不一致，通常就是 schema 設計已經開始偏掉的訊號。

## Conceptual vs Logical Modeling

資料設計不是直接跳到 `CREATE TABLE`。  
可以把它拆成至少兩層：

### Conceptual Model

conceptual model 比較接近 business understanding。

重點是：

- 有哪些 entities
- 它們怎麼互相關聯
- 哪些業務概念需要被區分

常見表達方式是 ER diagram。

### Logical Model

logical model 開始把概念翻成結構。

重點是：

- tables
- columns
- relationships
- keys
- schema shape

這一層才會開始落到 relational model、normalized model 或 star schema 等具體資料形狀。

## Relationships and Referential Integrity

關聯式資料庫不是只有把資料拆成很多 table，更重要的是把 table 之間的關係說清楚。

foreign key 的核心意義是：

- 某欄位的值必須對應到另一張表中已存在的 key
- 這個欄位通常應該和被參照欄位有相容的 domain / type
- 它負責保護 referential integrity

例如：

```sql
ALTER TABLE order_items
ADD CONSTRAINT order_items_order_id_fkey
FOREIGN KEY (order_id) REFERENCES orders(id);
```

referential integrity 的重點是：

- 不能插入指向不存在 parent record 的 child record
- 不能隨便刪除仍被 child records 參照的 parent record，除非你明確定義後續行為

### ON DELETE Actions

foreign key 不只是「有沒有關聯」，還包含 parent row 被刪掉時要怎麼辦。

常見選項：

- `NO ACTION` / `RESTRICT`：直接擋下刪除
- `CASCADE`：連 child rows 一起刪
- `SET NULL`：把 child foreign key 設成 `NULL`
- `SET DEFAULT`：把 child foreign key 改成預設值

這些不是單純語法問題，而是業務語意：

- 明細資料是否應跟著主資料一起消失
- 歷史資料是否需要保留但解除關聯
- 系統是否允許 orphan-like 狀態

如果這些問題沒先想清楚，資料庫雖然能建立 relation，但不一定能保住正確的資料生命週期。

## Normalized vs Dimensional Thinking

資料設計常見的兩種方向：

- normalized relational design
- dimensional design

### Normalized Design

比較適合：

- OLTP
- 上游主資料管理
- 一致性高於查詢便利性

它重視：

- 降低 redundancy
- 降低 update anomaly
- 讓資料關係更精確

### Dimensional Design

比較適合：

- OLAP
- BI / reporting
- 穩定的 slicing, dicing, aggregation

它重視：

- fact / dimension 分工
- 查詢容易理解
- 報表與分析消費效率

如果分析是主要用途，常會看到 denormalized schema 與 dimensional modeling。

## Star vs Snowflake

當進入分析模型時，常見兩種形態：

- `star schema`
- `snowflake schema`

### Star Schema

特點：

- fact table 記事件或度量
- dimension table 記描述性欄位
- 查詢較直觀
- 比較容易被 BI 工具與分析師理解

### Snowflake Schema

特點：

- dimension 進一步正規化
- 冗餘較少
- 結構更細
- 查詢與理解成本通常較高

實務上若主要用途是分析與報表，star schema 往往比較自然；若維度本身需要高度去重與結構化維護，snowflake 才比較可能有吸引力。

## Views As Reusable Query Surfaces

view 可以理解成 stored query 所暴露出的 virtual table。

```sql
CREATE VIEW scifi_books AS
SELECT title, author, genre
FROM dim_book_sf
JOIN dim_genre_sf
  ON dim_genre_sf.genre_id = dim_book_sf.genre_id
JOIN dim_author_sf
  ON dim_author_sf.author_id = dim_book_sf.author_id
WHERE dim_genre_sf.genre = 'science fiction';
```

之後可以像查普通 table 一樣查它：

```sql
SELECT *
FROM scifi_books;
```

### Why Views Help

- 把常用 join 邏輯包起來
- 避免重複撰寫相同查詢
- 對使用者提供較友善的資料介面
- 不需要改 physical schema 就能提供新的資料視角

對資料設計來說，view 常是 physical tables 和 end users 之間的緩衝層。

### What Views Are Not

- 不是把資料複製一份
- 不是萬能的效能優化工具
- 不是 schema 設計不良時的永久補丁

如果下游反覆依賴某個很重的 view，可能表示：

- 應該建立更明確的 semantic layer
- 或者該把那段邏輯 materialize 成更正式的分析表

## Access Control Is Part of Design

權限設計不是收尾工作，而是 schema design 的一部分。

需要先想：

- 所有人是否該看同樣資料
- 誰只能讀
- 誰能寫
- 哪些資料應透過 view 暴露而不是直接開放原表

常見語法形式會是：

```sql
GRANT SELECT ON some_view TO analyst_role;
REVOKE INSERT ON raw_table FROM analyst_role;
```

這種做法讓 access model 跟資料責任邊界一致，而不是所有人都直接連到最底層資料表。

## Roles

role 的設計重點不只是建立 user，而是建立權限集合。

一個 role 可能代表：

- 某類使用者
- 某個職能群組
- 某種可操作範圍

好的做法通常是先想角色，再把 user 掛上角色，而不是針對每個 user 單獨散發權限。

## Choosing a DBMS

資料庫選型通常也應該回到 intended use：

- real-time relational structured data 常偏 OLTP
- historical analytical workloads 常偏 OLAP
- raw / heterogeneous / large-scale log data 可能更適合 data lake 或其他 schema-on-read 型態

沒有單一 DBMS 對所有場景都最佳。  
重點不是找「最強資料庫」，而是找最適合目前 workload 和 governance 需求的系統。

## Practical Design Questions

- 這份資料主要是拿來更新，還是拿來分析
- query pattern 是單筆交易，還是跨表聚合
- 需要 normalized model 還是 dimensional model
- 哪些邏輯適合落在 table，哪些適合落在 view
- 哪些使用者應該直接看 raw tables，哪些只該看 curated view
- 權限應該綁在 user，還是 role
- 這個系統需要 schema-on-write 還是 schema-on-read 的彈性

## Common Mistakes

- 還沒定義使用情境，就急著決定 schema 形狀
- 用 OLTP 結構直接承擔大量分析查詢
- 把 view 當成所有設計問題的補丁
- 權限直接發給 individual users，沒有角色層
- 想同時優化所有 workload，結果每一種都不夠好

## Related Topics

- [Database Normalization](./database-normalization.md)
- [PostgreSQL](./postgresql.md)
- [Business Analysis in SQL](./business-analysis-in-sql.md)
- [Data Modeling Foundations](../data-engineering/data-modeling-foundations.md)
- [Dimensional Modeling and Star Schema](../data-engineering/dimensional-modeling-and-star-schema.md)
