# Data Preparation in Power BI

在 Power BI 裡，資料準備通常不是報表之前的一段雜務，而是整個 BI workflow 的第一個穩定化步驟。  
如果欄位型別錯、文字值不一致、欄位命名混亂，後面的 model、DAX 與 report 都會變得脆弱。

## A Simple Workflow

在 Power BI Desktop 裡，常見流程可以先想成：

1. connect data
2. open Power Query
3. check data types and column names
4. inspect quality with preview features
5. apply text / numerical / date transformations
6. `Close & Apply`

重點不是做很多 transformation，而是把清理步驟變成可重跑的 recipe。

## What Clean Data Means Here

在 Power BI / Power Query 的脈絡裡，乾淨資料通常至少包含：

- missing values 已被辨識
- typos 與 data entry errors 已被修正
- duplicated data 已被處理
- irrelevant data 被排除
- outliers 已被檢查
- 每個欄位有正確 data type
- column / table names 簡短且可讀

這些條件看起來基礎，但它們會直接影響後面：

- relationship 能不能建立
- measures 結果會不會失真
- visual filters 能不能正常運作

## Power Query as a Repeatable Cleaning Layer

Power Query 的重要性不只在於它能清資料，而是它會把每一步 transformation 保留成 `Applied Steps`。

這代表：

- 你不是手動修一次資料而已
- refresh 時會重新套用同樣步驟
- 清理流程可以被檢查、調整與重跑

這是 Power BI 很重要的工程化特性。  
比起在 Excel 裡手動改值，`Applied Steps` 更接近一條可重現的 preparation pipeline。

## Data Types Come Early

Power Query 會自動推測欄位型別，但這一步不應該完全交給自動判斷。

常見型別包括：

- numerical
- date / time
- text
- logical
- binary

型別如果一開始判錯，後面很容易連鎖出問題：

- date 被當成 text，時間排序與 date functions 都會失效
- 數值被當成 text，無法正確聚合
- categorical code 被當成數值，容易被誤算平均

Tip: 匯入後先確認型別，通常比做任何視覺化還重要。

## Data Preview Features

Power Query 的 `View` ribbon 底下有一組很實用的 preview features：

- `Column distribution`
- `Column quality`
- `Column profile`

它們可以先當成資料檢查儀表板，而不是進階功能。

## Why Preview Matters

data preview 的價值主要有三個：

- 幫你提早看到 errors 與 inconsistencies
- 幫你確認某個 transformation 之後資料變成什麼樣子
- 幫你判斷下一步該做哪種清理

預設 profile 常只基於前 `1000` rows，所以它很適合快速診斷，但不代表一定等於完整資料分布。

## Cleaning Text Columns

文字欄位是最容易把報表和模型搞亂的來源之一。  
Power Query 裡的 clean text 通常意味著：

- 沒有 typo
- 表示方式一致
- capitalization 一致
- 沒有 leading / trailing whitespace
- 沒有 control characters
- 一欄只放一種資訊

最後一點很重要。  
如果一個欄位同時塞 `City, State`、`First Last`、或多段混合訊息，後面做分群、篩選、關聯都會比較痛苦。

## Practical Text Transformations

在 `Transform` ribbon 裡，常用的文字清理包括：

- format / capitalization 調整
- `Trim`
- `Clean`
- split column
- merge columns

其中兩個最值得養成習慣：

- `Trim`: 移除前後空白
- `Clean`: 移除換行、carriage return 等 control characters

如果資料來源很多，`Trim + Clean` 幾乎可以當成文字欄位的預設第一輪處理。

## Cleaning Numerical Columns

數值欄位的清理重點通常不是把數字「變漂亮」，而是確保它們可被可靠地聚合、比較與建模。

常見檢查包括：

- missing values
- obvious errors
- outliers
- precision 是否合理

Power Query 常見的數值 transformation 包括：

- absolute value
- logarithm
- multiply by scalar
- add scalar
- rounding

這些操作通常不是為了炫技，而是為了讓數值更符合業務定義或分析需求。  
例如單位換算、把負號修正為絕對值、或把過度細碎的小數整理成合理精度。

## Working with Date Columns

在 Power Query 裡，date / time 是獨立型別，不只是格式化後的字串。

當欄位型別正確後，常見可用 transformation 包括：

- extract year / quarter / month / week / day
- start or end of year / quarter / month / week
- age extraction

這些操作很常用，因為很多後續分析都依賴時間層次：

- 年 -> 季 -> 月
- cohort / aging
- period-based aggregation

如果日期在 preparation 階段就處理乾淨，後面建立 hierarchy、calendar logic 或 time-based reporting 會順很多。

## Practical Heuristics

- 先修型別與欄位命名，再做複雜 transformation。
- `Applied Steps` 要保持可讀，不要讓清理流程變成黑箱。
- 先用 preview features 找問題，再決定要不要 split、replace、filter 或 recast。
- `Trim` 與 `Clean` 很適合當文字欄位的第一輪標準化。
- 一欄盡量只存一件事，這樣 model 與 filter 才不容易失真。
- date 欄位要盡早轉成真正的 date / time type，不要拖到報表層。

## Mental Model

一句話總結：

Power BI 的 data preparation，可以先理解成用 Power Query 把原始資料轉成 `typed + profiled + transformed + repeatable` 的分析輸入層。
