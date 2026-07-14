# Feature Engineering Principles

Feature engineering is the process of turning raw data into informative inputs for a model.

## Why It Matters

- Better features often improve performance more than switching algorithms.
- Features determine what information the model can actually use.
- Poor feature design can introduce [leakage](data-leakage.md), noise, or instability.

## Common Principles

- Make features reflect information available at prediction time.
- Prefer meaningful domain-driven transformations over arbitrary complexity.
- Respect the structure of the data: numeric, categorical, text, temporal, grouped.
- Keep transformations reproducible and consistent between training and inference.

## Start with Data Understanding

特徵工程不該從「先做一堆轉換」開始，而是先回答：

- 這份資料是怎麼被收集的
- 欄位代表什麼
- 哪些欄位只是記錄流程副產品
- 分析或預測的目標到底是什麼

如果對資料來源、業務流程或欄位語意沒有基本理解，常常會把無關欄位、洩漏欄位或噪音欄位誤當成有效特徵。

## Feature Engineering Also Includes Dropping Data

很多時候，最重要的特徵工程不是新增欄位，而是先移除沒有價值的資料。

常見該優先檢查的欄位包括：

- auto-generated record id
- 幾乎全為常數的欄位
- 與任務無關的描述欄位
- 合併或 join 後重複出現的欄位

row-level 也要檢查：

- duplicated records
- 明顯格式錯誤的觀測
- 少數極端值是否其實是資料錄入錯誤

如果 duplicate removal 會影響結果，要先定義「哪種欄位組合才算同一筆資料」，不要只機械地刪重。

## Common Examples

- Log-transforming skewed numeric variables
- Extracting day-of-week or month from timestamps
- Creating interaction features
- Aggregating behavior over a past time window
- Building one-row-per-entity basetables for a specific reference date

也常見這些更直接的特徵構造：

- multiplying two numeric features，例如面積 = 長 × 寬
- differencing 或 ratio features
- binning continuous variables into ranges
- 把 count 類欄位轉成 binary presence / absence signal

## Risks

- [Data leakage](data-leakage.md)
- Overly sparse or noisy features
- Unstable encodings for high-cardinality categories
- Features that depend on business rules that later change

## Missing Data Is Part of Feature Engineering

缺值處理不是獨立話題，它本身就是特徵工程的一部分。

常見決策順序是：

1. 先量化缺值有多少、集中在哪些欄位
2. 判斷缺值是否稀少、是否近似隨機
3. 決定要刪除、保留、補值，還是另外做 missingness indicator

補值方式通常包括：

- rule-based: 依 business logic 指定值
- statistics-based: mean、median、mode
- model-based: 用其他特徵預測缺值

真正重要的不是「有沒有補值」，而是補值方式是否合理且能在 production 重現。

## Time Awareness Matters

如果資料帶有時間順序，特徵工程與資料切分都必須尊重時間。

例如：

- 不要用未來資料生成當下可用的特徵
- train / test split 不應任意打散時間序列
- 聚合特徵要確認 window 只使用當下以前的資訊

很多 feature leakage 其實不是模型太複雜，而是時間邏輯被忽略。

## Basetable Thinking Helps

如果你的資料其實來自 event log、transaction log 或 user history，先把問題轉成 `basetable` 往往更清楚。

實務上會先固定：

- prediction unit
- reference date
- feature window
- target window

然後再問每個欄位能不能合法地進入模型。

如果這個步驟沒有做好，後面的補值、編碼、scaling 都只是把錯的資料整理得更整齊而已。

## Practical Rule

Ask whether the feature is informative, available at prediction time, and stable enough to maintain.

## Related Concepts

- [Data Leakage](data-leakage.md)
- [Feature Selection](../preprocessing/feature-selection.md)
- [Categorical Encoding](../preprocessing/categorical-encoding.md)
- [Pipeline Basics](../workflow/pipeline-basic.md)
- [Basetable and Time-Aware Feature Engineering](basetable-and-time-aware-feature-engineering.md)

[Back to Foundations](README.md)
