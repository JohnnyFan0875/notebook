# Excel Data Validation

Excel 的 data validation 不是分析工具，而是資料輸入階段的 quality control。

它的核心價值很直接：

- 阻止明顯不合法的輸入
- 讓每筆資料更一致
- 把 business rules 前移到資料輸入當下

如果資料在進表時就能被限制，後面通常能少掉很多人工清理。

## What It Really Does

可以把 data validation 想成對 cell 輸入加上一層規則：

- 只允許某種資料型別
- 只允許某個範圍
- 只允許清單中的值
- 只在某個公式條件成立時才接受輸入

除此之外，它也不只是「擋錯」：

- 可以加入 input instructions
- 可以設定 custom error messages
- 可以讓工作表更像一個受控的輸入介面

## Why It Matters

data validation 最主要的價值有兩個：

- `data integrity`: 讓資料符合預期結構與規則
- `error reduction`: 降低手動輸入造成的 typo 與不一致

這對收集型工作表特別重要，例如：

- 表單
- 估價工具
- 報價單
- 內部營運台帳
- 手動維護的 reference sheet

## A Good Validation Workflow

實務上可以用這個順序設計：

1. 先定義 business requirements。
2. 把規則翻成可操作的 validation rule。
3. 在 Excel 中實作對應的 validation。
4. 故意輸入 invalid data 做測試。
5. 補齊提示文字與錯誤訊息，讓使用者知道怎麼改。

這個順序很重要，因為很多 validation 失敗，不是 Excel 功能不夠，而是一開始就沒把規則定清楚。

## Common Rule Types

### Numeric Ranges

最常見的是數值上下限。

例如：

- 年份只能在 `2000` 到 `2025`
- `APR` 不能超出公司允許範圍
- 付款期數必須在某個政策範圍內

這類規則很適合防止：

- 少打一個零
- 不合理的百分比
- 超出業務政策的輸入

### Fixed-Length Text

有些欄位的重點不是內容語意，而是格式長度。

例如：

- `VIN` 必須是 `17` 個字元
- 某種 ID 必須固定長度

這種情況常會搭配 `Text Length` 或 custom formula。

### Controlled Choice Lists

當欄位應該只能從固定集合中選值時，dropdown list 很有用。

典型情境：

- maker
- color
- status
- region
- loan type

這能大幅減少：

- 拼字不一致
- 同義詞混用
- 大小寫風格混亂

如果同一欄會被拿來 group、filter 或 pivot，list validation 通常比事後清理划算得多。

### Date / Time Rules

有些欄位不是「有填就好」，而是必須在某個時間邏輯下有效。

例如：

- 日期不能早於今天
- 日期不能晚於某個截止日
- 還款起始日必須晚於簽約日

這類規則常需要 custom formula，而不是只靠基本 date type。

### Formula-Based Rules

當規則和多個欄位有關，或條件比較特製時，可以用 custom formula。

適合：

- APR 依貸款類型有不同範圍
- 某欄必須在另一欄不為空時才能填
- 某個分類只能搭配特定狀態

這時 data validation 真正做的是 enforcement of business logic，而不只是格式檢查。

## User Guidance Matters

很多人只設 validation 規則，卻忘了使用者體驗。

一個比較完整的輸入設計通常包含兩層：

### Input Guidance

在使用者輸入前就告訴他：

- 這格要填什麼
- 可接受的範圍是什麼
- 格式應該長怎樣

這比事後一直跳錯誤訊息更友善。

### Error Messages

custom error messages 不只是提示「你錯了」，而是要說清楚：

- 哪裡錯
- 規則是什麼
- 應該怎麼改

好的錯誤訊息會讓工作表更像工具，而不是陷阱。

## A Business Example Mindset

如果你在做 loan calculator、報價表或申請表，可以先把欄位分成三類：

- `free text but constrained`
- `must choose from list`
- `must satisfy business formula`

例如車貸計算器裡常見的規則：

- `VIN`: must be 17 characters
- `APR`: must stay within realistic or policy-approved bounds
- `term`: must remain within company policy
- `maker` / `color`: should come from controlled lists

這樣設計時，validation 就不再只是 Excel 技巧，而是表單結構的一部分。

## Limits You Should Know

Excel data validation 很有用，但不要把它想得太萬能。

常見限制包括：

- 沒有內建的 duplicates prevention
- 可能被 copy/paste 覆蓋
- 對複雜邏輯支援有限

這代表：

- unique key 檢查常需要額外公式、conditional formatting 或後續 QA
- 不能因為設了 validation 就假設資料一定乾淨
- 對高風險流程，validation 應該只是第一層防線

## Practical Heuristics

- 規則來自 business policy，不是來自你剛好會用哪個 Excel 功能。
- 先想使用者會輸入什麼錯，再決定 validation 怎麼設。
- 對關鍵欄位優先設 validation，不要一開始就追求全表 100% 覆蓋。
- validation 設完之後，一定要故意輸入錯值測試。
- 如果規則太複雜、跨欄依賴很多，考慮改成更結構化的資料收集流程。

## Relation to Data Cleaning

data validation 和 data cleaning 不一樣：

- `validation` 是 prevention
- `cleaning` 是 correction

最理想的狀態不是後面很會清，而是前面就少收錯資料。

所以它在 spreadsheet workflow 裡的角色比較像：

`input guardrail -> cleaner downstream data -> less repair work later`

## Mental Model

可以把 Excel data validation 濃縮成一句話：

它不是讓資料變聰明，而是讓輸入變得更笨也更安全，從而讓整個 workbook 更可靠。
