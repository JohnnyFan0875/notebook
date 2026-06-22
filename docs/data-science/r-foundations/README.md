# R Foundations

這個章節整理資料分析工作裡最常反覆用到的 R 基礎。重點不是把語法當成單獨知識點背下來，而是建立一套能處理時間索引、寫出可重用函數、並安全迭代資料結構的工作習慣。

## Sections

- [Vectors in R](vectors.md)
- [Data Frames in R](data-frames.md)
- [Categorical Data in R](categorical-data.md)
- [Lists in R](lists.md)
- [Date and Time in R](datetime.md)
- [Control Flow in R](control-flow.md)
- [Functions in R](functions.md)
- [The apply Family](apply-family.md)

## 建議閱讀方式

- 如果你常在時間欄位轉換、格式解析或日曆欄位提取卡住，先補 [Date and Time in R](datetime.md)。
- 如果你剛接觸 R 的資料結構，先從 [Vectors in R](vectors.md) 與 [Data Frames in R](data-frames.md) 開始。
- 如果你常搞混類別標籤與其底層編碼，補 [Categorical Data in R](categorical-data.md)。
- 如果你需要把不同型別的物件包成同一個分析物件，補 [Lists in R](lists.md)。
- 如果你不確定什麼時候該用 `if`、`for`、`while`，先看 [Control Flow in R](control-flow.md)。
- 如果你的分析腳本開始重複貼上同樣邏輯，先補 [Functions in R](functions.md)。
- 如果你常在 list、data frame 或矩陣上做重複彙總，最後看 [The apply Family](apply-family.md)。

## 工作心法

- R 很擅長向量化運算；只有在狀態需要逐步更新時，才真的需要 loop。
- 先理解 vector、factor、data frame、list 的差別，後面的 indexing 與 `apply` 才不容易混亂。
- 日期時間與缺失值是分析腳本最常出錯的兩個來源，應該優先建立防呆習慣。
- `apply` 類函數的重點不是「少寫幾行」，而是把資料結構與回傳型別想清楚。
