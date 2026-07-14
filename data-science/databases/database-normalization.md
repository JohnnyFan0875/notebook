# Database Normalization

這篇整理資料庫正規化的核心心智模型。正規化的重點不是把 schema 拆得越碎越好，而是降低冗餘、避免更新異常，讓資料結構更一致、更容易維護。

## Why Normalization Exists

如果同一份事實散落在多個地方重複保存，常見問題會是：

- 同一實體出現多種寫法
- 名稱或屬性變更時要同步改很多列
- 插入新資料時被迫先補不相干欄位
- 刪除某列時意外把重要資訊一起刪掉

例如在 `loan` 表直接放 `bank_name`，又另外有 `bank` 表保存銀行資訊，就容易出現：

- 不同銀行名字撞名
- 銀行改名時多張表不同步
- 一個實體在系統裡沒有穩定主鍵可追蹤

這時通常應該在交易表存 `bank_id`，把描述性資料留在 `bank` 維表。

## Normalization as Dependency Management

可以把正規化想成處理 functional dependency：

- 一個欄位應該依賴哪個 key
- 某個屬性是不是其實描述的是另一個實體
- 同一列內是否混了多個層次的事實

如果欄位依賴的不是整個 key，或依賴另一個非 key 欄位，通常就是 schema 還可以再整理的訊號。

## Key Vocabulary

在談正規化前，先把幾個 key 名詞分清楚：

- superkey：任何能唯一識別一列的欄位集合，即使裡面還塞了多餘欄位
- candidate key：已經 minimal 的 superkey，少任何一個欄位都不再唯一
- primary key：從 candidate key 中實際被選來當主要識別子的那一個
- composite key：由多個欄位一起組成的 key

可以把它想成：

- superkey 重點是「能唯一」
- candidate key 重點是「能唯一，而且沒有冗餘欄位」
- primary key 重點是「系統最後正式採用哪一個」

這些差異在 2NF 特別重要，因為 partial dependency 幾乎都發生在 composite key 上。

## First Normal Form (1NF)

1NF 的核心是欄位值要保持原子性，避免一格裡塞多個值或多個概念。

不理想的設計常見像：

- `full_name` 同時混 `first_name` 和 `last_name`
- 一個欄位用逗號串多個課程、電話或標籤
- 重複欄位如 `phone1`, `phone2`, `phone3`

1NF 的方向通常是：

- 一欄只放一種資料
- 重複值改成多列或獨立關聯表
- 能拆成穩定結構的欄位就拆

例如：

```sql
CREATE TABLE student (
  id         SERIAL PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name  VARCHAR(50) NOT NULL,
  course     VARCHAR(50) NOT NULL,
  home_room  SMALLINT NOT NULL
);
```

這比把姓名、課程資訊混成一格更容易查詢與約束。

## Second Normal Form (2NF)

2NF 要求先滿足 1NF，並且所有非 key 欄位都要完整依賴整個 candidate key，而不是只依賴其中一部分。

這在複合主鍵情境最常出現。

如果一張表的 key 是 `(textbook_id, publisher_id)`，但 `publisher_site` 只依賴 `publisher_id`，那麼把它放在同一張表就會造成 partial dependency。

處理方式通常是把描述 publisher 的欄位拆出去：

```sql
CREATE TABLE publisher (
  id   SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  site VARCHAR(50)
);

CREATE TABLE textbook (
  id           SERIAL PRIMARY KEY,
  name         VARCHAR(100) NOT NULL,
  quantity     SMALLINT NOT NULL DEFAULT 0,
  publisher_id INTEGER REFERENCES publisher(id)
);
```

## Third Normal Form (3NF)

3NF 要求先滿足 2NF，並避免 non-key attribute 依賴另一個 non-key attribute，也就是 transitive dependency。

典型訊號像是：

- `employee` 表裡存 `department_name` 和 `department_location`
- 但其實 `department_location` 是依賴 `department_name`

這代表 department 本身是另一個實體，應該拆成獨立表，再用外鍵關聯。

## Practical Tradeoff

正規化不是唯一目標。分析型系統與 OLTP 系統常有不同取捨：

- 交易系統通常更重視一致性與更新安全，正規化價值高
- 分析系統常為了查詢效率或易用性做部分反正規化
- star schema 本身就是一種為分析而接受冗餘的設計

所以真正問題不是「要不要正規化」，而是：

- 這張表主要服務更新還是查詢
- 冗餘帶來的維護成本是否可接受
- 是否已有穩定 ETL 可以承擔反正規化後果

## Common Anomalies

### Update Anomaly

同一事實出現在多列，修改時容易漏改。

### Insert Anomaly

想新增某個實體，卻因為表設計耦合，必須先補另一個還不存在的資訊。

### Delete Anomaly

刪掉一列業務資料時，連唯一的維表資訊也被一起刪掉。

## Practical Heuristics

- 如果某些欄位總是一起描述另一個實體，考慮拆表
- 如果同一文字描述重複出現很多次，考慮改成 surrogate key + lookup table
- 如果欄位值內含多值清單，先懷疑是否違反 1NF
- 如果某欄位只依賴複合 key 的一部分，先懷疑是否違反 2NF
- 如果欄位描述的是另一個非 key 欄位，先懷疑是否違反 3NF

## Mental Checklist

- 這張表的主鍵到底是什麼
- 每個非 key 欄位依賴的是哪個 key
- 是否混入另一個實體的描述性欄位
- 是否存在 update / insert / delete anomaly
- 這是 OLTP 設計，還是分析型讀取模型
