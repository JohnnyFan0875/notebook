# R Foundations

這個章節整理資料分析工作裡最常反覆用到的 R 基礎。重點不是把語法當成單獨知識點背下來，而是建立一套能處理時間索引、寫出可重用函數、並安全迭代資料結構的工作習慣。

## 建議閱讀順序

1. 先讀資料結構與流程控制：`vectors -> data frames -> lists -> categorical -> control flow -> functions`。
2. 再讀資料整理日常：`datetime -> importing data -> missing data -> tidyverse workflow -> dplyr/tidyr/data.table`。
3. 接著讀可重用與穩定性：`functional programming -> defensive programming -> apply family -> object systems`。
4. 如果工作走向建模，再讀 `explanatory modeling -> tidymodels -> sampling -> statistical functions`。
5. 如果工作偏效能、工程或文字資料，再各自走 `writing efficient R / Rcpp / parallel`、`package development / reporting`、`regex / fuzzy matching / text analysis / scraping / social media`。

## 主題分組

### 語言基礎與資料結構

- [Vectors in R](vectors.md)
- [Data Frames in R](data-frames.md)
- [Lists in R](lists.md)
- [Categorical Data in R](categorical-data.md)
- [Control Flow in R](control-flow.md)
- [Functions in R](functions.md)
- [Date and Time in R](datetime.md)
- [Object-Oriented Programming with S3 and R6](object-oriented-programming-s3-r6.md)
- [SAS to R Mental Model](sas-to-r-mental-model.md)

### 資料整理與匯入

- [Importing Data in R](importing-data.md)
- [Missing Data in R](missing-data.md)
- [Tidyverse Workflow in R](tidyverse-workflow.md)
- [Joining Data with dplyr](joining-data-with-dplyr.md)
- [Data Reshaping with tidyr](data-reshaping-with-tidyr.md)
- [Joining and Reshaping with data.table](data-table-joins-and-reshaping.md)
- [dplyr Programming Patterns](dplyr-programming-patterns.md)

### 函數式思維與程式穩定性

- [Functional Programming with purrr](functional-programming-with-purrr.md)
- [Advanced purrr Patterns](functional-programming-with-purrr-advanced.md)
- [Defensive Programming in R](defensive-programming.md)
- [The apply Family](apply-family.md)

### 建模與統計工作流

- [Explanatory Modeling in R](explanatory-modeling-in-r.md)
- [Modeling with tidymodels](modeling-with-tidymodels.md)
- [Sampling in R](sampling-in-r.md)
- [Statistical Functions in R](statistical-functions.md)
- [Survey Data Analysis in R](survey-data-analysis.md)

### 效能與工程化

- [Writing Efficient R Code](writing-efficient-r-code.md)
- [Rcpp for R Performance](rcpp-for-r-performance.md)
- [Parallel Programming in R](parallel-programming-in-r.md)
- [R Package Development](package-development.md)
- [Reporting with R Markdown](reporting-with-r-markdown.md)

### 文字、網頁與非結構化資料

- [Regular Expressions in R](regular-expressions.md)
- [String Distance and Fuzzy Matching in R](string-distance-and-fuzzy-matching.md)
- [Text Analysis in R](text-analysis.md)
- [Web Scraping in R](web-scraping-in-r.md)
- [Social Media Analysis in R](social-media-analysis.md)

## 建議閱讀方式

- 如果你常在時間欄位轉換、格式解析或日曆欄位提取卡住，先補 [Date and Time in R](datetime.md)。
- 如果你剛接觸 R 的資料結構，先從 [Vectors in R](vectors.md) 與 [Data Frames in R](data-frames.md) 開始。
- 如果你常搞混類別標籤與其底層編碼，補 [Categorical Data in R](categorical-data.md)。
- 如果你需要把不同型別的物件包成同一個分析物件，補 [Lists in R](lists.md)。
- 如果你不確定什麼時候該用 `if`、`for`、`while`，先看 [Control Flow in R](control-flow.md)。
- 如果你的分析腳本開始重複貼上同樣邏輯，先補 [Functions in R](functions.md)。
- 如果你開始碰到 `print()` / `summary()` 的 method dispatch，或需要帶狀態的分析物件，補 [Object-Oriented Programming with S3 and R6](object-oriented-programming-s3-r6.md)。
- 如果你已經會寫基本函數，但常在 list iteration、批次分析或錯誤容忍流程上反覆手寫 loop，補 [Functional Programming with purrr](functional-programming-with-purrr.md)。
- 如果你已經會 `map()`，但開始想整理巢狀 API 資料、封裝 reusable mappers，或把 `partial()` / `compose()` 組成可重用流程，補 [Advanced purrr Patterns](functional-programming-with-purrr-advanced.md)。
- 如果你開始擔心輸入檢查、錯誤訊息、命名規則或腳本穩定性，補 [Defensive Programming in R](defensive-programming.md)。
- 如果你需要在 R 裡連資料庫、讀 API、處理 JSON 或其他統計軟體格式，補 [Importing Data in R](importing-data.md)。
- 如果你在 R 裡常遇到 `NA`、隱藏缺值標記或想追蹤 imputation，補 [Missing Data in R](missing-data.md)。
- 如果你原本比較熟 SAS，想先把 session、物件、pipeline 與 output object 的差異講清楚，補 [SAS to R Mental Model](sas-to-r-mental-model.md)。
- 如果你想把散點圖、`lm()`、`broom` 輸出與模型比較串成一條可讀的 regression workflow，補 [Explanatory Modeling in R](explanatory-modeling-in-r.md)。
- 如果你已經會做基本資料整理，想把切分資料、前處理、模型與評估串成一致的機器學習流程，補 [Modeling with tidymodels](modeling-with-tidymodels.md)。
- 如果你需要在大資料量下做高效 join、查找、批次整併與 reshape，補 [Joining and Reshaping with data.table](data-table-joins-and-reshaping.md)。
- 如果你已經確認 bottleneck 落在少數計算熱點，想把小型函式降到 C++，補 [Rcpp for R Performance](rcpp-for-r-performance.md)。
- 如果你要用 R 抓網頁節點、表格或處理 scraping request 細節，補 [Web Scraping in R](web-scraping-in-r.md)。
- 如果你想在 R 裡實作 random sample、stratified sample 或 bootstrap workflow，補 [Sampling in R](sampling-in-r.md)。
- 如果你需要從 log、半結構化字串或文字欄位裡抽 pattern，補 [Regular Expressions in R](regular-expressions.md)。
- 如果你的資料值不只是格式混亂，還包含 typo、近似拼法或要做 approximate join，補 [String Distance and Fuzzy Matching in R](string-distance-and-fuzzy-matching.md)。
- 如果你想把評論、文件或留言拆成 tokens，做 stop-word 清理、詞典式 sentiment 或 LDA topic modeling，補 [Text Analysis in R](text-analysis.md)。
- 如果你的 R 函數開始跨專案重用，想把文件、依賴與測試一起管好，補 [R Package Development](package-development.md)。
- 如果你要把分析、圖表與文字整成可重跑的正式交付物，補 [Reporting with R Markdown](reporting-with-r-markdown.md)。
- 如果你想用 R 抓 tweet、清理社群文字、做簡單 sentiment 或 retweet network，補 [Social Media Analysis in R](social-media-analysis.md)。
- 如果你拿到 NHANES 這類複雜抽樣資料，不確定 weights、`svymean()` 或 weighted plots 該怎麼用，補 [Survey Data Analysis in R](survey-data-analysis.md)。
- 如果你常在 list、data frame 或矩陣上做重複彙總，最後看 [The apply Family](apply-family.md)。
- 如果你已經懂基本統計概念，但常忘記在 R 裡該用哪個函式，補 [Statistical Functions in R](statistical-functions.md)。

## 工作心法

- R 很擅長向量化運算；只有在狀態需要逐步更新時，才真的需要 loop。
- 當工作對象從 vector 變成 list、巢狀物件或多組參數時，`purrr` 往往比手寫 loop 更容易維持輸出一致。
- 一旦 `purrr` 開始和 predicate、function operators、巢狀 JSON 一起使用，先把資料結構講清楚，比急著寫 `map()` 更重要。
- 文字清理常分兩步：先用 regex 做規則化，再用 string distance 處理剩下的近似錯字。
- 先理解 vector、factor、data frame、list 的差別，後面的 indexing 與 `apply` 才不容易混亂。
- 日期時間與缺失值是分析腳本最常出錯的兩個來源，應該優先建立防呆習慣。
- 當 script 開始變長，防呆、命名一致性與少複製貼上，比再多背幾個函式更重要。
- `apply` 類函數的重點不是「少寫幾行」，而是把資料結構與回傳型別想清楚。
